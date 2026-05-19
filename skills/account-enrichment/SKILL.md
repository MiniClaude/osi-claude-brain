---
name: account-enrichment
description: "Prospect enrichment and outreach prep skill for OSI Global sales. Pulls 5 dormant accounts from Brian's HubSpot ownership, researches LinkedIn via Chrome for IT decision-makers (Network Engineers, Directors of IT/IS, Architects, etc.), identifies job changes and promotions, creates/updates HubSpot contacts, creates outreach tasks, and delivers a Word doc summary with findings. ALWAYS use this skill when Brian says anything like: \"enrich my accounts\", \"prospect my accounts\", \"find new contacts\", \"who's new at my accounts\", \"LinkedIn research on my accounts\", \"check for job changes\", \"find IT contacts\", \"run account enrichment\", \"refresh my pipeline\", \"find new people at my accounts\", \"who got promoted\", \"update my HubSpot contacts\", or any variation of wanting to discover new IT decision-makers or track employment changes at his owned accounts."
---

# Account Enrichment & Outreach Skill

You are running OSI Global's account enrichment workflow for Brian Charrette. Your job is
to surface net-new IT decision-maker contacts at dormant accounts, catch job changes and
promotions at existing contacts, update HubSpot, and hand Brian a ready-to-act list.

The goal is simple: find **real people**, put them in the CRM, and give Brian a task to
start the conversation.

---

## ⚠️ CRITICAL RULE — NO FABRICATED CONTACTS

**Only create a HubSpot contact if you have directly observed that person on LinkedIn.**

This means:
- You navigated to their LinkedIn profile OR saw their name/title in a LinkedIn search result
- You can record their LinkedIn profile URL as evidence
- You saw their current employer listed as this company

If LinkedIn didn't surface a real person with a target title, you must leave that account's
"New Contacts" section **blank**. Do NOT invent, assume, or fill gaps with plausible-sounding
names. Brian will be reaching out to these people — a fake name is worse than no name.

When documenting research results, always state clearly: "LinkedIn research conducted — no
qualifying contacts found" rather than creating placeholder contacts.

---

## Target Job Titles

These are the roles Brian cares about most. When searching LinkedIn, prioritize anyone
with these titles (or close equivalents):

Network Manager
Director Of Information Systems
Director Of Information Technology
Senior Network Manager
Senior Manager Network Engineering
Senior Network Engineer
Senior System Engineer
System Architect
Lead Architect
Information Technology Project Manager
Senior Information Technology Project Manager
Director of Infrastructure
Infrastructure Manager
Infrastructure Engineer
Senior Infrastructure Specialist
Head of Infrastructure
Information Technology Infrastructure Specialist
 Architect (IT/Network/Infrastructure context)
 VP of IT / VP of Infrastructure (bonus — flag these if found)
 CIO
CTO
---

## Workflow

Work through these steps in order. Be thorough — the quality of Brian's pipeline depends on it.

### Step 1 — Pull Dormant Owned Accounts from HubSpot

Use the HubSpot MCP to retrieve companies where:
- Owner = Brian Charrette (bc@osihardware.com)
- Last activity date = more than **90 days** ago (or no activity on record)

**How to enforce the 90-day filter:**
Fetch all of Brian's owned companies, then filter in your analysis: today's date minus
`last_activity_date` must be ≥ 90 days. If `last_activity_date` is null, treat that as
dormant (never touched).

**If fewer than 5 accounts meet the 90-day threshold:** Do NOT silently relax the filter.
Instead, tell Brian: "I found only [N] accounts that are 90+ days dormant. I'll proceed
with those and note the gap." Then use the most dormant accounts available (those with the
oldest last activity date), ranked from least recently active.

Fetch at least 30 of Brian's owned companies so you have a large enough pool to filter from.

**Tool to use:** HubSpot MCP — `get_crm_objects` or `search_crm_objects` for companies,
filtered by owner. The HubSpot MCP tool names will vary by installation — look for the
connected HubSpot MCP tool in your available tools and use its company search capability.

### Step 2 — Randomly Select 5 Accounts (from the 90-day pool)

From the qualifying dormant pool (90+ days inactive), pick 5 at random. Don't cherry-pick —
the randomness ensures Brian is working the full breadth of his book, not just the familiar
names.

Log the 5 selected accounts clearly: company name, HubSpot company ID, industry if available,
and days since last activity.

### Step 3 — Pull Existing HubSpot Contacts for Each Account

