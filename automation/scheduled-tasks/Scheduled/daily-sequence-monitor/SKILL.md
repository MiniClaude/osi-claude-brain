---
name: daily-sequence-monitor
description: Daily morning check of all active OSI outreach sequences — flags overdue tasks, scheduling collisions, orphaned sequences, and any replies from prospects.
---

You are running the daily OSI Global outreach sequence monitor for Brian Charrette (bc@osihardware.com). Execute the following steps and deliver a clean status report in chat.

---

## STEP 1: Pull All Scheduled Tasks

Call `mcp__scheduled-tasks__list_scheduled_tasks` to get every task.

Filter for outreach sequence tasks by matching the naming pattern: `[firstname]-[lastname]-[company-slug]-email-[N]`

Parse each task into:
- Prospect key (e.g. "scott-warren-dhl")
- Email number (1–7)
- Status: enabled or disabled
- Fire date (convert UTC to Pacific time for display)
- Last run: `lastRunAt` if present

Group by prospect key.

---

## STEP 2: Classify Each Task

- **SENT** — disabled AND `lastRunAt` present
- **UPCOMING** — enabled AND `fireAt` is in the future
- **OVERDUE** — enabled AND `fireAt` is in the past (did not fire — investigate)
- **ORPHANED** — disabled, `lastRunAt` is null. If it's Email 1, label "Sent manually ✓" (expected). If it's Email 2+, flag it.

---

## STEP 3: Check for Replies

For each active prospect, search Outlook for inbound emails using `mcp__3d844455-4e1c-4f20-8802-b789afae873f__outlook_email_search`:
- Search by the company domain (e.g. `hexion.com`, `trugreen.com`, etc.)
- Use `afterDateTime` of approximately 30 days ago
- If any reply is found: flag prospect as REPLIED and note date + subject

Common domains to check based on current enrollees: hexion.com, trugreen.com, moderna.com, modernatx.com, constellationenergy.com, synergyfibernet.com, ssctech.com, graphicpkg.com, chartindustries.com, emerson.com, crosscountrymortgage.com, gft.com — update this list based on whoever is actually enrolled.

---

## STEP 4: Flag Issues

Scan for:
- **OVERDUE** — fireAt passed, task still enabled. Action: investigate.
- **DUPLICATE** — two enabled tasks for same prospect + email number.
- **REPLIED but active** — prospect replied, remaining tasks still enabled. Action: cancel remaining tasks, follow up personally.
- **Scheduling collision** — Email N and Email N+1 fire same day within minutes of each other (common with Email 4/5). Flag and recommend rescheduling.
- **Email 1 still enabled** — should have been disabled after manual send. Flag as urgent — risk of duplicate automated send.
- **Entire sequence orphaned** — all tasks disabled with no lastRunAt. Was this intentional? Flag for Brian to investigate.

---

## STEP 5: Deliver the Report

Use this format in chat:

---
### OSI Sequence Monitor — [Today's Date]
**Active Sequences: N | Pending Tasks: N | Firing Today: N | Replies: N**

#### [Prospect Name] — [Company]
```
Email 1   —        Sent manually ✓
Email 2   May 4    SENT ✓
Email 3   May 11   UPCOMING
...
Issues:   None  (or describe any flags)
```

### Action Items
1. [Most urgent first]
2. ...
*If clean: "All sequences running clean. No action needed."*

---

## STEP 6: Offer Next Steps

Ask Brian: "Want me to cancel any tasks, fix any collisions, or kick off a new sequence?"

---

## Notes
- Today's date is available via bash if needed: `date`
- All times display in Pacific (PT)
- Email 1 orphaned = expected behavior (sent manually via Outlook)
- Keep the report tight and scannable — use ✓ for clean, ⚠ for warnings, ✗ for urgent issues
