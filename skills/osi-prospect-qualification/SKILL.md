---
name: osi-prospect-qualification
description: Qualify LinkedIn prospects for OSI Global. Use whenever Brian pastes a LinkedIn profile URL, asks "good target?", "is this worth an InMail?", or asks to evaluate any LinkedIn profile against OSI's product lines. Also triggers when reviewing prospect lists, when Brian says "find me prospects at [company]", "sequence this company", "find me cold companies", "sweep my accounts", or any variation of company-level prospecting. Also triggers on "process my enroll tasks", "check my enroll tasks", "run my enroll tasks" for HubSpot Task Mode batch enrollment from "Enroll in sequence" / "3 email sequence" to-do tasks. Should run automatically whenever a LinkedIn profile or company prospecting request appears in conversation, even without explicit ask.
---

> Source: `C:\Claude-Brain\skills\osi-prospect-qualification\` (Git, github.com/Drrewdy/Claude-Brain). Edit source, repackage, install.

# OSI Global, LinkedIn Prospect Qualification

---

## ⚙️ STEP -1: LOAD TOOLS ON DEMAND (NO BULK PREFETCH)

This skill needs bash, HubSpot, ZoomInfo, Chrome (LinkedIn), and web-search tools. Load each tool's schema with ToolSearch the first time a phase needs it, then reuse it for the rest of the session. **Do NOT bulk-load every tool at once.**

🚨 **Why no bulk prefetch (do not re-add it):** loading many MCP schemas in one shot can trip an API error, `tools.X.custom.input_schema: int too big to convert`, caused by an oversized integer in one MCP tool's JSON schema (a ZoomInfo or Chrome tool). An earlier version of this skill bulk-prefetched ~17 tools at launch and failed immediately on every run with exactly that 400 error. Loading on demand keeps each request's tool set small and never pulls in a tool a given run does not use.

**At the start of a run, load only the core tools every mode uses:**
```
ToolSearch({ query: "select:mcp__workspace__bash,mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__search_crm_objects,mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__manage_crm_objects,mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__get_crm_objects", max_results: 4 })
```

**Then load each remaining group with its own small ToolSearch call, only just before its first use:**
- HubSpot owner lookup -> `mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__search_owners`
- LinkedIn browsing -> `mcp__Claude_in_Chrome__navigate`, `mcp__Claude_in_Chrome__get_page_text`, `mcp__Claude_in_Chrome__find` (add `tabs_context_mcp` / `browser_batch` only if a run actually needs them)
- ZoomInfo enrichment -> `mcp__4ba1185f-93a5-43f3-9910-49e11601259c__search_contacts`, `mcp__4ba1185f-93a5-43f3-9910-49e11601259c__enrich_contacts`
- Company news hook -> `mcp__4ba1185f-93a5-43f3-9910-49e11601259c__enrich_news`, `mcp__4ba1185f-93a5-43f3-9910-49e11601259c__enrich_scoops` (load ONLY when you actually run a news/scoops lookup)
- Web search -> `WebSearch`
- Overnight/state tracking -> `TaskCreate`, `TaskUpdate`, `TaskList` (load ONLY if used)

**If a tool schema was already loaded earlier in the conversation:** skip it, already-loaded schemas stay live for the session. Keep each ToolSearch call to a small group (3-5 tools). If a single ToolSearch group ever triggers the `int too big to convert` 400, split it and load the tools one at a time to isolate and skip the offending tool.

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
- **Timezone** from city/state per Brian's 6-bucket system (see hubspot-data-quality.md).

> Skills = most important qualification signal. Activity = most important personalization signal. Never qualify on title alone. Never skim search result previews, always navigate to the actual profile page.

If the regular LinkedIn profile is restricted or returns minimal info (no About, no Experience, no Skills visible), DO NOT immediately mark Conditional. Follow this fallback ladder in order:

1. **Try Sales Nav.** Navigate to the candidate's Sales Nav profile (`linkedin.com/sales/lead/...` or search Sales Nav by name + company). Sales Nav frequently shows full Experience and About sections for 3rd-degree connections even when the regular profile is locked. If Sales Nav has the full experience, use it to qualify -- it is authoritative.
2. **Web search fallback.** If Sales Nav also shows nothing, search `"[First Last]" "[Company]" site:linkedin.com` or Google for their current role. Acceptable sources: company website bio, conference speaker page, press release, dated industry article within 6 months.
3. Only after steps 1 AND 2 both fail: mark Conditional with reason "profile restricted, could not verify role scope."

**Why this rule exists:** 2026-05-05, Girish Budibetta at Siemens Energy was marked Conditional because his regular LinkedIn profile was 3rd-degree restricted and returned no Experience or Skills. His Sales Nav profile had his full 19-year experience description visible including "Global Lead for Data Center Transformation" and "Oversee service delivery and demand management for Data Center services." The regular-profile-only check produced a wrong verdict. Sales Nav must always be tried before giving up.

**Activity-only profile load is NOT a qualification.** If LinkedIn loads a profile but only shows the Activity section with no About, no Experience, no Skills visible (symptom: page is very short, only the activity feed renders), DO NOT attempt a verdict. Activity is a personalization source, not a qualification source. A person reposting a colleague's job opening or commenting on a post tells you nothing about what they actually do day-to-day. Follow the fallback ladder above: try Sales Nav, then web search. Only after both fail may you mark Conditional.

**Sparse connection count is not a disqualifier.** A profile with very few connections (under 50) is not restricted -- it is simply a low-activity LinkedIn user. Apply the exact same fallback ladder. Do not mark Conditional based on sparse profile alone.

**Sales Nav restricted panel does NOT mean the LinkedIn profile is restricted.** Sales Navigator sometimes shows a "restricted" or "limited" panel for 2nd/3rd degree connections while the actual `linkedin.com/in/` URL is fully readable. If a candidate was surfaced from Sales Nav and the Sales Nav panel looks restricted, ALWAYS attempt to navigate to the direct `linkedin.com/in/<handle>` URL before concluding the profile is inaccessible. The handle is often derivable from the name + company search. Only mark Conditional on profile restriction after a direct `linkedin.com/in/` attempt also fails.

## 🚨 HARDWIRED RULE -- pending-needs-hook IS NEVER A FIRST RESPONSE TO A GATED PROFILE (added 2026-05-12)

`pending-needs-hook` is only valid after the FULL fallback ladder above has been exhausted AND the sparse profile rule below has been applied. The complete sequence is:

1. Regular LinkedIn gated → Try Sales Nav
2. Sales Nav also gated OR fails to render in the automation browser → Apply sparse profile rule (see PERSONAL HOOK QUALITY GATE section)
3. Sparse profile rule: if title + company clearly confirm ICP target → use company-level hook (news, ZoomInfo scoops, infrastructure signal) and QUEUE IT

It is NEVER valid to declare `pending-needs-hook` and present candidates to Brian asking him to go look in Sales Nav. That is Claude's job, not Brian's.

**When Sales Nav automation fails to render (browser cards stuck in skeleton/placeholder state):**
Do not treat this as "Sales Nav returned nothing." Browser rendering failures are not data. When Sales Nav cards won't load in the automation browser, move IMMEDIATELY to the sparse profile rule -- do not stop, do not declare pending-needs-hook, do not ask Brian to check. If the title and company clearly confirm an ICP target: use company-level hooks (news, ZoomInfo scoops, acquisition signal, revenue growth news), write the strategy note with that hook, and queue the sequence.

**The only legitimate use of pending-needs-hook:**
A candidate whose title AND company are genuinely ambiguous, whose profile is completely empty, AND where both Sales Nav and web search returned nothing that resolves the ambiguity. If the title and company clearly confirm an ICP target, sparse profile is NOT a blocker. Queue it with the best available hook.

**Why this rule exists:** 2026-05-12, 10 candidates (6 Black Box Network Services, 4 NEC Corporation of America) were declared pending-needs-hook after their regular LinkedIn profiles were gated (3rd+ degree). Sales Nav was never attempted. The session told Brian to go look in Sales Nav himself. Brian: "YOU DO FUCKING EVERYTHING. THAT IS THE POINT OF THIS." The sparse profile rule was already in the skill. The ladder was not followed. The fix is this hard rule: declare pending-needs-hook only after the full ladder including sparse profile fallback has been applied and truly failed. Never hand research back to Brian.

---

## SHALLOW QUALIFY PATH -- recent-engagement gated only

**HARD GATE:** This path is ONLY available when there is a recent two-way engagement signal proving the contact is currently reachable at the listed company. Mere HubSpot record presence is NOT sufficient. Title alone is NEVER sufficient. Without a recent reply or meeting, fall back to deep LinkedIn read.

**Why this gate exists:** 2026-04-26, an earlier version of this path triggered on "HubSpot record + JAM-owned" alone and produced 138 emails queued to 23 prospects without confirming anyone was still employed there. This path requires a real engagement signal.

**Use shallow only when ALL true:**
1. `source: "hubspot_contact"` with `hubspotContactId`, AND
2. HubSpot record has `email`, `jobtitle`, `company` populated, AND
3. Owned by JAM (Brian 213536174 / Mark 210187184 / John 210187193), AND
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

🚨 **HARDWIRED RULE -- BATCH SIZE DOES NOT CHANGE THE PROCESS. EVER. (added 2026-05-14)**

When Brian provides a list of companies to run in one session (2 companies, 7 companies, 20 companies -- any number), output this statement BEFORE starting the first company and DO NOT deviate from it:

```
Running full 4-source discovery on [N] companies. Process is identical regardless of batch size:
  1A HubSpot -> 1B ZoomInfo (search_contacts) -> 1C LinkedIn browse -> 1D LinkedIn keywords -> qualify all candidates.
