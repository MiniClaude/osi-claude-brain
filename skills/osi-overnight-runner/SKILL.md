---
name: osi-overnight-runner
description: >
  Orchestrator for OSI Global overnight prospecting and sequencing. Manages two scheduled tasks
  (Discovery Mega + Processing Recurring), the state file (overnight-candidates.json), and the
  branch logic (Processing → Discovery Mega Re-Fire → Refill → Wrap-up). Invokes osi-discovery-sweep
  per company in Discovery Mega fires, invokes osi-prospect-qualification per candidate in
  Processing fires, invokes osi-outreach-sequence on Yes-with-email handoffs. Triggers on:
  "run sequences tonight", "run a sequence", "run sequences for the following companies",
  Andy pasting a LinkedIn profile, OR scheduled-task fire (9 fires/day, skips 8 AM to 2 PM ET).
---

> Source: `C:\Claude-Brain\skills\osi-overnight-runner\` (Git, github.com/Drrewdy/Claude-Brain). Cowork `.claude/skills/` is a copy. Edit source, repackage, install.

# OSI Overnight Runner (orchestrator)

---

## 🛡️ PRE-FLIGHT DRIFT CHECK (run BEFORE any branch logic)

Before invoking any sub-skill (`osi-prospect-qualification`, `osi-outreach-sequence`, `osi-discovery-sweep`), do a 10-second self-validation. This is the seatbelt that catches drift between morning auto-heal runs.

### Steps (run inline, no subagents)

1. For each sub-skill the runner invokes (`osi-prospect-qualification`, `osi-outreach-sequence`, `osi-discovery-sweep`), confirm the source file is reachable via Read tool at `C:\Claude-Brain\skills\<skill>\SKILL.md`. If any source 404s, log to `C:\Claude-Brain\overnight-run-log.md` (one line per missing source) and EXIT THE FIRE CLEANLY. Do NOT attempt to recover or fall back. Andy will see the log and fix.

2. For each sub-skill that has a runtime backing store entry (qualification and outreach do; discovery-sweep is source-only), Read the runtime SKILL.md at `C:\Users\Andy\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\local-agent-mode-sessions\skills-plugin\<plugin-id>\<session-id>\skills\<skill>\SKILL.md`. Verify the runtime is a valid stub:
   - Under 5 KB
   - Contains the literal string `RUNTIME REDIRECT STUB`
   - Contains the redirect target `C:\Claude-Brain\skills\<skill>\SKILL.md`
   - Frontmatter `name:` matches the skill

3. If a runtime is invalid (full content, missing, wrong target), regenerate the stub from source and atomic-write to runtime. Use the same template `morning-skill-sync` uses (frontmatter copied from source with em-dashes sanitized, then the standard redirect body). Log the auto-heal to `overnight-run-log.md` with prefix `PREFLIGHT-HEAL`.

4. If the runtime mount path is unavailable in this fire (skills-plugin not mounted), log `PREFLIGHT-WARN: skills-plugin mount unavailable, sub-skills will load from source via stub fallback` and continue. Do NOT call `request_cowork_directory` (would prompt).

5. Em-dash audit: scan every regenerated stub for U+2014. If present, sanitization failed; log a bug and skip the write. Stubs must be em-dash free per Andy Rule #4.

Pre-flight is a heartbeat, not a barrier. Source unreachable = abort. Runtime stub stale = heal silently and continue. Mount unavailable = continue (the morning-skill-sync next 9 AM run will catch up).

After pre-flight passes, proceed to the branch logic below.

**Why this exists:** stubs and morning auto-heal cover most drift cases, but there's a 24-hour window between auto-heal runs where a re-install or corruption could leave the runtime stale. Pre-flight closes that window. Defense in depth.

---

## 🛑 HARDWIRED RULE, NO AGENT-TOOL SUBAGENT DISPATCHES DURING SCHEDULED FIRES

The orchestrator MUST NOT use the `Agent` tool to dispatch subagents during a scheduled-task fire. Run all qualification, discovery, and outreach work INLINE in the orchestrator's own context. "Invoke osi-prospect-qualification" means: read the skill file into your own context and execute Profile Mode here. It does NOT mean dispatch an Agent subagent.

Why: every Agent dispatch spawns a fresh sandbox context. The fresh context does not inherit the parent session's approved folder mounts (Claude-Brain, skills-plugin, etc.). On startup, before any subagent tool call runs, Cowork prompts Andy to approve each mount. The "no approval prompts" rule below cannot catch this because it's enforced inside subagent tool calls, but the mount approval fires at subagent *startup*, before any subagent code executes. There is no way to suppress it from inside the subagent.

This is a single-context runner. Read the per-candidate / per-company skill, run it inline, atomic-write the state, advance to the next item. The full pipeline already fits comfortably inside one orchestrator context, every successful fire for the past week ran this way.

**Why this rule exists:** 2026-04-29, Processing Recurring fire dispatched 8 Agent subagents (one per pending candidate) instead of running Profile Mode inline. Each dispatch triggered a folder approval prompt in Andy's UI. Andy halted the run mid-fire. Zero yes-with-email fired. Previous fires (Cantor Fitzgerald 3-of-3 at 2026-04-29T00:12, Aidan Rigney at 17:15) ran inline and produced no prompts. Diff between working fires and this fire: subagent dispatches. Removed.

If a future Claude session reads "invoke osi-prospect-qualification" and reaches for the Agent tool, stop. Read the skill file with the Read tool, follow the steps in your own context, and write state directly. That is the runner.

---

## 🛑 HARDWIRED RULE, NO APPROVAL PROMPTS DURING SCHEDULED FIRES

If any tool call triggers an approval prompt of any kind during a scheduled-task fire, the orchestrator (and every subagent it dispatches) MUST abort that step immediately. Do not proceed. Do not retry. Do not "try a different way to get the same data." Log the prompt-triggering call to `Claude-Brain/overnight-run-log.md` as a skill bug, apply the local stop-gate (mark candidate Conditional, mark company skipped, etc.), continue with the next item OR exit clean.

This applies to the orchestrator AND to every subagent (Agent tool dispatch) the orchestrator spawns. Subagents inherit this rule.

Examples that trigger this rule:
- `web_fetch` or `WebFetch` to a domain that prompts (anything outside the already-approved MCP connectors).
- `mcp__Claude_in_Chrome__navigate` to a non-LinkedIn domain that prompts.
- `request_cowork_directory` on a mount Andy has not pre-approved.
- `mcp__scheduled-tasks__create_scheduled_task` if approval is required (only the kickoff tasks in Company / Auto Mode pre-approve this; mid-run scheduling that prompts is forbidden).
- ANY future tool that prompts. Do not enumerate. The trigger is the prompt itself, not the tool.

The runner is fully autonomous overnight. Any prompt is a bug in the skill that called the prompting tool. The skill must be edited to remove the path that calls it; the fire stops doing that step until the skill is fixed.

**Why this rule exists:** 2026-04-29, Patti Paulo (ExteNet Systems) qualification subagent hit a restricted LinkedIn profile and followed the qualification skill's Path B fallback, which sent a `web_fetch` to `extenet.com/about-us/leadership/patti-paulo`. That fetch prompted Andy for permission overnight. The qualification skill explicitly authorized Path B with corporate-website verification, so the subagent was right per the skill but the skill was wrong per the runner contract. Replace the long allowlist of "pre-approved connectors that subagents may use" with this single inverted rule: any prompt = abort. Every overnight-touched skill carries the same rule.

---

## 🛑 HARDWIRED RULE, BRANCH A EARLY EXIT FORBIDDEN

The only two valid exits from Branch A are: (a) 2 yes-with-email sequences fired this run, or (b) zero pending candidates remain in `state.candidates`. Nothing else.

(Cap was 3 pre-2026-05-01; lowered to 2 by Andy on 2026-05-01 for token-budget control after $25 day-one extra-usage spend on the new $300 monthly cap. The historical 3-cap text below in this skill is preserved for context but the active cap is 2.)

The following are NOT valid reasons to exit Branch A early. Do not invent them, do not act on them:
- "Token budget feels tight", the documented budget is the budget; if a fire feels expensive, that is the budget being used as designed.
- "The queue looks stale", the runner verifies each candidate; the stale ones produce No / Conditional verdicts and that's the system working, not a reason to bail.
- "Andy can manually triage" / "next fire will catch it", no, the rule says fire 3 this run.
- "First N candidates were all No / Conditional, the pattern will continue", keep going. The next pending may be the Yes.
- "The next pending is a `hubspot_contact` source and is heavier", qualify it anyway, or skip ahead per the cadence rule below, but do NOT exit.

If 2 yes-with-email haven't fired and there are pending candidates remaining, keep qualifying. Always. Why this rule exists: 2026-04-27 fire processed 3 candidates (1 No, 2 Conditional), exited at 0 of (then-)3 yes-with-email citing token budget, leaving 94 pending. Token budget was a fabricated concern not present in the rule. This block prevents that recurrence. (Cap was 3 at the time of that incident; lowered to 2 on 2026-05-01. The rule itself, "don't exit early on token-budget excuses," is independent of the cap value.)

---

## 🛑 HARDWIRED RULE, NO BULK PATH A VERIFICATION

Branch A processes pending candidates ONE AT A TIME, full pipeline each. The pipeline per candidate is: invoke `osi-prospect-qualification` Profile Mode (which handles Path A LinkedIn read, ZoomInfo, HubSpot writes, and on Yes-with-email hands off to `osi-outreach-sequence` for the 6-email queue write). Then move to candidate N+1 and run the same full pipeline. Repeat until 2 yes-with-email or pending exhausted.

The following pattern is FORBIDDEN:
- Pull N pending candidates (N > 1).
- Run a quick Path A web search (`site:linkedin.com "name" "company"`) on each one IN BATCH.
- Mark the ones that don't resolve as Conditional / No.
- Mark the ones that DO resolve as "still pending, full Chrome read deferred to next fire."
- Exit the fire with 0 yes-with-email, claiming the bulk verify was "efficient."

This pattern looks productive (9 dispositioned!) but produces zero outreach output, defers the actual work indefinitely, and burns the budget on a step that the per-candidate skill already does correctly inside its own pipeline.

The correct flow when candidate N is No or Conditional: log the verdict, atomic write the state, advance to N+1 immediately, invoke FULL qualification on N+1 (not a Path A preview, full Profile Mode). Continue until 2 yes-with-email fire or pending exhausted.

Why this rule exists: 2026-04-28 14:09Z fire took Joe Bishop as candidate #1, marked Conditional (no LinkedIn match), then pivoted to bulk Path A web-search across 24+ candidates instead of advancing to candidate #2 with full qualification. Disposed 9 as No / Conditional, left 6 verified-ICP candidates "deferred to next fire," exited with 0 yes-with-email. Self-justified the pivot in the log as "efficient." It was not efficient, it was a fabricated optimization not in the spec. The 6 verified-ICP candidates were exactly the candidates Branch A is for. Each should have been run through full qualification + outreach handoff in this fire.

If a fire needs to skip ahead in the pending pool (cadence rule says `linkedin_search` before `hubspot_contact`), that ordering is fine, but every candidate the runner picks gets the full pipeline. Never the bulk-preview shortcut.

---

## 🛑 HARDWIRED RULE, ANDY-NAMED DISCOVERY OUTRANKS PROCESSING

When Andy adds companies mid-run with `added_via` matching `andy_named_*` and a recent timestamp, those companies must reach Discovery Mega before the next Processing fire grinds further on the existing pending queue. The previous branch order (Processing → Discovery Mega Re-Fire) made this impossible: as long as `pending > 0`, Branch A won and Branch B never fired, so Andy-named companies sat in `discovery_pending` indefinitely behind a backlog of stale candidates.

The new top priority is **Branch A-prime, ANDY-NAMED DISCOVERY PRIORITY** (defined below). It fires BEFORE Branch A when:
- Any company in `state.companies` has `status: "discovery_pending"` AND
- `added_via` starts with `andy_named_` AND
- The company was added in the last 24 hours (parse the date suffix or `selection_notes` timestamp; if neither is parseable, treat as recent).

Action: schedule a fresh Discovery Mega one-time task to fire in 2-5 minutes via `mcp__scheduled-tasks__create_scheduled_task`, log the dispatch, exit. The current fire does not run Branch A. The Discovery Mega catches up the new companies, then the next regular Processing fire resumes Branch A.

Branch A still runs on every other fire (no recent Andy-named additions), and Branch B still exists for the case of mid-run additions WITHOUT recent Andy-named flag (e.g. Refill appended via Branch C and the Discovery Mega scheduling failed).

Why this rule exists: 2026-04-28, Andy named 10 companies (Gulf Stream Coach, WSP, KONE Elevators, Princeton, Cantor Fitzgerald, Bank of America, ExteNet Systems, OpenX, DRW, Iconectiv) for a 2 PM Discovery Mega. They were appended to `state.companies` as `discovery_pending`. The runner saw 36+ pending candidates, won Branch A on every fire from kickoff onward, and never reached Branch B. The 10 companies sat untouched for 4+ hours while Andy waited. This branch fixes that.

---

## 🛑 CADENCE, BRANCH A CANDIDATE ORDERING

When picking the next pending candidate in Branch A, prefer `source: "linkedin_search"` candidates over `source: "hubspot_contact"` candidates within the pending pool. Reasons:
- LinkedIn-sourced candidates carry a direct `linkedinUrl`, Path A employer verification is one navigation away.
- HubSpot supplements often carry stale 2022-era records and a higher rate of "left the company" / "stale title" outcomes that consume tokens for No / Conditional verdicts.
- Faster qualification per candidate means more shots at Yes-with-email per fire and a higher chance of hitting the 3-ceiling before pending exhaustion.

Implementation: filter pending into two buckets, take from `linkedin_search` first; once that bucket is empty, take from `hubspot_contact`. Within each bucket, take in array order.

Stale HubSpot supplements still get qualified, they're just deferred behind the fresher LinkedIn-sourced candidates. They are NEVER skipped or marked anything other than `pending` until qualification produces a verdict.

---

## 🛑 HARDWIRED RULES

This skill ONLY orchestrates. It manages scheduled tasks, the state file, and branch routing. It NEVER does the per-company or per-candidate work itself.

**This skill DOES:**
- Manage `C:\Claude-Brain\overnight-candidates.json` (the state file)
- Schedule the Discovery Mega one-time task and the two Processing Recurring tasks (weekday + weekend) at kickoff
- Read state file at every fire and route to the correct branch
- Invoke `osi-discovery-sweep` per discovery_pending company in Discovery Mega fires
- Invoke `osi-prospect-qualification` per pending candidate in Processing fires
- Forward qualification's Yes-with-email handoff to `osi-outreach-sequence`
- Run the Refill cold-company selector (HubSpot search + filters)
- Schedule fresh Discovery Mega tasks when Refill or mid-run additions add companies
- Update Excel Tab 2 (per-company summary) at run wrap-up
- Log all branch decisions and failures to `Claude-Brain/overnight-run-log.md`

**This skill DOES NOT:**
- Read individual LinkedIn profiles (delegated to `osi-prospect-qualification`).
- Run keyword search rounds at companies (delegated to `osi-discovery-sweep`).
- Draft emails (delegated to `osi-outreach-sequence`).
- Write strategy notes / LINKED_IN_CONNECT tasks (delegated to `osi-prospect-qualification`).
- Write to email-queue.json directly (delegated to `osi-outreach-sequence`).

If a Processing fire ends up doing any of the above directly instead of invoking the right skill, that is a bug. Always invoke.

---

## INPUT

- The state file `C:\Claude-Brain\overnight-candidates.json`.
- The email queue `C:\Claude-Brain\email-queue.json` (read-only at orchestration time; outreach-sequence writes to it).
- The Cowork scheduled-tasks system (Discovery Mega one-time tasks + Processing Recurring recurring task).

---

## OUTPUT

- State file updates (company status flips, candidate status flips, stagger metadata).
- Scheduled task creations (Discovery Mega for each Refill batch or mid-run addition).
- Branch decisions logged to `Claude-Brain/overnight-run-log.md`.
- Excel Tab 2 row(s) appended at wrap-up.

---

## HANDOFF (this skill is the top of the chain)

This skill INVOKES three other skills as part of orchestration. It is not handed off TO from anywhere except Andy's command at kickoff or a scheduled-task fire.

| Branch | Skill invoked | Per |
|---|---|---|
| Discovery Mega fire | `osi-discovery-sweep` | each `discovery_pending` company in state.companies |
| Processing fire (Branch A, PROCESSING) | `osi-prospect-qualification` | each `pending` candidate in state.candidates, up to 2 yes-with-email per fire |
| Processing fire (Branch A, after qualification handoff) | `osi-outreach-sequence` | each Yes-with-email handoff from qualification |

---

## RELATED SKILLS

- **`osi-discovery-sweep`**, per-company light search. Invoked by Discovery Mega.
- **`osi-prospect-qualification`**, per-candidate heavy qualifier. Invoked by Processing Branch A.
- **`osi-outreach-sequence`**, per-qualified-candidate email writer. Invoked via qualification's handoff inside Processing Branch A.

---

## ARCHITECTURE, two scheduled tasks

Overnight = exactly two tasks in Cowork's scheduled-tasks system.

### 1. Discovery Mega, one-time task

Fires once at kickoff (or at Refill, or at mid-run addition). Hits ALL companies marked `discovery_pending` in the state file in a SINGLE fire. Invokes `osi-discovery-sweep` per company. All candidates land in `state.candidates` with status `pending`. Then disables itself.

Each Refill cycle schedules a NEW Discovery Mega one-time task. Discovery Mega is the ONLY mechanism that runs Discovery Sweep on companies. There is no per-company drip.

Token budget per Discovery Mega fire: ~100-150K for 5 companies (light per-company sweep, ~20-30K each). Comfortable. (Batch was 10 pre-2026-05-01; lowered to 5 for token-budget control.)

### 2. Processing Recurring, recurring task

Two recurring crons in local ET (Cowork adds ~9 min jitter):
- **Weekday cron**, `0 0,2,4,6,14,16,18,20,22 * * 1-5`. 9 fires/day Mon-Fri at 2pm, 4pm, 6pm, 8pm, 10pm, midnight, 2am, 4am, 6am ET. **Daytime blackout 8 AM to 2 PM ET on weekdays.** Andy is at his desk during the blackout.
- **Weekend cron**, `0 */2 * * 0,6`. 12 fires/day Sat-Sun at every even hour (12am, 2am, 4am, 6am, 8am, 10am, 12pm, 2pm, 4pm, 6pm, 8pm, 10pm ET). **No blackout on weekends**, Andy isn't at the desk so the runner can grind continuously.

Combined coverage: continuous fires from Mon 2 PM ET through Fri 8 AM ET (with weekday daytime blackouts mid-week), then continuous Fri 2 PM ET through Mon 8 AM ET with no blackout (weekend cron handles Sat + Sun, weekday cron resumes Mon at 12 AM). Architecture documented 2026-04-28 at Andy's request.

Both recurring tasks use the SAME Processing Recurring prompt below. Same orchestrator, same branch logic, same skill. The cron split is purely a schedule concern.

Five branches, top-to-bottom priority:

**Branch A-prime, ANDY-NAMED DISCOVERY PRIORITY** (any company `status: "discovery_pending"` with `added_via` starting `andy_named_` AND added in the last 24 hours):
- Schedule a new Discovery Mega one-time task to fire in 2-5 minutes via `mcp__scheduled-tasks__create_scheduled_task`. Use the Discovery Mega prompt template below.
- Log the dispatch and the list of qualifying companies.
- Exit. Do NOT run Branch A this fire. The Discovery Mega catches up, the next regular fire resumes Branch A.
- This branch outranks Branch A so that Andy's mid-run named companies cannot get blocked behind a long pending queue.

**Branch A, PROCESSING** (any pending candidates):
- Take the first pending candidate.
- Invoke `osi-prospect-qualification` Profile Mode.
- Handle the verdict:
  - ❌ No or ⚠️ Conditional → STOP-GATE. Log. Continue to next pending.
  - ✅ Yes-no-email → qualification created strategy note + LINKED_IN_CONNECT + 2 LI fallback tasks. Does NOT count toward 3-slot limit. Continue to next pending.
  - ✅ Yes-with-email → forward qualification's handoff to `osi-outreach-sequence`. Counts as 1 of 3.
- Continue until 2 yes-with-email sequences fire OR no pending candidates remain.
- Log status line. Exit.

**Branch B, DISCOVERY MEGA RE-FIRE** (no pending candidates AND any company status `discovery_pending`):
- This branch handles the case where Andy added companies mid-run, OR Branch C (Refill) just appended companies but Discovery Mega hasn't fired on them yet.
- Schedule a new Discovery Mega one-time task to fire in 2-5 minutes. Use the Discovery Mega prompt template below.
- Log status line. Exit.

**Branch C, REFILL** (no pending candidates AND no discovery_pending companies). Fires in BOTH Company Mode and Auto Mode runs:
- Run the cold-company selector (steps below).
- Pick top 5 cold companies. Append to `state.companies` with status `discovery_pending`. Atomic write.
- Schedule a new Discovery Mega one-time task to fire in 2-5 minutes.
- If the selector returns 0 eligible companies, skip the append, fall through to Branch D.
- Log status line including refill batch number + companies picked. Exit.

**Branch D, WRAP-UP** (no pending, no discovery_pending, AND last Refill selector returned 0):
- Update Tab 2 of `prospects-tracker-new.xlsx` with per-company summary if not already done this run.
- Final status line to `overnight-run-log.md`: `WRAP-UP, refill selector exhausted, run complete.`
- Exit clean. Future fires also fall through to wrap-up until Andy starts a new run.

Token budget per Processing fire: ~150-240K (3 sequences × 50-80K each for full LinkedIn read + ZoomInfo + HubSpot writes + email drafts). Branches B and C are cheap (state-file write + one-time-task schedule). Branch D is cheap (Excel write + log).

### Why split into two tasks

Discovery is bursty (one fire = many candidates). Processing is steady (3 sequences/fire). Mixing them means Processing competes with Discovery for token budget and the backlog grows faster than it drains. Splitting keeps each task's load predictable. Two scheduled tasks = two approval pools (Andy approves LinkedIn / HubSpot / ZoomInfo / Chrome ONCE per task on first fire, all subsequent fires reuse).

### NO Discovery Fallback. NO 1-company-per-fire trickle.

The old "Discovery Fallback, pick the FIRST discovery_pending company per fire" branch was removed 2026-04-26. It dragged Discovery out across many fires and left companies sitting unprocessed. Discovery only happens via Discovery Mega (always all-companies-upfront).

### NO Auto-Mode-only Refill.

Refill fires in BOTH Company Mode and Auto Mode runs. If Andy started the run with a named list, the runner finishes that list AND THEN refills with cold Andy-owned companies, because the goal is to keep every fire slot full while the recurring task is enabled. Andy stops refill by disabling the recurring task.

The earlier "Auto-Mode Pivot" was removed because it (a) used a broken shallow-qualify shortcut, (b) drip-fed companies one-per-fire, and (c) was gated on `mode == "auto"` which surprised Andy when his Company Mode runs ended early. The current Refill is the fixed version: full upfront Discovery Mega per refill, fires in any mode.

---

## RUN MODES

### Interactive Mode (in-session, Andy at keyboard)

Andy pastes one LinkedIn profile, OR says "build a sequence for [Name]".
1. Invoke `osi-prospect-qualification` Profile Mode on the candidate.
2. If verdict is ✅ Yes-with-email, qualification hands off to `osi-outreach-sequence`.
3. `osi-outreach-sequence` drafts all 6 emails in interactive form.
4. Show review to Andy → wait for `ready` → open Outlook with Email 1 → Andy clicks Send → say `sent` → queue Emails 2-6.

Interactive Mode does NOT touch the state file or the scheduled tasks. It is a one-off.

### Company Mode (in-session kickoff, then overnight)

Andy says "run sequences for the following companies: X, Y, Z".
1. Kickoff (in-session, ~2 minutes):
   - Read existing `overnight-candidates.json`. Preserve pending entries.
   - Append Andy's named companies to `state.companies` with status `discovery_pending`. JAM-tree (Andy / Mark / John) ownership is fine in Company Mode, Mark- and John-owned companies are allowed when Andy names them explicitly.
   - Schedule **Discovery Mega** one-time task to fire in 2-5 minutes.
   - Schedule **Processing Recurring** with cron `0 0,2,4,6,14,16,18,20,22 * * *` if not already scheduled (9 fires/day, daytime blackout 8 AM to 2 PM ET).
   - Andy approves both schedule calls.
2. Overnight (scheduled tasks):
   - Discovery Mega fire processes all named companies in one upfront sweep, files candidates as `pending`.
   - Processing Recurring works through pending candidates 3/fire.
   - When Andy's named list is fully processed, Refill fires (yes, even in Company Mode) and picks 5 cold Andy-owned companies, schedules new Discovery Mega. Cycle continues until selector returns 0 OR Andy disables the task.

Kickoff does NOT do LinkedIn search, qualification, or outreach itself.

### Auto Mode (in-session kickoff, then overnight, no named companies)

Andy says "run sequences tonight" with no companies.
1. Kickoff:
   - Read existing `overnight-candidates.json`. Preserve pending entries.
   - Run cold-company selector (steps below). Pick top 5. Append to `state.companies` with status `discovery_pending`.
   - Schedule Discovery Mega + Processing Recurring (same as Company Mode).
2. Overnight: same as Company Mode. Refill cycles continue until cold pool exhausted.

Auto Mode is overnight-only. The selector is Andy-owned ONLY (owner ID 196669355, NOT Mark or John).

---

## COLD-COMPANY SELECTOR (Refill + Auto Mode kickoff)

Same logic in both places. Used by Refill (Branch C) and by Auto Mode kickoff.

### Selector steps (in order)

1. **HubSpot search**, `objectType: companies`, filters: `hubspot_owner_id = 196669355` (Andy ONLY, Mark 210187184 and John 210187193 are NOT eligible. Auto-picked Mark/John accounts are off-limits. They can be processed only when Andy names them explicitly in Company Mode.) AND (`notes_last_contacted` 6+ months ago OR null). Sort by `notes_last_contacted` ASC. Pull a generous candidate pool (~50).
2. **Active client filter**, for each candidate, check associated deals. Skip any with closed-won deal in last 12 months OR open deal in active pipeline stage. Do NOT use Lifecycle Stage. Log each skip: `SKIPPED: [Company], active client (deal: [name])`.
3. **M&A check**, quick web search per candidate for recent acquisitions / mergers / rebrands. If the company is a subsidiary of an active OSI customer (e.g. Cable One brands), skip, that customer relationship is owned by another rep. Log skip: `SKIPPED: [Company], M&A subsidiary of [parent], [parent] is OSI customer of [rep]`.
4. **OSI fit check**, keep telecom, ISPs, cable MSOs, fiber, carriers, regional MSOs, data centers, IT infrastructure plays, banks/credit unions with internal IT, hospitals/health systems with IT infra, manufacturers with real IT footprint. Skip retail, food service, pure software/SaaS, hyperscalers, professional services without IT infra ownership.
5. **Queue-prevent filter**, open `C:\Claude-Brain\email-queue.json`. Skip any company where ANY entry has `status: "pending"` OR (`status: "sent"` with `sendDate` within last 30 days).
5a. **DNP filter**, read `C:\Claude-Brain\do-not-auto-prospect.json`. Skip any company whose name case-insensitively matches (substring or exact) any entry in that file. These companies are excluded from Auto Mode and Refill permanently. They can still be worked in Company Mode when Andy names them explicitly. Log each skip: `SKIPPED: [Company], on do-not-auto-prospect list`.
6. **State-dedup filter**, skip any company already present in `state.companies` (any status). Prevents the same coldest companies being re-picked every refill.
7. **Rank**, by OSI fit signal first (telecom + ISPs + DCs first, then enterprise IT, then everything else), then by `notes_last_contacted` ASC. Pick the top **10**.
8. **Write**, append the 5 picks to `state.companies` with `status: "discovery_pending"`. Atomic state file write.
9. **Schedule**, schedule a new one-time Discovery Mega task to fire in 2-5 minutes.

### If selector returns 0

The cold pool is exhausted. Fall through to WRAP-UP. Log: `REFILL EXHAUSTED, selector returned 0 after filters. Wrap-up.`

### Why state-dedup is critical

Without filter 6, the selector would re-pick the same coldest companies every refill and the pool would never advance. `state.companies` is the authoritative list of "already touched this run."

### Why owner-ID filter is critical

Auto-picked Mark/John accounts are off-limits because that's the boundary between "Andy named this, JAM-tree fine" and "the runner picked this on its own, Andy-only." Mark/John accounts can still be processed in Company Mode when Andy names them explicitly.

---

## DISCOVERY MEGA prompt template

When the orchestrator schedules a new Discovery Mega one-time task, use this prompt:

```
You are running OSI Discovery Mega. Process ALL companies marked status discovery_pending in C:\Claude-Brain\overnight-candidates.json.

