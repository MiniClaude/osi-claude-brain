---
name: osi-old-customer-reengagement
description: >
  Generate and fully automate a 5-email re-engagement sequence for dormant OSI Global customers
 , people who previously bought from OSI and have gone quiet. Researches the account via ZoomInfo
  scoops and news before writing anything. Emails lead with fresh angles tied to real research,
  not "just checking in." Andy reviews everything first. On "ready", Email 1 is pre-composed in
  Outlook for Andy to send, then Emails 2-5 schedule automatically via email-queue.json.
  Trigger on: "re-engage old customer", "old customer sequence", "revive this account",
  "circle back on old account", or any time Andy pastes a contact who previously bought from OSI
  and wants outreach built. Do NOT use this for cold prospects, use osi-outreach-sequence instead.
---

> **SYNC NOTE:** This skill exists in two locations: `C:\Claude-Brain\skills\osi-old-customer-reengagement\` (Git-versioned, source of truth, backed up at github.com/Drrewdy/Claude-Brain) and the local Cowork `.claude/skills/` mount. Any edits must go into `C:\Claude-Brain\skills\` and be pushed to GitHub. If returning after days away, run `git pull` first to get the latest, then check the local Cowork copy and re-install the `.skill` file if the source has drifted.

# OSI Global, Old Customer Re-Engagement Sequence

## Your job

Andy has given you a contact who previously bought from OSI and went quiet. This is a warm
relationship, they know who OSI is. Your job is to re-open the door with fresh angles tied
to real research, not repeat the last conversation.

Read this entire skill before producing any output.

5 emails. 28-day cadence. Andy sends Email 1 himself. The rest schedule automatically.

---

## 🛑 STEP 0, MANDATORY READ OF DRAFTING RULES

Before drafting any email body or subject, **Read `C:\Claude-Brain\playbook\drafting-rules.md` in full** and load it into context. Single source of truth for product lines, voice rules, branding rules, dead phrases, hook priority, templates, the Bad Example anti-template, and the 6-item self-check.

This is a re-engagement skill: pass `is_cold=False` and `allow_circle_back=True` to the validator. Branding rule still applies: SmartOptics is still NOT named in re-engagement bodies unless the customer already knows them by name from a prior conversation. Default to "OSI transceivers".

---

## 🛑 VALIDATOR BEFORE DELIVERY

Every drafted body and subject runs through `C:\Claude-Brain\scripts\validate_email.py` before being presented to Andy or written to the queue.

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

If `ValueError` raises: rewrite and re-validate. Do NOT write any failing entry to the queue.

---

## Andy Rules, apply to every output

- No em-dashes (U+2014) anywhere. Not once. Split into two sentences instead.
- Keep prose tight and direct. No fluff.
- Emails must feel like a human wrote them to one specific person.
- Tone: warm reconnect, strategic advisor. Not a vendor checking in.
- Emails are short. Mobile-friendly. Scannable in 10 seconds.
- **Never say "checking in", "circling back", or "just wanted to follow up."** All banned.
- **Do not apologize for the silence.** Acknowledge it if needed, move forward.
- **Do not list past purchases.** They know what they bought. Lead with where they are going.
- Do NOT type "Andy" or any name at the bottom of email bodies. Outlook signature handles the sign-off.

---

## Step 1: Gather Contact Info

Ask Andy to provide or paste:
- Contact full name, title, company, email
- What OSI sold them historically (product lines are enough, optics, DIMMs, TPM, DWDM, storage, networking, pro services)
- How long since last contact and any context on why it went quiet

If Andy pastes a HubSpot record, extract fields directly. Do not press for history that isn't offered, research fills the gaps.

---

## Active Sequence Check, hard stop before anything else

Before any other work on this prospect, check the email queue. This prevents stacking duplicate sequences on the same person, which wrecks sender reputation and is bad form.

Open `C:\Claude-Brain\email-queue.json` using plain Python `open(path,'r')`. The queue is Git-versioned along with the rest of Claude-Brain. Andy syncs between his two laptops manually via `git pull` / `git push`. Scan every entry for a match with this prospect:

- Match by `to` field equal to the prospect's email address (case-insensitive), OR
- Match by `prospectName` + `company` both matching the prospect's full name and company (case-insensitive)

**SKIP this prospect entirely if any matched entry has:**
- `status: "pending"` (already enrolled in an active sequence), OR
- `status: "sent"` with a `sendDate` within the last 30 calendar days (sequence recently completed)

Entries with status `paused-*`, `canceled-*`, or older `sent` (>30 days ago) do NOT block. Proceed normally in those cases, but note in the strategy note that a prior sequence completed on [date] so this run is effectively a re-engagement.

**Skip behavior by mode:**

- **Interactive mode:** Tell Andy:
  > SKIPPED: [First Last] at [Company], [reason: "already enrolled, N emails pending, next send [date]" OR "recent sequence completed [date]"]. Override?

  Wait for explicit "override" from Andy before proceeding. Without override, stop and move on to the next prospect (batch mode) or end (single-prospect mode).

- **Overnight / Auto / Company / Batch modes:** Skip silently. Log the skip to `Claude-Brain/prospects-tracker-new.xlsx` Tab 2 (Company Status) with status `SKIPPED - already enrolled` or `SKIPPED - recent sequence` and the reason in the Notes column. Continue to the next prospect.

This check runs BEFORE HubSpot ownership check, ZoomInfo enrichment, or any research. Fail fast and cheap. Never stack a sequence on top of an active or recently completed one.

---

## Approved Vendor Rule, read list from Claude-Brain file

OSI is an approved vendor at a list of accounts maintained in `Claude-Brain/approved-vendors.json`. Read that file at sequence-build time (plain Python: `open(path,'r')`) and check if the prospect's company matches any entry (case-insensitive substring match, e.g. "Desjardins Group" matches "Desjardins").

**If the prospect's company matches an approved-vendor entry:**
- **Email 1:** Include ONE line acknowledging approved-vendor status. Soft, peer-to-peer phrasing. Examples:
  - "Side note, we're already on your approved vendor list, so no new vendor onboarding if anything ever needs to move fast."
  - "For context, we're an approved vendor at [Company] already, so standing up a PO is painless if it comes to that."
- **ONE other email, Email 3 or Email 4, Claude picks whichever fits the narrative:** Brief reminder. One line. Example: "Quick reminder we're already approved at [Company] if timing matters."
- **All other emails:** Do NOT mention approved-vendor status.

**If the prospect's company does NOT match the approved-vendor list:**
- Do NOT mention approved-vendor status anywhere in the sequence. Do not invent it.

**Phrasing rules:**
- Never "vetted" or "pre-approved", sounds like marketing. "Approved vendor" is the term.
- Never mention "procurement" in Email 1, telegraphs the sales motion. Just note we're on the list.

To add a company to the approved-vendor list, Andy edits `Claude-Brain/approved-vendors.json` directly and adds the company name to `approved_vendor_companies`.

---

## Step 2: HubSpot Ownership Check

Search HubSpot by name and current company.

**Hard stop if owned by another rep:**
> OWNED BY ANOTHER REP: [First Last] at [Company] is in HubSpot (ID: [id]) owned by [rep name]. Do you want to proceed?

Wait for Andy's explicit instruction before continuing.

JAM owner IDs, only proceed if owned by:
- Andy McLean: 196669355
- Mark Metz: 210187184
- John Houston: 210187193

---

## Step 3: ZoomInfo Enrichment

Run two passes in parallel:

### 3a, Contact Data
Pull: email (validation 80+), direct phone, mobile phone.
- Never save a company main/switchboard number. Direct and mobile only.
- City and state always come from LinkedIn, never ZoomInfo.

### 3b, Account Research (the re-entry hook)
Pull: `enrich_scoops`, `enrich_news`, and `enrich_intent` on the company domain.

Look for: funding rounds, acquisitions, DC buildouts, infrastructure announcements, leadership
changes (CIO, CTO, VP of IT, Director of Network), network modernization, 400G/DWDM refresh
signals, server refresh, OEM end-of-life, cost-cutting, vendor consolidation, AI buildout.

Capture the 2 or 3 strongest signals. These become the backbone of Email 1.

If ZoomInfo returns nothing useful, fall back to a market trigger: DIMMs pricing, Park Place/
Service Express merger, 400G adoption, OEM end-of-life pressure.

---

## Step 4: LinkedIn Job Change Check

Before writing anything, verify the contact is still at the company and still in a relevant role.

Navigate to their LinkedIn profile. If they have moved on, stop and tell Andy, the sequence
should either follow them to their new company or be redirected to a new contact at the
original account.

Also note city and state from their LinkedIn location field, required for HubSpot.
Infer timezone using Andy's 6-bucket system:
- US Eastern → us_slash_eastern
- US Central → us_slash_central
- US Mountain → us_slash_mountain
- US Pacific → us_slash_pacific
- US Alaska (AKST/AKDT) → us_slash_alaska
- Canada Atlantic (AST/ADT, e.g. Halifax, Moncton, Saint John) → canada_slash_atlantic
- Outside these six → use the closest matching bucket

---

## Step 5: Previous Employer OSI Client Check

Pull their work history from LinkedIn. Search HubSpot for any of their previous employers.
If a match is found, flag it in the strategy note. If no match, skip this section entirely
in the note, do not write "none found."

---

## Step 6: Determine Lead Angle

Based on what they bought previously and what the research surfaced, assign a lead angle
to each email slot. Use vertical intelligence below to guide the opener choice.

The goal: each email leads with a different OSI product line or angle. Never repeat the
same play twice in the same sequence.

Product lines available:
1. Optics, SmartOptics transceivers, private-labeled. Sample offer is the opening wedge.
2. DWDM and Open Line Systems, SmartOptics DCP, 30-50% below Ciena/Nokia. Ships fast.
3. Compute and Components, DIMMs from Samsung/Hynix/Micron. Lead with DIMMs.
4. Storage, NetApp TPM, pre-owned storage.
5. TPM, 40-60% below OEM. Multi-vendor. Gartner-recognized, privately owned, no PE.
6. Pre-Owned and New Networking, Pre-owned Cisco/Juniper/Arista. New Nokia authorized.
7. Professional Services, Strong signal only. Never lead cold.

---

## Step 7: Calculate Send Dates

**Email 1** = next business day after today (or the day Andy says "ready").

**Send windows (each email has its own window in the 6-window sender architecture):**
- Email 1: 4 PM ET (`sendTime: "4pm"`)
- Email 2: 11 AM ET (`sendTime: "11am"`)
- Email 3: 12 PM ET (`sendTime: "12pm"`)
- Email 4: 1 PM ET (`sendTime: "1pm"`)
- Email 5: 2 PM ET (`sendTime: "2pm"`)

**Cadence (business days, self-healing, each email anchors to prior email's actual send date):**

| # | Send date | Gap from prior | Type |
|---|---|---|---|
| 1 | Day 1 (next business day) |, | Email |
| 2 | 5 business days after Email 1 actual send | +5 bd | Email |
| 3 | 2 business days after Email 2 actual send | +2 bd | Email |
| 4 | 5 business days after Email 3 actual send | +5 bd | Email |
| 5 | 8 business days after Email 4 actual send | +8 bd | Email |

Total span: 20 business days from Email 1 to Email 5 (roughly 28 calendar days). Wider overall cadence than new-outreach because old customers need more breathing room.

The master osi-email-sender task runs every weekday at 11 AM, 12 PM, 1 PM, 2 PM, 3 PM, and 4 PM Eastern. Each fire window processes queue entries whose `sendTime` matches that window.

**Skip weekends AND holidays on every send date.** If any calculated date lands on a
Saturday, Sunday, or holiday, push to the next business day.

**Holidays to skip:**

US federal holidays (observed):
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

Also skip: Good Friday, Black Friday, Christmas Eve (Dec 24), New Year's Eve (Dec 31).

**2026 hardcoded:** Apr 3 (Good Friday), May 25 (Memorial), Jun 19 (Juneteenth), Jul 3 (Jul 4 observed), Sep 7 (Labor), Nov 26 (Thanksgiving), Nov 27 (Black Friday), Dec 24, Dec 25, Dec 31.

**2027 hardcoded:** Jan 1, Mar 26 (Good Friday), May 31 (Memorial), Jun 18 (Juneteenth observed), Jul 5 (Jul 4 observed), Sep 6 (Labor), Nov 25 (Thanksgiving), Nov 26 (Black Friday), Dec 24, Dec 31.

---

## Step 8: Write All 5 Emails

Write every email before doing anything else.

---

### Email 1 (Day 0), Research-Led Re-Entry

Open with a specific observation from the research, ZoomInfo intent topic, scoop, or
recent company news. This is not a cold reach. They know OSI. Lead with something that
shows you were paying attention.

Transition into the strongest OSI angle based on their history and the research signal.
One clear ask: 20 minutes to compare notes.

3-4 short paragraphs. No corporate speak. No name at the bottom.

---

### Email 2 (Day 5), Different Angle

Pivot hard to a different OSI product line, one they haven't heard from you on recently,
or one the research hinted at. Show range. Make it clear OSI is not a one-product shop.

2-3 short paragraphs. Soft close: "worth a conversation if this is on the radar."

---

### Email 3 (Day 10), "Any thoughts?"

This email is ALWAYS the same. Reply in Email 1's thread (RE: subject = sender uses Reply flow).

Body: **Any thoughts?**

That is the entire body. Nothing else. No greeting. No sign-off. No additional text. The sender's Reply flow attaches the prior thread natively. Do NOT include `On X wrote:` placeholders or `>` lines in the queue body.

---

### Email 4 (Day 17), Direct Yes/No

🚫 **STANDALONE fresh-subject touch.** New subject line means NEW MAIL flow, sender types the body verbatim. Body must contain ONLY the new pitch. New angle not yet covered. End with a direct yes or no question.
Examples: "Is that a live conversation for your team right now?" or "Worth 15 minutes or
should I take you off the list?"

2-3 sentences plus the question.

NEVER include `On <date>, Andy McLean wrote:`, `>` quoted lines, or any prior email content. The 2026-04-29 incident pattern.

---

### Email 5 (Day 28), Clean Close

🚫 **STANDALONE fresh-subject touch.** New subject line, NEW MAIL flow, body verbatim. Short. Respectful. Leaves the door open without groveling.

Do not call this a breakup. Do not apologize. One sentence close:
- "Whenever the next project lands on your desk, I'd like to be the first call."
- "No pitch, no pressure, just a phone number when the timing is right."

NEVER include any quoted thread or prior email content. No name at the bottom. Outlook signature handles it.

---

## Step 9: Humanization Pass

Run every email through this list. Rewrite anything that fails.

**Banned AI vocabulary:** remove "crucial," "pivotal," "landscape," "underscore," "delve,"
"showcase," "testament," "enhance," "foster," "garner," "leverage" (as a verb), "seamless,"
"robust," "cutting edge." Replace with plain alternatives or cut the sentence.

**No hyphens** in email bodies or subject lines. "End of life" not "end-of-life",
"24/7/365" not "24-hour", "third party" not "third-party".

**No em-dashes (U+2014)** anywhere. Not once. Split into two sentences.

**No rule of three.** Break any three-item list into natural prose.

**No -ing pileup** at sentence tails. Kill trailing participial clauses like "highlighting
our advantage", "ensuring uptime", "reflecting market shifts."

**No negative parallelisms.** Remove "it's not just X, it's Y" constructions.

**Vary sentence length.** Mix short punchy sentences with longer ones.

**Use "is/are/has"** instead of "serves as," "stands as," "functions as."

**Final read-aloud check.** Mentally read each email aloud. If it sounds like a press
release or a vendor pitching, rewrite it. It should sound like one person emailing another.

---

## Step 10: Generate Subject Lines

For each email EXCEPT Email 3 (which is a reply, inherits Email 1's subject):
- Write 5 subject line options
- Mix: 2-3 professional and specific, 1-2 unexpected or curiosity-driven
- No hyphens in subject lines
- **Pick one at random and commit to it.** Do not ask Andy which to use. Claude chooses.
  Use actual randomness across runs so the same sequence does not always get the safe choice.
- Present all 5 to Andy with the selected one clearly marked (bold + "SELECTED")

If Andy explicitly tells you to swap a subject line after seeing the set, honor that.
Otherwise the random pick stands.

---

## Step 11: Write Call Script and Voicemail

**Skip entirely if no phone number was found.**

Format exactly as below, no paragraphs, no extra text:

QUICK CONNECT KEYWORDS
[6-10 spoken trigger words relevant to this specific person]

LIVE CALL SCRIPT
OPENER: [Full opener from library below, or custom if a strong company hook was found]
VM: [One line. 15 seconds max. One-sentence hook. "I'm sending you something right now, subject line is [Email 1 subject]." Ends with Andy's email: "that's andy at osiglobal dot com." No phone number. Present or future tense only. Never past tense.]

### Opener Library

**Telco / Service Provider network engineer**
"Hey [Name], how have you been? It's Andy with OSI Global. We supply ZR and ZR+ coherent optics to carrier teams as a secondary source when Cisco or Lumentum timelines slip. Is that something your team is running into right now?"

**Bank / Financial Institution network engineer**
"Hey [Name], how have you been? It's Andy with OSI Global. We supply certified compatible optics to bank IT teams, mostly for the break-glass scenario where something fails and you can't wait two weeks for OEM. I was going to send a few complimentary SFPs your way. Would that be useful?"

**Enterprise IT / Consulting network engineer**
"Hey [Name], how have you been? It's Andy with OSI Global. We work with enterprise IT teams on third party maintenance, specifically replacing OEM support on Cisco gear that is running fine but coming off warranty. Is that a conversation your team is having right now?"

**Manufacturing network engineer**
"Hey [Name], how have you been? It's Andy with OSI Global. We supply certified compatible optics and networking spares to manufacturing IT teams for the break-glass scenario. I was going to send a few complimentary SFPs so you've got a Plan B on the shelf. Worth it?"

**Director or VP any vertical**
"Hey [Name], how have you been? It's Andy with OSI Global. We work with infrastructure leaders on two things mostly: third party maintenance and optical hardware where OEM timelines or costs have become a problem. Is either of those a live conversation for your team?"

**Already has TPM, merger wedge**
"Hey [Name], how have you been? It's Andy with OSI Global. With the Park Place and Service Express merger, a lot of teams have been taking a fresh look at their TPM relationships. Have you had a chance to renegotiate since the merger, or are you still on the same rates?"

**Systems / Infrastructure engineer, DIMMs**
"Hey [Name], how have you been? It's Andy with OSI Global. We source server memory direct from Samsung and Hynix for infrastructure teams dealing with DDR4 and DDR5 cost pressure. Is that on your radar right now?"

**Storage engineer / admin**
"Hey [Name], how have you been? It's Andy with OSI Global. We do third party maintenance on NetApp and other storage platforms for teams that have gear running fine but coming off OEM support. Is that a conversation you're having?"

**IT Director, compute and infrastructure**
"Hey [Name], how have you been? It's Andy with OSI Global. We work with IT leaders on server memory and third party maintenance, mostly for teams carrying OEM costs on infrastructure that has been running fine for years. Is budget pressure on that something you're dealing with?"

**Transport engineer / Optical network engineer, DWDM**
"Hey [Name], how have you been? It's Andy with OSI Global. We supply open line DWDM systems, 30 to 50% below Ciena and Nokia, with no licensing headaches. A few teams have been using us to fill capacity gaps without going back to the OEM. Is that a conversation worth having for your network?"

---

## Step 12: Write LinkedIn Re-Engagement Message

Under 300 characters. Short and timely. Reference the research hook or something specific
from their profile. Do not mention it has been a while. No pitch. No mutual connections.

---

## Step 13: Present for Review, Wait for "Ready"

Present everything to Andy:

1. **Research summary**, 3-5 bullets on what ZoomInfo scoops, news, and intent surfaced.
   Show the hook. This is what gives the sequence legs.
2. **Angle distribution**, confirm which OSI product line leads each email
3. **All 5 emails in full**, for each: email number, send date, all 5 subject lines with
   selected one marked in bold + "SELECTED", full body
4. **Call script and voicemail** (if phone found)
5. **LinkedIn re-engagement message**
6. **Proposed send schedule as a table**

**Stop completely. Do not send. Do not open Outlook. Do not write to the queue. Wait.**

End with: "Look it over and say **ready** when you want to send."

---

## Step 14: On "Ready", Send Email 1, Then Schedule the Rest

When Andy says "ready" (or any clear go-ahead like "send it", "looks good", "do it"):

### Send Email 1 via Outlook

1. Navigate to https://outlook.office.com in Chrome
2. If login screen appears, stop and notify Andy
3. Click New mail
4. Enter prospect's email in To field, press Tab
5. Enter selected subject line exactly
6. Click in body above signature, type email body exactly as written
7. Do NOT click Send, leave pre-composed for Andy

Tell Andy: "Email 1 is ready in Outlook. Click Send when you're good, then say **sent** and I'll schedule the rest."

When Andy says "sent":
- Briefly confirm in Sent Items
- Schedule Emails 2-5 via email-queue.json (below)
- Create all HubSpot tasks

### Schedule Emails 2-5 via email-queue.json

**Queue file:** C:\Claude-Brain\email-queue.json

Each entry:

```json
{
  "id": "[firstname]-[lastname]-[company-slug]-oldcust-[N]",
  "prospectName": "[First Last]",
  "company": "[Company]",
  "to": "[email address]",
  "subject": "[subject line, sanitized]",
  "body": "[sanitized body. RE: subject (Reply flow): JUST the new reply text. Sender's Reply flow attaches the prior thread natively. New subject (NEW MAIL flow): ONLY the new pitch. NEVER include `On X wrote:` placeholders or `>` quoted lines, those go through verbatim and produce the 2026-04-29 incident pattern. ALL bodies em-dash and en-dash free per sanitizer below.]",
  "sendDate": "[YYYY-MM-DD]",
  "sendTime": "[4pm for Email 1, 11am for Email 2, 12pm for Email 3, 1pm for Email 4, 2pm for Email 5]",
  "status": "pending",
  "addedDate": "[today YYYY-MM-DD]"
}
```

**Task ID format:** `[firstname]-[lastname]-[company-slug]-oldcust-[N]`
Example: `jane-smith-acme-oldcust-2`

#### MANDATORY: Sanitize before queue write

Before appending any entry, run the canonical sanitizer from `osi-outreach-sequence` Step 6.7 on every body and every subject. The sanitizer strips em-dashes (U+2014), en-dashes (U+2013), quote markers in fresh-subject Email 4/5 bodies, and asserts the result is clean. If it raises, STOP the queue write and surface to Andy. Do NOT append a partial sequence.

Identical function definition to keep this skill self-contained:

```python
import re

