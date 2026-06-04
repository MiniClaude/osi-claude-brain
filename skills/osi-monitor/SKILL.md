---
name: osi-monitor
description: >
  Daily sequence monitor for OSI Global outreach. Runs at 11 AM weekdays. Checks all active
  scheduled email tasks, scans Outlook inbox for bounces, cross-references HubSpot for replies,
  auto-cancels remaining tasks on confirmed hard bounces, AUTO-PAUSES the remaining sequence on
  any non-OOO reply (including shipment address confirmations), flags anything needing Andy's
  attention, and outputs a clean daily summary. Trigger: "run monitor", "sequence status",
  "what's in flight", "check sequences", "resume [name]", "cancel [name]", or automatically via
  scheduled task at 11 AM weekdays.
---

> **SYNC NOTE:** This skill exists in two locations: `C:\Claude-Brain\skills\osi-monitor\` (Git-versioned, source of truth, backed up at github.com/Drrewdy/Claude-Brain) and the local Cowork `.claude/skills/` mount. Any edits must go into `C:\Claude-Brain\skills\` and be pushed to GitHub. If returning after days away, run `git pull` first to get the latest, then check the local Cowork copy and re-install the `.skill` file if the source has drifted.

# OSI Sequence Monitor

## Your job

Check everything running, catch anything broken, fix it automatically, tell Andy what you did. Output a clean summary. Fast.

Read this entire skill before producing any output.

---

## 🚨 SALES NAV RULE, NON-NEGOTIABLE, APPLIES EVERYWHERE IN THIS SKILL

**Any time Email 1's send date changes for any reason, stranded fix, overdue fix, ordering fix, Andy request, any reason at all, the HubSpot "Sales Nav -- Send connection request" task for that prospect MUST be rescheduled to match the new Email 1 date. This is not optional. This is not a secondary step. Do it in the same write pass.**

Procedure (applies every single time E1 date changes):
1. Find the contact in HubSpot by email address.
2. Search tasks on that contact where `hs_task_subject` contains "Sales Nav -- Send connection request" AND `hs_task_status = NOT_STARTED`.
3. Exactly one match: update `hs_timestamp` to the new E1 date at 20:00 UTC (4pm ET).
4. Already COMPLETED: leave it. Flag in summary: "Sales Nav connect already sent on [old date], LinkedIn arm fired ahead of rescheduled E1."
5. Zero or multiple NOT_STARTED matches: do NOT auto-update. Flag for Andy to handle manually. Still fix the email queue.

Never reschedule E1 without also addressing this task. If the HubSpot lookup fails, note it and move on, but do not skip the email queue fix.

---

## Step 1: Pull All Active Scheduled Tasks

Use mcp__scheduled-tasks__list_scheduled_tasks to get all scheduled tasks.

Filter for OSI outreach email tasks. Identify by task ID format: [firstname]-[lastname]-[company-slug]-email-[N].

Group by prospect, strip the -email-N suffix to get the prospect key (e.g. brett-baker-lippert).

For each prospect, build a status list:
- **Fired:** enabled: false AND fireAt date is in the past
- **Upcoming:** enabled: true AND fireAt date is in the future
- **Overdue:** enabled: true AND fireAt date is in the past (should have fired but did not)

---

## Step 2: Full Queue Sweep, Auto-Fix All Overdue Entries

Read `C:\Claude-Brain\email-queue.json`. Scan every entry where `status: "pending"` AND `sentAt: null` AND `sendDate` is in the past. There is no lookback ceiling. If an entry is 10 days overdue, it still gets fixed.

**E1 overdue:** handled by Step 5 (stranded sequence auto-fix). Skip here, do not double-process.

**E2-6 overdue:** auto-fix immediately.

For each overdue E2-6 entry:
1. **New send date AND send time:** determine the new date and time together.
   - Send windows (ET): 11:00, 12:00, 13:00, 14:00, 15:00, 16:00.
   - Get current ET hour (convert from UTC: ET = UTC - 4 in summer, UTC - 5 in winter).
   - **Next unfired window** = smallest window hour that is strictly greater than the current ET hour. E.g., monitor runs at 11:45 ET → next window = 12:00. Monitor runs at 13:20 ET → next window = 14:00. Monitor runs at 15:10 ET → next window = 16:00.
   - If a next unfired window exists AND current ET time is before 15:30 → reschedule to **today**, set `sendTime` to that window (e.g. "16:00"). Do NOT keep the entry's original sendTime; the original window has already passed.
   - If current ET time is 15:30 or later (only the 4pm window remains and there is not enough time for Andy to act on pre-flight risks) → reschedule to the **next business day**. Keep the entry's original `sendTime` (it will hit its normal window the next day).
2. **Respread remaining entries:** calculate the offset in business days between the original sendDate and the new date. Push every subsequent pending entry for that prospect forward by the same offset, preserving original cadence gaps exactly.
3. **Audit trail:** add `rescheduled` field to each updated entry: `"From <old-date> to <new-date> on <today> (overdue-auto-fix)"`. Atomic write only: write to `email-queue.json.tmp`, then `os.replace(tmp, original)`.

Report each fix in the summary under AUTO-FIXED OVERDUE: Name | Company | Email N | was due [old date] | rescheduled to [new date] | E[N+1]-6 respread.

---

## Step 3: Scan Outlook Inbox for Bounces

**Lookback window:** read `C:\Claude-Brain\monitor-last-run.json` to get the timestamp of the last successful monitor run. Search Outlook for bounces received since that timestamp. If the file is missing, or if the last run was more than 7 days ago, use a 7-day lookback. This ensures nothing is missed if the monitor skips days.

Navigate to https://outlook.office.com in Chrome.

If login screen appears, stop and note it in the summary. Do not proceed with Outlook checks.

Go to Inbox. Search for emails received since the last run (see above) where sender contains: mailer-daemon OR postmaster, OR subject contains: undeliverable OR delivery failed OR returned mail.

For each bounce found:
1. Extract the original recipient email address from the bounce notification
2. Search HubSpot for a contact with that email address
3. If found:
   a. Identify all remaining enabled scheduled tasks for that prospect (task IDs matching [firstname]-[lastname]-[company-slug]-email-*)
   b. Cancel all remaining tasks, set enabled: false via mcp__scheduled-tasks__update_scheduled_task
   c. Update HubSpot strategy note on the contact: prepend "EMAIL BOUNCED [date], all remaining sequence tasks canceled. Verify email address before re-enrolling."
   d. Add to bounce report
4. If no HubSpot contact found for the bounced address, flag it for Andy to investigate manually

---

## Step 4: Check HubSpot for Replies, Auto-Pause on non-OOO

**Lookback window:** use the same last-run timestamp from `monitor-last-run.json` (see Step 3). Check for replies received since that timestamp, not just 48 hours. If file missing, use 7 days.

For each prospect who had an email task fire since the last monitor run:

Search HubSpot for recent inbound activity on that contact:
- Inbound emails logged in the last 7 days
- Notes added since their last outbound email
- Meetings booked

### Out-of-office filter, applied first
If the reply body contains any of these phrases, skip entirely. Do not pause. Do not flag.

Keywords: "out of office", "on vacation", "away from the office", "will return", "maternity leave", "parental leave", "extended leave", "on PTO", "back on [date]"

### Any other reply, auto-pause the remaining sequence
If the reply is not an OOO, treat it as human engagement and auto-pause the remaining queue entries for that prospect immediately. No waiting for Andy's confirmation. No lost momentum while Andy is asleep.

Steps:
1. Read `C:\Claude-Brain\email-queue.json`.
2. Find every entry where the prospectName matches AND status is `"pending"`.
3. Change each of those entries' status from `"pending"` to `"paused-reply-[YYYY-MM-DD]"`. **Atomic write only:** write the modified queue to `C:\Claude-Brain\email-queue.json.tmp`, then `os.replace(tmp, original)`. Never write directly to the live file. A mid-write crash on the live file leaves the queue truncated and the next email-sender fire fails to parse JSON. This has happened (2026-04-29).
4. Update the HubSpot strategy note on the contact, prepend this line:
   > REPLY RECEIVED [date], sequence auto-paused. Andy to review and decide whether to resume or cancel.
5. Add to the monitor output in the PAUSED ON REPLY section.

Special case: if the reply contains a shipping address (street number, city, state, zip, or explicit "ship to" / "send to" / "address is" language), treat it as a SHIPMENT REQUESTED reply. Still auto-pause the sequence. Then do all of the following automatically:

**1. Determine product to send.**
Check the queue entry for this prospect's Email 1 `id` suffix to find the sequence type from the strategy note or queue metadata:
- `Sample-Offer Network` or any Pain-Led optics/DWDM sequence → **SFPs**
- `Sample-Offer Server` or any Pain-Led DIMM/compute sequence → **DIMMs**
- Unknown / cannot determine → default to **SFPs**, flag in summary

**2. Write a row to the Swag tab in `Claude-Brain/prospects-tracker-new.xlsx`.**
Tab name: "Swag". Create it if it doesn't exist. Columns:
Name | Company | Title | Email | Date Reply Received | Shipping Address | Product to Send | Date Shipped | Tracking # | Follow-up Status

Fill in everything known now. Leave Date Shipped, Tracking #, and Follow-up Status blank for Andy to complete.

**3. Create two HubSpot tasks on the contact.**

Task 1, Ship task:
- Subject: `Ship swag to [First Name] at [Company]`
- Due: today
- Type: `TODO`
- Owner: Andy (213536174)
- Body: `[First Name] replied with a shipping address. Send [SFPs/DIMMs]. Address: [extracted address].`

Task 2, Follow-up task:
- Subject: `Follow up with [First Name] re: swag shipment`
- Due: 4 business days from today (so it fires after delivery)
- Type: `TODO`
- Owner: Andy (213536174)
- Body: `Check in after swag shipment. Ask if the [SFPs/DIMMs] arrived and if they had a chance to test them.`

**4. Log in the summary under SHIPMENT REQUESTED:** Name | Company | product | address | "Ship task + follow-up task created in HubSpot. Row added to Swag tab."

If the HubSpot task creation fails, flag it but still write the Swag tab row. If the Excel write fails, flag it but still create the HubSpot tasks. Never block the auto-pause on a downstream write failure.

### Resuming or canceling a paused sequence
When Andy says "resume [name]": flip those entries back to `"pending"` and adjust send dates if needed so the next send is at least 2 business days out from today. **Atomic write only** (`.tmp` + `os.replace`), never direct.

When Andy says "cancel [name]": change to `"canceled-reply"` and leave them. **Atomic write only**.

🚨 **HARD RULE, every write to `email-queue.json` or `overnight-candidates.json` is atomic.** Read full file, modify in memory, write to `<file>.tmp`, then `os.replace(tmp, file)`. Never `open(file, 'w')` directly. A mid-write crash on the live file leaves it truncated and the next reader fails. We have hit this twice on 2026-04-29 and it cost hours. No exceptions.

---

## Step 5: Stranded Sequences, Detect and Auto-Fix

A sequence is "stranded" when Email 2 or later is queued in `pending` but the matching Email 1 was never actually sent (status still `pending`, sentAt null). This happens when a send window misfires (sender skipped, scheduler outage, validator failure). Email 2's subject is `RE: …`, so if the sender fires it before E1 goes out, it lands as an out-of-thread fresh email and looks broken to the prospect.

### Detection
Read `C:\Claude-Brain\email-queue.json`. For each prospect with any pending entry, check whether their Email 1 entry (the `-1` id suffix) has `status: pending` AND `sentAt: null` AND a `sendDate` in the past. If yes, the whole sequence is stranded.

### Auto-fix, no decision required

Do not ask Andy what to do. Auto-reschedule immediately.

**New E1 date and send time:** E1 always uses the 4pm (16:00 ET) window.
   - If current ET time is before 15:30 → reschedule E1 to **today**, `sendTime: "16:00"`.
   - If current ET time is 15:30 or later → reschedule E1 to the **next business day**, `sendTime: "16:00"`.

**Respread E2-6:** calculate the business-day offset between the original E1 date and the new E1 date. Push every subsequent entry (E2-6) forward by that same offset, preserving the original cadence gaps exactly.

**Audit trail:** add a `rescheduled` field to each updated queue entry: `"From <old-date> to <new-date> on <today> (stranded-sequence auto-fix)"`. Atomic write only: write to `email-queue.json.tmp`, then `os.replace(tmp, original)`. Never write directly to the live file.

**🚨 CRITICAL: also reschedule the Sales Nav connection request task in HubSpot.** The LinkedIn connection request is tied to E1's date. If E1 moves, the task must move with it or the LinkedIn arm fires out of sync with the email arm.

For each rescheduled prospect:
- Find the contact in HubSpot by email address.
- Search for tasks on that contact where `hs_task_subject` contains "Sales Nav -- Send connection request" AND `hs_task_status = NOT_STARTED`.
- If exactly one match: update its `hs_timestamp` to the new E1 date at 20:00 UTC (4pm ET).
- If COMPLETED already: leave it. Flag in the summary: "Sales Nav connect already sent on <old date>, LinkedIn arm fired ahead of rescheduled E1."
- If zero matches or multiple NOT_STARTED matches: do NOT auto-update. Flag for Andy to handle manually.

**Report in the summary:**
> AUTO-FIXED STRANDED: [Name] | [Company] | E1 moved from [old date] to [new date] | E2-6 respread | Sales Nav task moved to [new date]

Never reschedule the queue without also addressing the Sales Nav task. Skipping that step silently breaks the cadence.

---

## Step 5.1: Ordering Sweep, Fix E2+ Scheduled Before E1

After Steps 2 and 5, do a pass over all pending entries. For each prospect, check whether any E2-6 entry has the same `sendDate` as E1 AND a `sendTime` that is earlier in the day than E1's `sendTime` (e.g. E2 at 11am, E1 at 4pm, same day, wrong order).

**Auto-fix:** keep E1 where it is. Push E2 to the next business day at 11am. Respread E3-6 from there using the original cadence gaps.

Atomic write. Add `rescheduled` audit field to each changed entry: `"From <old> to <new> on <today> (ordering-fix)"`.

Report under AUTO-FIXED ORDERING: Name | Company | E2 moved from [date 11am] to [new date] | E3-6 respread.

**🚨 If E1's date also changed as part of this fix, apply the Sales Nav rule at the top of this skill immediately.**

---

## Step 5.2: Company Gap Sweep, No Two Prospects at Same Company Same Day

After all queue fixes in Steps 2, 5, and 5.1, scan all pending entries and group by company. If two or more prospects at the same company have a pending entry on the same `sendDate`, there is a conflict.

**Auto-fix:** keep the entry with the earlier `addedDate` on its current date. Push the later-added entry forward one business day. If that day also has a conflict, push again. Repeat until clear.

Atomic write. Add `rescheduled` audit field: `"From <old> to <new> on <today> (company-gap-fix)"`.

Report under AUTO-FIXED COMPANY GAP: Name | Company | moved from [date] to [new date] | conflict with [other prospect name].

---

## Step 5.3: Cadence Integrity Check

After all reschedules in Steps 2, 5, 5.1, and 5.2, do a final pass on every prospect's pending entries. Verify the gap between each consecutive pair (E1-E2, E2-E3, E3-E4, E4-E5, E5-E6) is at least 1 business day.

If any gap is zero or negative (two entries on the same day or out of order after compounding fixes), push the later entry forward until the gap is at least 1 business day and run the company gap check again.

Atomic write. Report any corrections under AUTO-FIXED CADENCE: Name | Company | which pair was compressed | fix applied.

---

## Step 5.4: Sales Nav Task Audit, Every E1 Going Out Today

For every prospect with a pending Email 1 (`-1` id suffix) scheduled for today's 4pm window:

1. Find the contact in HubSpot by email address.
2. Search for ALL tasks on that contact where `hs_task_subject` contains "Sales Nav -- Send connection request".
3. Three cases:

   **Case A, Task found AND status is COMPLETED:** All good. Connection request already sent. No action needed.

   **Case B, Task found AND status is NOT_STARTED:** The email-sender gate will hold this E1 at 4pm and push it to tomorrow. Flag immediately as a pre-flight risk:
   - Risk type: `li-task-pending`
   - Message: `LI connection request not sent. Email-sender gate WILL hold E1 at 4pm and reschedule to tomorrow unless you send the connection request first.`
   - Recommended action: `Send Sales Nav connection request now, or let the gate push it.`
   - List under PRE-FLIGHT RISKS, not SALES NAV TASKS CREATED.

   **Case C, No task found:** Create the task now. Fields:
   - Subject: `Sales Nav -- Send connection request to [First Name] [Last Name]`
   - Due date: today
   - Type: `TODO`
   - Owner: Andy (HubSpot owner ID 213536174)
   - Body: `Day 1 connection request. Email 1 goes out at 4pm today.`
   - Report under SALES NAV TASKS CREATED: Name | Company | task created for today.

4. If the HubSpot contact lookup fails, flag it: Name | Company | contact not found, Sales Nav task could not be verified, check manually.

This runs every day before the pre-flight risk check. No E1 should go out without Andy knowing whether the connection request has been sent.

---

## Step 5.5: Pre-Flight Risks (run before listing today's sends)

For every queue entry firing TODAY, run a series of checks against HubSpot signal at the same company. Anything flagged is surfaced in the PRE-FLIGHT RISKS section of the summary so Andy can swap or hold before the 4 PM batch.

### Pre-flight checks per prospect

For each prospect with a pending entry sending today:

**Check 1, Email pattern mismatch.**
- If the entry has `emailResolution: "dominant-pattern"` or `"manual-required"` → flag. Andy verifies before send.
- If entry has no `emailResolution` field (queued under old skill version) → run the resolver from `knowledge/email-pattern-resolver.md` and flag any pattern mismatch against the verified company pattern.

**Check 2, Recent replies anywhere at the company.**
Search HubSpot for any contact whose `company` matches AND `hs_email_last_reply_date >= today - 7 days`. If yes → flag: someone at the company is engaged. Andy may want to coordinate or hold.

**Check 3, Recent bounces at the company.**
Search HubSpot for any contact whose `company` matches AND `hs_email_bounce > 0` with `hs_email_last_send_date >= today - 30 days`. If yes → flag: company has known bad addresses. Verify our `to:` isn't one.

**Check 4, Recent opens / multiple reads.**
Search HubSpot for any contact at the company whose `hs_email_open > 0` and `hs_email_last_open_date >= today - 14 days`. Multiple opens of recent OSI sends from the same company may signal interest worth knowing about before adding noise. Note in pre-flight, don't auto-hold.

**Check 5, Unverified employer.**

Verification is per-prospect, not per-company. Never blanket-flag everyone at the 5 unverified-batch companies, that wastes Andy's time on prospects he's already cleared.

Order of checks for each queue entry:

1. **Queue entry tag (fast path):** if the entry has `employerVerified: "<date> <source>"` → skip the flag entirely. Verified.

2. **Contact note (durable path):** if no queue tag, search HubSpot for any note associated with the contact whose body contains `EMPLOYER VERIFIED` or `EMPLOYER VERIFICATION`. If found → verified. Skip the flag. Optionally back-fill the queue entry's `employerVerified` field from the note's date so the fast path catches it next time.

3. **Strategy note explicit verification line:** the qualification skill writes `SOURCE: [Path A, LinkedIn full read]` or `[Path B, ZoomInfo + web-search verification, EMPLOYER VERIFICATION: [source + date]]` into the strategy and fit note. If the contact's strategy note has either of those lines → verified.

4. **Fallback (only if all above missing):** if the company appears in the 5-company unverified-batch list from CLAUDE.md (S&P Global, OEC Fiber, Fidelity Communications, Vero Networks, Midcontinent), AND none of the above verification signals are present → flag as `employer-unverified`. Recommended action: `Verify on LinkedIn or cancel`.

This way Andy verifies once per prospect (manual LinkedIn check or qualification skill writes the strategy-note line) and never sees that prospect flagged again.

**Check 6, `hs_additional_emails` mismatch.**
For each prospect, pull the contact's `hs_additional_emails`. If the queue entry's `to:` is in that list (i.e. we're sending to a known alt) → flag. Andy may have intended the primary.

### Output format

```
PRE-FLIGHT RISKS, review before 4 PM:
[If any:
  - [risk-type] Name | Company | reason | recommended action
  ...]
