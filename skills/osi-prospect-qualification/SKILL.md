---
name: osi-prospect-qualification
description: Qualify LinkedIn prospects for OSI Global. Use whenever Andy pastes a LinkedIn profile URL, asks "good target?", "is this worth an InMail?", or asks to evaluate any LinkedIn profile against OSI's product lines. Also triggers when reviewing prospect lists, when Andy says "find me prospects at [company]", "sequence this company", "find me cold companies", "sweep my accounts", or any variation of company-level prospecting. Should run automatically whenever a LinkedIn profile or company prospecting request appears in conversation, even without explicit ask.
---

> Source: `C:\Claude-Brain\skills\osi-prospect-qualification\` (Git, github.com/Drrewdy/Claude-Brain). Edit source, repackage, install.

# OSI Global, LinkedIn Prospect Qualification

---

## WHO OWNS WHAT

Strict boundary with **osi-outreach-sequence**.

| Responsibility | Owner |
|---|---|
| Verdict (Yes / No / Conditional) | this skill |
| Read LinkedIn profile in full (About, Experience, Skills, Activity) | this skill |
| Resolve LinkedIn URL from name+company | this skill |
| ZoomInfo enrichment (email, direct phone, mobile) | this skill |
| Strategy note creation | this skill |
| LINKED_IN_CONNECT task creation (provisional next-biz-day timestamp) | this skill |
| No-email-no-phone LI fallback tasks | this skill |
| Email 1 Day 1 stagger calc + LINKED_IN_CONNECT hs_timestamp final update | osi-outreach-sequence |
| Drafting 6 emails, email-queue writes | osi-outreach-sequence |
| Excel tracker rows | osi-outreach-sequence |

**Handoff rule:** when verdict is Yes AND ZoomInfo returns valid email, end with `HANDOFF: invoke osi-outreach-sequence on [First Last] at [Company].` The LINKED_IN_CONNECT task was created with a provisional timestamp; osi-outreach-sequence will update it to the real Day 1 after computing the stagger. If no email, the 2 LI fallback tasks are the complete plan; do NOT hand off.

---

## Role

Sales coach + outreach strategist for OSI Global. Two modes:
1. **Profile Mode** -- qualify a single prospect. Three input paths: LinkedIn URL / name+company / in-memory candidate from osi-discovery-sweep.
2. **Company Mode** -- given a company, find and rank targets interactively.

Always return a clear Yes / No / Conditional verdict with tight reasoning.

---

## TOOL CHOICE -- regular LinkedIn, NOT Sales Navigator

Use `linkedin.com/in/...` for both search and profile reading. Sales Nav pages are heavier and Show more / See all skills buttons are unreliable there.

- Candidate search: regular LinkedIn people search.
- Profile reading: regular LinkedIn profile (expanded About, Experience, Skills, activity feed).
- ZoomInfo: contact-data lookup only (email, direct phone, mobile). NOT for finding IT titles at banks / credit unions / insurance, see warning in Company Mode.
- HubSpot: ownership, company, contact checks.
- Sales Nav URL: save to `hs_linkedin_url` only if easily available; otherwise save the regular `/in/` URL. Do NOT navigate to Sales Nav as part of normal flow.

---

## Approved Vendor Rule

See `C:\Claude-Brain\playbook\drafting-rules.md` Section 9 for verbatim phrasing and email-by-email behavior. The drafting skill (osi-outreach-sequence) loads drafting-rules.md at Step 0 and applies the rule at draft time. Qualification does NOT need to handle approved-vendor language -- just record the company name in the strategy note and the drafter handles the rest.

To add a company to the approved list: edit `C:\Claude-Brain\approved-vendors.json` directly.

---

## MODE 1: Profile Mode (Single prospect)

Three input paths.

### Step 0: Route the input (check in order)

**Branch 1 -- In-memory from discovery:** if input is a candidate card passed from osi-discovery-sweep (has `firstName`, `lastName`, `linkedinUrl` or `company`, `source`), proceed directly to Step 1 using the LinkedIn URL if present, or resolve via name+company if not.

**Branch 2 -- HubSpot-sourced with engagement gate:** if input has `source: "hubspot_contact"` AND `hubspotContactId`, check the SHALLOW QUALIFY PATH gate below. If gate passes, use that path. If gate fails, fall back to Step 1 (deep read).

**Branch 3 -- URL provided:** proceed to Step 1 with that URL.

**Branch 4 -- Name + company only:** resolve URL first.
1. Search LinkedIn people for `"[First Last]" "[Company]"`.
2. Exactly one match -> use it, proceed to Step 1.
3. Multiple matches -> pick the one whose current company matches. If still ambiguous, web search `site:linkedin.com/in/ "[First Last]" "[Company]"`, take first result that resolves.
4. No match -> mark candidate `no` reason "could not resolve LinkedIn profile". Exit. Do NOT guess a URL.

### Step 1: Read the Full LinkedIn Profile

Navigate to the URL. Expand and read EVERYTHING:
- Full **About**, click Show more if truncated.
- Every **Experience** entry, expand all role descriptions, including older roles.
- Complete **Skills** list via `/details/skills/`, endorsement counts.
- **Activity feed** via `/recent-activity/all/`, last 3-6 months of posts, reposts, comments. Look for technical signals (400G, DWDM, DIMMs, network refresh, vendor changes, AI buildout), pain points, vendors name-checked, certifications, current initiatives. Activity is the richest Personal Hook source.
- **City + state** from location field, required for HubSpot.
- **Timezone** from city/state per Andy's 6-bucket system (see hubspot-data-quality.md).

> Skills = most important qualification signal. Activity = most important personalization signal. Never qualify on title alone. Never skim search result previews, always navigate to the actual profile page.

If LinkedIn restricts or 404s the profile, fall back to web search: `"[First Last]" "[Company]" site:linkedin.com` or a general Google search for their current role. If still unresolvable, mark Conditional with reason "profile restricted, could not verify employer."

**Sales Nav restricted panel does NOT mean the LinkedIn profile is restricted.** Sales Navigator sometimes shows a "restricted" or "limited" panel for 2nd/3rd degree connections while the actual `linkedin.com/in/` URL is fully readable. If a candidate was surfaced from Sales Nav and the Sales Nav panel looks restricted, ALWAYS attempt to navigate to the direct `linkedin.com/in/<handle>` URL before concluding the profile is inaccessible. The handle is often derivable from the name + company search. Only mark Conditional on profile restriction after a direct `linkedin.com/in/` attempt also fails.

---

## SHALLOW QUALIFY PATH -- recent-engagement gated only

**HARD GATE:** This path is ONLY available when there is a recent two-way engagement signal proving the contact is currently reachable at the listed company. Mere HubSpot record presence is NOT sufficient. Title alone is NEVER sufficient. Without a recent reply or meeting, fall back to deep LinkedIn read.

**Why this gate exists:** 2026-04-26, an earlier version of this path triggered on "HubSpot record + JAM-owned" alone and produced 138 emails queued to 23 prospects without confirming anyone was still employed there. This path requires a real engagement signal.

**Use shallow only when ALL true:**
1. `source: "hubspot_contact"` with `hubspotContactId`, AND
2. HubSpot record has `email`, `jobtitle`, `company` populated, AND
3. Owned by JAM (Andy 196669355 / Mark 210187184 / John 210187193), AND
4. Email domain matches the company's known/derived primary domain, AND
5. **Recent positive engagement: at least ONE of:**
   - Inbound reply received from this contact within the last **12 months**, OR
   - Meeting logged with this contact within the last **12 months**
6. AND no hard-bounce ever recorded against this email, AND
7. AND not on the hard-block list at `C:\Claude-Brain\hard-block.json`.

If ANY of 1-7 fails -> fall back to deep LinkedIn read (Step 1). No exceptions. Opens, deliveries, and clicks do NOT qualify -- replies and meetings only.

### How to verify the engagement gate

Before any other work, check via `get_crm_objects` and the contact's associations:
- `hs_email_last_reply_date` if populated, OR enumerate associated emails where direction is `INCOMING_EMAIL` within 12mo.
- Associated meetings, filter to outcome != NO_SHOW and timestamp within 12mo.
- `hs_email_bounce` and most recent outbound email status. Any hard-bounce = gate fails.

If gate passes -> shallow qualify steps below. If fails -> log `engagement_gate_failed: <reason>`, go to deep read.

### Shallow Qualify steps (only after gate passes)

1. Pull HubSpot contact via `get_crm_objects`. Read: firstname, lastname, jobtitle, company, email, phone, mobilephone, city, state, hs_timezone, hs_linkedin_url, notes_last_contacted.
2. ICP check by title + vertical. Apply DISQUALIFIERS list. Ambiguous title -> fall back to deep.
3. Active sequence check. Skip if already enrolled or recently sent.
4. ZoomInfo enrichment, only if HubSpot is missing email, phone, or mobilephone. If all three populated and phone formatted correctly, skip ZoomInfo. If ZoomInfo IS run, the 7-attempt retry matrix applies -- no shortcut.
5. LinkedIn URL resolution: if `hs_linkedin_url` populated, use it. If not, one-shot LinkedIn search by name+company; write back to HubSpot if resolved.
6. Personal Hook: build from the recent reply/meeting itself (quote what they said last), previous employers (HubSpot notes), company news (`enrich_scoops` or `enrich_news`), or vertical-specific hook fallback.
7. Generate outreach package, strategy note, LINKED_IN_CONNECT task, call script, VM, LinkedIn invite, Email 1 opener. Annotate strategy note with `SOURCE: HubSpot shallow qualify (engagement-gated, last reply/meeting <date>)`.
8. Handoff to osi-outreach-sequence, same format as deep path. LINKED_IN_CONNECT task has provisional timestamp; outreach-sequence computes the real Day 1 and updates it.

### When to escalate back to deep (even if gate passed)
- Vague title ("IT Specialist", "Technology Manager" with no industry clue)
- Most recent reply mentions departure language
- HubSpot company field disagrees with email domain
- Anything that makes you unsure -- default to deep

---

## MODE 2: Company Mode

🚨 **NEVER CAP CANDIDATES AT A COMPANY. EVER.**
Cast the widest net possible. If 12 people at a company are worth qualifying, qualify all 12. If you stop early, you will not come back to this company for months and those people will never get contacted. The only reason to stop qualifying people at a company is that you have genuinely run out of relevant titles -- not because some arbitrary number was hit. This rule is non-negotiable.

When Andy says "find me prospects at [Company]" without running a full discovery sweep.

### Step 0: Company pre-checks

**THIS STEP IS MANDATORY BEFORE TOUCHING LINKEDIN OR ZOOMINFO. DO NOT SKIP.**

#### 0A. Build the company name variant list

Take the input company name and generate all likely HubSpot search strings. Strip and permute:

1. **Full name as-is** ("GTT Communications")
2. **Drop legal suffix** (strip: Inc, Inc., LLC, Ltd, Corp, Corporation, Holdings, Group, Co, Co., Company, Companies, International, Solutions, Services, Systems, Networks, Telecom, Telecommunications, Broadband, Fiber, Cable, Communications, Technology, Technologies) -> "GTT"
3. **First word only** ("GTT")
4. **Acronym expansion if input is an acronym** (e.g., "GTT" -- try "Global Telecom and Technology" via web search if unclear)
5. **Common rebrand / trade name** -- if you know or can quickly derive it (e.g., "tw telecom" -> "TW Telecom" -> also try "Level 3" post-acquisition)

Run ALL of the following HubSpot searches and UNION the results before drawing any conclusion:

**Name searches (run one per variant, stop adding variants when results are clearly the same company):**
```
search_crm_objects({
  objectType: "companies",
  filterGroups: [{filters: [
    {propertyName: "name", operator: "CONTAINS_TOKEN", value: "<variant>"}
  ]}],
  properties: ["name","domain","hubspot_owner_id","notes_last_contacted","hs_object_id","hs_lastmodifieddate"]
})
```
Run this for: full name, stripped name, first-word, any known trade name.

**Domain search (REQUIRED -- catches "GTT" stored as gtt.net when input is "GTT Communications"):**
First, derive the likely domain: strip "Communications", "Inc", etc., lowercase, add ".com" / ".net" / ".org". For GTT Communications -> try gtt.com AND gtt.net. Then:
```
search_crm_objects({
  objectType: "companies",
  filterGroups: [{filters: [
    {propertyName: "domain", operator: "EQ", value: "<derived_domain>"}
  ]}],
  properties: ["name","domain","hubspot_owner_id","notes_last_contacted","hs_object_id","hs_lastmodifieddate"]
})
```
Try each plausible domain variant (gtt.com, gtt.net, gttcommunications.com). Stop when you get a hit.

**Union all results.** If ANY search returns a company record that is clearly the same company (same brand, same domain, obvious name variant), treat it as a match. Do NOT require an exact name match.

#### 0B. M&A check

After the HubSpot search, run one web search: `"[Company] acquired" OR "[Company] merger" OR "[Company] rebranded" site:reuters.com OR site:businesswire.com OR site:prnewswire.com`

If a material acquisition or merger is found:
- Identify the acquiring company.
- Run the HubSpot company search again for the acquiring company name.
- If the acquiring company is in HubSpot and owned by another rep: STOP. Flag to Andy (see 0C).
- If JAM-owned or not in HubSpot: proceed but note the M&A context in the strategy note.

#### 0C. Ownership decision

From the unioned HubSpot results, determine ownership:

| Scenario | Action |
|---|---|
| Not found in HubSpot under any name or domain variant | Proceed. New account. |
| Found, JAM-owned (Andy 196669355 / Mark 210187184 / John 210187193) | Proceed. |
| Found, other rep, last activity within 3 months | STOP. Flag to Andy: "**[Company] is owned by [Rep Name] in HubSpot (last activity [date]). Do not prospect -- active account under another rep.**" Do NOT prospect silently. |
| Found, other rep, no activity in 3+ months, not a client | STOP. Flag to Andy: "**[Company] is in HubSpot under [Rep Name] but no activity since [date]. Flagging for account-request -- do not prospect yet.**" Log to `overnight-run-log.md`. |
| Found under a variant name / domain the input didn't match | STOP. Flag to Andy: "**Heads up: '[Input Name]' appears to already be in HubSpot as '[HubSpot Name]' (domain: [domain], owner: [rep]). Treating as same company.**" Then apply ownership rules above. |
| M&A: target acquired by a company owned by another rep | STOP. Flag to Andy: "**[Input Company] was acquired by [Acquirer]. [Acquirer] is owned by [Rep] in HubSpot. Do not prospect [Input Company] contacts -- they roll up to an account owned by another rep.**" |

**The flag message must always say: company name as stored in HubSpot, domain, owner name, last activity date, and what Andy should do next. Never skip silently.**

### Step 1: LinkedIn candidate search

**Exhaust the search.** Finding 1-2 and stopping is not acceptable.

**Round 1, English priority titles:**
- "network engineer" OR "network architect"
- "transport engineer" OR "optical engineer" OR "DWDM"
- "IT infrastructure" OR "infrastructure architect"
- "data center manager" OR "data center engineer"
- "IT asset manager" OR "IT vendor manager"
- "telecom" OR "telecommunications engineer"

**Round 2, French keywords (REQUIRED for Quebec: Desjardins, National Bank, Caisse, Hydro-Quebec, Bell, Videotron, Cogeco):**
- "ingenieur reseau" OR "architecte reseau"
- "architecte telecom" OR "ingenieur telecom"
- "infrastructure TI" OR "architecte infrastructure"
- "architecture detaillee" OR "expert telecom"
- "conception reseaux" OR "operations telecom"

**Round 3, Secondary titles** (when Round 1-2 thin, or any enterprise company):
- Senior Infrastructure Engineer, Systems Engineer / Administrator
- Storage Engineer / Administrator, Virtualization Engineer
- NOC Manager, Director of IT Operations, VP of Technology
- Head of IT, Technology Manager

**Pagination, non-negotiable:** every page of every search until LinkedIn says no more.

**ZoomInfo warning for large financial institutions** (Desjardins, National Bank, Caisse, Intact, etc.): ZoomInfo is UNRELIABLE for finding IT titles. Use LinkedIn directly.

**Minimum effort:**
- Small/mid (under 500 emp): 2+ combinations, all pages.
- Large (500-5,000): 4+ combinations, all pages.
- Enterprise (5,000+): 6+ combinations. Fewer than 5 found = not enough.

### Step 2: Read EVERY relevant profile in full

No cap. Every candidate whose card suggests IT/network/telecom relevance gets a full profile read (About, Experience, Skills via `/details/skills/`, Activity, city/state, timezone bucket).

### Step 3: Return ranked shortlist

Yes first, then Conditional, then No with brief reasons. No cap on Yes count. Each Yes includes recommended OSI angle.

**Company Mode sweep verdict format (one line per candidate):**
```
[Name] | [Title] | Yes / No / Conditional | [one phrase reason]
```
Example: `Jamie Ross | Sr. Network Engineer | Yes | DWDM + compute skills, active in role`
Example: `Kevin Walsh | Facilities Manager | No | M&E only, no IT hardware`

Do not write paragraphs per candidate during a sweep. Reserve the full OUTPUT FORMAT for Profile Mode (single prospect).

### Step 4: HubSpot check on shortlist

Flag any already owned or with prior touchpoints before Andy reaches out.

---

## CONTACT VERIFICATION PROTOCOL

When confirming if existing HubSpot contacts are still at a company:

1. Search LinkedIn by name + company (regular LinkedIn people search).
2. Navigate to LinkedIn profile, read About + Experience to confirm current employer + start date.
3. **Fallback if LinkedIn returns no profile:** Google `"[First Last]" "[Company]"` via WebSearch. People almost always show up. Acceptable sources: company website team page, conference speaker bio, press release, podcast bio, recent industry article. Source must be within the last 6 months.
4. Report: still at company / left (note new employer if found) / between roles / can't locate.

**ZoomInfo NO_MATCH or COMPANY_ONLY_MATCH is NOT a verification failure.** ZI failing to find a person means they are not in ZI's database -- it does not mean their employer is unconfirmable. When ZI whiffs, go to LinkedIn. A "could not verify current employer" Conditional is only valid after BOTH (a) LinkedIn search by name + company returned no live profile (try full name, last+first, common nickname variants) AND (b) a web search returned no dated source within 6 months.

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
- Strong networking past + irrelevant current = nothing.

### 3. Skills
- Read EVERY skill, featured AND full list via `/details/skills/`.
- **Green flags:** Data Center, Networking, Network Architecture, IT Infrastructure, IT Operations, Cloud Computing, Vendor Management, Storage, Compute, VMware, Cisco, Dell, HP, DWDM, Fiber Optics, Optical Networking, Capacity Planning, ITIL, Disaster Recovery.
- **Red flags:** only M&E (chillers, generators, UPS, HVAC), only facility services, only HR/finance/marketing.

---

## STOP-GATE -- No / Conditional verdicts

The instant a verdict forms:
- **No or Conditional:** STOP. No ZoomInfo. No HubSpot contact create/update. No strategy note. No tasks. Move to next.
- **Yes:** proceed to ZoomInfo enrichment + HubSpot save + outreach package.

HubSpot slots and ZoomInfo credits are reserved for Yes only.

---

## ZOOMINFO ENRICHMENT -- every Yes verdict

After Yes verdict, enrich before any HubSpot write or outreach. ZoomInfo files companies under shorter names than HubSpot stores them. The skill MUST try multiple name variants before recording no-match.

### HARDWIRED RULE -- ZOOMINFO RETRY MATRIX

Every ZoomInfo enrichment for a Yes verdict MUST attempt the following lookups in order, stopping ONLY when `matchStatus === "FULL_MATCH"` with a non-empty `email` is returned. Each attempt's exact input + matchStatus is recorded verbatim in the strategy note's ZI ATTEMPTS block.

**Attempt 1 -- Stored company name** (HubSpot `company` field as-is):
```
enrich_contacts({contacts: [{firstName, lastName, companyName: "<HubSpot company>"}]})
```

**Attempt 2 -- Short form** (strip suffixes: Communications, Inc, Inc., LLC, Group, Corp, Corporation, Holdings, Companies, Company, Technology, Industries, International, Solutions, Services, Systems, Networks, Telecom, Telecommunications, Broadband, Fiber, Cable). Skip-with-log if short form === stored.

**Attempt 3 -- First word only** ("Lingo Communications" -> "Lingo", "Patrick Industries" -> "Patrick").

**Attempt 4 -- Domain stem** (strip TLD and www.: "lingo.com" -> "lingo", "spglobal.com" -> "spglobal").

**Attempt 5 -- name + companyId** (REQUIRED if any earlier attempt returned `COMPANY_ONLY_MATCH` carrying a `zoominfoCompanyId`):
```
enrich_contacts({contacts: [{firstName, lastName, companyId: "<zoominfoCompanyId>"}]})
```

**Attempt 6 -- search_contacts with name + short-form company:**
```
search_contacts({firstName, lastName, companyName: "<short form>"})
```

**Attempt 7 -- search_contacts via LinkedIn URL** (only if candidate has a LinkedIn URL):
```
search_contacts({externalURL: "<linkedin profile URL>"})
```

If ALL seven attempts return non-FULL_MATCH or empty email, ONLY THEN mark `yes-no-email`. Strategy note must contain all attempt logs verbatim.

Strategy note format (mandatory, placed at top of EMAIL RESOLUTION block):

```
ZI ATTEMPTS (mandatory retry matrix):
  1. companyName="Lingo Communications" -> COMPANY_ONLY_MATCH (zoominfoCompanyId 456817366)
  2. companyName="Lingo" -> FULL_MATCH (id 9391145248, accuracyScore 99)
  3-7. <skipped, match found at attempt 2>