Read these skills first:
- C:\Claude-Brain\skills\osi-overnight-runner\SKILL.md (you are the orchestrator)
- C:\Claude-Brain\skills\osi-discovery-sweep\SKILL.md (the per-company skill you invoke)

For EACH discovery_pending company in sequence, invoke osi-discovery-sweep with the company's name, hubspot_company_id (if any), and tier. Discovery Sweep does the M&A check, HubSpot ownership check, LinkedIn keyword search rounds, captures cards into state.candidates with status pending, marks the company discovery_complete, and logs.

Discovery Sweep is LIGHT. It does NOT click into individual LinkedIn profiles. Profile reads are Processing's job (osi-prospect-qualification).

When ALL companies marked discovery_complete, exit. Do NOT do Processing, that's the recurring task's job.

Failure modes per skill: log to overnight-run-log.md, never silent. If a single company errors, log + skip + move on. Other companies still get done.
```

Token budget: ~100-150K for 5 companies. Generous ceiling, Discovery Mega's whole job is one concentrated burst.

---

## PROCESSING RECURRING prompt template

The Processing Recurring scheduled task uses this prompt:

```
You are the OSI Processing Recurring runner. Two recurring tasks share this prompt. Weekday cron `0 0,2,4,6,14,16,18,20,22 * * 1-5` (9 fires/day Mon-Fri, daytime blackout 8 AM to 2 PM ET). Weekend cron `0 */2 * * 0,6` (12 fires/day Sat-Sun, no blackout).

