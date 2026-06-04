---
name: osi-3email-reengagement
description: >
  Generate a hyper-personalized 3-email re-engagement sequence for OSI Global prospects
  who have already been through a previous outreach sequence. Use this skill when Andy
  uploads a LinkedIn profile and indicates this is a second-touch outreach, months after
  the original sequence. Triggers on: "re-engagement," "second touch," "circle back,"
  "went through the sequence," "re-engage [name]," or any time Andy uploads a profile
  and mentions it has been months since last contact. Always research recent company news
  before writing. Always run this skill before writing any re-engagement outreach.
---

> **SYNC NOTE:** This skill exists in two locations: `C:\Claude-Brain\skills\osi-3email-reengagement\` (Git-versioned, source of truth, backed up at github.com/Drrewdy/Claude-Brain) and the local Cowork `.claude/skills/` mount. Any edits must go into `C:\Claude-Brain\skills\` and be pushed to GitHub.

# OSI Global 3-Email Re-Engagement Sequence

## Your job

Andy has given you a LinkedIn profile. This person has already been through a previous outreach sequence and did not respond. They know who OSI is. Your job is to re-open the door with fresh angles, not re-introduce the company. Produce the full outreach package: strategy note, call scripts, LinkedIn message, and individual HubSpot email tasks, each ready to press send.

Read this entire skill before producing any output.

---

## ⚙️ STEP -1: LOAD TOOLS ON DEMAND (NO BULK PREFETCH)

**Do NOT bulk-load every tool at once.** Loading many MCP schemas in one shot can trip an API error, `tools.X.custom.input_schema: int too big to convert`, from an oversized integer in one MCP tool's JSON schema (a ZoomInfo or Chrome tool). Load each tool with its own small ToolSearch call the first time a phase needs it.

Load only the core tools up front:
```
ToolSearch({ query: "select:mcp__workspace__bash,mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__search_crm_objects,mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__manage_crm_objects,mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__get_crm_objects", max_results: 4 })
```

Then load each remaining group with its own small ToolSearch call just before first use:
- ZoomInfo -> `mcp__4ba1185f-93a5-43f3-9910-49e11601259c__enrich_contacts` (add `enrich_news` / `enrich_scoops` only when you actually run a news/scoops lookup)
- LinkedIn -> `mcp__Claude_in_Chrome__navigate`, `mcp__Claude_in_Chrome__get_page_text` (add `tabs_context_mcp` only if needed)
- Web search -> `WebSearch`
- State tracking -> `TaskCreate`, `TaskUpdate` (only if used)

Keep each ToolSearch group small (3-5 tools). If a group ever triggers the `int too big to convert` 400, split it and load tools one at a time to isolate and skip the offender.

After both return, all schemas are live. Do not call ToolSearch again during the run.

---

## 🛑 STEP 0: MANDATORY READ OF DRAFTING RULES

Before drafting any email body, subject line, LinkedIn message, voicemail script, or call opener, **Read `C:\Claude-Brain\playbook\drafting-rules.md` in full** and load it into context. Single source of truth for product lines, voice rules, branding rules, dead phrases, hook priority, templates, the Bad Example anti-template, and the 6-item self-check.

Step 0 is non-negotiable. Do NOT rely on training data for the drafting rules.

This is a re-engagement skill: pass `is_cold=False` and `allow_circle_back=True` to the validator. Branding rule still applies: SmartOptics is NOT named in re-engagement bodies unless the prospect already knows them by name from a prior conversation. Default to "OSI transceivers".

---

## 🛑 HARDWIRED RULE: NO EMPLOYER VERIFICATION, NO SEQUENCE

Before any HubSpot write, any email queued, or any task created, the prospect's current employer must be confirmed. HubSpot records go stale. A contact existing in HubSpot from a prior sequence is NOT verification that they still work there.

**Path A (default, strongly preferred):** Full LinkedIn profile read. About + Experience + Skills + Activity. The current Experience entry confirms the company and start date.

**Path B (fallback, only when LinkedIn truly does not exist):** ZoomInfo email at the company's corporate domain AND a dated web-search confirmation that they currently work there. Acceptable sources: company website team page, conference speaker bio, press release, podcast bio, recent industry article. Source must be within the last 6 months. Strategy note carries an explicit `EMPLOYER VERIFICATION: [source URL + date]` line.

If neither path closes: mark `no` in strategy note as "could not verify current employer", STOP. Do not queue.

---

## 🛑 VALIDATOR BEFORE DELIVERY

Every drafted body and subject runs through `C:\Claude-Brain\scripts\validate_email.py` before being presented to Andy or written to any task.

```python
import sys
sys.path.insert(0, r'C:\Claude-Brain\scripts')
from validate_email import validate_or_raise

