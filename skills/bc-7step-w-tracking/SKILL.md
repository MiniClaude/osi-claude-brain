---
name: bc-7step-w-tracking
description: "Build and fully automate a 7-email cold outreach sequence for any OSI Global prospect WITH AUTOMATIC BCC TRACKING on every send. Identical flow to bc-7email-custom, but every send (live Email 1 plus all 6 scheduled follow-ups) auto-populates the BCC field with bc@osihardware.com and 21878985@bcc.hubspot.com. First BCC puts a copy in Brian's Outlook inbox so he can see sends actually fired. Second BCC auto-logs the email to the HubSpot contact timeline, no Chrome extension or integration sign-in needed. ALWAYS use this skill when Brian says \"run a tracked sequence\", \"run a sequence with tracking\", \"sequence with bcc\", \"tracked outreach\", \"bc-7step-W-tracking\", \"run the tracking sequence\", \"w tracking\", or otherwise indicates he wants sends BCC'd to his inbox and the HubSpot logging address. The original bc-7email-custom skill is preserved as a no-tracking fallback."
---

# OSI Global Outreach Sequence — With BCC Tracking

Generates and fully automates a personalized 7-email outreach sequence for any prospect.
Every send BCCs Brian's inbox and his HubSpot logging address automatically. Brian reviews everything first. When he says "run", Email 1 goes out immediately and the rest schedule automatically.

**Tracking BCCs applied to every send in this skill:**
- `bc@osihardware.com` — copy lands in Brian's Outlook inbox so he can confirm sends fired
- `21878985@bcc.hubspot.com` — auto-logs email onto the HubSpot contact timeline

If either address ever changes, update them in Step 7b and the three task prompt blocks in Step 7d.

---

## Signature Block — Use This Every Time

Do NOT rely on Outlook's auto-signature — it is inconsistent. Every send step explicitly clears whatever Outlook auto-inserts and types this signature instead:

```
Brian Charrette
Director of Key Accounts
Desk: 805.845.5167 | Cell: 805.682.9358
Systems: HPE / Dell / Cisco UCS / Supermicro / APC
Network: Cisco / Aruba / Juniper / Fortinet / APC / Opengear
Optical: Transceivers / DAC / AOC / Cables / DWDM Line Systems
Service: Systain Third Party Maintenance / Professional Services
```

If this signature ever needs to change, update it here AND in all send steps below.

---

## Step 1: Gather Prospect Info

Ask Brian to paste or provide:
- Full name
- Title
- Company and domain
- Email address
- Any context he has (pain points, source, notes)

If Brian pastes a HubSpot contact record, extract all fields directly from it.

---

## Step 2: Research the Prospect

Before writing a single word, research the company and role:

- Use web search to find what the company does, their scale, tech stack if public, any recent news
- Identify what infrastructure problems are most likely for someone in their role at their company size
- Think about which OSI pillar fits best:
  - **Network/telecom/colocation** → TPM + hardware lifecycle angle
  - **Software/cloud/SaaS** → optics, high-density connectivity, speed to deploy
  - **Financial services** → reliability, compliance, EOL risk mitigation
  - **Enterprise IT/infrastructure title** → all pillars apply, lead with TPM cost savings
- Note 1-2 specific, concrete details to weave into Email 1 so it feels researched, not templated

---

## Step 3: Write the 7-Email Sequence

Write all 7 emails before doing anything else. Use Brian's voice throughout:
direct, no-nonsense, outcomes over transactions, zero corporate fluff.

### Email 1 — Cold Intro (Day 0)
- 3-4 short paragraphs max
- Open with what problem you solve for people in their role
- Reference something specific about their company or industry (from research)
- One clear ask: 15-minute call
- End the body with just 'Brian' on its own line — the send steps will clear any Outlook auto-signature and append the correct signature block automatically

### Email 2 — Different Angle (Day 4)
- Pivot to a different OSI capability than Email 1 (optics if Email 1 was TPM, or vice versa)
- Do not repeat what was in Email 1
- 2-3 short paragraphs
- No hard ask — soft "worth a conversation if..."

### Email 3 — Soft Touch (Day 10)
- Acknowledge the silence without being apologetic
- Reference a pattern you see at companies like theirs (without namedropping)
- Offer them an easy out — "if timing is off, just say the word"
- 2-3 short paragraphs