Read these skills first:
- C:\Claude-Brain\skills\osi-overnight-runner\SKILL.md (you are the orchestrator)
- C:\Claude-Brain\skills\osi-prospect-qualification\SKILL.md (per-candidate heavy qualifier)
- C:\Claude-Brain\skills\osi-outreach-sequence\SKILL.md (per-qualified-candidate email writer)

Open C:\Claude-Brain\overnight-candidates.json. If missing: log alert to overnight-run-log.md, exit.

Branch (top to bottom priority):

A-prime. ANDY-NAMED DISCOVERY PRIORITY, any company `status: "discovery_pending"` with `added_via` starting `andy_named_` AND added in last 24h → schedule a fresh Discovery Mega one-time task to fire in 2-5 minutes via `mcp__scheduled-tasks__create_scheduled_task`. Log dispatch + list of qualifying companies. Exit (do NOT run Branch A this fire). This outranks Branch A so Andy's mid-run named companies are never blocked behind a stale pending queue.

A. PROCESSING, any candidate status pending → take first (linkedin_search bucket before hubspot_contact bucket per the cadence rule), invoke osi-prospect-qualification FULL Profile Mode (NOT a Path A web-search preview, full pipeline). On verdict:
   - No / Conditional: STOP-GATE per qualification. Atomic write state. ADVANCE TO NEXT PENDING. Run full pipeline on next candidate. Continue.
   - Yes-no-email: qualification creates strategy note + LINKED_IN_CONNECT + 2 LI fallback tasks. Does NOT count toward 3-slot limit. Continue.
   - Yes-with-email: forward qualification's handoff to osi-outreach-sequence. Counts as 1 of 3.
   Continue until 2 yes-with-email OR no pending. Log, exit.

   FORBIDDEN: bulk Path A web-search across multiple pending candidates instead of running each through full Profile Mode. The bulk-preview pattern produces zero outreach output and burns the fire on a step the per-candidate skill already does correctly. See "NO BULK PATH A VERIFICATION" hardwired rule. If a candidate is restricted on LinkedIn, the qualification skill handles it inside its own pipeline (Path B fallback or header-only verification per the audit rule); the orchestrator does not preview.

