---
name: osi-outreach-sequence
description: >
  Fully automated outreach sequence for OSI Global prospects. Sends 6 emails via Outlook
  (Email 1 at 4 PM ET, Email 2 at 11 AM, Email 3 at 12 PM, Email 4 at 1 PM, Email 5 at 2 PM,
  Email 6 at 3 PM — each email has its own dedicated window). Creates LinkedIn connection
  request task on Day 1. Runs in three modes: Interactive (Andy pastes one LinkedIn profile
  and reviews before sending), Company (Andy names companies, run overnight), or Auto
  (no companies named, Claude picks cold HubSpot companies owned by Andy with no activity
  6+ months). Overnight runs use a four-task-type pipeline: Kickoff schedules the work,
  Discovery tasks do LinkedIn candidate search per company, Processing batches qualify
  and fire up to 3 sequences every 2 hours, Wrap-up task writes the summary. Triggers on:
  "run a sequence", "outreach sequence", "build a sequence for", "run sequences for the
  following companies", "run sequences tonight", pasting a LinkedIn profile, or uploading
  a profile file. Always use this skill for new prospect outreach.
---

> **SYNC NOTE:** This skill exists in two locations: `C:\Claude-Brain\skills\osi-outreach-sequence\` (Git-versioned, source of truth, backed up at github.com/Drrewdy/Claude-Brain) and the local Cowork `.claude/skills/` mount. Any edits must go into `C:\Claude-Brain\skills\` and be pushed to GitHub. If returning after days away, run `git pull` first to get the latest, then check the local Cowork copy and re-install the `.skill` file if the source has drifted.

# OSI Global Outreach Sequence

---

## 🚦 WHO OWNS WHAT — read this first, every time

This skill works in tandem with **osi-prospect-qualification**. The boundary between them is strict. Never cross it.

| Responsibility | Owner skill |
|---|---|
| Qualify (verdict Yes / No / Conditional) | osi-prospect-qualification |
| Read the LinkedIn profile in full (About, Experience, Skills, activity / posts) | osi-prospect-qualification |
| Resolve LinkedIn URL from name+company when URL not provided | osi-prospect-qualification |
| Shallow qualify path for HubSpot-sourced contacts (title + ICP only) | osi-prospect-qualification |
| ZoomInfo enrichment (email, direct phone, mobile) | osi-prospect-qualification |
| Strategy note on HubSpot contact | osi-prospect-qualification |
| `LINKED_IN_CONNECT` task creation (provisional due_date) | osi-prospect-qualification |
| No-email-no-phone LinkedIn message fallback tasks | osi-prospect-qualification |
| Kickoff: write state file + schedule Discovery/Processing/Wrap-up tasks | **osi-outreach-sequence** (this skill) |
| Auto Mode cold-company selection (when no companies named) | **osi-outreach-sequence** (this skill) |
| Discovery task: LinkedIn candidate search for one or more companies | **osi-outreach-sequence** (this skill) |
| Processing batch: consume pending candidates, fire up to 3 sequences | **osi-outreach-sequence** (this skill) |
| Wrap-up task: Tab 2 Excel summary + session log | **osi-outreach-sequence** (this skill) |
| `LINKED_IN_CONNECT` task final due_date (match Email 1's Day 1) | **osi-outreach-sequence** (this skill) |
| Drafting the 6 emails | **osi-outreach-sequence** (this skill) |
| email-queue.json writes and scheduling | **osi-outreach-sequence** (this skill) |
| Same-company stagger math (from state metadata) | **osi-outreach-sequence** (this skill) |
| Active sequence check (prevent duplicate enrollment) | **osi-outreach-sequence** (this skill) |
| Excel tracker Tab 1 (Prospects) | **osi-outreach-sequence** (this skill) — appended per sequence |
| Excel tracker Tab 2 (Company Status) | **osi-outreach-sequence** Wrap-up task |

---

## 🛑 STOP IF NO EMAIL — this skill requires a valid email address

This skill drafts and schedules 6 emails via email-queue.json. No email means no sequence. If ZoomInfo did not return a valid email for this prospect, STOP immediately. Qualification's no-email-no-phone LinkedIn message fallback tasks are the complete plan in that case.

---

## RUN MODES — three ways a run starts

Modes describe how a run is triggered. Task types (next section) describe how any overnight run executes.

### Interactive Mode

Triggered by: Andy pastes a single LinkedIn profile URL, or says "build a sequence for [Name]", or a short multi-prospect prompt where Andy is present at the keyboard.

Bypasses the overnight pipeline entirely. Qualification runs live, this skill drafts 6 emails, Andy reviews and clicks send on Email 1, then Emails 2-6 are queued. One prospect at a time.

### Company Mode

Triggered by: "run sequences for the following companies: X, Y, Z" or similar multi-company overnight command.

Andy provides the company list. Kickoff writes those companies directly into the state file (`overnight-candidates.json`) with status `discovery_pending`. Discovery tasks, Processing batches, and Wrap-up run as scheduled.

### Auto Mode

Triggered by: "run sequences tonight" or "find me targets" with no specific company names.

No company list from Andy. Kickoff runs the cold-company selector:
1. Search HubSpot for companies with `hubspot_owner_id: 196669355` (Andy) where `notes_last_contacted` is 6+ months ago or never.
2. **Active client filter:** for each cold company, search HubSpot for closed-won deals or deals in an active pipeline stage. If a deal is found, skip the company. Do NOT use Lifecycle Stage (often wrong). Log the skip with reason: `SKIPPED: [Company] — active client (deal found: [deal name])`.
3. **OSI fit check:** confirm the company operates networking, telecom, data center, or IT infrastructure at relevant scale. Skip retail, food service, pure software, anything clearly outside OSI's ICP.
4. **Queue-prevent filter:** skip any company with pending entries in email-queue.json (already in an active sequence for another contact).
5. Rank remaining companies by OSI fit and pick the top N (default 3-4 for a one-night run, scalable up for multi-night runs).
6. Write the picked companies into the state file with status `discovery_pending`. From this point, Auto Mode proceeds identically to Company Mode — same Discovery → Processing → Wrap-up pipeline.

Auto Mode is overnight-only. Never runs during the daytime interactive flow.

---

## TASK TYPES — four distinct task types, each on its own clock

This is the core execution architecture used by both Company Mode and Auto Mode. Interactive Mode bypasses it.

### 1. Kickoff (in-session, Andy at keyboard, ~2 minutes)

Triggered by: any Company Mode or Auto Mode command. Runs in the foreground while Andy is present.

Kickoff does four things:
1. **Read leftover `overnight-candidates.json` if present.** Pending entries carry into tonight's run.
2. **Populate the company list.** In Company Mode, write Andy's pasted company list into the state file with status `discovery_pending`. In Auto Mode, run the cold-company selector (see Auto Mode section above) and write the selected companies into the state file.
3. **Schedule Discovery tasks** (grouped 3-4 companies per task) staggered 30-60 minutes apart at the start of the run.
4. **Schedule Processing batches** at 2-hour intervals across the overnight window, plus the Wrap-up task to fire 15 minutes after the last Processing batch.

Kickoff does NOT do LinkedIn candidate search. That happens in Discovery tasks. Kickoff also does NOT do HubSpot writes beyond the Auto Mode company selection queries. Andy approves each `create_scheduled_task` call once at kickoff, then walks away.

**Why this matters:** the old design crammed LinkedIn search into the in-session kickoff window. 17 companies × multiple keyword rounds × pagination = hours of browser work that never fit in 20 minutes. Discovery tasks solve that by moving heavy search to their own scheduled time slots.

### 2. Discovery task (scheduled, heavy token budget, one per 3-4 companies)

Each Discovery task receives a list of 3-4 company names in its prompt. It processes them sequentially:

For each company in its prompt:
1. **M&A check** — web search for recent acquisitions, rebrands. Update company name if needed.
2. **HubSpot ownership check** — apply JAM decision tree. Skip other-rep companies with recent activity. Log other-rep with 3+ months no activity for account-request. Proceed on JAM-owned or not-in-HubSpot.
3. **Regular LinkedIn candidate search** (NOT Sales Navigator — see qualification skill's TOOL CHOICE section). Run all keyword rounds: English priority titles, French keywords for Quebec companies, secondary titles if first round is thin. Paginate through every page of every search.
4. **Append candidates** to `overnight-candidates.json`. Each candidate entry: `{id, firstName, lastName, company, linkedinUrl (optional), source: "linkedin_search", status: "pending", addedDate}`.
5. **Append status line** to `Claude-Brain/overnight-run-log.md`: `[timestamp] Discovery [company] — N candidates found, M qualified titles, HubSpot ownership: [owner]`.
6. **Update company status** to `discovery_complete` in the state file.
7. Move to next company in the list.

Discovery tasks do NOT qualify, enrich, write strategy notes, or fire emails. They only produce the candidate list.

### 3. Processing batch (scheduled, LIGHT token budget, 3 sequences per fire)

Each Processing batch fires every 2 hours. Its token ceiling is the 3 Yes-with-email outreach sequences per batch — this constraint is hard and never expands.

On fire:
1. Open `overnight-candidates.json`. If missing OR zero pending candidates: write alert line to `overnight-run-log.md` (`[timestamp] BATCH N FIRED WITH EMPTY QUEUE`). Exit.
2. Take first candidate with status `pending`.
3. Invoke `osi-prospect-qualification` Profile Mode.
   - If candidate has `linkedinUrl`: use it directly.
   - If candidate has only `firstName` + `lastName` + `company` (no URL): qualification resolves the URL via LinkedIn search first, then proceeds.
   - If `source: "hubspot_contact"` and `hubspotContactId` present: qualification may take the shallow-qualify path (title + ICP check only).
4. Update candidate's status to one of `no`, `conditional`, `yes-no-email`, `yes-with-email`. Atomic write the state file.
5. Branch by verdict:
   - **No / Conditional:** STOP-GATE per qualification skill. No ZoomInfo, no HubSpot writes, no tasks. Return to step 2 for next candidate.
   - **Yes-no-email:** qualification creates 2 LI fallback tasks. Does NOT count toward 3 outreach slots. Return to step 2.
   - **Yes-with-email:** qualification writes strategy note + LINKED_IN_CONNECT task. Then this skill: calculate Email 1 Day 1 using same-company stagger from state metadata, update LINKED_IN_CONNECT due_date, append 6 emails to email-queue.json, append entry to prospects-tracker-new.xlsx Tab 1, update stagger metadata in state file. This counts as 1 of 3 slots.
6. Continue until 3 outreach sequences fire OR queue has no pending candidates.
7. Append status line to `overnight-run-log.md`: `[timestamp] Batch N — K outreach fired, L candidates evaluated, queue P pending`.
8. Exit.

### 4. Wrap-up task (scheduled, fires after last Processing batch)

One dedicated task. Runs once at end of overnight window.

1. Read `overnight-candidates.json` and `email-queue.json`.
2. Tally per-company: prospects found, verdicts, sequences fired.
3. Update `Claude-Brain/prospects-tracker-new.xlsx` Tab 2 (Company Status): one row per company for this run with Status (Completed / Partial / Not Started), Prospects Found, Sequences Created, Notes.
4. Write session log to `Claude-Brain/sessions/session-YYYY-MM-DD.md` summarizing the run: total candidates processed, total sequences fired, per-company breakdown, anything needing Andy's attention.
5. Leave remaining `status: "pending"` candidates in the state file untouched. They carry into the next run.
6. Append final status line to `overnight-run-log.md`.

Tab 2 summary lives in the Wrap-up task, not the last Processing batch. Keeping it separate means if a Processing batch fails or times out, the summary still gets written.

---

## STATE FILE SCHEMA — overnight-candidates.json

Path: `C:\Claude-Brain\overnight-candidates.json` (local, git-versioned).

```json
{
  "run_id": "2026-04-24-weekend",
  "created": "2026-04-24T17:00:00-04:00",
  "mode": "company",
  "companies": [
    {"name": "Midcontinent Communications, Inc.", "status": "discovery_pending"},
    {"name": "Lingo Communications", "status": "discovery_pending"},
    {"name": "Visionary Broadband", "status": "discovery_complete"}
  ],
  "candidates": [
    {
      "id": "john-lubeck-midcontinent",
      "firstName": "John",
      "lastName": "Lubeck",
      "company": "Midcontinent Communications, Inc.",
      "linkedinUrl": "https://www.linkedin.com/in/john-lubeck-abc123/",
      "source": "linkedin_search",
      "hubspotContactId": null,
      "status": "yes-with-email",
      "verdict_reason": "Director Core IP & Transport at cable MSO — DWDM fit",
      "addedDate": "2026-04-24",
      "processedDate": "2026-04-24"
    }
  ],
  "stagger": {
    "Midcontinent Communications, Inc.": {
      "last_day1": "2026-04-27",
      "person_count": 1
    }
  },
  "log": {
    "discovery_runs": [
      {"taskId": "discovery-a", "fired": "2026-04-24T18:00:00-04:00", "companies": ["Midco", "Lingo"], "candidates_added": 23}
    ],
    "processing_runs": [
      {"taskId": "batch-1", "fired": "2026-04-24T21:30:00-04:00", "sequences_fired": 0, "empty_queue": true}
    ]
  }
}
```

**`mode`:** `"company"` | `"auto"` — records which mode kicked off the run. Informational.

**Company statuses:** `discovery_pending` → `discovery_complete`. No further change; candidates carry their own status.

**Candidate statuses:** `pending` → one of `no`, `conditional`, `yes-no-email`, `yes-with-email`, `skipped-active-sequence`, `pending-retry`.

**Stagger metadata** (`stagger[company_name]`):
- `last_day1`: ISO date of the most recent Email 1 Day 1 scheduled for this company in this run.
- `person_count`: how many Yes-with-email sequences scheduled at this company so far. Determines whether the next stagger gap is 4 biz days or the 10-biz-day cooling gap at person 6.

**Candidate source values:**
- `linkedin_search`: discovered via LinkedIn people search in a Discovery task. Full deep qualify required.
- `hubspot_contact`: pulled from HubSpot with verified email + title + company. Eligible for shallow qualify path.

**Atomic writes — apply to every write of this file or email-queue.json:** always write to `.tmp` then `os.replace`. Never delete-then-write; that leaves a window where the file doesn't exist and any concurrent read gets a missing-file error.

---

## FAILURE MODES — explicit, loud, never silent

### Queue file missing or unreadable
Processing batch: write alert line to `overnight-run-log.md`: `[timestamp] BATCH N — queue file missing or unreadable at [path]`. Exit.
Discovery task: create the file with empty candidates array, then proceed.

### Queue has zero pending candidates
Processing batch: write alert line: `[timestamp] BATCH N — empty queue (N total, 0 pending)`. Exit. Do NOT silently exit.

### LinkedIn unreachable or rate-limited
Discovery task: log the failure, move to next company in its list. Do not block subsequent companies.
Processing batch: if qualification fails to read a profile after retry, mark candidate `conditional` with reason, move on. Next batch may retry.

### ZoomInfo returns no data for a Yes verdict
Qualification handles this — marks candidate `yes-no-email`, creates 2 LI fallback tasks. Does not count toward outreach slots. Processing batch continues.

### HubSpot write fails on strategy note or task
Log the failure, mark candidate `yes-with-email-hubspot-incomplete` with reason. Still queue the 6 emails (email-queue.json is the authoritative outreach record). Surface in wrap-up for Andy to review.

### Discovery task aborts mid-company
Company's status stays `discovery_pending`. Next Discovery task in the chain retries it (or a manual re-fire can target just that company).

### Chrome not responsive in scheduled session
Retry once after 30s. If still broken, log alert line and exit. Next batch fires clean.

**The rule:** every failure writes a line to `overnight-run-log.md` with timestamp, task ID, and reason. No silent exits. If Andy opens that file Monday morning, he sees the full run history.

---

## MID-RUN COMPANY ADDITIONS

If Andy pastes additional companies during an active overnight run:

1. Append new companies to `companies[]` array in `overnight-candidates.json` with status `discovery_pending`.
2. Schedule a new Discovery task for them (grouped 3-4 per task) to fire in the next available discovery slot before Monday morning.
3. Their candidates enter the same queue and get picked up by subsequent Processing batches automatically.

The state file is the source of truth. If a company isn't in `overnight-candidates.json`, it doesn't get processed.

---

## Andy Rules — apply to every output

### Voice and tone
- Tone: peer-to-peer, not vendor-to-buyer. Andy reaches out as Andy, not as a company.
- Emails are short. Mobile-friendly. Scannable in 10 seconds.
- Keep prose tight and direct. No fluff.

### Sign-off
- Do NOT type "Andy" or any name at the bottom of the email body. Outlook's signature block handles the sign-off automatically. Typing a name manually creates a doubled sign-off when Outlook appends the signature.
- This applies to every email in the sequence, including Email 1 and the breakup.

### Humanization ruleset — final-pass filter before any email is saved to the queue
Run every draft through this list and rewrite anything that fails:

- **Banned AI vocabulary:** remove "crucial", "pivotal", "landscape", "underscore", "delve", "showcase", "testament", "enhance", "foster", "garner". Replace with plain alternatives or cut the sentence.
- **No hyphens** in email bodies or subject lines. Rewrite "end-of-life" as "end of life", "24-hour" as "24/7/365", "third-party" as "third party".
- **No em-dashes (—)** anywhere. Not once. Split into two sentences if needed.
- **No rule of three.** Break any three-item list into natural prose.
- **No "-ing" pile-up** at sentence tails. Kill trailing participial clauses like "highlighting our advantage", "ensuring uptime", "reflecting market shifts", "contributing to cost savings".
- **No negative parallelisms.** Remove "it's not just X, it's Y" constructions.
- **Vary sentence length.** Mix short punchy sentences with longer ones.
- **Use "is / are / has"** instead of "serves as", "stands as", "functions as".
- **Final read-aloud check.** Mentally read each email aloud. If it sounds like a press release or a vendor pitching, rewrite it. It should sound like one person emailing another.

Any email that fails any of the above gets rewritten before it is saved or scheduled.

---

## Approved Vendor Rule — read list from Claude-Brain file

OSI is an approved vendor at a list of accounts maintained in `Claude-Brain/approved-vendors.json`. Read that file at sequence-build time (plain Python: `open(path,'r')`) and check if the prospect's company matches any entry (case-insensitive substring match, e.g. "Desjardins Group" matches "Desjardins").

**If the prospect's company matches an approved-vendor entry:**
- **Email 1:** Include ONE line acknowledging approved-vendor status. Soft, peer-to-peer phrasing. Examples:
  - "Side note, we're already on your approved vendor list, so no new vendor onboarding if anything ever needs to move fast."
  - "For context, we're an approved vendor at [Company] already, so standing up a PO is painless if it comes to that."
- **ONE other email — Email 3 or Email 4 — Claude picks whichever fits the narrative:** Brief reminder. One line. Example: "Quick reminder we're already approved at [Company] if timing matters."
- **All other emails:** Do NOT mention approved-vendor status.

**If the prospect's company does NOT match the approved-vendor list:**
- Do NOT mention approved-vendor status anywhere in the sequence. Do not invent it.

**Phrasing rules:**
- Never "vetted" or "pre-approved". "Approved vendor" is the term.
- Never mention "procurement" in Email 1. Telegraphs the sales motion. Just note we're on the list.

To add a company to the approved-vendor list, Andy edits `Claude-Brain/approved-vendors.json` directly.

---

## Active Sequence Check — hard stop before anything else

Before any other work on this prospect, check the email queue. This prevents stacking duplicate sequences on the same person, which wrecks sender reputation and is bad form.

Open `C:\Users\Andy\OneDrive - OSI Hardware\Claude-Brain\email-queue.json` using plain Python `open(path,'r')`. Scan every entry for a match:

- Match by `to` field equal to the prospect's email address (case-insensitive), OR
- Match by `prospectName` + `company` both matching the prospect's full name and company (case-insensitive)

**SKIP this prospect entirely if any matched entry has:**
- `status: "pending"` (already enrolled in an active sequence), OR
- `status: "sent"` with a `sendDate` within the last 30 calendar days (sequence recently completed)

Entries with status `paused-*`, `canceled-*`, or older `sent` (>30 days ago) do NOT block. Proceed normally, but note in the strategy note that a prior sequence completed on [date] so this run is effectively a re-engagement.

**Skip behavior by mode:**
- **Interactive mode:** Tell Andy: `SKIPPED: [First Last] at [Company] — [reason]. Override?`. Wait for explicit "override" before proceeding.
- **Processing batch:** skip silently. Log to `overnight-run-log.md` with reason. Mark candidate status `skipped-active-sequence`. Continue to next candidate.

This check runs BEFORE qualification starts any deeper research. Fail fast and cheap.

---

## OUTREACH FLOW — what a Yes-with-email sequence looks like

This is the work done per Yes-with-email prospect, inside a Processing batch or in Interactive Mode. Qualification has already done its job (verdict, strategy note, LINKED_IN_CONNECT task, call script, VM, LinkedIn invite).

### Step 1: Determine Sequence Type

Based on role, title, and company vertical — pick one:

| Sequence | Target roles | Lead angle |
|---|---|---|
| Network | Network Engineer, Architect, Transport Engineer | Free SFP sample |
| Server | Systems Engineer, Infrastructure Engineer, Server Admin | Free DIMM sample |
| TPM | IT Director, DC Manager, IT Asset Manager, Procurement, CIO mid-market | OEM cost pain |
| DWDM | Transport Engineer, Optical NE, Network Planner at carrier/CLEC/MSO | Cost vs Ciena/Nokia |
| Storage | Storage Admin, Storage Engineer | Pre-owned NetApp + TPM |
| Pre-owned | Anyone managing Cisco/Juniper/Arista environments | Pre-owned gear + OSI TPM |

**Calls sequence label** (for the strategy note header): Call - Network / Call - Server / Call - TPM / Call - DWDM / Call - Storage / Call - Networking

### Step 2: Calculate Dates — same-company stagger from state metadata

Open `overnight-candidates.json`. Read `stagger[company_name]`:
- `last_day1`: ISO date of the most recent Day 1 scheduled for this company in this run.
- `person_count`: how many Yes-with-email sequences scheduled at this company so far.

Set this candidate's Day 1:
- `person_count == 0` (first person at this company this run): Day 1 = next business day after today.
- `person_count` in 1-4 (persons 2-5 at same company): Day 1 = `last_day1` + 4 business days.
- `person_count == 5` (person 6): Day 1 = `last_day1` + 10 business days. Cooling gap for receiving domain rolling-velocity.
- `person_count >= 6` (persons 7+): Day 1 = `last_day1` + 4 business days. Return to normal cadence.

After scheduling, update state metadata:
- `stagger[company_name].last_day1` = this person's Day 1
- `stagger[company_name].person_count += 1`

**Why read from state file, not email-queue:** the email queue has 500+ entries. Scanning every time is slow. State metadata is O(1) and cares about THIS run's scheduled Day 1s.

### Day 1 + cadence

Each email has its own dedicated send window:

| Email | sendTime | Window |
|---|---|---|
| 1 | `4pm` | 4 PM Eastern |
| 2 | `11am` | 11 AM Eastern |
| 3 | `12pm` | 12 PM Eastern |
| 4 | `1pm` | 1 PM Eastern |
| 5 | `2pm` | 2 PM Eastern |
| 6 | `3pm` | 3 PM Eastern |

The master osi-email-sender task runs every weekday at 11 AM, 12 PM, 1 PM, 2 PM, 3 PM, and 4 PM Eastern. Each fire processes queue entries whose `sendTime` matches that window.

**Full cadence:**

| # | Send date | Gap from prior |
|---|---|---|
| 1 | Day 1 | — |
| 2 | 2 business days after Email 1 actual send | +2 bd |
| 3 | 4 business days after Email 2 actual send | +4 bd |
| 4 | 6 business days after Email 3 actual send | +6 bd |
| 5 | 5 business days after Email 4 actual send | +5 bd |
| 6 | 6 business days after Email 5 actual send | +6 bd |

Total sequence length: 23 business days from Email 1 Day 1 to Email 6, assuming no slips.

**Self-healing cadence — each email anchors to prior email's ACTUAL send date, not Email 1's planned date.** When the sender fires Email N, it updates Email N+1's `sendDate` in the queue to `N biz days after today`. If Email 1 slips a day because the 4 PM window was missed, Email 2 automatically shifts a day later.

**Skip weekends AND holidays on every send date, including Day 1.** Holiday list lives in `Claude-Brain/holidays.json` — read at runtime, do not hardcode. If the file is missing, fall back to the standard US federal holidays plus Good Friday, Black Friday, Christmas Eve, New Year's Eve.

Plus: LinkedIn connection request task due Day 1 (also skip weekends/holidays).

### Step 3: Write All 6 Emails

#### Email 1 (Day 1) — 1st Touch

**Network sequence:**
> Hi [First Name],
>
> I'm just prepping this package for you. I have a box of swag and a pair of sample SFPs to send from the team at OSI Global.
>
> Do you come into the office, or is there a better address to ship it to?

**Server sequence:**
> Hi [First Name],
>
> I'd like to send you a sample DIMM from our current batch. Same spec as what you're running, manufacturer warranty, won't touch your OEM support contract.
>
> Do you come into the office, or is there a better address to ship it to?

(No name at the end of either template. Outlook signature handles the sign-off.)

**TPM / DWDM / Storage / Pre-owned — pain-led opener:**
Short. 3-4 sentences max. Lead with their specific pain based on role and company. Reference the Personal Hook. One clear ask at the end. No corporate speak. No "Andy" at the bottom.

Subject line: Short, specific, not flaggable as spam. You decide based on the target.

#### Email 2 (2 bd after Email 1 actual send) — Sequence Email

Subject: RE: [same subject as Email 1]

Content branches by Email 1 archetype:

- **Archetype A — sample-offer Email 1** (body contains "sample", "swag", or shipping address question): Body is literally "Any thoughts?" — nothing else.
- **Archetype B — pain-led Email 1**: Body is 2-3 sentences. Do NOT repeat Email 1's argument. Pick ONE move: new data point on the same pain, adjacent pain on a related OSI product line, or company signal that surfaced since Email 1. End with ONE concrete ask.

Quote Email 1 below in standard reply format. No greeting. No sign-off.

#### Email 3 (4 bd after Email 2 actual send) — Sequence Email

New subject line. Different angle from Email 1. Introduce a relevant pain point or OSI product line not covered in Email 1. Short. 3-4 sentences. One ask. Quote Email 2 below.

#### Email 4 (6 bd after Email 3 actual send) — Sequence Email

New subject line. Different OSI product line. Short. 3-4 sentences. One ask. Quote Email 3.

#### Email 5 (5 bd after Email 4 actual send) — Sequence Email

New subject line. Another OSI product line not yet covered. Short. 3-4 sentences. One ask. Quote Email 4.

#### Email 6 (6 bd after Email 5 actual send) — Breakup

New subject line. Clean close. No ask. One sentence. Examples:
- "Should I close the file on this one, or is the timing just off?"
- "No worries if now isn't the right time. Happy to circle back when things shift."

Quote Email 5.

### Step 4: Present for Review (Interactive Mode only — skip in Processing batch)

Present all 6 emails with subject lines, call script, voicemail, LinkedIn invite, and proposed schedule as a table.

End with: "Look it over and say **ready** when you want to send."

Stop. Do not open Outlook until Andy says ready.

### Step 5: Send and Schedule

**Interactive Mode on "ready":** Open Outlook in Chrome with Email 1 pre-composed:
1. Navigate to https://outlook.office.com
2. If login screen appears, stop and notify Andy
3. Click New mail
4. Enter prospect's email in To field, press Tab
5. Enter subject line exactly
6. Click in body above signature, type email body exactly as written
7. Do NOT click Send. Leave pre-composed for Andy.

Tell Andy: "Email 1 is ready in Outlook. Click Send when you're good, then say **sent** and I'll schedule the rest."

When Andy says "sent": confirm, then schedule Emails 2-6 via email-queue.json.

**Processing batch:** Append all 6 emails directly to email-queue.json. No Outlook step.

### email-queue.json entry format

Path: `C:\Users\Andy\OneDrive - OSI Hardware\Claude-Brain\email-queue.json`

```json
{
  "id": "[firstname]-[lastname]-[company-slug]-[N]",
  "prospectName": "[First Last]",
  "company": "[Company]",
  "to": "[email address]",
  "subject": "[subject line exactly]",
  "body": "[full email body including quoted thread — preserve all line breaks]",
  "sendDate": "[YYYY-MM-DD]",
  "sendTime": "[4pm / 11am / 12pm / 1pm / 2pm / 3pm]",
  "status": "pending",
  "addedDate": "[today YYYY-MM-DD]"
}
```

### How to write to the queue (atomic pattern — same as state file)

```python
import json, os

