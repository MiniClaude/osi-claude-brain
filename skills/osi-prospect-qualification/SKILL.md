---
name: osi-prospect-qualification
description: Qualify LinkedIn prospects for OSI Global. Use whenever Andy pastes a LinkedIn profile URL, asks "good target?", "is this worth an InMail?", or asks to evaluate any LinkedIn profile against OSI's product lines. Also triggers when reviewing prospect lists, when Andy says "find me prospects at [company]", or when invoked by the osi-outreach-sequence recurring runner. Should run automatically whenever a LinkedIn profile or company prospecting request appears in conversation, even without explicit ask.
---

> Source: `C:\Claude-Brain\skills\osi-prospect-qualification\` (Git, github.com/Drrewdy/Claude-Brain). Cowork `.claude/skills/` is a copy. Edit source, repackage, install.

# OSI Global — LinkedIn Prospect Qualification

---

## 🚦 WHO OWNS WHAT

Strict boundary with **osi-outreach-sequence**.

| Responsibility | Owner |
|---|---|
| Verdict (✅ Yes / ❌ No / ⚠️ Conditional) | this skill |
| Read LinkedIn profile in full (About, Experience, Skills, Activity) | this skill |
| Resolve LinkedIn URL from name+company | this skill |
| Shallow qualify path for HubSpot-sourced contacts | this skill |
| ZoomInfo enrichment (email, direct phone, mobile) | this skill |
| Strategy note + LINKED_IN_CONNECT task creation | this skill |
| No-email-no-phone LI fallback tasks | this skill |
| Drafting 6 emails, email-queue writes, stagger math, LINKED_IN_CONNECT due_date final | osi-outreach-sequence |
| Excel tracker rows | osi-outreach-sequence |

**Handoff rule:** when verdict is ✅ Yes AND ZoomInfo returns valid email, end with `HANDOFF: invoke osi-outreach-sequence on [First Last] at [Company]...`. If no email, the 2 LI fallback tasks are the complete plan; do NOT hand off.

---

## Role
Sales coach + outreach strategist for OSI Global. Two modes:
1. **Profile Mode** — qualify a single prospect. Three input paths: LinkedIn URL / name+company / HubSpot-sourced queue entry (shallow).
2. **Company Mode** — given a company, find and rank targets (interactive; overnight uses outreach skill's Discovery branch).

Always return a clear Yes / No / Conditional verdict with tight reasoning.

---

## TOOL CHOICE — regular LinkedIn, NOT Sales Navigator

Use `linkedin.com/in/...` for both search and profile reading. Sales Nav pages are heavier and Show more / See all skills buttons are unreliable there.

- Candidate search: regular LinkedIn people search.
- Profile reading: regular LinkedIn profile (expanded About, Experience, Skills, activity feed).
- ZoomInfo: contact-data lookup only (email, direct phone, mobile). NOT for finding IT titles at banks / credit unions / insurance — see warning in Company Mode.
- HubSpot: ownership, company, contact checks.
- Sales Nav URL: save to `hs_linkedin_url` only if easily available; otherwise save the regular `/in/` URL. Do NOT navigate to Sales Nav as part of normal flow.

---

## Approved Vendor Rule

OSI is approved at companies in `Claude-Brain/approved-vendors.json`. Read at write time. Case-insensitive substring match.

**If matched:**
- Email 1: ONE soft acknowledgment. "Side note, we're already on your approved vendor list, so no new vendor onboarding if anything ever needs to move fast."
- One of Email 3 OR Email 4: brief reminder. "Quick reminder we're already approved at [Company] if timing matters."
- Other emails: silent.

**If not matched:** never mention. Don't invent. Never use "vetted" or "pre-approved". Never mention "procurement" in Email 1.

To add a company: edit `Claude-Brain/approved-vendors.json` directly.

---

## MODE 1: Profile Mode (Single prospect)

Three input paths.

### Step 0 — Route the input (check in order)

**Branch 1 — HubSpot-sourced:** if input has `source: "hubspot_contact"` AND `hubspotContactId`, jump to **SHALLOW QUALIFY PATH** below. Skip Step 1.

**Branch 2 — URL provided:** proceed to Step 1 with that URL.

**Branch 3 — Name + company only:** resolve URL first.
1. Search LinkedIn people for `"[First Last]" "[Company]"`.
2. Exactly one match → use it, proceed to Step 1.
3. Multiple matches → pick the one whose current company matches. If still ambiguous, fall back to web search `site:linkedin.com/in/ "[First Last]" "[Company]"`, take first result that resolves.
4. No match → mark candidate `no` reason "could not resolve LinkedIn profile". Exit. Do NOT guess a URL.

### Step 1 — Read the Full LinkedIn Profile

Navigate to the URL. Expand and read EVERYTHING:
- Full **About** — click Show more if truncated.
- Every **Experience** entry — expand all role descriptions, including older roles.
- Complete **Skills** list via `/details/skills/` — endorsement counts.
- **Activity feed** via `/recent-activity/all/` — last 3-6 months of posts, reposts, comments. Look for technical signals (400G, DWDM, DIMMs, network refresh, vendor changes, AI buildout), pain points, vendors name-checked, certifications, current initiatives. Activity is the richest Personal Hook source.
- **City + state** from location field — required for HubSpot.
- **Timezone** from city/state per Andy's 6-bucket system (see hubspot-data-quality.md).

> Skills = most important qualification signal. Activity = most important personalization signal. Never qualify on title alone. Never skim search result previews — always navigate to the actual profile page.

---

## SHALLOW QUALIFY PATH — HubSpot-sourced only

When candidate has `source: "hubspot_contact"` AND a valid `hubspotContactId`, the deep profile read is overkill. HubSpot-sourced contacts already passed human judgment.

**Use shallow only when ALL true:**
- `source: "hubspot_contact"` with `hubspotContactId`, AND
- HubSpot record has `email`, `jobtitle`, `company` populated, AND
- Owned by JAM (Andy 196669355 / Mark 210187184 / John 210187193).

If ANY fails → fall back to deep Profile Mode.

### Shallow Qualify steps

1. **Pull HubSpot contact** via `get_crm_objects` with the `hubspotContactId`. Read: firstname, lastname, jobtitle, company, email, phone, mobilephone, city, state, hs_timezone, hs_linkedin_url, notes_last_contacted.

2. **ICP check by title + vertical** — apply DISQUALIFIERS list. If title fits an OSI product line and company fits a vertical (telco / bank / manufacturing / healthcare / consulting / enterprise IT) → ✅ Yes. If title is clearly off (HR, Finance, Facilities M&E, Legal, Marketing) → ❌ No. If ambiguous → fall back to deep, do NOT guess.

3. **Active sequence check** — per outreach skill rule. Skip if already enrolled or recently sent.

4. **ZoomInfo enrichment** — only if HubSpot is missing `email`, `phone`, or `mobilephone` properly formatted. If all three populated and phone formatted `+1 (XXX) XXX-XXXX`, skip ZoomInfo entirely.

5. **LinkedIn URL resolution** — if `hs_linkedin_url` populated, use it. If not, one-shot LinkedIn search by name+company; write back to HubSpot if resolved. If fails, proceed without — LINKED_IN_CONNECT task surfaces it for manual lookup.

6. **Personal Hook** — thinner without deep read. Build from: previous employers (HubSpot notes), recent contact history, company news (`enrich_scoops` or `enrich_news` one quick call), or vertical-specific hook fallback ("ran into the same cable MSO transport lead-time squeeze last week at [peer company]").

7. **Generate outreach package** — strategy note, LINKED_IN_CONNECT task, call script, VM, LinkedIn invite, Email 1 opener with Personal Hook. Annotate strategy note with `SOURCE: HubSpot shallow qualify`.

8. **Handoff** to osi-outreach-sequence — same format as deep path.

### When to escalate back to deep
- Vague title ("IT Specialist", "Technology Manager" with no industry clue)
- Thin HubSpot record (only name + email)
- 2+ years old with no recent touchpoint
- Anything that makes you unsure — default to deep. Wrong Yes wastes more time than 2 extra minutes of profile reading.

---

## MODE 2: Company Mode

When Andy says "find me prospects at [Company]" interactively. (Overnight uses outreach skill's Discovery branch instead — same logic, scheduled.)

### Step 0 — Company pre-checks

**A. OSI fit check** — only if the company was picked automatically (not named by Andy, not pre-vetted by outreach Kickoff). If interactive Company Mode and Andy named the company, skip.

**B. M&A check** — recent acquisitions, mergers, rebrands. May change company name in HubSpot. People who left to new companies are separate clean targets.

**C. HubSpot ownership** (JAM tree):
- Not in HubSpot → proceed.
- JAM-owned → proceed.
- Other rep, recent activity (within 3 months) → skip silent.
- Other rep, no activity 3+ months, not a client → log for account-request, do NOT prospect.

### Step 1 — LinkedIn candidate search

**Exhaust the search.** Finding 1-2 and stopping is not acceptable. Large companies have dozens of relevant targets.

**Round 1 — English priority titles:**
- "network engineer" OR "network architect"
- "transport engineer" OR "optical engineer" OR "DWDM"
- "IT infrastructure" OR "infrastructure architect"
- "data center manager" OR "data center engineer"
- "IT asset manager" OR "IT vendor manager"
- "telecom" OR "telecommunications engineer"

**Round 2 — French keywords (REQUIRED for Quebec: Desjardins, National Bank, Caisse, Hydro-Quebec, Bell, Videotron, Cogeco):**
- "ingénieur réseau" OR "architecte réseau"
- "architecte télécom" OR "ingénieur télécom"
- "infrastructure TI" OR "architecte infrastructure"
- "architecture détaillée" OR "expert télécom"
- "conception réseaux" OR "opérations télécom"

**Round 3 — Secondary titles (when round 1-2 thin, or for any enterprise company):**
- Senior Infrastructure Engineer, Systems Engineer / Administrator
- Storage Engineer / Administrator, Virtualization Engineer
- NOC Manager, Director of IT Operations, VP of Technology
- Head of IT, Technology Manager

**Pagination — non-negotiable:** every page of every search until LinkedIn says no more. Don't stop at page 1-2. 10 pages = read all 10.

**ZoomInfo warning for large financial institutions** (Desjardins, National Bank, Caisse Desjardins, Intact, etc.): ZoomInfo is UNRELIABLE — its keyword matching returns branch network directors / distribution network managers / sales network roles, not IT. Use LinkedIn directly with the keyword rounds above.

**Minimum effort:**
- Small/mid (< 500 emp): ≥ 2 keyword combinations, all pages.
- Large (500-5,000): ≥ 4 combinations, all pages.
- Enterprise (5,000+: Desjardins, Bell, BNY, Citi): ≥ 6 combinations. Expect 10+ qualified. <5 found = haven't searched enough.

### Step 2 — Read EVERY relevant profile in full

No cap. Every candidate whose result card suggests IT/network/telecom relevance gets a full profile read (About, Experience, Skills via `/details/skills/`, Activity, city/state, timezone bucket).

**Title alone means nothing.** "Conseiller Architecture Détaillée" could be server admin or DWDM architect. "Infrastructure Architect" could be VMware or network. Read the profile every time.

### Step 3 — Return ranked shortlist
✅ Yes first, then ⚠️ Conditional, then ❌ No with brief reasons. No cap on Yes count. Each Yes includes recommended OSI angle.

### Step 4 — HubSpot check on shortlist
Flag any already owned or with prior touchpoints before Andy reaches out.

---

## CONTACT VERIFICATION PROTOCOL

When confirming if existing HubSpot contacts are still at a company:

1. Search Sales Navigator with the correct company ID (find it in `/sales/company/[ID]` URL). **BNY Mellon**: company ID `162750` post-2024 rebrand. If 0 results, do NOT conclude they've left — could be rebrand, private profile, or name variation.
2. **Mandatory fallback:** Google `"[First Last]" "[Company]"` via WebSearch. People almost always show up.
3. Navigate to LinkedIn profile, read About + Experience entries to confirm current employer + start date.
4. Report: still at company / left (note new employer if found, fresh target candidate) / between roles / can't locate (say so explicitly).

---

## THREE-POINT QUALIFICATION CHECK

Evaluate every prospect on all three. Never skip.

### 1. Current Role (most important)
- Exact title? Does it touch networking / compute / storage / IT infrastructure / IT operations?
- Buying / influencing / purely technical-operational?
- How long in role?

### 2. Past Roles (trajectory)
- Career moved toward or away from OSI's world?
- Left IT/networking for HR / finance / facilities / unrelated?
- Strong networking past + irrelevant current = nothing. Sourcing background = relevant only if covering IT hardware (not facility services).

### 3. Skills
- Read EVERY skill — featured AND full list via `/details/skills/`.
- **Green flags:** Data Center, Networking, Network Architecture, IT Infrastructure, IT Operations, Cloud Computing, Vendor Management, Storage, Compute, VMware, Cisco, Dell, HP, DWDM, Fiber Optics, Optical Networking, Capacity Planning, ITIL, Disaster Recovery.
- **Red flags:** only M&E (chillers, generators, UPS, HVAC), only facility services (carrier hotel, colocation), only HR/finance/marketing.

---

## 🛑 STOP-GATE — No / Conditional verdicts

The instant a verdict forms:
- **❌ No or ⚠️ Conditional:** STOP. No ZoomInfo. No HubSpot contact create/update. No strategy note. No tasks. Log to output (Excel tracker if Company Mode). Move to next.
- **✅ Yes:** proceed to ZoomInfo enrichment + HubSpot save + outreach package.

HubSpot slots and ZoomInfo credits are reserved for ✅ Yes only.

---

## ZOOMINFO ENRICHMENT — every ✅ Yes verdict

After Yes verdict (and stop-gate), enrich before any HubSpot write or outreach.

### What to pull
`enrich_contacts` with required fields: `email`, `phone` (direct dial — NOT company main), `mobilePhone`.

```
enrich_contacts({
  contacts: [{firstName, lastName, companyName}],
  requiredFields: ["email", "phone", "mobilePhone"]
})
```

If empty, retry with `jobTitle` added. If still nothing, mark `yes-no-email`, create 2 LI fallback tasks, do NOT hand off to outreach.

### Results
- Email found → HubSpot `email`.
- Direct phone → HubSpot `phone`.
- Mobile → HubSpot `mobilephone`.
- Nothing → "ZoomInfo: no data found". `yes-no-email` path.
- Never confuse direct phone with company main.

City / state / timezone → ALWAYS LinkedIn, NEVER ZoomInfo.

### Email domain validation — before handoff to outreach

ONE web search to confirm the email domain is the company's corporate domain, not consumer ISP / subsidiary brand / stale pre-acquisition.

Search: `"[Company name] corporate email domain"`

- Match → proceed.
- Consumer ISP / residential brand / dead domain → invalid. Flag, do NOT queue, pattern-match real corporate domain or hand back to Andy.

Examples to catch: Altafiber employees with `@zoomtown.com`; post-acquisition employees on dead domain; franchise operators on franchisor's consumer system.

One search, no rabbit holes.

---

## DISQUALIFIERS (Hard No)

- Current role is **Facilities / M&E** (chillers, generators, UPS, PDUs).
- Current role is HR / Finance / Legal / Marketing / Sales with no IT infrastructure component.
- Skills entirely facility services (carrier hotel, colocation, HVAC, electrical).
- Career fully moved away from IT/networking, no return.
- Hyperscaler (Meta, Google, AWS, Microsoft) building fully custom — only proceed if you can identify a specific hardware procurement function.

---

## CONDITIONAL QUALIFIERS

- Title right but they're a **planner / optimizer** rather than buyer — influencer or path to buyer.
- **Sourcing professional** — only proceed if category covers IT hardware (not facility services or wireless mobility).
- **Restricted profile** (2nd/3rd connection, skills hidden) — qualify on what's available, revisit after connect.
- **Recently changed roles** — verify new role before assuming old role's relevance carries over.

---

## REAL EXAMPLES

| Prospect | Title | Company | Verdict | Reason |
|---|---|---|---|---|
| William Clarke | Facilities Supervisor | ISS | ❌ No | M&E only — chillers, generators. No IT hardware skills. |
| Onur Turkcu | Backbone Network Planner | Meta | ⚠️ Conditional | Right space (DWDM, ex-Infinera), but planner not buyer. Meta builds custom. Path to buyer only. |
| Ron Kemp | VP IT Infrastructure & Operations | Precision Castparts | ✅ Yes | 30yr IT infra, manages vendors, global manufacturer — TPM + servers + VMware wedge. |
| John Lee | Senior Manager Infrastructure | Wells Fargo | ✅ Yes | Data Center Engineering at major bank, 35 endorsements DC + Vendor Management. Strong TPM. |
| FNU Avantika | Associate Director, Network Technology | AT&T | ✅ Yes | Strategic sourcing/procurement embedded in AT&T Network Technology. Lead with cost savings. |

---

## HubSpot writes — for every ✅ Yes verdict

Always create regardless of data:
- LinkedIn connection request task (provisional due_date — outreach updates).
- Strategy and Fit note.

Email creation, scheduling, and the 6-email sequence are owned by `osi-outreach-sequence`, NOT here.

### Data quality requirements

Read **`C:\Claude-Brain\playbook\hubspot-data-quality.md`** for required fields, phone format, mobile rule, timezone bucket, pre-write checklist. Hard requirements — don't skip.

### Step 1: Create or update contact record

All required fields per data-quality playbook. If prospect not in HubSpot, create them first (linked to company) before note + tasks.

### Step 2: Create Strategy and Fit note

objectType: `notes`, owner: 196669355, associated to contact.

```
QUICK CONNECT KEYWORDS
[6-10 keywords, one line]

