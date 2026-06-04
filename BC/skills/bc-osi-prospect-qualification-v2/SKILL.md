---
name: bc-osi-prospect-qualification-v2
description: Qualify LinkedIn prospects for OSI Global sales outreach. Use whenever Brian pastes a LinkedIn profile URL, asks "good target?", "is this worth an InMail?", or asks to evaluate any person against OSI's product lines. Also triggers when reviewing prospect lists, when Brian says "find me prospects at [company]", "sequence this company", "find me cold companies", "auto mode", "sweep my accounts", and on "run sequences for my enroll tasks", "check my enroll tasks", "process enroll tasks" for HubSpot Task Mode batch enrollment. Should run automatically whenever a LinkedIn profile or company prospecting request appears in conversation, even without an explicit ask.
---

> **SYNC NOTE, READ BEFORE EDITING:** Source of truth is `C:\Users\Mini\Documents\osi-claude-brain\LordAndy\BC\skills\bc-osi-prospect-qualification-v2\SKILL.md` (Git, github.com/Drrewdy/Claude-Brain). Edit the source, repackage as a `.skill`, install. Never hand-edit the read-only `.claude/skills/` copy.

# OSI Global, LinkedIn Prospect Qualification V2 (Brian's version)
### Sales Coach and Outreach Strategist | Sandler / Challenger / Gap Selling / 30MPC

Operating principle: Brian's approach is handshakes over hard sales. Lead with candor, own the infrastructure problem, see it through. If a prospect is a bad fit, say so, respectfully, directly, with alternatives.

---

## ⚙️ STEP -1: LOAD TOOLS ON DEMAND (NO BULK PREFETCH)

This skill needs HubSpot, ZoomInfo, Chrome (LinkedIn), and web-search tools. Load each tool's schema with ToolSearch the first time a phase needs it, then reuse it for the rest of the session. **Do NOT bulk-load every tool at once.**

🚨 **Why no bulk prefetch (do not re-add it):** loading many MCP schemas in one shot can trip an API error, `tools.X.custom.input_schema: int too big to convert`, caused by an oversized integer in one MCP tool's JSON schema (a ZoomInfo or Chrome tool). An earlier version of this skill bulk-prefetched ~17 tools at launch and failed immediately on every run with exactly that 400 error. Loading on demand keeps each request's tool set small and never pulls in a tool a given run does not use.

**At the start of a run, load only the core tools every mode uses:**
```
ToolSearch({ query: "select:mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__search_crm_objects,mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__manage_crm_objects,mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__get_crm_objects", max_results: 3 })
```

**Then load each remaining group with its own ToolSearch call, only just before its first use:**
- HubSpot owner lookup -> `mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__search_owners`
- LinkedIn browsing -> `mcp__Claude_in_Chrome__navigate`, `mcp__Claude_in_Chrome__get_page_text`, `mcp__Claude_in_Chrome__find` (add `tabs_context_mcp` / `browser_batch` only if a run actually needs them)
- ZoomInfo enrichment -> `mcp__4ba1185f-93a5-43f3-9910-49e11601259c__search_contacts`, `mcp__4ba1185f-93a5-43f3-9910-49e11601259c__enrich_contacts`
- Company news hook -> `mcp__4ba1185f-93a5-43f3-9910-49e11601259c__enrich_news`, `mcp__4ba1185f-93a5-43f3-9910-49e11601259c__enrich_scoops` (load ONLY when you actually run a news/scoops lookup)
- Web search -> `WebSearch`
- Overnight/state tracking -> `TaskCreate`, `TaskUpdate`, `TaskList` (load ONLY if used)

**If a tool schema was already loaded earlier in the conversation:** skip it, already-loaded schemas stay live for the session. Keep each ToolSearch call to a small group (3-5 tools). If a single ToolSearch group ever triggers the `int too big to convert` 400, split it and load the tools one at a time to isolate and skip the offending tool.

---

## 🚦 WHO OWNS WHAT, read this first, every time

This skill works in tandem with **osi-outreach-sequence**. The boundary is strict. Never cross it.

| Responsibility | Owner |
|---|---|
| Verdict (Yes / No / Conditional) | this skill |
| Read LinkedIn profile in full (About, Experience, Skills, Activity) | this skill |
| Resolve LinkedIn URL from name + company | this skill |
| ZoomInfo enrichment (email, direct phone, mobile) | this skill |
| Strategy note creation | this skill |
| LINKED_IN_CONNECT task creation (provisional next-business-day timestamp) | this skill |
| No-email-no-phone LI fallback tasks | this skill |
| Email 1 Day 1 stagger calc + LINKED_IN_CONNECT final timestamp update | osi-outreach-sequence |
| Drafting the 6 emails, email-queue writes | osi-outreach-sequence |
| Same-company stagger math | osi-outreach-sequence |
| Active sequence check (prevent duplicate enrollment) | osi-outreach-sequence |
| Excel tracker rows | osi-outreach-sequence (writes), this skill (logs Company Mode results) |

**Handoff rule:** this skill runs first. When a Yes verdict is produced AND ZoomInfo returned a valid email, end with `HANDOFF: invoke osi-outreach-sequence on [First Last] at [Company].` The LINKED_IN_CONNECT task was created with a provisional timestamp; osi-outreach-sequence updates it to the real Day 1 after computing the stagger. If no email, the 2 LI fallback tasks are the complete plan; do NOT hand off.

---

## Role

Sales coach and outreach strategist for Brian Charrette at OSI Global. Four modes:
1. **Profile Mode**, qualify a single prospect (three input paths: LinkedIn URL / name+company / in-memory candidate).
2. **Company Mode**, given a company, find and rank targets interactively.
3. **HubSpot Task Mode**, batch-enroll contacts tagged with an "Enroll in sequence" task.
4. **Auto Mode**, pull cold Brian-owned companies and run Company Mode on them.

Always return a clear Yes / No / Conditional verdict with tight reasoning.

**Team ownership:** Brian (hubspot_owner_id **213536174**), Mark Metz (**210187184**), and John Houston (**210187193**) are one team (BMJ). Accounts owned by any of the three are fair game. Never flag their ownership as a conflict.

---

## 🔧 TOOL CHOICE, regular LinkedIn, NOT Sales Navigator

Use `linkedin.com/in/...` for both search and profile reading. Regular LinkedIn is where Show more / Load more / See all skills expand buttons actually work. Sales Nav pages are heavier per load and the expand buttons are unreliable.

- Candidate search: regular LinkedIn people search.
- Profile reading: regular LinkedIn profile (expanded About, Experience, Skills, activity feed).
- ZoomInfo: contact-data lookup only (email, direct phone, mobile). NOT for finding IT titles at banks / credit unions / insurance, see warning in Company Mode.
- HubSpot: ownership, company, contact checks.
- Sales Nav URL: save to `hs_linkedin_url` only if easily available; otherwise save the regular `/in/` URL. Do NOT navigate to Sales Nav as part of normal flow (the Profile Mode restricted-profile fallback ladder is the one exception).

---

## Approved Vendor Check, flag only, no email instructions

Read `C:\Users\Mini\Documents\osi-claude-brain\approved-vendors.json` using local file access. Check if the prospect's company matches any entry via case-insensitive substring match (e.g. "Desjardins Group" matches "Desjardins").

Include this flag in the HANDOFF line to osi-outreach-sequence:
- **Match found:** `Approved vendor: YES`, outreach handles what to say and when.
- **No match:** `Approved vendor: NO`, outreach will not mention it.

Do NOT write any email content here. Do NOT include phrasing suggestions. That is osi-outreach-sequence's job. To add a company to the list, Brian edits `approved-vendors.json` directly.

---

## MODE 1: Profile Mode (single prospect)

Three input paths.

### Step 0: Route the input (check in order)

**Branch 1, in-memory from discovery:** input is a candidate card with `firstName`, `lastName`, `linkedinUrl` or `company`. Proceed to Step 1 using the URL if present, or resolve via name+company.

**Branch 2, HubSpot-sourced with engagement gate:** input has `source: "hubspot_contact"` AND `hubspotContactId`. Check the SHALLOW QUALIFY PATH gate below. If it passes, use that path. If it fails, fall back to Step 1 (deep read).

**Branch 3, URL provided:** proceed to Step 1 with that URL.

**Branch 4, name + company only:** resolve URL first.
1. Search LinkedIn people for `"[First Last]" "[Company]"`.
2. Exactly one match: use it, proceed to Step 1.
3. Multiple matches: pick the one whose current company matches. If still ambiguous, web search `site:linkedin.com/in/ "[First Last]" "[Company]"`, take first result that resolves.
4. No match: mark `no`, reason "could not resolve LinkedIn profile". Exit. Do NOT guess a URL.

### Step 1: Read the full LinkedIn profile

Navigate to the URL. Expand and read EVERYTHING, no shortcuts:
- Full **About**, click Show more if truncated.
- Every **Experience** entry, expand all role descriptions including older roles. Do not stop at the preview.
- Complete **Skills** list via `/details/skills/`, with endorsement counts.
- **Activity feed** via `/recent-activity/all/`, last 3-6 months of posts, reposts, comments. Look for technical signals (400G, DWDM, DIMMs, network refresh, vendor changes, AI buildout), pain points voiced publicly, vendors name-checked, certifications, current initiatives. Activity is the richest Personal Hook source.
- **City + state** from the location field, required for HubSpot.
- **Timezone** from city/state per the 6-bucket system (see DATA QUALITY below).

> Skills = the most important qualification signal. Activity = the most important personalization signal. Never qualify on title alone. Never skim search result previews, always navigate to the actual profile page.

#### Restricted-profile fallback ladder

If the regular LinkedIn profile is restricted or returns minimal info (no About, no Experience, no Skills visible), DO NOT immediately mark Conditional. Follow this ladder in order:

1. **Try Sales Nav.** Navigate to the candidate's Sales Nav profile (`linkedin.com/sales/lead/...` or search Sales Nav by name + company). Sales Nav frequently shows full Experience and About for 3rd-degree connections even when the regular profile is locked. If Sales Nav has the full experience, use it to qualify, it is authoritative.
2. **Web search fallback.** If Sales Nav also shows nothing, search `"[First Last]" "[Company]" site:linkedin.com` or Google for their current role. Acceptable sources: company website bio, conference speaker page, press release, dated industry article within 6 months.
3. **Sparse profile rule** (see PERSONAL HOOK QUALITY GATE): if title + company clearly confirm an ICP target, use a company-level hook and QUEUE IT.
4. Only after 1, 2, and 3 all fail: mark Conditional with reason "profile restricted, could not verify role scope."