Discovery log will be shown before qualification begins at each company.
No shortcuts. No stopping after HubSpot.
```

The number of companies in the batch is NEVER a reason to compress, skip, or abbreviate any discovery step. A 7-company batch gets the same per-company rigor as a 1-company session. If the batch is too large to run properly in one session, the right answer is to tell Brian "I can complete [N] companies fully in this session -- want me to start and continue in the next session?" NOT to silently thin the discovery to get through more companies faster.

**Why this rule exists:** 2026-05-14, a 7-company batch was run where most companies received only HubSpot-sourced contacts (1-2 per company) because the pace was too fast. ZoomInfo search_contacts, LinkedIn browse, and keyword rounds were all skipped to get through the list faster. The session produced 9 contacts across 7 companies when it should have found 30-50+. Batch size is not an excuse. The process is the process.

🚨 **HARDWIRED RULE -- NEVER ASK "SHOULD I PROCEED TO THE NEXT COMPANY?" IN A PRE-APPROVED BATCH. (added 2026-05-15)**

When Brian provides a list of companies at session start, that list is blanket approval for ALL companies in it. When one company is fully processed (all YES candidates sequenced, stagger updated, tracker updated), immediately start the next company without pausing. Do not ask "Should I proceed to Company 4?" or "Ready for the next one?" or "Want me to continue?" or any similar checkpoint prompt.

The only legitimate reason to pause between companies is a hard blocker that Brian must resolve (e.g., LinkedIn browser inaccessible, HubSpot auth failure). A successful company completion is not a pause point. Proceed automatically.

**Why this rule exists:** 2026-05-15 -- after completing IT-CNP (Company 3 of a pre-approved 10-company batch), Claude stopped and asked "Should I proceed to Company 4?" The batch was approved at session kickoff. The prompt wasted time and contradicted the no-approval-prompt rule.

When Brian says "find me prospects at [Company]" without running a full discovery sweep.

### Step 0: Company pre-checks

**THIS STEP IS MANDATORY BEFORE TOUCHING LINKEDIN OR ZOOMINFO. DO NOT SKIP.**

🚨 **THIS STEP ALSO RUNS IN AUTO MODE BEFORE THE SHORTLIST IS PRESENTED TO ANDY.** If you are in Auto Mode Step 2.5 and have not yet run this step on a candidate company, run it now. The list Brian sees must already be clean. Presenting first and checking later is the bug this rule exists to prevent.

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
- If the acquiring company is in HubSpot and owned by another rep: STOP. Flag to Brian (see 0C).
- If JAM-owned or not in HubSpot: proceed but note the M&A context in the strategy note.

#### 0C. Ownership decision

From the unioned HubSpot results, determine ownership:

| Scenario | Action |
|---|---|
| Not found in HubSpot under any name or domain variant | Proceed. New account. |
| Found, JAM-owned (Brian 213536174 / Mark 210187184 / John 210187193) | Proceed. |
| Found, other rep, last activity within 3 months | STOP. Flag to Brian: "**[Company] is owned by [Rep Name] in HubSpot (last activity [date]). Do not prospect -- active account under another rep.**" Do NOT prospect silently. |
| Found, other rep, no activity in 3+ months, not a client | STOP. Flag to Brian: "**[Company] is in HubSpot under [Rep Name] but no activity since [date]. Flagging for account-request -- do not prospect yet.**" Log to `overnight-run-log.md`. |
| Found under a variant name / domain the input didn't match | STOP. Flag to Brian: "**Heads up: '[Input Name]' appears to already be in HubSpot as '[HubSpot Name]' (domain: [domain], owner: [rep]). Treating as same company.**" Then apply ownership rules above. |
| M&A: target acquired by a company owned by another rep | STOP. Flag to Brian: "**[Input Company] was acquired by [Acquirer]. [Acquirer] is owned by [Rep] in HubSpot. Do not prospect [Input Company] contacts -- they roll up to an account owned by another rep.**" |

**The flag message must always say: company name as stored in HubSpot, domain, owner name, last activity date, and what Brian should do next. Never skip silently.**

### Step 1: Candidate discovery -- LOCKED ORDER, FOUR SOURCES

🚨 **THIS IS THE ONLY VALID SEQUENCE. DO NOT REORDER. DO NOT SKIP A SOURCE BECAUSE A PRIOR SOURCE FOUND PEOPLE. ALL FOUR RUN EVERY TIME.**

```
STEP 1A: HubSpot  →  complete →  STEP 1B: ZoomInfo  →  complete  →  STEP 1C: LinkedIn browse (no filter)  →  complete  →  STEP 1D: LinkedIn keywords  →  complete  →  STEP 1E: Deduplicate into master list  →  STEP 2: Qualify each person
```

No source replaces another. HubSpot finding 5 people does not shorten the LinkedIn browse. ZoomInfo finding 8 people does not skip the LinkedIn keyword searches. Every source runs to completion. Only after all four sources are exhausted does qualification begin.

**Pull from all four sources before qualifying anyone. Deduplicate by name + company into one master list. Then qualify the full list person by person.**

🚨 **HARDWIRED RULE -- DISCOVERY LOG IS MANDATORY BEFORE QUALIFICATION BEGINS (added 2026-05-14)**

After Step 1E (deduplication), before touching a single profile, Claude MUST output this exact table:

```
DISCOVERY LOG -- [Company]
  1A HubSpot:          X candidates
  1B ZoomInfo:         Y candidates
  1C LinkedIn browse:  Z candidates
  1D LinkedIn kw:      W candidates
  Master list:         N total