### Email 4 — Swag & Sample SFPs / Address Confirm (Day 12)
- Subject is always: **Re: Confirming address** (new email, not a literal reply — the subject line makes it look like a follow-up in their inbox)
- Body is always the same — do not personalize or change it:

> I'm just prepping this package for you. I have a box of swag and a pair of sample SFPs to send to you from the team here at OSI Global IT.
>
> Do you come into the office? Is that the best address to send it to right now?

- End the body with just 'Brian' on its own line — the send steps handle the signature
- This email works because it creates a reason to reply that has nothing to do with a sales pitch
- If they reply with an address, pause all remaining scheduled tasks and follow up on the shipment

### Email 5 — "Any thoughts?" (Day 14)
- This email is ALWAYS the same: reply in original thread, two words only
- Body: **Any thoughts?**
- Nothing else. No greeting, no signature, no additional text.
- This is sent as a REPLY to Email 1's thread, not a new email

### Email 6 — Pattern Interrupt (Day 18)
- Ask a single direct yes/no question about their specific environment
- EOL gear, contract renewals, optics gaps — pick the most relevant one based on research
- 2-3 sentences only
- "If yes, worth talking. If no, I'll stop bothering you."

### Email 7 — Breakup (Day 28)
- Short, respectful, leaves the door open
- Acknowledge you've sent several notes, respect their time
- No pitch. Just close the loop and give them an easy way back in.
- End the body with just 'Brian' on its own line — the send steps handle the signature

---

## Step 4: Humanize Every Email

Apply these rules to every email before finalizing:

- **No AI vocabulary**: remove "crucial," "pivotal," "landscape," "underscore," "delve," "showcase," "testament," "enhance," "foster," "garner"
- **No hyphens**: rewrite any hyphenated phrases (e.g. "end of life" not "end-of-life", "24/7/365" not "24-hour")
- **No em dashes**: replace with commas or periods
- **No rule of three**: break up any triple-item lists into natural prose
- **No -ing pileup**: avoid "highlighting," "ensuring," "reflecting," "contributing to" tacked onto sentences
- **No negative parallelisms**: avoid "it's not just X, it's Y"
- **Vary sentence length**: mix short punchy sentences with longer ones
- **Use "is/are/has"** instead of "serves as," "stands as," "functions as"
- **Read every email aloud mentally** — if it sounds like a press release, rewrite it

After applying, do a final check: "What makes this obviously AI-generated?" Fix whatever you find.

---

## Step 5: Generate Subject Lines

For each email EXCEPT Email 4 (fixed subject: "Re: Confirming address") and Email 5 (reply, inherits original subject):
- Write 5 subject line options
- Mix: 2-3 professional/catchy + 2 outlandish/unexpected
- No hyphens in subject lines
- Randomly select one of the 5 for use when sending
- Present all 5 to Brian with the selected one clearly marked

---

## Step 6: Generate Call Scripts + HubSpot Note + LinkedIn Task

Do this step automatically after the emails are written — before presenting anything to Brian for review. No input from Brian needed; just execute all four sub-steps in order.

### 6a — Write the Voicemail Script

Write a personalized voicemail script for this prospect. Target 25 seconds or less when read aloud (~60-70 words). Use this structure:

