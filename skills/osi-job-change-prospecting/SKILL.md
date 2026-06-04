---
name: osi-job-change-prospecting
description: >
  Weekly LinkedIn Sales Navigator prospecting workflow with two phases. Phase A: finds
  1st-degree connections who changed jobs or got promoted in the past week. Phase B: finds
  new 1st-degree connections made in the past week. Both phases qualify against OSI ICP,
  check HubSpot company ownership, pull full contact and company history before writing
  outreach, create 2 LinkedIn InMail tasks (2 weeks apart) for qualified JAM-owned targets,
  and log everyone worth noting in the Excel tracker.
  Trigger on: "run job change search", "check for new job changes", "weekly prospecting",
  "new connections", or when the scheduled Monday task fires.
---

# OSI Job Change Prospecting Workflow

## Sales Navigator URLs

### Phase A: Job Changes
Navigate here for job change prospecting. LinkedIn generates a new session automatically
even when the sessionId in the URL has expired.

```
https://www.linkedin.com/sales/search/people?query=(recentSearchParam%3A(id%3A5452872586%2CdoLogHistory%3Atrue)%2Cfilters%3AList((type%3ARECENTLY_CHANGED_JOBS%2Cvalues%3AList((id%3ARPW%2Ctext%3AChanged%2520jobs%2CselectionType%3AINCLUDED)))%2C(type%3ARELATIONSHIP%2Cvalues%3AList((id%3AF%2Ctext%3A1st%2520degree%2520connections%2CselectionType%3AINCLUDED)))))
```

This filter shows: 1st-degree connections who changed jobs in the past week.

**If this returns 0 or unexpectedly many results:** The `RPW` filter ID may have drifted.
Go to Sales Nav manually, apply 1st degree + "Changed jobs" with the Past Week timeframe,
save the search, and update the `recentSearchParam id` and filter value in this URL.
For a one-time backfill (first ever run), replace `RPW` with `RPC` to get the last 90 days.

### Phase B: New Connections
Navigate here for new connections from the past week.

```
https://www.linkedin.com/sales/search/people?query=(recentSearchParam%3A(id%3A5522322210%2CdoLogHistory%3Atrue)%2Cfilters%3AList((type%3ACONNECTION_DATE%2Cvalues%3AList((id%3APW%2Ctext%3APast%2520week%2CselectionType%3AINCLUDED)))%2C(type%3ARELATIONSHIP%2Cvalues%3AList((id%3AF%2Ctext%3A1st%2520degree%2520connections%2CselectionType%3AINCLUDED)))))
```

This filter shows: 1st-degree connections added in the past week.
Saved search ID `5522322210` confirmed 2026-05-04.

**If this returns 1K+ results:** The saved search ID has expired or the filter is not
applying correctly. Go to Sales Nav manually, apply 1st degree + Connection date: Past week,
save the search, then update the `recentSearchParam id` in this URL with the new ID.

---

## Andy Rules

- No em-dashes anywhere. Not once.
- Hard No = silent skip. Do not log in Excel.
- Everyone else worth noting goes in Excel regardless of company ownership.

### Task creation rules
- Contact's new company is JAM-owned or not in HubSpot: update company, create tasks.
- Contact's new company is another rep's, BUT their current HubSpot company is JAM-owned:
  do NOT update their company (keep them in JAM territory), DO still create tasks.
- Contact's HubSpot record is already under another rep's company: no tasks. Excel only.

### Excel logging for other-rep contacts
When logging a contact whose HubSpot record is under another rep, capture all of:
- Company owner name
- LinkedIn URL
- HubSpot contact URL
- Last activity date (most recent email, call, or note)
- Whether they are a purchasing customer or have open deals

### Resolving partial LinkedIn names (privacy-blocked profiles)
When a Sales Nav result shows only a first name + last initial (e.g. "Tim W." or "Antonio F."):
1. Search LinkedIn for the person by keyword + company name to get the full name.
2. Use the full name to search HubSpot directly.
3. If not found by name, check their past companies from LinkedIn work history,
   then search HubSpot under each past company for a contact with matching first name
   and last initial.

## JAM Team Owner IDs

- Brian Charrette: 213536174
- Mark Metz: 210187184
- John Houston: 210187193

---

## Workflow Overview

Run both phases every week. Phase A and Phase B use the same qualification, history,
HubSpot, and task-creation logic (Steps 3-9). The only difference is the Sales Nav URL
and the "Change Type" logged in Excel.

- **Phase A** - Job Changes: Change Type = "Job Change" or "Promotion"
- **Phase B** - New Connections: Change Type = "New Connection"

Complete Phase A fully, then run Phase B. Log all results in the same Excel tracker.

---

## Step 1: Read the Excel Tracker