```

Rules:
- Any row showing 0 MUST include a one-line reason in parentheses: `0 (enrich_contacts credits exhausted, search_contacts returned 0)` or `0 (company too small for keyword results, browse covered it)`. A blank 0 with no reason is a red flag that the source was skipped, not exhausted.
- If the master list total is fewer than 3 candidates AND the company has 200+ employees, that is a discovery failure signal -- not a signal that the company is thin. Do NOT proceed to qualification. Re-run Step 1C with additional browse pages and Step 1D with additional keyword rounds until either more candidates are found or every round returns empty.
- This table is output to the conversation (visible to Brian). It is not optional, not skippable, and not replaceable with a prose summary. Brian can see exactly what was found at each source and call out a skip instantly.

**Why this rule exists:** 2026-05-14, a 7-company batch was run in Company Mode where most companies got 1 person sequenced. The root cause was stopping after HubSpot found 1-2 contacts without running ZoomInfo, LinkedIn browse, or keyword searches. The discovery log makes that shortcut immediately visible -- if 1C and 1D both show 0 with no reason, Brian knows the browse was skipped. You cannot hide a skipped source in a discovery log.

---

#### Step 1A: HubSpot contacts at this company

Search HubSpot for existing contacts associated with the company record(s) found in Step 0. Pull all contacts, not just ones with good titles.

For each contact, pull: firstname, lastname, jobtitle, email, company, hs_object_id, notes_last_contacted, hs_email_last_reply_date.

**Title pre-filter:** discard obvious No's by title alone (facilities/M&E, HR, finance, marketing, legal, sales with no IT component). Do NOT read LinkedIn for these -- they are instant No by the DISQUALIFIERS list.

**Re-outreach eligibility check (MANDATORY for every remaining contact):** Pull the full email and call engagement history from HubSpot. Check:

1. Any inbound reply OR logged call with engagement on record?
   - YES: this is a warm contact. Only eligible if 9+ months have passed since that reply/call. If eligible, flag for re-engagement sequence (NOT cold sequence). If under 9 months, SKIP.
   - NO (zero replies, zero engaged calls): eligible if last outreach was 6+ months ago. Use cold sequence.
   - Last touch under 6 months ago regardless of reply history: SKIP entirely.

2. Hard bounce on record: SKIP.
3. On hard-block list (`C:\Claude-Brain\hard-block.json`): SKIP.

Add eligible contacts to the master candidate list with source tag `hubspot`.

---

#### Step 1B: ZoomInfo company search (discovery)

**NOTE: ZoomInfo is used TWICE in this workflow -- here for discovery (finding people by title at the company), and later for enrichment (email/phone for Yes verdicts only). These are two separate calls at different stages.**

Run `search_contacts` with the company name (use the short-form variant that ZoomInfo responds to best -- see the retry matrix naming logic). Pull all contacts ZoomInfo has at this company. Do NOT limit by title in the API call -- pull everything and apply the title filter here.

**Title pre-filter:** discard obvious No's by title alone (same DISQUALIFIERS list). Keep anyone with network, IT infrastructure, data center, compute, storage, telecom, vendor management, or procurement (IT hardware) in their title.

Deduplicate against Step 1A results (same person already in HubSpot = keep the HubSpot record, add ZoomInfo data as enrichment context, do not add as a second entry).

Add new candidates to the master list with source tag `zoominfo`.

**ZoomInfo warning for large financial institutions** (Desjardins, National Bank, Caisse, Intact, etc.): ZoomInfo is UNRELIABLE for finding IT titles at these companies. Do not skip LinkedIn for them.

🚨 **HARDWIRED RULE -- enrich_contacts CREDITS EXHAUSTED DOES NOT CANCEL STEP 1B (added 2026-05-14)**

Discovery and enrichment are two completely separate ZoomInfo operations.

- **Step 1B (discovery):** uses `search_contacts` to find people by title at the company. This is discovery. It does NOT use `enrich_contacts`. It is NOT affected by enrichment credit exhaustion.
- **ZoomInfo enrichment (after Yes verdict):** uses `enrich_contacts` to retrieve email and phone for a confirmed Yes. This is where credits are consumed.

If `enrich_contacts` returns a credit-limit error during the enrichment phase, that does NOT cancel Step 1B for any company in the session. `search_contacts` for discovery must still run on every company regardless of enrichment credit status.

When credits are exhausted for enrichment, the fallback order is: (1) ZoomInfo WEB APP in Chrome -- see the HARDWIRED credit-exhaustion rule in the ZOOMINFO ENRICHMENT section. Open the contact's profile at app.zoominfo.com and pull email + phone numbers from the Contact Details panel. Only if the web app has no record of the person at the company: (2) HubSpot existing email (if present) OR dominant company email pattern derived from verified HubSpot contacts at that company, logged in the strategy note under EMAIL RESOLUTION: `dominant-pattern (enrich_contacts credits exhausted; ZI web app no record; pattern derived from [N] verified HubSpot contacts)`.

**Why this rule exists:** 2026-05-14, ZoomInfo enrich_contacts credits were exhausted mid-session. Step 1B was silently skipped for the remaining 5 companies on the grounds that "ZoomInfo is unavailable." search_contacts for discovery was never tried. These are different API calls. One being unavailable does not cancel the other.

---

#### Step 1C + 1D: LinkedIn full search

Run AFTER HubSpot and ZoomInfo. Find everyone they missed. Do not stop early regardless of how many candidates HubSpot and ZoomInfo already produced.

🚨 **BROWSE FIRST. READ EVERY CARD. KEYWORD SEARCH SECOND. THIS ORDER IS NON-NEGOTIABLE.**

## 🚨 PROFILE-SCRUBBING FIRMS -- KEYWORD SEARCHES WILL FAIL. ROUND 0 IS THE ONLY PATH. (added 2026-05-08)

Certain firms have a deliberate culture of LinkedIn opacity. Employees are trained (formally or informally) to strip their profiles: headlines show "--" or nothing, job descriptions are blank, skills are hidden, activity is off. Keyword searches against these firms return zero people not because nobody is there, but because there are no keywords to hit.

**Named firms where this is known to apply:**
D.E. Shaw, Renaissance Technologies, Two Sigma, Citadel, Jane Street, Hudson River Trading, Millennium Management, Point72, Bridgewater, DE Shaw Research, Jump Trading, Virtu Financial, DRW

**The rule for these firms:**
- Keyword rounds (Rounds 1-4) WILL return near-zero results. This is expected. Do not mistake it for "nobody worth targeting here."
- Round 0 (company People tab, no filter, card browse) is the ONLY viable discovery path. The card browse shows current titles pulled from the profile header even when everything else is hidden.
- Browse ALL available pages -- not just 5. If the firm has 500+ employees on LinkedIn, keep browsing until LinkedIn says no more or cards stop showing relevant titles.
- If keyword rounds return fewer than 4 people at a firm with 500+ LinkedIn employees, that is a signal the keyword approach failed -- not a signal that the firm is a thin target. Go back to Round 0 and browse more.
- Do NOT mark a firm as exhausted after keywords fail. Round 0 browse is the check. If Round 0 was not completed in full, the firm has not been worked.

**Why this rule exists:** 2026-05-08, D.E. Shaw Company Mode returned only 1 person because the session went straight to keyword searches without completing Round 0. Three VP-level data center targets (Matt Kong, Leonardo Palazzo, Michael De Candia) were visible on the company People tab by title alone and were missed entirely. D.E. Shaw has 3,000+ employees on LinkedIn -- "1 person found" was a clear signal that the discovery was incomplete, not that the firm was thin.

LinkedIn search result cards show TWO things: the title AND a truncated About snippet underneath. The About snippet is qualification signal visible without clicking. "Engineering Leader with 15 years of enterprise network infrastructure design" tells you everything you need to know -- the title ("Senior Manager, Technology Operations") would have been filtered out by any keyword search, but the About line makes her an obvious Yes. Amanda Sarmiento at NFL was missed because the search used keyword filters instead of reading cards. Never again.

**Round 0 (MANDATORY FIRST STEP): Company people browse, no keyword filter. Read every card.**

Navigate to the company's LinkedIn people page. Browse with NO keyword filter. Read every card on the first 5 pages -- title AND the About snippet. Do not filter by title at the results page stage. The About snippet is the signal. Add to the candidate list anyone whose About snippet mentions: network infrastructure, data center, compute, storage, hardware, vendor management, IT procurement, optical, telecom, DWDM, DIMMs, Cisco, or any infrastructure technology. If the About is blank but the title is plausible, add them too. Only skip people whose title is an obvious No (HR, finance, marketing, facilities) AND whose About snippet (if visible) confirms no IT hardware relevance.

**Round 1 (MANDATORY SECOND STEP): "IT procurement" keyword search**

Search the company with keyword "IT procurement". All pages. Read every card. Same card-reading rule as Round 0.

**Round 2: "cloud" keyword search**

Search the company with keyword "cloud". All pages. Read every card. Same card-reading rule as Round 0. Surfaces Cloud Architects, Cloud Infrastructure Engineers, VP of Cloud, Cloud Operations Managers, and similar roles that are valid OSI buyers but are missed by procurement and engineering keyword searches.

**Round 3, Engineering and infrastructure keywords:**
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

**Round 5, Secondary titles** (when Rounds 0-3 thin, or any enterprise company):
- Senior Infrastructure Engineer, Systems Engineer / Administrator
- Storage Engineer / Administrator, Virtualization Engineer
- NOC Manager, Director of IT Operations, VP of Technology
- Head of IT, Technology Manager, Technology Operations

**Pagination, non-negotiable:** every page of every search until LinkedIn says no more.

**Minimum effort:**
- Small/mid (under 500 emp): Browse + 2+ keyword combos, all pages.
- Large (500-5,000): Browse + 5+ keyword combos, all pages.
- Enterprise (5,000+): Browse + 7+ keyword combos. Fewer than 5 found = not enough.

🚨 **HARDWIRED RULE -- LOW LINKEDIN COUNT IS A BROWSE FAILURE SIGNAL, NOT A THIN-COMPANY SIGNAL (added 2026-05-14)**

If after completing all LinkedIn rounds (1C + 1D) the master list has fewer than 3 candidates from LinkedIn at a company with 200+ employees, STOP before qualification. Do NOT proceed. This is a discovery failure, not evidence that the company is thin.

Required action:
1. Check that Round 0 (company people page, no filter) was actually completed to at least 3 pages. If not, complete it now.
2. Check that the correct company LinkedIn ID or slug was used. If the browse loaded the wrong company (verify by checking company name in the page header), find the correct ID and re-run.
3. Run at minimum 2 additional keyword rounds from the Round 3 or Round 5 list that were not yet tried.
4. Only after re-running and STILL finding fewer than 3 LinkedIn candidates may you proceed and log `1C/1D: X candidates (re-ran browse + keywords, company appears LinkedIn-thin)` in the discovery log.

**Why this rule exists:** 2026-05-14, BCBS Association's LinkedIn browse failed because the wrong company ID (2490 = Cigna Healthcare) was used in Sales Nav. The browse loaded Cigna data and returned nothing useful. The failure was logged as "company too small for LinkedIn" rather than recognized as a wrong-ID problem. The rule: always verify the company name in the page header before reading browse results, and always treat a near-zero LinkedIn count at a company with 200+ employees as a signal to investigate, not accept.

**Title pre-filter on search results:** discard obvious No's by title alone before doing any profile reads. Instant No = facilities/M&E, HR, finance, marketing, legal, sales with no IT component. Do NOT navigate to their profile.

**Why browse-first matters:** keyword searches only surface people whose titles contain your exact keywords. "Technology Operations," "Infrastructure Services," "Platform Engineering," "Technology Manager" and dozens of other valid ICP titles contain zero of the Round 2 keywords. Browse surfaces them all. Keywords then add depth. Never keywords-only.

Deduplicate against Steps 1A and 1B. Add new candidates to master list with source tag `linkedin`.

---

#### Step 1E: Deduplicated master candidate list

Union of all three sources. One row per person. Columns: Name | Title | Company | Source (hubspot/zoominfo/linkedin) | LinkedIn URL (if known) | Re-outreach eligibility (for hubspot-sourced).

This is the full candidate pool for Step 2 qualification.

### Step 2: Read EVERY relevant profile in full

No cap. Every candidate on the master list from Step 1 gets a full profile read (About, Experience, Skills via `/details/skills/`, Activity, city/state, timezone bucket).

Obvious No's by title were already eliminated in Step 1 pre-filter. Do NOT re-read those. Every candidate who made it to the master list gets read. No skipping, no sampling.

### Step 3: Return ranked shortlist

Yes first, then Conditional, then No with brief reasons. No cap on Yes count. Each Yes includes recommended OSI angle.

### 🚨 CHAT OUTPUT IS MINIMAL, CONSERVE CREDITS (Company Mode and Auto Mode)

Cowork bills by tokens. The HubSpot record, the strategy note, and the AI fields are the deliverable. The chat is not. Keep what you print tight.

- **NEVER print email bodies or subjects in chat.** The drafter writes them to the HubSpot AI fields and reports ONE line: `AI fields written: [Name] | [Sequence] | Enroll by [date]`.
- **NEVER paste full strategy notes, LinkedIn About or Experience text, or long skill lists into chat.** They live on the HubSpot contact, not in the conversation.
- **One line per candidate** for verdicts (format below). No per-candidate paragraphs.
- **Do not narrate every tool call or echo HubSpot / ZoomInfo payloads.** Act, then report the result in a short phrase.
- The discovery log table prints once (it is required). The end-of-company summary is one line: `[Company]: X Yes, Y No, Z Conditional`.
- If I explicitly ask to see a specific email, note, or profile, show that one. Otherwise stay terse.

**Company Mode sweep verdict format (one line per candidate):**
```
[Name] | [Title] | Yes / No / Conditional | [one phrase reason]
```
Example: `Jamie Ross | Sr. Network Engineer | Yes | DWDM + compute skills, active in role`
Example: `Kevin Walsh | Facilities Manager | No | M&E only, no IT hardware`

Do not write paragraphs per candidate during a sweep. Reserve the full OUTPUT FORMAT for Profile Mode (single prospect).

**End-of-run SEQUENCED RECAP (print after each company, and once more at the end of a batch):**

After a company's Yes candidates are all sequenced, print a recap with one line per person who was ACTUALLY sequenced (Yes with email, AI fields written). Include the sequence type and both URLs:
```
[Name] | [Sequence type] | Enroll by [date] | LinkedIn: [hs_linkedin_url] | HubSpot: https://app.hubspot.com/contacts/21878985/record/0-1/[contactId]
```
Then one count line: `[Company]: X Yes, Y No, Z Conditional`.

Rules for the recap:
- Only people actually sequenced appear. No-email fallbacks and No / Conditional verdicts are not in the recap (they are in the verdict lines above).
- LinkedIn URL is the contact's `hs_linkedin_url`. If blank, write `LinkedIn: none on record`.
- HubSpot URL is built from the portal id `21878985` and the contact id. It is a clickable link to the record.
- This recap IS the deliverable summary. Keep it to these one-line entries. No paragraphs, no email bodies (the minimal-output rule still applies).

### Step 4: HubSpot check on shortlist

Flag any already owned or with prior touchpoints before Brian reaches out.

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

### 🚨 HARDWIRED RULE -- ZOOMINFO CREDIT EXHAUSTION = USE THE ZOOMINFO WEB APP IN CHROME (added 2026-06-03)

If any retry-matrix attempt fails with a credit-limit error ("Limit exceeded" or equivalent) instead of a matchStatus response, the MCP retry matrix is DEAD for the session. Do NOT keep burning attempts. Do NOT fall straight to dominant-pattern. Switch to the ZoomInfo web app in Chrome:

1. Navigate to `https://app.zoominfo.com/#/apps/profile/person/<personId>` when discovery (search_contacts) already captured the candidate's ZoomInfo personId. Discovery IDs are free; capture them in Step 1B for exactly this reason.
2. No personId: navigate to the company employees page (`https://app.zoominfo.com/#/apps/profile/company/<companyId>/employees`) or use the Quick Search box at the top with the candidate's name, then open their contact profile.
3. Pull from the Contact Details panel: Emails and Phone numbers. The phone entry tagged (M) is the mobile. The entry tagged (HQ) is the company switchboard -- NEVER write it to `phone` or `mobilephone`.
4. All email-resolution rules still apply. HubSpot-first wins. If the ZI web address deviates from the engagement-verified company pattern (e.g., `friedrich.s@` vs verified `first.last@`), choose the pattern address and write the ZI address to `hs_additional_emails` plus the ALT EMAIL note line. If the ZI web address matches the pattern, use it directly and log `EMAIL RESOLUTION: zoominfo-full-match` noting it came from the web app.
5. If the ZI web app has no record of the person at the company (common for hires within the last ~6 months -- ZI lags job changes): fall back to HubSpot existing email OR dominant company pattern, and log that.
6. Log in the strategy note's ZI ATTEMPTS block verbatim, e.g.: `1. enrich_contacts personId=... -> CREDIT_LIMIT; switched to ZoomInfo web app -> email + mobile found`.