LIVE CALL SCRIPT (omit entire section if no phone)
OPENER: [full opener from playbook/opener-library.md]
VM: [one line, 15s max. One-sentence hook. "I'm sending you something right now, subject line is [Email 1 subject]." Ends with "that's andy at osiglobal dot com." Present/future tense only.]

THE PLAY
[One paragraph: why they qualify + the hook + the attack plan. Include Previous Employer OSI Client Check ONLY if a HubSpot match was found.]

THE PERSONAL HOOK
[1-2 specific LinkedIn details that anchor Email 1 + LinkedIn invite when outreach runs.]
```

Never use em-dashes anywhere in the note.

### Step 3: Create LINKED_IN_CONNECT task — every ✅ Yes

Task housekeeping first: if prospect has an existing `LINKED_IN_CONNECT` task (e.g., "Sales Nav -- Send connection request"), mark it COMPLETED via `manage_crm_objects` updateRequest before creating the new one.

Create:
- Subject: `Sales Nav -- Send connection request -- [First Last] | [Company]`
- Type: `LINKED_IN_CONNECT` (never `LINKED_IN_MESSAGE`, never `TODO`)
- Due: provisional next business day — outreach updates to Email 1 Day 1.
- Notes: LinkedIn invite text (under 300 chars, references Personal Hook, no pitch, no mutual connections).
- Owner: 196669355.

### Step 4: If NO email — LinkedIn fallback tasks (regardless of phone availability)

**Trigger:** ZoomInfo (or HubSpot for shallow path) did NOT return a valid business email. Phone availability is independent — if no email, create the LI tasks even if phone is available. The phone gets used in the call script (already in the strategy note).

These tasks are IN ADDITION to LINKED_IN_CONNECT (which is always created for every ✅ Yes), not instead of.

**Duplicate-task check (MANDATORY before either task):** query HubSpot for tasks on this contact. If any task with `hs_task_type = LINKED_IN_MESSAGE` AND `hs_task_status` `NOT_STARTED` or `IN_PROGRESS`, skip BOTH new tasks. Log: "Existing LinkedIn message task on HubSpot. No new tasks created." One active LinkedIn task = stop. Applies regardless of subject line.

If duplicate check passes:
- Task 1: `LINKED_IN_MESSAGE`, "1st LI -- [First Last] | [Company]", due 7 days. Notes: 1st LI message draft (3 sentences max).
- Task 2: `LINKED_IN_MESSAGE`, "2nd LI -- [First Last] | [Company]", due 21 days. Notes: 2nd LI message draft (1-2 sentences).

7 days + 21 days = the 2 InMails land 2 weeks apart.

These tasks PLUS the LINKED_IN_CONNECT task PLUS the strategy note are the complete outreach plan for no-email prospects. Do NOT hand off to osi-outreach-sequence (no email = no sequence).

**Yes-no-email candidate status in the queue:** mark `yes-no-email` so the Processing runner knows this candidate's outreach is complete and DOES NOT count toward the 3-yes-with-email-per-fire target. The runner continues evaluating the next pending candidate.

---

## FRESH HOOK SEARCH — every ✅ Yes before writing outreach

ZoomInfo scoops lag real news by weeks. ONE targeted web search for company news in last 30 days.

Search: `"[Company name] news [current month] [current year]"`

Score:
- Acquisition / merger / exec hire / earnings / product launch / buildout / partnership → Email 1 hook.
- Generic PR fluff / awards / charity → ignore.
- Nothing → fall back to LinkedIn + ZoomInfo scoops.

Record in Strategy and Fit:
`Fresh hook (30-day news): [one-line summary + source URL]`

One search. No rabbit holes.

---

## PLAYBOOK REFERENCES (read these when needed, not on every fire)

- **`C:\Claude-Brain\playbook\product-lines.md`** — OSI product lines, sequence-type table, DWDM talking points, who buys what.
- **`C:\Claude-Brain\playbook\vertical-intel.md`** — what to lead with by industry (telco, banks, consulting, manufacturing, healthcare). Park Place / Service Express merger wedge. TPM positioning.
- **`C:\Claude-Brain\playbook\opener-library.md`** — 12 cold-call openers + cold call rules. Use when writing LIVE CALL SCRIPT.
- **`C:\Claude-Brain\playbook\hubspot-data-quality.md`** — required fields, phone format, timezone buckets, pre-write checklist.
- **`C:\Claude-Brain\playbook\voice-rules.md`** — Andy's voice + humanization filter. Apply to call script, VM, LinkedIn invite text.

---

## OUTPUT FORMAT — Profile Mode

```
**[Name] — [Title], [Company]**
Current role: [Assessment]
Career trajectory: [Toward or away from OSI's world]
Skills: [Relevant ones; call out red flags]
CRM/Engagement: [Prior HubSpot touchpoints]
Verdict: ✅ Yes / ❌ No / ⚠️ Conditional
[1-3 sentences max. Direct.]

For ✅ Yes: run ZoomInfo, generate outreach package below. For No / Conditional: STOP-GATE.

Contact Info (ZoomInfo + LinkedIn):
- Email: [verified or "not found"]
- Direct: [direct dial or "not found"]
- Cell: [mobile or "not found"]
- Location: [city, state from LinkedIn]
- Timezone: [bucket]
```

After ✅ Yes (with email): output Strategy and Fit, Live Call Script, Voicemail, LinkedIn invite. Then HANDOFF to outreach.

---

## OUTREACH PACKAGE — auto-generate for every ✅ Yes verdict

### 1. Strategy and Fit

**Quick Connect Keywords** — 6-10 spoken trigger words for cold call.

**Previous Employer OSI Client Check** — list previous employers, note HubSpot matches. Skip section if no matches found.

**Target Sequences** — every applicable OSI product line. Choose from playbook/product-lines.md sequence list.

**The Play** — 1-2 sentences. Concrete attack based on title + company + background.

**The Personal Hook** — 1-2 specific LinkedIn details. Priority: (1) recent post/repost/comment in last 3-6 months [strongest], (2) recent job change / cert, (3) past company that's an OSI customer, (4) specific project, (5) unusual skill combo. Hook appears in Email 1 + LinkedIn invite.

### 2. Live Call Script

Under 30s spoken. Format:

```
KEYWORDS: [5-8 spoken trigger words]
HOOK: [Company news or personal trigger, one sentence. "none — using library opener" if nothing.]
OPENER: [full opener from playbook/opener-library.md, or custom if HOOK is strong]
```

### 3. Voicemail

15s max. One voicemail, never two. Hook drawn from Personal Hook. Name Email 1 subject. End with "that's andy at osiglobal dot com." No phone number. Present/future tense only.

```
"Hey [Name], Andy with OSI Global. [One-sentence hook]. I'm sending you something right now, subject line is [Email 1 subject]. That's andy at osiglobal dot com."
```

### 4. LinkedIn Invite

Under 300 chars. Low friction, networking framing, not pitching. Reference Personal Hook. No mutual connections.

---

## HANDOFF to osi-outreach-sequence

For every ✅ Yes with valid email, end with:

> HANDOFF: invoke osi-outreach-sequence on [First Last] at [Company]. Strategy note live on HubSpot contact ID [id]. Personal Hook: [hook]. Recommended sequence: [Call - Network / Server / TPM / DWDM / Storage / Networking].

Outreach updates LINKED_IN_CONNECT due_date to match Email 1 Day 1 (synchronized: LinkedIn invite 2 PM, call sequence enrollment, voicemail, Email 1 auto-fires 4 PM, all same day).

If ZoomInfo NO email: do NOT hand off. The 2 LI fallback tasks ARE the plan.

---

## EXCEL TRACKER — log every Company Mode session

Append all ✅ Yes and ⚠️ Conditional to `Claude-Brain/prospects-tracker-new.xlsx`.

Columns: Name | Title | Company | LinkedIn URL | OSI Angle | HubSpot Status | Action | Date Added | Notes

- HubSpot Status: "Not found" / "Andy" / "Team JAM" / "Owned by [rep]"
- Action: "Pursue" / "Request account — no activity since [date]" / "Skip"
- Notes: M&A context, news hook, flag reason

Also log ❌ No prospects belonging to a company flagged for account-request.

---

## FAILURE MODES

- LinkedIn URL unresolvable → mark `no` reason "could not resolve LinkedIn profile". Do NOT guess.
- Profile restricted/closed/deleted → qualify on available data. Critical signals hidden → `conditional`. Don't Yes a closed profile without strong HubSpot evidence.
- ZoomInfo no data on Yes → `yes-no-email`, 2 LI fallback tasks, NO handoff. Log.
- HubSpot ownership: other rep with recent activity → skip silent. Log to overnight-run-log if batch.
- Shallow-qualify input but HubSpot record missing → fall back to deep.
- Web search times out → proceed without, flag in strategy note.
- Chrome unresponsive → retry once after 30s, log + mark `pending-retry`, next batch picks up.

Every failure logs to `Claude-Brain/overnight-run-log.md`. Never silent.

---

## RULES
- Never Yes on title alone — verify with skills + trajectory (except shallow-qualify path, which is explicit + bounded).
- Never skim search result previews — always navigate to full profile.
- When can't locate someone on Sales Nav, always Google `"[name] [company]"` before concluding they've left.
- "VP" at banks (BNY, Citi, JPM) is a job grade, not a seniority indicator — verify with skills + trajectory.
- Never disqualify based on technical depth — OSI has engineers who join calls.
- Never guess at tech stack or buying authority — only reference what's confirmed.
- Restricted profile → say so, qualify on available.
- Run Step 0 before any LinkedIn work in Company Mode.
- Check HubSpot on shortlist before recommending outreach.
- Be a coach, not an assistant. Bad fit → say it directly.
- Company Mode → return ranked shortlist, no raw lists.
- Always ZoomInfo on every ✅ Yes — email, direct phone, mobile only. Never company main.
- City / state / timezone always from LinkedIn, never ZoomInfo.
- HubSpot tasks for connection requests → ALWAYS `LINKED_IN_CONNECT`. Never `LINKED_IN_MESSAGE` (that's InMail). Never `TODO`.
- Timezone: 6-bucket only. See playbook/hubspot-data-quality.md.