def sanitize_body(text: str, email_index: int) -> str:
    if text is None: return ""
    EM = chr(0x2014)  # em-dash, banned by Andy Rule #4 so referenced via chr()
    EN = chr(0x2013)  # en-dash
    text = (text
        .replace(" " + EM + " ", ". ").replace(EM + " ", ". ").replace(" " + EM, ".").replace(EM, "-")
        .replace(" " + EN + " ", ". ").replace(EN, "-"))
    if email_index >= 4:  # Email 4 and 5 are NEW MAIL flow in this skill
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
        raise ValueError(f"sanitize_body left dashes. Text starts: {text[:80]!r}")
    return text.strip()

def sanitize_subject(subject: str) -> str:
    if subject is None: return ""
    EM = chr(0x2014)
    EN = chr(0x2013)
    subject = (subject.replace(" " + EM + " ", ", ").replace(EM, "-").replace(" " + EN + " ", ", ").replace(EN, "-"))
    subject = re.sub(r"\s+", " ", subject).strip()
    if EM in subject or EN in subject:
        raise ValueError(f"sanitize_subject left dashes. Subject: {subject!r}")
    return subject

# Apply to every email before queue append
for i, email in enumerate(emails, start=1):
    email["body"]    = sanitize_body(email["body"], i)
    email["subject"] = sanitize_subject(email["subject"])
    if not email["body"]:
        raise ValueError(f"Email {i} body empty after sanitization. Stopping. ID: {email.get('id')}")