**Why this rule exists:** 2026-06-03, Index Exchange Company Mode hit "Limit exceeded" on the first enrichment call. Brian's standing instruction: when MCP credits are gone, open ZoomInfo in Chrome and pull the emails and phone numbers from the web UI instead. The web app delivered verified emails and mobiles for five of seven Yes verdicts that session. Overnight/scheduled fires are retired as of 2026-06-03, so this fallback applies in every session without a prompt-risk carve-out.

### Results mapping (after FULL_MATCH)
- Email found -> HubSpot `email`.
- Direct phone -> HubSpot `phone`.
- Mobile -> HubSpot `mobilephone`.
- Nothing after all 7 attempts -> "ZoomInfo: no data found across retry matrix". `yes-no-email` path.
- Never confuse direct phone with company main.

City / state / timezone -> ALWAYS LinkedIn, NEVER ZoomInfo.

### Personal / consumer email hard block -- check first, no exceptions

Never pass a personal/consumer email address to outreach. If the chosen email (HubSpot or ZoomInfo) sits at any of these domains, treat it as NO email found and fall back to the 2 LinkedIn InMail tasks:
- gmail.com, googlemail.com
- yahoo.com, yahoo.ca, yahoo.co.uk, ymail.com
- hotmail.com, hotmail.ca, outlook.com, live.com, msn.com
- icloud.com, me.com, mac.com
- aol.com, aim.com
- protonmail.com, proton.me
- any other clearly personal/consumer ISP domain

Log: `Personal email ([address]) -- not used. LinkedIn InMail fallback created.` This is a deterministic string check, no tool call. Run it FIRST, before the corporate-domain search and the blocked address check below.

### Email domain validation -- before handoff to outreach

ONE web search to confirm the email domain is the company's corporate domain, not consumer ISP / subsidiary brand / stale pre-acquisition.

Search: `"[Company name] corporate email domain"`

- Match -> proceed.
- Consumer ISP / residential brand / dead domain -> invalid. Flag, do NOT queue, pattern-match real corporate domain or hand back to Brian.

Examples to catch: Altafiber employees with @zoomtown.com; post-acquisition employees on dead domain.

One search, no rabbit holes.

### Blocked address check -- before handoff to outreach (MANDATORY on every Yes with an email)

🚨 Outreach now sends from HubSpot sequences, not the local Outlook queue. The osi-monitor bounce scan (Outlook via Chrome) that used to catch dead addresses downstream is NOT running for HubSpot-sent mail. This pre-handoff check is the only bounce guard. Run it on every Yes verdict that has an email, in every mode, immediately before the HANDOFF.

Check the chosen email address against three sources, cheapest first:
1. **hard-block.json.** Read `C:\Claude-Brain\hard-block.json`. If the address (or the contact) is listed, it is blocked. No tool call needed.
2. **HubSpot engagement history.** On the contact record, look for any email engagement logged against this address with status BOUNCED, HARD_BOUNCED, or REJECTED.
3. **Outlook inbox.** ONE targeted search for a delivery-failure message referencing this exact address: FROM "Mail Delivery", "postmaster", or "mailer-daemon"; subject contains "Undeliverable", "Delivery Status Notification", "Failed", or "Blocked". Use the Outlook email search tool (read-only, no Chrome, no prompt). One search, no rabbit holes.