EMAIL RESOLUTION: zoominfo-full-match
  chosen: kimberly.rodriguez@lingo.com
  attempt: 2
```

**FORBIDDEN: marking `yes-no-email` after fewer than 7 attempts.** Run all 7. No exceptions for token budget, time, or "the others will fail anyway."

**Why this rule exists:** 2026-04-28, Kimberly Rodriguez at Lingo Communications was queued with no email after a single `enrich_contacts` call returned `COMPANY_ONLY_MATCH`. A single-word retry returned `FULL_MATCH`. Run all 7.

### Results mapping (after FULL_MATCH)
- Email found -> HubSpot `email`.
- Direct phone -> HubSpot `phone`.
- Mobile -> HubSpot `mobilephone`.
- Nothing after all 7 attempts -> "ZoomInfo: no data found across retry matrix". `yes-no-email` path.
- Never confuse direct phone with company main.

City / state / timezone -> ALWAYS LinkedIn, NEVER ZoomInfo.

### Email domain validation -- before handoff to outreach

ONE web search to confirm the email domain is the company's corporate domain, not consumer ISP / subsidiary brand / stale pre-acquisition.

Search: `"[Company name] corporate email domain"`

- Match -> proceed.
- Consumer ISP / residential brand / dead domain -> invalid. Flag, do NOT queue, pattern-match real corporate domain or hand back to Andy.

Examples to catch: Altafiber employees with @zoomtown.com; post-acquisition employees on dead domain.

One search, no rabbit holes.

---

## DISQUALIFIERS (Hard No)

- Current role is Facilities / M&E (chillers, generators, UPS, PDUs).
- Current role is HR / Finance / Legal / Marketing / Sales with no IT infrastructure component.
- Skills entirely facility services (carrier hotel, colocation, HVAC, electrical).
- Career fully moved away from IT/networking, no return.
- Hyperscaler (Meta, Google, AWS, Microsoft) building fully custom, only proceed if you can identify a specific hardware procurement function.

---

## CONDITIONAL QUALIFIERS

- Title right but they are a planner / optimizer rather than buyer, influencer, or path to buyer.
- Sourcing professional -- only proceed if category covers IT hardware (not facility services or wireless mobility).
- Restricted profile (2nd/3rd connection, skills hidden) -- qualify on what is available, revisit after connect.
- Recently changed roles -- verify new role before assuming old role's relevance carries over.

---

## REAL EXAMPLES

| Prospect | Title | Company | Verdict | Reason |
|---|---|---|---|---|
| William Clarke | Facilities Supervisor | ISS | No | M&E only, chillers, generators. No IT hardware skills. |
| Onur Turkcu | Backbone Network Planner | Meta | Conditional | Right space (DWDM, ex-Infinera), but planner not buyer. Meta builds custom. Path to buyer only. |
| Ron Kemp | VP IT Infrastructure & Operations | Precision Castparts | Yes | 30yr IT infra, manages vendors, global manufacturer, TPM + servers + VMware wedge. |
| John Lee | Senior Manager Infrastructure | Wells Fargo | Yes | Data Center Engineering at major bank, 35 endorsements DC + Vendor Management. Strong TPM. |
| FNU Avantika | Associate Director, Network Technology | AT&T | Yes | Strategic sourcing/procurement embedded in AT&T Network Technology. Lead with cost savings. |

---

## HubSpot writes -- for every Yes verdict

Always create regardless of data:
- LinkedIn connection request task with a provisional `hs_timestamp` = next business day at 4 PM ET.
- Strategy and Fit note.

Email creation, scheduling, and the 6-email sequence are owned by `osi-outreach-sequence`, NOT here.

### HARDWIRED RULE -- STAGGER IS OUTREACH-SEQUENCE'S JOB

This skill does NOT compute the final Email 1 Day 1. It creates the LINKED_IN_CONNECT task with a provisional timestamp (next business day at 4 PM ET) so the task exists in HubSpot before handoff. `osi-outreach-sequence` owns the stagger table, computes the real Day 1, and updates the LINKED_IN_CONNECT task timestamp in its Step 11. One skill owns stagger. No drift.

The following paths are FORBIDDEN:
- "Compute the stagger here and pass email1_day1 to outreach-sequence." NO. Stagger lives in outreach-sequence.
- "Leave hs_timestamp blank; outreach-sequence will set it." NO. Set a provisional next-business-day timestamp so the task is never in HubSpot with a null due date.

### HARDWIRED RULE -- ATOMIC WRITES TO STATE FILES

Every modification to `C:\Claude-Brain\overnight-candidates.json` and `C:\Claude-Brain\email-queue.json` is an atomic write. Read the full file, modify in memory, write to `<file>.tmp`, then `os.replace(tmp, file)`. NEVER `open(file, 'w')` directly.

```python
import os, json
PATH = 'C:/Claude-Brain/overnight-candidates.json'
with open(PATH) as f: state = json.load(f)
# modify state in memory
tmp = PATH + '.tmp'
with open(tmp, 'w') as f: json.dump(state, f, indent=2)
os.replace(tmp, PATH)
```

**Why this rule exists:** 2026-04-29, JSON corruption on both overnight-candidates.json and email-queue.json from direct file writes during concurrent operations. Atomic writes eliminate the truncation failure mode.

### HARDWIRED RULE -- STEPS 1-3.5 ARE TRANSACTIONAL

Step 1, Step 2, Step 3, Step 3.5 execute as one transaction. Fixed order. If any step fails or its read-back fails, abort BEFORE handing off to osi-outreach-sequence. Flip candidate to status `pending-relookup`, log to `overnight-run-log.md`. NO email queue entries written for failed transactions.

Order:
1. **Step 1** -- Update or create contact.
2. **Step 2** -- Create Strategy and Fit note (depends on Step 1 contact ID).
3. **Step 3** -- Create LINKED_IN_CONNECT task with provisional `hs_timestamp` = next business day at 4 PM ET.
4. **Step 3.5** -- Read-back verification: fetch just-created task ID. Confirm task associated to contact. Confirm `hs_task_type` is `LINKED_IN_CONNECT`. If any check fails: ABORT. Flip to `pending-relookup`. Log. No handoff.
5. **Handoff** -- to osi-outreach-sequence with payload `{contactId, sequenceType, hookSummary, ...}`. Outreach-sequence computes the real Day 1, queues emails, and updates the LINKED_IN_CONNECT task timestamp.

**FORBIDDEN paths:**
- "Hand off to outreach-sequence first, it will create the task." NO. Task is owned by this skill.
- "Skip the read-back, the task creation returned an ID." NO. The ID returning does not prove the timestamp is right. Atta Meer's task creation returned an ID. The timestamp was still wrong.
- "If read-back fails, retry once and continue." NO. Read-back failure means something is structurally wrong. Flip to `pending-relookup`.

**Why this rule exists:** 2026-04-28, Joel Emter had Email 1 queued and zero LINKED_IN_CONNECT task because Step 3 silently failed and the handoff happened anyway. Atta Meer had Day 1 computed twice with two different values, no read-back to catch it.

### Data quality requirements

Read `C:\Claude-Brain\playbook\hubspot-data-quality.md` for required fields, phone format, mobile rule, timezone bucket, pre-write checklist.

### Step 1: Create or update contact record

**HUBSPOT-FIRST SEARCH (mandatory before any create):**
Before writing anything to HubSpot, run TWO searches and union the results.

**Search A -- lastname only (catches nickname variants):**
```
search_crm_objects({
  objectType: "contacts",
  filterGroups: [{filters: [
    {propertyName: "lastname", operator: "EQ", value: "<Last>"}
  ]}],
  properties: ["firstname","lastname","email","company","hs_object_id","hubspot_owner_id"]
})
```

**Search B -- email domain (catches records where name was entered differently):**
```
search_crm_objects({
  objectType: "contacts",
  filterGroups: [{filters: [
    {propertyName: "email", operator: "CONTAINS_TOKEN", value: "@<company_domain>"}
  ]}],
  properties: ["firstname","lastname","email","company","hs_object_id","hubspot_owner_id"]
})
```
Skip Search B if you do not yet have a confirmed corporate email domain.

**Name-variant matching (apply to Search A results):**
After pulling results by lastname, check if the `firstname` in any result is a known variant of the prospect's first name. Common pairs to check:

| Formal | Nicknames |
|---|---|
| Andrew | Andy, Drew |
| William | Bill, Will, Billy |
| Robert | Bob, Rob, Bobby |
| Richard | Rick, Rich, Dick |
| James | Jim, Jimmy |
| Michael | Mike, Mikey |
| Thomas | Tom, Tommy |
| Joseph | Joe, Joey |
| David | Dave |
| Daniel | Dan, Danny |
| Christopher | Chris |
| Matthew | Matt |
| Anthony | Tony |
| Charles | Chuck, Charlie |
| Stephen/Steven | Steve |
| Edward | Ed, Eddie, Ted |
| Patrick | Pat |
| Timothy | Tim |
| Jonathan | Jon, Jonny |
| Nathaniel | Nate, Nathan |
| Benjamin | Ben |
| Samuel | Sam |
| Alexander | Alex, Xander |
| Nicholas | Nick |
| Gregory | Greg |
| Raymond | Ray |
| Lawrence | Larry |
| Gerald | Jerry |
| Donald | Don |
| Ronald | Ron |
| Kenneth | Ken |
| Jeffrey | Jeff |
| Douglas | Doug |
| Katherine | Kate, Kathy, Kat |
| Elizabeth | Liz, Beth, Betty, Ellie |
| Jennifer | Jen, Jenny |
| Margaret | Meg, Maggie, Peg |
| Patricia | Pat, Tricia |
| Deborah | Deb, Debbie |
| Susan | Sue, Susie |
| Barbara | Barb |
| Christine | Chris, Christy |
| Stephanie | Steph |

If the prospect's first name is not on this list, also check if it is a shortened form of what HubSpot has stored (e.g., "Rob" in HubSpot, "Robert" on LinkedIn) or vice versa.

**Matching logic (union of Search A and B results):**
Filter all results to records where `company` matches the prospect's company (exact or close-enough -- "Midco" matches "Midcontinent Communications"). From those, a record is a match if ANY of:
- `firstname` exactly matches the prospect's first name, OR
- `firstname` is a known variant of the prospect's first name per the table above, OR
- `email` domain matches the confirmed corporate domain AND `lastname` matches.

**If a match is found:**
- Use that contact's `hs_object_id` as `hubspotContactId`. Do NOT create a new record.
- Use that contact's primary `email` for all queue entries. Do NOT substitute a ZoomInfo-derived address unless HubSpot has no email at all.
- If ZoomInfo returned a different email, write the ZoomInfo address to `hs_additional_emails` and append this line to the strategy note (below THE PERSONAL HOOK, above the ZI ATTEMPTS block): `ALT EMAIL <date>: ZoomInfo lists <zi_email>. Using <hubspot_email>. Pattern: <pattern> verified by HubSpot existing record.`
- If multiple matches found (true ambiguity -- two people with same last name at same company): surface both to Andy and stop. Do not guess.

**If no match found:** create the contact (linked to company) before note + tasks. All required fields per data-quality playbook.

**Why this rule exists:** 2026-04-27, a duplicate John Lubeck contact was created at Midco using ZoomInfo's `jlubeck@midco.com` instead of the existing verified record at `john.lubeck@midco.com`. Six emails queued to the wrong address before catch. Name-variant search added to catch cases where a contact is stored as "Andy" in HubSpot but sourced as "Andrew" from LinkedIn.

### Step 2: Create Strategy and Fit note

🚨 **WRITE ONCE. FINAL FORMAT ONLY. NO DRAFTS.**

Do NOT create a note and then update it. Do NOT write a placeholder. Finish ALL research (LinkedIn full read, ZoomInfo retry matrix, fresh hook search) BEFORE touching HubSpot. The note is written exactly once, in final format, as a single atomic action.

objectType: `notes`, owner: 196669355, associated to contact.

Write in this exact order with these exact labels:

```
Fresh hook (30-day news): [one-line summary + URL, or "none"]

