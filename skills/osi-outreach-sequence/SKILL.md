---
name: osi-outreach-sequence
description: >
  Outreach sequence skill for OSI Global. Sends 6 emails via Outlook (Email 1 at 4 PM ET,
  Email 2 at 11 AM, Email 3 at 12 PM, Email 4 at 1 PM, Email 5 at 2 PM, Email 6 at 3 PM).
  Creates a LinkedIn connection request task on Day 1. Three modes: Interactive (Andy
  pastes one LinkedIn profile and reviews live), Company (Andy names companies, run
  overnight), or Auto (no companies, Claude picks cold HubSpot companies owned by Andy
  with 6+ months no activity). Overnight runs use a single recurring task that fires
  hourly and routes itself between Discovery and Processing. Triggers on: "run a sequence",
  "outreach sequence", "build a sequence for", "run sequences for the following companies",
  "run sequences tonight", pasting a LinkedIn profile, or uploading a profile file.
---

> Source: `C:\Claude-Brain\skills\osi-outreach-sequence\` (Git, github.com/Drrewdy/Claude-Brain). Cowork `.claude/skills/` is a copy. Edit source, repackage, install.

# OSI Global Outreach Sequence

---

## 🚦 WHO OWNS WHAT

Strict boundary with **osi-prospect-qualification**.

| Responsibility | Owner |
|---|---|
| Verdict (Yes / No / Conditional), profile read, URL resolution, shallow qualify, ZoomInfo enrichment, strategy note, LINKED_IN_CONNECT task creation, no-email LI fallback tasks | qualification |
| Kickoff (write state file + schedule recurring runner) | this skill |
| Auto Mode cold-company selection | this skill |
| Recurring runner (hourly: Discovery, Processing, or Wrap-up) | this skill |
| Drafting 6 emails, email-queue.json writes, same-company stagger from state metadata | this skill |
| Active sequence check (prevent duplicates) | this skill |
| LINKED_IN_CONNECT task final due_date (match Email 1 Day 1) | this skill |
| Excel tracker Tab 1 (per-prospect) and Tab 2 (per-company, in wrap-up phase) | this skill |

---

## 🛑 STOP IF NO EMAIL

This skill drafts 6 emails. No email = no sequence. If ZoomInfo returned no valid email, STOP. Qualification's 2 LI fallback tasks are the complete plan.

---

## RUN MODES

### Interactive Mode
Andy pastes one LinkedIn profile or "build a sequence for [Name]". Live, in-session. Qualification → this skill drafts 6 emails → Andy "ready" → Outlook composes Email 1 → Andy clicks Send → "sent" → Emails 2-6 queue.

### Company Mode
"run sequences for the following companies: X, Y, Z". Andy's list goes into the state file with status `discovery_pending`. Recurring runner picks up.

### Auto Mode
"run sequences tonight" with no companies. Kickoff runs cold-company selector:
1. HubSpot search: `hubspot_owner_id: 196669355`, `notes_last_contacted` 6+ months ago or null.
2. **Active client filter:** skip any with closed-won deals or active pipeline stage. Do NOT use Lifecycle Stage. Log skips: `SKIPPED: [Company] — active client (deal: [name])`.
3. **OSI fit check:** keep companies in networking, telecom, data center, or IT infrastructure at relevant scale. Skip retail, food service, pure software.
4. **Queue-prevent filter:** skip any with pending entries in email-queue.json.
5. Rank by OSI fit, pick top N (default 3-4 per night).
6. Write to state file with `discovery_pending`. Then proceed identically to Company Mode.

Auto Mode is overnight-only.

---

## ARCHITECTURE — two tasks, separate concerns

Overnight = exactly two scheduled tasks:

1. **Discovery Mega** — ONE-TIME, fires once at kickoff. Hits ALL companies in a single fire. Heavy token. All candidates land in the queue. Then disables itself.
2. **Processing Recurring** — fires every 2 hours. PURE Processing only. 3 sequences per fire. Light token, predictable. Runs until queue drains, then idles in wrap-up.

Two tasks = two approval pools. Andy approves LinkedIn / HubSpot / ZoomInfo / Chrome ONCE on each task's first fire. All subsequent fires reuse.

**Why split:** Discovery is bursty (one company = many candidates). Processing is steady (3 sequences/fire). Mixing them means Processing competes with Discovery for token budget and the backlog grows faster than it drains. Splitting keeps each task's load predictable.

### Kickoff (in-session, ~2 minutes)

Triggered by Company or Auto Mode command. Andy at keyboard.

1. Read existing `C:\Claude-Brain\overnight-candidates.json`. Preserve pending entries.
2. Populate company list:
   - **Company Mode:** Andy's named list, all marked `discovery_pending`.
   - **Auto Mode:** run cold-company selector (HubSpot owned by Andy + 6+ months no activity + active-client filter + OSI fit check + queue-prevent filter), pick top **5** companies, mark `discovery_pending`.
3. Schedule **Discovery Mega** as a one-time task firing in 2-5 minutes (or immediately via Run now).
4. Schedule **Processing Recurring** as a recurring task, cron `0 */2 * * *` (every 2 hours, fires :00 of every other hour).
5. Done. Andy approves both schedule calls.

Kickoff does NOT do LinkedIn search, qualification, or outreach.

### Discovery Mega — one-time, all companies in one fire

Prompt template:

```
You are running OSI Discovery Mega. Process ALL companies with status discovery_pending in C:\Claude-Brain\overnight-candidates.json.