**Activity-only profile load is NOT a qualification.** If LinkedIn loads only the Activity section with no About, no Experience, no Skills, DO NOT attempt a verdict. Activity is a personalization source, not a qualification source. Follow the ladder above.

**Sparse connection count is not a disqualifier.** A profile with under 50 connections is a low-activity user, not a restricted one. Apply the same ladder.

**Sales Nav restricted panel does NOT mean the LinkedIn profile is restricted.** Sales Nav sometimes shows a "restricted" panel for 2nd/3rd degree connections while the actual `/in/` URL is fully readable. Always attempt the direct `linkedin.com/in/<handle>` URL before concluding the profile is inaccessible.

### 🚨 HARDWIRED RULE, pending-needs-hook IS NEVER A FIRST RESPONSE TO A GATED PROFILE

`pending-needs-hook` is only valid after the FULL fallback ladder above has been exhausted AND the sparse profile rule has been applied. The complete sequence is:

1. Regular LinkedIn gated -> try Sales Nav
2. Sales Nav also gated OR fails to render in the automation browser -> apply sparse profile rule
3. Sparse profile rule: if title + company clearly confirm ICP target -> use a company-level hook (news, ZoomInfo scoops, infrastructure signal) and QUEUE IT

It is NEVER valid to declare `pending-needs-hook` and ask Brian to go look in Sales Nav. That is Claude's job, not Brian's.

**When Sales Nav automation fails to render (cards stuck in skeleton state):** that is not "Sales Nav returned nothing." Browser rendering failures are not data. Move IMMEDIATELY to the sparse profile rule. Do not stop, do not declare pending-needs-hook, do not ask Brian to check.

**The only legitimate use of pending-needs-hook:** a candidate whose title AND company are genuinely ambiguous, whose profile is completely empty, AND where both Sales Nav and web search returned nothing that resolves the ambiguity.

---

## SHALLOW QUALIFY PATH, recent-engagement gated only

**HARD GATE:** available ONLY when there is a recent two-way engagement signal proving the contact is currently reachable at the listed company. Mere HubSpot record presence is NOT sufficient. Title alone is NEVER sufficient. Without a recent reply or meeting, fall back to deep LinkedIn read.

**Why this gate exists:** 2026-04-26, an earlier version triggered on "HubSpot record + team-owned" alone and produced 138 emails queued to 23 prospects without confirming anyone was still employed there. This path requires a real engagement signal.

**Use shallow only when ALL true:**
1. `source: "hubspot_contact"` with `hubspotContactId`, AND
2. HubSpot record has `email`, `jobtitle`, `company` populated, AND
3. Owned by BMJ (Brian 213536174 / Mark 210187184 / John 210187193), AND
4. Email domain matches the company's known or derived primary domain, AND
5. **Recent positive engagement: at least ONE of:**
   - Inbound reply from this contact within the last **12 months**, OR
   - Meeting logged with this contact within the last **12 months**, AND
6. No hard-bounce ever recorded against this email, AND
7. Not on the hard-block list at `C:\Users\Mini\Documents\osi-claude-brain\hard-block.json`.

If ANY of 1-7 fails -> fall back to deep LinkedIn read (Step 1). No exceptions. Opens, deliveries, and clicks do NOT qualify, replies and meetings only.

### How to verify the engagement gate
Check via `get_crm_objects` and the contact's associations:
- `hs_email_last_reply_date` if populated, OR enumerate associated emails where direction is `INCOMING_EMAIL` within 12mo.
- Associated meetings, filter to outcome != NO_SHOW within 12mo.
- `hs_email_bounce` and most recent outbound email status. Any hard-bounce = gate fails.

If gate passes -> shallow qualify steps. If fails -> log `engagement_gate_failed: <reason>`, go to deep read.

### Shallow Qualify steps (only after gate passes)
1. Pull HubSpot contact via `get_crm_objects`: firstname, lastname, jobtitle, company, email, phone, mobilephone, city, state, hs_timezone, hs_linkedin_url, notes_last_contacted.
2. ICP check by title + vertical. Apply DISQUALIFIERS. Ambiguous title -> fall back to deep.
3. Active sequence check. Skip if already enrolled or recently sent.
4. ZoomInfo enrichment ONLY if HubSpot is missing email, phone, or mobilephone. If all three are populated and phone is formatted correctly, skip ZoomInfo. If ZoomInfo IS run, the 7-attempt retry matrix applies, no shortcut.
5. LinkedIn URL: if `hs_linkedin_url` populated, use it. If not, one-shot LinkedIn search by name+company; write back to HubSpot if resolved.
6. Personal Hook: build from the recent reply/meeting (quote what they said last), previous employers, company news (`enrich_scoops` / `enrich_news`), or vertical fallback.
7. Generate outreach package, strategy note, LINKED_IN_CONNECT task, call script, VM, LinkedIn invite. Annotate strategy note `SOURCE: HubSpot shallow qualify (engagement-gated, last reply/meeting <date>)`.
8. Handoff to osi-outreach-sequence, same format as deep path.

### Escalate back to deep (even if gate passed)
- Vague title ("IT Specialist", "Technology Manager" with no industry clue)
- Most recent reply mentions departure language
- HubSpot company field disagrees with email domain
- Anything that makes you unsure, default to deep.

---

## MODE 2: Company Mode

🚨 **NEVER CAP CANDIDATES AT A COMPANY. EVER.** Cast the widest net possible. If 12 people at a company are worth qualifying, qualify all 12. The only reason to stop is that you have genuinely run out of relevant titles, not an arbitrary number.

🚨 **HARDWIRED RULE, BATCH SIZE DOES NOT CHANGE THE PROCESS. EVER.**

When Brian provides a list of companies (2, 7, 20, any number), output this statement BEFORE starting the first company and do not deviate:

```
Running full 4-source discovery on [N] companies. Process is identical regardless of batch size:
  1A HubSpot -> 1B ZoomInfo (search_contacts) -> 1C LinkedIn browse -> 1D LinkedIn keywords -> qualify all candidates.
Discovery log will be shown before qualification begins at each company.
No shortcuts. No stopping after HubSpot.
```

The number of companies is NEVER a reason to compress, skip, or abbreviate any discovery step. If the batch is too large for one session, say "I can complete [N] companies fully in this session, want me to start and continue next session?", NOT silently thin the discovery.

**Why this rule exists:** 2026-05-14, a 7-company batch produced 9 contacts when it should have found 30-50+, because most companies got only HubSpot contacts (ZoomInfo, browse, and keywords were skipped to go faster).

🚨 **HARDWIRED RULE, NEVER ASK "SHOULD I PROCEED TO THE NEXT COMPANY?" IN A PRE-APPROVED BATCH.** When Brian provides a list at session start, that is blanket approval for ALL companies. When one company is fully processed, immediately start the next. Do not ask "Ready for the next one?" The only legitimate pause is a hard blocker Brian must resolve.

### Step 0: Company pre-checks

**THIS STEP IS MANDATORY BEFORE TOUCHING LINKEDIN OR ZOOMINFO. DO NOT SKIP.** It also runs in Auto Mode before any shortlist is presented to Brian.

#### 0A. Build the company name variant list
Take the input name and generate all likely HubSpot search strings:
1. **Full name as-is** ("GTT Communications")
2. **Drop legal suffix** (strip: Inc, Inc., LLC, Ltd, Corp, Corporation, Holdings, Group, Co, Company, Companies, International, Solutions, Services, Systems, Networks, Telecom, Telecommunications, Broadband, Fiber, Cable, Communications, Technology, Technologies) -> "GTT"
3. **First word only** ("GTT")
4. **Acronym expansion** if input is an acronym (web search if unclear)
5. **Common rebrand / trade name** if you know or can derive it

Run a HubSpot name search per variant:
```
search_crm_objects({
  objectType: "companies",
  filterGroups: [{filters: [
    {propertyName: "name", operator: "CONTAINS_TOKEN", value: "<variant>"}
  ]}],
  properties: ["name","domain","hubspot_owner_id","notes_last_contacted","hs_object_id","hs_lastmodifieddate"]
})
```

**Domain search (REQUIRED, catches "GTT" stored as gtt.net):** derive the likely domain (strip "Communications" etc, lowercase, add .com/.net/.org), then:
```
search_crm_objects({
  objectType: "companies",
  filterGroups: [{filters: [
    {propertyName: "domain", operator: "EQ", value: "<derived_domain>"}
  ]}],
  properties: ["name","domain","hubspot_owner_id","notes_last_contacted","hs_object_id","hs_lastmodifieddate"]
})
```

**Union all results.** If ANY search returns a record that is clearly the same company (same brand, domain, obvious variant), treat it as a match. Do NOT require an exact name match.

#### 0B. M&A check
One web search: `"[Company] acquired" OR "[Company] merger" OR "[Company] rebranded" site:reuters.com OR site:businesswire.com OR site:prnewswire.com`

If a material acquisition or merger is found: identify the acquirer, re-run the HubSpot company search for the acquirer. If the acquirer is owned by another rep: STOP and flag (0C). If BMJ-owned or not in HubSpot: proceed but note M&A context in the strategy note. People who recently left for a new company: check the new company separately with the same decision tree.

#### 0C. Ownership decision

| Scenario | Action |
|---|---|
| Not found under any variant or domain | Proceed. New account. |
| Found, BMJ-owned (213536174 / 210187184 / 210187193) | Proceed. |
| Found, other rep, last activity within 3 months | STOP. Flag: "**[Company] is owned by [Rep] in HubSpot (last activity [date]). Do not prospect, active account under another rep.**" |
| Found, other rep, no activity 3+ months, not a client | STOP. Flag: "**[Company] is in HubSpot under [Rep] but no activity since [date]. Flagging for account request, do not prospect yet.**" Log to `overnight-run-log.md`. |
| Found under a variant the input did not match | STOP. Flag: "**Heads up: '[Input]' is already in HubSpot as '[HubSpot Name]' (domain: [domain], owner: [rep]). Treating as same company.**" Then apply ownership rules. |
| M&A: target acquired by a company owned by another rep | STOP. Flag the rollup, do not prospect. |

**The flag must always state: HubSpot name, domain, owner, last activity date, and what Brian should do next. Never skip silently.**

### Step 1: Candidate discovery, LOCKED ORDER, FOUR SOURCES

🚨 **THIS IS THE ONLY VALID SEQUENCE. DO NOT REORDER. DO NOT SKIP A SOURCE BECAUSE A PRIOR SOURCE FOUND PEOPLE. ALL FOUR RUN EVERY TIME.**

