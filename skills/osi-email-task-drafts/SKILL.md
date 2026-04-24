---
name: osi-email-task-drafts
description: Auto-draft reply emails for every HubSpot email task that is due today or overdue for Andy. For each task, identifies the associated contact, reads the FULL HubSpot engagement history (meeting notes, emails, calls), checks for a fresh external hook via one targeted web search, and drafts a thread-matched reply in Andy's voice. Drafts are written into the task's notes field so Andy can review and send. Skips outreach-sequence auto-tasks (generic "Send follow-up email" with empty body) — those are handled by osi-outreach-sequence. Trigger on "run email tasks", "draft my email tasks", "write drafts for email tasks", "do my follow-ups", or when Andy asks you to go through email tasks due.
---

> **SYNC NOTE:** This skill exists in two locations: `C:\Claude-Brain\skills\osi-email-task-drafts\` (Git-versioned, source of truth, backed up at github.com/Drrewdy/Claude-Brain) and the local Cowork `.claude/skills/` mount. Any edits must go into `C:\Claude-Brain\skills\` and be pushed to GitHub. If returning after days away, run `git pull` first to get the latest, then check the local Cowork copy and re-install the `.skill` file if the source has drifted.

# OSI Email Task Drafts

Fully automated draft-generator for Andy's HubSpot email tasks. Run this whenever Andy says "run email tasks" (or equivalent). It sweeps all email tasks due today or overdue, pulls the current state of each contact's relationship from HubSpot engagements, writes thread-matched drafts directly into the HubSpot task notes, and reports back.

---

## 🚨 Critical drafting rules

### Rule 1 — Ignore the task title. Read the history.

**Do NOT use the task subject/title as drafting material.** Task titles are often months stale. The subject tells you WHICH contact to draft for — nothing more.

### Rule 2 — READ the full engagement history. Strictly.

Andy's words: *"READ THE FUCKING OLDER EMAILS, CALLS AND MEETINGS. STRICT, SEE WHAT IS HAPPENING."*

Pull 15 each of EMAIL / CALL / NOTE and 10 MEETING_EVENT records for the contact. Then **call `get_crm_objects` on each and read the full body text end-to-end** — not titles, not snippets, not just the 3 most recent. Also pull 5 most recent company-level engagements for colleague context.

Every draft must reference **at least 2 specifics** (named products, standards, projects, named partner-side engineers, prior commitments) pulled directly from what you read. If you can't find 2 specifics, do NOT invent them — write the thin-context fallback.

### Rule 3 — HubSpot for specifics, plus ONE fresh-hook web search per contact.

HubSpot engagement history is where specifics come from (products, projects, commitments, named people). In addition, run exactly ONE targeted web search per contact before drafting, to surface a fresh 30-day external hook (company news, earnings, exec change, acquisition, buildout, product launch). If the search returns something real, weave it into the opener. If it returns nothing or generic PR fluff, ignore it and proceed. Do NOT run multiple searches per contact, do NOT chase down second-order results, and do NOT use Outlook search, LinkedIn, or ZoomInfo as drafting sources. The fresh-hook search is additive to HubSpot; it does not replace the engagement history read.

If the contact has no engagement history in HubSpot AND no fresh external hook surfaces, write the thin-context fallback and flag for manual review.

### Data sources (in order of usefulness for specifics)

- NOTE objects — Teams / Zoom meeting transcripts and summaries. **Often the richest source of technical specifics** (product families, standards, requirements, named engineers at partners).
- EMAIL objects — threads logged to HubSpot via Outlook integration. Read direction to understand who said what.
- CALL objects — call history bodies often contain disposition notes and next-step commitments.
- MEETING_EVENT objects — calendar metadata; less detail than NOTEs but useful for timeline.

---

## When to trigger

- "run email tasks"
- "draft my email tasks" / "draft email tasks"
- "write drafts for my follow-ups"
- "do my email follow-ups"
- "go through my email tasks"
- "email task drafts"

Also after the morning monitor when Andy's ready to work through follow-ups.

---

## Scope (default)

**Included:**
- Andy's email tasks (ownerId `196669355`) that are `NOT_STARTED` with `hs_timestamp <= end of today` (due today OR overdue)
- Custom tasks with specific subjects

**Excluded:**
- Generic `"Send follow-up email"` tasks with empty `hs_task_body` — these are from `osi-outreach-sequence` and already have pre-scheduled Outlook drafts.

**Overwrite rule:** Tasks that already have a draft in `hs_task_body` are NOT excluded. The skill always produces a fresh draft and overwrites whatever is there. Previous drafts (auto or manual) will be replaced. Andy's expectation: the draft in the task is always the current one, built from the latest HubSpot history and today's fresh-hook search. If Andy wants to preserve a specific draft, he sends the email (or marks the task complete) before re-running the skill.

---

## Execution plan

### Step 1 — Pull tasks

Andy's `ownerId` is `196669355`. Today's date comes from `<env>`.

```
search_crm_objects(
  objectType: "TASK",
  filterGroups: [{
    filters: [
      { propertyName: "hubspot_owner_id", operator: "EQ", value: "196669355" },
      { propertyName: "hs_task_status", operator: "EQ", value: "NOT_STARTED" },
      { propertyName: "hs_task_type", operator: "EQ", value: "EMAIL" },
      { propertyName: "hs_timestamp", operator: "LTE", value: "<today end-of-day UTC>" }
    ]
  }],
  properties: ["hs_task_subject", "hs_task_body", "hs_timestamp", "hs_task_priority", "hubspot_owner_id"],
  sorts: [{ propertyName: "hs_timestamp", direction: "ASCENDING" }],
  limit: 100
)
```

### Step 2 — Filter to drafting queue

- **Draft queue:** every task whose subject is NOT exactly "Send follow-up email". Body content does not matter — empty bodies get a fresh draft, and existing drafts get overwritten with a fresh draft.
- **Skip — sequence:** subject = "Send follow-up email" AND empty body (osi-outreach-sequence tasks). These have pre-scheduled Outlook drafts already; leave them alone.

Report counts in the opening message: `drafted (fresh) | drafted (overwrote previous) | skipped (sequence)`.

### Step 3 — Dispatch parallel subagents

Divide the draft queue into 4–5 batches of ~8–10 tasks. Dispatch `general-purpose` subagents in parallel (single message, multiple Agent calls) with the prompt in Step 4.

### Step 4 — Subagent task-drafter prompt

Give each agent this prompt (substitute the batch's task list):

> You are drafting email reply content for Andy McLean (andy@osiglobal.com) at OSI Global — IT hardware / maintenance / optics. Today is {today's date}.
>
> **🚨 CRITICAL RULE: Do NOT use the task subject/title as drafting material.** Task titles are often outdated. The subject only tells you which task to work on. Draft only from current-state HubSpot engagements.
>
> **For each task:**
>
> 1. `get_crm_objects` objectType="TASK", taskId — get task details (you need the body to check for existing drafts, not the subject for drafting context).
>
> 2. Find associated contact: `search_crm_objects` objectType="CONTACT", filter `associatedWith: [{objectType: "tasks", operator: "EQUAL", objectIdValues: [taskId]}]`. Properties: firstname, lastname, email, jobtitle, company, phone.
>
> 3. **🚨 STRICT: READ THE FULL HISTORY — not just metadata, not just the most recent few.** Pull the full set of HubSpot engagements for this contact. Associated-with searches on the contact:
>    - `search_crm_objects` objectType="EMAIL", sort by `-hs_createdate`, limit **15**. Then `get_crm_objects` on the full set with properties `["hs_email_subject", "hs_email_text", "hs_email_direction", "hs_email_from_email", "hs_email_to_email", "hs_createdate"]`. **Read every body** end-to-end. Do not skim.
>    - `search_crm_objects` objectType="CALL", sort by `-hs_createdate`, limit **15**. Then `get_crm_objects` with properties `["hs_call_title", "hs_call_body", "hs_call_disposition", "hs_call_direction", "hs_createdate", "hs_call_duration"]`. **Read every call-log body** — disposition + notes together.
>    - `search_crm_objects` objectType="NOTE", sort by `-hs_createdate`, limit **15**. Then `get_crm_objects` with `["hs_note_body", "hs_createdate"]`. **Read every note body** — these often contain Teams / Zoom meeting transcripts and summaries with the most useful technical specifics.
>    - `search_crm_objects` objectType="MEETING_EVENT", sort by `-hs_createdate`, limit **10**. Then `get_crm_objects` with `["hs_meeting_title", "hs_meeting_body", "hs_meeting_start_time", "hs_createdate", "hs_internal_meeting_notes"]`. **Read every meeting body**.
>
>    If the contact is associated with a company, also pull the 5 most recent engagements on the COMPANY record (via `associatedWith` with `objectType: "companies"`) — these often surface context from colleagues that's relevant to the target contact.
>
> 4. **Run ONE fresh-hook web search.** Search the web (via WebSearch or workspace web_fetch) with query: `"[Company name] news [current month] [current year]"`. Score the top results:
>    - Real news (acquisition, merger, exec hire, earnings, product launch, buildout, partnership, outage): capture the one-line summary + source URL and use it as the opener hook in the draft.
>    - Generic PR fluff, award posts, charity drives, job listings: ignore.
>    - Nothing recent: skip and proceed with HubSpot specifics only.
>
>    ONE search per contact. Do not run a second search, do not pivot keywords, do not chase results. If the first search does not surface a usable hook, move on. Do NOT run `outlook_email_search`, LinkedIn, or ZoomInfo.
>
> 5. **Before drafting, extract a "specifics inventory" from HubSpot history + the fresh hook (if found).** List, for yourself:
>    - Named products / model families (e.g., SAR-Hm/Hmc, ACX5448, Nutanix, VxRail)
>    - Technical standards / specs (e.g., IEC 61850, 10G SR, port density requirements)
>    - Project / initiative names (e.g., Nokia pilot, Dallas lab visit, HP/Cisco rightsizing, Thanksgiving data center build)
>    - Named colleagues at the target or partner (e.g., "Chris at Nokia engineering", "Bashar in procurement")
>    - Specific prior offers / commitments (e.g., "shadow-quote in 24 hours", "advance overnight replacement")
>    - Open questions or unanswered asks from the last contact message
>    - Fresh external hook from the 30-day news search (if one surfaced)
>
>    If your inventory has **2+ specifics** (HubSpot history + fresh hook both count), you can write a full substantive draft weaving them in. If it has fewer, write the shorter thin-context fallback + ⚠️ flag — do NOT invent specifics.
>
> 6. **Draft a substantive 3–5 paragraph reply in Andy's voice** that weaves in **at least 2 specifics from your inventory**. Match the formality/length/tone of the most recent real reply from the contact. NEVER draft from the task title — it is stale reference only.
>
> 7. Write to `hs_task_body` via `manage_crm_objects` updateRequest, `confirmationStatus: "CONFIRMATION_WAIVED_FOR_SESSION"`. **OVERWRITE** the body with the fresh draft. Do not append, do not preserve the prior draft. The task body after this write should contain ONLY the fresh draft — nothing else. If the task had a previous draft, note that in the output status (`drafted (overwrote previous)`) but do not keep any of the prior content.
>
> **Draft format:**
> ```
> <div dir="auto"><p style="margin:0;"><strong>DRAFT (auto-generated {today} — based on HubSpot engagement history):</strong></p><p style="margin:0;"><em>Last engagement: {most recent email/call/meeting with 1-line summary and date}</em></p><p style="margin:0;"><br></p><p style="margin:0;">Subject: [subject line]</p><p style="margin:0;"><br></p><p style="margin:0;">Hi [Name],</p><p style="margin:0;"><br></p><p style="margin:0;">[body]</p><p style="margin:0;"><br></p><p style="margin:0;">Andy</p></div>
> ```
>
> Including the "Last engagement" line lets Andy see at a glance what the draft is anchored on — if it's stale or wrong, he can skip.
>
> **Edge cases:**
> - Existing body has a previous draft → overwrite it with the fresh draft. Status = `drafted (overwrote previous)`.
> - No contact associated → write "NO CONTACT ASSOCIATED — manual review needed." to the task body (overwriting anything else there).
> - Contact exists but zero HubSpot engagements in last 12 months → write a short "circling back / worth reconnecting?" draft AND flag "⚠️ thin context — no recent HubSpot engagement" at the top. Overwrite any prior content.
>
> **Output:** Table with columns: `Task ID | Contact | Company | Status (drafted-fresh / drafted-overwrote / no-contact / thin-context) | Last engagement anchor (date + 1-line)`.

### Step 5 — Consolidate and report

Compile a single summary for Andy after all subagents return.

Format exactly:

```
EMAIL TASK DRAFTS -- [Day, Date]