QUEUE = r'C:\Users\Andy\OneDrive - OSI Hardware\Claude-Brain\email-queue.json'

with open(QUEUE, 'r') as f:
    queue = json.load(f)

new_entries = [ ... ]  # array of entry dicts

existing_ids = {e.get("id") for e in queue}
to_add = [e for e in new_entries if e["id"] not in existing_ids]
queue.extend(to_add)

tmp = QUEUE + '.tmp'
with open(tmp, 'w') as f:
    json.dump(queue, f, indent=2)
os.replace(tmp, QUEUE)
```

Do NOT use the MCP Write tool for the queue (its prior-Read requirement breaks on large cloud-synced files).

### Respread / reschedule — sync BOTH layers

Any time you touch an already-queued prospect's emails to change dates or times, you MUST also update any matching per-email scheduled tasks in the Cowork scheduler.

1. Call `mcp__scheduled-tasks__list_scheduled_tasks` and filter for taskIds starting with the prospect's prefix.
2. For every matching task with a future `fireAt`, compare against the queue's new `sendDate` + `sendTime`. If they differ, call `mcp__scheduled-tasks__update_scheduled_task` with corrected `fireAt` in ISO 8601 with ET offset.
3. Leave already-disabled tasks alone.
4. If no per-email tasks exist, skip. The master sender handles the queue on its own fire windows.
5. Re-list and diff at the end of the respread. Log any leftover drift.

### Step 6: Update LINKED_IN_CONNECT task due_date + state metadata

After Email 1's final Day 1 is locked in:

1. **Find the existing `LINKED_IN_CONNECT` task** on the HubSpot contact (qualification created it with provisional due_date). Call `manage_crm_objects` updateRequest and set `hs_timestamp` to Email 1's Day 1. This is the ONLY HubSpot write this skill performs.
2. **Update state metadata** in `overnight-candidates.json`: set `stagger[company_name].last_day1` = this prospect's Email 1 Day 1. Increment `stagger[company_name].person_count`. Atomic write.

### Step 7: Append to Excel tracker Tab 1

File: `Claude-Brain/prospects-tracker-new.xlsx`, Tab 1 — Prospects.

Append one row per person:

Columns: Name | Title | Company | LinkedIn URL | OSI Angle | HubSpot Status | Action | Date Added | Notes

Tab 2 (Company Status) is the Wrap-up task's job. Do NOT touch Tab 2 from a Processing batch.

---

## OSI Product Lines

1. **Optics** — SmartOptics transceivers, private-labeled. Sample offer is the opening wedge.
2. **DWDM and Open Line Systems** — SmartOptics DCP platform, 30-50% below Ciena/Nokia. Ships fast.
3. **Compute and Components** — DIMMs from Samsung/Hynix/Micron. Lead with DIMMs.
4. **Storage** — NetApp TPM, pre-owned storage.
5. **TPM** — 40-60% below OEM. Multi-vendor. Gartner-recognized, privately owned, no PE.
6. **Pre-Owned and New Networking** — Pre-owned Cisco/Juniper/Arista. New Nokia authorized.
7. **Professional Services** — Strong signal only. Never lead cold.

---

## Vertical Intelligence

### Telco and Service Providers
Lead with optics. Do NOT open with free SFPs. Lead with supply chain reliability. TPM rarely the opener at engineer level.

### Large Banks and Financial Institutions
Lead with optics. Free SFP offer works. Do NOT lead with TPM. If known TPM provider, use Park Place/Service Express merger wedge.

### Professional Services and Consulting
TPM viable opener. Lead with pain not price. Free optics also works.

### Manufacturing
Free optics as break-glass insurance. TPM for aging Cisco gear.

### Healthcare
TPM with documented SLAs. DIMMs for server refresh. Gartner-recognized, privately owned, no PE matters here.

---

## TPM Positioning

**Unknown if they have TPM:**
- Banks: optics opener, TPM is second conversation
- Consulting: TPM can open, lead with pain not savings %
- Manufacturing/enterprise: TPM strong, aging gear and OEM end-of-life is the hook

**Known TPM provider (Park Place, Service Express, Curvature):**
Merger wedge: "With the Park Place and Service Express merger, a lot of teams have been taking a fresh look at their TPM relationships. Have you had a chance to renegotiate since the merger, or are you still on the same rates?"

---

## DWDM / SmartOptics Talking Points

- Cost: 30-50% below Ciena and Nokia. Minimal licensing fees.
- Space and power: significant reduction vs. traditional DWDM platforms.
- Simplicity: easier to deploy and manage.
- Lead times: ships faster than OEMs.
- Pedigree: backed by original engineering core. Not grey market.

---

## Cold Call Opener Rules

1. Open with "How have you been?" — 6.6x baseline meeting rate.
2. State a clear reason for calling.
3. End with a question about their world. Never "Is now a good time?"
4. Never ask "Is now a good time?"
5. Voicemails: 15 seconds max. No phone number. End with Andy's email address spelled audibly ("that's andy at osiglobal dot com"). Always present or future tense. Never past tense.

---

## PROMPT TEMPLATES — for scheduled tasks

### Kickoff prompt (runs in-session, Andy at keyboard)

```
You are running Kickoff for an overnight OSI Global outreach run. Do NOT do LinkedIn search, qualification, or outreach here. Only schedule the work.