for i, email in enumerate(emails, start=1):
    validate_or_raise(
        body=email['body'],
        subject=email['subject'],
        email_index=i,
        is_cold=False,
        allow_circle_back=True,
    )
```

If `ValueError` raises: rewrite and re-validate. Do NOT deliver any email that fails validation.

---

## Andy Rules, apply to every output

- No em-dashes (U+2014) anywhere. Not once. Split into two sentences if needed.
- Keep prose tight and direct. No fluff.
- Emails must feel like a human wrote them to one person, not a mass blast.
- Tone: peer-to-peer. They have heard Andy's name before. Acknowledge time has passed without being awkward about it.
- Emails are short. Mobile-friendly. Scannable in 10 seconds.

---

## Active Sequence Check, hard stop before anything else

Before any other work on this prospect, check the email queue. This prevents stacking duplicate sequences on the same person, which wrecks sender reputation and is bad form.

Open `C:\Claude-Brain\email-queue.json` using plain Python `open(path,'r')`. Scan every entry for a match with this prospect:

- Match by `to` field equal to the prospect's email address (case-insensitive), OR
- Match by `prospectName` + `company` both matching the prospect's full name and company (case-insensitive)

**SKIP this prospect entirely if any matched entry has:**
- `status: "pending"` (already enrolled in an active sequence), OR
- `status: "sent"` with a `sendDate` within the last 30 calendar days (sequence recently completed)

Entries with status `paused-*`, `canceled-*`, or older `sent` (>30 days ago) do NOT block. Proceed normally.

**Skip behavior:**

- **Interactive mode:** Tell Andy:
  > SKIPPED: [First Last] at [Company], [reason: "already enrolled, N emails pending, next send [date]" OR "recent sequence completed [date]"]. Override?

  Wait for explicit "override" from Andy before proceeding. Without override, stop.

- **Overnight / Auto / Batch modes:** Skip silently. Log to `Claude-Brain/overnight-run-log.md` with timestamp, name, company, and reason. Continue to the next prospect.

This check runs BEFORE any research. Fail fast and cheap.

---

## Approved Vendor Rule, read list from Claude-Brain file

Read `Claude-Brain/approved-vendors.json` at sequence-build time (plain Python: `open(path,'r')`). Case-insensitive substring match against the prospect's company name.

**If matched:**
- **Email 1:** ONE soft line acknowledging approved-vendor status. Examples:
  - "Side note, we're already on your approved vendor list, so no new vendor onboarding if anything ever needs to move fast."
  - "For context, we're an approved vendor at [Company] already, so standing up a PO is painless if it comes to that."
- **Email 3:** Brief one-line reminder. Example: "Quick reminder we're already approved at [Company] if timing matters."
- **Email 2:** Do NOT mention approved-vendor status.

**If NOT matched:** Do NOT mention approved-vendor status anywhere. Do not invent it.

**Phrasing rules:**
- Never "vetted" or "pre-approved". "Approved vendor" is the term.
- Never mention "procurement" in Email 1.

---

## Step 1: Employer Verification

Confirm the prospect still works at the company from the original sequence. Use Path A (LinkedIn) by default. Use Path B only if LinkedIn is not available. If neither closes, STOP-GATE and log.

Note the verification source in the strategy note under `EMPLOYER VERIFICATION:`.

---

## Step 2: Research (do this before writing anything)

**HubSpot Check**
Search HubSpot for the prospect and their current company. Pull any existing notes to understand what was sent previously. Note the HubSpot owner. Only create tasks if owned by Andy McLean (196669355), Mark Metz (210187184), or John Houston (210187193).

If owned by another rep, flag it and wait for Andy's instruction before proceeding.

**ZoomInfo Contact Enrichment**
Run `enrich_contacts` with the prospect's name and company. Capture:
- Email (use existing HubSpot email if already verified; ZoomInfo is enrichment only)
- Direct dial phone
- Mobile phone (never substitute a switchboard)
- Job title (LinkedIn is authoritative; ZoomInfo is a cross-check)

If ZoomInfo returns an email different from the HubSpot primary, write the ZoomInfo address to `hs_additional_emails` and prepend a note: `ALT EMAIL [date]: ZoomInfo lists [email]. Using [chosen]. Pattern: [pattern] verified by [signal].`

**Company News Research**
Use ZoomInfo `enrich_scoops` and `enrich_news`. Look for: funding rounds, acquisitions, mergers, new DC buildouts, infrastructure announcements, leadership changes, network modernization, cost-cutting or vendor consolidation, 400G/DWDM/server refresh signals.

This feeds the hook in Email 1. If no news found, fall back to a market trigger: DIMMs pricing, Park Place/Service Express merger, 400G adoption trends.

---

## Step 3: Determine contact data available

| Data available | Email tasks | Call tasks | VM + call script in notes |
|---|---|---|---|
| Email + phone | Yes | Yes | Yes |
| Email only | Yes | No | No |
| Phone only | No | Yes | Yes |
| Neither | No | No | No |

**EVERYONE regardless of data:**
- LinkedIn connection request task (LINKED_IN_CONNECT), always created on Day 1
- Strategy and Fit note, always saved to HubSpot

---

## Step 4: Email-Pattern Verification (MANDATORY before drafting)

Before drafting, verify the prospect's `to:` address against the company's verified email pattern. Algorithm: `knowledge/email-pattern-resolver.md`.

Check the existing HubSpot contact's strategy note for an EMAIL RESOLUTION block.

- `hubspot-existing` or `verified-pattern`: proceed.
- `dominant-pattern`: proceed but include `"emailResolution": "dominant-pattern"` in each queue entry.
- `manual-required`: STOP. Do NOT draft or queue. Return: `"Pattern signal too weak at [Company]. Andy must verify [email] before queueing."` Do not retry.

If no EMAIL RESOLUTION block exists in the strategy note, run the resolver inline:
1. Search HubSpot for all contacts at the same company.
2. Bucket emails by pattern, score per `email-pattern-resolver.md`.
3. If the prospect's address matches the verified or dominant pattern, proceed.
4. If it doesn't, STOP-GATE. Log to `overnight-run-log.md`.

---

## Step 5: Compute Day 1 (same-company stagger)

Read `state.stagger[company_name]` from `C:\Claude-Brain\overnight-candidates.json`:

| `person_count` | Day 1 |
|---|---|
| `0` | Next business day (skip weekends + holidays) |
| `1-4` | `last_day1` + 4 business days |
| `5` | `last_day1` + 10 business days (cooling gap) |
| `6+` | `last_day1` + 4 business days |

After scheduling Email 1, update `last_day1` and increment `person_count`. Atomic write to state file.

**Skip weekends + holidays.** Holiday list: `Claude-Brain/holidays.json`. Fallback if missing: US federal holidays + Good Friday + Black Friday + Christmas Eve + New Year's Eve.

---

## Step 6: Produce all outputs in this exact order

---

### 1. Strategy and Fit

**Quick Connect Keywords**
6-10 spoken trigger words to listen for on a call. Only ones relevant to this prospect and their current situation.

**What Was Sent Before**
Summarize what OSI product lines were targeted in the original sequence based on HubSpot notes. If notes unavailable, infer from profile and title.

**New Angles for Re-Engagement**
Identify 1-2 product lines or talking points NOT covered last time. This sequence must feel different, not like a repeat.

**Target Sequences**
List OSI product lines to lead with this time. Choose from: Optics, DWDM, TPM, Compute and Components (lead DIMMs), Storage, Pre-Owned and New Networking, Professional Services (strong signal only).

**The Play**
1-2 sentences. How to re-approach with a fresh angle. Be specific about what has changed.

**The Personal Hook**
A timely trigger from research: company news, recent LinkedIn post, job change, market event. Must feel current. Do not reuse the hook from the original sequence.

**Previous Employer OSI Client Check**
List previous employers. Note HubSpot matches. Skip section entirely if no matches.

**EMPLOYER VERIFICATION**
State the source and date used to confirm current employer. Example: `LinkedIn profile, Experience section, current role start date [month year].`

---

### 2. Live Call Script

**Skip entirely if no phone number available.**

Format exactly as below, no paragraphs, no extra text:

KEYWORDS: [5-8 spoken trigger words including technical terms and any news-driven triggers]
HOOK: [Company news or personal trigger in one sentence. If nothing: none, using library opener]
OPENER: [Full opener from OPENER LIBRARY, or custom if HOOK is populated]
VM: [One line. 15 seconds max. One-sentence new hook. "I'm sending you something right now, subject line is [Email 1 subject]." Ends with Brian's email: "that's bc at osihardware dot com." No phone number. Present or future tense only. Never past tense.]

#### OPENER LIBRARY

**Telco / Service Provider network engineer**
"Hey [Name], how have you been? It's Brian with OSI Global. We supply ZR and ZR+ coherent optics to carrier teams as a secondary source when Cisco or Lumentum timelines slip. Is that something your team is running into right now?"

**Bank / Financial Institution network engineer**
"Hey [Name], how have you been? It's Brian with OSI Global. We supply certified compatible optics to bank IT teams, mostly for the break-glass scenario where something fails and you can't wait two weeks for OEM. I was going to send a few complimentary SFPs your way. Would that be useful?"

**Enterprise IT / Consulting network engineer**
"Hey [Name], how have you been? It's Brian with OSI Global. We work with enterprise IT teams on third party maintenance, specifically replacing OEM support on Cisco gear that is running fine but coming off warranty. Is that a conversation your team is having right now?"

**Manufacturing network engineer**
"Hey [Name], how have you been? It's Brian with OSI Global. We supply certified compatible optics and networking spares to manufacturing IT teams for the break-glass scenario. I was going to send a few complimentary SFPs so you've got a Plan B on the shelf. Worth it?"

**Director or VP any vertical**
"Hey [Name], how have you been? It's Brian with OSI Global. We work with infrastructure leaders on two things mostly: third party maintenance and optical hardware where OEM timelines or costs have become a problem. Is either of those a live conversation for your team?"

**Already has TPM, merger wedge**
"Hey [Name], how have you been? It's Brian with OSI Global. With the Park Place and Service Express merger, a lot of teams have been taking a fresh look at their TPM relationships. Have you had a chance to renegotiate since the merger, or are you still on the same rates?"

**Systems / Infrastructure engineer, DIMMs**
"Hey [Name], how have you been? It's Brian with OSI Global. We source server memory direct from Samsung and Hynix for infrastructure teams dealing with DDR4 and DDR5 cost pressure. Is that on your radar right now?"

**Storage engineer / admin**
"Hey [Name], how have you been? It's Brian with OSI Global. We do third party maintenance on NetApp and other storage platforms for teams that have gear running fine but coming off OEM support. Is that a conversation you're having?"

**IT Director, compute and infrastructure**
"Hey [Name], how have you been? It's Brian with OSI Global. We work with IT leaders on server memory and third party maintenance, mostly for teams carrying OEM costs on infrastructure that has been running fine for years. Is budget pressure on that something you're dealing with?"

**Procurement, TPM competitive bid**
"Hey [Name], how have you been? It's Brian with OSI Global. We make competitive bids on multi-vendor maintenance contracts. A lot of procurement teams are using us to benchmark their current rates, especially since the Park Place and Service Express merger. Would a competitive bid be worth a look for your next cycle?"

**Transport engineer / Optical network engineer, DWDM**
"Hey [Name], how have you been? It's Brian with OSI Global. We supply open line DWDM systems, 30 to 50% below Ciena and Nokia, with no licensing headaches. A few teams have been using us to fill capacity gaps without going back to the OEM. Is that a conversation worth having for your network?"

**Network architect, metro or long-haul WDM**
"Hey [Name], how have you been? It's Brian with OSI Global. We do open architecture DWDM, SmartOptics platform, significantly less rack space and power than traditional Ciena or Nokia boxes, and ships faster. Is that something that fits anything on your roadmap right now?"

---

### 3. Voicemail Script

**Skip entirely if no phone number available.**

One voicemail. Never two. 15 seconds max. They know who Andy is. Lead with the new hook. Name Email 1 subject line. End with Brian's email address spelled audibly ("that's bc at osihardware dot com"). No phone number. Always present or future tense. Never past tense.

"Hey [Name], Brian with OSI Global. [One sentence new hook]. I'm sending you something right now, subject line is [Email 1 subject]. That's andy at osiglobal dot com."

---

### 4. Re-Engagement Message (LinkedIn)

Under 300 characters. Short and timely. Reference the new hook. Do not mention it has been months since last contact. No mutual connections.

---

### 5. The 3-Email Re-Engagement Sequence

**Cadence (business days, each email anchors to prior email's actual send date):**

| # | Send date | Send window | Type |
|---|---|---|---|
| 1 | Day 1 (computed in Step 5) | 4 PM ET (sendTime: "4pm") | Email |
| 2 | 10 business days after Email 1 actual send | 11 AM ET (sendTime: "11am") | Email |
| 3 | 12 business days after Email 2 actual send | 12 PM ET (sendTime: "12pm") | Email |

Total span: roughly 22 business days (about 30 calendar days) from Email 1 to Email 3. Wider gaps than new outreach because re-engagement needs breathing room.

**Subject line rules:**
- Email 1: You decide. Fresh and specific. References the new hook or a timely trigger. Never a repeat of the original sequence subject.
- Email 2: RE: same subject as Email 1.
- Email 3: New subject line. Clean close. Leave the door open.

**Email 1 (Day 1, 4 PM ET)**
Lead with the new hook. Company news, market trigger, or a product angle not covered in the original sequence. Do not re-introduce OSI. Do not acknowledge the previous sequence directly. Short, 3-4 sentences. One ask. Under 90 words.

**Email 2 (10 business days after Email 1 actual send, 11 AM ET)**
Body: `Any thoughts?`

That is the entire body. Nothing else. The sender's Reply flow attaches the prior thread natively. Do NOT include any quoted text, `On X wrote:` placeholders, or `>` lines in the queue body. Just `Any thoughts?` is correct.

**Email 3 (12 business days after Email 2 actual send, 12 PM ET)**
🚫 **STANDALONE fresh-subject touch.** Email 3 has a NEW subject line. NEW MAIL flow types the body verbatim into the prospect's inbox exactly as written. The body must contain ONLY the new pitch. Clean close. Leave the door open with one sentence. Examples:
- "Should I close the file on this one, or is the timing just off?"
- "No worries if now isn't the right time. Happy to circle back when things shift."

NEVER include `On <date>, Andy McLean wrote:`, `>` quoted lines, or any prior email content. Doing so causes the 2026-04-29 incident pattern: placeholder text lands in the prospect's inbox verbatim.

**Send-window assignments:**
- Email 1: `sendTime: "4pm"`
- Email 2: `sendTime: "11am"`
- Email 3: `sendTime: "12pm"`

**Re-engagement tone rules:**
- Do not re-introduce OSI or explain what they do.
- Do not acknowledge the previous sequence directly.
- Lead with something new: company news, market trigger, pricing window, product update.
- Make them feel like this outreach is timely, not persistent.

---

## Step 7: 6-Item Self-Check (MANDATORY before sanitize and validator)

For every drafted email body, write out answers to these six questions in working context BEFORE calling sanitize and validator. The validator catches strings; this self-check catches semantics it cannot see.

1. **Does the first sentence reference the prospect or a timely trigger, not OSI?** (Email 1 only. Pass = new hook, company news, role signal. Fail = "I'm Andy", "I work with", any OSI-first opener.)
2. **Is the new hook actually in Email 1?** (Email 1 only. The hook must be a real timely trigger, not generic geography or title alone. If thin, ABORT and log to `overnight-run-log.md`.)
3. **Is there exactly ONE product line in this email?** (All emails. Surgical Isolation rule.)
4. **Did I name SmartOptics?** (Must be no unless prospect already knows the name from a prior conversation.)
5. **Did I claim OSI manufactures?** (All emails. Must be no.)
6. **Did I sign with "Andy" at the bottom?** (All emails. Must be no. Outlook signature handles it.)

If any answer is wrong, REWRITE before passing to sanitize. Do not paper over with sanitize.

If question 2 fails (thin or no hook), do NOT write Email 1. Log to `overnight-run-log.md` and exit. Andy will pull a real hook next session.

---

## Step 8: Sanitize Bodies (MANDATORY before validator)

Run this on every body and subject before queue write. Never skip.

```python
import re