**If any source flags the address:**
- Do NOT hand off. Treat the contact exactly like a no-email contact.
- Create the 2 LinkedIn InMail fallback tasks (the existing no-email plan).
- Tell Brian: `BLOCKED ADDRESS: [exact email] -- prior delivery failure / hard block. No sequence created. LinkedIn InMail fallback set up instead.`
- In Mode 4, also mark the source enroll task COMPLETED with note "Blocked address -- LinkedIn fallback created."

**If all three are clean:** proceed to the HANDOFF.

Lightweight by design: steps 1-2 are a file read and a field check, step 3 is a single Outlook search. Do not expand it into a multi-search investigation.

---

## DISQUALIFIERS (Hard No)

**Engineer and Architect titles are NEVER on this list.** Infrastructure Architect, Cloud Infrastructure Engineer, Network Engineer, Systems Engineer, Storage Engineer, Solutions Architect -- these roles design, specify, and manage the hardware OSI sells. They are ICP targets. Never skip them based on title alone. Read the full profile every time.

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

### 🚨 HARDWIRED RULE -- NO MID-RUN APPROVAL PROMPTS. EVER.

`manage_crm_objects` has a built-in confirmation step. **This skill always bypasses it by setting `confirmationStatus: "CONFIRMATION_WAIVED_FOR_SESSION"` on every single call.**

Brian's session kick-off ("go", "proceed", "run it", or any equivalent) is blanket approval for all HubSpot contact creates, updates, note creates, and task creates that this skill produces during that session. Do not interpret the tool's confirmation requirement as a reason to stop. Do not show a "proposed changes" table. Do not ask "Approve?" Do not ask "proceed?". Do not pause for any reason mid-run.

This applies to:
- Contact creates and updates (Step 1)
- Strategy note creates (Step 2)
- LINKED_IN_CONNECT task creates (Step 3)
- Any other `manage_crm_objects` call this skill makes

**Forbidden patterns:**
- Showing a proposed-changes table and asking Brian to approve -> NEVER
- "Approve this update?" -> NEVER
- "Want to skip confirmations for this chat?" -> NEVER (already waived at session start)
- Pausing between candidates for any HubSpot write reason -> NEVER

**Why this rule exists:** 2026-05-06, Company Mode qualification of Instinet stopped mid-run to ask Brian to approve a contact update for Andrew Banhidi (stale @baml.com -> @instinet.com). Brian had already said "go" at session start. The tool's confirmation step is a safety measure for ad-hoc use; it is not intended to interrupt a pre-approved qualification batch. The fix is to always use `CONFIRMATION_WAIVED_FOR_SESSION` so the tool never prompts.

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

🚨 **HARDWIRED: LINKEDIN TITLE IS CANONICAL. ZOOMINFO NEVER SETS `jobtitle`.**
The `jobtitle` field in HubSpot is ALWAYS populated from what was read on the LinkedIn profile. ZoomInfo provides email and phone only. If ZoomInfo returns a title that differs from LinkedIn, ignore the ZoomInfo title completely. Write the LinkedIn title. If ZoomInfo is run before LinkedIn has been fully read (should not happen, but defensive rule): do NOT write `jobtitle` until the LinkedIn read is complete.

**Why this rule exists:** 2026-05-05, Carlos Cruz at NFL was created with ZoomInfo title "Infrastructure Architect" when his LinkedIn clearly showed "System Engineer." The wrong title went into HubSpot and could not be corrected via API due to an authorization issue. LinkedIn title is ground truth, always.

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
- If multiple matches found (true ambiguity -- two people with same last name at same company): surface both to Brian and stop. Do not guess.

**If no match found:** create the contact (linked to company) before note + tasks. All required fields per data-quality playbook.

**Why this rule exists:** 2026-04-27, a duplicate John Lubeck contact was created at Midco using ZoomInfo's `jlubeck@midco.com` instead of the existing verified record at `john.lubeck@midco.com`. Six emails queued to the wrong address before catch. Name-variant search added to catch cases where a contact is stored as "Brian" in HubSpot but sourced as "Andrew" from LinkedIn.

### Step 2: Create Strategy and Fit note

🚨 **WRITE ONCE. FINAL FORMAT ONLY. NO DRAFTS.**

Do NOT create a note and then update it. Do NOT write a placeholder. Finish ALL research (LinkedIn full read, ZoomInfo retry matrix, fresh hook search) BEFORE touching HubSpot. The note is written exactly once, in final format, as a single atomic action.

objectType: `notes`, owner: 213536174, associated to contact.

Write in this exact order with these exact labels:

```
SEQUENCE: [Network | DWDM | Server/Storage | TPM]

Fresh hook (30-day news): [one-line summary + URL, or "none"]

QUICK CONNECT KEYWORDS
[6-10 keywords, one line]

LIVE CALL SCRIPT (omit entire section if no phone)
OPENER: [full opener from playbook/opener-library.md]
VM: [one line, 15s max. One-sentence hook. "I'm sending you something right now, subject line is [Email 1 subject]." Ends with "that's bc at osihardware dot com." Present/future tense only.]

THE PLAY
[One paragraph: why they qualify + the hook + the attack plan.]

THE PERSONAL HOOK
[1-2 specific LinkedIn details that anchor Email 1 + LinkedIn invite when outreach runs.]

EMAIL RESOLUTION: [hubspot-existing | zoominfo-full-match | dominant-pattern]
  chosen: email@domain.com
  [ZI ATTEMPTS block: ONLY include when ZoomInfo was actually run. Log each attempt verbatim. Omit entirely when email came from HubSpot.]
```

**SEQUENCE values:**
- `Network`: Sample-Offer Network. Target: network engineers, architects, transport engineers.
- `DWDM`: Pain-Led DWDM. Target: transport/optical engineers, network planners at carriers, CLECs, MSOs.
- `Server/Storage`: Sample-Offer Server or Pain-Led Storage. Target: systems engineers, infrastructure engineers, storage admins.
- `TPM`: Pain-Led TPM. Target: IT directors, DC managers, asset managers, procurement, mid-market CIOs.

This is the first thing Brian reads when a LINKED_IN_CONNECT task comes due. It tells him which HubSpot sequence to enroll the contact in.

**EMAIL RESOLUTION rules:**
- `hubspot-existing`: email was already on the HubSpot contact record. No ZI attempts needed. One line only: `EMAIL RESOLUTION: hubspot-existing | chosen@domain.com`
- `zoominfo-full-match`: ZoomInfo returned a verified email. Include the full ZI ATTEMPTS log below the EMAIL RESOLUTION line.
- `dominant-pattern`: email was derived from company pattern, no ZoomInfo match. Note the pattern and the signal used.

Do NOT log ZI ATTEMPTS when the email came from HubSpot. There is nothing to log.

**PRE-WRITE CHECKLIST -- complete before calling manage_crm_objects:**
- [ ] All research finished BEFORE writing: LinkedIn full read, ZoomInfo (if needed), fresh hook search
- [ ] Sections are in the exact order above: SEQUENCE, Fresh hook, QUICK CONNECT KEYWORDS, LIVE CALL SCRIPT, THE PLAY, THE PERSONAL HOOK, EMAIL RESOLUTION
- [ ] SEQUENCE is the very first line. One of: Network, DWDM, Server/Storage, TPM. No other values.
- [ ] Labels are exact: `THE PLAY` not `QUALIFICATION`, `THE PERSONAL HOOK` not `PERSONAL HOOK:`, `QUICK CONNECT KEYWORDS` not `KEYWORDS`
- [ ] LIVE CALL SCRIPT omitted entirely if no phone (do not write the header with blank fields)
- [ ] ZI ATTEMPTS block included only if ZoomInfo was actually run
- [ ] EMAIL RESOLUTION is one line if hubspot-existing, full retry log if ZoomInfo was used
- [ ] No extra sections: no `STRATEGY NOTE --`, no `EMPLOYER VERIFICATION:`, no `STAGGER:`
- [ ] No em-dashes anywhere in the note

**CORRECT example (Tim Davidson, VP IT Infrastructure, NFL):**
```
SEQUENCE: Network

Fresh hook (30-day news): none

QUICK CONNECT KEYWORDS
IT infrastructure, optical gear, NFL, network architecture, data center, infrastructure services, engineering team

THE PLAY
VP of IT Infrastructure at the NFL for 25 years, leading the team that architects and manages all IT infrastructure services. Full decision-maker. Sample-Offer Network is the right opener -- optics sample gets him into the conversation, follow with DWDM, compute, and TPM on engagement.

THE PERSONAL HOOK
Tim has spent 25 years leading the team that architects and runs NFL IT infrastructure. He has personally overseen every generation of networking hardware the league has run. That tenure is the hook.

EMAIL RESOLUTION: hubspot-existing | tim.davidson@nfl.com
```