Open Claude-Brain/job-change-tracker.xlsx and note who has already been processed.
Skip anyone already in the tracker.

---

## Step 2: Navigate to Sales Navigator

### Phase A: Job Changes
Use the Phase A URL. Read all pages (navigate to &page=2, &page=3 as needed).
Use get_page_text first, it loads all cards at once. If that fails, use read_page
with depth 5 and look for the list of lead cards.

For each person shown:
1. Note name, title, company, change type (hired vs promoted).
2. Quick ICP screen, Silent Skip (no log) if clearly not a buyer:
   - Project/program managers, sales reps, designers, recruiters, finance/legal/HR roles
   - Hyperscaler employees (Google, Meta, Amazon at scale)
   - Anyone with zero networking/hardware/infrastructure signals
3. Everyone else: full ICP check → history pull → HubSpot check → action.

### Phase B: New Connections
Use the Phase B URL. Same page navigation and loading approach as Phase A.

For each person shown:
1. Note name, title, company. Change type = "New Connection."
2. Same quick ICP screen as Phase A, Silent Skip if clearly not a buyer.
3. Check Excel tracker first, skip anyone already logged from a prior job change run.
4. Everyone else: full ICP check → history pull → HubSpot check → action.

**Message tone for new connections:** These people just connected with Andy. The opener
should acknowledge the new connection naturally, not a cold reach, but also not
over-familiar. Reference something specific about their role or company. Keep it warm
and conversational. No pitch in Touch 1.

---

## Step 3: ICP Qualification

Target profile: network engineers, infrastructure managers, IT directors, procurement
managers with IT focus, data center engineers. Mid-to-large enterprise, carrier,
telecom, or regional data center operator.

Key skills to look for: Cisco, optical networking, DWDM, transceivers, data center
infrastructure, network design, server/storage procurement, SD-WAN, BGP/OSPF.

---

## Step 4: Pull Full History Before Doing Anything Else

For every qualified prospect, pull all available history before writing outreach or
making any HubSpot changes. Do this in parallel where possible.

### 4a. LinkedIn Message History (Sales Navigator)
- Navigate to their Sales Nav lead page.
- Read the Timeline / Relationship section, it shows past InMail threads, notes,
  and interactions Andy has had with this person.
- Note: date of last contact, what was discussed, any responses received.

### 4b. LinkedIn Message History (Regular LinkedIn)
- If Sales Nav timeline is sparse, navigate to linkedin.com/messaging and search
  for the person's name to find any direct message threads.
- Note any responses, questions asked, samples requested, or follow-ups promised.

### 4c. HubSpot Contact History
Search all of the following associated with the contact ID (sort DESCENDING by timestamp):
- **Emails**: objectType "emails", subject line, direction, date
- **Calls**: objectType "calls", outcome, notes, date
- **Notes**: objectType "notes", content, date
- **Tasks (completed)**: objectType "tasks", filter hs_task_status = COMPLETED

Key questions to answer:
- When was the last touchpoint?
- What was discussed or sent (samples, quotes, vendor approvals)?
- Was there a response or was it one-way?
- Are there any open commitments or follow-ups promised?

### 4d. HubSpot Company Purchasing History
Search for deals associated with the contact's current or past company:
- search_crm_objects objectType "deals", associatedWith the company ID
- Note: deal name, stage, amount, close date, owner
- If the company has been a customer or has an active deal, flag this prominently.
  It changes the outreach angle entirely, reference the existing relationship.

---

## Step 5: HubSpot Ownership Check

1. Search HubSpot for the contact by name.
   - If privacy-blocked on LinkedIn, use past companies to find them (see Andy Rules above).
2. Search HubSpot for their NEW company. Note the owner ID.
3. Resolve owner ID to a name using search_owners.
4. Decide action:
   - JAM-owned or new company not in HubSpot: update contact + create tasks.
   - New company is another rep's but current HubSpot company is JAM's:
     do NOT update company, DO create tasks.
   - Contact's current HubSpot record is under another rep: no tasks, Excel only.

---

## Step 6: Create or Update HubSpot Records

### Company update rule (IMPORTANT)
Only update a contact's company association if the new company is:
- Already owned by Andy/Mark/John (JAM team), OR
- Not in HubSpot at all (create it, assign to Andy 213536174, then associate)

If new company is another rep's: leave contact's company as-is. Still create tasks.

For contacts NOT in HubSpot: create contact + associate with company.
For contacts already in HubSpot: update job title. Update company per rule above.
For companies NOT in HubSpot: create company record (owner: 213536174).

---

## Step 7: Create LinkedIn InMail Tasks

