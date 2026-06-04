# Claude-Brain: System Documentation

This is the project documentation for Andy's Second Brain, the OSI Global sales automation and prospecting system that lives in this repository.

It explains what the system is, how the pieces fit together, and where to look when something needs changing. For the operating rules and personal context, see [CLAUDE.md](../CLAUDE.md) at the repo root. That file is the source of truth for behavior. This folder is the map.

Last updated: 2026-06-04.

---

## 1. What this system is

A file based "second brain" that runs Andy's outbound sales motion for OSI Global. It does four things:

1. **Finds and qualifies prospects** against OSI's product lines (optics, DWDM, compute/DIMMs, storage, TPM, networking gear, professional services).
2. **Writes personalized outreach** (multi email sequences and LinkedIn touches) in Andy's voice.
3. **Schedules and sends** that outreach, increasingly through HubSpot's cloud rather than the local queue.
4. **Monitors** what is in flight: bounces, replies, and follow up tasks.

Everything is plain files (Markdown, JSON, Excel) in one Git repository so it syncs across Andy's two laptops and is backed up privately on GitHub.

---

## 2. Repository layout

| Path | What lives there |
|---|---|
| `CLAUDE.md` | Master instructions and operating rules. Read first, every session. |
| `docs/` | This documentation. |
| `skills/` | All reusable skills (source folders) and their packaged `.skill` files. The heart of the system. See Section 4. |
| `knowledge/` | Sales playbook, company story, email pattern resolver, competitive intel. |
| `playbook/` | Drafting rules, voice rules, opener library, product lines, vertical intel, HubSpot data quality. Loaded by the drafting skills. |
| `accounts/` | Account level research and strategy notes. |
| `people/` | Contact and prospect summaries. |
| `outreach/` | Saved outreach drafts and sequences, organized by prospect. |
| `meetings/` | Meeting notes and prep. |
| `inbox/` | Drop zone for raw notes to be processed. |
| `sessions/` | End of session summaries, one per day (`session-YYYY-MM-DD.md`). |
| `scripts/` | Helper scripts (e.g. `validate_email.py`). |
| `BC/` | Brian Charrette's shared work area. Separate collaborator, separate skill set. See Section 7. |
| `tests/`, `test-prompts/` | Test prompts and fixtures for skills. |
| `Hubspot/`, `team-starter/` | Supporting data and onboarding material. |

### Key runtime files (repo root)

These are state files the skills read and write. They are Git versioned (manual sync) so both laptops stay consistent.

| File | Purpose |
|---|---|
| `email-queue.json` | The scheduled email queue. Legacy send path. Being migrated to HubSpot AI fields (Section 5). |
| `email-sender.lock` | Lock file the email sender uses to avoid double sends. |
| `hard-block.json` | Addresses and contacts that must never receive outreach. |
| `do-not-auto-prospect.json` | Companies excluded from Auto Mode prospecting. |
| `approved-vendors.json` | Vendors with special drafting language rules. |
| `holidays.json` | Non sending days for cadence math. |
| `overnight-candidates.json` | Candidate queue for the (now retired) overnight runner. |
| `reengagement-tracker.json` | State for cold and re engagement workflows. |
| `monitor-last-run.json` | Last run marker for the daily monitor. |
| `meeting-followup-state.json` | State for meeting follow up automation. |
| `prospects-tracker-new.xlsx` | Master Excel tracker. Includes the "Company Pipeline" and "Companies Prospected" tabs used by Auto Mode. |

Files ending in `.bak`, `.broken`, or with date stamps are historical backups. They are safe to ignore for normal work.

---

## 3. How a prospect moves through the system

The end to end flow, from a name to a sent email:

```
Discover  ->  Qualify  ->  Strategy note + LinkedIn task  ->  Draft sequence  ->  Schedule/send  ->  Monitor
(osi-prospect-     (same)        (HubSpot contact)            (osi-outreach-       (HubSpot AI       (osi-monitor)
 qualification)                                                sequence)            fields or queue)
```

1. **Discover.** Either a single LinkedIn profile (Profile Mode), a company ("find me prospects at X", Company Mode), or a cold account sweep (Auto Mode). Company Mode uses a locked four source discovery: HubSpot, ZoomInfo, LinkedIn browse, LinkedIn keyword, then dedupe.
2. **Qualify.** Verify current employer (LinkedIn first, ZoomInfo is enrichment only), apply the three point check (role, trajectory, skills), and return a Yes / No / Conditional verdict. No employer verification means no sequence.
3. **Write the contact.** On a Yes, write a strategy note to the HubSpot contact (including the SEQUENCE line and Personal Hook) and create a LinkedIn connect task. Ownership is checked first so JAM team accounts are respected.
4. **Draft.** `osi-outreach-sequence` reads the strategy note and drafts the full sequence, computing the Day 1 date from same company stagger metadata.
5. **Deliver.** Either written to HubSpot AI fields for cloud sending (the current direction) or appended to `email-queue.json` for the local sender (legacy). See Section 5.
6. **Monitor.** `osi-monitor` checks tasks, scans for bounces and replies, auto pauses sequences on any human reply, and flags anything needing Andy.

---

## 4. The skills

Skills are the reusable workflows. Each is a folder under `skills/[name]/SKILL.md` (the editable source of truth) plus a packaged `skills/[name].skill` file. Editing rules are in Section 6.

