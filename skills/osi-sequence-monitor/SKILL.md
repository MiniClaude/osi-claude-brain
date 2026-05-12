---
name: osi-sequence-monitor
description: >
  Monitor all active OSI Global outreach sequences — check task status, flag issues, and surface
  HubSpot replies. ALWAYS use this skill when Brian says "check my sequences", "sequence status",
  "what sequences are running", "any overdue emails", "who's enrolled", "did anyone reply",
  "check my outreach", "what tasks are pending", "sequence monitor", or any variation of wanting
  to see the health of his active outreach campaigns. Produces a clean status report with action items.
---

# OSI Sequence Monitor

Pulls all active outreach tasks, groups them by prospect, checks for issues, and flags anyone
who has replied in HubSpot so Brian knows when to cancel remaining tasks.

---

## Step 1: Pull All Scheduled Tasks

Call `mcp__scheduled-tasks__list_scheduled_tasks` to get every task.

Filter for outreach sequence tasks by matching the naming pattern:
`[firstname]-[lastname]-[company-slug]-email-[N]`

Parse each matching task into:
- **Prospect key**: firstname + lastname + company (e.g., "scott-warren-dhl")
- **Email number**: the trailing digit (1 through 7)
- **Status**: enabled or disabled
- **Fire date**: the `fireAt` timestamp (convert to Pacific time for display)
- **Last run**: `lastRunAt` if present

Group all tasks by prospect key to build one record per enrolled contact.

---

## Step 2: Classify Each Task

For every task, apply this logic:

**SENT** — disabled AND `lastRunAt` is present (fired and auto-disabled)

**UPCOMING** — enabled AND `fireAt` is in the future

**OVERDUE** — enabled AND `fireAt` is in the past (should have fired but didn't — something went wrong)

**ORPHANED** — disabled but `lastRunAt` is null (was disabled manually before it fired — may mean email was sent another way, like Email 1 sent manually)

Note: Email 1 in most sequences will show as ORPHANED because Brian sends it immediately via Outlook, then the task gets disabled. That is expected behavior, not an error. Flag it as "Sent manually" rather than an issue.

---

## Step 3: Build the Per-Prospect Summary

For each enrolled prospect, produce a record:

```
Prospect: [Full Name] — [Company]
Sequence: 7-email / 28-day cadence
─────────────────────────────────────────
Email 1  [date]   Sent manually ✓
Email 2  [date]   SENT ✓  (or UPCOMING / OVERDUE / ORPHANED)
Email 3  [date]   UPCOMING — fires Apr 25 @ 9AM PT
Email 4  [date]   UPCOMING — fires Apr 27 @ 9AM PT
Email 5  [date]   UPCOMING — fires Apr 29 @ 9AM PT
Email 6  [date]   UPCOMING — fires May 3 @ 9AM PT
Email 7  [date]   UPCOMING — fires May 13 @ 9AM PT
─────────────────────────────────────────
Issues:  [none — or list any flags]
```

---

## Step 4: Check HubSpot for Replies

For each enrolled prospect, search Outlook for recent inbound email activity from their address.

Use `mcp__3d844455-4e1c-4f20-8802-b789afae873f__outlook_email_search` with:
- `sender`: the prospect's email address
- `afterDateTime`: the date Email 1 was sent (approximate from task creation dates)

If any inbound email is found from that address:
- Flag the prospect as **REPLIED**
- Note the date and subject of the reply
- Add an action item: "Cancel remaining tasks for [Name] — they replied on [date]"

If no reply is found, mark as **No reply yet**.

---

## Step 5: Flag Issues

Scan all tasks and flag any of the following:

- **OVERDUE** — a task whose fireAt has passed but is still enabled. Action: investigate why it didn't fire, then either re-arm or cancel.
- **DUPLICATE** — two enabled tasks for the same prospect + email number. Action: disable the duplicate.
- **REPLIED but still active** — a prospect replied but remaining tasks are still enabled. Action: cancel remaining tasks and follow up personally.
- **Missing tasks** — a sequence has gaps (e.g., Email 2 and 4 exist but Email 3 is missing). Flag the gap.
- **Orphaned Email 1 task still enabled** — if a task named `*-email-1` is still enabled after today (it should have been disabled or never created after the skill update). Disable it.

---

## Step 6: Build the Report

Produce a clean summary in the chat. Use this structure:

---

### OSI Outreach Sequence Monitor
*[Date and time of report]*

**Active Sequences: [N]**
**Total Pending Tasks: [N]**
**Overdue Tasks: [N]**
**Replies Detected: [N]**

---

#### [Prospect Name] — [Company]
[Per-prospect block from Step 3, with reply status appended]

---

#### [Next Prospect Name] — [Company]
[Same structure]

---

### Action Items
1. [Most urgent issue first — e.g., "Cancel remaining tasks for X — they replied on Apr 14"]
2. [Next issue]
3. [etc.]

*If no issues: "All sequences are running clean. No action needed."*

---

## Step 7: Offer Next Steps

After delivering the report, ask Brian:

"Want me to cancel any tasks, re-arm anything overdue, or kick off a new sequence for anyone?"

---

## Notes on Task Naming

The standard task ID format is: `[firstname]-[lastname]-[company-slug]-email-[N]`

Some older tasks may use slightly different formats (e.g., `-email-4a`, `-email-4b` from early Scott Warren tasks). Parse these best-effort and group them under the same prospect. Email 4a and 4b both count as part of the Email 4 slot.

---

## Tone

Keep the report tight and scannable. Brian doesn't need prose — he needs a status board.
Use ✓ for clean, ⚠ for warnings, ✗ for errors that need immediate action.