QUICK CONNECT KEYWORDS
[6-10 keywords, one line]

LIVE CALL SCRIPT (omit entire section if no phone)
OPENER: [full opener from playbook/opener-library.md]
VM: [one line, 15s max. One-sentence hook. "I'm sending you something right now, subject line is [Email 1 subject]." Ends with "that's andy at osiglobal dot com." Present/future tense only.]

THE PLAY
[One paragraph: why they qualify + the hook + the attack plan.]

THE PERSONAL HOOK
[1-2 specific LinkedIn details that anchor Email 1 + LinkedIn invite when outreach runs.]

ZI ATTEMPTS (mandatory retry matrix):
  1. companyName="..." -> ...
EMAIL RESOLUTION: zoominfo-full-match
  chosen: email@domain.com
  attempt: N
```

**Forbidden labels:** `ANGLE FOR EMAIL 1`, `WHY HE'S A YES`, `OSI ANGLES`. These are not part of the format. If you find yourself writing them, stop and use `THE PLAY` and `THE PERSONAL HOOK` instead.

The outreach skill reads `THE PERSONAL HOOK` and `THE PLAY` by exact label match. If the labels are wrong, the outreach skill cannot parse the note and will draft from memory, which produces wrong emails.

Never use em-dashes anywhere in the note.