Read C:\Claude-Brain\skills\osi-outreach-sequence\SKILL.md and C:\Claude-Brain\skills\osi-prospect-qualification\SKILL.md first.

For EACH discovery_pending company in sequence:
1. M&A check (web search for rebrand / acquisition).
2. HubSpot ownership check (JAM tree).
3. Regular LinkedIn candidate search (NOT Sales Nav). All keyword rounds, paginate every page. For HubSpot-rich accounts (existing customers / SQL leads with 8+ contacts), shortcut: pull strong-fit HubSpot contacts as source `hubspot_contact` instead of LinkedIn search — saves time, leverages curation.
4. Append candidates to state file with status pending. Atomic write (.tmp + os.replace).
5. Update company status to discovery_complete.
6. Append status line to C:\Claude-Brain\overnight-run-log.md.

When ALL companies marked discovery_complete, exit. Do NOT do Processing — that's the recurring task's job.

Failure modes per skill: log to overnight-run-log.md, never silent. If a single company errors, log + skip + move on. Other companies still get done.
```

Token budget: heavy by design. Generous ceiling — Discovery Mega's whole job is one big concentrated burst.

### Processing Recurring — every 2 hours, 3 sequences per fire

Prompt template:

```
You are the OSI Processing Recurring runner. Fires every 2 hours. ONE TASK = ONE APPROVAL POOL.

Read C:\Claude-Brain\skills\osi-outreach-sequence\SKILL.md and C:\Claude-Brain\skills\osi-prospect-qualification\SKILL.md first.

Open C:\Claude-Brain\overnight-candidates.json. If missing: log alert to overnight-run-log.md, exit.

PRIORITY (top to bottom):

1. PROCESSING (any candidate status pending):
   - Take first pending candidate.
   - Invoke qualification Profile Mode (accepts linkedinUrl OR name+company OR hubspot_contact source).
   - Update candidate status atomically: no / conditional / yes-no-email / yes-with-email.
   - Branch:
     - No / Conditional: STOP-GATE per qualification. Continue.
     - Yes-no-email: qualification creates 2 LI fallback tasks. Doesn't count toward 3-slot limit. Continue.
     - Yes-with-email: qualification writes strategy note + LINKED_IN_CONNECT task. Then this skill: same-company stagger from state metadata, append 6 emails to email-queue.json, append Tab 1 row, update LINKED_IN_CONNECT due_date, increment stagger metadata. Counts as 1 of 3.
   - Continue until 3 outreach sequences fire OR no pending candidates remain.
   - Log status line. Exit.

