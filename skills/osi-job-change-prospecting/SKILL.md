---
name: osi-job-change-prospecting
description: >
  Weekly LinkedIn Sales Navigator job-change prospecting workflow. Finds 1st-degree
  connections who changed jobs or got promoted in the past week (or 3 months for the
  initial run). Qualifies each against OSI ICP, checks HubSpot company ownership,
  pulls full contact and company history before writing any outreach, creates 2
  LinkedIn InMail tasks (2 weeks apart) for qualified JAM-owned targets, and logs
  everyone worth noting in the Excel tracker. Trigger on: "run job change search",
  "check for new job changes", "weekly prospecting", or when the scheduled Monday task fires.
---

# OSI Job Change Prospecting Workflow

## Sales Navigator URL

Navigate here to start every run. LinkedIn generates a new session automatically
even when the sessionId in the URL has expired.

```
https://www.linkedin.com/sales/search/people?query=(recentSearchParam%3A(id%3A5452872586%2CdoLogHistory%3Atrue)%2Cfilters%3AList((type%3ARECENTLY_CHANGED_JOBS%2Cvalues%3AList((id%3ARPC%2Ctext%3AChanged%2520jobs%2CselectionType%3AINCLUDED)))%2C(type%3ARELATIONSHIP%2Cvalues%3AList((id%3AF%2Ctext%3A1st%2520degree%2520connections%2CselectionType%3AINCLUDED)))))
```

This filter shows: 1st-degree connections who changed jobs in the last 90 days.

**For the weekly run:** Focus on entries showing "less than 1 month ago" or
"X weeks ago" that were not present in the previous week's run. Cross-reference
the Excel tracker (Claude-Brain/job-change-tracker.xlsx) to avoid duplicates.

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

- Andy McLean: 196669355
- Mark Metz: 210187184
- John Houston: 210187193

---

## Step 1: Read the Excel Tracker

Open Claude-Brain/job-change-tracker.xlsx and note who has already been processed.
Skip anyone already in the tracker.

---

## Step 2: Navigate to Sales Navigator

Use the URL above. Read all pages (navigate to &page=2, &page=3 as needed).
Use get_page_text first — it loads all cards at once. If that fails, use read_page
with depth 5 and look for the list of lead cards.

For each person shown:
1. Note name, title, company, change type (hired vs promoted), timeframe.
2. Quick ICP screen — Silent Skip (no log) if clearly not a buyer:
   - Project/program managers, sales reps, designers, recruiters, finance/legal/HR roles
   - Hyperscaler employees (Google, Meta, Amazon at scale)
   - Anyone with zero networking/hardware/infrastructure signals
3. Everyone else: full ICP check → history pull → HubSpot check → action.

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
- Read the Timeline / Relationship section — it shows past InMail threads, notes,
  and interactions Andy has had with this person.
- Note: date of last contact, what was discussed, any responses received.

### 4b. LinkedIn Message History (Regular LinkedIn)
- If Sales Nav timeline is sparse, navigate to linkedin.com/messaging and search
  for the person's name to find any direct message threads.
- Note any responses, questions asked, samples requested, or follow-ups promised.

### 4c. HubSpot Contact History
Search all of the following associated with the contact ID (sort DESCENDING by timestamp):
- **Emails**: objectType "emails" — subject line, direction, date
- **Calls**: objectType "calls" — outcome, notes, date
- **Notes**: objectType "notes" — content, date
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
  It changes the outreach angle entirely — reference the existing relationship.

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
- Not in HubSpot at all (create it, assign to Andy 196669355, then associate)

If new company is another rep's: leave contact's company as-is. Still create tasks.

For contacts NOT in HubSpot: create contact + associate with company.
For contacts already in HubSpot: update job title. Update company per rule above.
For companies NOT in HubSpot: create company record (owner: 196669355).

---

## Step 7: Create LinkedIn InMail Tasks

For each qualified target eligible for tasks:
- Task 1: "LinkedIn InMail - [Name] - [Company] (Touch 1)" — LINKED_IN_MESSAGE — due TODAY
- Task 2: "LinkedIn InMail - [Name] - [Company] (Touch 2)" — LINKED_IN_MESSAGE — due 2 WEEKS
- Owner: 196669355
- Body: Full drafted message

### Message guidelines
- Warm, peer-to-peer tone. Andy speaks as a person, not a company.
- No pitch in Touch 1. Open a conversation.
- No em-dashes. Under 200 words.
- Always reference their new role and company specifically.
- **If any prior history exists (LinkedIn messages, HubSpot emails, calls, samples sent):**
  The message MUST feel like picking up where you left off, not a cold intro. Reference
  the specific interaction — what was discussed, what was sent, what was agreed. Never
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

Color coding:
- Green (E2EFDA): Tasks created
- Orange (FCE4D6): Good target, different rep owns company
- Yellow (FFF2CC): Conditional / monitoring
- Light Blue (EAF0FB): Unloaded / needs manual review
- Grey (F2F2F2): Skipped (note reason)

Save updated file back to Claude-Brain.

---

> **SYNC NOTE:** This skill exists in two locations that must ALWAYS be kept in sync:
> - `Claude-Brain/skills/osi-job-change-prospecting/SKILL.md` (OneDrive — source of truth)
> - `.claude/skills/osi-job-change-prospecting/SKILL.md` (Cowork local — what triggers the skill)
>
> Any time changes are made to one, apply them to the other immediately. After editing, repackage
> `Claude-Brain/skills/osi-job-change-prospecting.skill` and reinstall via Cowork if the local
> Cowork copy was updated directly. If only the local copy was updated, sync back to OneDrive.

---

## Step 9: Save Session Summary

Save or append a summary to Claude-Brain/sessions/session-YYYY-MM-DD.md:
- How many people scanned
- How many qualified
- How many tasks created
- Names of anyone logged under other reps
- Any partial names still unresolved
