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

Check everything running, catch anything broken, flag anything Andy needs to act on. Output a clean summary. Fast.

Read this entire skill before producing any output.

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

## Step 2: Flag Overdue Tasks

Any task where enabled: true and fireAt is in the past is a failure. It should have sent but did not.

Flag each one:
> OVERDUE: [Name] at [Company], Email [N] was due [date/time]. Still enabled. Check Cowork Scheduled Tasks sidebar.

Do not attempt to resend automatically. Flag only.

---

## Step 3: Scan Outlook Inbox for Bounces

Navigate to https://outlook.office.com in Chrome.

If login screen appears, stop and note it in the summary. Do not proceed with Outlook checks.

Go to Inbox. Search for emails received in the last 48 hours where sender contains: mailer-daemon OR postmaster, OR subject contains: undeliverable OR delivery failed OR returned mail.

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

For each prospect who had an email task fire in the last 48 hours:

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

Special case: if the reply is specifically a shipping address tied to a swag or sample request, still auto-pause. Flag it distinctly in the summary as SHIPMENT REQUESTED so Andy knows to ship before doing anything else.

### Resuming or canceling a paused sequence
When Andy says "resume [name]": flip those entries back to `"pending"` and adjust send dates if needed so the next send is at least 2 business days out from today. **Atomic write only** (`.tmp` + `os.replace`), never direct.

When Andy says "cancel [name]": change to `"canceled-reply"` and leave them. **Atomic write only**.

🚨 **HARD RULE, every write to `email-queue.json` or `overnight-candidates.json` is atomic.** Read full file, modify in memory, write to `<file>.tmp`, then `os.replace(tmp, file)`. Never `open(file, 'w')` directly. A mid-write crash on the live file leaves it truncated and the next reader fails. We have hit this twice on 2026-04-29 and it cost hours. No exceptions.

---

## Step 5: Stranded Sequences, Detect and Repair

A sequence is "stranded" when Email 2 or later is queued in `pending` but the matching Email 1 was never actually sent (status still `pending`, sentAt null). This happens when a send window misfires (sender skipped, OneDrive migration, scheduler outage). Email 2's subject is `RE: …`, so if the sender ever fires it, it lands as an out-of-thread fresh email and looks broken to the prospect.

### Detection
Read `C:\Claude-Brain\email-queue.json`. For each prospect with any pending entry, check whether their Email 1 entry (the `-1` id suffix) has `status: pending` and `sentAt: null` AND a `sendDate` in the past. If yes, the whole sequence is stranded.

### Surface to Andy
List each stranded prospect in the monitor summary under a dedicated **STRANDED SEQUENCES** section, before the daily send list. For each one:
- Name | Company | E1 was due [date] | E2+ scheduled but blocked

Offer Andy three options: (a) reschedule E1 to a future weekday and respread E2-6 forward, (b) cancel all remaining entries, (c) Andy sends E1 manually then I respread E2-6.

### When rescheduling, REQUIRED steps
If Andy picks reschedule (option a or c):

1. Update the queue entry for E1 to the new sendDate/sendTime. Push E2-6 forward by the same business-day offset to preserve the original cadence. Add a `rescheduled` audit field on each updated entry: `"From <old> to <new> on <today> (<reason>)"`.

2. **🚨 CRITICAL, also reschedule the Sales Nav connection request task in HubSpot.** The prospect's Day-1 LinkedIn connection request task is tied to the original E1 date. If E1 moves, the connection task moves with it, otherwise the LinkedIn touch fires before the email arm and the cadence breaks.

   For each rescheduled prospect:
   - Find the contact in HubSpot by email address.
   - Search for tasks associated with that contact where `hs_task_subject` contains "Sales Nav -- Send connection request" AND `hs_task_status = NOT_STARTED`.
   - If exactly one match: update its `hs_timestamp` to the new E1 datetime (use the same time-of-day as the new E1 send window, e.g. 4pm ET = 20:00 UTC).
   - If COMPLETED already: leave it alone but flag in the summary as "Sales Nav connect already sent on <old date>, connection arm fired ahead of new E1 date".
   - If multiple NOT_STARTED matches or none: do NOT auto-update. Flag for Andy to handle manually.

3. Confirm in the monitor output:
   > Rescheduled E1-E6 for [Name]. Sales Nav connect task moved to [new date].

Never reschedule the queue without also addressing the Sales Nav task. Skipping step 2 silently breaks the cadence.

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

Examples of risk-type tags: `pattern-mismatch`, `dominant-pattern-only`, `manual-verify`, `recent-reply-co`, `recent-bounce-co`, `recent-opens-co`, `employer-unverified`, `alt-email-target`.

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
[If any: Name | Company | reply date | address | "Confirm shipment"]
[If none: None.]

OVERDUE TASKS: [N]
[If any: Name | Company | Email N | was due date]
[If none: None.]

STRANDED SEQUENCES: [N]
[If any: Name | Company | E1 was due [date] | E2+ blocked | needs decision]
[If none: None.]

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
- **Whenever Email 1 is rescheduled (stranded-sequence repair or any other reason), the matching Sales Nav connection request task in HubSpot must be moved to the same date.** Never reschedule the email arm without addressing the LinkedIn arm. See Step 5 for the procedure.
- If Outlook login screen appears, note it and skip all Outlook-dependent checks.
- If scheduled tasks API returns an error, note it in the summary and move on.
- Keep the summary under 30 lines if possible. Andy reads this at 11 AM and needs to act on it fast.