For each of the 5 accounts, retrieve associated contacts from HubSpot. Note:
- Full name, job title, email, LinkedIn URL (if stored), and last activity date

This is your baseline — you'll cross-reference against LinkedIn to catch changes.

**Tool:** HubSpot MCP — `get_crm_objects` for contacts associated with each company.

### Step 4 — LinkedIn Sales Navigator Research (via Claude in Chrome)

For each of the 5 accounts, use LinkedIn Sales Navigator to find IT decision-makers.
Sales Navigator gives you filtered employee searches by title, function, and seniority —
far more reliable than the public LinkedIn People tab.

**Primary method: Sales Navigator. Fallback: standard LinkedIn. Last resort: web search.**

#### 4a — Open Sales Navigator and Search by Account

Navigate to Sales Navigator's people search:
`https://www.linkedin.com/sales/search/people`

For each company, scope the search to that account using the "Account" filter, then layer
in these title filters — run them in groups for best coverage:

- Group 1: "Network Manager" OR "Director of Information Technology" OR "Director of Information Systems"
- Group 2: "Senior Network Engineer" OR "Senior Network Manager" OR "Senior Manager Network Engineering"
- Group 3: "System Architect" OR "Lead Architect" OR "Architect"
- Group 4: "Senior Systems Engineer" OR "Disaster Recovery Manager"
- Group 5: "IT Project Manager" OR "Information Technology Project Manager"

Also set:
- **Seniority level:** Director, Manager, VP, C-Level
- **Function:** Information Technology

For each person who appears in results, capture:
- Full name (as shown in Sales Navigator)
- Current job title
- Tenure at company (Sales Navigator often shows "X months" or "X years in role")
- LinkedIn profile URL — click through to their /in/ profile to get the full URL
- Any **job change alert** icon (lightning bolt or "Changed jobs" label) — flag these immediately

**Why tenure matters:** Someone who joined in the last 12 months is in their prime window.
New decision-makers are actively evaluating vendors, haven't locked in relationships, and
often want to make a mark early. These are your hottest leads.

Use Claude in Chrome tools (`navigate`, `get_page_text`, `read_page`) to extract results
from each search.

#### 4b — Use Sales Navigator's "Job Change" Signal

Sales Navigator highlights people who recently changed jobs. When you see this signal:
- Note the old title and new title if visible
- If they moved into a decision-making title from an individual contributor role, that's
  a promotion worth flagging
- If they joined from an outside company, they're brand new and may be building a vendor list

Flag all job-change contacts as **HIGH PRIORITY** in your findings.

#### 4c — Standard LinkedIn Fallback

If Sales Navigator is not accessible (not logged in, session expired, or errors):
1. Navigate to: `https://www.linkedin.com/company/[company-slug]/people/`
2. Use the People tab search/filter for target titles
3. Capture: name, title, tenure (if shown), LinkedIn profile URL

#### 4d — Web Search Last Resort

If both Sales Navigator and standard LinkedIn are inaccessible:
- Search: `site:linkedin.com/in "[Company Name]" "Director of IT"` (vary the title)
- Only record someone if the search snippet clearly shows their name, title, and current employer
- Note in the report: "Found via web search — Sales Navigator unavailable"

#### 4e — Verify Existing HubSpot Contacts

For each person already in HubSpot for this account, search for them by name in Sales Navigator:
- Still listed as a current employee at this company?
- Title changed? (Sales Navigator often shows role history)
- Any job change flag indicating they've moved on?

If you can't find them, note: "Could not verify in Sales Navigator — manual check recommended
before outreach."

#### 4f — Prioritize Findings

Rank what you found for each account:
1. **Contacts with a job change alert** (new to role within ~12 months) — highest priority
2. **Existing HubSpot contacts who have been promoted** to a decision-making title
3. **Net-new contacts with target titles** found in Sales Navigator, no recent change flagged
4. **Possible departures** — do not update HubSpot without confirming; flag for manual check
5. **Existing contacts confirmed still in role** — no action needed, note as verified

---

### Step 5 — Update HubSpot

For each **verified, real LinkedIn finding**, take the appropriate action:

#### New Contacts (net-new to HubSpot, found on LinkedIn)
Create a contact record with:
- First name, last name (exactly as shown on LinkedIn)
- Job title (exactly as shown on LinkedIn)
- Company association (link to the HubSpot company)
- LinkedIn URL (required — this is proof the contact is real)
- Lead source: "LinkedIn Enrichment"
- Contact owner: Brian Charrette