- **"Hey [First Name], this is Brian Charrette from OSI Global IT..."**
- One sentence on why you're calling — tie it to something specific about their role or company (use the research from Step 2)
- One OSI capability most relevant to their environment
- Callback number (Brian's direct line) and a soft reason to call back
- Conversational tone — this should sound like a real voicemail, not a sales script

Apply the same humanization rules from Step 4: no AI vocabulary, no em dashes, no rule of three. Read it aloud mentally — if it sounds like a recording, rewrite it.

### 6b — Write the Live Call Script

Write a live call script for when the prospect actually picks up. Structure it as follows:

**Opening:**
> "Hey [First Name] — Brian Charrette, OSI Global IT. Did I catch you at a bad time?"

**30-second pitch (if they stay on):**
- What OSI does for companies like theirs, in plain language
- The single most relevant proof point for their role (TPM savings, optics speed, EOL coverage — pick one based on research)
- One qualifying question to open the conversation

**If they're interested:** Ask for 15 minutes on the calendar.

**Objection handlers (one sentence each):**
- "Send me info" → "Sure — what's the best email? I'll keep it short."
- "Not interested" → "Fair enough — is it timing, or just not a fit right now?"
- "We use OEMs" → "That's most of our customers before they switch. What's your renewal cycle look like?"

**Close:**
> "I'll shoot you a quick email right after so you have my info."

Apply the same humanization rules from Step 4. This should sound like Brian actually talks.

### 6c — Create HubSpot Note on the Contact Record

Using `mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__manage_crm_objects`, create a Note on the contact record.

**Note body must follow this exact format — plain text only, no markdown:**

```
VOICEMAIL SCRIPT
[Full voicemail script text]


LIVE CALL SCRIPT
[Full live call script text — opening, pitch, objection handlers, close]
```

Two blank lines between the voicemail section and the live call section. HubSpot notes don't render markdown, so keep it plain text.

**If the contact doesn't exist in HubSpot yet:** Create the contact first (name, email, company, title from Step 1), then create the note and associate it.

**If the contact already exists:** Look them up by email, get their contact ID, and associate the note to that ID.

### 6d — Create LinkedIn Connection Task in HubSpot

Write a LinkedIn connection message for this prospect. Keep it under 300 characters (LinkedIn's hard limit for connection requests). Personalize it — reference something specific about their role or company. No pitch. Brian's voice: direct, warm, not salesy. The goal is to get connected, not to sell on the first touch.

Then create a HubSpot Task on the contact using `mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__manage_crm_objects`:

- **Title:** `LinkedIn Connection — [First Name] [Last Name]`
- **Type:** TODO
- **Due date:** Today
- **Priority:** HIGH
- **Body/notes:** [The LinkedIn connection message]
- Associate the task with the contact record

After completing all four sub-steps, confirm in chat: "HubSpot note added (voicemail + call scripts). LinkedIn connection task created."

---

## Step 7: Present for Review — Wait for "Run"

After completing Steps 1 through 6, present all 7 emails to Brian in full. For each email show:
- Email number and day in the sequence
- All 5 subject line options with the selected one clearly marked
- Full email body

Then show the proposed send schedule as a table, with BOTH the raw cadence day AND the final computed weekday-only send date.

**Stop completely. Do not send. Do not schedule. Wait.**

End with: "Look it over and say **run** when you're ready."

---

## Step 8: On "Run" — Send Email 1 Immediately, Then Queue the Rest

When Brian says "run" (or any clear go-ahead like "send it", "looks good", "do it"):

### 8a — Pre-flight check: Outlook session must be live

Before doing anything else, open Chrome and navigate to https://outlook.office.com. If a sign-in screen appears, STOP and tell Brian: "Chrome Outlook session is expired — sign in before I run this sequence." Do not proceed until the session is live. This prevents the silent-failure mode where tasks fire but emails never send.

### 8b — Send Email 1 Right Now via Chrome

Send Email 1 immediately using Outlook in the browser. No scheduling — send it live right now:

1. In the already-open Outlook tab, click New mail
2. In the To field, type the prospect's email address and press Tab
3. Click "Bcc" in the compose header to reveal the BCC field, then in that field type exactly: bc@osihardware.com, 21878985@bcc.hubspot.com and press Tab. Confirm both pills appear in the BCC line before continuing.
4. Click the Subject field and type the selected subject line exactly
5. Click anywhere in the email body area. Press Ctrl+A to select all text (this clears any Outlook auto-signature), then press Delete.
6. Type the email body exactly as written, then press Enter twice and type the following signature exactly:

Brian Charrette
Director of Key Accounts
Desk: 805.845.5167 | Cell: 805.682.9358
Systems: HPE / Dell / Cisco UCS / Supermicro / APC
Network: Cisco / Aruba / Juniper / Fortinet / APC / Opengear
Optical: Transceivers / DAC / AOC / Cables / DWDM Line Systems
Service: Systain Third Party Maintenance / Professional Services

7. Click Send
8. Confirm the email was sent before moving on to scheduling

BCC on every send covers both records at once. bc@osihardware.com puts a copy in Brian's inbox so he can see the send actually fired. 21878985@bcc.hubspot.com auto-logs the email to the HubSpot contact timeline. No extension, no integration sign-in required. If Brian's BCC tracking addresses ever change, update them in Step 8b (live Email 1 send) AND the queue entry `bcc` field used by all 6 queued emails in Step 8d.

### 8c — Compute Weekday + Holiday-Safe Send Dates for Emails 2 Through 7

**CRITICAL RULE: No email is ever allowed to fire on a Saturday, Sunday, or a US federal / B2B-observed holiday.**

Base cadence (business days from Day 0, where Day 0 is today — the day Brian said "run"):

| # | Days from Day 0 | Send window (PT) | Type |
|---|---|---|---|
| 2 | +4 bd | 11am | Different angle |
| 3 | +10 bd | 12pm | Soft touch |
| 4 | +12 bd | 1pm | Swag / address confirm |
| 5 | +14 bd | 2pm | "Any thoughts?" reply |
| 6 | +18 bd | 3pm | Pattern interrupt |
| 7 | +28 bd | 4pm | Breakup |

The send windows map to the master `osi-email-sender` scheduled task, which sweeps the queue at 11am / 12pm / 1pm / 2pm / 3pm / 4pm PT every weekday. The master sender dedupes per-recipient (max one send per recipient per day) so any catch-up of overdue entries can't fire duplicates.

**Weekend + holiday skip — apply to every computed sendDate:**

1. Compute the raw date by adding the business-day count from Day 0 (skipping weekends automatically).
2. If the result lands on a US federal or B2B-observed holiday, push to the next business day.

**Holidays to avoid:** New Year's Day, MLK Day, Presidents Day, Good Friday, Memorial Day, Juneteenth, Independence Day, Labor Day, Columbus Day, Veterans Day, Thanksgiving, Black Friday, Christmas Eve, Christmas Day, New Year's Eve.

Hardcoded 2026: Jan 1 Thu, Jan 19 Mon, Feb 16 Mon, Apr 3 Fri, May 25 Mon, Jun 19 Fri, Jul 3 Fri, Sep 7 Mon, Oct 12 Mon, Nov 11 Wed, Nov 26 Thu, Nov 27 Fri, Dec 24 Thu, Dec 25 Fri, Dec 31 Thu.

Print the proposed schedule in chat with both raw cadence day and final shifted send date for Brian to eyeball before queueing.

### 8d — Append Emails 2-7 to email-queue.json

**Queue file:** `C:\Users\Mini\Documents\osi-claude-brain\automation\email-queue.json`

This is the single source of truth for all outbound sequence sends. The master `osi-email-sender` scheduled task reads this queue every weekday at 11am / 12pm / 1pm / 2pm / 3pm / 4pm PT and sends whatever's due in that window, with hard dedup so a recipient never gets more than one email per calendar day.

**Do NOT create individual Cowork scheduled tasks for emails.** That was the old architecture, which caused duplicate sends every time the machine was off and a stack of past-due tasks fired all at once when it came back. The queue + master sender model is retry-safe and dedup-safe.

**Queue entry schema — one entry per email (6 total: Emails 2 through 7):**

```json
{
  "id": "[firstname]-[lastname]-[company-slug]-email-[N]",
  "to": "prospect@company.com",
  "bcc": "bc@osihardware.com, 21878985@bcc.hubspot.com",
  "subject": "[selected subject line — or 'Re: Confirming address' for Email 4 — or empty string for Email 5 which is a reply]",
  "body": "[full body text, exactly as written, no signature — the master sender appends the canonical signature block]",
  "sendDate": "YYYY-MM-DD",
  "sendTime": "11am | 12pm | 1pm | 2pm | 3pm | 4pm",
  "status": "pending",
  "isReply": false,
  "emailNumber": 2,
  "cadenceGap": 4,
  "priorEmailId": "[firstname]-[lastname]-[company-slug]-email-1",
  "sequenceId": "[firstname]-[lastname]-[company-slug]",
  "addedDate": "[today YYYY-MM-DD]"
}
```

**Special fields per email:**

- **Email 4 (swag/address confirm):** `subject: "Re: Confirming address"`, `isReply: false`, body is the fixed swag/SFP text (see Step 3 Email 4). No personalization. Cadence gap from Email 3: 2 bd.
- **Email 5 ("Any thoughts?"):** `isReply: true`, `subject: ""`, `body: "Any thoughts?"`. The master sender will find the oldest Sent Item to this recipient and click Reply on it. No signature on this one. Cadence gap from Email 4: 2 bd.
- **Email 7 (breakup):** Cadence gap from Email 6: 10 bd.

`cadenceGap` is the business-day gap from the prior email. The master sender uses this to self-heal the cadence: when it fires email N, it updates email N+1's `sendDate` to `[today + cadenceGap business days, skipping weekends and holidays]`. That means if email 3 slips a day for any reason, email 4 automatically shifts a day later too — the gap stays intact instead of compressing.

**Dedup before append — required:**

Before appending, scan the existing queue for entries where `to` matches this prospect's email (case-insensitive). If any have `status: "pending"` or `status: "sent"` within the last 30 days, STOP and tell Brian: "SKIPPED: [Name] is already enrolled or recently completed a sequence. Override?" Wait for explicit "override" before proceeding.

This prevents the bug where running this skill twice on the same prospect doubles up the queue.

**Queue write — OneDrive-safe Python pattern (no permission prompts, atomic):**

```python
import json, os

QUEUE = r'C:\Users\Mini\Documents\osi-claude-brain\automation\email-queue.json'

# 1. Read existing queue
with open(QUEUE, 'r') as f:
    queue = json.load(f)

# 2. Build the 6 new entries (Emails 2 through 7)
new_entries = [ ... ]  # list of entry dicts per schema above

# 3. Dedup by id (prevents accidental re-add on rerun)
existing_ids = {e.get('id') for e in queue}
to_add = [e for e in new_entries if e['id'] not in existing_ids]
queue.extend(to_add)

# 4. Atomic write
tmp = QUEUE + '.tmp'
with open(tmp, 'w') as f:
    json.dump(queue, f, indent=2)
os.replace(tmp, QUEUE)
```

Do NOT use the MCP Write tool — its prior-Read requirement breaks on cloud-synced files. Do NOT delete the file first.

### 8e — Confirm

After the write, confirm in chat:

- `Email 1 sent to [prospect@email] at [HH:MM PT] with BCC tracking.`
- `6 emails queued (Emails 2-7) at [sendDate 1] / [2] / [3] / [4] / [5] / [6]. Master osi-email-sender will pick them up at the right PT window.`
- `LinkedIn task synced to today: [date].`
- `Call script + voicemail live on HubSpot contact note.`

---

## Step 9: Save Markdown Reference File

Use the Write tool to save [lastname]-[company]-sequence.md to the user's Email folder.
Include the schedule table at top, then each email with all 5 subject options and full body.
Do NOT use the docx skill for sequence files.

---

## Step 10: Confirm and Hand Off

Present Brian with:
1. Link to the Word doc
2. The full schedule table (all 7 emails, weekdays, dates, subjects) — confirm again that zero dates fall on Sat/Sun
3. Note: if the prospect replies at any point, delete the remaining scheduled tasks from the Cowork Scheduled sidebar

---

## OSI Messaging Reference

**Lead with the right pillar by role:**
- Network/Infrastructure Architect, Network Engineer → TPM cost savings + hardware lifecycle + EOL support
- Director/VP of IT → OpEx reclamation, vendor simplification, budget control
- Data Center / Colo roles → optics, Smartoptics 800G, open line systems, fast fulfillment
- Procurement / Finance → 50-80% savings vs OEM, Gartner-recognized credibility

**Core proof points to weave in naturally (pick 1-2 per sequence, not all of them):**
- 24/7/365 TAC coverage at roughly half of OEM pricing (Systain TPM)
- Same-day fulfillment — 6,000+ DIMMs shipped same-day
- Transceivers 1G to 400G, coded for 40+ OEM platforms, including custom builds OEMs won't make
- Largest global Smartoptics partner — 800G transponders in stock
- EOL product support long after OEM walks away
- Privately owned — no quarterly targets, no investor pressure, answers to clients only

**Brian's voice — always:**
- Direct, no-nonsense, outcomes over transactions
- Short emails — 3-4 paragraphs max, most under 100 words
- First person, specific, no corporate language
- Candid: if something isn't relevant, say so
- Confident but not aggressive