def sanitize_body(text: str, email_index: int) -> str:
    if text is None:
        return ""

    EM = chr(0x2014)   # em-dash
    EN = chr(0x2013)   # en-dash
    text = (text
        .replace(" " + EM + " ", ". ")
        .replace(EM + " ", ". ")
        .replace(" " + EM, ".")
        .replace(EM, "-")
        .replace(" " + EN + " ", ". ")
        .replace(EN, "-"))

    # Email 3 is STANDALONE. Strip any quote markers defense-in-depth.
    if email_index >= 3:
        markers = [
            r"\n*\s*-{5,}\s*On .* wrote\s*-{5,}",
            r"\nOn .*,? .* (?:McLean )?(?:wrote|wrote:)",
            r"\n>+ ",
            r"\nFrom: Andrew McLean",
        ]
        for m in markers:
            match = re.search(m, text)
            if match:
                text = text[:match.start()].rstrip()
                break

    text = re.sub(r" {2,}", " ", text)
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text)

    if EM in text or EN in text:
        raise ValueError(f"sanitize_body left dashes in body. Bug. Text starts: {text[:80]!r}")

    return text.strip()


def sanitize_subject(subject: str) -> str:
    if subject is None:
        return ""
    EM = chr(0x2014)
    EN = chr(0x2013)
    subject = (subject
        .replace(" " + EM + " ", ", ")
        .replace(EM, "-")
        .replace(" " + EN + " ", ", ")
        .replace(EN, "-"))
    subject = re.sub(r"\s+", " ", subject).strip()
    if EM in subject or EN in subject:
        raise ValueError(f"sanitize_subject left dashes. Bug. Subject: {subject!r}")
    return subject


