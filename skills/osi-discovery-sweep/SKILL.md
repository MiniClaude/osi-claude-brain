---
name: osi-discovery-sweep
description: >
  Per-company light search-and-capture for OSI Global overnight prospecting. Given a single company,
  runs M&A check, HubSpot ownership check, LinkedIn keyword search rounds, and captures candidate
  cards (name + headline + URL + city) into the state file with status pending. Does NOT read
  individual LinkedIn profiles in full. Does NOT qualify. Does NOT write to HubSpot. Does NOT
  draft emails. Triggers when invoked by osi-overnight-runner Discovery Mega per discovery_pending
  company.
---

> Source: `C:\Claude-Brain\skills\osi-discovery-sweep\` (Git, github.com/Drrewdy/Claude-Brain). Cowork `.claude/skills/` is a copy. Edit source, repackage, install.

# OSI Discovery Sweep

---

## 🛑 HARDWIRED RULE, RUN INLINE, NO AGENT-TOOL DISPATCHES

This skill is invoked inline from the orchestrator (Discovery Mega fire). The orchestrator reads this SKILL.md into its own context and runs per-company sweeps there. It must NOT use the `Agent` tool to dispatch subagents, every dispatch spawns a fresh sandbox that re-prompts Andy for folder mount approval. See osi-overnight-runner SKILL.md for the longer explanation. **Why:** 2026-04-29 Processing fire dispatched 8 subagents and triggered mount prompts before Andy halted the run.

---

## 🛑 HARDWIRED RULE, NO APPROVAL PROMPTS DURING SCHEDULED FIRES

If any tool call triggers an approval prompt during a scheduled-task fire, abort that step. Do not proceed. Do not retry. Mark the company `discovery_complete` with `discovery_notes` flagging the prompt-triggering call as a skill bug. Log to `Claude-Brain/overnight-run-log.md`. Move to next company.

What this means for M&A research and ownership checks during scheduled fires:
- M&A check: use ZoomInfo `enrich_scoops`, `enrich_news`, `account_research` (already-approved MCP). No `web_fetch` / `WebFetch` / `WebSearch` to arbitrary domains. ZI scoops can be stale, and that is acceptable; the alternative (a prompt overnight) is not.
- LinkedIn (Chrome MCP) keyword searches: allowed.
- HubSpot reads/writes: allowed.
- Anything that prompts: abort.

Interactive sessions (Andy at keyboard) keep the broader research surface. The rule fires only when the session is launched by a scheduled task. Detect via the dispatching context (orchestrator handoff or `<scheduled-task>` wrapper).

**Why this rule exists:** 2026-04-29, companion qualification fire (Patti Paulo, ExteNet) prompted Andy via web_fetch overnight. Discovery Sweep had a similar surface (M&A web search) that could trigger the same prompt. Inverted rule applied here too: any prompt = abort.

---

## 🛑 HARDWIRED RULES

This skill is intentionally LIGHT. The job is to get candidate names + URLs into the queue so Processing can qualify them later. Nothing more.

**This skill DOES:**
- One M&A web search per company (rebrand / acquisition / parent)
- One HubSpot ownership query per company
- LinkedIn keyword search rounds (paginate every page until LinkedIn says no more)
- Capture name + headline + URL + city + connection degree from each search result CARD
- Append candidates to `state.candidates` with status `pending`, source `linkedin_search`
- Optionally also surface existing HubSpot contacts at the company as source `hubspot_contact` (name + ID hints, NOT replacements for LinkedIn search)
- Update company status to `discovery_complete`
- Log status line to `Claude-Brain/overnight-run-log.md`

**This skill DOES NOT:**
- Click into individual LinkedIn profiles. No About reads. No Experience reads. No Skills page. No Activity feed.
- Qualify (no verdict). Verdict is `osi-prospect-qualification` Profile Mode's job, runs later in Processing.
- Run ZoomInfo. ZoomInfo is `osi-prospect-qualification`'s job.
- Write to HubSpot (no contact creation, no notes, no tasks). HubSpot writes are `osi-prospect-qualification`'s job.
- Write to `email-queue.json`. That's `osi-outreach-sequence`'s job.
- Decide which company to process next. That's the orchestrator's job (`osi-overnight-runner`).

**Why light:** because Processing is heavy (full LinkedIn read + ZoomInfo + HubSpot writes + email drafts per candidate, capped at 3 per fire). Discovery Sweep being light is what lets one Discovery Mega fire process 10 companies upfront in a single ~200-300K-token burst. Mixing heavy reads in here would force a per-company drip and break the architecture.

---

## INPUT

One company at a time, with these fields:
- `name` (required)
- `hubspot_company_id` (optional, if company exists in HubSpot)
- `domain` (optional)
- `tier` (optional, e.g. `telecom`, `enterprise_it`)
- `selection_notes` (optional, why the company is in the list)

The orchestrator (`osi-overnight-runner`) iterates over `state.companies` where `status == "discovery_pending"` and invokes this skill once per company.

---

## OUTPUT

After this skill runs on one company:
- N entries appended to `state.candidates`, each with: `id`, `firstName`, `lastName`, `company`, `linkedinUrl`, `title` (from card headline), `source` (`linkedin_search` or `hubspot_contact`), `status: "pending"`, `addedDate`. Atomic write (`.tmp` + `os.replace`).
- That company's entry in `state.companies` flipped to `status: "discovery_complete"` with `discovery_completed_at` timestamp and `discovery_notes` (one-line summary: candidates captured, M&A signal, HubSpot ownership status, anything skipped). Atomic write.
- One status line appended to `Claude-Brain/overnight-run-log.md`.

---

## HANDOFF

NONE. After Discovery Sweep finishes one company, it exits and returns control to the orchestrator (`osi-overnight-runner` Discovery Mega fire), which moves to the next discovery_pending company.

The candidates this skill files do NOT go straight into qualification. They sit in the queue with status `pending` until the next Processing Recurring fire picks them up. Processing then invokes `osi-prospect-qualification` Profile Mode on each one.

---

## RELATED SKILLS

- **`osi-overnight-runner`**, orchestrator. Calls this skill in Discovery Mega fires. Manages state file. Schedules new Discovery Mega when Refill or mid-run additions add companies.
- **`osi-prospect-qualification`**, Profile Mode. Heavy per-candidate qualifier. Picks up the candidates this skill files, runs full LinkedIn read, ZoomInfo, writes HubSpot strategy note + LINKED_IN_CONNECT task. Returns verdict.
- **`osi-outreach-sequence`**, email drafter. Invoked by qualification on Yes-with-email verdict. Drafts 6 emails, queues to `email-queue.json`.

---

## STEPS

### Step 1, M&A check (one web search)

Search `"[Company name] news [current month] [current year] acquisition merger rebrand"` or similar. ONE search.

Outcomes:
- **Subsidiary of an active OSI customer owned by another rep** (e.g. Cable One brands like Sparklight or Fidelity Communications): mark company `discovery_complete` with note `SKIPPED, subsidiary of [parent], [parent] is OSI customer of [rep name]`. Do not file any candidates. Move on.
- **Recent acquisition / rebrand**: note in `discovery_notes`. Continue with current company name + corrected company if needed.
- **Nothing notable**: continue.

### Step 2, HubSpot ownership check (JAM tree)

Query the company's `hubspot_owner_id`:
- **Not in HubSpot** → proceed.
- **Owned by Andy 196669355 / Mark 210187184 / John 210187193** (JAM tree) → proceed.
- **Other rep, last activity within 3 months** → skip silent. Mark company `discovery_complete` with note `SKIPPED, owned by [rep], active within 3 months`. No candidates.
- **Other rep, no activity 3+ months, not a client** → log for account-request, skip. Mark company `discovery_complete` with note `SKIPPED, owned by [rep], inactive 3+ months, flag for account-request`. No candidates.

This rule applies regardless of how the company entered the run. The orchestrator's Auto Mode kickoff selector pre-filters Andy-only ownership; this is a defense-in-depth check.

### Step 3, LinkedIn candidate search

Use regular `linkedin.com/in/...` (NOT Sales Nav). Run all keyword rounds:

**Round 1, English priority titles:**
- `"network engineer"` OR `"network architect"`
- `"transport engineer"` OR `"optical engineer"` OR `"DWDM"`
- `"IT infrastructure"` OR `"infrastructure architect"`
- `"data center manager"` OR `"data center engineer"`
- `"IT asset manager"` OR `"IT vendor manager"`
- `"telecom"` OR `"telecommunications engineer"`

**Round 2, French keywords (REQUIRED for Quebec accounts: Desjardins, National Bank, Caisse, Hydro-Quebec, Bell, Videotron, Cogeco):**
- `"ingénieur réseau"` OR `"architecte réseau"`
- `"architecte télécom"` OR `"ingénieur télécom"`
- `"infrastructure TI"` OR `"architecte infrastructure"`
- `"architecture détaillée"` OR `"expert télécom"`
- `"conception réseaux"` OR `"opérations télécom"`

**Round 3, Secondary titles** (when Rounds 1-2 are thin, OR for any enterprise company):
- Senior Infrastructure Engineer, Systems Engineer / Administrator
- Storage Engineer / Administrator, Virtualization Engineer
- NOC Manager, Director of IT Operations, VP of Technology
- Head of IT, Technology Manager

**Pagination, non-negotiable:** every page of every search until LinkedIn says no more results. Don't stop at page 1-2. 10 pages = read all 10.

**Minimum effort by company size:**
- Small/mid (< 500 emp): ≥ 2 keyword combinations, all pages
- Large (500-5,000): ≥ 4 combinations, all pages
- Enterprise (5,000+): ≥ 6 combinations, all pages. Expect 10+ qualified. <5 found = haven't searched enough.

**No cap on Yes count per company.** Cast a wide net. Profile Mode in Processing is the gate; Discovery Sweep is the sweep.

### Step 4, Capture cards (NO profile clicks)

For EACH search result card that looks plausibly IT/network/telecom (loose filter, when in doubt, capture and let Profile Mode decide), record from the card:
- Name (first + last)
- Headline (current title + company as shown on the card)
- Profile URL (`linkedin.com/in/[handle]`)
- Location (city + region)
- Connection degree (1st / 2nd / 3rd / 3rd+)
- Source: `linkedin_search`

Append to `state.candidates` with `status: "pending"`, `addedDate: [today's date]`. Atomic write (`.tmp` + `os.replace`).

**DO NOT click the card. DO NOT navigate to the profile. DO NOT load `/details/skills/`. DO NOT load Activity feed.** Profile reads are Profile Mode's job in Processing. This is the line.

If a card is clearly off-target (Sales role, HR, Finance, Facilities only, totally unrelated industry like retail/F&B), skip it without filing. Saves Profile Mode a wasted run later. But err on the side of capture, Profile Mode is the gate.

### Step 5, HubSpot contact surface (optional, light)

If this is an existing HubSpot company with associated contacts, optionally surface those contacts as candidates with source `hubspot_contact`:
- Pull contact list via HubSpot CRM search (associatedWith filter on the company).
- Filter to plausibly IT/network/telecom titles.
- File each as a candidate with: `firstName`, `lastName`, `company`, `hubspotContactId`, `title` (from HubSpot `jobtitle`), `source: "hubspot_contact"`, `status: "pending"`.

These are name + ID hints. They go through the SAME full Profile Mode read in Processing as `linkedin_search` candidates. **There is no shortcut path.** HubSpot is a starting point, never a stopping point.

This step is OPTIONAL. The LinkedIn keyword rounds in Step 3 are mandatory. Adding HubSpot contacts is supplementary.

### Step 6, Mark company complete

Update the company's entry in `state.companies`:
- `status: "discovery_complete"`
- `discovery_completed_at: [ISO8601 timestamp]`
- `discovery_notes: "[N] candidates captured. M&A: [signal]. HubSpot ownership: [JAM/other]. [Anything skipped]."`

Atomic write.

### Step 7, Log

Append one status line to `Claude-Brain/overnight-run-log.md`:

```
[ISO8601 timestamp] DISCOVERY SWEEP | company=[Name] | hsId=[id or none] | M&A=[signal] | LI candidates captured=[N] | HubSpot supplements=[N] | skipped reasons=[list]
```

---

## FAILURE MODES, never silent

Every failure logs to `Claude-Brain/overnight-run-log.md` with timestamp + reason:

- **LinkedIn unreachable** → log, mark company `discovery_pending` (so the next Discovery Mega retries it), exit.
- **HubSpot query fails** → proceed without HubSpot ownership check, flag in `discovery_notes`. Better to over-prospect than skip.
- **Web search times out (M&A check)** → proceed without M&A note, flag in `discovery_notes`.
- **Single search round fails (one keyword)** → log, continue with remaining keyword rounds. Don't abort the company.
- **State file write fails** → retry once, then log + exit. Do NOT proceed with a stale state.

---

## RULES

- Never click into a profile in Discovery Sweep. The whole point of this skill is to be light.
- Never qualify. No verdict here. Verdict is Profile Mode's job in Processing.
- Never write to HubSpot. The orchestrator's runner doesn't need a HubSpot record at Discovery time, that's created when Profile Mode qualifies the candidate.
- Cast a wide net. Capture more rather than fewer cards. Profile Mode will filter.
- Always paginate every keyword round to the end.
- Always log. Silent failures are forbidden.
- Mid-run, if Andy adds a company manually to `state.companies` with `status: "discovery_pending"`, the orchestrator's next Processing fire will detect it and schedule a new Discovery Mega. This skill is invoked the same way.
