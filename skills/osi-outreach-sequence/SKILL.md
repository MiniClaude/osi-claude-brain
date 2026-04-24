---
name: osi-outreach-sequence
description: >
  Fully automated outreach sequence for OSI Global prospects. Sends 6 emails via Outlook
  (Email 1 at 4 PM ET, Email 2 at 11 AM, Email 3 at 12 PM, Email 4 at 1 PM, Email 5 at 2 PM, Email 6 at 3 PM — each email has its own dedicated window). Creates 7 call tasks in HubSpot (Days 9-31) plus LinkedIn
  connection request task on Day 1. Runs interactively (Andy reviews before sending) or overnight
  (fully automated). Triggers on: "run a sequence", "outreach sequence", "build a sequence for",
  "run sequences for the following companies", pasting a LinkedIn profile, or uploading a profile
  file. In Company Mode, finds and qualifies prospects at named companies then runs the full
  sequence for each qualified person. In Auto Mode (no companies provided), pulls cold companies
  from HubSpot owned by Andy with no activity in 6+ months and prospects those automatically.
  Always use this skill for new prospect outreach.
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
| ZoomInfo enrichment (email, direct phone, mobile) | osi-prospect-qualification |
| Strategy note on HubSpot contact (keywords, call script, VM, The Play, Personal Hook, ENROLL IN CALLS SEQUENCE label) | osi-prospect-qualification |
| `LINKED_IN_CONNECT` task creation (subject, type, owner, LinkedIn invite text in notes, provisional due_date = next business day) | osi-prospect-qualification |
| `LINKED_IN_CONNECT` task **final due_date** (updated to match Email 1's Day 1 after same-company stagger math) | **osi-outreach-sequence** (this skill) |
| No-email-no-phone LinkedIn message fallback tasks (1st LI, 2nd LI) | osi-prospect-qualification |
| Drafting the 6 emails | **osi-outreach-sequence** (this skill) |
| email-queue.json writes and scheduling | **osi-outreach-sequence** (this skill) |
| Same-company stagger math | **osi-outreach-sequence** (this skill) |
| Active sequence check (prevent duplicate enrollment) | **osi-outreach-sequence** (this skill) |
| Excel tracker Tab 1 (Prospects) and Tab 2 (Company Status) | **osi-outreach-sequence** (this skill) |

---

## 🛑 STOP IF NO EMAIL — this skill requires a valid email address

This skill drafts and schedules 6 emails via email-queue.json. No email means no sequence. If ZoomInfo did not return a valid email for this prospect, STOP immediately. Do not run this skill. Qualification's no-email-no-phone LinkedIn message fallback tasks are the complete plan in that case.

---

## 📥 HANDOFF FROM osi-prospect-qualification — assumes qualification has already run

When this skill runs, it assumes osi-prospect-qualification has ALREADY completed on this prospect, which means:

- LinkedIn profile has already been read in full
- ZoomInfo has already been run (email, direct phone, mobile captured)
- Strategy note is already live on the HubSpot contact record
- `LINKED_IN_CONNECT` task is already created with the LinkedIn invite text

**Do NOT re-read LinkedIn. Do NOT re-run ZoomInfo. Do NOT re-write the strategy note. Do NOT re-create the LINKED_IN_CONNECT task.** Those are qualification's jobs.

**One thing this skill DOES update on the existing LINKED_IN_CONNECT task: its due_date.** Qualification creates the task with a provisional due_date of "next business day." Once this skill calculates the final Day 1 for Email 1 (applying same-company stagger), it must update the LINKED_IN_CONNECT task's due_date to match. This is critical because Andy's workflow is synchronized: LinkedIn invite sent at 2 PM, call sequence enrollment, voicemail, then Email 1 auto-fires at 4 PM, all on the same day. If the LINKED_IN_CONNECT due_date and Email 1's Day 1 drift apart, the touches fire on different days and the coordinated attack breaks.

Implementation: after Email 1's final send date is locked in, call `manage_crm_objects` updateRequest on the LINKED_IN_CONNECT task and set `hs_timestamp` (the task due_date) to Email 1's Day 1 date. Do this before writing to email-queue.json so the task queue reflects the correct morning-of-Day-1 surface.

If the strategy note is missing on the contact (or this skill was triggered directly without qualification running first), STOP and invoke osi-prospect-qualification Profile Mode first. Then continue here.

When running in Company Mode (Andy provides company names) or Auto Mode (cold HubSpot companies picked by Claude): the first step is always to invoke qualification's Company Mode per company. Qualification returns a ranked shortlist. This skill then runs per ✅ Yes prospect (with email found) in that list.

---

## Your job

Andy has given you a LinkedIn profile. Produce the full outreach package: 6 personalized emails sent automatically via Outlook (each email has its own dedicated send window — Email 1 at 4 PM ET, Email 2 at 11 AM, Email 3 at 12 PM, Email 4 at 1 PM, Email 5 at 2 PM, Email 6 at 3 PM), 7 call tasks in HubSpot, and a LinkedIn connection request task on Day 1. Andy calls and sends the invite in the afternoon. Email 1 fires at 4 PM Eastern. Everything else runs itself.

Read this entire skill before producing any output.

---

## MODES

This skill has three modes. All three assume osi-prospect-qualification runs on each candidate per the HANDOFF block above. This skill orchestrates WHEN qualification and outreach work happen, across time and across multiple scheduled sessions. Qualification's content (profile reads, verdict, note, LINKED_IN_CONNECT task creation) is NOT duplicated here; it lives in osi-prospect-qualification.

### Interactive Mode — Andy at the keyboard, single or small batch

**Triggered by:** Andy pastes a single LinkedIn profile, or says "build a sequence for [Name]", or a short multi-prospect prompt where Andy is present.

1. Invoke osi-prospect-qualification Profile Mode on the prospect. Qualification produces verdict. If No or Conditional: STOP-GATE applies, end here.
2. If Yes with email: qualification has written the strategy note and created the LINKED_IN_CONNECT task (with provisional due_date).
3. This skill drafts the 6 emails and call script using the Personal Hook from the strategy note.
4. Present everything to Andy for review.
5. Andy says "ready."
6. Open Outlook in Chrome with Email 1 pre-composed. Andy clicks Send himself.
7. Andy says "sent."
8. Calculate Email 1's final Day 1 (applying same-company stagger if others at this company are already in the queue).
9. Update the LINKED_IN_CONNECT task's due_date to match Email 1's Day 1.
10. Schedule Emails 2-6 via email-queue.json.

**Batch size in Interactive Mode is flexible.** Andy can run 4-5 prospects in one session when he is watching.

### Company Mode — Andy names companies, runs overnight or unattended

**Triggered by:** "run sequences for the following companies: X, Y, Z" or similar multi-company prompts. Typically scheduled overnight while Andy sleeps.

Company Mode splits work across two phases:

#### PHASE 1 — Kickoff (Andy at the keyboard, roughly 10-20 minutes)

##### Step 0 — Check for leftover queue from last night (ALWAYS runs first, before any search work)

Before doing any company checks or LinkedIn searches, open `Claude-Brain/overnight-candidates.json` if it exists. Count entries where `status == "pending"` (candidates from a prior night's kickoff that never got processed). This is the leftover queue.

**Leftover queue is the front of tonight's batch work, always.** New candidates from tonight's kickoff (if any) append to the back of the queue. This guarantees that unfinished work from last night never gets stranded and wasted.

Decision tree based on leftover count and Andy's command:

- **Leftover count is 0 or file doesn't exist:** fresh run. Build the queue from scratch per the command (named companies or Auto Mode).

- **Leftover count is between 1 and (batch count × batch size, default 21):** combine. Leftover entries stay at the front of the queue. Fill the remaining slot capacity with new candidates.
  - If Andy named companies: run steps 1-4 below on those companies and append their candidates to the back of the queue.
  - If Andy did NOT name companies (Auto Mode trigger): run the Auto Mode selector (cold companies + active-client filter + OSI fit check + queue-prevent filter, per the Auto Mode section), pick enough companies to cover the remaining gap, and append their candidates.
  - Goal: every overnight batch has work.

- **Leftover count is >= (batch count × batch size):** do NOT search for more. The pending queue already saturates tonight's capacity. Skip steps 1-4 entirely and go straight to the pre-schedule step. Tell Andy: "Leftover queue from [date] has N pending candidates, enough to fill tonight's 7 batches. No new search performed."

Never reset or archive the queue automatically. The only way to start entirely fresh is an explicit Andy command: "fresh run" or "reset queue and run overnight sequences for [companies]." On a fresh-run command, archive the existing file as `overnight-candidates-YYYY-MM-DD-archived.json` and rebuild from scratch.

##### Step 1 onward — company-by-company search work (only runs if Step 0 decided to add new candidates)

For each company Andy named (or Auto Mode selected) in Step 0's gap-fill:

1. **M&A check** — search for recent acquisitions, mergers, rebrands. Update company name if needed.
2. **HubSpot ownership check** — apply the JAM ownership decision tree. Skip other-rep companies with recent activity; log other-rep with 3+ months no activity for account-request; proceed on JAM-owned or not-in-HubSpot.
3. **Regular LinkedIn candidate search** (NOT Sales Navigator — see qualification skill's TOOL CHOICE section). Run all keyword rounds: English priority titles, French keywords for Quebec companies, secondary titles if first round is thin. Paginate through every page of every search. Collect every candidate whose title or search-result card suggests IT / network / telecom relevance.
4. **No profile reads at kickoff. No ZoomInfo at kickoff. No HubSpot contact writes at kickoff.** Just candidate names, LinkedIn URLs, and source company.

Append all newly-collected candidates to the back of `Claude-Brain/overnight-candidates.json` (after any leftover entries from Step 0). Queue order: leftover company A, leftover company B, ..., new company A, new company B, ... Each entry:

```json
{
  "company": "Desjardins",
  "firstName": "...",
  "lastName": "...",
  "linkedinUrl": "https://www.linkedin.com/in/.../",
  "status": "pending"
}
```

Then **pre-schedule identical batches at 2-hour intervals** across the overnight window. Use `mcp__scheduled-tasks__create_scheduled_task` for each batch. Every batch fires with the same prompt: "read `overnight-candidates.json`, work the pending candidates from the top, run until 3 Yes-with-email outreach sequences fire OR the queue is exhausted, then end." Andy approves each `create_scheduled_task` call once at kickoff (session-level "always allow"), then walks away.

**Default batch schedule:** 7 batches at 7 PM / 9 PM / 11 PM / 1 AM / 3 AM / 5 AM / 7 AM = up to 21 sequences launched overnight. Andy can change batch count or spacing with an explicit override in the kickoff prompt.

**Why pre-schedule rather than self-spawn?** Tested 2026-04-17. An orchestrator scheduled task attempting to create child scheduled tasks in an unattended session failed silently because each `create_scheduled_task` call required a fresh tool approval Andy wasn't present to give. Pre-scheduling all batches at kickoff (while Andy is at the keyboard) sidesteps that constraint entirely.

#### PHASE 2 — Per-batch (overnight, each batch fires on its clock)

Each scheduled batch runs identical logic. It is fully self-contained:

1. Read `overnight-candidates.json`.
2. Take the first candidate with `status: "pending"`.
3. Invoke osi-prospect-qualification Profile Mode on that candidate. Qualification does the full regular-LinkedIn profile read (About, Experience, Skills, activity feed) and forms the verdict.
4. Update the candidate's status in the queue to one of: `"no"`, `"conditional"`, `"yes-no-email"`, `"yes-with-email"`. Write the queue file back (atomic: `.tmp` then `os.replace`).
5. Branch by verdict:
   - **No or Conditional:** STOP-GATE applies (qualification's rule — no ZoomInfo, no HubSpot contact, no strategy note, no tasks). Return to step 2.
   - **Yes with no email after ZoomInfo:** qualification creates the LinkedIn fallback tasks (1st LI + 2nd LI). This does NOT count toward the 3 outreach slots. Return to step 2.
   - **Yes with email:** qualification writes the strategy note and creates the LINKED_IN_CONNECT task (with provisional due_date). This skill takes over: draft 6 emails, calculate Email 1's final Day 1 with same-company stagger, update the LINKED_IN_CONNECT task's due_date to match, append 6 entries to email-queue.json. **This is slot 1 (or 2, or 3) of 3.**
6. Continue evaluating candidates until 3 outreach sequences have fired OR the queue has no pending candidates remaining.
7. End the batch.

**Same-company stagger math** is applied by this skill at step 5 when calculating Email 1's Day 1. Persons 1-5 at the same company: 4 business days between consecutive Day 1 dates. Person 6: 10 business days after person 5. Persons 7+: back to 4 business days. Stagger is per-company across the entire email queue, not per-batch.

**Final-batch responsibility:** the last batch of the night (by scheduled fire time) updates Tab 2 of the Excel tracker with the full run summary (company-by-company: Yes count / Sequences Fired / Pending count), writes a session log to `Claude-Brain/sessions/session-YYYY-MM-DD.md`, and cleans up any remaining `status: "pending"` candidates in `overnight-candidates.json` (leaves them marked `pending` for the next night's run).

### Auto Mode — Claude picks cold companies, runs overnight

**Triggered by:** "run sequences tonight" or "find me targets" with no specific company names.

Identical to Company Mode, with three additional checks at the top of Phase 1 kickoff:

1. **Cold-company selection.** Search HubSpot for companies owned by Andy (`hubspot_owner_id: 196669355`) with `notes_last_contacted` 6+ months ago or never contacted.
2. **Active client filter (Auto Mode only).** For each cold company, search HubSpot for closed-won deals or deals in an active pipeline stage. Do NOT use Lifecycle Stage (often wrong). If a deal is found, skip the company and note why:
> SKIPPED: [Company] — active client (deal found: [deal name]). Not prospected.
3. **OSI fit check (Auto Mode only).** For each remaining cold company, confirm it operates networking, telecom, data center, or IT infrastructure at relevant scale. Skip retail, food service, pure software, anything clearly outside OSI's ICP.
4. **Queue-prevent filter.** Filter out any company with pending entries in the email queue (already in an active sequence).
5. Rank remaining companies by OSI fit and pick the top N (default 3-4 for a one-night run).
6. From this point, Auto Mode proceeds identically to Company Mode Phase 1 step 1 onward (M&A check per selected company, HubSpot ownership per company, regular-LinkedIn search, build overnight-candidates.json, pre-schedule batches).

**Auto Mode never runs during the daytime interactive flow.** It is overnight-only.

Token efficiency in Company mode: qualify all prospects at a company first, then run sequences for the Yes prospects without re-displaying all the qualification reasoning. Keep output tight. Never print full emails in the chat — write them directly into the scheduled tasks and HubSpot note only.

---

## TOOLS — owned by osi-prospect-qualification

This skill does not directly use HubSpot for contact lookup, ZoomInfo for enrichment, or LinkedIn for profile research. Qualification owns all three. See the ownership table at the top of this file. Tools this skill DOES use: `mcp__scheduled-tasks__*` for batch scheduling, Outlook via Chrome for Email 1 composition in Interactive Mode, and Python file I/O for email-queue.json writes.

---

## QUALIFICATION GATE — owned by osi-prospect-qualification

The verdict (Yes / No / Conditional) is formed by osi-prospect-qualification before this skill runs. If qualification did not return a Yes with email, this skill should never have been invoked. See the STOP IF NO EMAIL block at the top of this file.

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
  - "Side note — we're already on your approved vendor list, so no new vendor onboarding if anything ever needs to move fast."
  - "For context, we're an approved vendor at [Company] already, so standing up a PO is painless if it comes to that."
- **ONE other email — Email 3 or Email 4 — Claude picks whichever fits the narrative:** Brief reminder. One line. Example: "Quick reminder we're already approved at [Company] if timing matters."
- **All other emails:** Do NOT mention approved-vendor status.

**If the prospect's company does NOT match the approved-vendor list:**
- Do NOT mention approved-vendor status anywhere in the sequence. Do not invent it.

**Phrasing rules:**
- Never "vetted" or "pre-approved" — sounds like marketing. "Approved vendor" is the term.
- Never mention "procurement" in Email 1 — telegraphs the sales motion. Just note we're on the list.

To add a company to the approved-vendor list, Andy edits `Claude-Brain/approved-vendors.json` directly and adds the company name to `approved_vendor_companies`.

---

## Active Sequence Check — hard stop before anything else

Before any other work on this prospect, check the email queue. This prevents stacking duplicate sequences on the same person, which wrecks sender reputation and is bad form.

Open `C:\Claude-Brain\email-queue.json` using the plain Python `open(path,'r')` (the file is on local disk now, not OneDrive). Scan every entry for a match with this prospect:

- Match by `to` field equal to the prospect's email address (case-insensitive), OR
- Match by `prospectName` + `company` both matching the prospect's full name and company (case-insensitive)

**SKIP this prospect entirely if any matched entry has:**
- `status: "pending"` (already enrolled in an active sequence), OR
- `status: "sent"` with a `sendDate` within the last 30 calendar days (sequence recently completed)

Entries with status `paused-*`, `canceled-*`, or older `sent` (>30 days ago) do NOT block. Proceed normally in those cases, but note in the strategy note that a prior sequence completed on [date] so this run is effectively a re-engagement.

**Skip behavior by mode:**

- **Interactive mode:** Tell Andy:
  > SKIPPED: [First Last] at [Company] — [reason: "already enrolled, N emails pending, next send [date]" OR "recent sequence completed [date]"]. Override?

  Wait for explicit "override" from Andy before proceeding. Without override, stop and move on to the next prospect (batch mode) or end (single-prospect mode).

- **Overnight / Auto / Company / Batch modes:** Skip silently. Log the skip to `Claude-Brain/prospects-tracker-new.xlsx` Tab 2 (Company Status) with status `SKIPPED - already enrolled` or `SKIPPED - recent sequence` and the reason in the Notes column. Continue to the next prospect.

This check runs BEFORE HubSpot ownership check, ZoomInfo enrichment, or any research. Fail fast and cheap. Never stack a sequence on top of an active or recently completed one.

---

## Step 1: HubSpot ownership + contact lookup — owned by osi-prospect-qualification

Qualification performs the HubSpot ownership check (JAM only: Andy 196669355, Mark 210187184, John 210187193) and the contact-exists check. Do not repeat here. If the prospect reached this skill, qualification already cleared ownership.

---

## Step 2: ZoomInfo enrichment — owned by osi-prospect-qualification

Qualification runs `enrich_contacts` for email, direct phone, mobile. Do not repeat here. If the prospect reached this skill, the email field on the HubSpot contact is already populated.

Same-company stagger math (used by this skill at Step 4) reads the email queue for prior Day 1 dates at the same company. That is an internal check of this skill's own output — not a ZoomInfo call.

---

## Step 3: Determine Sequence Type

Based on role, title, and company — pick one:

| Sequence | Target roles | Lead angle |
|---|---|---|
| Network | Network Engineer, Architect, Transport Engineer | Free SFP sample |
| Server | Systems Engineer, Infrastructure Engineer, Server Admin | Free DIMM sample |
| TPM | IT Director, DC Manager, IT Asset Manager, Procurement, CIO mid-market | OEM cost pain |
| DWDM | Transport Engineer, Optical NE, Network Planner at carrier/CLEC/MSO | Cost vs Ciena/Nokia |
| Storage | Storage Admin, Storage Engineer | Pre-owned NetApp + TPM |
| Pre-owned | Anyone managing Cisco/Juniper/Arista environments | Pre-owned gear + OSI TPM |

**Calls sequence label** (used in the strategy note header): Call - Network / Call - Server / Call - TPM / Call - DWDM / Call - Storage / Call - Networking

---

## Step 4: Calculate Dates

### Same-company stagger rule — apply BEFORE setting Day 1

Check the email queue for other contacts at the same company. Count how many people at this company are already enrolled (status = "pending" or "sent" in the queue).

- Persons 1-5 at the same company: set this person's Day 1 as **4 business days** after the most recent Day 1 at that company.
- Person 6: set Day 1 as **10 business days** after person 5's Day 1. This is a one-time cooling gap to let the receiving domain's rolling-velocity window roll off before resuming.
- Persons 7 and beyond: return to **4 business days** after the most recent Day 1. The 10-day gap already reset the receiving server's baseline; further spacing delays outreach without adding deliverability protection.

This protects sender reputation by reducing email frequency to the same domain as volume increases.

### Day 1 + cadence

**Day 1** = next business day after today (or staggered per same-company rule above).

Each email in the sequence has its own dedicated send window. Set `sendTime` in the queue entry per email slot:

- **Email 1** sends at **4 PM Eastern** — set sendTime: "4pm"
- **Email 2** sends at **11 AM Eastern** — set sendTime: "11am"
- **Email 3** sends at **12 PM Eastern** — set sendTime: "12pm"
- **Email 4** sends at **1 PM Eastern** — set sendTime: "1pm"
- **Email 5** sends at **2 PM Eastern** — set sendTime: "2pm"
- **Email 6** sends at **3 PM Eastern** — set sendTime: "3pm"

The master osi-email-sender task runs every weekday at 11 AM, 12 PM, 1 PM, 2 PM, 3 PM, and 4 PM Eastern. Each fire processes the queue entries whose `sendTime` matches that window. This 6-window design distributes send load across the day so no single window carries a burst.

**Full sequence cadence — 6 emails + LinkedIn task:**

| # | Send date | Gap from prior | Type |
|---|---|---|---|
| 1 | Day 1 (next business day) | — | Email |
| 2 | 2 business days after Email 1 actual send | +2 bd | Email |
| 3 | 4 business days after Email 2 actual send | +4 bd | Email |
| 4 | 6 business days after Email 3 actual send | +6 bd | Email |
| 5 | 5 business days after Email 4 actual send | +5 bd | Email |
| 6 | 6 business days after Email 5 actual send | +6 bd | Email |

Total sequence length: 23 business days from Email 1's Day 1 to Email 6, assuming no slips.

**Self-healing cadence — anchor to prior email's ACTUAL send date, not Email 1's planned date.**

Each email's send date is calculated relative to the PRIOR email's actual fire date, not relative to Email 1's planned Day 1. This keeps the cadence intact when any send slips. If Email 1 fires a day late because the 4 PM sender window was missed, Email 2 automatically shifts a day later too. If Email 3 fires on time, Email 4 stays 6 business days after Email 3. The sequence self-corrects instead of compressing gaps.

Implementation: at sequence creation time, write all 6 email entries to email-queue.json with provisional send dates calculated forward from Email 1's planned Day 1. When the sender fires Email N, it updates Email N+1's sendDate in the queue to `N biz days after today`, where N is the gap from the table above. If Email N+1 has already been recomputed and no longer matches the planned date, that is expected — the queue is the living schedule, not a frozen plan.

**Skip weekends AND holidays on every send date, including Day 1.** If any calculated date lands on a Saturday, Sunday, or holiday below, push it to the next business day (and recompute subsequent sends from the new anchor if needed).

**Holidays to avoid — never send on these dates:**

US federal holidays (observed, 10 per year):
- New Year's Day (Jan 1, observed nearest weekday)
- Martin Luther King Jr. Day (3rd Monday of January)
- Presidents Day (3rd Monday of February)
- Memorial Day (last Monday of May)
- Juneteenth (Jun 19, observed nearest weekday)
- Independence Day (Jul 4, observed nearest weekday)
- Labor Day (1st Monday of September)
- Columbus Day (2nd Monday of October)
- Veterans Day (Nov 11, observed nearest weekday)
- Thanksgiving Day (4th Thursday of November)
- Christmas Day (Dec 25, observed nearest weekday)

Widely observed in B2B (skip these too):
- Good Friday (varies; 2026 is Apr 3, 2027 is Mar 26)
- Day after Thanksgiving (Black Friday)
- Christmas Eve (Dec 24)
- New Year's Eve (Dec 31)

**Hardcoded dates for the active calendar window — reference when calculating:**

2026: Jan 1 Thu, Jan 19 Mon (MLK), Feb 16 Mon (Presidents), **Apr 3 Fri (Good Friday)**, **May 25 Mon (Memorial)**, **Jun 19 Fri (Juneteenth)**, **Jul 3 Fri (Jul 4 observed)**, **Sep 7 Mon (Labor)**, Oct 12 Mon (Columbus), Nov 11 Wed (Veterans), **Nov 26 Thu (Thanksgiving)**, **Nov 27 Fri (Black Friday)**, **Dec 24 Thu (Xmas Eve)**, **Dec 25 Fri (Christmas)**, **Dec 31 Thu (NYE)**

2027: **Jan 1 Fri (NYD)**, Jan 18 Mon (MLK), Feb 15 Mon (Presidents), **Mar 26 Fri (Good Friday)**, **May 31 Mon (Memorial)**, **Jun 18 Fri (Juneteenth observed)**, **Jul 5 Mon (Jul 4 observed)**, **Sep 6 Mon (Labor)**, Oct 11 Mon (Columbus), Nov 11 Thu (Veterans), **Nov 25 Thu (Thanksgiving)**, **Nov 26 Fri (Black Friday)**, **Dec 24 Fri (Xmas Eve + observed)**, **Dec 31 Fri (NYE)**

**Apply to EVERY email in the sequence** — not just Day 1. If any email's computed send date lands on a holiday (e.g., Email 4 computed as 6 business days after Email 3 lands on Memorial Day), push to the next business day. The business-day count already skips weekends; the holiday overlay pushes any business day that lands on a holiday to the next business day. Subsequent emails then recalculate from that shifted date per the self-healing cadence rule.

**Apply to same-company stagger too** — when calculating Day 1 for Person 2+ as "4 business days after most recent Day 1 at this company," count only real business days (skip weekends AND holidays).

Plus: LinkedIn connection request task due Day 1 (also skip weekends/holidays).

No call tasks are created. The LOB is noted at the top of the strategy note so Andy can enroll the contact in the correct calls sequence manually.

---

## Step 5: Write All 6 Emails

Write every email before doing anything else.

---

### Email 1 (Day 1) — 1st Touch

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

(No name at the end of either template — Outlook signature handles the sign-off.)

**TPM / DWDM / Storage / Pre-owned sequences — pain-led opener:**
Short. 3-4 sentences max. Lead with their specific pain based on role and company. Reference the Personal Hook. One clear ask at the end. No corporate speak. No "Andy" at the bottom — Outlook signature handles it.

Subject line: Short, specific, not flaggable as spam. You decide based on the target.

---

### Email 2 (2 business days after Email 1 actual send) — Sequence Email

Subject: RE: [same subject as Email 1]

Email 2 content BRANCHES by Email 1 archetype. Do NOT write "Any thoughts?" for every sequence. That bump only works when Email 1 asked a one-line logistics question. For consultative pitches it lands weak and wastes the touch.

**How to classify Email 1:**
- Look at the body. If it contains any of: "sample", "swag", "Do you come into the office", "is there a better address to ship it to" → **sample-offer archetype** (Network SFP sequence, Server DIMM sequence, any Email 1 that asked for a shipping address).
- Otherwise → **pain-led archetype** (TPM, DWDM, Storage, Pre-owned, or any consultative Email 1 that ended with "Worth X minutes?" or a similar conversation ask).

**Archetype A — sample-offer Email 1:**

Body is literally:
> Any thoughts?

That's the whole thing. The prospect just needs to answer the shipping question. A longer Email 2 on a shipping ask looks like pressure.

**Archetype B — pain-led Email 1:**

Body is 2-3 sentences. Do NOT repeat Email 1's argument verbatim. Pick ONE of these moves:
- **New data point on the same pain** — add a fresh stat, customer example, or lead-time number that sharpens Email 1's hook.
- **Adjacent pain on a related OSI product line** — if Email 1 was DWDM, open a door on optics supply or TPM. If Email 1 was servers, open a door on DIMMs or storage.
- **Company signal that surfaced since Email 1** — a news item, a hire, an acquisition, a build announcement that makes the pitch more relevant now than two days ago.

End with ONE concrete ask. Not "any thoughts?" Ask for a specific 15 minutes, a sample of a different product, a pointer to the right person, or a direct yes/no on a narrow question.

Example (Email 1 pitched DWDM): "Most carriers in active buildout see OEM transport lead times stretch past a quarter by Q3. SmartOptics usually ships in weeks and runs 30 to 50% below Ciena or Nokia. Worth 15 minutes to compare it against what you have on order?"

Example (Email 1 pitched TPM): "Heard Pensando maintenance is running 40% higher on renewal this cycle. We run multi-vendor TPM on Cisco, Dell, HP, and NetApp at roughly half OEM. Worth a quick look at what's coming off contract in the next two quarters?"

Example (Email 1 pitched server refresh + DIMMs): "DDR4 DIMM pricing has softened another 15% since last month while DDR5 has not moved. If any of the refresh is going to workloads that don't need DDR5, we can save real budget on that line item. Want me to price out a sample config for your next rack?"

**Both archetypes:**

Then quoted Email 1 below in standard reply format:
> On [Day 1 date], Andy McLean wrote:
> [Full Email 1 text]

No greeting. No sign-off. Outlook signature handles the sign-off. Never type "Andy" at the bottom.

When writing the entry to email-queue.json, the `body` field is: [new reply text] + "\n\n" + [quote marker line] + "\n" + [Full Email 1 text]. The osi-email-sender parses out everything before the quote marker and uses native Outlook Reply, so the quote marker itself is just a parse anchor, not what actually goes in the rendered email.

---

### Email 3 (4 business days after Email 2 actual send) — Sequence Email

New subject line. Different angle from Email 1. Introduce a relevant pain point or OSI product line not covered in Email 1. Short. 3-4 sentences. One ask.

Quote Email 2 below in standard reply format.

---

### Email 4 (6 business days after Email 3 actual send) — Sequence Email

New subject line. Introduce a different OSI product line relevant to this prospect. Short. 3-4 sentences. One ask. Reference something specific about their world where possible.

Quote Email 3 below in standard reply format.

---

### Email 5 (5 business days after Email 4 actual send) — Sequence Email

New subject line. Introduce another OSI product line not yet covered. Short. 3-4 sentences. One ask.

Quote Email 4 below in standard reply format.

---

### Email 6 (6 business days after Email 5 actual send) — Breakup

New subject line. Clean close. No ask. One sentence. Leave the door open.
Examples:
- "Should I close the file on this one, or is the timing just off?"
- "No worries if now isn't the right time. Happy to circle back when things shift."

Quote Email 5 below in standard reply format.

---

## Step 6: Call script, voicemail, and LinkedIn invite — owned by osi-prospect-qualification

Qualification has already generated the full call script (KEYWORDS + HOOK + OPENER from the 12-opener library), the voicemail line, and the LinkedIn invite text. All three live in the strategy note and (for the LinkedIn invite) in the LINKED_IN_CONNECT task notes. Do not regenerate any of them here.

If the strategy note is missing these pieces, qualification was skipped or failed. STOP and invoke qualification first.

---

## Step 8: Present for Review (Interactive Mode Only)

Skip entirely in overnight mode.

Present all 6 emails with subject lines, call script, voicemail, LinkedIn invite, and proposed schedule as a table.

End with: "Look it over and say **ready** when you want to send."

Stop. Do not open Outlook until Andy says ready.

---

## Step 9: Send and Schedule

### Interactive Mode — on "ready"

Open Outlook in Chrome with Email 1 pre-composed:
1. Navigate to https://outlook.office.com
2. If login screen appears, stop and notify Andy
3. Click New mail
4. Enter prospect's email in To field, press Tab
5. Enter subject line exactly
6. Click in body above signature, type email body exactly as written
7. Do NOT click Send — leave it pre-composed for Andy

Tell Andy: "Email 1 is ready in Outlook. Click Send when you're good, then say **sent** and I'll schedule the rest."

When Andy says "sent":
- Confirm sent (check Sent Items briefly)
- Schedule Emails 2-6 using overnight mode below
- Create all HubSpot tasks

### Overnight Mode — fully automated

Do NOT create individual scheduled tasks for emails. Instead, append all 6 emails to the queue file.

**Queue file:** C:\Claude-Brain\email-queue.json

Each entry:

```json
{
  "id": "[firstname]-[lastname]-[company-slug]-[N]",
  "prospectName": "[First Last]",
  "company": "[Company]",
  "to": "[email address]",
  "subject": "[subject line exactly]",
  "body": "[full email body including quoted thread — preserve all line breaks]",
  "sendDate": "[YYYY-MM-DD]",
  "sendTime": "[4pm for Email 1 / 11am for Email 2 / 12pm for Email 3 / 1pm for Email 4 / 2pm for Email 5 / 3pm for Email 6, all Eastern]",
  "status": "pending",
  "addedDate": "[today YYYY-MM-DD]"
}
```

The master osi-email-sender task runs every weekday at 11 AM, 12 PM, 1 PM, 2 PM, 3 PM, and 4 PM Eastern. Each fire window processes queue entries whose `sendTime` matches that specific window. No individual scheduled tasks needed.

### How to write to the queue

The queue file lives on local disk at `C:\Claude-Brain\email-queue.json`. Use Python's `open(path, 'w')` to overwrite cleanly:

```python
import json, os

QUEUE = r'C:\Claude-Brain\email-queue.json'
# Or from the sandbox mount:
# QUEUE = '/sessions/.../mnt/Claude-Brain/email-queue.json'

# Step 1: Read existing content (the file is on local disk, no cloud fallback needed).
with open(QUEUE, 'r') as f:
    queue = json.load(f)

# Step 2: Build new entries (Jan, Eric, Tina, Dimitar, or whoever).
new_entries = [ ... ]  # array of entry dicts

# Step 3: Dedupe by id so re-runs don't create duplicates.
existing_ids = {e.get("id") for e in queue}
to_add = [e for e in new_entries if e["id"] not in existing_ids]
queue.extend(to_add)

# Step 4: Atomic write with open('w'). Bypasses the Write-tool's prior-Read requirement
#         and avoids needing cowork delete permission.
tmp = QUEUE + '.tmp'
with open(tmp, 'w') as f:
    json.dump(queue, f, indent=2)
os.replace(tmp, QUEUE)
```

Do NOT use the MCP Write tool for the queue file (its prior-Read requirement breaks on cloud-only files). Do NOT delete the file first (cowork delete permission does not reliably carry across scheduled sessions).

Same pattern applies to `prospects-tracker-new.xlsx` — read via SharePoint if local read fails, write via Python (use `openpyxl` with `load_workbook` on bytes from SharePoint, then `wb.save(path)`).

### Respread / reschedule — sync BOTH layers, never just the queue

Any time you touch an already-queued prospect's emails to change dates or times (respread, cancel-and-reschedule, bulk shift, same-company re-stagger, manual nudge, etc.), you MUST also update any matching per-email scheduled tasks in the Cowork scheduler. Editing email-queue.json alone is not enough.

**Why this rule exists:** Some sequences (legacy or hybrid) have per-email scheduled tasks named `[firstname]-[lastname]-[company-slug]-email-[N]` that fire at their own `fireAt` regardless of what email-queue.json says. If those tasks hold stale dates from before a respread, they will spawn sessions on the old dates. On 2026-04-20, the 4/19 overnight respread updated email-queue.json for Brett Baker but not the per-email scheduled tasks. Stale Email 1 and Email 2 tasks fired hours before their respread queue times, three concurrent sessions launched, and Outlook was hijacked while the sessions clawed at the same tab.

**How to sync after ANY queue edit that changes sendDate or sendTime:**

1. Call `mcp__scheduled-tasks__list_scheduled_tasks` and filter for taskIds starting with the prospect's `[firstname]-[lastname]-[company-slug]-email-` prefix.
2. For every matching task with a future `fireAt`, compare against the queue's new `sendDate` + `sendTime`. If they differ, call `mcp__scheduled-tasks__update_scheduled_task` with the corrected `fireAt` in ISO 8601 with ET offset: `2026-04-22T11:00:00-04:00` during EDT, or `-05:00` during EST.
3. Leave already-disabled tasks alone (those are one-time tasks that have already fired in the past).
4. If NO per-email scheduled tasks exist for this prospect, skip — the master osi-email-sender handles the queue on its own fire windows.
5. Before finishing the respread, re-list and diff every per-email task's `fireAt` against its matching queue entry. Both layers must agree. Log any leftover drift.

**Do not trust memory alone for this.** Always run the list-and-diff at the end of a respread.

---

## Step 10: Update the LINKED_IN_CONNECT task due_date to match Email 1's Day 1

This is the ONLY HubSpot write this skill performs. All contact creation, strategy note writing, and LINKED_IN_CONNECT task CREATION are owned by osi-prospect-qualification and have already happened before this skill runs.

After Email 1's final Day 1 is locked in at Step 4, do this exactly once per prospect:

1. Find the existing `LINKED_IN_CONNECT` task on the contact (subject format: `Sales Nav -- Send connection request -- [First Last] | [Company]`).
2. Call `manage_crm_objects` updateRequest on that task and set `hs_timestamp` (the due_date field) to Email 1's Day 1 date.
3. Do this BEFORE writing email-queue.json entries, so the task surface reflects the correct morning-of-Day-1 timing.

**Why this matters:** Andy's workflow is synchronized. LinkedIn invite sent at 2 PM, call sequence enrollment, voicemail, then Email 1 auto-fires at 4 PM. All four touches must land on the same day. If the LINKED_IN_CONNECT due_date and Email 1's Day 1 drift apart, the coordinated attack breaks.

**Everything else related to HubSpot (contact record, strategy note, LinkedIn invite text, LinkedIn message fallback tasks for no-email cases) is qualification's job.** If any of those are missing when this skill runs, STOP and invoke qualification first.

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
- Space and power: Significant reduction vs. traditional DWDM platforms.
- Simplicity: Easier to deploy and manage.
- Lead times: Ships faster than OEMs.
- Pedigree: Backed by original engineering core. Not grey market.

---

## Cold Call Opener Rules

1. Open with "How have you been?" — 6.6x baseline meeting rate.
2. State a clear reason for calling.
3. End with a question about their world. Never "Is now a good time?"
4. Never ask "Is now a good time?"
5. Voicemails: 15 seconds max. No phone number. End with Andy's email address spelled audibly ("that's andy at osiglobal dot com"). Always present or future tense ("I'm sending" or "I'm about to send"). Never past tense.

---

## Step 11: Update the Excel Tracker

File: Claude-Brain/prospects-tracker-new.xlsx

### Tab 1 — Prospects

Append one row per person after every sequence is created.

Columns: Name | Title | Company | LinkedIn URL | OSI Angle | HubSpot Status | Action | Date Added | Notes

- HubSpot Status: "Andy — HubSpot ID [id]" / "Not found"
- Action: "Pursue — sequence live"
- Notes: Personal Hook and lead angle in 1-2 sentences

### Tab 2 — Company Status

Update after every company is processed (or attempted). One row per company per run.

Columns: Company | Date Run | Status | Prospects Found | Sequences Created | Notes

**Status values:**
- Completed — all qualified prospects found and sequenced
- Partial — started but did not finish (token limit or time). Note how many were done vs. remaining.
- Not Started — ran out of time before this company was reached

After every overnight run, update Tab 2 for all 4 companies. Even companies that were not started get a row with status "Not Started" so Andy knows to carry them into the next run.

**Never skip Tab 2.** If the session ends before all companies are done, write the company status rows first — this is more important than any individual prospect row.