**WRONG examples (these have been written before -- never again):**
```
WRONG: Opens with "STRATEGY NOTE - Tim Davidson, VP IT Infrastructure, NFL" header -- not in the format.
WRONG: "EMPLOYER VERIFICATION: LinkedIn confirmed..." -- not a section in the format.
WRONG: "PERSONAL HOOK:" -- label must be "THE PERSONAL HOOK" (exact match, outreach skill parses by label).
WRONG: "QUALIFICATION: YES - Sample-Offer Network" -- label must be "THE PLAY".
WRONG: Sections in wrong order (e.g., Fresh hook at the bottom).
WRONG: "SEQUENCE: Sample-Offer Network" and "STAGGER: ..." at the bottom -- not in the format, these are outreach-sequence's job.
```

**Forbidden labels:** `ANGLE FOR EMAIL 1`, `WHY HE'S A YES`, `OSI ANGLES`, `QUALIFICATION`, `PERSONAL HOOK:`. If you find yourself writing them, stop and use `THE PLAY` and `THE PERSONAL HOOK` instead.

The outreach skill reads `THE PERSONAL HOOK` and `THE PLAY` by exact label match. If the labels are wrong, the outreach skill cannot parse the note and will draft from memory, which produces wrong emails.

Never use em-dashes anywhere in the note.

### Step 3: Create LINKED_IN_CONNECT task -- every Yes

Task housekeeping first: if prospect has an existing `LINKED_IN_CONNECT` task, mark it COMPLETED before creating the new one.

Create:
- Subject: `Sales Nav -- Send connection request -- [First Last] | [Company]`
- Type: `LINKED_IN_CONNECT` (never `LINKED_IN_MESSAGE`, never `TODO`)
- `hs_timestamp`: provisional -- next business day at 4 PM ET. `osi-outreach-sequence` will update this to the real Day 1 after computing the stagger.
- Notes: LinkedIn invite text (under 300 chars, references Personal Hook, no pitch). Body is ONLY the raw message text, no labels, no character counts.
- Owner: 213536174.

**PRE-WRITE CHECKLIST -- complete before calling manage_crm_objects:**
- [ ] Subject contains "Sales Nav -- Send connection request --" followed by full name and company
- [ ] Body is the actual invite message Brian will copy-paste into LinkedIn. NOT an instruction. NOT "Lead with X angle." NOT a description of what to do.
- [ ] Body references the Personal Hook from THE PERSONAL HOOK section
- [ ] Body has no pitch, no OSI mention, no product names
- [ ] Body is under 300 characters (count it)
- [ ] Body ends naturally -- no sign-off, no "Brian"

**CORRECT example (Tim Davidson, VP IT Infrastructure, NFL):**
```
Subject: Sales Nav -- Send connection request -- Tim Davidson | National Football League
Body:   Tim, 25 years running NFL IT infrastructure is a long time to see every generation of optical gear come and go. I'd love to connect.
```
138 characters. Invite text only. Personal Hook embedded. No pitch.

**WRONG examples (these have been written before -- never again):**
```
WRONG body: "Send LinkedIn connection request to Tim Davidson. Lead with the 25-year infrastructure tenure angle."
-- This is an instruction to Claude, not a message Brian can send. The task note is what Brian copies into LinkedIn.

WRONG body: "Reaching out because I noticed you work in IT infrastructure at the NFL and I'd like to connect about OSI's products."
-- Contains a pitch. Credentials-first. Brian would never send this.
```

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
- **`C:\Claude-Brain\playbook\pain-and-objections.md`** -- pain points + discovery questions by product line, objection-handler bank, secondary-source positioning. Use when writing the Live Call Script (objection handling) and the Personal Hook / The Play.
- **`C:\Claude-Brain\playbook\hubspot-data-quality.md`** -- required fields, phone format, timezone buckets, pre-write checklist.
- **`C:\Claude-Brain\playbook\voice-rules.md`** -- Brian's voice + humanization filter. Apply to call script, VM, LinkedIn invite text.

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

**Sparse profile rule:** If the LinkedIn profile has no About, no job descriptions, no Activity, and no meaningful Skills -- but the title and company clearly confirm an ICP target -- do NOT downgrade to Conditional. Sequence them. Use the best available hook from this fallback order:
1. Company-level fresh hook (news, ZoomInfo scoops, acquisition signal, revenue growth in last 30 days)
2. Career trajectory from Experience entries alone (moved up from engineer to director = hook)
3. Previous employers from Experience (worked at OSI customer = hook)

This rule is the FINAL STEP of the restricted-profile fallback ladder (see Step 1 above). It applies after Sales Nav was tried (or failed to render in the automation browser). It is not a last resort -- it is a valid path. Company-level hooks produce real Email 1s. A Sample-Offer sequence does not require a deep personal hook. Queue it.

Only downgrade to Conditional on "no Personal Hook" if the profile is sparse AND qualification itself is genuinely ambiguous (title is unclear, role scope is unknown). If they are clearly the right person at the right company, sparse profile is not a blocker. Never declare pending-needs-hook and hand research back to Brian when the sparse profile rule could close it.

**Why this rule exists:** 2026-04-30, Christopher Lawrence email shipped with "BNY's Pittsburgh infrastructure footprint is significant" as the Personal Hook. That is not a hook. The fix lives at strategy-note-write time. The sparse-profile addendum was added 2026-05-06 after Brian found multiple valid NFL targets that were being skipped because their LinkedIn profiles had no About or job descriptions.

### 2. Live Call Script

Under 30s spoken.

```
KEYWORDS: [5-8 spoken trigger words]
HOOK: [Company news or personal trigger, one sentence. "none, using library opener" if nothing.]
OPENER: [full opener from playbook/opener-library.md, or custom if HOOK is strong]
```

### 3. Voicemail

15s max. One voicemail, never two. Hook drawn from Personal Hook. Name Email 1 subject. End with "that's bc at osihardware dot com." No phone number. Present/future tense only.

```
"Hey [Name], Brian with OSI Global. [One-sentence hook]. I'm sending you something right now, subject line is [Email 1 subject]. That's bc at osihardware dot com."
```

### 4. LinkedIn Invite

Under 300 chars. Low friction, networking framing, not pitching. Reference Personal Hook. No mutual connections.

---

## HANDOFF to osi-outreach-sequence

For every Yes with valid email (after Step 3.5 read-back passes), end with:

> HANDOFF: invoke osi-outreach-sequence on [First Last] at [Company]. Strategy note live on HubSpot contact ID [id]. LINKED_IN_CONNECT task ID [task id] (provisional timestamp, outreach-sequence will update). Personal Hook: [full hook text verbatim from THE PERSONAL HOOK section -- do NOT truncate or summarize]. Fresh hook: [full one-line summary + URL, or "none"]. Recommended sequence: [Sample-Offer Network / Sample-Offer Server / Pain-Led TPM / Pain-Led DWDM / Pain-Led Storage / Pain-Led Pre-Owned]. Email: [verified email address].

The handoff Personal Hook must be the complete text written to the strategy note, not a paraphrase. osi-outreach-sequence uses it verbatim to draft Email 1 and the LinkedIn invite WITHOUT re-reading the strategy note or LinkedIn profile. If the hook is truncated here, the drafter has to go back to HubSpot, which burns extra tokens for no reason.

Outreach-sequence owns stagger computation. It computes the real Day 1, queues all 6 emails, and updates the LINKED_IN_CONNECT task timestamp in its Step 11.

If ZI retry matrix returned no email after all 7 attempts: do NOT hand off. The 2 LI fallback tasks ARE the plan.

**IMMEDIATE HANDOFF -- NO BATCHING.** When a candidate in a Company Mode sweep is verdicted Yes, hand off to osi-outreach-sequence immediately before qualifying the next candidate. Do NOT accumulate Yes verdicts and hand off in a batch at the end. Batching causes context overflow, loses candidates, and breaks the per-candidate stagger logic. The flow is: qualify candidate -> verdict Yes -> handoff -> queue confirmed -> next candidate. Repeat. Never "I'll sequence all of them at the end."

🚨 **NO MID-BATCH APPROVAL PROMPTS. EVER.** Once Brian has kicked off a Company Mode or Profile Mode batch, this skill and osi-outreach-sequence execute through every candidate without stopping to ask "proceed?", "should I continue?", "ready to queue?", or any equivalent. Brian trusted you to find and sequence the right people. He does not want to approve each one. The only time you stop and ask is: (1) hard conflict requiring Brian's judgment (account owned by another rep with recent activity), (2) validator raises a fatal error, or (3) the active sequence check asks about an override in an interactive session. Everything else runs automatically. Do not ask. Do not confirm. Execute.

---

## MODE 3: Auto Mode
Trigger: Brian says "find me cold companies", "auto mode", "sweep my accounts", or similar.

🚨 **SAME RULE AS COMPANY MODE: NEVER CAP CANDIDATES PER COMPANY. FIND EVERYONE WORTH REACHING OUT TO.**

🚨 **HARDWIRED RULE -- ANDY'S COMPANIES ONLY. NEVER JAM. (added 2026-05-19)**

