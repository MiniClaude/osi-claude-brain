# Andy's Second Brain  -  Master Instructions

## 🚨 READ THE SKILL FIRST. EVERY TIME. NO EXCEPTIONS. (added 2026-05-05)

When Andy's message mentions a skill by name OR triggers a skill workflow, the FIRST action is to read that skill's SKILL.md. Before any HubSpot call. Before any LinkedIn search. Before any ZoomInfo call. Before writing a single word of outreach.

Trigger -> Skill to read FIRST:
- "find prospects at [company]" / "find me people at" / "qualify" -> `C:\Claude-Brain\skills\osi-prospect-qualification\SKILL.md`
- "run a sequence" / "outreach sequence" / "build a sequence" -> BOTH `C:\Claude-Brain\skills\osi-prospect-qualification\SKILL.md` AND `C:\Claude-Brain\skills\osi-outreach-sequence\SKILL.md`. Read both. Not one. Both.
- "re-engage" / "re-engagement" -> `C:\Claude-Brain\skills\osi-3email-reengagement\SKILL.md`
- "3-email" / "short sequence" -> `C:\Claude-Brain\skills\osi-3email-new\SKILL.md`
- "find cold connections" -> `C:\Claude-Brain\skills\osi-cold-reengagement\SKILL.md`
- "run the monitor" / "sequence status" -> `C:\Claude-Brain\skills\osi-monitor\SKILL.md`
- "send emails" / "email sender" -> `C:\Claude-Brain\skills\osi-email-sender\SKILL.md`

If Andy says "read the [X] skill" in his message: read it IMMEDIATELY as the first tool call. Not after trying something. Not after asking a clarifying question. First.

**Company Mode always requires BOTH skills.** If Andy asks to find AND sequence prospects at a company, that is Company Mode. Company Mode is governed by osi-prospect-qualification (discovery, qualification, LinkedIn browsing) AND osi-outreach-sequence (drafting, queueing). Reading only the outreach skill and skipping the qualification skill is a guaranteed failure mode -- the outreach skill contains zero discovery logic.

**Special alert -- hedge funds and quant firms:** D.E. Shaw, Renaissance, Two Sigma, Citadel, Jane Street, Millennium, Point72, and similar firms have employees who deliberately scrub LinkedIn profiles. Keyword searches return near-zero results at these firms. The ONLY viable discovery path is the Round 0 card browse in the qualification skill. If the qualification skill has not been read, you do not know this rule. Read it first.

**Why this rule exists:** 2026-05-05 -- Andy's first message said "find prospects at siemens energy... read the prospecting skill and outreach skill." Claude ignored it and improvised. 2026-05-08 -- Company Mode on D.E. Shaw read the outreach skill but not the qualification skill. The Round 0 browse was skipped. Three VP-level data center targets were missed because keyword searches returned nothing against a firm where employees deliberately strip their profiles.

---

## 🚨 NO APPROVAL PROMPTS DURING SCHEDULED FIRES (added 2026-04-29)

If any tool call triggers an approval prompt during a scheduled-task fire (overnight runner, processing recurring, monitor, email-sender, any cron-fired session), abort that step immediately. Apply the local stop-gate (mark candidate Conditional / `pending-relookup`, mark company skipped, etc.), log to `Claude-Brain/overnight-run-log.md` as a skill bug, continue with the next item or exit clean.

Applies to the orchestrator AND to every subagent (Agent tool dispatch) it spawns. Subagents inherit the rule. The trigger is the prompt itself, not a specific tool. Do not maintain an allowlist that drifts. Do not rationalize "this prompt is small." Any prompt = abort.

What this means in practice:
- Verification during scheduled fires is LinkedIn (Chrome MCP) only. No corporate website fetches, no Google for bio confirmation, no podcast pages, no press release fetches.
- M&A and personalization research during scheduled fires is ZoomInfo `enrich_scoops` / `enrich_news` / `account_research` only. ZI can be stale; the alternative (a prompt overnight) is not acceptable.
- HubSpot reads/writes, ZoomInfo, Outlook compose (when pre-approved at kickoff), file system, atomic state writes: allowed.
- If a verification fails because the only allowed source could not close it, mark Conditional and move on. Do NOT pivot to a different surface that might prompt.

If a fire triggers a prompt, that is a bug in the skill that called the prompting tool. Stop and fix the skill. Do NOT one-off it.