1. Read existing C:\Claude-Brain\overnight-candidates.json if present. Preserve pending candidates.

2. Populate the company list:
   - If Andy provided companies: write them into the state file with status "discovery_pending".
   - If Auto Mode (no companies named): run the cold-company selector — HubSpot search for owner 196669355 with notes_last_contacted 6+ months ago, apply active-client filter + OSI fit check + queue-prevent filter, pick top N, write to state file.

3. Write/update overnight-candidates.json with run_id, mode ("company" or "auto"), companies array, candidates array (preserving pending), and empty stagger metadata.

4. Schedule Discovery tasks (3-4 companies each, staggered 30-60 min apart at run start).

5. Schedule Processing batches at 2-hour intervals across the overnight window.

6. Schedule the Wrap-up task to fire 15 min after the last Processing batch.

7. Report to Andy: state file created, N Discovery tasks scheduled, M Processing batches scheduled, 1 Wrap-up task scheduled.
```

### Discovery task prompt template

```
You are running an OSI Global Discovery task. Process this list of companies sequentially:

COMPANIES: [Midcontinent Communications, Inc., Lingo Communications, Visionary Broadband, Cincinnati Bell]

Read C:\Claude-Brain\skills\osi-outreach-sequence\SKILL.md "Discovery task" section first.