2. WRAP-UP (no candidates pending — Discovery Mega has done its job and Processing has drained the queue):
   - Update Tab 2 of prospects-tracker-new.xlsx with per-company summary.
   - Final status line to overnight-run-log.md.
   - Exit clean. Future fires also exit on wrap-up until new work added.

Note: this runner does NOT do Discovery. If new companies are added mid-run with discovery_pending status, Andy must schedule a new Discovery Mega manually (or run Kickoff again).

Token ceiling: 3 outreach sequences per fire. Hard limit. Finish current candidate cleanly and exit if approaching.

Failure modes per skill: log to overnight-run-log.md, never silent. Retry once on transient failures.
```

Cron: `0 */2 * * *` — every 2 hours at :00 (Cowork adds ~9 min jitter).

### JAM ownership decision tree
- Not in HubSpot → proceed.
- Owned by Andy 196669355 / Mark 210187184 / John 210187193 → proceed.
- Other rep, last activity within 3 months → skip silent.
- Other rep, no activity 3+ months → log for account-request, do NOT prospect.

---

## STATE FILE — overnight-candidates.json

```json
{
  "run_id": "2026-04-24-weekend",
  "mode": "company",
  "companies": [{"name": "Midcontinent Communications, Inc.", "status": "discovery_pending"}],
  "candidates": [{
    "id": "john-lubeck-midcontinent",
    "firstName": "John", "lastName": "Lubeck",
    "company": "Midcontinent Communications, Inc.",
    "linkedinUrl": "https://www.linkedin.com/in/...",
    "source": "linkedin_search",
    "status": "pending",
    "addedDate": "2026-04-24"
  }],
  "stagger": {"Midcontinent Communications, Inc.": {"last_day1": "2026-04-27", "person_count": 1}}
}
```

**Company statuses:** `discovery_pending` → `discovery_complete`.
**Candidate statuses:** `pending` → `no` / `conditional` / `yes-no-email` / `yes-with-email` / `skipped-active-sequence`.
**Source:** `linkedin_search` (deep qualify) or `hubspot_contact` (eligible for shallow qualify).
**Atomic writes:** always `.tmp` + `os.replace`. Never delete-then-write.

---

## FAILURE MODES — never silent

Every failure logs to `Claude-Brain/overnight-run-log.md` with timestamp + reason:
- Queue file missing → log alert, exit.
- Empty queue → wrap-up branch.
- LinkedIn unreachable in Discovery → log, exit, next hour retries.
- Profile read fails in Processing → mark candidate `conditional`, continue.
- ZoomInfo no data on Yes → mark `yes-no-email`, qualification creates LI fallback tasks. Doesn't count.
- HubSpot write fails on note/task → mark `yes-with-email-hubspot-incomplete`. Still queue 6 emails (queue is authoritative).
- Chrome unresponsive → retry once after 30s, then log + exit.

---

## MID-RUN COMPANY ADDITIONS

Append new entries to `companies[]` with status `discovery_pending`. The runner picks them up next fire. State file is the source of truth.

---

## Voice + humanization rules

Read **`C:\Claude-Brain\playbook\voice-rules.md`** before drafting any email. Hard rules: no em-dashes, no hyphens, no "Andy" at sign-off, banned AI vocab list.

---

## Approved Vendor Rule

OSI is approved vendor at companies in `Claude-Brain/approved-vendors.json`. Read at sequence-build. Case-insensitive substring match.

**If matched:**
- Email 1: ONE soft acknowledgment. "Side note, we're already on your approved vendor list, so no new vendor onboarding if anything ever needs to move fast."
- One of Email 3 OR Email 4 (Claude picks): one-line reminder. "Quick reminder we're already approved at [Company] if timing matters."
- Other emails: silent.

**If not matched:** never mention. Don't invent.

Never use "vetted" / "pre-approved" / mention "procurement" in Email 1.

---

## Active Sequence Check — runs first

Open `C:\Claude-Brain\email-queue.json`. Match by `to` (email, case-insensitive) OR `prospectName` + `company`.

**Skip if any matched entry has:**
- `status: "pending"`, OR
- `status: "sent"` with `sendDate` in last 30 calendar days.

`paused-*`, `canceled-*`, `sent` >30 days do NOT block. Note in strategy note this is a re-engagement.

**Behavior:** Interactive — ask Andy "Override?". Recurring runner — skip silently, log, mark `skipped-active-sequence`, continue.

---

## OUTREACH FLOW — per Yes-with-email prospect

Qualification has produced verdict + strategy note + provisional LINKED_IN_CONNECT task + call script + VM + LinkedIn invite.

### Step 1: Sequence Type
Pick from product-lines.md sequence table. Read **`C:\Claude-Brain\playbook\product-lines.md`** if you don't already know which sequence fits this title + company.

Verticals — read **`C:\Claude-Brain\playbook\vertical-intel.md`** for what to lead with.

### Step 2: Day 1 — same-company stagger from state metadata

Read `stagger[company_name]` from state file:
- `person_count == 0`: Day 1 = next business day (skip weekends + holidays).
- `1-4`: Day 1 = `last_day1` + 4 business days.
- `5`: Day 1 = `last_day1` + 10 business days (cooling gap).
- `6+`: Day 1 = `last_day1` + 4 business days.

After scheduling, update `last_day1` and increment `person_count`. Atomic write.

Why state metadata, not email-queue scan: queue has 500+ entries; state metadata is O(1) and tracks THIS run only.

### Step 3: Cadence

| Email | sendTime | Gap from prior actual send |
|---|---|---|
| 1 | `4pm` | — (Day 1) |
| 2 | `11am` | +2 bd |
| 3 | `12pm` | +4 bd |
| 4 | `1pm` | +6 bd |
| 5 | `2pm` | +5 bd |
| 6 | `3pm` | +6 bd |

Master `osi-email-sender-v2` fires 11 AM-4 PM ET weekdays. Each window processes queue entries with matching `sendTime`.

**Self-healing:** when Email N fires, recompute Email N+1's sendDate as `N biz days after today`.

**Skip weekends + holidays.** Holiday list: `Claude-Brain/holidays.json` (read at runtime). Fallback if missing: US federal holidays + Good Friday + Black Friday + Christmas Eve + New Year's Eve.

LinkedIn connection request task due Day 1 (skip weekends/holidays).

### Step 4: Write 6 Emails

**Email 1 — sample-offer (Network):**
> Hi [First],
>
> I'm just prepping this package for you. I have a box of swag and a pair of sample SFPs to send from the team at OSI Global.
>
> Do you come into the office, or is there a better address to ship it to?

**Email 1 — sample-offer (Server):**
> Hi [First],
>
> I'd like to send you a sample DIMM from our current batch. Same spec as what you're running, manufacturer warranty, won't touch your OEM support contract.
>
> Do you come into the office, or is there a better address to ship it to?

**Email 1 — pain-led (TPM / DWDM / Storage / Pre-owned):** 3-4 sentences. Lead with their specific pain (role + company). Reference Personal Hook from strategy note. One clear ask. No name at bottom.

Subject: short, specific, not spam-flaggable.

**Email 2** (RE: same subject) branches by archetype:
- **Sample-offer Email 1:** body literally `Any thoughts?` — nothing else.
- **Pain-led Email 1:** 2-3 sentences. Pick ONE move: new data point on same pain / adjacent product line / fresh company signal. End with ONE concrete ask.

Quote Email 1 below. No greeting. No sign-off.

**Email 3** (new subject): different angle / product line not yet covered. 3-4 sentences. One ask. Quote Email 2.

**Email 4** (new subject): another product line. 3-4 sentences. One ask. Quote Email 3.

**Email 5** (new subject): another product line. 3-4 sentences. One ask. Quote Email 4.

**Email 6 — breakup** (new subject): clean close, no ask. One sentence. "Should I close the file on this one, or is the timing just off?" or "No worries if now isn't the right time. Happy to circle back when things shift." Quote Email 5.

### Step 5: Present for Review (Interactive only)

Show all 6 + call script + VM + LinkedIn invite + send schedule. End with: "Look it over and say **ready** when you want to send." Stop. Wait.

### Step 6: Send + Schedule

**Interactive on "ready":** open `https://outlook.office.com` in Chrome. New mail → To, subject, body. Do NOT click Send. Tell Andy: "Email 1 ready in Outlook. Click Send when good, then say **sent**." On "sent": confirm Sent Items, queue Emails 2-6.