### Step 3: Create LINKED_IN_CONNECT task -- every Yes

Task housekeeping first: if prospect has an existing `LINKED_IN_CONNECT` task, mark it COMPLETED before creating the new one.

Create:
- Subject: `Sales Nav -- Send connection request -- [First Last] | [Company]`
- Type: `LINKED_IN_CONNECT` (never `LINKED_IN_MESSAGE`, never `TODO`)
- `hs_timestamp`: provisional -- next business day at 4 PM ET. `osi-outreach-sequence` will update this to the real Day 1 after computing the stagger.
- Notes: LinkedIn invite text (under 300 chars, references Personal Hook, no pitch). Body is ONLY the raw message text, no labels, no character counts.
- Owner: 196669355.

### Step 3.5: Read-back verification (MANDATORY before handoff)

Immediately after creating the LINKED_IN_CONNECT task, fetch it back via `search_crm_objects` filtered by the new task's `hs_object_id`. Confirm:
- Task exists.
- `hs_task_type` is `LINKED_IN_CONNECT`.
- Task is associated to the contact ID from Step 1.

If any check fails: ABORT. Flip to `pending-relookup`. Log. No handoff. No queue write.

### Step 4: If NO email -- LinkedIn fallback tasks

**Trigger:** ZoomInfo retry matrix returned no FULL_MATCH after all 7 attempts.