B. DISCOVERY MEGA RE-FIRE, no pending AND any company discovery_pending → schedule a new one-time Discovery Mega task to fire in 2-5 minutes (same prompt template as kickoff). Log, exit.

C. REFILL, no pending AND no discovery_pending (fires in BOTH Company Mode and Auto Mode) → run cold-company selector (Andy-owned ONLY for the selector, Mark/John never auto-picked, 6+ months no activity, active-client filter, M&A check, OSI fit check, queue-prevent filter, state-dedup filter), pick top 5, append to state.companies as discovery_pending, schedule new Discovery Mega in 2-5 minutes. If selector returns 0, fall through to D. Log, exit.

D. WRAP-UP, no pending, no discovery_pending, AND last refill selector returned 0 → update Tab 2 of prospects-tracker-new.xlsx, write final status line "WRAP-UP, refill selector exhausted, run complete", exit clean. Future fires also fall through to wrap-up until Andy starts a new run.

NO 1-company-per-fire trickle anywhere. Discovery only happens via Discovery Mega (always all-companies-upfront).

Token ceiling: 2 outreach sequences per fire (Branch A). Branches B, C, D are cheap.

Failure modes per skill: log to overnight-run-log.md, never silent.
```

---

## STATE FILE, `overnight-candidates.json`

Path: `C:\Claude-Brain\overnight-candidates.json`. Sticky across runs. Atomic writes only (`.tmp` + `os.replace`).

### Schema

```json
{
  "run_id": "YYYY-MM-DD-name",
  "created": "ISO8601",
  "mode": "company | auto",
  "companies": [
    {
      "name": "Company Name",
      "status": "discovery_pending | discovery_complete",
      "hubspot_company_id": 12345,
      "domain": "example.com",
      "tier": "telecom | enterprise_it | manufacturing | ...",
      "added_via": "andy_named_YYYY-MM-DD | refill_YYYY-MM-DD | manual_add",
      "selection_notes": "...",
      "discovery_completed_at": "ISO8601",
      "discovery_notes": "..."
    }
  ],
  "candidates": [
    {
      "id": "firstname-lastname-company-slug",
      "firstName": "First",
      "lastName": "Last",
      "company": "Company Name",
      "linkedinUrl": "https://www.linkedin.com/in/handle",
      "title": "Director, Network Engineering",
      "source": "linkedin_search | hubspot_contact",
      "hubspotContactId": 12345,
      "status": "pending | no | conditional | yes-no-email | yes-with-email | skipped-active-sequence | pending-relookup",
      "addedDate": "YYYY-MM-DD",
      "processedDate": "ISO8601",
      "verdict_reason": "..."
    }
  ],
  "stagger": {
    "Company Name": {
      "last_day1": "YYYY-MM-DD",
      "person_count": 0
    }
  }
}
```

### Status state machines

**Companies:** `discovery_pending` → `discovery_complete`. Once complete, only flipped back to `discovery_pending` if the original Discovery used the now-removed shallow shortcut (rare) and a fresh sweep is needed.

**Candidates:**
- `pending` → after qualification → `no` / `conditional` / `yes-no-email` / `yes-with-email` / `skipped-active-sequence`
- `pending-relookup` is reserved for emergency pause (something got mis-queued and needs human review before re-qualification). The runner does NOT process `pending-relookup` candidates automatically; they must be manually flipped back to `pending`.

### Atomic writes

Always write to `state.tmp` then `os.replace(state.tmp, state)`. Never delete-then-write.

---

## KICKOFF (in-session, ~2 minutes)

Triggered by Andy's command: "run sequences for the following companies: X, Y, Z" (Company Mode), "run sequences tonight" (Auto Mode), or paste a single profile (Interactive Mode, no kickoff).

For Company Mode and Auto Mode:

1. Read existing `C:\Claude-Brain\overnight-candidates.json`. Preserve pending entries.
2. Populate company list:
   - **Company Mode:** Andy's named list, all marked `discovery_pending`. JAM-tree owners (Mark, John) are fine in Company Mode.
   - **Auto Mode:** run cold-company selector (Andy-owned ONLY), pick top 5, mark `discovery_pending`.
3. Schedule **Discovery Mega** as a one-time task firing in 2-5 minutes (or immediately via Run now). Use the Discovery Mega prompt template above.
4. Schedule **Processing Recurring** as TWO recurring tasks if not already scheduled (one weekday, one weekend). Use the Processing Recurring prompt template above for both.
   - Weekday: cron `0 0,2,4,6,14,16,18,20,22 * * 1-5` (9 fires/day Mon-Fri, daytime blackout 8 AM to 2 PM ET).
   - Weekend: cron `0 */2 * * 0,6` (12 fires/day Sat-Sun, no blackout).
5. Done. Andy approves both schedule calls.

Kickoff does NOT invoke discovery-sweep, qualification, or outreach-sequence directly. Those run only in scheduled-task fires.

---

## MID-RUN ADDITIONS

If Andy adds a company manually to `state.companies` with `status: "discovery_pending"` while a run is in progress, the next Processing Recurring fire detects it via Branch B (Discovery Mega Re-Fire) and schedules a fresh Discovery Mega task. The new Discovery Mega processes the added company in its next fire.

If Andy adds a candidate manually to `state.candidates` with `status: "pending"`, the next Processing Recurring fire picks it up via Branch A (Processing) and runs qualification on it.

State file is the source of truth. Edits to it propagate naturally through the next fire.

---

## JAM OWNERSHIP DECISION TREE

Used by `osi-discovery-sweep` (Step 2 HubSpot ownership check) and by Refill selector (filter 1 + filter 3).

| Situation | Action |
|---|---|
| Not in HubSpot | Proceed |
| Owned by Andy (196669355) | Proceed |
| Owned by Mark (210187184) | Proceed in Company Mode (Andy named); SKIP in Refill / Auto Mode |
| Owned by John (210187193) | Proceed in Company Mode (Andy named); SKIP in Refill / Auto Mode |
| Other rep, recent activity (within 3 months) | Skip silent. Log to overnight-run-log.md |
| Other rep, no activity 3+ months, not a client | Log for account-request. Do NOT prospect |

Refill / Auto-Mode boundary is hardwired: only Andy's owner ID is auto-picked by the selector. Mark and John accounts only enter the run when Andy names them explicitly in Company Mode at kickoff.

---

## FAILURE MODES, never silent

Every failure logs to `Claude-Brain/overnight-run-log.md` with timestamp + reason:
- State file missing → log alert, exit. Don't try to recreate.
- Discovery Mega scheduling fails → retry once, then log + exit. Andy may need to manually reschedule.
- Processing Recurring scheduled task disabled → next fire never happens, but the state file is preserved. Andy can re-enable.
- Branch routing logic crashes mid-fire → log the partial state (which candidate / company was being processed), exit. Next fire picks up.
- A skill invocation fails (discovery-sweep / qualification / outreach-sequence) → log the failure, mark the company or candidate appropriately, continue with the next item. Don't abort the entire fire on one bad item.

---

## RULES

- Orchestrator never does the work itself, always invokes the right skill.
- Refill fires in BOTH Company Mode and Auto Mode. Never gate on mode for Refill.
- Refill selector is Andy-owned ONLY (Mark/John never auto-picked).
- Discovery only happens via Discovery Mega (one-time task). Never per-fire trickle.
- Every Refill cycle and every mid-run addition schedules a fresh Discovery Mega.
- State file is the source of truth. Atomic writes only.
- Branch A (Processing) is top priority every fire, leftover pending candidates from previous runs get worked first.
- 2 yes-with-email per fire is the hard ceiling for Branch A (lowered from 3 on 2026-05-01). Yes-no-email and No / Conditional do NOT count toward this ceiling.
- Wrap-up only triggers when refill selector returns 0 (true exhaustion). Future fires fall through to wrap-up cleanly until Andy starts a new run.
- Never auto-pivot to Mark/John accounts. Andy approves those explicitly via Company Mode at kickoff.
- Always log every branch decision and every failure.