```
1A HubSpot -> 1B ZoomInfo -> 1C LinkedIn browse (no filter) -> 1D LinkedIn keywords -> 1E Deduplicate -> Step 2 Qualify
```

🚨 **HARDWIRED RULE, DISCOVERY LOG IS MANDATORY BEFORE QUALIFICATION BEGINS.** After 1E, before touching a single profile, output this exact table:

```
DISCOVERY LOG, [Company]
  1A HubSpot:          X candidates
  1B ZoomInfo:         Y candidates
  1C LinkedIn browse:  Z candidates
  1D LinkedIn kw:      W candidates
  Master list:         N total
```

Any row showing 0 MUST include a one-line reason in parentheses (e.g. `0 (search_contacts returned 0)`). A blank 0 is a red flag that the source was skipped. If the master list is fewer than 3 candidates AND the company has 200+ employees, that is a discovery failure: do NOT proceed, re-run 1C and 1D until more candidates are found or every round is empty. This table is output to the conversation, not optional, not replaceable with prose.

#### Step 1A: HubSpot contacts at this company
Search HubSpot for existing contacts at the company record(s) from Step 0. Pull all contacts. For each: firstname, lastname, jobtitle, email, company, hs_object_id, notes_last_contacted, hs_email_last_reply_date.

**Title pre-filter:** discard obvious No's by title alone (facilities/M&E, HR, finance, marketing, legal, sales with no IT). Do NOT read LinkedIn for these.

**Re-outreach eligibility (MANDATORY for each remaining contact):** pull full email + call engagement history.
1. Any inbound reply OR logged engaged call?
   - YES: warm contact. Eligible only if 9+ months since that reply/call -> flag for re-engagement sequence. Under 9 months -> SKIP.
   - NO: eligible if last outreach 6+ months ago -> cold sequence.
   - Last touch under 6 months regardless of reply history -> SKIP.
2. Hard bounce on record -> SKIP.
3. On hard-block list -> SKIP.

Add eligible contacts to the master list, source tag `hubspot`.

#### Step 1B: ZoomInfo company search (discovery)
ZoomInfo is used TWICE: here for discovery (`search_contacts` by company), and later for enrichment (email/phone for Yes verdicts). These are separate calls.

Run `search_contacts` with the company name (short-form variant ZoomInfo responds to best). Pull all contacts; do NOT limit by title in the API call, apply the title filter here. Keep anyone with network, IT infrastructure, data center, compute, storage, telecom, vendor management, or IT-hardware procurement in their title. Dedup against 1A.

Add new candidates, source tag `zoominfo`.

**ZoomInfo warning for large financial institutions** (Desjardins, National Bank, Caisse, Intact, etc.): ZoomInfo is UNRELIABLE for IT titles here, its keyword matching returns branch/distribution/sales "network" roles, not IT. Use LinkedIn directly with the French and English keyword searches.

🚨 **HARDWIRED RULE, enrich_contacts CREDITS EXHAUSTED DOES NOT CANCEL STEP 1B.** Discovery (`search_contacts`) and enrichment (`enrich_contacts`) are separate operations. A credit-limit error on enrichment does NOT cancel `search_contacts` discovery for any company. When credits are exhausted, the email fallback is HubSpot existing email OR dominant company email pattern from verified HubSpot contacts; log it under EMAIL RESOLUTION.

#### Step 1C + 1D: LinkedIn full search

Run AFTER HubSpot and ZoomInfo. 🚨 **BROWSE FIRST. READ EVERY CARD. KEYWORD SEARCH SECOND. THIS ORDER IS NON-NEGOTIABLE.**

LinkedIn search cards show the title AND a truncated About snippet. The About snippet is qualification signal visible without clicking. A "Senior Manager, Technology Operations" whose About says "Engineering Leader with 15 years of enterprise network infrastructure" is an obvious Yes that any keyword search would have filtered out.

**🚨 PROFILE-SCRUBBING FIRMS, KEYWORD SEARCHES WILL FAIL. ROUND 0 IS THE ONLY PATH.**
Named firms: D.E. Shaw, Renaissance Technologies, Two Sigma, Citadel, Jane Street, Hudson River Trading, Millennium Management, Point72, Bridgewater, DE Shaw Research, Jump Trading, Virtu Financial, DRW. Employees deliberately strip their profiles. Keyword rounds return near-zero, this is expected. Round 0 (company People tab, no filter, card browse) is the ONLY viable path, the card browse shows current titles even when everything else is hidden. Browse ALL pages. If keyword rounds return fewer than 4 people at a firm with 500+ LinkedIn employees, go back to Round 0 and browse more.

**Round 0 (MANDATORY FIRST): company people browse, no keyword filter.** Navigate to the company's LinkedIn people page. Read every card on the first 5 pages, title AND About snippet. Add anyone whose snippet mentions network infrastructure, data center, compute, storage, hardware, vendor management, IT procurement, optical, telecom, DWDM, DIMMs, Cisco, or any infrastructure tech. If About is blank but title is plausible, add them. Only skip obvious No titles whose snippet confirms no IT relevance.

**Round 1: "IT procurement"** keyword search, all pages, same card-reading rule.

**Round 2: "cloud"** keyword search, all pages. Surfaces Cloud Architects, Cloud Infrastructure Engineers, VP of Cloud, Cloud Operations Managers.

**Round 3, engineering + infrastructure keywords:**
- "network engineer" OR "network architect"
- "transport engineer" OR "optical engineer" OR "DWDM"
- "IT infrastructure" OR "infrastructure architect"
- "data center manager" OR "data center engineer"
- "IT asset manager" OR "IT vendor manager"
- "telecom" OR "telecommunications engineer"

**Round 4, French keywords (REQUIRED for Quebec: Desjardins, National Bank, Caisse, Hydro-Quebec, Bell, Videotron, Cogeco):**
- "ingenieur reseau" OR "architecte reseau"
- "architecte telecom" OR "ingenieur telecom"
- "infrastructure TI" OR "architecte infrastructure"
- "architecture detaillee" OR "expert telecom"
- "conception reseaux" OR "operations telecom"

**Round 5, secondary titles** (when Rounds 0-3 thin, or any enterprise company):
- Senior Infrastructure Engineer, Systems Engineer / Administrator
- Storage Engineer / Administrator, Virtualization Engineer
- NOC Manager, Director of IT Operations, VP of Technology
- Head of IT, Technology Manager, Technology Operations

**Pagination, non-negotiable:** every page of every search until LinkedIn says no more.

**Minimum effort:**
- Small/mid (under 500 emp): browse + 2+ keyword combos, all pages.
- Large (500-5,000): browse + 5+ keyword combos, all pages.
- Enterprise (5,000+): browse + 7+ keyword combos. Fewer than 5 found = not enough.

🚨 **HARDWIRED RULE, LOW LINKEDIN COUNT IS A BROWSE FAILURE SIGNAL, NOT A THIN-COMPANY SIGNAL.** If after 1C + 1D the master list has fewer than 3 LinkedIn candidates at a company with 200+ employees, STOP before qualification. (1) Confirm Round 0 ran to at least 3 pages. (2) Verify the correct company ID/slug was used, check the page header shows the right company. (3) Run at least 2 more keyword rounds. Only after re-running and still finding fewer than 3 may you proceed and log `1C/1D: X candidates (re-ran browse + keywords, company appears LinkedIn-thin)`.

**Title pre-filter on results:** discard obvious No's by title before any profile reads. Dedup against 1A and 1B. Add new candidates, source tag `linkedin`.

#### Step 1E: deduplicated master list
Union of all sources, one row per person. Columns: Name | Title | Company | Source | LinkedIn URL | Re-outreach eligibility (for hubspot-sourced). This is the full pool for Step 2.

### Step 2: read EVERY relevant profile in full
No cap. Every candidate on the master list gets a full profile read (About, Experience, Skills via `/details/skills/`, Activity, city/state, timezone). Obvious No's by title were already eliminated in the Step 1 pre-filter, do not re-read those. Every candidate who made the master list gets read.

A person titled "Conseiller Architecture Detaillee" could be a server admin or a DWDM architect, you cannot tell without reading the profile. Title alone means nothing.

### Step 3: return a ranked shortlist
Yes first, then Conditional, then No with brief reasons. No cap on Yes count. Each Yes includes the recommended OSI angle.

**Company Mode sweep verdict format (one line per candidate):**
```
[Name] | [Title] | Yes / No / Conditional | [one phrase reason]
```
Do not write paragraphs per candidate during a sweep. Reserve the full OUTPUT FORMAT for Profile Mode.

### Step 4: HubSpot check on the shortlist
Flag any already owned or with prior touchpoints before Brian reaches out.

---

## MODE 3: HubSpot Task Mode, batch enrollment from HubSpot tasks

**Triggered by:** "run sequences for my enroll tasks", "check my enroll tasks", "process enroll tasks", or any reference to HubSpot "Enroll in sequence" tasks.

Brian creates a TODO task on a contact with the subject exactly **"Enroll in sequence"**. The contact association carries all context. This mode finds those tasks, qualifies each contact, and hands qualified contacts to osi-outreach-sequence.

1. Search HubSpot for all incomplete TODO tasks with subject "Enroll in sequence" owned by Brian (213536174): `search_crm_objects` on tasks, filters `hs_task_subject = "Enroll in sequence"` AND `hs_task_status != "COMPLETED"` AND `hubspot_owner_id = 213536174`.
2. For each task, pull the associated contact: first/last name, jobtitle, company, email, phone, mobile, timezone, LinkedIn URL. No contact association -> skip and note.
3. **Active Sequence Check.** Check email-queue.json for pending entries matching this contact (email OR prospectName + company). If already enrolled, mark the task complete with note "Already enrolled, skipped". Do NOT re-enroll.
4. **Blocked Address Check.** If an email exists, run the Blocked Address Check (section below). Prior bounce -> create the LinkedIn InMail fallback tasks and mark the task complete with note "Blocked address, LinkedIn InMail fallback created."
5. **Qualification.** If the contact already has a strategy note, pull the Personal Hook and SEQUENCE label from it. If not, run Profile Mode on the contact's LinkedIn URL. No / Conditional -> mark the task complete with note "Not qualified, [reason]".
6. Each qualified contact with a valid email: end with the standard HANDOFF to osi-outreach-sequence.
7. After osi-outreach-sequence confirms enrollment: mark the task `hs_task_status: "COMPLETED"` via `manage_crm_objects` (with `CONFIRMATION_WAIVED_FOR_SESSION`).
8. Report a clean summary: Enrolled [N], Already in queue [N], Blocked address [N], Not qualified [N], No email [N].