TASKS REVIEWED: [N]
DRAFTED (fresh): [N]
DRAFTED (overwrote previous): [N]
SKIPPED (sequence task): [N]
NO CONTACT ASSOCIATED: [N]
THIN CONTEXT (flagged): [N]

DRAFTS READY FOR REVIEW:
[Table: Contact | Company | Last engagement anchor | HubSpot task URL]

THIN-CONTEXT FLAGS:
[List any tasks flagged "thin context — no recent HubSpot engagement". Andy reviews these manually before sending.]

NO CONTACT ASSOCIATED:
[List any tasks with no contact attached. Andy needs to associate the contact in HubSpot before the draft can be written.]

STATUS: [ALL CLEAR / ISSUES FOUND -- see flags above]
```

Keep the summary under 25 lines. Andy works through drafts in HubSpot directly — the summary is a dispatch list, not a report.

If zero tasks were drafted (no tasks due), end with one line: "No drafts needed today. [N] tasks in outreach sequences."

---

## Rules

- Always overwrite existing drafts with a fresh one each run. The task body is never preserved or appended to; it is replaced entirely. If Andy hand-edited a prior draft and wanted to keep it, he would have sent it already.
- Never invent specifics. If fewer than 2 are found, write thin-context fallback + flag.
- HubSpot engagement history is the primary source for specifics. ONE targeted 30-day news web search is allowed per contact for a fresh hook. Never use Outlook search, LinkedIn, or ZoomInfo as drafting sources. Never run more than one web search per contact.
- Never modify the task status. Andy marks tasks complete himself after sending.
- Never use em-dashes in the draft body. Split into two sentences instead.
- If subagent batch returns an error for a task, log it in the summary as "ERROR -- [reason]" and move on.