Interactive sessions (Andy at keyboard) keep the broader research surface. The rule fires only when the session is launched by a scheduled task.

**Why this rule exists:** 2026-04-29 — overnight Processing Recurring fire ran a Patti Paulo (ExteNet Systems) qualification subagent that hit a restricted LinkedIn profile and followed the qualification skill's documented Path B fallback by `web_fetch`-ing `extenet.com/about-us/leadership/patti-paulo`. That fetch prompted Andy for browser permission overnight. The orchestrator promised zero prompts during scheduled fires; the qualification skill broke the promise via a documented fallback. The fix is the inverted rule above plus parallel rules in osi-overnight-runner, osi-prospect-qualification, osi-discovery-sweep, osi-outreach-sequence.

---

## 🚨 HUBSPOT-FIRST EMAIL RESOLUTION (added 2026-04-27)

Before creating any new HubSpot contact OR queueing any email, search HubSpot by `firstname + lastname + company`. Use the existing contact's primary email. Do NOT trust ZoomInfo as the authority on contact identity. ZoomInfo is enrichment only.

If no HubSpot match exists, derive the company's **verified** email pattern from engagement signals (replies, opens, bounces) at that company — not from "most common stored format." Stored formats include the bad ZoomInfo guesses we're trying to filter out. Full algorithm at `knowledge/email-pattern-resolver.md`.

When ZoomInfo returns an email different from the chosen address, write the ZoomInfo address to the contact's `hs_additional_emails` and prepend a top-of-notes line: `ALT EMAIL <date>: ZoomInfo lists <email>. Using <chosen>. Pattern: <pattern> verified by <signal>.` Andy reviews every contact before sending — that line surfaces the alternate.

**Why this rule exists:** on 2026-04-27 the prospecting flow created a duplicate John Lubeck contact at Midco using the ZoomInfo-pattern email `jlubeck@midco.com` instead of finding the existing HubSpot record under the verified primary `john.lubeck@midco.com`. Six emails queued to the wrong address before catch. The HubSpot-first rule prevents the dupe; the engagement-weighted pattern check prevents bad-pattern guesses; the alt-email note keeps Andy's manual-review step efficient.

---

## 🚨 NO EMPLOYER VERIFICATION, NO SEQUENCE (added 2026-04-26)

Every candidate must have current employer verified before any verdict, any HubSpot write, any email queued. Two valid paths:

**Path A (default, strongly preferred):** full LinkedIn profile read. About + Experience + Skills + Activity. The current Experience entry confirms the company and start date.

**Path B (fallback, only when LinkedIn truly does not exist):** ZoomInfo email at the company's corporate domain AND a dated web-search confirmation that they currently work there. Acceptable sources: company website team page, conference speaker bio, press release, podcast bio, recent industry article naming them at the company. Source must be within the last 6 months. Strategy note carries an explicit `EMPLOYER VERIFICATION: [source URL + date]` line.

If neither path closes: mark `no` for "could not verify current employer", STOP-GATE.

🛑 **ZoomInfo NO_MATCH or COMPANY_ONLY_MATCH is NOT a verification failure.** ZI failing to match a person means ZI doesn't have them in its database. It does NOT mean their employer is unconfirmable. The employer truth lives on LinkedIn, not in ZoomInfo. When ZI returns NO_MATCH or COMPANY_ONLY_MATCH, the next step is ALWAYS Path A: LinkedIn search by name + company. Anyone with a LinkedIn presence is findable in under 30 seconds via name + employer search. A "could not verify current employer" Conditional verdict is ONLY valid after BOTH (a) LinkedIn search by name + company returned no live profile (try full name, last+first, common nickname variants), AND (b) a web search returned no dated source within 6 months. Skipping Path A because ZI whiffed is a bug. Re-process the candidate via Path A.

What's NOT allowed: "they're in HubSpot so they probably still work there." HubSpot records go stale. ZoomInfo records go stale. Title alone never qualifies. The verification step is the whole point.

**Why this rule exists:** on 2026-04-24 the qualification skill was rewritten to add a "shallow qualify path" that skipped LinkedIn for HubSpot-sourced contacts on the theory that human curation already happened. By 2026-04-26 this had produced 138 emails queued to 23 prospects across S&P Global, OEC Fiber, Fidelity Communications, Vero Networks, and Midcontinent without anyone confirming those people were still employed there. The path was ripped out the same day. If a future Claude session ever proposes a "speed up by skipping employer verification" optimization, point it at this section first.

