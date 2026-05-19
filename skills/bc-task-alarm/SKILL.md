---
name: bc-task-alarm
description: >
  Brian Charrette's all-in-one daily "alarm clock" that surfaces everything due or overdue across ALL sources in one clean report.
  Checks: HubSpot tasks (overdue + due today + upcoming 7 days), email-queue.json for stuck/hung sequence sends,
  and Cowork scheduled tasks for anything that fired or missed. Delivers a prioritized action list — not a data dump.
  ALWAYS use this skill when Brian says anything like: "what's due", "what do I have due", "task check", "alarm",
  "daily check", "what's on my plate", "what's overdue", "morning check", "show my tasks", "what needs attention",
  "what's pending", "catch me up", "what's stuck", "anything overdue", "check my sequences", "sequence check",
  "what emails are stuck", "run my alarm", "bc-task-alarm", or any variation of wanting a consolidated view of
  everything that needs his attention today. Trigger even if he just says "alarm" or "what do I have" with no other context.
---

# bc-task-alarm — Daily Due / Overdue Alarm

Pull everything that needs Brian's attention right now into one clean, prioritized report. Three sources, one output.

---

## Sources to Check (run all three in parallel)

### 1. HubSpot Tasks
Use `mcp__df6165ad-*__search_crm_objects` with `objectType: "tasks"`.

**Overdue** — Pull tasks where `hs_timestamp` is BEFORE today's date and status is NOT_STARTED or IN_PROGRESS, owned by Brian (owner ID: 213536174). Use a timestamp filter like `LT: <today at 00:00 UTC as epoch ms>`. Cap at 25 results, sorted ascending by `hs_timestamp` (oldest first).

**Due Today** — Same filters but `hs_timestamp` BETWEEN today 00:00 UTC and today 23:59 UTC. Cap at 25.

**Upcoming (next 7 days)** — `hs_timestamp` BETWEEN tomorrow 00:00 UTC and 7 days from now. Cap at 15 for the preview. Don't show full details — just a count + list of subjects.

Properties to request: `["hs_task_subject", "hs_task_body", "hs_task_status", "hs_task_type", "hs_timestamp", "hs_task_priority"]`

**Handling the backlog:** Brian has a large task backlog (thousands of old tasks). For overdue tasks older than 30 days, show a count only — don't list them individually. Focus the detail view on tasks overdue within the last 30 days.

### 2. Email Queue (Stuck Sequence Sends)
Read the queue file:
`C:\Users\MINI OSI RIG\OneDrive - OSI Hardware\Documents\Claude\OSI-Brain\email-queue.json`

Use the Read file tool directly on the Windows path first (this is the preferred method in Cowork — it has direct file system access). If the Read tool fails, fall back to the SharePoint MCP (`mcp__3d844455-*__sharepoint_search` for `email-queue.json`, then `read_resource`). If still unreachable, note "email queue unavailable — OneDrive sync may be paused" in the output and continue.

**What to flag:**
- `status: "pending"` entries where `sendDate` is today or earlier — these are emails that should have fired but haven't yet (may be waiting for the next send window, or genuinely stuck)
- `status: "error"` entries — these are hard failures that need manual attention
- `status: "paused-*"` entries — paused sequences that may need a decision

**Group by prospect** so Brian sees "3 pending emails for JD Cheek / Vertafore" rather than a flat list of 15 individual entries.

For pending entries that are due TODAY (not past due) — these are likely just waiting for the next send window (11am/12pm/1pm/2pm/3pm/4pm PT). Note this so Brian knows they're normal, not stuck.

For pending entries where `sendDate` was YESTERDAY or earlier — flag these as potentially stuck. Show the prospect name, company, which email number in the sequence, and the scheduled date.

### 3. Cowork Scheduled Tasks
Use `mcp__scheduled-tasks__list_scheduled_tasks`.

**Overdue / Missed** — Tasks where `nextRunAt` is in the past (before current time) AND `enabled: true`. These fired or should have fired.

**Due Today** — Tasks where `nextRunAt` falls within today.

**Coming up (next 3 days)** — Brief list only (subject + date/time), no details.

For one-time tasks that have already fired (`nextRunAt` is past and no future run), note them as "completed/fired" rather than "stuck" — they ran as expected.

For recurring tasks (have a cron pattern), show next fire time only.

---

## Cross-Computer Note
Cowork scheduled tasks are **local to this machine**. If Brian set up a task on another computer, it won't appear here unless it was written to the OneDrive queue or HubSpot. The email queue IS cross-machine (OneDrive-synced), so sequence sends from either computer show up. HubSpot tasks are cloud and always current.

---

## Output Format

Lead with a **quick summary line** — something like:
`"3 overdue HubSpot tasks | 2 stuck queue emails | 1 scheduled task missed — here's what needs your attention:"`

Then sections in priority order:

---

### OVERDUE (action needed)

#### HubSpot — Overdue Tasks (last 30 days)
For each task:
```
[TYPE] Subject — Contact/Company
Due: [date] ([X days overdue])
Note: [hs_task_body excerpt if helpful, 1 line max]
```

If there are tasks older than 30 days, add a line like:
`+ 47 older overdue tasks in HubSpot (pre-May 2025) — consider a bulk-complete sweep`

#### Email Queue — Stuck Sends
For each stuck prospect:
```
[SEQUENCE STUCK] Prospect Name / Company
Email #X was due [date] — still pending
```

#### Scheduled Tasks — Missed
```
[TASK MISSED] Task description
Was scheduled for [date/time]
```

---

### DUE TODAY

#### HubSpot Tasks
Same format as above, no "days overdue" field.

#### Email Queue — Sending Today
```
[SENDING TODAY] Prospect Name / Company
Email #X — scheduled for today, next send window will pick it up
```

#### Scheduled Tasks — Today
```
[SCHEDULED TODAY] Task description — fires at [time]
```

---

### UPCOMING (next 7 days)
Keep this brief — just a count and a flat list:
```
HubSpot: 8 tasks due
- Subject 1 (due Mon)
- Subject 2 (due Tue)
...
Scheduled tasks: 3 firing
- Task A (Mon 9am)
- Task B (Wed 11am)
```

---

### TAIL LINE
End with one of these (pick whichever fits):
- If everything is clean: `"All clear — nothing overdue. [N] tasks due today."`
- If there are issues: `"Flagged [N] items. Start with the stuck queue entries — those need manual attention."`

---

## Tone & Style
- Direct, no filler. Brian knows what he's looking at.
- Use the emoji flags ([OVERDUE], [STUCK], etc.) as quick scannable markers — but don't go overboard.
- If a section is empty, say so in one line and move on. Don't skip sections silently.
- No em dashes, no en dashes — use a comma or period instead.
- Keep the whole output scannable in under 30 seconds.

---

## Error Handling
- If HubSpot returns an error or times out, note it and continue with the other sources.
- If the email queue is unreachable, note "email queue offline (OneDrive sync may be paused)" and continue.
- If scheduled tasks fail, note it and continue.
- Never abort the whole report because one source fails.