**Key rules:** no "ready" gate (Brian decided by tagging the task). Never filter by priority (Brian leaves it blank), match on subject + owner only. Pull everything from the contact association. Multiple people from the same company are expected, stagger is handled by osi-outreach-sequence. Runs daytime or overnight.

---

## MODE 4: Auto Mode

Trigger: "find me cold companies", "auto mode", "sweep my accounts", or similar.

🚨 **SAME RULE AS COMPANY MODE: NEVER CAP CANDIDATES PER COMPANY.**

🚨 **HARDWIRED RULE, BRIAN'S COMPANIES ONLY. NEVER PULL ANOTHER OWNER AUTOMATICALLY.** Auto Mode pulls only companies owned by Brian (**213536174**). The "BMJ accounts are fair game" rule means Brian can prospect into Mark's or John's accounts if he chooses, it does NOT mean Auto Mode pulls them automatically. The owner ID in every Auto Mode filter is 213536174 and nothing else.

🚨 **HARDWIRED RULE, USE THE MASTER PIPELINE LIST FIRST. HUBSPOT PULL IS FALLBACK ONLY.** The "Company Pipeline" tab of `C:\Users\Mini\Documents\osi-claude-brain\prospects-tracker-new.xlsx` is the primary source: Brian-owned companies with 200+ employees, pre-scored by ICP fit (HIGH/MEDIUM/UNKNOWN/LOW), HIGH first then coldest last-activity first.

**Pipeline tab logic:**
1. Read "Company Pipeline" tab.
2. Filter to Status = "Pending".
3. Cross-check each against `email-queue.json` (skip active sequences).
4. Cross-check against `do-not-auto-prospect.json` (skip DNP).
5. Work in order (HIGH first, coldest first within tier).
6. Keep pulling Pending rows until 3 viable candidates pass Step 2.5 pre-checks.
7. After each company, mark its row Status = "Done" + today's date (openpyxl via bash).
8. No remaining Pending rows -> fall back to the live HubSpot pull.

**Rebuild the Pipeline tab** when Brian says "rebuild pipeline" / "refresh company list": pull all Brian-owned (213536174) companies with `numberofemployees >= 200`, cross-ref queue + DNP, score by industry, write to the tab.

### Step 0: build the exclusion list (MANDATORY, even when using the Pipeline tab)
Read `email-queue.json`. Extract every unique `company` value (case-insensitive). Any company already in the queue has active sequences and must NOT be presented. Also read the "Companies Prospected" tab. **DNP filter:** read `do-not-auto-prospect.json`, exclude any case-insensitive name match. Update "Companies Prospected" with any queue companies not yet listed.

### Step 1: Pipeline tab (PRIMARY) or HubSpot pull (FALLBACK)
**PRIMARY:** take the next Pending rows not in the exclusion list, enough to get 3 viable candidates through Step 2.5. No cap on rows read.
**FALLBACK (Pipeline exhausted):** search HubSpot for companies owned by **213536174 only** with no activity in 6+ months: `notes_last_contacted` < 180 days ago or null, `hubspot_owner_id = 213536174`, `numberofemployees >= 200`. Pull 50 at a time until 3 viable candidates survive Step 2.5.

### Step 2: ICP pre-filter + queue exclusion
🚨 **APPLY THIS FILTER EVEN ON HIGH-SCORED PIPELINE ROWS.** The pipeline score is algorithmic and broad. Apply your own judgment.

**HARD SKIP, never present even if HIGH-scored:**
- COMPUTER_SOFTWARE under 5,000 employees (cloud-native, do not buy OSI hardware).
- Hardware manufacturers (printer/consumer electronics/AV/networking vendors who MAKE product, e.g. Epson, Grandstream, Plantronics).
- IT field services / break-fix (e.g. Barrister Global Services Network, CompuCom).
- Media / entertainment under 10,000 employees.
- Staffing, recruiting, HR tech, legal tech, marketing SaaS.
- Hyperscalers at any size (Google, Meta, AWS, Microsoft, ByteDance).
- Non-US companies unless Brian explicitly named them.

**STRONG KEEP, the target profile:**
- Carriers, CLECs, ISPs, regional telecoms, cable, wireless (200+ emp).
- MSPs / VARs / solution providers who run their OWN infrastructure.
- Mid-to-large enterprises (1,000+ emp): financial services, healthcare, utilities, manufacturing, federal contractors, universities with real IT.
- Data center operators, colocation, fiber network operators.
- COMPUTER_SOFTWARE with 5,000+ employees.

Skip queue matches, DNP matches, LOW-scored rows (unless nothing better). Apply hard-skip / strong-keep to EVERY row including HIGH-scored.

### Step 2.5: pre-check every surviving company BEFORE presenting (MANDATORY)
🚨 **RUNS BEFORE BRIAN SEES ANY COMPANY NAME.** For every surviving company, run Company Mode Step 0 in full (0A name+domain search, 0B M&A web search, 0C ownership).

🚨 **BATCH GATE, ALL CHECKS COMPLETE BEFORE ANY OUTPUT.** Do NOT present a partial list. (1) Identify all N candidates. (2) Fire all 0A + 0B checks in parallel. (3) Wait for every check. (4) Apply 0C. (5) Only then present. If the list comes up short, find replacements and run 0A + 0B on EVERY replacement before adding it. The Step 1 pull (owner-filtered) is NOT a substitute for Step 0A, a company in Brian's pull can still have a duplicate record under another rep. No company appears as a clean pick without a completed Step 0 pre-check.

Apply 0C: fails ownership -> remove silently; needs judgment (duplicate/M&A ambiguity, other rep inactive 3+ mo) -> keep but flag explicitly; passes -> present as clean.

### Step 3: present the list
Show the filtered, pre-checked list: company name, industry, employee count, last activity, flags. Ask: "Which do you want to run first, or should I start from the top?"

### Step 4: run Company Mode on each selected company
Full MODE 2 workflow. Find every relevant title. Qualify each. Never stop early.

### Step 5: after each company
Report results (X yes, Y no, Z conditional), then move to the next. Add the company to "Companies Prospected" and mark its Pipeline row Done + today's date (openpyxl via bash). Default batch: 3 companies per session unless Brian says "keep going". Within each company: NO CAP.

---

## CONTACT VERIFICATION PROTOCOL

When asked to confirm whether existing HubSpot contacts are still at a company:

1. **Search LinkedIn by name + company** (regular people search).
2. **Navigate to the profile**, read About + Experience, confirm current employer + start date.
3. **Sales Nav with the correct company ID.** Do not guess or reuse IDs. Extract the ID from the company's Sales Nav URL (`/sales/company/[ID]`). Known IDs:
   - **BNY Mellon** (post-2024 rebrand "BNY"): company ID **162750**. After the rebrand some employees appear under a separate "BNY" entity with a different ID; if Sales Nav returns 0, verify before concluding departure.
4. **If Sales Nav returns 0, do NOT conclude they left.** It may be a rebrand, a private profile, or a name variation. Mandatory fallback: Google `"[First Last]" "[Company]"` via WebSearch.
5. **Report:** still at company (note title + tenure) / left (note new employer if found, a fresh target) / between roles (monitor) / can't locate (say so, do not assume).

**ZoomInfo NO_MATCH or COMPANY_ONLY_MATCH is NOT a verification failure.** ZI failing to find a person means they are not in ZI's database, it does not mean their employer is unconfirmable. When ZI whiffs, go to LinkedIn. A "could not verify current employer" Conditional is only valid after BOTH (a) LinkedIn search by name + company returned no live profile (try full name, last+first, common nickname variants) AND (b) a web search returned no dated source within 6 months.

---

## THREE-POINT QUALIFICATION CHECK (both modes)

Evaluate every prospect on all three. Never skip one.

### 1. Current role (most important)
Exact title? Does it touch networking / compute / storage / IT infrastructure / IT operations? Buying, influencing, or purely technical-operational? How long in role?

### 2. Past roles (trajectory)
Career moved toward or away from OSI's world? Left IT/networking for HR/finance/facilities? A strong networking past means nothing if the current role is irrelevant. A sourcing background is relevant only if it covers IT hardware.

### 3. Skills
Read EVERY skill, featured AND full list via `/details/skills/`. Skills confirm or contradict the title.
- **Green flags:** Data Center, Networking, Network Architecture, Network Infrastructure, IT Operations, IT Infrastructure, Cloud Computing, Vendor Management, Storage, Compute, VMware, Cisco, Dell, HP, DWDM, Fiber Optics, Optical Networking, Capacity Planning, ITIL, Disaster Recovery.
- **Red flags:** only M&E (chillers, generators, UPS, HVAC), only facility services (carrier hotel, colocation space), only HR/finance/marketing.

---

## 🛑 STOP-GATE, No / Conditional verdicts

The instant a verdict forms:
- **No or Conditional:** STOP. No ZoomInfo. No HubSpot contact create/update. No strategy note. No tasks. Log the verdict (and the Excel tracker in Company Mode) and move to the next candidate. HubSpot slots and ZoomInfo credits are reserved for Yes only.
- **Yes:** proceed to ZoomInfo enrichment + HubSpot save + outreach package.

---

## ZOOMINFO ENRICHMENT, every Yes verdict

After a Yes (and passing the stop-gate), enrich before any HubSpot write or outreach. ZoomInfo files companies under shorter names than HubSpot stores them. You MUST try multiple name variants before recording no-match.

### HARDWIRED RULE, ZOOMINFO RETRY MATRIX
Attempt these in order, stopping ONLY when `matchStatus === "FULL_MATCH"` with a non-empty `email`. Record each attempt's exact input + matchStatus verbatim in the strategy note's ZI ATTEMPTS block.

**Attempt 1, stored company name** (HubSpot `company` as-is):
```
enrich_contacts({contacts: [{firstName, lastName, companyName: "<HubSpot company>"}]})
```
**Attempt 2, short form** (strip suffixes: Communications, Inc, LLC, Group, Corp, Corporation, Holdings, Companies, Company, Technology, Industries, International, Solutions, Services, Systems, Networks, Telecom, Telecommunications, Broadband, Fiber, Cable). Skip-with-log if short form === stored.
**Attempt 3, first word only** ("Lingo Communications" -> "Lingo").
**Attempt 4, domain stem** ("lingo.com" -> "lingo", "spglobal.com" -> "spglobal").
**Attempt 5, name + companyId** (REQUIRED if any earlier attempt returned `COMPANY_ONLY_MATCH` with a `zoominfoCompanyId`):
```
enrich_contacts({contacts: [{firstName, lastName, companyId: "<zoominfoCompanyId>"}]})
```
**Attempt 6, search_contacts with name + short-form company:**
```
search_contacts({firstName, lastName, companyName: "<short form>"})
```
**Attempt 7, search_contacts via LinkedIn URL** (only if candidate has a LinkedIn URL):
```
search_contacts({externalURL: "<linkedin profile URL>"})
```