**Duplicate-task check (MANDATORY before either task):** query HubSpot for tasks on this contact. If any task with `hs_task_type = LINKED_IN_MESSAGE` AND status NOT_STARTED or IN_PROGRESS, skip BOTH new tasks. One active LinkedIn task = stop.

If duplicate check passes:
- Task 1: `LINKED_IN_MESSAGE`, "1st LI -- [First Last] | [Company]", due 7 days. Notes: 1st LI message draft (3 sentences max).
- Task 2: `LINKED_IN_MESSAGE`, "2nd LI -- [First Last] | [Company]", due 21 days. Notes: 2nd LI message draft (1-2 sentences).

These tasks PLUS the LINKED_IN_CONNECT task PLUS the strategy note are the complete outreach plan for no-email prospects. Do NOT hand off to osi-outreach-sequence.

---

## FRESH HOOK SEARCH -- every Yes before writing outreach

ONE targeted web search for company news in last 30 days.

Search: `"[Company name] news [current month] [current year]"`

**Strong fresh hooks (use as Email 1 angle):**
- Acquisition or merger, senior exec hire, earnings beat or miss (only when it connects to infrastructure spend), product launch, buildout announcement, strategic partnership.

**Weak fresh hooks (OMIT -- do NOT write filler):**
- Awards, charity announcements, generic PR, random press releases, blog posts, marketing campaigns, sustainability reports.