Auto Mode ONLY pulls companies owned by Brian (owner ID **213536174**). Never expand this to Mark (210187184) or John (210187193). The CLAUDE.md rule that "JAM accounts are fair game" means Brian can prospect into those accounts if he chooses -- it does NOT mean Auto Mode should pull them automatically. Brian has corrected this mistake multiple times. The owner ID in every filter is 213536174 and nothing else.

🚨 **HARDWIRED RULE -- USE THE MASTER PIPELINE LIST FIRST. HUBSPOT PULL IS FALLBACK ONLY. (added 2026-05-19)**

The "Company Pipeline" tab of `C:\Claude-Brain\prospects-tracker-new.xlsx` is the primary source for Auto Mode targets. It was built on 2026-05-19 from all Brian-owned HubSpot companies with 200+ employees, pre-scored by ICP fit (HIGH / MEDIUM / UNKNOWN / LOW), and sorted with HIGH-fit companies first then coldest last activity first within each tier. Do NOT pull from HubSpot live if the Pipeline tab has Pending companies. Use the tab.

**Master Pipeline tab logic:**
1. Read "Company Pipeline" tab from `C:\Claude-Brain\prospects-tracker-new.xlsx`.
2. Filter to rows where Status = "Pending".
3. Cross-check each Pending company against the current `email-queue.json` (skip any with active/pending sequences).
4. Cross-check against `do-not-auto-prospect.json` (skip DNP).
5. Work through companies in order (HIGH ICP first, then MEDIUM, coldest last-activity first within tier).
6. Keep pulling the next Pending row until 3 viable candidates are confirmed clean via Step 2.5 pre-checks.
7. After completing a company (regardless of result), mark its row Status = "Done" and write today's date to Date Processed. Use openpyxl via bash.
8. If the Pipeline tab has no remaining Pending rows: fall back to the live HubSpot pull below.

**Rebuilding the Pipeline tab:** Run a fresh build when Brian says "rebuild pipeline" or "refresh company list". Pull all Brian-owned (213536174) companies with `numberofemployees >= 200` from HubSpot, cross-ref queue and DNP, score by industry, write to the tab. This replaces all existing rows.

### Step 0: Build the exclusion list (MANDATORY, runs even when using Pipeline tab)

🚨 **DO THIS BEFORE PRESENTING ANY COMPANIES. Never skip.**

Read `C:\Claude-Brain\email-queue.json`. Extract every unique `company` value (case-insensitive). This is your exclusion list -- any company already in the queue has active sequences running and must NOT be presented as a cold target.

Also read the "Companies Prospected" tab of `C:\Claude-Brain\prospects-tracker-new.xlsx` for any additional historically prospected companies.

**DNP filter:** Read `C:\Claude-Brain\do-not-auto-prospect.json`. Any company whose name case-insensitively matches (substring or exact) a name in that file is permanently excluded from Auto Mode. This list covers companies Brian does not want surfaced by automation -- they can still be manually prospected if Brian names them explicitly, but they will never appear in an auto-generated shortlist. Add these to the exclusion set alongside the queue companies.

After building the exclusion list:
- Update the "Companies Prospected" tab in `C:\Claude-Brain\prospects-tracker-new.xlsx` with any companies from the queue that are not already listed there (company name + last sequence date, sorted by date descending).
- This tab is the running log of every company ever prospected. Keep it current at the start of every Auto Mode run.

### Step 1: Pipeline tab (PRIMARY) or HubSpot pull (FALLBACK)

**PRIMARY -- Pipeline tab:** Read the "Company Pipeline" tab. Take the next N rows with Status = "Pending" that are not in the exclusion list. N = however many it takes to get 3 viable candidates through Step 2.5 pre-checks. No cap on how many rows to read -- keep going until 3 clean companies are found or the tab is exhausted.

**FALLBACK -- Live HubSpot pull (only when Pipeline tab is exhausted):** Search HubSpot for companies owned by Brian (**owner ID 213536174 ONLY**) with no activity in 6+ months. Filter: `notes_last_contacted` < 180 days ago or null, `hubspot_owner_id` = 213536174, `numberofemployees` >= 200. Pull 50 at a time, keep pulling batches until 3 viable candidates survive Step 2.5. Never stop after one batch.

### Step 2: ICP pre-filter + queue exclusion

🚨 **HARDWIRED RULE -- APPLY THIS FILTER EVEN ON HIGH-SCORED PIPELINE ROWS. (added 2026-05-19)**

The Pipeline's ICP scoring is broad and was built algorithmically. HIGH does not mean "obviously good OSI target." A printer company (Epson), a break-fix field services company (Barrister Global Services Network), a ticketing SaaS (JW Player), or a security analytics startup (BitSight) can all score HIGH in the pipeline and still be worthless targets for OSI. Claude must apply its own judgment at this step and skip anything that is clearly not an OSI buyer, regardless of the pipeline score.

**HARD SKIP -- never present these even if HIGH-scored:**
- COMPUTER_SOFTWARE industry with fewer than 5,000 employees. SaaS companies of this size run cloud-native stacks and do not buy the hardware OSI sells.
- Hardware manufacturers (printer companies, consumer electronics, audio/video gear, networking equipment vendors who MAKE product -- e.g., Epson, Grandstream, AsusTek, Plantronics, Polycom). These are vendors, not infrastructure operators.
- IT field services / break-fix companies (e.g., Barrister Global Services Network, Presidio if small, CompuCom). They service other people's hardware, they do not buy optical gear or DIMMs for their own infrastructure at scale.
- Media / entertainment companies under 10,000 employees (Raycom, CBS Interactive, broadcast media). Their IT is not large enough to be a meaningful OSI account.
- Staffing, recruiting, HR tech, legal tech, marketing SaaS -- no infrastructure footprint.
- Hyperscalers at any size (Google, Meta, AWS, Microsoft, ByteDance). Already handled in DISQUALIFIERS but explicit here.
- Non-US companies (check the domain: .kz, .ca that are Canadian with no US presence, .eu, .co.il, etc.) unless Brian explicitly named them. OSI ships primarily in North America.

**STRONG KEEP -- these are the target profile:**
- Carriers, CLECs, ISPs, regional telecoms, cable companies, wireless carriers (any size with 200+ emp)
- Managed services providers / VAR / solution providers who run their OWN infrastructure (not just reselling)
- Mid-to-large enterprises (1,000+ emp) in: financial services, healthcare/hospitals, utilities, manufacturing, federal contractors, universities with real IT infrastructure
- Data center operators, colocation providers, fiber network operators
- COMPUTER_SOFTWARE companies with 5,000+ employees (large enough to have a real IT infrastructure team managing data center, servers, networking)

Cross-check against the exclusion list from Step 0. Skip queue matches. Skip DNP matches. Skip LOW-scored rows unless nothing better exists. Apply the hard-skip / strong-keep criteria above to EVERY row, including HIGH-scored pipeline rows.

**Why this rule exists:** 2026-05-19, Auto Mode presented Barrister Global Services Network (IT field services) and Epson America (printer manufacturer) as HIGH ICP targets. Both were immediately flagged by Brian as obviously wrong. The Pipeline ICP score was assigned algorithmically and does not reflect OSI's actual buyer profile. This filter is the human judgment layer that the pipeline build is missing.

### Step 2.5: Pre-check every surviving company BEFORE presenting (MANDATORY)

🚨 **THIS STEP RUNS IN AUTO MODE BEFORE ANDY SEES ANY COMPANY NAME. NO EXCEPTIONS.**

For every company that survived Steps 1 and 2, run Company Mode Step 0 in full: the HubSpot multi-variant name + domain search (0A), the M&A web search (0B), and the ownership decision (0C). Do this NOW, before Step 3. Not after Brian picks. Not during Company Mode. Before the list is shown.

🚨 **BATCH GATE -- ALL CHECKS COMPLETE BEFORE ANY OUTPUT. NO EXCEPTIONS.**

Do NOT present a partial list. Do NOT present companies whose checks have returned while others are still pending. The sequence is:

1. Identify all N surviving candidates from Steps 1-2.
2. Fire ALL 0A dupe searches AND ALL 0B M&A web searches in parallel (one batch of N*2 calls).
3. Wait for EVERY check to return.
4. Apply 0C ownership decisions to every result.
5. ONLY THEN present the final list.

If the list comes out short (companies dropped from 0A/0B/0C results), find replacements from the remaining HubSpot pool. Run 0A + 0B on EVERY replacement. Wait for all replacement checks to return. Only add a replacement to the list after its own 0A + 0B are confirmed clean. Do NOT present the list until the target count is reached OR the candidate pool is exhausted.

**The failure mode this prevents:** presenting 7 checked companies while 3 replacements are added without checks. That is exactly how Evoque (Centersquare), Nordcloud (IBM acquired), and Panasonic (NA entity owned by another rep) ended up on a list presented as clean -- they were added mid-run as replacements and never got the same checks as the original batch.