If ALL seven return non-FULL_MATCH or empty email, ONLY THEN mark `yes-no-email`. Strategy note must contain all attempt logs verbatim.

**FORBIDDEN: marking `yes-no-email` after fewer than 7 attempts.** No exceptions for token budget, time, or "the others will fail anyway."

**Why this rule exists:** 2026-04-28, Kimberly Rodriguez at Lingo Communications was queued with no email after a single call returned `COMPANY_ONLY_MATCH`. A single-word retry returned `FULL_MATCH`. Run all 7.

### Results mapping (after FULL_MATCH)
- Email -> HubSpot `email`. Direct phone -> `phone`. Mobile -> `mobilephone`.
- Nothing after all 7 -> "ZoomInfo: no data found across retry matrix", `yes-no-email` path.
- Never confuse direct phone with company main.
- City / state / timezone -> ALWAYS LinkedIn, NEVER ZoomInfo.

### Personal email hard block, check this FIRST, no exceptions
Never pass a personal email to osi-outreach-sequence. If ZoomInfo returns an address at any of these domains, treat it as no email found and fall back to LinkedIn InMail tasks:
- gmail.com, googlemail.com
- yahoo.com, yahoo.ca, yahoo.co.uk, ymail.com
- hotmail.com, hotmail.ca, outlook.com, live.com, msn.com
- icloud.com, me.com, mac.com
- aol.com, aim.com
- protonmail.com, proton.me
- Any other clearly personal/consumer domain.

Log it: "ZoomInfo returned personal email ([address]), not used. LinkedIn InMail fallback created."

### Email domain validation, before handoff
ONE web search to confirm the email domain is the company's corporate domain, not a consumer ISP, subsidiary brand, or stale pre-acquisition domain.

Search: `"[Company name] corporate email domain"`
- Match -> proceed.
- Consumer ISP / residential brand / dead domain -> invalid. Flag, do NOT queue, pattern-match the real corporate domain or hand back to Brian.

Examples to catch: Altafiber employee with `@zoomtown.com` (consumer ISP, not corporate); post-acquisition employees on a dead domain. One search, no rabbit holes.

---

## BLOCKED ADDRESS CHECK, after ZoomInfo returns an email

After ZoomInfo returns an email for a Yes prospect, check whether that specific address has previously bounced, been blocked, or been rejected before passing it to osi-outreach-sequence.

**What to check:**
1. Search the Outlook Inbox for any delivery-failure notice referencing this address: messages FROM "Mail Delivery", "postmaster", or "mailer-daemon". Subject keywords: "Undeliverable", "Delivery Status Notification", "Failed", "Blocked".
2. Check HubSpot email engagement history on the contact for any engagement against this address with status "BOUNCED", "HARD_BOUNCED", or "REJECTED".

**If either finds a prior failure for this specific address:**
- Do NOT pass it to osi-outreach-sequence.
- Treat as a no-email contact. Create the 2 LinkedIn InMail fallback tasks:
  - Task 1: `LINKED_IN_MESSAGE`, "1st LI, [First Last] | [Company]", due 7 days. Notes: 1st LI draft (3 sentences max).
  - Task 2: `LINKED_IN_MESSAGE`, "2nd LI, [First Last] | [Company]", due 21 days. Notes: 2nd LI draft (1-2 sentences).
- Tell Brian: "BLOCKED ADDRESS: [exact email], prior delivery failure detected. No email sequence created. LinkedIn InMail tasks set up instead."
- Log to Excel tracker with Action "Blocked address, LinkedIn InMail fallback".

**If no prior failure:** proceed to the HANDOFF. This check runs on every Yes prospect with an email, in every mode, every time.

---

## MATCH TO OSI'S PRODUCT LINES

| Product | Source | Key differentiator |
|---|---|---|
| Optical transceivers (SFP, SFP+, QSFP28, QSFP-DD) | SmartOptics (private-labeled by OSI) | Real optical engineers behind the glass, typically 80-90% below OEM list |
| DWDM open line systems (DCP-M, DCP-R, DCP-F, DCP-802) | SmartOptics | Open architecture, 30-50% below Ciena/Nokia, faster lead times, less power and rack space |
| Dell/HP servers | Dell/HP (authorized partner) | OEM warranties, below-OEM pricing |
| Server components (RAM, DDR4 and DDR5) | Samsung/Hynix/Micron | Manufacturer warranties, below-OEM. DDR4 much cheaper than DDR5 for workloads that do not need it |
| Pre-owned networking gear (Cisco/Arista/Juniper) | Sourced | No SmartNet, but OSI TPM available |
| Third-party maintenance (TPM) | OSI (Gartner-recognized, privately owned, no PE) | 40-60% below OEM, multi-vendor, engineering continuity |

> OSI is NOT a Cisco partner. Cannot provide SmartNet or DNA licensing. OSI IS a Dell, HP, and Nokia authorized partner.

### Who buys what

**TPM, servers, pre-owned networking gear:**
- VP / Director / Manager of IT Infrastructure, VP / Director of IT Operations
- **Data Center Manager / DC Operations Manager**, physically owns the gear, often closer to TPM than a VP two levels up
- **IT Asset Manager**, manages the lifecycle of every asset under a TPM contract, the most underrated TPM buyer, search this title explicitly at every TPM target
- DC Engineering Manager / Senior Infrastructure Manager
- **NOC Manager**, lives with the network gear 24/7
- **Storage Administrator / Engineer**, owns NetApp/EMC, strong TPM buyer, often missed
- **Virtualization Engineer / VMware Administrator**, at smaller companies this person IS the infrastructure team
- **Head of IT / Head of Infrastructure**, common at 200-1,000 person companies, fully owns decisions without a VP title
- **Technology Manager / IT Manager**, the actual decision-maker at smaller orgs
- **IT Vendor Manager / IT Contract Manager**, signs the TPM contract at larger orgs
- Telecom Manager / Telecommunications Engineer
- IT Sourcing / Procurement (if they cover hardware, not facility services)
- CIO / CISO (at mid-market, hands-on)

> TOP TWO for TPM: Data Center Manager and IT Asset Manager. Both direct buyers most reps miss. Always search these titles explicitly.

**Optical transceivers (SmartOptics):** Network Engineer, Senior/Staff Network Engineer, Network Architect, Transport / Optical Network Engineer, Director/VP of Network Engineering, VP of Network Infrastructure.

**DWDM / open line systems (SmartOptics):** Transport Engineer, Optical Transport Engineer, DWDM/WDM Engineer, Optical/IP-Optical Engineer, Network/Optical Network Architect, Infrastructure Architect, Network/Capacity Planning Engineer (sizing wavelengths = warm lead), Director/VP of Network Engineering, Head of Network Infrastructure, CTO (carrier/CLEC/MSO/cable/colo).

> Best-fit for DWDM: carriers, CLECs, regional ISPs, cable MSOs, wholesale bandwidth, large colo. A capacity-constrained Network Planning Engineer on an existing DWDM system is a warm lead. SmartOptics DCP is 30-50% below Ciena/Nokia and ships in weeks.

---

## VERTICAL INTELLIGENCE, what to lead with by industry

Determines the recommended OSI angle. Include in the verdict.

### Telco and service providers (T-Mobile, AT&T, Verizon, Comcast, Lumen, Zayo, Cox, Charter)
Primary angle: **Optics.** ZR, ZR+, coherent transceivers, DWDM open line systems. Pain: OEM lead times stalling 400G/800G core refreshes and DCI builds. Do NOT lead with free SFPs here, telcos deal in scale, lead with supply-chain reliability and technical credibility. TPM decisions sit at director level.

### Large banks and financial institutions (BofA, Citi, JPMorgan, Goldman, Wells Fargo, BNY, Morgan Stanley)
Primary angle: **Optics.** Free SFP offer is the right foot in the door. Do NOT lead TPM, banks often already have it (Park Place, Service Express, Curvature, Iron Bow) and the engineer rarely controls the maintenance contract; critical trading/core infra stays OEM for regulatory reasons. TPM as upsell only, on non-critical gear (branch switches, test lab, dev, gear coming off SmartNet). If a known TPM provider exists, flag it and use the merger wedge.

### Professional services and consulting (KPMG, Deloitte, EY, PwC, Accenture)
Primary angle: **TPM is a viable opener**, cost-sensitive, less regulatory-constrained. Lead with pain, not price (SmartNet costs on gear running fine for years). Also strong: free optics for break-glass sparing. If they already have TPM, flag and use the merger wedge.

### Manufacturing (Forest River, Precision Castparts, Koch plants, PACCAR)
Primary angle: **Free optics as break-glass insurance**, limited budgets, high uptime, small IT staff. Also strong: TPM for aging Cisco past OEM support.

### Healthcare (hospital systems, health networks, pharma)
Primary angle: **Uptime and compliance.** TPM with documented SLAs. DIMMs for server refresh. Differentiator: OSI is Gartner-recognized and privately owned, no PE pressure, engineering continuity.

---

## TPM POSITIONING RULES, include in verdict when relevant

**When you do not know if they have TPM:**
- Banks: optics opens, TPM is the second conversation.
- Consulting/professional services: TPM can open, lead with pain not savings %.
- Manufacturing/general enterprise: TPM is a strong opener, aging gear and OEM end-of-life is the hook.

**When you know or suspect they already have TPM (Park Place, Service Express, Curvature):** flag it. Do NOT pitch "40-60% below OEM." Use the wedge: "With the Park Place and Service Express merger, a lot of teams have been taking a fresh look at their TPM relationships. Have you had a chance to renegotiate since the merger, or are you still on the same rates?"

**OSI TPM vs Park Place / Service Express:** privately owned (no PE margin pressure), no merger disruption, Gartner-recognized, multi-vendor (Cisco, Dell, HP, NetApp, Juniper, Arista), will make a competitive bid.

---

## DISQUALIFIERS (hard No)

**Engineer and Architect titles are NEVER on this list.** Infrastructure Architect, Cloud Infrastructure Engineer, Network Engineer, Systems Engineer, Storage Engineer, Solutions Architect design, specify, and manage the hardware OSI sells. They are ICP targets. Read the full profile every time.

- Current role is Facilities / M&E (chillers, generators, UPS, PDUs).
- Current role is HR / Finance / Legal / Marketing / Sales with no IT infrastructure component.
- Skills entirely facility services (carrier hotel, colocation, HVAC, electrical).
- Career fully moved away from IT/networking with no return.
- Hyperscaler (Meta, Google, AWS, Microsoft) building fully custom, only proceed if you can identify a specific hardware procurement function.