### Prospecting and qualification
- **osi-prospect-qualification** Qualifies LinkedIn prospects against OSI's product lines. Four modes: Profile (one URL), Company ("find me prospects at X"), Auto (cold account sweep from the pipeline tab), and Task Mode (batch process "Enroll in sequence" / "3 email sequence" to do tasks). Returns Yes / No / Conditional and hands Yes verdicts to the right outreach skill.
- **osi-job-change-prospecting** Weekly Sales Navigator workflow. Finds first degree connections who changed jobs or are new connections, qualifies them, and creates LinkedIn tasks.
- **osi-cold-reengagement** Finds cold first degree LinkedIn connections and creates two InMail tasks two weeks apart. No full sequence.

### Drafting and outreach
- **osi-outreach-sequence** Drafts and queues the full 6 email sequence for one qualified prospect. Owns stagger math, drafting, and the queue or AI field writes.
- **osi-3email-new** Shorter 3 email new outreach, for directors or lighter touch targets.
- **osi-3email-reengagement** 3 email re engagement for prospects who already completed a sequence months earlier.
- **osi-old-customer-reengagement** 5 email sequence to revive dormant past customers. Researches the account before writing.
- **osi-email2-rewriter** Redrafts pain led Email 2s in the queue before the morning send window.

### Sending and monitoring
- **osi-email-sender** Sends all due emails from `email-queue.json` via Outlook. Intended cadence: weekday late mornings through afternoon (legacy path).
- **osi-monitor** Daily sequence monitor. Checks tasks, bounces, and replies. Auto cancels on hard bounce, auto pauses on reply.
- **osi-email-task-drafts** Auto drafts reply emails for HubSpot email tasks due today or overdue.
- **osi-meeting-followup** Meeting follow up automation.

### Reporting and maintenance
- **andy-monthly-account-count** Tracks Andy's HubSpot account ownership over time and builds a dashboard.
- **osi-overnight-runner**, **osi-discovery-sweep** Batch orchestration skills (read by direct file path). The overnight runner is retired as of 2026-05-29.

Trigger phrases for each skill are in its `SKILL.md` frontmatter `description` and summarized in `CLAUDE.md`.

---

## 5. The outreach delivery migration (important)

There are two delivery paths, and the system is mid migration between them.

- **Legacy: local queue.** Emails are written to `email-queue.json` and sent from a laptop via Outlook by `osi-email-sender` on a schedule. The weakness: it depends on a laptop being on and the sender firing.
- **Current direction: HubSpot AI fields.** As of 2026-05-29, qualified emails are written directly into HubSpot contact AI fields (`ai_email_body_1` through `6`, `ai_email_subject_1` through `6`). Andy enrolls the contact in a HubSpot sequence, and HubSpot sends from the cloud with no laptop dependency. The LinkedIn connect task date is the cue telling Andy when to enroll.

When working outreach, confirm which path a given contact uses before assuming. New work favors AI fields.

---

## 6. Editing skills (redirect stub architecture)

The Cowork runtime does not hold real skill logic. It holds a one line redirect that tells Claude to read the live source at `C:\Claude-Brain\skills\[name]\SKILL.md` and run that. This makes runtime drift impossible by construction.

**To change a skill:** edit `skills/[name]/SKILL.md`. That is the live file. The runtime reads it on every fire. There is no force copy step.

**Do not** copy full skill content over a runtime stub. The stub is correct and should stay about 2 KB of redirect text. If a skill misbehaves, fix the source, not the runtime.

Repackaging the `.skill` zip is only needed to move a skill between machines or reinstall it. Note that the zip holds full content, so reinstalling from it can reintroduce drift until re stubbed.

Full detail and the incident history are in [CLAUDE.md](../CLAUDE.md) under "Skill Editing & Install Workflow".

---

## 7. Collaborators

- **Andy, Mark Metz, John Houston (JAM)** are one team. Accounts owned by Mark or John are fair game, never flagged as a conflict.
- **Brian Charrette (bc@osihardware.com)** has collaborator write access to this repository and works out of the `BC/` folder. Brian maintains his own parallel skill set under `BC/skills/` (his own owner ID and his own vault paths). Those skills are quarantined to `BC/` and should not trigger in Andy's sessions. Treat `BC/` as Brian's space.

---

## 8. Git and sync

This repo is the single source of truth, working copy at `C:\Claude-Brain\` on each laptop, backed up to the private GitHub repo `github.com/Drrewdy/Claude-Brain`.

- Pull before starting, push when finished. For `.xlsx` files: pull, edit, push immediately to avoid merge pain.
- **No auto git inside skills or scheduled tasks.** Skills read and write to disk only. Andy (or an interactive session) handles commit and push. This avoids stuck `.git/index.lock` files and log noise during unattended fires.
- A `.git/index.lock` left behind by a killed process is a known recurring issue on these machines. Removing it (`rm -f .git/*.lock`) when no git process is running is safe.

---

## 9. Operating rules that shape everything

These come from `CLAUDE.md` and are worth knowing before touching the system:

- **Read the relevant skill first**, every time, before any HubSpot, LinkedIn, or ZoomInfo call.
- **No approval prompts during scheduled fires.** If a tool would prompt during an unattended run, abort that step, log it, and move on.
- **No employer verification, no sequence.** Every candidate's current employer is verified before any verdict or write.
- **HubSpot first email resolution.** Search HubSpot before creating a contact or trusting a ZoomInfo address.
- **The Andy Rules:** keep responses under 100 words unless asked for more, keep technical specs and sales strategy in separate sections, write outreach as a human, and never use the em dash character.

When in doubt, `CLAUDE.md` wins over this document.