for i, email in enumerate(emails, start=1):
    email["body"]    = sanitize_body(email["body"], i)
    email["subject"] = sanitize_subject(email["subject"])
    if not email["body"]:
        raise ValueError(f"Email {i} body is empty after sanitization. Stopping.")
```

If `sanitize_body` raises, STOP the entire queue write. Do NOT append a partial sequence. Surface the error to Andy with the offending email index.

---

## Step 9: Write to Queue

Build 3 entries in memory, then append atomically. Do NOT use the MCP Write tool for the queue.

**Entry format:**

```json
{
  "id": "[firstname]-[lastname]-[company-slug]-[N]",
  "prospectName": "[First Last]",
  "company": "[Company]",
  "to": "[email]",
  "subject": "[subject, sanitized]",
  "body": "[sanitized body]",
  "sendDate": "YYYY-MM-DD",
  "sendTime": "[4pm/11am/12pm]",
  "status": "pending",
  "addedDate": "YYYY-MM-DD",
  "emailResolution": "[hubspot-existing | verified-pattern | dominant-pattern]"
}
```

**Atomic write:**

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

After the write succeeds, output exactly one confirmation line and nothing else:

`Queued: [First Last] | Re-engagement | Day 1 [YYYY-MM-DD]`

---

## Step 10: Save to HubSpot

🚨 **ALL `manage_crm_objects` calls use `confirmationStatus: "CONFIRMATION_WAIVED_FOR_SESSION"`.** Never show a proposed-changes table. Never ask "Approve?". Andy's session kickoff is blanket approval for all HubSpot writes this skill produces.

### Task housekeeping, do this first

1. **Mark any existing `LINKED_IN_CONNECT` task COMPLETED.** Set `hs_task_status` = `COMPLETED` on that task via `manage_crm_objects` updateRequest.

2. **Create a NEW `LINKED_IN_CONNECT` task** (Sales Nav connection request) scheduled for Day 1. Subject format: `Sales Nav -- Send connection request -- [First Last] | [Company]`. Owner: 196669355. Notes: the LinkedIn re-engagement message text.

The connection request fires Day 1 regardless of whether Andy was previously connected. If already connected, Andy handles the LinkedIn side manually. The task still surfaces the action.

### Update contact record

Required fields to verify/refresh on every re-engagement save:

| Field | Source | Enforcement |
|---|---|---|
| `jobtitle` | LinkedIn top card (authoritative, overwrite stale HubSpot value) | Hard |
| `email` | Existing HubSpot primary (use ZoomInfo as alt, never replace verified) | Soft |
| `phone` | ZoomInfo `phone` field or existing HubSpot value | Hard format |
| `mobilephone` | ZoomInfo `mobilePhone` field only | Hard format + NEVER switchboard |
| `hs_linkedin_url` | Current LinkedIn URL | Hard |
| `hs_timezone` | From LinkedIn city/state | Hard |

**Phone format:** `+1 (XXX) XXX-XXXX` for US/CA. Upgrade existing records missing the country code.

**Mobile phone rule:** NEVER put a company main/switchboard number in `mobilephone`. If ZoomInfo returns no mobile, leave blank.

**Associated company:** Confirm the contact is still linked to the correct company record. If they changed companies, create/find the new company record and re-associate.

### Strategy and Fit note

objectType: "notes", owner 196669355, associated to contact.

Note format:

```
EMPLOYER VERIFICATION
[Source and date used to confirm current employer.]