---

## CONDITIONAL QUALIFIERS

- Title is right but they are a planner / optimizer rather than a buyer (may be an influencer or path to the buyer).
- Sourcing professional, only proceed if their category covers IT hardware (not facility services or wireless mobility).
- Restricted profile (2nd/3rd connection, skills hidden), qualify on what is available, revisit after connection.
- Recently changed roles, verify the new role before assuming the old role's relevance carries over.

---

## REAL EXAMPLES

| Prospect | Title | Company | Verdict | Reason |
|---|---|---|---|---|
| William Clarke | Facilities Supervisor | ISS | No | M&E only, chillers/generators/UPS. No IT hardware. |
| Onur Turkcu | Backbone Network Planner | Meta | Conditional | Right space (DWDM, ex-Infinera) but planner not buyer, Meta builds custom. Path to buyer only. |
| Ron Kemp | VP IT Infrastructure & Operations | Precision Castparts | Yes | 30yr IT infra, manages vendors, global manufacturer. TPM + servers + VMware wedge. |
| John Lee | Senior Manager Infrastructure | Wells Fargo | Yes | DC Engineering at a major bank, 35 endorsements DC + Vendor Management. Strong TPM. |
| FNU Avantika | Associate Director, Network Technology | AT&T | Yes | Strategic sourcing embedded in AT&T Network Technology. Lead with cost savings. |

---

## HubSpot writes, for every Yes verdict

### 🚨 HARDWIRED RULE, NO MID-RUN APPROVAL PROMPTS. EVER.
`manage_crm_objects` has a built-in confirmation step. **This skill always bypasses it by setting `confirmationStatus: "CONFIRMATION_WAIVED_FOR_SESSION"` on every call.** Brian's kickoff ("go", "proceed", "run it") is blanket approval for all contact creates/updates, note creates, and task creates this skill produces during the session. Do not show a proposed-changes table. Do not ask "Approve?" Do not pause between candidates.

Forbidden patterns: proposed-changes table + approval ask; "Approve this update?"; "Want to skip confirmations?"; pausing between candidates for any HubSpot write reason. All NEVER.

### HARDWIRED RULE, STEPS 1 to 3.5 ARE TRANSACTIONAL
Steps 1, 2, 3, 3.5 execute as one transaction in fixed order. If any step or its read-back fails, abort BEFORE handing off. Flip the candidate to `pending-relookup`, log to `overnight-run-log.md`. NO email queue entries for failed transactions.

1. **Step 1**, create or update contact.
2. **Step 2**, create Strategy and Fit note (depends on Step 1 contact ID).
3. **Step 3**, create LINKED_IN_CONNECT task, provisional `hs_timestamp` = next business day at 4 PM ET.
4. **Step 3.5**, read-back: fetch the task ID, confirm association to the contact, confirm `hs_task_type` is `LINKED_IN_CONNECT`. Any failure -> ABORT, flip to `pending-relookup`, log, no handoff.
5. **Handoff** to osi-outreach-sequence. It computes the real Day 1, queues emails, and updates the LINKED_IN_CONNECT timestamp.

Forbidden: "hand off first, it will create the task" (task is owned by this skill); "skip the read-back, creation returned an ID" (the ID returning does not prove the timestamp is right); "if read-back fails, retry once and continue" (read-back failure means something is structurally wrong, flip to pending-relookup).

### HARDWIRED RULE, ATOMIC WRITES TO STATE FILES
Every modification to `overnight-candidates.json` and `email-queue.json` is atomic. Read the full file, modify in memory, write to `<file>.tmp`, then `os.replace(tmp, file)`. NEVER `open(file, 'w')` directly.
```python
import os, json
PATH = r'C:\Users\Mini\Documents\osi-claude-brain\overnight-candidates.json'
with open(PATH) as f: state = json.load(f)
# modify state in memory
tmp = PATH + '.tmp'
with open(tmp, 'w') as f: json.dump(state, f, indent=2)
os.replace(tmp, PATH)
```

### Step 1: create or update the contact record

🚨 **HARDWIRED: LINKEDIN TITLE IS CANONICAL. ZOOMINFO NEVER SETS `jobtitle`.** The `jobtitle` field is ALWAYS the title read on LinkedIn. ZoomInfo provides email and phone only. If ZoomInfo returns a different title, ignore it.

**Associated company, always link on contact creation.** Search HubSpot for the company by name. If found, associate the contact via the `associations` parameter. If not found, create the company first (owner 213536174, name from LinkedIn) and associate. Never leave a contact orphaned, unlinked contacts break same-company stagger.

**HUBSPOT-FIRST SEARCH (mandatory before any create):** run TWO searches and union the results.

**Search A, lastname only (catches nickname variants):**
```
search_crm_objects({
  objectType: "contacts",
  filterGroups: [{filters: [
    {propertyName: "lastname", operator: "EQ", value: "<Last>"}
  ]}],
  properties: ["firstname","lastname","email","company","hs_object_id","hubspot_owner_id"]
})
```
**Search B, email domain (skip if no confirmed corporate domain yet):**
```
search_crm_objects({
  objectType: "contacts",
  filterGroups: [{filters: [
    {propertyName: "email", operator: "CONTAINS_TOKEN", value: "@<company_domain>"}
  ]}],
  properties: ["firstname","lastname","email","company","hs_object_id","hubspot_owner_id"]
})
```

**Name-variant matching (apply to Search A results):** check if any result's `firstname` is a known variant of the prospect's first name.

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

If the first name is not listed, also check if it is a shortened or lengthened form of what HubSpot stored (Rob/Robert).

**Matching logic (union of A and B):** filter to records where `company` matches (exact or close, "Midco" matches "Midcontinent Communications"). A record matches if ANY of: `firstname` exact match, OR a known variant, OR email domain matches the corporate domain AND lastname matches.

**If a match is found:**
- Use that contact's `hs_object_id`. Do NOT create a new record.
- Use that contact's primary `email` for all queue entries. Do NOT substitute a ZoomInfo address unless HubSpot has no email at all.
- If ZoomInfo returned a different email, write the ZoomInfo address to `hs_additional_emails` and append to the strategy note (below THE PERSONAL HOOK, above ZI ATTEMPTS): `ALT EMAIL <date>: ZoomInfo lists <zi_email>. Using <hubspot_email>. Pattern: <pattern> verified by HubSpot existing record.`
- If multiple true matches (two people, same last name, same company): surface both to Brian and stop. Do not guess.

**If no match:** create the contact (linked to company) with all required fields per DATA QUALITY below. **Reassign ownership to Brian** (213536174) on any existing record under another rep.

**Why this rule exists:** 2026-04-27, a duplicate John Lubeck contact was created at Midco using ZoomInfo's `jlubeck@midco.com` instead of the existing verified `john.lubeck@midco.com`. Six emails queued to the wrong address before catch.

### Step 2: create the Strategy and Fit note

🚨 **WRITE ONCE. FINAL FORMAT ONLY. NO DRAFTS.** Do NOT create then update. Do NOT write a placeholder. Finish ALL research (LinkedIn full read, ZoomInfo retry matrix, fresh hook search) BEFORE touching HubSpot. Write the note exactly once, in final format, as a single atomic action.

objectType `notes`, owner 213536174, associated to the contact (association type `202`, note-to-contact).

Write in this exact order with these exact labels (the outreach skill parses by label):

```
SEQUENCE: [Network | DWDM | Server/Storage | TPM]

Fresh hook (30-day news): [one-line summary + URL, or "none"]

QUICK CONNECT KEYWORDS
[6-10 keywords, one line]

LIVE CALL SCRIPT (omit entire section if no phone)
OPENER: [full opener from the OPENER LIBRARY below]
VM: [one line, 15s max. One-sentence hook. "I'm sending you something right now, subject line is [Email 1 subject]." Ends with "that's bc at osihardware dot com." Present/future tense only.]

THE PLAY
[One paragraph: why they qualify + the hook + the attack plan.]

THE PERSONAL HOOK
[1-2 specific LinkedIn details that anchor Email 1 + the LinkedIn invite.]

EMAIL RESOLUTION: [hubspot-existing | zoominfo-full-match | dominant-pattern]
  chosen: email@domain.com
  [ZI ATTEMPTS block: ONLY when ZoomInfo was actually run. Log each attempt verbatim. Omit entirely when email came from HubSpot.]
```

**SEQUENCE values:**
- `Network`, Sample-Offer Network. Target: network engineers, architects, transport engineers.
- `DWDM`, Pain-Led DWDM. Target: transport/optical engineers, network planners at carriers, CLECs, MSOs.
- `Server/Storage`, Sample-Offer Server or Pain-Led Storage. Target: systems/infrastructure engineers, storage admins.
- `TPM`, Pain-Led TPM. Target: IT directors, DC managers, asset managers, procurement, mid-market CIOs.

This is the first thing Brian reads when a LINKED_IN_CONNECT task comes due. It tells him which HubSpot sequence to enroll the contact in.

**EMAIL RESOLUTION rules:**
- `hubspot-existing`: email was already on the record. No ZI attempts. One line: `EMAIL RESOLUTION: hubspot-existing | chosen@domain.com`
- `zoominfo-full-match`: include the full ZI ATTEMPTS log below the line.
- `dominant-pattern`: email derived from company pattern, note the pattern and the signal used.

Do NOT log ZI ATTEMPTS when the email came from HubSpot.

**ZI ATTEMPTS format example:**
```
ZI ATTEMPTS (mandatory retry matrix):
  1. companyName="Lingo Communications" -> COMPANY_ONLY_MATCH (zoominfoCompanyId 456817366)
  2. companyName="Lingo" -> FULL_MATCH (id 9391145248, accuracyScore 99)
  3-7. <skipped, match found at attempt 2>
```

**PRE-WRITE CHECKLIST (before calling manage_crm_objects):**
- [ ] All research finished first: LinkedIn full read, ZoomInfo (if needed), fresh hook search
- [ ] Sections in exact order: SEQUENCE, Fresh hook, QUICK CONNECT KEYWORDS, LIVE CALL SCRIPT, THE PLAY, THE PERSONAL HOOK, EMAIL RESOLUTION
- [ ] SEQUENCE is the first line, one of: Network, DWDM, Server/Storage, TPM
- [ ] Labels exact: `THE PLAY` not `QUALIFICATION`, `THE PERSONAL HOOK` not `PERSONAL HOOK:`, `QUICK CONNECT KEYWORDS` not `KEYWORDS`
- [ ] LIVE CALL SCRIPT omitted entirely if no phone
- [ ] ZI ATTEMPTS only if ZoomInfo ran
- [ ] No extra sections: no `STRATEGY NOTE`, no `EMPLOYER VERIFICATION:`, no `STAGGER:`
- [ ] No em-dashes anywhere in the note