**Why the ZI NO_MATCH sub-rule exists:** on 2026-04-28 the 10:25Z runner fire processed 11 S&P Global candidates and marked 4 of them Conditional ("could not verify employer") solely on ZoomInfo NO_MATCH or COMPANY_ONLY_MATCH responses. Andy could find every one of them on LinkedIn in seconds. The shortcut treated ZoomInfo as the verification source, which is exactly backwards. ZoomInfo enriches. LinkedIn verifies. Same fire also flagged Daymond Tadlas at Consumer Cellular under the identical mistake. All five were flipped back to `pending` and the rule was hardwired so a future Claude session cannot repeat the shortcut.

---

## 🚨 OSI PRODUCT LINES - EVALUATE ALL OF THESE EVERY TIME YOU QUALIFY A PROSPECT

1. **Optics** - OSI transceivers (SmartOptics-manufactured, private-labeled). Sample offer is the opening wedge for any network engineer or architect.
2. **DWDM & Open Line Systems** - SmartOptics DCP platform. 30-50% below Ciena/Nokia. Ships in weeks.
3. **Compute & Components** - Dell/HP servers (authorized partner). **DIMMs ARE A HUGE PLAY RIGHT NOW** - Samsung/Hynix/Micron, manufacturer warranties, below-OEM. DDR4 significantly cheaper than DDR5 for workloads that don't need it. Lead with DIMMs first, server refresh second.
4. **Storage** - NetApp TPM, pre-owned storage gear, server components.
5. **TPM** - Gartner-recognized, privately owned, no PE, 40-60% below OEM. Multi-vendor (Cisco, Dell, HP, NetApp, Juniper, Arista).
6. **Pre-Owned & New Networking Gear** - Pre-owned Cisco/Juniper/Arista (tested, OSI TPM available). New Nokia (authorized partner).
7. **Professional Services** - Deployment, network design, migration. Second-conversation topic only - never lead cold.

**Anyone with Servers, Hardware, Storage, or Data Center skills = Compute/Components target. Do not skip this.**

---

## ⚡ SESSION STARTUP CHECKLIST
You are reading this file as part of session startup. Before doing anything else, read ALL of the following:
- [ ] Every file in `knowledge/`  -  sales playbook, qualification skill, and anything else in the folder
- [ ] Every file in `people/`  -  know who Andy is already tracking
- [ ] Every file in `accounts/`  -  know the active accounts and context
- [ ] Every file in `outreach/`  -  know what's been sent or drafted
- [ ] Check `inbox/` for any new files Andy has dropped
- [ ] Skim the most recent file in `sessions/`  -  know where things left off
- [ ] Confirm ready: tell Andy you've read everything and are ready to work

**Do not qualify prospects, write outreach, or give account advice until all folders above are read.**

---