**Recurring runner:** append all 6 to email-queue.json. No Outlook step.

### email-queue.json entry

Path: `C:\Claude-Brain\email-queue.json`

```json
{
  "id": "[firstname]-[lastname]-[company-slug]-[N]",
  "prospectName": "[First Last]",
  "company": "[Company]",
  "to": "[email]",
  "subject": "[subject]",
  "body": "[full body including quoted thread]",
  "sendDate": "YYYY-MM-DD",
  "sendTime": "[4pm/11am/12pm/1pm/2pm/3pm]",
  "status": "pending",
  "addedDate": "YYYY-MM-DD"
}
```

### Atomic queue write

```python
import json, os
QUEUE = r'C:\Claude-Brain\email-queue.json'
with open(QUEUE, 'r') as f: queue = json.load(f)
existing_ids = {e.get("id") for e in queue}
queue.extend([e for e in new_entries if e["id"] not in existing_ids])
tmp = QUEUE + '.tmp'
with open(tmp, 'w') as f: json.dump(queue, f, indent=2)
os.replace(tmp, QUEUE)
```

Do NOT use the MCP Write tool for the queue.

### Respread — sync both layers

Editing email-queue.json alone is not enough if there are per-email scheduled tasks. List them via `mcp__scheduled-tasks__list_scheduled_tasks`, update via `update_scheduled_task` to match new sendDate + sendTime. Re-list and diff at the end.