If no strong fresh hook found: `Fresh hook (30-day news): none`

If strong hook found: `Fresh hook (30-day news): [one-line summary + source URL]`

One search. No rabbit holes. Filler in this field gets surfaced into Email 1 as bad personalization.

---

## PLAYBOOK REFERENCES

- **`C:\Claude-Brain\playbook\product-lines.md`** -- OSI product lines, sequence-type table, DWDM talking points, who buys what.
- **`C:\Claude-Brain\playbook\vertical-intel.md`** -- what to lead with by industry. Park Place / Service Express merger wedge. TPM positioning.
- **`C:\Claude-Brain\playbook\opener-library.md`** -- 12 cold-call openers + cold call rules.
- **`C:\Claude-Brain\playbook\hubspot-data-quality.md`** -- required fields, phone format, timezone buckets, pre-write checklist.
- **`C:\Claude-Brain\playbook\voice-rules.md`** -- Andy's voice + humanization filter. Apply to call script, VM, LinkedIn invite text.

---

## OUTPUT FORMAT -- Profile Mode

```
**[Name], [Title], [Company]**
Current role: [Assessment]
Career trajectory: [Toward or away from OSI's world]
Skills: [Relevant ones; call out red flags]
CRM/Engagement: [Prior HubSpot touchpoints]
Verdict: Yes / No / Conditional
[1-3 sentences max. Direct.]
```