[If none: All pre-flight checks clean.]
```

Examples of risk-type tags: `pattern-mismatch`, `dominant-pattern-only`, `manual-verify`, `recent-reply-co`, `recent-bounce-co`, `recent-opens-co`, `employer-unverified`, `alt-email-target`, `li-task-pending`.

Keep recommendations to 5-10 words: `Swap to john.lubeck@`, `Hold, verify employer`, `Confirm primary vs alt`, etc.

---

## Step 5.6: Weekly Validator Audit (Mondays only)

On the Monday fire only, run a validator audit pass over the last 7 days of `sent` queue entries to catch drift. Skip on every other weekday. The audit catches the case where someone hand-edited a queue entry, or where a stale skill version queued a non-compliant body before the validator was wired in.

```python
import sys
sys.path.insert(0, r'C:\Claude-Brain\scripts')
from validate_email import audit_queue_file
import datetime

# Run only on Mondays.
if datetime.date.today().weekday() == 0:
    findings = audit_queue_file(
        queue_path=r'C:\Claude-Brain\email-queue.json',
        days_back=7,
    )
    if findings:
        # Surface in the daily summary AND log to overnight-run-log.md
        with open(r'C:\Claude-Brain\overnight-run-log.md', 'a', encoding='utf-8') as f:
            f.write(f"\n\n## Weekly validator audit, {datetime.date.today().isoformat()}\n")
            f.write(f"Found {len(findings)} sent entry/entries with rule violations:\n\n")
            for finding in findings:
                f.write(f"- **{finding['prospect']}** at {finding['company']} ({finding['id']}) sent {finding['sendDate']}:\n")
                for v in finding['violations']:
                    f.write(f"  - [{v['rule']}] {v['detail']}\n")