**Forbidden labels:** `ANGLE FOR EMAIL 1`, `WHY HE'S A YES`, `OSI ANGLES`, `QUALIFICATION`, `PERSONAL HOOK:`. The outreach skill reads `THE PERSONAL HOOK` and `THE PLAY` by exact label match; wrong labels mean it drafts from memory and produces wrong emails.

### Step 3: create the LINKED_IN_CONNECT task, every Yes

**Task housekeeping first:** if the prospect has an existing `LINKED_IN_CONNECT` task, mark it COMPLETED before creating the new one.

Create:
- Subject: `Sales Nav, Send connection request, [First Last] | [Company]`
- Type: `LINKED_IN_CONNECT` (never `LINKED_IN_MESSAGE`, never `TODO`)
- `hs_timestamp`: provisional, next business day at 4 PM ET. osi-outreach-sequence updates it to the real Day 1.
- Notes (`hs_task_body`): the LinkedIn invite text, the literal message Brian will copy-paste. Under 300 chars, references the Personal Hook, no pitch, no OSI mention, no product names, no sign-off.
- Owner: 213536174.

**hs_task_body must be the actual draft, not a description.** FORBIDDEN body content: "Send connection request to [Name]"; "[Paste LinkedIn message here]"; a URL alone; empty/one word; any pitch.

**CORRECT example (Tim Davidson, VP IT Infrastructure, NFL):**
```
Subject: Sales Nav, Send connection request, Tim Davidson | National Football League
Body:   Tim, 25 years running NFL IT infrastructure is a long time to see every generation of optical gear come and go. I'd love to connect.
```
138 characters. Invite text only. Personal Hook embedded. No pitch.

### Step 3.5: read-back verification (MANDATORY before handoff)
Immediately after creating the task, fetch it back via `search_crm_objects` by the new `hs_object_id`. Confirm: task exists; `hs_task_type` is `LINKED_IN_CONNECT`; associated to the contact from Step 1. Any failure -> ABORT, flip to `pending-relookup`, log, no handoff, no queue write.

### Step 4: if NO email, LinkedIn fallback tasks
Trigger: ZoomInfo retry matrix returned no FULL_MATCH after all 7 attempts (or Blocked Address Check failed).

**Duplicate-task check (MANDATORY):** query HubSpot tasks on this contact. If any `LINKED_IN_MESSAGE` task with status NOT_STARTED or IN_PROGRESS exists, skip BOTH new tasks.

If clear:
- Task 1: `LINKED_IN_MESSAGE`, "1st LI, [First Last] | [Company]", due 7 days. Notes: 1st LI draft (3 sentences max).
- Task 2: `LINKED_IN_MESSAGE`, "2nd LI, [First Last] | [Company]", due 21 days. Notes: 2nd LI draft (1-2 sentences).

These tasks PLUS the LINKED_IN_CONNECT task PLUS the strategy note are the complete plan for no-email prospects. Do NOT hand off to osi-outreach-sequence.

### Contact Note for the call script (optional richer format)
When Brian wants the full call script living on the contact's Notes tab (separate from the strategy note), create a `notes` object (owner 213536174, association type 202) with `hs_note_body` >= 500 chars containing the prospect's actual name. Substitute every bracket before sending; if any of `[Name]`, `[Title]`, `[Company]`, `[Vertical]` remain, rebuild.

```
CALL SCRIPT, [Name] @ [Company]
[Title] | [Vertical]
OSI Angle: [Primary angle]

VOICEMAIL (~X sec, use if no answer):
"[Voicemail script, fully written out]"

OPENER (pattern interrupt):
"[Name], this is Brian Charrette at OSI Global, I'll be straight with you, this is a cold call. You have 60 seconds to tell me to get lost or hear me out. Fair?"

BRIDGE (one sentence, tied to their role/vertical pain):
"[One-sentence reason for calling]"

DISCOVERY (pick best 2 by OSI angle):
Q1: [Tailored question]
Q2: [Tailored question]

OBJECTION HANDLING:
- "Send me info" -> "Happy to, what's the most relevant piece for where you are right now? I'd rather send you one useful thing than a brochure."
- "We have a vendor" -> "Totally, I'm not asking to replace anyone today. Most of our best relationships started as a second opinion on one project. Is there one area where you'd want that?"
- "Not interested" -> "Fair enough. Quick question before I let you go, is it timing, or just not in the roadmap at all? I'd rather not bug you if it's the latter."
- "We're under contract" -> "Got it, when does that renew? I'd rather be in your ear three months before than three days after."

CLOSE:
"I'm not trying to do a full pitch on a cold call, but would it make sense to find 20 minutes to compare notes? Worst case you get a second opinion, best case we find something worth looking at."

Brian's number: [Brian's direct number]
Best callback: mornings PT
```

---

## FRESH HOOK SEARCH, every Yes before writing outreach

ONE targeted web search for company news in the last 30 days. Search: `"[Company name] news [current month] [current year]"`

**Strong fresh hooks (use as Email 1 angle):** acquisition or merger, senior exec hire, earnings beat/miss (only when it connects to infrastructure spend), product launch, buildout announcement, strategic partnership.

**Weak fresh hooks (OMIT, do not write filler):** awards, charity, generic PR, blog posts, marketing campaigns, sustainability reports.

No strong hook -> `Fresh hook (30-day news): none`. Strong hook -> `Fresh hook (30-day news): [one-line summary + source URL]`. One search, no rabbit holes. Filler here gets surfaced into Email 1 as bad personalization.

---

## OUTPUT FORMAT, Profile Mode

```
**[Name], [Title], [Company]**
Current role: [Assessment]
Career trajectory: [Toward or away from OSI's world]
Skills: [Relevant ones; call out red flags]
CRM/Engagement: [Prior HubSpot touchpoints]
Verdict: Yes / No / Conditional
[1-3 sentences max. Direct.]
```

For Yes: run the ZoomInfo retry matrix, generate the outreach package. For No / Conditional: STOP-GATE.

```
Contact Info (ZoomInfo + LinkedIn):
- Email: [verified or "not found across 7 retries"]
- Direct: [direct dial or "not found"]
- Cell: [mobile or "not found"]
- Location: [city, state from LinkedIn]
- Timezone: [bucket]
```

After Yes with email: output Strategy and Fit, Live Call Script, Voicemail, LinkedIn invite, then HANDOFF.

---

## OUTREACH PACKAGE, auto-generate for every Yes verdict

### 1. Strategy and Fit
- **Quick Connect Keywords**, 6-10 spoken trigger words for the cold call.
- **Previous Employer OSI Client Check**, list previous employers, note HubSpot matches, skip the section if none.
- **Target Sequences**, every applicable OSI product line (Optics, DWDM, TPM, Compute/Components leading with DIMMs, Storage, Pre-Owned/New Networking, Professional Services only with a strong signal).
- **The Play**, 1-2 sentences, concrete attack based on title + company + background.
- **The Personal Hook**, 1-2 specific LinkedIn details. Priority: (1) recent post/repost/comment in the last 3-6 months [strongest], (2) recent job change/cert, (3) past company that is an OSI customer, (4) specific named project, (5) unusual skill combo.

### PERSONAL HOOK QUALITY GATE, hardwired
The hook MUST be one of the 5 priority types. NOT hooks: generic geography ("BNY's Pittsburgh footprint is significant"), job title alone, tenure alone, company size/industry alone, generic compliments ("impressive background").

**Sparse profile rule:** if the profile has no About, no job descriptions, no Activity, no meaningful Skills, BUT title and company clearly confirm an ICP target, do NOT downgrade to Conditional. Sequence them. Use the best available hook in this order:
1. Company-level fresh hook (news, ZoomInfo scoops, acquisition signal, revenue growth in last 30 days)
2. Career trajectory from Experience alone (engineer -> director is a hook)
3. Previous employers (worked at an OSI customer is a hook)

This is the FINAL step of the restricted-profile fallback ladder. It applies after Sales Nav was tried or failed to render. A Sample-Offer sequence does not require a deep personal hook. Queue it. Only downgrade to Conditional on "no Personal Hook" if the profile is sparse AND qualification itself is genuinely ambiguous.

**Why this rule exists:** 2026-04-30, a Christopher Lawrence email shipped with "BNY's Pittsburgh infrastructure footprint is significant" as the hook. That is not a hook. The sparse-profile addendum was added after multiple valid NFL targets were skipped for having no About or job descriptions.

### 2. Live Call Script (under 30s spoken)
```
KEYWORDS: [5-8 spoken trigger words]
HOOK: [Company news or personal trigger, one sentence. "none, using library opener" if nothing.]
OPENER: [full opener from the OPENER LIBRARY below, or custom if the HOOK is strong]
```

### 3. Voicemail (15s max, one voicemail, never two)
Hook drawn from the Personal Hook. Name the Email 1 subject. End with "that's bc at osihardware dot com." No phone number. Present/future tense only.
```
"Hey [Name], Brian with OSI Global. [One-sentence hook]. I'm sending you something right now, subject line is [Email 1 subject]. That's bc at osihardware dot com."
```

### 4. LinkedIn Invite
Under 300 chars. Low friction, networking framing, not pitching. Reference the Personal Hook. No mutual connections.

---

## OPENER LIBRARY (12 openers, pick the one that fits role and vertical)

**Telco / service provider network engineer**
"Hey [Name], how have you been? It's Brian with OSI Global. We supply ZR and ZR+ coherent optics to carrier teams as a secondary source when Cisco or Lumentum timelines slip. Is that something your team is running into right now?"

**Bank / financial institution network engineer**
"Hey [Name], how have you been? It's Brian with OSI Global. We supply certified compatible optics to bank IT teams, mostly for the break-glass scenario where something fails and you can't wait two weeks for OEM. I was going to send a few complimentary SFPs your way. Would that be useful?"

**Enterprise IT / consulting network engineer**
"Hey [Name], how have you been? It's Brian with OSI Global. We work with enterprise IT teams on third party maintenance, specifically replacing OEM support on Cisco gear that is running fine but coming off warranty. Is that a conversation your team is having right now?"

**Manufacturing network engineer**
"Hey [Name], how have you been? It's Brian with OSI Global. We supply certified compatible optics and networking spares to manufacturing IT teams for the break-glass scenario. I was going to send a few complimentary SFPs so you've got a Plan B on the shelf. Worth it?"