For Yes: run ZoomInfo retry matrix, generate outreach package below. For No / Conditional: STOP-GATE.

```
Contact Info (ZoomInfo + LinkedIn):
- Email: [verified or "not found across 7 retries"]
- Direct: [direct dial or "not found"]
- Cell: [mobile or "not found"]
- Location: [city, state from LinkedIn]
- Timezone: [bucket]
```

After Yes (with email): output Strategy and Fit, Live Call Script, Voicemail, LinkedIn invite. Then HANDOFF to outreach-sequence (no email1_day1 -- outreach-sequence computes Day 1 from stagger).

---

## OUTREACH PACKAGE -- auto-generate for every Yes verdict

### 1. Strategy and Fit

**Quick Connect Keywords** -- 6-10 spoken trigger words for cold call.

**Previous Employer OSI Client Check** -- list previous employers, note HubSpot matches. Skip section if no matches found.

**Target Sequences** -- every applicable OSI product line. Choose from playbook/product-lines.md sequence list.

**The Play** -- 1-2 sentences. Concrete attack based on title + company + background.

**The Personal Hook** -- 1-2 specific LinkedIn details. Priority order: (1) recent post/repost/comment in last 3-6 months [strongest], (2) recent job change / cert, (3) past company that is an OSI customer, (4) specific named project, (5) unusual skill combo.

### PERSONAL HOOK QUALITY GATE -- hardwired

The hook MUST be one of the 5 priority types above. The following are NOT Personal Hooks:

- Generic geography. "BNY's Pittsburgh footprint is significant" is filler, not a hook.
- Job title alone. "Saw you're a Senior Network Engineer" is not a hook.
- Tenure alone. "Saw you've been at the company for 5 years" is not a hook.
- Company size or industry alone.
- Generic compliments. "Impressive background" is not a hook.

If after a full LinkedIn read (About + Experience + Skills + Activity feed) NO qualifying hook of priority types 1 through 5 can be pulled, the verdict is downgraded to Conditional with reason "no Personal Hook available."

**Why this rule exists:** 2026-04-30, Christopher Lawrence email shipped with "BNY's Pittsburgh infrastructure footprint is significant" as the Personal Hook. That is not a hook. The fix lives at strategy-note-write time.

### 2. Live Call Script

Under 30s spoken.

