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

Group by prospect — strip the -email-N suffix to get the prospect key (e.g. brett-baker-lippert).

For each prospect, build a status list:
- **Fired:** enabled: false AND fireAt date is in the past
- **Upcoming:** enabled: true AND fireAt date is in the future
- **Overdue:** enabled: true AND fireAt date is in the past (should have fired but did not)

---

## Step 2: Flag Overdue Tasks

Any task where enabled: true and fireAt is in the past is a failure. It should have sent but did not.

Flag each one:
> OVERDUE: [Name] at [Company] — Email [N] was due [date/time]. Still enabled. Check Cowork Scheduled Tasks sidebar.

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
   b. Cancel all remaining tasks — set enabled: false via mcp__scheduled-tasks__update_scheduled_task
   c. Update HubSpot strategy note on the contact: prepend "EMAIL BOUNCED [date] — all remaining sequence tasks canceled. Verify email address before re-enrolling."
   d. Add to bounce report
4. If no HubSpot contact found for the bounced address, flag it for Andy to investigate manually

---

## Step 4: Check HubSpot for Replies — Auto-Pause on non-OOO

For each prospect who had an email task fire in the last 48 hours:

Search HubSpot for recent inbound activity on that contact:
- Inbound emails logged in the last 7 days
- Notes added since their last outbound email
- Meetings booked

### Out-of-office filter — applied first
If the reply body contains any of these phrases, skip entirely. Do not pause. Do not flag.

Keywords: "out of office", "on vacation", "away from the office", "will return", "maternity leave", "parental leave", "extended leave", "on PTO", "back on [date]"

### Any other reply — auto-pause the remaining sequence
If the reply is not an OOO, treat it as human engagement and auto-pause the remaining queue entries for that prospect immediately. No waiting for Andy's confirmation. No lost momentum while Andy is asleep.

Steps:
1. Read `C:\Claude-Brain\email-queue.json`.
2. Find every entry where the prospectName matches AND status is `"pending"`.
3. Change each of those entries' status from `"pending"` to `"paused-reply-[YYYY-MM-DD]"`. Write the file back.
4. Update the HubSpot strategy note on the contact — prepend this line:
   > REPLY RECEIVED [date] — sequence auto-paused. Andy to review and decide whether to resume or cancel.
5. Add to the monitor output in the PAUSED ON REPLY section.

Special case: if the reply is specifically a shipping address tied to a swag or sample request, still auto-pause. Flag it distinctly in the summary as SHIPMENT REQUESTED so Andy knows to ship before doing anything else.

### Resuming or canceling a paused sequence
When Andy says "resume [name]": flip those entries back to `"pending"` and adjust send dates if needed so the next send is at least 2 business days out from today.

When Andy says "cancel [name]": change to `"canceled-reply"` and leave them.

---

## Step 5: Emails Sending Today

List every email task scheduled to fire today (any time remaining today).

Format: Name | Company | Email N | Subject | Send time

This gives Andy a heads-up on what's going out today so he can make his calls before 3 PM.

---

## Step 6: Output Summary

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

SENDING TODAY:
[List: Name | Company | Email N | Subject | Time]
[If none: No emails scheduled for today.]

STATUS: [ALL CLEAR / ISSUES FOUND -- see above]
---

If everything is clean, end with: "All clear. [N] sequences running."

---

## Step 7: Update Excel Tracker — Unenrolled Tab

File: Claude-Brain/prospects-tracker-new.xlsx, Tab 3 "Unenrolled"

After every monitor run, append a row for anyone unenrolled during this run. This includes:
- Hard bounces (auto-canceled by the monitor)
- Auto-paused on reply (by the monitor — Step 4)
- Manual cancellations Andy requested ("cancel sequence for [name]")
- Reply-based cancellations Andy confirmed

Columns: Name | Company | Date Unenrolled | Reason | Emails Sent | Emails Remaining | Notes

**Reason values:**
- Hard bounce — bad email address
- Hard bounce — domain blocked
- Auto-paused — reply received
- Auto-paused — shipment requested
- Replied — Andy canceled
- Connected — Andy canceled
- Andy request

**Emails Sent / Remaining:** count from the scheduled tasks that fired vs. were still enabled at cancellation time.

If no one was unenrolled this run, skip this step entirely.

---

## Rules

- Never modify tasks except to cancel on a confirmed hard bounce, auto-pause on a non-OOO reply, or Andy's explicit instruction.
- Never flag out-of-office auto-replies as actionable. Never pause on OOO.
- Auto-pause (not cancel) on non-OOO replies. Andy decides whether to resume or cancel after reviewing.
- If Outlook login screen appears, note it and skip all Outlook-dependent checks.
- If scheduled tasks API returns an error, note it in the summary and move on.
- Keep the summary under 30 lines if possible. Andy reads this at 11 AM and needs to act on it fast.