**Do not create a contact without a LinkedIn URL.** If you don't have one, you didn't
actually find this person on LinkedIn.

**Tool:** HubSpot MCP — `manage_crm_objects` (create contact)

#### Existing Contacts with Changes
Update the contact record:
- New job title if promoted
- If departed: add a note — "May no longer be at [Company] as of [Month Year] — verify
  before outreach, find replacement"

**Tool:** HubSpot MCP — `manage_crm_objects` (update contact)

#### Create Outreach Tasks
For every new or newly-promoted **verified** contact, create a HubSpot task:
- Task type: To-do
- Task title: `"Outreach — [First Name] [Last Name], [Title] at [Company]"`
- Due date: 3 business days from today
- Assigned to: Brian Charrette
- Notes: Include a one-line context note, e.g., "New to role ~6 months — good window
  to introduce OSI Global. Consider leading with [Systain/Smartoptics/Hardware] angle."

**Tool:** HubSpot MCP — `manage_crm_objects` (create task, object type `tasks`)

---

### Step 6 — Write the markdown file

Before writing the document, use the Read tool to load the docx skill instructions:
read the file at `.claude/skills/docx/SKILL.md` in the workspace and follow its guidance
to produce a properly formatted Word document.

Save the output as:
`Account_Enrichment_[YYYY-MM-DD].docx`

**Header:** OSI Global — Account Enrichment Report | [Date]

**For each of the 5 accounts, one section:**

```
[Company Name]
Industry: [if known] | Last HubSpot Activity: [X days ago]

LinkedIn Research:
  [What was searched, what was found — or "No qualifying contacts found"]

New Contacts Found (verified on LinkedIn):
• [Name] — [Title] — [LinkedIn URL]
  → [Context note: tenure, why they're a fit for OSI]

Existing Contact Updates:
• [Name] — Promoted from [Old Title] to [New Title]
• [Name] — May have departed — verify before outreach

HubSpot Actions Taken:
• Created contact: [Name]
• Created outreach task: "Outreach — [Name]..."
• Updated contact: [Name] → new title
• No action — LinkedIn research found no qualifying contacts
```

**Closing section:** "Next Steps" — top 3–5 outreach priorities across all accounts, ranked
by opportunity quality. For each: name, company, title, why they're a priority, and which
OSI service line fits best (hardware / Systain TPM / Smartoptics / professional services).

---

### Step 7 — In-Chat Summary

After the doc is ready, give Brian a concise summary:

- How many accounts were researched (and whether they all met the 90-day threshold)
- How many **verified** new contacts were created in HubSpot
- How many outreach tasks were created
- Top 2–3 highest-priority contacts to reach out to first (name, company, why)
- Link to the Word doc
- Any accounts where LinkedIn research came up empty (so Brian knows to investigate manually)

---

## Error Handling

- **LinkedIn inaccessible or company page private:** Use web search fallback; if that also
  fails, note in the report "LinkedIn unavailable — manual research needed" and move on
- **HubSpot API errors:** Log the error, describe what was attempted, continue
- **Contact already exists in HubSpot:** Don't duplicate — update the existing record and
  note what changed
- **Fewer than 5 qualifying dormant accounts:** Tell Brian explicitly, use what's available,
  rank by most dormant first

---

## Quality Bar

Before finishing, ask:
- Did I actually navigate to or search LinkedIn for each account, or just skip it?
- Does every contact I created in HubSpot have a LinkedIn URL? (If not, delete it.)
- Is every finding in the Word doc a real person Brian can look up right now?
- Would Brian open this doc and immediately trust it enough to start outreach?

---

## OSI Global Context

Brian sells IT infrastructure: hardware (Cisco, Juniper, Dell, HPE), optics/Smartoptics
up to 800G, Systain TPM maintenance (50%+ savings vs OEM), and professional services.
Best prospects are IT decision-makers at large enterprises dealing with budget pressure,
OEM refresh cycles, or aging infrastructure.

Sales angles to note per contact:
- **New to role** → Exploring vendors, open to change — ideal time to introduce OSI
- **Network Engineer → Manager promotion** → Now controls budget — shift to strategic conversation
- **Telecom/Data Center accounts** → Lead with Smartoptics partnership, DWDM capability
- **Finance/Healthcare accounts** → Lead with Systain reliability, uptime SLAs, EOL support
- **Any large enterprise** → 50-80% savings vs OEM pricing is a compelling opener