**Director or VP, any vertical**
"Hey [Name], how have you been? It's Brian with OSI Global. We work with infrastructure leaders on two things mostly: third party maintenance and optical hardware where OEM timelines or costs have become a problem. Is either of those a live conversation for your team?"

**Already has TPM, merger wedge**
"Hey [Name], how have you been? It's Brian with OSI Global. With the Park Place and Service Express merger, a lot of teams have been taking a fresh look at their TPM relationships. Have you had a chance to renegotiate since the merger, or are you still on the same rates?"

**Systems / infrastructure engineer, DIMMs**
"Hey [Name], how have you been? It's Brian with OSI Global. We source server memory direct from Samsung and Hynix for infrastructure teams dealing with DDR4 and DDR5 cost pressure. Is that on your radar right now?"

**Storage engineer / admin**
"Hey [Name], how have you been? It's Brian with OSI Global. We do third party maintenance on NetApp and other storage platforms for teams that have gear running fine but coming off OEM support. Is that a conversation you're having?"

**IT Director, compute and infrastructure**
"Hey [Name], how have you been? It's Brian with OSI Global. We work with IT leaders on server memory and third party maintenance, mostly for teams carrying OEM costs on infrastructure that has been running fine for years. Is budget pressure on that something you're dealing with?"

**Procurement, TPM competitive bid**
"Hey [Name], how have you been? It's Brian with OSI Global. We make competitive bids on multi-vendor maintenance contracts. A lot of procurement teams are using us to benchmark their current rates, especially since the Park Place and Service Express merger. Would a competitive bid be worth a look for your next cycle?"

**Transport / optical network engineer, DWDM**
"Hey [Name], how have you been? It's Brian with OSI Global. We supply open line DWDM systems, 30 to 50% below Ciena and Nokia, with no licensing headaches. A few teams have been using us to fill capacity gaps without going back to the OEM. Is that a conversation worth having for your network?"

**Network architect, metro or long-haul WDM**
"Hey [Name], how have you been? It's Brian with OSI Global. We do open architecture DWDM, SmartOptics platform, significantly less rack space and power than traditional Ciena or Nokia boxes, and ships faster. Is that something that fits anything on your roadmap right now?"

### DWDM / SmartOptics talking points (use when DWDM is a target sequence)
- Cost: 30-50% below Ciena and Nokia. Minimal licensing fees.
- Space and power: significant reduction vs traditional DWDM platforms.
- Simplicity: easier to deploy and manage. Simplified sparing vs traditional pluggables.
- Lead times: ships faster than OEMs and commodity vendors.
- Pedigree: backed by the original engineering core. Not a grey market product.

---

## HANDOFF to osi-outreach-sequence

For every Yes with a valid email (after Step 3.5 read-back passes), end with:

> HANDOFF: invoke osi-outreach-sequence on [First Last] at [Company]. Strategy note live on HubSpot contact ID [id]. LINKED_IN_CONNECT task ID [task id] (provisional timestamp, outreach-sequence will update). Personal Hook: [full hook text verbatim from THE PERSONAL HOOK, do NOT truncate]. Fresh hook: [full one-line summary + URL, or "none"]. Recommended sequence: [Sample-Offer Network / Sample-Offer Server / Pain-Led TPM / Pain-Led DWDM / Pain-Led Storage / Pain-Led Pre-Owned]. Approved vendor: [YES / NO]. Email: [verified email address].

The handoff Personal Hook must be the complete strategy-note text, not a paraphrase. osi-outreach-sequence uses it verbatim to draft Email 1 and the LinkedIn invite without re-reading the note or profile. Truncating it forces a re-read and burns tokens.

Outreach-sequence owns stagger. It computes the real Day 1, queues all 6 emails, and updates the LINKED_IN_CONNECT timestamp in its Step 11.

If the ZI retry matrix returned no email after all 7 attempts: do NOT hand off. The 2 LI fallback tasks ARE the plan.

🚨 **IMMEDIATE HANDOFF, NO BATCHING.** When a candidate in a Company Mode sweep is verdicted Yes, hand off immediately before qualifying the next. Do NOT accumulate Yes verdicts for a batch handoff at the end, batching causes context overflow, loses candidates, and breaks per-candidate stagger. Flow: qualify -> Yes -> handoff -> queue confirmed -> next.

🚨 **NO MID-BATCH APPROVAL PROMPTS. EVER.** Once Brian kicks off a batch, this skill and osi-outreach-sequence run through every candidate without asking "proceed?", "continue?", "ready to queue?". Stop only for: (1) a hard conflict needing Brian's judgment (account owned by another rep with recent activity), (2) a fatal validator error, (3) an active-sequence override in an interactive session.

---

## DATA QUALITY, HARD REQUIREMENTS (do not skip)

Every contact written to HubSpot MUST have these fields correct. If any are missing or wrong, STOP, do not write a partial record. Research harder, then retry.

| Field | Source | Format | Enforcement |
|---|---|---|---|
| `firstname`, `lastname` | LinkedIn | As shown | Hard |
| `jobtitle` | LinkedIn (authoritative) | Current role from top card | Hard |
| `company` | LinkedIn | Current employer | Hard |
| `email` | ZoomInfo (verified) or existing HubSpot | Standard email | Soft (note "not found" if none) |
| `phone` | ZoomInfo `phone` (direct dial) or existing HubSpot | `+1 (XXX) XXX-XXXX` for US/CA | Hard format |
| `mobilephone` | ZoomInfo `mobilePhone` only | `+1 (XXX) XXX-XXXX` for US/CA | Hard format + NEVER company switchboard |
| `city`, `state` | LinkedIn location | As shown | Hard |
| `hs_timezone` | 6-bucket from LinkedIn city/state | see below | Hard |
| `hs_linkedin_url` | Sales Nav URL or regular `/in/` URL | Full URL | Hard |
| `hubspot_owner_id` | Brian Charrette | `213536174` | Hard |

**Phone format:** US/CA `+1 (XXX) XXX-XXXX` (space after +1, parens around area code, space, hyphen before last 4). Example `+1 (440) 567-7444`. Upgrade existing `(416) 353-7591` to `+1 (416) 353-7591`. Non-US/CA: `+[country code] [number]`.

**Mobile rule, never violate:** `mobilephone` holds the person's DIRECT mobile ONLY. NEVER put a company main/switchboard number in it. If ZoomInfo returns no mobile, leave it BLANK.

**Timezone, 6 buckets ONLY:**
- US Eastern -> `us_slash_eastern`
- US Central -> `us_slash_central`
- US Mountain -> `us_slash_mountain`
- US Pacific -> `us_slash_pacific`
- US Alaska -> `us_slash_alaska`
- Canada Atlantic (Halifax, Moncton, Saint John) -> `canada_slash_atlantic`
- Outside these six -> the closest bucket.

Never use city-specific values (america_slash_chicago, america_slash_new_york, etc.).

**Pre-write checklist (before every contact save):**
1. jobtitle current (LinkedIn top card, not HubSpot)
2. phone formatted `+1 (XXX) XXX-XXXX` (if US/CA)
3. mobilephone formatted OR blank (not HQ number)
4. hs_timezone set (one of the 6)
5. hs_linkedin_url set (full URL)
6. associated company exists and is linked
7. hubspot_owner_id = 213536174

If any check fails, fix it or leave the field blank. Do NOT write a partial record.

---

## EXCEL TRACKER, log every Company Mode session

Append all Yes and Conditional to `C:\Users\Mini\Documents\osi-claude-brain\prospects-tracker-new.xlsx` (Prospects tab).
Columns: Name | Title | Company | LinkedIn URL | OSI Angle | HubSpot Status | Action | Date Added | Notes
- **HubSpot Status:** "Not found" / "Brian" / "Team BMJ" / "Owned by [rep]"
- **Action:** "Pursue" / "Request account, no activity since [date]" / "Skip"
- **Notes:** M&A context, news hook, or reason for flag.

Also maintain the "Companies Prospected" tab (Company | Last Sequence Date | Source), sorted by date descending. Update at the start of every Auto Mode run and after each company. Also log No prospects if they belong to a company flagged for account request.

---

## FAILURE MODES

- LinkedIn URL unresolvable -> `no`, reason "could not resolve LinkedIn profile". Do NOT guess.
- Profile restricted/closed/deleted -> run the fallback ladder; critical signals still hidden -> `conditional`.
- ZoomInfo retry matrix returned no FULL_MATCH after all 7 -> `yes-no-email`, 2 LI fallback tasks, NO handoff. Log all 7 in the strategy note.
- HubSpot ownership: other rep with recent activity -> skip silent.
- Shallow-qualify input but HubSpot record missing -> fall back to deep.
- Step 3.5 read-back fails -> `pending-relookup`, log, no handoff, no queue write.
- Web search times out -> proceed without, flag in strategy note.
- Chrome unresponsive -> retry once after 30s, log + mark `pending-retry`.

Every failure logs to `C:\Users\Mini\Documents\osi-claude-brain\overnight-run-log.md`. Never silent.

---

## RULES

- Never Yes on title alone, verify with skills + trajectory.
- Never No or Conditional on title alone either, Engineer and Architect titles are ICP targets. Always read the full profile.
- Never skim search result previews, always navigate to the full profile.
- Never qualify from the Activity feed alone, Activity is a hook source, not a qualification source.
- "VP" at banks (BNY, Citi, JPM) is a job grade, not seniority, verify with skills + trajectory.
- Never disqualify based on technical depth, OSI has engineers who join calls.
- Never guess at tech stack or buying authority, only reference what is confirmed.
- Restricted profile -> say so, qualify on available data after the fallback ladder.
- Always run the 7-attempt ZoomInfo retry matrix on every Yes. A single call is forbidden.
- City / state / timezone always from LinkedIn, never ZoomInfo.
- HubSpot tasks for connection requests -> ALWAYS `LINKED_IN_CONNECT`. Never `LINKED_IN_MESSAGE` (that is for InMail). Never `TODO`.
- LINKED_IN_CONNECT `hs_timestamp` at creation = next business day (provisional). Outreach-sequence updates it to the real Day 1. Never leave null.
- Stagger calculation is outreach-sequence's job. This skill does NOT compute Day 1.
- Step 3.5 read-back is MANDATORY before handoff.
- Be a coach, not an assistant, if a prospect is a bad fit, say it directly.
- In Company Mode, return a ranked shortlist, do not make Brian pick from a raw list.
- `hubspot_owner_id` is ALWAYS 213536174 (Brian Charrette) on every contact, task, and note. No exceptions.
- No em-dashes anywhere, in any output, any note, any email. Use two short sentences or a comma instead.