QUICK CONNECT KEYWORDS
[6-10 keywords, one line]

LIVE CALL SCRIPT (omit entire section if no phone number)
OPENER: [full opener from library]
VM: [one line, 15 seconds max.]

WHAT WAS SENT BEFORE
[Summary of prior sequence product lines and dates if known.]

NEW ANGLES
[1-2 product lines or angles being used this time that were not used before.]

THE PLAY
[One tight paragraph: new hook + what changed + attack plan.]

--- EMAIL SEQUENCE ---
Email 1 - Day 1 - [Date] - Subject: [subject]
[full email body]

Email 2 - Day 14 (approx) - [Date] - Subject: RE: [subject]
Any thoughts?

Email 3 - Day 30 (approx) - [Date] - Subject: [new subject]
[full email body]
```

Never use em-dashes anywhere in the note.

---

## Step 11: Update Excel Tracker

Append a row to `Claude-Brain/prospects-tracker-new.xlsx`, Tab 1.

Columns: Name | Title | Company | LinkedIn URL | OSI Angle | HubSpot Status | Action | Date Added | Notes

Use `openpyxl` to load and append. If the file is locked or the write fails, log to `overnight-run-log.md` and continue. The Excel tracker is a convenience record, not the source of truth. Never block the queue write on a tracker failure.

---

## Step 12: Update Stagger Metadata

Update `state.stagger[company_name]` in `C:\Claude-Brain\overnight-candidates.json`:
- `last_day1`: the just-computed Day 1
- `person_count`: increment by 1

Atomic write. If write fails, retry once. If still fails, log and continue with the queue unchanged.

---

## FAILURE MODES (never silent)

Every failure logs to `Claude-Brain/overnight-run-log.md` with timestamp + reason + prospect name + company:

| Failure | Action |
|---|---|
| Employer verification fails | Log, mark candidate `no-employer-verify`, STOP. Do NOT queue. |
| Active sequence check hits | Log `skipped-active-sequence`, exit. |
| Email pattern = `manual-required` | Log, STOP. Do NOT queue. Surface to Andy. |
| Sanitize raises | Log, STOP entire queue write. Surface offending email index. |
| Validator raises | Log violation list, flip candidate to `pending-relookup`, exit. |
| Queue write fails | Retry once, then log + exit. Do NOT proceed on stale queue. |
| LINKED_IN_CONNECT task update fails | Log `linkedin-task-incomplete`, keep queue entries. Queue is authoritative. |
| Excel append fails | Log warning only. Do NOT block queue. |
| Stagger metadata write fails | Log, retry once, default to next business day if still fails. |

---

## DWDM / SmartOptics talking points (re-engagement context only, not cold)

- Cost: 30-50% below Ciena and Nokia. Minimal licensing fees.
- Space and power: Significant reduction vs. traditional DWDM platforms.
- Simplicity: Easier to deploy and manage.
- Lead times: Ships faster than OEMs.
- Pedigree: Backed by original engineering core. Not grey market.

---

## OSI Product Lines

1. **Optics**, OSI transceivers. Sample offer is the opening wedge.
2. **DWDM and Open Line Systems**, SmartOptics DCP, 30-50% below Ciena/Nokia.
3. **Compute and Components**, DIMMs from Samsung/Hynix/Micron. Lead with DIMMs.
4. **Storage**, NetApp TPM, pre-owned storage.
5. **TPM**, 40-60% below OEM. Multi-vendor. Gartner-recognized, privately owned, no PE.
6. **Pre-Owned and New Networking**, Pre-owned Cisco/Juniper/Arista. New Nokia authorized.
7. **Professional Services**, Strong signal only. Never lead cold.