```

**Write pattern (after sanitization):**

```python
import json, os

QUEUE = r'C:\Claude-Brain\email-queue.json'

with open(QUEUE, 'r') as f:
    queue = json.load(f)

new_entries = [ ... ]  # array of entry dicts for Emails 2-5, ALREADY SANITIZED

existing_ids = {e.get("id") for e in queue}
to_add = [e for e in new_entries if e["id"] not in existing_ids]
queue.extend(to_add)

tmp = QUEUE + '.tmp'
with open(tmp, 'w') as f:
    json.dump(queue, f, indent=2)
os.replace(tmp, QUEUE)
```

Do NOT use the MCP Write tool for the queue file. Do NOT delete the file first.

---

## Step 15: Save to HubSpot

### Task housekeeping, always do this first

When a prospect is being processed and they have an existing `LINKED_IN_CONNECT` task in HubSpot (the "Sales Nav -- Send connection request" task that triggered this sequence):

1. **Mark the existing task COMPLETED.** Set `hs_task_status` = `COMPLETED` on that task via `manage_crm_objects` updateRequest. This removes it from Andy's open task queue.

2. **Create a NEW `LINKED_IN_CONNECT` task** scheduled for Day 1 (the date Email 1 fires). Use the standard subject format: `Sales Nav -- Send connection request -- [First Last] | [Company]`. Owner: 196669355. Notes: the LinkedIn invite text. This surfaces the connection request on Andy's task queue the morning of Day 1 so he can send the LinkedIn invite the same day Email 1 fires.

Do this for EVERY prospect regardless of whether they had an existing task or not (if no existing task, just create the new one).

---


### Create or update contact record

### Data quality, HARD REQUIREMENTS (do not skip)

Every contact written to HubSpot MUST have these fields populated correctly. If any are missing or wrong, STOP, do not write the record. Research harder, then retry.

**Required fields on every save:**
| Field | Source | Format | Enforcement |
|---|---|---|---|
| `firstname`, `lastname` | LinkedIn | As shown | Hard |
| `jobtitle` | LinkedIn (authoritative) | Current role from top card | Hard |
| `company` | LinkedIn | Current employer | Hard |
| `email` | ZoomInfo (verified 80+) or existing HubSpot value | Standard email | Soft (note "not found" if ZI returns nothing) |
| `phone` | ZoomInfo `phone` field (direct dial) or existing HubSpot value | `+1 (XXX) XXX-XXXX` for US/CA | **Hard format** |
| `mobilephone` | ZoomInfo `mobilePhone` field only | `+1 (XXX) XXX-XXXX` for US/CA | **Hard format + NEVER company switchboard** |
| `city`, `state` | LinkedIn location field | As shown | Hard |
| `hs_timezone` | Andy's 6-bucket from LinkedIn city/state | `us_slash_eastern` / `us_slash_central` / `us_slash_mountain` / `us_slash_pacific` / `us_slash_alaska` (US Alaska) / `canada_slash_atlantic` (Canada Atlantic). Outside these six, use the closest matching bucket. | **Hard** |
| `hs_linkedin_url` | Sales Nav URL (`linkedin.com/sales/lead/[ID]/`) OR regular `linkedin.com/in/` URL | Full URL | **Hard** |

**Phone format rule:**
- US and Canada numbers: `+1 (XXX) XXX-XXXX`, with the space after `+1`, parentheses around area code, space before first block, hyphen before last 4.
- Example: `+1 (440) 567-7444`
- If existing HubSpot data has `(416) 353-7591` without country code, UPGRADE it to `+1 (416) 353-7591` when you write.
- Non-US/CA: use `+[country code] [number]` appropriate to the region.

**Mobile phone rule, never violate:**
- `mobilephone` holds the person's DIRECT mobile/cell ONLY.
- NEVER put a company main/switchboard number in `mobilephone`.
- If ZoomInfo returns no mobile, leave `mobilephone` BLANK. Do not substitute.

**Pre-write checklist, run BEFORE every contact save:**
1. jobtitle is current (pulled from LinkedIn top card, not HubSpot)
2. phone formatted `+1 (XXX) XXX-XXXX` (if US/CA)
3. mobilephone formatted OR blank (not HQ number)
4. hs_timezone set (one of the 6 buckets)
5. hs_linkedin_url set (full URL)
6. Associated company record exists and is linked

If any check fails, FIX IT or leave the field blank. Do NOT write a partial record.

---


### LinkedIn & association rules, apply on every contact save

**Job title, always refresh from LinkedIn (authoritative).**
Even if HubSpot already has a `jobtitle` value, pull the current title from the prospect's LinkedIn profile top card and overwrite. HubSpot titles go stale; LinkedIn is source of truth. Fallback order if LinkedIn is unreachable (closed profile, URL broken, private): use the ZoomInfo enriched `jobTitle` field. Only if neither is available, leave the existing HubSpot value alone.

**Associated company, always link on contact creation.**
Before creating or updating a contact, search HubSpot for the company by name (`search_crm_objects` objectType=COMPANY, `query` = company name). If found, associate the contact to that company record via the `associations` parameter in `manage_crm_objects.createRequest` or `updateRequest`. If the company is not found in HubSpot, create a new company record first (owner: 196669355, name: company name from LinkedIn) and then associate the contact to it.

Never leave a contact orphaned from its company. Unlinked contacts break same-company stagger logic, deal tracking, and reporting.


Required fields: first name, last name, job title, company, email (ZoomInfo), phone
(ZoomInfo direct field), mobile (ZoomInfo mobilePhone field), city (LinkedIn), state
(LinkedIn), timezone (hs_timezone, 6-bucket system), LinkedIn URL (hs_linkedin_url,
regular linkedin.com/in/ URL).

Do NOT save a company main/switchboard number. Direct and mobile only.
City, state, and timezone always come from LinkedIn, never ZoomInfo.

### Create strategy note, EVERYONE

objectType: "notes", owner 196669355, associated to contact.

Format exactly:

ENROLL IN CALLS SEQUENCE: [Call - Network / Call - Server / Call - TPM / Call - DWDM / Call - Storage / Call - Networking]

QUICK CONNECT KEYWORDS
[6-10 keywords, one line]

LIVE CALL SCRIPT (omit entire section if no phone)
OPENER: [full opener from library]
VM: [one line, 15 seconds max. One-sentence hook. "I'm sending you something right now, subject line is [Email 1 subject]." Ends with Andy's email: "that's andy at osiglobal dot com." No phone number. Present or future tense only. Never past tense.]

THE PLAY
[One tight paragraph: why they qualify for re-engagement + the research hook + the attack
plan. Include Previous Employer OSI Client Check only if a HubSpot match was found. Skip
the section entirely if no matches.]

--- EMAIL SEQUENCE ---
Email 1 - Day 1 - [Date] - Subject: [subject]
[full email body]

Email 2 - Day 5 - [Date] - Subject: [subject]
[full email body]

Email 3 - Day 10 - [Date] - Subject: RE: [Email 1 subject]
Any thoughts?
---------- On [Date], Andy McLean wrote ----------
[Email 1 quoted]

Email 4 - Day 17 - [Date] - Subject: [subject]
[full email body + thread]

Email 5 - Day 28 - [Date] - Subject: [subject]
[full email body + thread]

Never use em-dashes anywhere in the note.

### LinkedIn Connection Request task, EVERYONE

- Subject: "Sales Nav -- Send connection request -- [First Last] | [Company]"
- Type: LINKED_IN_CONNECT
- Due: Day 1 (same date as Email 1)
- Notes: LinkedIn re-engagement message text
- Owner: 196669355

Check for existing connection request task first. Skip if already exists.

### If no email AND no phone, LinkedIn message tasks only

- Task 1: LINKED_IN_MESSAGE, "1st LI -- [First Last] | [Company]", due Day 1.
- Task 2: LINKED_IN_MESSAGE, "2nd LI -- [First Last] | [Company]", due Day 1 + 14.
Check for existing tasks first. Skip if exist.

---

## Step 16: Update Excel Tracker

File: Claude-Brain/prospects-tracker-new.xlsx, Tab 1, Prospects

Append one row after the sequence is created:

Columns: Name | Title | Company | LinkedIn URL | OSI Angle | HubSpot Status | Action | Date Added | Notes

- HubSpot Status: "Andy, HubSpot ID [id]" or "Not found"
- Action: "Pursue, old customer sequence live"
- Notes: What they bought before + research hook in 1-2 sentences

---

## Vertical Intelligence

### Telco and Service Providers
Lead with optics. Do NOT open with free SFPs. Lead with supply chain reliability.
TPM rarely the opener at engineer level.

### Large Banks and Financial Institutions
Lead with optics. Free SFP offer works here. Do NOT lead with TPM.
If known TPM provider, use Park Place/Service Express merger wedge.

### Professional Services and Consulting
TPM viable opener. Lead with pain not price. Free optics also works.

### Manufacturing
Free optics as break-glass insurance. TPM for aging Cisco gear.

### Healthcare
TPM with documented SLAs. DIMMs for server refresh.
Gartner-recognized, privately owned, no PE matters here.

---

## TPM Positioning

**Unknown if they have TPM:**
- Banks: optics opener, TPM is second conversation
- Consulting: TPM can open, lead with pain not savings %
- Manufacturing/enterprise: TPM strong, aging gear and OEM end-of-life is the hook

**Known TPM provider (Park Place, Service Express, Curvature):**
Merger wedge: "With the Park Place and Service Express merger, a lot of teams have been
taking a fresh look at their TPM relationships. Have you had a chance to renegotiate since
the merger, or are you still on the same rates?"

---

## DWDM / SmartOptics Talking Points

- Cost: 30-50% below Ciena and Nokia. Minimal licensing fees.
- Space and power: Significant reduction vs. traditional DWDM platforms.
- Simplicity: Easier to deploy and manage.
- Lead times: Ships faster than OEMs.
- Pedigree: Backed by original engineering core. Not grey market.

---

## Cold Call Opener Rules

1. Open with "How have you been?", 6.6x baseline meeting rate.
2. State a clear reason for calling.
3. End with a question about their world. Never "Is now a good time?"
4. Never ask "Is now a good time?"
5. Voicemails: 15 seconds max. No phone number. End with Andy's email address spelled audibly ("that's andy at osiglobal dot com"). Always present or future tense ("I'm sending" or "I'm about to send"). Never past tense.