### Step 7: Update LINKED_IN_CONNECT due_date + state metadata

After Day 1 locked:
1. Find existing LINKED_IN_CONNECT task on contact. `manage_crm_objects` updateRequest, set `hs_timestamp` to Email 1 Day 1.
2. Update `stagger[company_name].last_day1` and increment `person_count`. Atomic write state file.

### Step 8: Append to Excel Tab 1

`Claude-Brain/prospects-tracker-new.xlsx`, Tab 1. Columns: Name | Title | Company | LinkedIn URL | OSI Angle | HubSpot Status | Action | Date Added | Notes. Tab 2 is the wrap-up phase, not per-prospect.

---

## Recurring runner prompt template

```
You are the OSI Global overnight runner. Fires hourly. ONE TASK = ONE APPROVAL POOL.

Read C:\Claude-Brain\skills\osi-outreach-sequence\SKILL.md and C:\Claude-Brain\skills\osi-prospect-qualification\SKILL.md first.

Open C:\Claude-Brain\overnight-candidates.json. If missing: log alert to overnight-run-log.md, exit.

Branch:
A. Any company status discovery_pending → Discovery on FIRST one (M&A, HubSpot ownership, LinkedIn search all keyword rounds, paginate, append candidates pending, mark company complete, log, exit).
B. Else if any candidate pending → Processing. Take first, qualification Profile Mode, update status, branch verdict (No/Conditional STOP-GATE; Yes-no-email LI fallback; Yes-with-email queues 6 emails with stagger from state, updates LINKED_IN_CONNECT, appends Tab 1, updates stagger). Continue until 3 yes-with-email OR no pending. Log, exit.
C. Else → wrap-up. Update Tab 2. Log final line. Exit.

Failure modes per skill: log to overnight-run-log.md, never silent.
```

Cron: `0 * * * *`. Cowork adds ~9 min jitter (fires ~:09 each hour). Andy approves tools on first fire only.
