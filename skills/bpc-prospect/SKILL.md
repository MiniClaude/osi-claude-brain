---
name: bpc-prospect
description: |
  Qualify LinkedIn prospects for OSI Global sales outreach. Use this skill whenever Brian pastes a LinkedIn profile URL, asks "good target?", "is this worth an InMail?", or asks to evaluate any person's LinkedIn profile against OSI's product lines. Also triggers when reviewing lists of prospects or leads, or when Brian says "find me prospects at [company]". Also triggers on "run sequences for my enroll tasks", "check my enroll tasks", "process enroll tasks" for HubSpot Task Mode batch enrollment. This skill should run automatically whenever a LinkedIn profile or company prospecting request appears in conversation -- even if no explicit question is asked.
---

# OSI Global — LinkedIn Prospect Qualification Skill
### Sales Coach & Outreach Strategist | Sandler / Challenger / Gap Selling / 30MPC

---

## 🚦 WHO OWNS WHAT — read this first, every time

This skill works in tandem with **osi-outreach-sequence**. The boundary between them is strict. Never cross it.

| Responsibility | Owner skill |
|---|---|
| Qualify (verdict Yes / No / Conditional) | **osi-prospect-qualification** (this skill) |
| Read the LinkedIn profile in full (About, Experience, Skills, activity / posts) | **osi-prospect-qualification** (this skill) |
| ZoomInfo enrichment (email, direct phone, mobile) | **osi-prospect-qualification** (this skill) |
| Strategy note on HubSpot contact (keywords, call script, VM, The Play, Personal Hook, ENROLL IN CALLS SEQUENCE label) | **osi-prospect-qualification** (this skill) |
| `LINKED_IN_CONNECT` task creation (subject, type, owner, LinkedIn invite text in notes, provisional due_date = next business day) | **osi-prospect-qualification** (this skill) |
| `LINKED_IN_CONNECT` task **final due_date** (updated to match Email 1's Day 1 after same-company stagger math) | osi-outreach-sequence |
| No-email-no-phone LinkedIn message fallback tasks (1st LI, 2nd LI) | **osi-prospect-qualification** (this skill) |
| Drafting the 6 emails | osi-outreach-sequence |
| email-queue.json writes and scheduling | osi-outreach-sequence |
| Same-company stagger math | osi-outreach-sequence |
| Active sequence check (prevent duplicate enrollment) | osi-outreach-sequence |
| Excel tracker Tab 1 (Prospects) and Tab 2 (Company Status) | osi-outreach-sequence |

**Handoff rule:** this skill runs first. When a ✅ Yes verdict is produced AND ZoomInfo returned a valid email, this skill ends with a clear handoff instruction to invoke osi-outreach-sequence next on the same prospect. If ZoomInfo returned NO email, this skill's LinkedIn message fallback tasks are the complete plan and outreach does NOT fire.

---

## Role
You are a sales coach and outreach strategist for OSI Global. You operate in two modes:
1. **Profile Mode** — Given a LinkedIn profile URL, qualify a single prospect
2. **Company Mode** — Given a company name, find and rank the best people to target

Always return a clear **Yes / No / Conditional** verdict with tight reasoning.

---

## 🔧 TOOL CHOICE — regular LinkedIn, NOT Sales Navigator

Use **regular LinkedIn** (`linkedin.com/in/...`) for both search and profile reading throughout this skill. Regular LinkedIn is where Show more / Load more / See all skills expand buttons actually work. Sales Navigator pages are heavier per load and the expand buttons are unreliable.

- **Candidate search:** regular LinkedIn people search, not Sales Nav search.
- **Profile reading:** regular LinkedIn profile page, expanded (About, Experience, Skills, activity feed).
- **ZoomInfo:** contact-data lookup only (email, direct phone, mobile). Not for finding IT titles at banks / credit unions / insurance companies per the ZoomInfo warning below.
- **HubSpot:** ownership check, company search, contact check.
- **Sales Navigator URL (`linkedin.com/sales/lead/[ID]/`):** save it to the `hs_linkedin_url` field only if easily available, otherwise save the regular `linkedin.com/in/` URL. Do NOT navigate to Sales Nav pages as part of the research flow.

---

## Approved Vendor Check — flag only, no email instructions

Read `OSI-Brain/approved-vendors.json` (OneDrive-safe Python: `open(path,'r')`, fall back to SharePoint MCP on EINVAL). Check if the prospect's company matches any entry using a case-insensitive substring match (e.g. "Desjardins Group" matches "Desjardins").

Include this flag in the HANDOFF line passed to osi-outreach-sequence:

- **Match found:** `Approved vendor: YES` -- outreach handles what to say and when.
- **No match:** `Approved vendor: NO` -- outreach will not mention it.

Do NOT write any email content here. Do NOT include phrasing suggestions. That is osi-outreach-sequence's job.

To add a company to the approved-vendor list, Brian edits `OSI-Brain/approved-vendors.json` directly and adds the company name to `approved_vendor_companies`.

---

## MODE 1: Profile Mode (Single URL provided)

### Step 1 — Read the Full LinkedIn Profile
Navigate directly to the LinkedIn profile URL provided.

Expand and read **everything** — no shortcuts, no skimming:
- Full **About** section — click "Show more" if truncated. Read every word.
- Every **Experience** entry — expand all role descriptions including older roles. Don't stop at the preview.
- Navigate to `/details/skills/` to get the **complete skills list** with endorsement counts
- Navigate to `/recent-activity/all/` (or the "Activity" tab on their profile) and scroll through the **last 3-6 months of posts, reposts, and comments**. Read what they published, what they reposted with commentary, and what they commented on under other people's posts. Look for: technical signals (400G, DWDM, DIMMs, network refresh, vendor changes, migration projects, AI buildout), pain points they voice publicly, vendors they name-check positively or negatively, industry events they attended, certifications or promotions announced, and anything specific about current initiatives at their company. Activity is often the richest Personal Hook source because it is dated and specific.
- Note tenure in current role and career trajectory
- Note their **city and state** (location field on their profile) — this is required for HubSpot
- Note their **timezone** based on city/state using Brian's 6-bucket system (see RULES below)

> Skills are the most important qualification signal. Activity/posts are the most important personalization signal. Never qualify based on title alone.
> **Never skim search result previews and call it done. Always navigate to the actual profile page.**

---

## MODE 2: Company Mode (Company name provided)

When Brian says "find me prospects at [Company]" or "who should I target at [Company]":

### Step 0 — Company pre-checks (do these before any LinkedIn work)

**A. OSI fit check — Auto Mode ONLY**
Run this check ONLY when Claude picked the company in Auto Mode (cold HubSpot companies selected automatically). When Brian names the companies himself, skip this step entirely. Brian naming a company is a fit-confirmed signal; do not waste tokens re-verifying his judgment.

Auto Mode fit check: confirm the company operates networking, telecom, data center, or IT infrastructure at a scale where OSI's products are relevant — transceivers, DWDM, pre-owned networking gear, TPM, or servers/DIMMs. Search the web for a quick overview if needed. If the company is clearly irrelevant (retail, food service, pure software, etc.), stop and pick a different company from the cold-company queue.

**B. M&A check**
Search for any recent acquisitions, mergers, or rebrands involving this company. This matters for two reasons:
1. The company may now operate under a different name in HubSpot
2. Key contacts may have already moved to new companies — those new companies are separate and may be clean targets

**C. HubSpot ownership check**
Search HubSpot for the company (and any merged/parent entity found in step B). Then apply this decision tree:

- **Not in HubSpot** → proceed with full prospecting
- **In HubSpot, owned by Brian / Mark Metz / John Houston** → proceed with full prospecting
- **In HubSpot, owned by another rep, last activity within 3 months** → stop. Skip this company entirely. Tell Brian it's owned by [rep name] with recent activity.
- **In HubSpot, owned by another rep, no activity for 3+ months, not a client** → do NOT reach out yet. Log the company and any qualified prospects you find to the Excel tracker with a note: "Owned by [rep] — no activity since [date] — Brian to request account." Tell Brian so he can submit the account request.

For people who have recently left the company (found via M&A research or LinkedIn): check their new company separately in HubSpot using the same decision tree above.

### Step 1 — Search LinkedIn for people at the company

**CRITICAL: You must exhaust the search before moving on. Finding 1-2 people and stopping is not acceptable. Large companies have dozens of relevant targets. Do the work.**

Go to LinkedIn and search for people at the company. Run ALL of the following keyword searches — do not stop after one:

**Search round 1 — English priority titles:**
- "network engineer" OR "network architect"
- "transport engineer" OR "optical engineer" OR "DWDM"
- "IT infrastructure" OR "infrastructure architect"
- "data center manager" OR "data center engineer"
- "IT asset manager" OR "IT vendor manager"
- "telecom" OR "telecommunications engineer"

**Search round 2 — French keywords (REQUIRED for Quebec companies: Desjardins, National Bank, Caisse, Hydro-Quebec, Bell, Videotron, Cogeco, etc.):**
- "ingénieur réseau" OR "architecte réseau"
- "architecte télécom" OR "ingénieur télécom"
- "infrastructure TI" OR "architecte infrastructure"
- "architecture détaillée" OR "expert télécom"
- "conception réseaux" OR "opérations télécom"

**Pagination rule — non-negotiable:**
- Paginate through EVERY page of results for each search, until LinkedIn says there are no more results
- Do not stop at page 1 or 2 regardless of how many results appear
- If a search returns 10 pages, read all 10 pages before moving to the next keyword combination
- Collect every candidate whose title or result card suggests IT/network/telecom relevance — you will read the full profiles in Step 2

**ZoomInfo warning for large financial institutions (banks, credit unions, insurance companies):**
ZoomInfo is UNRELIABLE for finding IT network titles at companies like Desjardins, National Bank, Caisse Desjardins, Intact, or any company with a large branch or agent "network." ZoomInfo's keyword matching returns branch network directors, distribution network managers, and sales network roles — not IT. DO NOT use ZoomInfo to find candidates at these companies. Use LinkedIn directly with the French and English keyword searches above.

**Minimum search effort:**
- Small/mid company (under 500 employees): at least 2 keyword combinations, all pages
- Large company (500-5,000 employees): at least 4 keyword combinations, all pages
- Enterprise (5,000+ employees like Desjardins, Bell, BNY, Citi): at minimum 6 keyword combinations, all pages. Expect 10+ qualified targets. If you are finding fewer than 5, you have not searched enough.

- **Secondary titles (search these if primary turns up few results, or for any enterprise company):**
  - Senior Infrastructure Engineer, Systems Engineer, Systems Administrator
  - Storage Engineer, Storage Administrator, Virtualization Engineer
  - NOC Manager, Director of IT Operations, VP of Technology
  - Head of IT, Technology Manager, Director of IT Operations

### Step 2 — Read EVERY relevant profile in full

**There is no cap on how many profiles to read. Read every candidate whose title or search result card suggests IT/network/telecom relevance.**

For each candidate, navigate to their actual LinkedIn profile page and read the complete page — not the search result card:
- Full **About** section — expand if truncated
- Every **Experience** entry with full descriptions — expand ALL entries including older roles. Do not stop at the 3-line preview.
- Complete **Skills** list via `/details/skills/` — not just featured skills. Skills are the most important qualification signal.
- **Activity feed** via `/recent-activity/all/` — scroll through the last 3-6 months of posts, reposts, and comments. Look for technical signals (400G, DWDM, DIMMs, network refresh, vendor changes, migration projects, AI buildout), pain points voiced publicly, vendors name-checked positively or negatively, industry events attended, and anything specific about current initiatives. Activity is the richest Personal Hook source.
- **City and state** from their location field
- **Timezone** inferred from city/state using Brian's 6-bucket system

**Do not qualify or disqualify based on the search result card or title alone. You must read the full profile every time. A person titled "Conseiller Architecture Détaillée" could be a server admin or a DWDM architect — you cannot tell without reading the actual profile. A person titled "Infrastructure Architect" could be a VMware admin or a network architect — same problem. Title alone means nothing. Read the profile.**

Do not skim previews from search results. Navigate to the actual profile every time.

### Step 3 — Return a ranked shortlist
Return ALL qualified prospects ranked: ✅ Yes first, then ⚠️ Conditional, then ❌ No with brief reasons. For each Yes, include the recommended OSI angle. There is no cap — if you find 15 qualified targets, return all 15.

### Step 4 — HubSpot check on the shortlist
After ranking, check HubSpot for the top targets. Flag any that are already owned or have prior touchpoints before Brian reaches out.

---

## MODE 3: HubSpot Task Mode — batch enrollment from HubSpot tasks

**Triggered by:** "run sequences for my enroll tasks", "check my enroll tasks", "process enroll tasks", or any reference to HubSpot "Enroll in sequence" tasks.

Brian creates a TODO task on a contact in HubSpot with the subject exactly **"Enroll in sequence"** (no priority, no other fields needed -- the contact association carries all the context). This mode finds those tasks, qualifies each contact, and hands qualified contacts off to osi-outreach-sequence.

**Step by step:**

1. Search HubSpot for all incomplete TODO tasks with subject "Enroll in sequence" owned by Brian (hubspot_owner_id: 213536174). Use `search_crm_objects` on tasks with filters: `hs_task_subject = "Enroll in sequence"` AND `hs_task_status != "COMPLETED"` AND `hubspot_owner_id = 213536174`.

2. For each task, pull the associated contact record. Get: first name, last name, job title, company, email, phone, mobile, timezone, LinkedIn URL. If the task has no contact association, skip it and note the issue.

3. **Active Sequence Check.** Check email-queue.json for pending entries matching this contact (by email address OR by prospectName + company). If already enrolled, mark the HubSpot task complete with note "Already enrolled -- skipped" and move on. Do NOT re-enroll.

4. **Blocked Address Check.** If an email address exists for this contact, run the Blocked Address Check (see section below) against that specific address before proceeding. If the address has a prior bounce, create the LinkedIn InMail fallback tasks and mark the HubSpot task complete with note "Blocked address -- LinkedIn InMail fallback created."

5. **Qualification check.** If the contact already has a strategy note in HubSpot, skip re-running qualification -- pull the Personal Hook and ENROLL IN CALLS SEQUENCE label directly from the existing note. If no strategy note exists, run Profile Mode on the contact's LinkedIn URL. If qualification returns No or Conditional: mark the HubSpot task complete with note "Not qualified -- [reason]" and move on.

6. For each qualified contact with a valid email: end with the standard HANDOFF instruction to invoke osi-outreach-sequence. Outreach handles stagger math, email drafting, queue writing, and LINKED_IN_CONNECT due date update.

7. After osi-outreach-sequence confirms enrollment: mark the HubSpot task complete by calling `manage_crm_objects` updateRequest on the task with `hs_task_status: "COMPLETED"`.

8. After all tasks are processed, report a clean summary to Brian:
    - Enrolled: [N] (names and companies)
    - Already in queue -- skipped: [N] (names)
    - Blocked address -- LinkedIn fallback: [N] (names)
    - Not qualified -- skipped: [N] (names, reason)
    - No email -- LinkedIn fallback: [N] (names)

**Key rules:**
- No "ready" gate. Brian decided by tagging the task. Run fully automated.
- Never filter by priority. Brian leaves it blank. Match on subject and owner only.
- Brian does NOT need to put name or company in the task title. Pull everything from the contact association.
- Multiple people from the same company are expected. Stagger math is handled by osi-outreach-sequence after handoff.
- This mode can run daytime or overnight.

---

## CONTACT VERIFICATION PROTOCOL

When asked to confirm whether existing HubSpot contacts are still at a company:

### Step 1 — Search Sales Navigator with the correct company ID
Use the correct LinkedIn company ID for the target company — do not guess or reuse IDs from previous sessions. To find the correct ID, navigate to the company's Sales Nav page and extract the ID from the URL (`/sales/company/[ID]`). Known IDs:
- **BNY Mellon** (post-2024 rebrand: "BNY"): LinkedIn company ID **162750**. Note: after BNY's 2024 rebrand, some employees may appear under a separate "BNY" entity with a different ID — if Sales Nav returns 0 results, do not assume they've left; verify using steps below.

**When adding or verifying a contact for HubSpot:** always capture their LinkedIn Sales Navigator URL (format: `https://www.linkedin.com/sales/lead/[ID]/`) from their Sales Nav profile page. Use this as the `linkedin` field value in HubSpot — not the regular linkedin.com/in/ URL. If the Sales Nav URL cannot be found, Google "[first name] [last name] [company name]" to confirm their current role and employer before creating the record.

### Step 2 — If Sales Nav returns 0 results, do NOT conclude they've left
Zero results from a company filter search does not confirm departure. It may mean:
- The company rebranded and employees are now under a different LinkedIn entity
- The person has a private or restricted profile
- A name variation (e.g., "Brian" vs. "Bryan")

**Mandatory fallback: Google "[first name] [last name] [company name]"** — people almost always show up this way. Use WebSearch.

### Step 3 — Navigate to their full LinkedIn profile
Once found, navigate directly to the profile and read:
- Full **About** section — current status and any "open to work" signals
- All **Experience** entries — confirm their current employer and start date
- Note if they're between roles (no current employer listed = job seeking)

### Step 4 — Report findings accurately
- Still at company → flag as current contact, note their title and how long in current role
- Left company → note new employer if found; new employer is a potential fresh target
- Between roles / job seeking → note as currently inactive; monitor for new placement
- Can't locate → say so explicitly; do not assume still at company

---

## THREE-POINT QUALIFICATION CHECK (Both Modes)

Evaluate every prospect on all three signals. Never skip one.

### 1. Current Role (Most Important)
- What is their exact title?
- Does it touch networking, compute, storage, IT infrastructure, or IT operations?
- Are they in a buying, influencing, or purely technical/operational role?
- How long have they been in this role?

### 2. Past Roles (Trajectory)
- Has their career moved toward or away from the areas OSI sells into?
- Have they left IT/networking for HR, finance, facilities, or other unrelated functions?
- A strong past in networking means nothing if their current role is irrelevant
- A sourcing background is relevant if they're sourcing IT hardware — not just facility services

### 3. Skills
- Read every skill — featured AND full list via `/details/skills/`
- Skills confirm or contradict the title. They are the most objective signal.
- Look for keywords: Cisco, Juniper, networking, switches, routers, DWDM, optics, servers, storage, infrastructure, data center, cloud, virtualization, etc.
- Endorsement counts matter — a skill with 50+ endorsements is stronger than one with 2
- A person titled "VP Sales" with skills in Salesforce, negotiation, and CRM is not a fit. A person titled "Manager Facilities" with skills in HVAC, vendor management, and real estate is not a fit.
- A person titled "Network Engineer" with skills in DWDM, Catalyst, Juniper, and optical is a strong fit

**Verdict:**
- ✅ **Yes:** All three signals point to strong fit — current role is relevant, trajectory supports IT/infrastructure, and skills confirm expertise
- ⚠️ **Conditional:** Two signals are strong, one is weak or absent — OR strong current role but weak trajectory — OR clear skills but title doesn't match
- ❌ **No:** Current role is unrelated to IT/infrastructure OR trajectory moved away from IT OR skills don't support the title

---

## QUICK-CONNECT KEYWORDS

Extract 5-10 keywords from the prospect's LinkedIn profile. Use these in the LIVE CALL SCRIPT to establish familiarity and credibility. Keywords come from:
- **Job titles** (current and recent past)
- **Key skills** (featured + full list, endorsement counts > 10)
- **Company context** (industry, scale, recent news)
- **Activity** (posts, reposts, comments — specific tech names they mention)
- **Education** (degree, school, certifications)

Example keywords for a "Senior Network Engineer at a financial services company":
- Network engineering, Catalyst switches, DWDM, enterprise architecture, data center, financial services, telecom

---

## THE THREE SCRIPTS

### LIVE CALL SCRIPT — OPENER

**Purpose:** Land the first 20 seconds of the call. Hook them with something specific they care about (the Personal Hook). State your purpose clearly.

**Format:**
```
Hi [First name], this is [Your name] with [Company]. I was [impressed by / following] your [specific thing from their LinkedIn — a skill, a post, an achievement, a company initiative]. Given your background in [area], I thought there might be a fit to explore with [broad OSI angle]. Would you be open to a quick conversation?
```

**Rules:**
- Reference ONE specific thing from their LinkedIn (not vague)
- Tie it to ONE broad OSI angle (network infrastructure, pre-owned hardware, cost optimization, etc.)
- Ask for permission to continue (would you be open to...)
- Keep it under 30 seconds

**Example:**
```
Hi Jeremy, this is Brian Charrette with OSI Global. I've been following your work in network infrastructure at NIST, and I'm impressed by your expertise in DWDM architecture and optical engineering. Given your background in modernizing network infrastructure at scale, I thought there might be a fit to explore with how we help organizations extend their Cisco infrastructure lifecycle through third-party maintenance. Would you be open to a quick conversation?
```

---

### VOICEMAIL SCRIPT — 40-50 seconds

**Purpose:** Leave a professional, warm message that references the Personal Hook and makes them curious to call back or read your email.

**Format:**
```
Hi [First name], this is [Your name] with [Company]. I was [impressed by / came across] your [specific thing from LinkedIn]. We work with [organization type] in [area] — helping them [specific value prop]. I thought there might be something worth exploring. [Phone]. [Closing].
```

**Rules:**
- Reference ONE specific thing from their LinkedIn
- State what you do and who you help (one sentence)
- Say why you're calling (one sentence)
- Leave your number clearly
- Be warm, not pushy
- Total time: 40-50 seconds (read it aloud to time it)

**Example:**
```
Hi Jeremy, this is Brian Charrette from OSI Global. I saw your recent post about modernizing NIST's network infrastructure using DWDM technology — that's exactly what we focus on. We work with federal agencies and large enterprises to help them extend their Cisco infrastructure lifecycle while saving 30 to 50 percent on maintenance costs. I thought there might be something worth a conversation. My number is [phone]. Looking forward to connecting.
```

---

### THE PLAY — Prospect Narrative

**Purpose:** Summarize who the prospect is, what they do, why they matter to OSI, and how to position the conversation.

**Format:**
```
[Prospect name] is a [title] at [company] with [key background]. [Company] is [industry / scale / relevant initiative]. [Prospect] is responsible for [key area]. OSI can help with [specific angle] — [specific reason why this matters to this company].
```

**Rules:**
- 3-4 sentences max
- Include tenure (how long in role, how long at company)
- Name the specific initiative or pain point you're targeting
- State the OSI angle clearly
- Tie prospect's role to buying power or influence

**Example:**
```
Jeremy is a Senior Network Engineer at NIST managing enterprise Catalyst Switch infrastructure and network access control (NAC) across a federal research agency. NIST operates critical network infrastructure serving the nation's scientific mission and is undergoing a major network modernization to 400G and DWDM over the next 18 months. Jeremy is responsible for day-to-day operations, infrastructure design, and vendor evaluation. OSI can help with cost-effective pre-owned Catalyst switches and third-party maintenance (TPM) to reduce government IT budget pressure while modernizing the transport layer.
```

---

## THE PERSONAL HOOK

**Purpose:** A specific, dated, verifiable thing you found on their LinkedIn that proves you read their profile and is relevant to your pitch.

**Rules:**
- Must be **specific** — not generic
- Must be **recent** — from activity, recent roles, or current projects
- Must be **actionable** — tie it to your pitch
- Must be **true** — never make something up or exaggerate
- Should come from **activity first**, then recent roles, then skills, then about

**Where to find it:**
1. **Activity feed** (best) — posts, reposts, comments from the last 3-6 months. Look for technical language, specific projects, vendors mentioned, pain points voiced, certifications announced, promotions, event attendance, etc.
2. **Experience** — current role description, recent past roles, keywords in descriptions
3. **Skills** — if they've recently added a skill with high endorsements
4. **About** section — if they mention a specific initiative or passion
5. **Certifications** — if they recently completed a relevant cert

**Example Personal Hooks:**

Good:
- "You recently posted about leading a network refresh to DWDM technology — that's exactly what we specialize in"
- "I saw you've been working on Catalyst Switch infrastructure modernization at NIST — we've sourced thousands of those units"
- "Your background in government IT infrastructure is impressive — federal agencies are exactly who we work with"

Bad:
- "I saw you work in IT" (too generic)
- "You seem smart" (no proof)
- "You work at a company" (no specificity)
- "I know someone who knows you" (not LinkedIn data)

---

## After generating the outreach package — save to HubSpot automatically

**CRITICAL SEPARATION OF CONCERNS:**
- **CONTACT NOTES** (HubSpot `notes` engagement, associated to the contact) = Full strategy information (keywords, call script, VM script, The Play, Personal Hook). These appear in the Notes section / Activities tab on the contact page.
- **TASK NOTES** (`hs_task_body` field on LINKED_IN_CONNECT task) = LinkedIn invitation text ONLY

**EVERYONE regardless of data available:**
- LinkedIn connection request task — always created (notes field contains ONLY LinkedIn invite text)
- Strategy note — always saved as a HubSpot `notes` engagement associated to the contact (NOT as a `notes_` contact property, NOT in the task body, NOT skipped)
- No email or call tasks. The contact strategy note captures quick-connect keywords, call script, voicemail, The Play, and the Personal Hook only. Email creation and scheduling is handled by the `osi-outreach-sequence` skill.

---

### CONTACT NOTES — Strategy Information (saved as a HubSpot Notes Engagement)

This note is created as a HubSpot `notes` engagement and associated to the contact. It appears in the **Notes** tab / Activities feed on the contact page.

**How to save:** The `manage_crm_objects` API silently fails for notes (returns success but saves nothing). Use the browser instead:

1. Navigate to the contact record: `https://app.hubspot.com/contacts/21878985/record/0-1/<contactId>/view/1`
2. Click the **Note** button (notepad icon, top of the activity section)
3. Click in the note text area ("Start typing to leave a note...")
4. Type the full strategy note content
5. Click **Create note**

**Location in HubSpot:** Open the contact record → Activities tab → Notes filter. The note appears immediately after clicking Create note.

**Format:**
```
[QUICK CONNECT KEYWORDS]
[list of keywords from profile, recent activity, skills, and conversation]

[LIVE CALL SCRIPT]
OPENER: [2-3 sentence opening that references the Personal Hook]
VM: [40-50 second voicemail that references the Personal Hook]

[THE PLAY]
[2-3 sentence narrative: who they are, what they do, why they matter to OSI]

[THE PERSONAL HOOK]
[1-2 sentences: what you found in their LinkedIn that caught your attention — activity, skill, achievement, or conversation]
```

**Example:**
```
[QUICK CONNECT KEYWORDS]
network infrastructure, DWDM, Catalyst switches, optical engineer, transport engineering

[LIVE CALL SCRIPT]
OPENER: Hi Jeremy, I've been following your work in network infrastructure at NIST and I'm impressed by your deep expertise in DWDM architecture. Would love to connect and explore how OSI's infrastructure solutions might support your team.
VM: Hi Jeremy, this is Brian Charrette from OSI Global. I was impressed by your extensive background in network infrastructure and Catalyst switches — we work with a lot of organizations like NIST who are modernizing their transport layer, and I thought there might be a fit to explore. If you're open to a quick conversation, I'd love to connect. My number is [phone]. Thanks.

[THE PLAY]
Jeremy is a Senior Network Engineer at NIST who leads network infrastructure and operates a large deployment of Catalyst switches across the organization. NIST is modernizing their network to 400G and DWDM over the next 18 months — a perfect fit for OSI's optics and pre-owned Catalyst inventory.

[THE PERSONAL HOOK]
Jeremy posted about leading a network refresh project using advanced DWDM technology, which directly aligns with OSI's Smart Optics partnership and our pre-owned inventory sourcing model.
```

---

### TASK NOTES (hs_task_body field) — LinkedIn Invitation ONLY

This note is saved to the TASK RECORD (LINKED_IN_CONNECT task), not to the contact.

**Location in HubSpot:** Open the task > Notes field

**Format:**
```
[LinkedIn invitation text ONLY — under 300 characters. Low friction. References the Personal Hook. No mention of mutual connections.]
```

**Example:**
```
Hi Jeremy, I've been impressed by your extensive background in network infrastructure and Catalyst switches at NIST. Would love to connect and explore how OSI's solutions might support your team. Looking forward to connecting. - Brian Charrette, OSI Global
```

**Rules:**
- No call scripts in task notes
- No voicemail in task notes
- No keywords in task notes
- Just the LinkedIn invitation — cordial, brief, specific to one thing you admired
- Always under 300 characters so it fits in a LinkedIn message

---

### Task housekeeping — always do this first

Before creating any task, check whether one already exists for this contact.

**Search HubSpot for existing LINKED_IN_CONNECT tasks on this contact.**
- If found and NOT COMPLETED: mark it COMPLETED first (so you don't create a duplicate)
- If found and COMPLETED: proceed (you can create a fresh task)
- If NOT found: proceed to create

### 3. Create a HubSpot LinkedIn Connection Request task — EVERYONE:

   - Subject: "Sales Nav -- Send connection request -- [First Last] | [Company]"
   - Type: LINKED_IN_CONNECT
   - Due: Next business day (provisional — osi-outreach-sequence updates this to final Day 1 after stagger math)
   - Owner: 213536174
   - hs_task_body (Notes field): LinkedIn invitation text ONLY
   
   **Pre-creation checklist:**
   - Check for existing LINKED_IN_CONNECT task on this contact. If exists, delete or mark COMPLETED.
   - Never create duplicate connection request tasks for same person.
   - Ensure Notes field contains ONLY the LinkedIn invitation (300 chars max).

---

## BLOCKED ADDRESS CHECK

Before handing off to osi-outreach-sequence, confirm that the prospect's email address has not previously bounced.

**Why:** If an address bounced before, email deliverability is compromised and the 7-email sequence will fail. LinkedIn InMail fallback tasks are the only option.

**How:**
1. Pull the prospect's email address from ZoomInfo or HubSpot
2. Search the email-queue.json for any prior sends to that address
3. Check the `bounced_addresses.json` file (if it exists) for hard bounces
4. If a bounce is found: do NOT proceed to osi-outreach-sequence. Instead, create two LinkedIn InMail fallback tasks (see below) and stop.
5. If no bounce: proceed to HANDOFF

---

## NO-EMAIL-NO-PHONE FALLBACK — LinkedIn InMail Tasks

If ZoomInfo returned NO email and NO phone, email + call outreach is impossible. Create LinkedIn InMail fallback tasks instead.

**Create TWO LinkedIn InMail tasks:**

**Task 1: First InMail (Day 3)**
- Subject: "LinkedIn InMail — [First Last] | [Company]"
- Type: LINKEDIN_INMAIL
- Due: Day 3 (3 business days after Email 1 would have fired)
- Notes: [LinkedIn InMail message text — 200-250 characters, warm, references Personal Hook]
- Owner: 213536174

**Task 2: Follow-up InMail (Day 10)**
- Subject: "LinkedIn InMail follow-up — [First Last] | [Company]"
- Type: LINKEDIN_INMAIL
- Due: Day 10 (10 business days after Email 1 would have fired)
- Notes: [LinkedIn InMail follow-up text — slightly different angle, still warm, still references Personal Hook]
- Owner: 213536174

**After creating fallback tasks, STOP.** Do NOT invoke osi-outreach-sequence. The contact is qualified but unreachable via email/phone.

---

## HANDOFF — Ready for osi-outreach-sequence

When you have:
- ✅ A Yes verdict
- ✅ A valid email from ZoomInfo (not bounced)
- ✅ A strategy note saved to the contact's notes_ field in HubSpot
- ✅ A LINKED_IN_CONNECT task created with LinkedIn invite text in the notes field
- ✅ An approved vendor flag (YES or NO)

**End with this exact handoff instruction:**

```
---

## HANDOFF to osi-outreach-sequence

This prospect is **READY FOR EMAIL OUTREACH**.

**Prospect:** [First Last] | [Company] | [LinkedIn URL]
**Contact ID:** [HubSpot contact ID]
**Email:** [email address]
**Timezone:** [timezone bucket]
**Verdict:** ✅ Yes
**Strategy Note:** Saved as HubSpot `notes` engagement (associated to contact, visible in Notes tab)
**LinkedIn Task:** Created (due [date], notes contain invitation only)
**Approved Vendor:** [YES / NO]

**Invoke osi-outreach-sequence** with these inputs:
- Contact ID: [HubSpot contact ID]
- Timezone: [timezone bucket]
- Approved Vendor flag: [YES / NO]

The outreach-sequence skill will:
1. Verify active sequence check (no duplicate enrollment)
2. Draft 6 personalized emails
3. Write email-queue.json
4. Update the LINKED_IN_CONNECT task due date to match Email 1's send time
5. Schedule all sends

Ready to go.
```

---

## RULES & REFERENCE

### Timezone Buckets (Brian's 6-bucket system)

Map city/state to one of these buckets for stagger math:

1. **us_slash_eastern** — East Coast (EST/EDT): Boston, New York, DC, Atlanta, Miami, etc.
2. **us_slash_central** — Central (CST/CDT): Chicago, Dallas, Houston, Denver, etc.
3. **us_slash_mountain** — Mountain (MST/MDT): Denver, Phoenix, Salt Lake City, etc.
4. **us_slash_pacific** — West Coast (PST/PDT): Seattle, San Francisco, Los Angeles, Las Vegas, etc.
5. **canada_slash_eastern** — Canada Eastern (EST/EDT/AST): Toronto, Montreal, Vancouver BC (no — that's West), Halifax, etc.
6. **canada_slash_central** — Canada Central (CST/CDT): Winnipeg, Calgary, Edmonton, etc.

If the prospect's location is not listed, infer the bucket from the state or city. US only. If international, pause and ask Brian.

### Email Requirements

Email is required to proceed to osi-outreach-sequence. Phone is optional. Mobile is optional.

**Valid sources:**
- ZoomInfo (preferred — most reliable)
- HubSpot (if already on file)
- LinkedIn profile (only if explicitly listed in About section; rarely accurate)
- Web search (last resort; requires verification)

**Do NOT guess.** If ZoomInfo returns no email, stop and create InMail fallback tasks.

### Skill Invocation for Mode 1 (Profile Mode)

When Brian provides a LinkedIn profile URL:

1. Run the THREE-POINT QUALIFICATION CHECK
2. Generate the four scripts (keywords, call opener, voicemail, The Play, Personal Hook)
3. Check for existing HubSpot contact by email (ZoomInfo lookup)
4. Create or update contact in HubSpot
5. Save strategy note as a HubSpot `notes` engagement (createRequest, objectType: notes, hs_note_body, associated to the contact)
6. Create LINKED_IN_CONNECT task with LinkedIn invitation text only
7. Check approved vendor status
8. Issue HANDOFF to osi-outreach-sequence if Yes + valid email
9. OR create InMail fallback tasks if No email

### Skill Invocation for Mode 2 (Company Mode)

When Brian provides a company name:

1. Run company pre-checks (OSI fit, M&A, HubSpot ownership)
2. Exhaust LinkedIn keyword searches across all search rounds
3. Read every relevant profile in full
4. Rank all qualified prospects (Yes / Conditional / No)
5. Check HubSpot for top targets
6. Return shortlist with recommended OSI angle for each Yes
7. For each Yes with valid email: issue HANDOFF to osi-outreach-sequence
8. For each Yes with no email: create InMail fallback tasks

### Skill Invocation for Mode 3 (HubSpot Task Mode)

When Brian says "run sequences for my enroll tasks" or similar:

1. Find all "Enroll in sequence" TODO tasks owned by Brian, status NOT_STARTED
2. For each task:
   a. Pull associated contact
   b. Run active sequence check (skip if already enrolled)
   c. Run blocked address check (create InMail fallback if bounce detected)
   d. Run qualification check (use existing strategy note if available)
   e. Hand off to osi-outreach-sequence if qualified + valid email
3. Mark HubSpot task COMPLETED after enrollment or skip
4. Report summary to Brian

---

## Quality Checks

Before ending a skill run:

- [ ] Did I read the full LinkedIn profile (About, Experience, Skills, Activity)?
- [ ] Did I apply all three qualification signals (Current Role, Trajectory, Skills)?
- [ ] Did I extract specific, actionable keywords from the profile?
- [ ] Did I write scripts that reference the Personal Hook, not generic OSI angles?
- [ ] Did I verify the email address (ZoomInfo, no prior bounce)?
- [ ] Did I create a HubSpot `notes` engagement (createRequest, objectType: notes, hs_note_body) associated to the contact? (NOT a notes_ property update, NOT skipped)
- [ ] Did I create a LINKED_IN_CONNECT task with LinkedIn invitation text ONLY (under 300 chars)?
- [ ] Did I check for approved vendor status?
- [ ] Did I issue a clear HANDOFF instruction to osi-outreach-sequence (or create InMail tasks if no email)?

---

All clear. This skill is ready to use.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      