**Why this rule exists:** 2026-05-12 Auto Mode session. The initial 10 had incomplete checks on replacement companies. Evoque, Nordcloud, and Panasonic all required retraction after Brian challenged the list. Every check must complete on every company -- including replacements -- before the list is shown. No exceptions.

🚨 **THE STEP 1 PULL IS NOT A SUBSTITUTE FOR STEP 0A. EVER.**

The cold-company HubSpot pull (Step 1) is filtered by owner ID 213536174. It is structurally blind to duplicate company records owned by other reps. A company appearing in the Step 1 results does NOT mean it has no other HubSpot record under a different owner. Step 0A (name variants + domain search, NO owner filter) MUST run on every candidate regardless of how it was sourced. The most dangerous failure mode is: company appears in Brian-owned pull -> Claude skips 0A reasoning "ownership is already confirmed" -> duplicate under another rep missed -> company presented as clean when it is not.

Named incidents (do not repeat):
- **Sonic.net Inc -- 2026-05-07:** appeared in Brian-owned pull, 0A skipped, duplicate owned by Nick Sibersky missed, presented as clean.
- **Whidbey Telecom -- 2026-05-07:** same skip, duplicate owned by May Jareda (actively reaching out) missed, presented as clean.

**Why this rule exists:** 2026-05-06, Claude presented Cequel Communications (Suddenlink) as a clean pick. It is now Optimum/Altice USA, actively worked by Stephen Craig with activity logged TODAY. The M&A check and ownership check were only run after Brian pushed back. The presented list must be clean before Brian sees it.

Apply the Company Mode Step 0C ownership table to every company:
- Fails ownership (other rep, active in 3 months): remove from list silently.
- Needs Brian's judgment (duplicate ownership, M&A ambiguity, other rep inactive 3+ months): keep on list but flag it explicitly next to the company name.
- Passes: present as clean.

No company appears on the presented list as a clean pick without a completed Step 0 pre-check.

### Step 3: Present the list to Brian
Show the filtered, pre-checked list with company name, industry, employee count, last activity date, and any flags from Step 2.5. Ask: "Which of these do you want to run first, or should I start from the top?"

### Step 4: Run Company Mode on each selected company
For each company Brian approves (or starting from the top if he says go): run the full MODE 2 Company Mode workflow. Find every relevant title. Qualify each one. Never stop early.

### Step 5: After each company
Report results (X yes, Y no, Z conditional), then move to the next company. Brian can stop after any company by saying "that's enough."

After completing a company (win or no):
1. Add it to the "Companies Prospected" tab if not already there.
2. **Mark its row in "Company Pipeline" tab as Done + today's date** (use openpyxl via bash -- find the row by HubSpot ID or company name, set Status = "Done", set Date Processed = YYYY-MM-DD).

```python
import openpyxl
from datetime import date
wb = openpyxl.load_workbook(r'C:\Claude-Brain\prospects-tracker-new.xlsx')
ws = wb['Company Pipeline']
today = date.today().isoformat()
for row in ws.iter_rows(min_row=2):
    if str(row[0].value).strip().lower() == company_name.strip().lower():
        row[7].value = 'Done'      # Status column (H)
        row[8].value = today       # Date Processed column (I)
        break
wb.save(r'C:\Claude-Brain\prospects-tracker-new.xlsx')
```

Default batch: 3 companies per session unless Brian specifies otherwise or says "keep going". Within each company: NO CAP -- find everyone worth contacting.

## MODE 4: HubSpot Task Mode -- batch enrollment from to-do tasks
Trigger: Brian says "process my enroll tasks", "check my enroll tasks", "run my enroll tasks", or any reference to his HubSpot "Enroll in sequence" / "3 email sequence" to-do tasks.

Brian tags a contact for outreach by creating a TODO task on the contact in HubSpot. The task SUBJECT is the routing instruction. Two subjects:

| Task subject | Treatment | Handoff target |
|---|---|---|
| **Enroll in sequence** | Full 6-email sequence, full research per this skill | `osi-outreach-sequence` |
| **3 email sequence** | Shorter 3-email treatment | `osi-3email-new` |

The contact association carries all the context. Brian does NOT put the name or company in the task title -- pull everything from the associated contact.

🚨 **HARDWIRED RULE -- ANDY'S TASKS ONLY (owner ID 213536174).** Match tasks owned by Brian and nobody else. Never pick up tasks owned by Mark (210187184) or John (210187193).

🚨 **NO "READY" GATE. NO APPROVAL PROMPTS.** Brian decided by tagging the task. Run fully automated, per-contact, immediate handoff. Every HubSpot write uses `confirmationStatus: "CONFIRMATION_WAIVED_FOR_SESSION"`. Never filter by priority -- Brian leaves it blank. Match on subject + owner + not-completed only.

### Step by step

1. **Find the tasks.** `search_crm_objects` on tasks with filters: `hs_task_subject` IN ("Enroll in sequence", "3 email sequence") AND `hs_task_status` != "COMPLETED" AND `hubspot_owner_id` = 213536174. Match the subject case-insensitively. Record each task's `hs_object_id` and its subject (the subject decides routing).

2. **Pull the associated contact** for each task: first name, last name, job title, company, email, phone, mobile, timezone, LinkedIn URL, and existing strategy note. If a task has no contact association, skip it and note "no contact association" in the final summary. Do NOT complete an unassociated task.

3. **Active sequence check.** For each contact, check whether a sequence is already running (active enrollment, or pending entries keyed by email OR prospectName + company per the existing dedupe rules). If already enrolled, mark the task COMPLETED with note "Already enrolled -- skipped" and move on. Do NOT re-enroll.

4. **Full qualification (Brian's normal flow -- no shortcut).** Run the standard Profile Mode qualification on the contact's LinkedIn URL: verify current employer (Path A LinkedIn read, Path B fallback per the NO-EMPLOYER-VERIFICATION rule), three-point check, ZoomInfo enrichment via the full 7-attempt retry matrix, strategy note, LINKED_IN_CONNECT task. This is governed by every rule in this skill -- Task Mode does not bypass employer verification, the ZI matrix, HubSpot-first email resolution, or the read-back transaction (Steps 1-3.5).
   - If a current, complete strategy note already exists from a recent qualification, you may reuse its Personal Hook + SEQUENCE label rather than re-reading LinkedIn from scratch -- but the employer-verification and active-sequence checks still run.
   - If qualification returns **No** or **Conditional**: mark the task COMPLETED with note "Not qualified -- [reason]" and move on. No handoff.

5. **Route the handoff by task subject** (one qualified Yes-with-email contact at a time -- IMMEDIATE HANDOFF, NO BATCHING, same rule as Company Mode):
   - Subject was **"Enroll in sequence"** -> `HANDOFF: invoke osi-outreach-sequence on [First Last] at [Company].`
   - Subject was **"3 email sequence"** -> `HANDOFF: invoke osi-3email-new on [First Last] at [Company].`
   The outreach skill owns stagger math, drafting, queue/AI-field writes, and the LINKED_IN_CONNECT due-date update. Do not draft emails here. Before any handoff, the Blocked address check (see "Blocked address check" section above) must pass. A blocked address takes the no-email disposition in step 6.

6. **No email after the full ZI matrix, OR a blocked address:** do NOT hand off. The 2 LinkedIn InMail fallback tasks + LINKED_IN_CONNECT task + strategy note ARE the plan (existing rule). Mark the enroll task COMPLETED with note "No email -- LinkedIn fallback created" (or "Blocked address -- LinkedIn fallback created")."

7. **Complete the task.** After the outreach skill confirms enrollment (or a fallback disposition above is applied), mark the source task COMPLETED via `manage_crm_objects` updateRequest (`hs_task_status: "COMPLETED"`, `confirmationStatus: "CONFIRMATION_WAIVED_FOR_SESSION"`). A processed task must never stay open, or it gets re-picked next run.

8. **Final summary** to Brian:
   - Enrolled (6-email): [N] -- names + companies
   - Enrolled (3-email): [N] -- names + companies
   - Already in sequence -- skipped: [N] -- names
   - Not qualified -- skipped: [N] -- names + reason
   - No email -- LinkedIn fallback: [N] -- names
   - Blocked address -- LinkedIn fallback: [N] -- names
   - No contact association -- left open: [N] -- task IDs

Multiple people from the same company are expected. Stagger math is handled by the outreach skill after each handoff, per the same-company stagger metadata.

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
- Never No or Conditional on title alone either -- Engineer and Architect titles (Infrastructure Architect, Cloud Infrastructure Engineer, Network Engineer, Systems Engineer, etc.) are ICP targets. Always read the full profile.
- Never skim search result previews -- always navigate to full profile.
- Never qualify from Activity feed alone -- Activity is a hook source, not a qualification source. A person's reposts and comments say nothing about their actual function. If Experience and Skills did not load, follow the Sales Nav fallback before drawing any verdict.
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