For each company:
1. M&A check (web search for rebrand / acquisition).
2. HubSpot ownership check. Apply JAM decision tree. Skip other-rep companies with recent activity.
3. Regular LinkedIn candidate search (NOT Sales Navigator). All keyword rounds: English priority, French for Quebec companies, secondary titles if thin. Paginate every page.
4. Append candidates to C:\Claude-Brain\overnight-candidates.json with status "pending". Fields: id, firstName, lastName, company, linkedinUrl (if found), source: "linkedin_search".
5. Append status line to C:\Claude-Brain\overnight-run-log.md.
6. Update company status to "discovery_complete" in state file.

Do NOT qualify, enrich, or fire outreach. That's Processing batches' job.
```

### Processing batch prompt template

```
You are running Processing Batch N of M for an OSI Global overnight run.

Read C:\Claude-Brain\skills\osi-prospect-qualification\SKILL.md and C:\Claude-Brain\skills\osi-outreach-sequence\SKILL.md first.

Execute:
1. Open C:\Claude-Brain\overnight-candidates.json. If missing OR zero pending candidates: append alert line to C:\Claude-Brain\overnight-run-log.md and exit.
2. Take first pending candidate.
3. Invoke qualification Profile Mode (accepts linkedinUrl or name+company or hubspot_contact source).
4. Update candidate status atomically.
5. Branch on verdict. Yes-with-email: apply same-company stagger from state metadata, update LINKED_IN_CONNECT due_date, append 6 emails to C:\Users\Andy\OneDrive - OSI Hardware\Claude-Brain\email-queue.json, append row to Tab 1 of prospects-tracker-new.xlsx, update stagger metadata in state file.
6. Continue until 3 outreach sequences fire OR queue has no pending.
7. Append status line to overnight-run-log.md.
```

### Wrap-up task prompt template

```
You are running the Wrap-up task for an OSI Global overnight run.

Read C:\Claude-Brain\skills\osi-outreach-sequence\SKILL.md "Wrap-up task" section first.

1. Read C:\Claude-Brain\overnight-candidates.json and C:\Users\Andy\OneDrive - OSI Hardware\Claude-Brain\email-queue.json.
2. Tally per-company: prospects found, verdicts, sequences fired.
3. Update C:\Claude-Brain\prospects-tracker-new.xlsx Tab 2 (Company Status).
4. Write session log to C:\Claude-Brain\sessions\session-YYYY-MM-DD.md.
5. Leave pending candidates in state file untouched for next run.
6. Append final status line to overnight-run-log.md.
```