```

If `findings` is non-empty, surface a `WEEKLY VALIDATOR AUDIT` section in the daily summary listing each violating entry. This is informational only, the emails already shipped. The point is to show Andy the drift so he can fix the upstream skill that produced the bad body.

If `findings` is empty, the daily summary line reads: `Weekly validator audit: 7 days clean.`

On non-Monday fires, this step is silent.

---

## Step 6: Emails Sending Today

List every email task scheduled to fire today (any time remaining today).

Format: Name | Company | Email N | Subject | Send time

This gives Andy a heads-up on what's going out today so he can make his calls before 3 PM.

---

## Step 7: Output Summary

Format exactly as below. Keep it short.

---
OSI SEQUENCE MONITOR -- [Day, Date] -- 11 AM
---

SEQUENCES IN FLIGHT: [N] prospects enrolled

BOUNCES AUTO-CANCELED: [N]
[If any: Name | Company | bounced date | tasks canceled]
[If none: None.]

PAUSED ON REPLY: [N]
[If any: Name | Company | reply date | emails paused | "Resume or cancel?"]
[If none: None.]

SHIPMENT REQUESTED: [N]
[If any: Name | Company | product | address | HubSpot ship task due today | follow-up task due [date] | Swag tab updated]
[If none: None.]

AUTO-FIXED OVERDUE: [N]
[If any: Name | Company | Email N | was due [old date] | rescheduled to [new date] | remaining respread]
[If none: None.]

AUTO-FIXED STRANDED: [N]
[If any: Name | Company | E1 moved from [old date] to [new date] | E2-6 respread | Sales Nav task moved]
[If none: None.]

AUTO-FIXED ORDERING: [N]
[If any: Name | Company | E2 moved from [same-day] to [new date] | E3-6 respread]
[If none: None.]

AUTO-FIXED COMPANY GAP: [N]
[If any: Name | Company | moved from [date] to [new date] | conflict with [other prospect]]
[If none: None.]

AUTO-FIXED CADENCE: [N]
[If any: Name | Company | compressed gap fixed between [EN] and [EN+1] | new dates]
[If none: None.]

SALES NAV TASKS CREATED: [N]
[If any: Name | Company | task created for today]
[If none: All E1s today have Sales Nav tasks.]

PRE-FLIGHT RISKS: [N]
[If any: [risk-type] Name | Company | reason | recommended action]
[If none: All pre-flight checks clean.]

SENDING TODAY:
[List: Name | Company | Email N | Subject | Time]
[If none: No emails scheduled for today.]

STATUS: [ALL CLEAR / ISSUES FOUND -- see above]
---

If everything is clean, end with: "All clear. [N] sequences running."

---

## Step 7.5: Write Last-Run Timestamp

After producing the summary output, write `C:\Claude-Brain\monitor-last-run.json` with the current UTC timestamp:

```json
{"lastRun": "2026-05-20T18:15:00Z", "status": "success"}
```

Atomic write (`.tmp` + `os.replace`). This file is what Steps 3 and 4 use on the next run to know how far back to look. If the monitor errors out before this step, the file is not written, which means next run will use the 7-day fallback, safe behavior.

---

## Step 8: Update Excel Tracker, Unenrolled Tab

File: Claude-Brain/prospects-tracker-new.xlsx, Tab 3 "Unenrolled"

After every monitor run, append a row for anyone unenrolled during this run. This includes:
- Hard bounces (auto-canceled by the monitor)
- Auto-paused on reply (by the monitor, Step 4)
- Manual cancellations Andy requested ("cancel sequence for [name]")
- Reply-based cancellations Andy confirmed

Columns: Name | Company | Date Unenrolled | Reason | Emails Sent | Emails Remaining | Notes

**Reason values:**
- Hard bounce, bad email address
- Hard bounce, domain blocked
- Auto-paused, reply received
- Auto-paused, shipment requested
- Replied, Andy canceled
- Connected, Andy canceled
- Andy request

**Emails Sent / Remaining:** count from the scheduled tasks that fired vs. were still enabled at cancellation time.

If no one was unenrolled this run, skip this step entirely.

---

## Rules

- Never modify tasks except to cancel on a confirmed hard bounce, auto-pause on a non-OOO reply, or Andy's explicit instruction.
- Never flag out-of-office auto-replies as actionable. Never pause on OOO.
- Auto-pause (not cancel) on non-OOO replies. Andy decides whether to resume or cancel after reviewing.
- **🚨 SALES NAV RULE, see the prominent callout at the top of this skill. Any time E1's date changes for any reason, the HubSpot Sales Nav connection request task moves with it. No exceptions. No "I'll flag it for Andy." Fix it in the same pass.**
- Auto-fix everything: overdue entries, stranded sequences, ordering violations, company gap conflicts, cadence compression. Report what was fixed. Do not ask for permission first.
- Never reschedule the queue without also addressing the Sales Nav task. Skipping it silently breaks the LinkedIn arm of the cadence.
- If Outlook login screen appears, note it and skip all Outlook-dependent checks.
- If scheduled tasks API returns an error, note it in the summary and move on.
- Keep the summary under 30 lines if possible. Andy reads this at 11 AM and needs to act on it fast.