**Duplicate-task check (MANDATORY before creating either task):** Query HubSpot for tasks associated to this contact. If the contact has ANY task where `hs_task_type` = `LINKED_IN_MESSAGE` AND `hs_task_status` is `NOT_STARTED` or `IN_PROGRESS`, skip BOTH tasks entirely. Log in Excel and session summary: "existing LinkedIn task on HubSpot. No new tasks created." This applies regardless of the existing task's subject line. One active LinkedIn message task already queued = we do not pile on more.

For each qualified target eligible for tasks (and passing the duplicate check above):
- Task 1: "LinkedIn InMail - [Name] - [Company] (Touch 1)", LINKED_IN_MESSAGE, due TODAY
- Task 2: "LinkedIn InMail - [Name] - [Company] (Touch 2)", LINKED_IN_MESSAGE, due 2 WEEKS
- Owner: 213536174
- Body: **ONLY the raw draft message text. Nothing else.**

### Task body rule (HARD RULE, no exceptions)
The task body / note field on a Sales Navigator LinkedIn task is the literal message text Andy will paste into LinkedIn. It must contain ONLY the draft to send. Nothing else.

Do NOT include any of the following in the task body:
- Label prefixes like "LinkedIn invite (under 300 chars):", "Touch 1:", "Message:", "Draft:", "InMail body:"
- Character-count annotations like "(under 300 chars)" or "(280/300)"
- Subject lines, headers, or section dividers
- Strategy notes, ICP rationale, history summaries, or context
- Signoff metadata like a dash followed by "Andy" if it's not part of the actual message body
- Any framing, commentary, or instructions to Andy

❌ WRONG (do not do this):
```
LinkedIn invite (under 300 chars): Hey Charles, OSI worked with Patrick a while back. Sending a fresh batch of SmartOptics samples around to a few network admins this month. Open to swapping notes? Andy at OSI Global.
```

✅ RIGHT (the entire body field):
```
Hey Charles, OSI worked with Patrick a while back. Sending a fresh batch of SmartOptics samples around to a few network admins this month. Open to swapping notes? Andy at OSI Global.
```

The task subject already encodes the touch number and the contact. The body is just the message. Andy copies the body field straight into LinkedIn, anything other than the message itself has to be deleted by hand and that's the bug we're fixing.

### Message guidelines
- Warm, peer-to-peer tone. Andy speaks as a person, not a company.
- No pitch in Touch 1. Open a conversation.
- No em-dashes. Under 200 words.
- Always reference their new role and company specifically.
- **If any prior history exists (LinkedIn messages, HubSpot emails, calls, samples sent):**
  The message MUST feel like picking up where you left off, not a cold intro. Reference
  the specific interaction, what was discussed, what was sent, what was agreed. Never
  write a cold opener to a warm contact.
- **If the company has a purchasing history or active deal:** Reference the existing
  relationship directly. Lead with continuity, not prospecting.
- Touch 2 (2 weeks later): brief, low-pressure follow-up. Different angle or hook.
  Acknowledge you may have caught them at a bad time. Keep it short.

---

## Step 8: Update Excel Tracker

Open Claude-Brain/job-change-tracker.xlsx.
Add new rows for everyone processed. Do not duplicate rows already in the tracker.
Columns: Name, New Title, New Company, Change Type, ICP Verdict, HubSpot Company Owner,
Action Taken, HubSpot Contact URL (hyperlink), Sales Nav URL (hyperlink), Notes.

Change Type values: "Job Change", "Promotion", "New Connection"

Color coding:
- Green (E2EFDA): Tasks created
- Orange (FCE4D6): Good target, different rep owns company
- Yellow (FFF2CC): Conditional / monitoring
- Light Blue (EAF0FB): Unloaded / needs manual review
- Grey (F2F2F2): Skipped (note reason)

Save updated file back to Claude-Brain.

---

> **SYNC NOTE:** This skill exists in two locations that must ALWAYS be kept in sync:
> - `C:\Claude-Brain\skills\osi-job-change-prospecting\SKILL.md` (Git-versioned, source of truth, backed up at github.com/Drrewdy/Claude-Brain)
> - `.claude/skills/osi-job-change-prospecting/SKILL.md` (Cowork local, what triggers the skill)
>
> Any time changes are made to one, apply them to the other immediately. After editing, repackage
> `Claude-Brain/skills/osi-job-change-prospecting.skill` and reinstall via Cowork if the local
> Cowork copy was updated directly. If only the local Cowork copy was updated, sync the change back into `C:\Claude-Brain\skills\` and push to GitHub.

---

## Step 9: Save Session Summary

Save or append a summary to Claude-Brain/sessions/session-YYYY-MM-DD.md:
- How many people scanned
- How many qualified
- How many tasks created
- Names of anyone logged under other reps
- Any partial names still unresolved