```
KEYWORDS: [5-8 spoken trigger words]
HOOK: [Company news or personal trigger, one sentence. "none, using library opener" if nothing.]
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

For every Yes with valid email (after Step 3.5 read-back passes), end with:

> HANDOFF: invoke osi-outreach-sequence on [First Last] at [Company]. Strategy note live on HubSpot contact ID [id]. LINKED_IN_CONNECT task ID [task id] (provisional timestamp, outreach-sequence will update). Personal Hook: [hook]. Recommended sequence: [Call - Network / Server / TPM / DWDM / Storage / Networking].

Outreach-sequence owns stagger computation. It computes the real Day 1, queues all 6 emails, and updates the LINKED_IN_CONNECT task timestamp in its Step 11.

If ZI retry matrix returned no email after all 7 attempts: do NOT hand off. The 2 LI fallback tasks ARE the plan.

**IMMEDIATE HANDOFF -- NO BATCHING.** When a candidate in a Company Mode sweep is verdicted Yes, hand off to osi-outreach-sequence immediately before qualifying the next candidate. Do NOT accumulate Yes verdicts and hand off in a batch at the end. Batching causes context overflow, loses candidates, and breaks the per-candidate stagger logic. The flow is: qualify candidate -> verdict Yes -> handoff -> queue confirmed -> next candidate. Repeat. Never "I'll sequence all of them at the end."

---

## MODE 3: Auto Mode
Trigger: Andy says "find me cold companies", "auto mode", "sweep my accounts", or similar.

🚨 **SAME RULE AS COMPANY MODE: NEVER CAP CANDIDATES PER COMPANY. FIND EVERYONE WORTH REACHING OUT TO.**

### Step 0: Build the exclusion list (MANDATORY, before any HubSpot pull)

🚨 **DO THIS BEFORE PRESENTING ANY COMPANIES. Never skip.**

Read `C:\Claude-Brain\email-queue.json`. Extract every unique `company` value (case-insensitive). This is your exclusion list -- any company already in the queue has active sequences running and must NOT be presented as a cold target.

Also read the "Companies Prospected" tab of `C:\Claude-Brain\prospects-tracker-new.xlsx` for any additional historically prospected companies.

After building the exclusion list:
- Update the "Companies Prospected" tab in `C:\Claude-Brain\prospects-tracker-new.xlsx` with any companies from the queue that are not already listed there (company name + last sequence date, sorted by date descending).
- This tab is the running log of every company ever prospected. Keep it current at the start of every Auto Mode run.

### Step 1: Pull cold HubSpot companies
Search HubSpot for companies owned by Andy (owner ID 196669355) with no activity in 6+ months. Use `search_crm_objects` on the companies object, filter by `notes_last_contacted` < 180 days ago or null, `hubspot_owner_id` = 196669355. Pull up to 50 results sorted by last activity ascending (coldest first).

### Step 2: ICP pre-filter + queue exclusion
For each company, read: name, industry, employee count, city/state. Apply TWO filters:
1. Discard obvious non-fits (hyperscalers, pure software SaaS, gov agencies with no IT infra footprint). Keep telecom, ISPs, regional carriers, mid-large enterprise with data center or network infrastructure.
2. **Cross-check against the exclusion list from Step 0.** Any company whose name fuzzy-matches a name on the exclusion list (same root word, common abbreviation, or known alias -- e.g. "altafiber" = "Altafiber", "Midco" = "Midcontinent Communications") is EXCLUDED from the presented list. Do not present it. Do not mention it. It has active sequences.

### Step 3: Present the list to Andy
Show the filtered, excluded list with company name, industry, employee count, last activity date. Ask: "Which of these do you want to run first, or should I start from the top?"

### Step 4: Run Company Mode on each selected company
For each company Andy approves (or starting from the top if he says go): run the full MODE 2 Company Mode workflow. Find every relevant title. Qualify each one. Never stop early.

### Step 5: After each company
Report results (X yes, Y no, Z conditional), then move to the next company. Andy can stop after any company by saying "that's enough."

After completing a company (win or no), add it to the "Companies Prospected" tab if not already there.

Default batch: 3 companies per session unless Andy specifies otherwise or says "keep going". Within each company: NO CAP -- find everyone worth contacting.

## EXCEL TRACKER -- log every Company Mode session

Append all Yes and Conditional to `Claude-Brain/prospects-tracker-new.xlsx` (Prospects tab).

Columns: Name | Title | Company | LinkedIn URL | OSI Angle | HubSpot Status | Action | Date Added | Notes

Also maintain the "Companies Prospected" tab (separate from Prospects tab):
Columns: Company | Last Sequence Date | Source
Keep sorted by Last Sequence Date descending. Update at the start of every Auto Mode run (Step 0) and after completing each company (Step 5).

---

## FAILURE MODES

- LinkedIn URL unresolvable -> mark `no` reason "could not resolve LinkedIn profile". Do NOT guess.
- Profile restricted/closed/deleted -> qualify on available data. Critical signals hidden -> `conditional`.
- ZoomInfo retry matrix returned no FULL_MATCH after all 7 attempts -> `yes-no-email`, 2 LI fallback tasks, NO handoff. Log all 7 attempts in strategy note.
- HubSpot ownership: other rep with recent activity -> skip silent.
- Shallow-qualify input but HubSpot record missing -> fall back to deep.
- Step 3.5 read-back fails -> flip to `pending-relookup`, log, no handoff, no queue write.
- Web search times out -> proceed without, flag in strategy note.
- Chrome unresponsive -> retry once after 30s, log + mark `pending-retry`.

Every failure logs to `Claude-Brain/overnight-run-log.md`. Never silent.

---

## RULES

- Never Yes on title alone -- verify with skills + trajectory.
- Never skim search result previews -- always navigate to full profile.
- "VP" at banks (BNY, Citi, JPM) is a job grade, not seniority -- verify with skills + trajectory.
- Never disqualify based on technical depth -- OSI has engineers who join calls.
- Never guess at tech stack or buying authority -- only reference what is confirmed.
- Restricted profile -> say so, qualify on available.
- Always run the 7-attempt ZoomInfo retry matrix on every Yes. Single call is forbidden.
- City / state / timezone always from LinkedIn, never ZoomInfo.
- HubSpot tasks for connection requests -> ALWAYS `LINKED_IN_CONNECT`. Never `LINKED_IN_MESSAGE`. Never `TODO`.
- LINKED_IN_CONNECT `hs_timestamp` at creation = next business day (provisional). Outreach-sequence updates it to real Day 1 in its Step 11. Never leave null.
- Stagger calculation is outreach-sequence's job. This skill does NOT read `state.stagger` or compute Day 1.
- Step 3.5 read-back is MANDATORY before handoff. Failed read-back -> `pending-relookup`, no queue write.
- Timezone: 6-bucket only. See playbook/hubspot-data-quality.md.