## Who I Am
- **Name:** Andy (Andrew)  -  Solutions Executive at OSI Global
- **Email:** andy@osiglobal.com
- **Role:** Sales / Business Development  -  optical networking and data center hardware
- **Company:** OSI Global  -  sells networking hardware including DWDM, 400G transceivers, and optical components
- **CRM:** HubSpot (Owner ID: 196669355)
- **Communication platform:** Microsoft Teams
- **Working setup:** Two laptops, both synced via Git and GitHub. Working copy lives at `C:\Claude-Brain\` on both machines. Remote backup at `github.com/Drrewdy/Claude-Brain` (private repo). OneDrive is no longer used for syncing Claude-Brain content. The email queue (`email-queue.json`) lives at `C:\Claude-Brain\email-queue.json` along with everything else. Sync between laptops is via git push/pull. Skills that read or write the queue MUST `git pull` at the start of any batch and `git push` at the end so the other laptop sees the updates without manual intervention.

---

## The Andy Rules (ALWAYS follow these)

### 1. Brevity
All summaries, outreach drafts, and responses must be **under 100 words** unless I explicitly ask for more. I don't need fluff  -  get to the point.

### 2. Surgical Isolation
**Always** keep these two things completely separate:
- **Technical specs** (DWDM specs, 400G transceiver details, lead times, hardware comparisons, Smartoptics data)
- **Sales / business strategy** (outreach approach, account strategy, competitive positioning, pricing conversations)

Never mix them in the same output. If both are needed, present them in clearly labelled separate sections.

### 3. Defensibility
Everything you produce must be something I can explain and defend **solo**, without needing an engineer in the room. Avoid jargon I can't own. If something is technical, translate it into language I can use confidently on a call.

### 4. No Em-Dashes. Ever.
**NEVER use the character — in any output, any file, any email, any message. Not once. Not ever.**
Split thoughts into two sentences instead. This is non-negotiable.

### 5. No Re-explaining
You have full context in this file. Never make me re-explain who I am, what OSI does, or what my rules are. Read this file first, every session.

---

## OSI Global  -  What We Sell

### Core Products
- **DWDM hardware**  -  Dense Wavelength Division Multiplexing optical networking gear
- **400G transceivers and upgrades**  -  key growth area; many prospects are actively upgrading
- **Smartoptics**  -  our key vendor/product line; positioned against "anonymous factory" importers
- **Optical components**  -  broader portfolio for data center and carrier networks

### Key Sales Wedges
- **Lead time advantage**  -  we can deliver faster than anonymous factory importers; this is a top objection-handler
- **Smartoptics vs. grey market**  -  quality, warranty, and support differentiation
- **400G upgrade path**  -  many accounts still running 100G; we help them plan and execute the upgrade
- **Vendor-agnostic approach**  -  OSI can support multi-vendor environments

### Ideal Customer Profile
- Data center operators and managers
- Network engineers and IT directors at mid-to-large enterprises
- Telecom/carrier network teams
- Companies actively planning 400G upgrades or dealing with long lead times from other suppliers

---

## Key Accounts & Context

### Colleagues
- **Andy, Mark Metz, and John Houston are the same team.** Accounts owned by Mark or John in HubSpot are fully fair game. Never flag their ownership as a conflict. Never ask Andy to clear it with them.

---

## How I Work With Claude

### Session Startup
Every session, read this file first. Do not ask me to re-introduce myself or explain OSI. Start ready to work.

### My Preferred Output Style
- Short, punchy, direct
- No bullet-point overload  -  prose where possible
- Outreach drafts: conversational, not corporate. I'm reaching out as Andy, not as a company
- If I ask for an email or LinkedIn message, write it as if I'm a human being, not a press release

### What I Use Claude For
1. **LinkedIn outreach**  -  researching prospects, writing personalized connection messages and follow-ups
2. **Account research**  -  qualifying leads, understanding what a company does before I reach out
3. **HubSpot**  -  searching contacts, reviewing account notes, updating records
4. **Meeting prep**  -  pulling together what I know about a prospect before a call
5. **Second Brain capture**  -  processing notes I drop here into organized, searchable summaries
6. **Competitive intel**  -  comparing Smartoptics vs. competitors on lead time, specs, price

### Daily / On-Demand Workflow
When I say "process my notes" or "catch me up":
1. Check this folder for any new files I've dropped in
2. Summarize them following the Andy Rules
3. Flag anything that looks like a hot lead or action item
4. Ask if anything needs to go into HubSpot

---

## Second Brain Structure

**This Git-versioned folder is the single source of truth. Working copy lives at `C:\Claude-Brain\` on both laptops, backed up to GitHub (`github.com/Drrewdy/Claude-Brain`). All projects, notes, research, and outreach live here. Always point Cowork to this folder on both laptops.**

### Git / GitHub Workflow (READ THIS)
The folder is a Git repo, not a synced OneDrive folder. That means syncing is manual and explicit. Three commands in Git Bash run the whole show:
- **Start of session (pull down the latest):** `git pull`
- **End of session (push your changes up):** `git add .` then `git commit -m "what changed"` then `git push`

Rules of thumb: always `git pull` before starting work, always `git push` when finished. If Andy edits the same file on both laptops without pulling in between, Git will ask to merge. For `.xlsx` files this is painful, so for spreadsheets: pull, edit, push immediately.

If Claude is running a task that modifies files in this folder, Claude should offer to commit and push at the end of the task so the other laptop can pull the change.

### Folder Layout
- `Claude-Brain/` ← this folder (`C:\Claude-Brain\`)
  - `CLAUDE.md` ← this file  -  read every session before doing anything
  - `inbox/` ← drop raw notes here for processing
  - `sessions/` ← end-of-session summaries, one file per session (session-YYYY-MM-DD.md)
  - `people/` ← summaries of key contacts and prospects
  - `accounts/` ← account-level research and strategy notes
  - `outreach/` ← outreach templates and sequences
  - `knowledge/` ← product knowledge, competitive intel, talking points
    - `OSI-Sales-Playbook.md` ← **master sales playbook  -  read this for every outreach task**

### Key Files to Read
- Before any outreach or prospecting task: read `knowledge/OSI-Sales-Playbook.md`
- Before any LinkedIn prospecting or qualification: read `knowledge/OSI_Prospect_Qualification_Skill.md`
- For company-mode prospecting ("find me people at X company"): use the Company Mode workflow in `knowledge/OSI_Prospect_Qualification_Skill.md`

### Skills Folder

🚨 **HARD RULE: EVERY SKILL LIVES IN `Claude-Brain/skills/`. NO EXCEPTIONS.**
Both the source folder (`skills/[skill-name]/SKILL.md`) AND the packaged `.skill` file (`skills/[skill-name].skill`) must be inside the `skills/` directory. Never at the root of `Claude-Brain/`. Never in a sibling folder. Never scattered across multiple locations. If a Claude session creates a `.skill` file anywhere other than `Claude-Brain/skills/`, move it immediately. Runtime data files (like `reengagement-tracker.json`) belong at the root of `Claude-Brain/`, NOT in `skills/`. Skills folder is ONLY for skill sources and their packages.

🚨 **HARD RULE: `email-queue.json` LIVES IN `C:\Claude-Brain\` (manual git only).**
As of 2026-04-25 the email queue moved BACK from OneDrive to `C:\Claude-Brain\email-queue.json`. The OneDrive sync was eliminating itself one prompt at a time: every scheduled-task session triggered a Cowork mount approval prompt. Now the queue is git-versioned along with everything else.

🚨 **HARD RULE: NO AUTO GIT IN SCHEDULED TASKS / RUNNERS.**
Skills must NOT call `git pull` or `git push` automatically. Reasons: (1) `.git/index.lock` keeps getting stuck because the sandbox can't always delete it, blocking subsequent operations; (2) Andy only runs the runner on ONE laptop, so auto-sync isn't needed; (3) auto-git pollutes logs with `GIT WARN` noise every fire. Skills read and write to disk; Andy commits and pushes manually when he wants to sync to the other laptop.

If a skill or scheduled task previously did `git pull` / `git push` automatically, remove that logic. Do NOT log `GIT WARN` lines about lock files. Just write to disk cleanly and exit.

The hard-block list (`hard-block.json`) also stays in Git at `C:\Claude-Brain\hard-block.json` (manual sync, same rule).

Reusable skills live in `Claude-Brain/skills/` (NOT `.claude/skills/` - that is read-only). Current skills:
- `osi-outreach-7email` - Full 7-email hyper-personalized sequence. Trigger: "run the 7-email sequence for [name]"
- `osi-3email-new` - 3-email new outreach for directors or shorter-touch targets. Trigger: "3-email sequence for [name]"
- `osi-3email-reengagement` - 3-email re-engagement for prospects who already went through a 7-email sequence. Trigger: "re-engage [name]"
- `osi-cold-reengagement` - Finds cold 1st-degree LinkedIn connections, creates 2 InMail tasks 2 weeks apart. Regular LinkedIn only. Trigger: "find cold connections"
- `osi-prospect-qualification` - Qualification workflow for evaluating prospects against OSI ICP

### Skill Editing & Install Workflow (REDIRECT-STUB ARCHITECTURE, 2026-04-29)

🚨 **READ FIRST — the runtime is intentionally a stub.** As of 2026-04-29 the Cowork runtime backing store at `.../skills-plugin/<plugin-id>/<session-id>/skills/[skill-name]/SKILL.md` no longer contains real skill logic. It contains a one-line redirect that tells Claude to Read `C:\Claude-Brain\skills\[skill-name]\SKILL.md` and execute that file instead. Every scheduled-task fire, every skill triggering event, the runtime stub loads first, and the live source loads on top of it. The runtime cannot drift from source because it has no source-equivalent content of its own.

**If you find yourself "fixing" the runtime by copying full skill content over a stub, STOP.** That is the bug we just removed. The stub is correct. The runtime should be ~2 KB of redirect text and nothing else. If a skill behaves wrong, fix the source at `C:\Claude-Brain\skills\[skill-name]\SKILL.md`. Do not add content to the runtime.

**The new workflow when you edit a skill:**

1. **Edit** `Claude-Brain/skills/[skill-name]/SKILL.md` (source of truth, Git-versioned). That is the live file. Cowork's runtime stub will Read this file on every fire.
2. **(Optional) Repackage** the `.skill` zip for distribution between machines or for re-install via drag-drop:
   ```bash
   cd Claude-Brain/skills/[skill-name] && zip -rq /tmp/x.skill SKILL.md
   cp -f /tmp/x.skill Claude-Brain/skills/[skill-name].skill
   ```
   The `.skill` zip currently contains the FULL source content, not the stub. If anyone re-installs from the zip, they overwrite the stub with full content, which RE-INTRODUCES drift. The morning-skill-sync auto-heal (planned, not yet built) will detect that and re-stub. Until that's built, after a re-install you must manually re-apply the stub via the runtime install procedure below.
3. **No "force-copy to runtime" step.** The runtime is already a stub that pulls from source on every fire.

**If for any reason you need to install a stub (new skill, drift detected, post-reinstall heal):**

```python
# Pull the source frontmatter, generate a stub with the redirect body,
# write to the runtime SKILL.md path. The full source stays untouched.
# Reference implementation: see the 2026-04-29 stub deployment in this file's history.
```

The stub frontmatter must match the source frontmatter (preserves Cowork triggering by description). The stub body is the same redirect template across every skill.

**Source skills with no runtime entry** (`osi-overnight-runner`, `osi-discovery-sweep`, `osi-meeting-followup`): these are read by direct file path from scheduled-task prompts. They never need a runtime stub. Do not add one.

**Runtime-only skills** (`docx`, `pdf`, `pptx`, `xlsx`, `consolidate-memory`, `schedule`, `setup-cowork`, `skill-creator`): these ship with Cowork itself. We don't manage their source. Leave alone.

**If `.skill` files anywhere outside `Claude-Brain/skills/` get created:** delete immediately. They cause duplicate-skill confusion (caused a mess in April 2026).

**Why Claude-Brain is the ONLY editing location:** the runtime backing store has been found truncated/corrupted before (185 lines vs 449 actual). The Git-versioned `C:\Claude-Brain\` folder (backed up on GitHub) is the only reliable copy. Edit there. The runtime stub will pull the live version on every fire.

**Morning skill sync (auto-heal planned):** The `morning-skill-sync` scheduled task runs weekday mornings. Currently it reports drift; the planned upgrade is for it to auto-heal by re-stubbing the runtime if it detects full content where there should be a stub. Until that's built, drift is unlikely (because every fire reads source via the stub) but possible (if someone re-installs via drag-drop). If morning-skill-sync flags drift, force-stub the affected skills.

**Why this rewrite happened (2026-04-29 incident):** the `osi-email-sender` runtime fell 2,675 bytes behind source after multiple Claude sessions edited the source without doing the force-copy step. The email-sender then skipped 8 of 11 due entries because the runtime was missing a recent fix. Andy halted the run. The four-step manual workflow had been failing silently for at least a week. Architectural fix: replace the runtime with a redirect stub so drift becomes impossible by construction. The runtime cannot be stale if it contains no skill content.

### Cold Re-Engagement vs. Full Sequence - Keep These Separate
- **Cold re-engagement** = 2 InMail tasks only (no strategy doc, no email sequence). Used when working existing 1st-degree LinkedIn connections who've gone cold.
- **7-email or 3-email sequence** = full outreach package. Used when actively prospecting a specific person.
These are different workflows. Do not run both on the same person without Andy explicitly asking for both.

### 6-Month LinkedIn Message Check Rule
When running cold re-engagement:
- HubSpot last contacted 6+ months ago: skip LinkedIn message check. Already confirmed cold. Go straight to qualification.
- HubSpot last contacted within 6 months: disqualify immediately.
- No HubSpot record: always check LinkedIn messages before proceeding.

### Capture Rule
If I drop a file or paste text without instructions, assume I want it processed, summarized, and filed per the Andy Rules. Tell me where you filed it and flag any action items.

### Session Summary Rule
At the end of every session, save a summary to `sessions/` using the filename format `session-YYYY-MM-DD.md`. Include: what we worked on, any outputs created, action items, and anything that should go into HubSpot. Keep it under 150 words per the Andy Rules.

---

## LinkedIn Prospecting & Outreach Framework

### How to Research a Prospect (Always follow this process)
1. Start on **LinkedIn Sales Navigator**  -  pull the full profile
2. Switch to their **LinkedIn profile** for anything Sales Nav truncates
3. **Expand everything**  -  click every "Show more", "Load more", "See more" button on both platforms. No exceptions.
4. Read the **full About section**  -  if it's long, read all of it. People often describe their actual tech stack or infrastructure in there.
5. Read **every experience description**  -  especially at their current company. A title can be misleading; the description tells you what they actually do.
6. Read the **full skills list**  -  click through to load all skills and note endorsement counts. Skills are a truth filter.
7. **Check HubSpot**  -  is this person or their company already in CRM? Who owns the account?

### Qualification Criteria  -  Who I Want to Target
OSI sells optical networking hardware (DWDM, 400G, Smartoptics). The right person is someone who:
- **Buys or specifies** networking hardware  -  not just someone who works near it
- Has titles like: Network Engineer, IT Director, Data Center Infrastructure Manager, Network Architect, Infrastructure Lead, Procurement/Sourcing (IT/Network), VP of IT, Director of IT
- Shows **networking skills** with real endorsements: Cisco, optical networking, DWDM, transceivers, data center infrastructure, network design, vendor management for hardware
- Works at a **mid-to-large enterprise, carrier, telecom, or regional data center operator**  -  not a hyperscaler building at Google/Meta/ByteDance scale with custom supply chains
- Company is **actively upgrading infrastructure**  -  signs include 400G references, network modernization projects, data center buildouts

### Disqualifying Signals  -  Who to Skip
- **Program/Project Managers** embedded in a data center org  -  they manage processes, not hardware procurement. Title says "Data Center" but function is ops/change management.
- **Hyperscaler accounts** (Google, Meta, Amazon, ByteDance/TikTok at scale)  -  they build custom, OSI can't compete on that level
- Skills that are all project management, Lean Six Sigma, Scrum, supply chain ops  -  and zero networking/infrastructure skills
- Someone who "manages 700,000 servers" in a lifecycle/decommission role  -  that's an operations function, not a buying function

### The Verdict Format
Every prospect research session ends with a clear verdict:
- ✅ **Yes**  -  worth reaching out, here's why and here's the angle
- ❌ **No**  -  not the right fit, here's exactly why (so I can explain it if asked)

No grey area. If it's a maybe, default to No and explain what would need to be true for it to be a Yes.

### Example Verdict (Reference)
**Jeff Cheng, ByteDance**  -  ❌ No
Title says "Data Center Strategy & Operations" but his entire career is program management and organizational change inside a DC org. Skills: 29 endorsements for Project Management, 1 for Data Center Infrastructure. Zero networking, Cisco, storage, or hardware procurement skills. Works in a hyperscaler building at a scale OSI doesn't sell into. He manages programs around the hardware, not the procurement of it.

### Outreach Principles
- Personalize every message to something specific about the person or their company
- Lead with relevance  -  what's happening in their world that OSI can help with
- Keep connection requests under 300 characters
- Follow-up messages: one clear ask, no more
- Tone: direct, human, peer-to-peer  -  not vendor-to-buyer
- Never pitch in the first message  -  connect first, earn the conversation

---

## Notes on Data & Privacy
- This file lives in a private GitHub repo (`github.com/Drrewdy/Claude-Brain`) with the working copy at `C:\Claude-Brain\` on each laptop. The repo is private and only Andy has access.
- Do not store specific serial numbers, unreleased pricing, or confidential customer contract details in plain text here
- For sensitive deal specifics, reference HubSpot instead
- The old OneDrive Claude-Brain folder was DELETED 2026-04-30 on the work laptop. The personal laptop's `C:\Users\drrew\OneDrive\Claude-Brain` may still exist as a stale copy; do NOT read or write to it. The single source of truth is `C:\Claude-Brain\` on each laptop, synced via Git. Cowork's scheduled-task storage still writes to `C:\Users\Andy\OneDrive - OSI Hardware\Documents\Claude\Scheduled\` because that path is hardcoded in Cowork's `create_scheduled_task` tool. That folder is local-only (OneDrive Backup off); the "OneDrive" in the path name is misleading. Scheduled tasks fire fine from there. The Cowork app config is the only thing that could redirect that path, and it's not exposed via MCP.
