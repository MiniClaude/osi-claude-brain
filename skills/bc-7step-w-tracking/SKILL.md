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

## Step 8: On "Run" — Send Email 1 Immediately, Then Schedule the Rest

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

BCC on every send covers both records at once. bc@osihardware.com puts a copy in Brian's inbox so he can see the send actually fired. 21878985@bcc.hubspot.com auto-logs the email to the HubSpot contact timeline. No extension, no integration sign-in required. If Brian's personal BCC address ever changes, update the two references in Step 7b and the task prompts in Step 7d.

### 8c — Compute Weekday-Only Send Dates for Emails 2 Through 7

**CRITICAL RULE: No email is ever allowed to fire on a Saturday or Sunday. No exceptions.**

Reason: Scheduled tasks in Cowork only fire when the desktop app is running. Brian's machine is typically off on weekends, so weekend tasks queue up and fire in a burst on Monday morning, often before Chrome/Outlook is open and signed in. That causes the browser automation to fail silently: the task fires, lastRunAt gets set, but no email goes out. Beyond the technical failure, Brian doesn't want prospects receiving emails stamped with weekend timestamps either.

Base cadence (days from Day 0, where Day 0 is today — the day Brian said "run"):
- Email 2: Day 0 + 4 days, 9:00 AM Pacific
- Email 3: Day 0 + 10 days, 9:00 AM Pacific
- Email 4: Day 0 + 12 days, 9:00 AM Pacific
- Email 5: Day 0 + 14 days, 9:00 AM Pacific (reply in original thread)
- Email 6: Day 0 + 18 days, 9:00 AM Pacific
- Email 7: Day 0 + 28 days, 9:00 AM Pacific

**Weekend-skip logic — apply to every computed fireAt:**

1. Compute the raw date from the base cadence above.
2. Check the day of the week:
   - Monday through Friday → keep the date as-is
   - Saturday → push forward to the following Monday (same 9:00 AM PT)
   - Sunday → push forward to the following Monday (same 9:00 AM PT)
3. If two adjacent emails now collide on the same Monday (e.g., Email 3 Sat and Email 4 Sun both got pushed to the same Monday), keep them on that Monday but stagger the send times by 5 minutes each (9:00, 9:05, 9:10, etc.).
4. Before creating each task, state the final fireAt in chat: "Email 3 → Mon 4/27 @ 9:00 AM PT (originally Sat 4/25, shifted to next weekday)". Brian should be able to visually confirm every date is a weekday.

**Timezone offsets:** Use -07:00 April through October, -08:00 November through March.

### 8d — Create the Scheduled Tasks

**Task ID format:** `[firstname]-[lastname]-[company-slug]-email-[N]`
Example: `jane-smith-acme-email-2`

Use `mcp__scheduled-tasks__create_scheduled_task` with the computed weekday-only fireAt for each task.

**Task prompt for Emails 2, 3, 6, 7 (new emails):**

```
Send an email to [NAME] at [COMPANY] using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, STOP and notify Brian via a notification — do not attempt to send the email. Also create a todo in the task list titled "Outlook session expired — resend [NAME] Email [N]" so Brian can recover manually.
3. Click New mail
4. In the To field, enter: [EMAIL ADDRESS] and press Tab
5. Click "Bcc" in the compose header to reveal the BCC field, then in that field type exactly: bc@osihardware.com, 21878985@bcc.hubspot.com and press Tab. Confirm both pills appear before continuing.
6. Click the Subject field and enter exactly: [SUBJECT LINE]
7. Click anywhere in the email body area. Press Ctrl+A to select all text (clears any Outlook auto-signature), then press Delete.
8. Type the following exactly:

[EMAIL BODY]

Then press Enter twice and type the following signature exactly:

Brian Charrette
Director of Key Accounts
Desk: 805.845.5167 | Cell: 805.682.9358
Systems: HPE / Dell / Cisco UCS / Supermicro / APC
Network: Cisco / Aruba / Juniper / Fortinet / APC / Opengear
Optical: Transceivers / DAC / AOC / Cables / DWDM Line Systems
Service: Systain Third Party Maintenance / Professional Services

9. Click Send
10. Verify the email appears in Outlook Sent Items within the last 2 minutes. If it is not found, report failure and stop.
11. Confirm the email was sent and report back.

Do not modify the email body in any way.
```

**Task prompt for Email 4 (swag/address confirm):**

```
Send an email to [NAME] at [COMPANY] using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, STOP and notify Brian via a notification — do not attempt to send the email. Also create a todo in the task list titled "Outlook session expired — resend [NAME] Email 4" so Brian can recover manually.
3. Click New mail
4. In the To field, enter: [EMAIL ADDRESS] and press Tab
5. Click "Bcc" in the compose header to reveal the BCC field, then in that field type exactly: bc@osihardware.com, 21878985@bcc.hubspot.com and press Tab. Confirm both pills appear before continuing.
6. Click the Subject field and enter exactly: Re: Confirming address
7. Click anywhere in the email body area. Press Ctrl+A to select all text (clears any Outlook auto-signature), then press Delete.
8. Type the following exactly:

I'm just prepping this package for you. I have a box of swag and a pair of sample SFPs to send to you from the team here at OSI Global IT.

Do you come into the office? Is that the best address to send it to right now?

Brian

Then press Enter twice and type the following signature exactly:

Brian Charrette
Director of Key Accounts
Desk: 805.845.5167 | Cell: 805.682.9358
Systems: HPE / Dell / Cisco UCS / Supermicro / APC
Network: Cisco / Aruba / Juniper / Fortinet / APC / Opengear
Optical: Transceivers / DAC / AOC / Cables / DWDM Line Systems
Service: Systain Third Party Maintenance / Professional Services

9. Click Send
10. Verify the email appears in Outlook Sent Items within the last 2 minutes. If it is not found, report failure and stop.
11. Confirm the email was sent and report back.
```

**Task prompt for Email 5 ("Any thoughts?" — reply in original thread):**

```
Send a reply to [NAME] at [COMPANY] using Outlook. This must be a REPLY in the original thread, not a new email.

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, STOP and notify Brian via a notification — do not attempt to send the email. Also create a todo in the task list titled "Outlook session expired — resend [NAME] Email 5" so Brian can recover manually.
3. Go to Sent Items
4. Find the oldest email sent to [EMAIL ADDRESS] — that is the original cold outreach
5. Open it and click Reply
6. Press Ctrl+A to select all body text (including any auto-inserted signature), then press Delete — this email has no signature at all.
7. Click "Bcc" in the compose header to reveal the BCC field, then in that field type exactly: bc@osihardware.com, 21878985@bcc.hubspot.com and press Tab. Confirm both pills appear before continuing.
8. Type only: Any thoughts?
9. Do not add any greeting, signature, or additional text
10. Click Send
11. Verify the reply appears in Outlook Sent Items within the last 2 minutes. If it is not found, report failure and stop.
12. Confirm the reply was sent and report back.
```

Set `notifyOnCompletion: true` on all tasks.

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