---
name: aaa-hubspot-7-step
description: >
  Generate 1 to 7 personalized outreach emails for any OSI Global prospect and save them to the
  AI Email Subject 1-7 and AI Email Body 1-7 fields on the HubSpot contact record.

  ALWAYS use this skill when Brian says "AAA Hubspot 7 STEP", "aaa hubspot 7 step", "7 step",
  "generate 7 emails for [contact]", "populate the AI email fields with 7", "save 7 emails to
  the contact", "fill in the AI email fields on", or pastes a contact email and LinkedIn URL and
  wants 7 emails written and stored in HubSpot. Triggers on any request to generate a 7-email
  numbered outreach sequence and save them directly to HubSpot contact properties.
---

# OSI Global AI Email Fields Generator (AAA Hubspot 7 STEP)

Generates 1 to 7 personalized outreach emails for a prospect and writes them to the
AI Email Subject 1-7 and AI Email Body 1-7 properties on their HubSpot contact record.

---

## Step 1: Collect Inputs

You need:
- **Contact email address** (required — used to find the HubSpot record)
- **LinkedIn profile URL** (optional but use it if provided)
- **Number of emails** (1 to 7 — default to 7 if not specified)
- Any context Brian has about the prospect (pain points, source, prior interactions)

If a LinkedIn Sales Navigator URL is provided, navigate to it in Chrome to extract the
prospect's title, company, and background before writing anything.

---

## Step 2: Look Up the HubSpot Contact

Search HubSpot contacts by email address. Pull:
- First name, last name, title, company
- Any existing notes or activity that might inform tone

If the contact does not exist in HubSpot, create it before saving the email fields at the end.

---

## Step 3: Research the Prospect

Before writing a single word, do real research:

- Web search the company: what they do, their scale, recent news, tech stack if public
- Identify the prospect's likely infrastructure pain points based on their role and industry
- Pick the OSI angle(s) that fit best (see Messaging Reference below)
- Find 1 to 2 specific details to make Email 1 feel researched, not templated

If a LinkedIn URL was provided and Chrome is available, navigate to it and read the profile
for career history, tenure, and role specifics.

---

## Step 4: Write the Emails

Write all emails before saving anything. Number them 1 through N (where N is the count Brian
requested). Use Brian's voice throughout: direct, short, outcomes over transactions, zero fluff.

### Email 1 — Cold Intro
- 3 to 4 short paragraphs
- Open with the problem you solve for someone in their role
- Reference something specific about their company or role (from research)
- One clear ask: a 15-minute call
- No sign-off — Outlook signature handles it

### Email 2 — Different Angle (if N >= 2)
- Lead with a different OSI capability than Email 1
- 2 to 3 paragraphs
- Soft close — "worth a conversation if..."

### Email 3 — Soft Touch (if N >= 3)
- Acknowledge the silence without being apologetic
- Reference a pattern you see at companies like theirs
- Give them an easy out
- 2 to 3 paragraphs

### Email 4 — Swag & Sample SFPs / Address Confirm (if N >= 4)
**Subject is always:** Re: Confirming address

**Body is always (do not personalize or change):**
> I'm just prepping this package for you. I have a box of swag and a pair of sample SFPs to
> send to you from the team here at OSI Global IT.
>
> Do you come into the office? Is that the best address to send it to right now?

### Email 5 — "Any thoughts?" (if N >= 5)
**Body is always:** Any thoughts?

Store the subject as: Re: [subject from Email 1]

### Email 6 — Social Proof / Customer Win (if N >= 6)
- Lead with a brief, specific customer success story relevant to their role or vertical
- Keep it under 3 paragraphs — one sentence on the customer situation, one on what OSI did, one on the outcome
- Do NOT name the customer by name unless it is publicly known — use "a [type] company" instead
- End with a single question: something like "Would a similar approach make sense at [Company]?"
- Pick the story that maps closest to this prospect's pain point from the OSI proof points below

**Story angles to draw from (pick the most relevant one):**
- A regional fiber provider saved 60%+ on SFPs by switching from Cisco-branded to OSI-coded optics
- A state government IT team extended life on EOL Cisco gear 3 years past end of support with Systain TPM
- A university network team solved a DDR4 shortage same-day with OSI's fulfillment bench
- A data center operator deployed 800G open-line transport with Smartoptics at a fraction of OEM cost
- A telecom upgraded legacy routers to APC/Eaton power protection without a forklift upgrade

### Email 7 — Breakup / Close the Loop (if N >= 7)
- Short: 2 to 3 sentences max
- Acknowledge you've reached out several times, no pressure, understand if timing is off
- Leave the door open without groveling — you can circle back when something changes
- Do not apologize for reaching out
- End with a light question like "Is it just not the right time?" or just leave it open

**Example tone (do not copy verbatim):**
> I've sent a few notes your way. No response usually means either the timing's off or it's not
> a fit — either is fine.
>
> If things change on your end, I'm easy to find. Is it just not the right time?

---

## Step 5: Humanize Every Email

Apply before finalizing. Check every email:

- **No AI vocabulary**: remove "crucial," "pivotal," "landscape," "underscore," "delve,"
  "showcase," "testament," "enhance," "foster," "garner"
- **No dashes**: rewrite hyphenated phrases ("end of life" not "end-of-life"), no em dashes,
  no en dashes — use commas or periods instead
- **No rule of three**: break triple lists into natural prose
- **No -ing pileup**: avoid gerunds tacked onto sentence ends
- **Vary sentence length**: short punchy sentences mixed with longer ones
- **Use "is/are/has"** instead of "serves as," "stands as," "functions as"
- Read each email mentally out loud — if it sounds like a press release, rewrite it

---

## Step 6: Generate Subject Lines

For each email except Email 4 (fixed: "Re: Confirming address") and Email 5 (reply thread):
- Write 5 subject line options
- Mix: 2 to 3 professional/specific + 2 unexpected/pattern-interrupt
- No dashes in subject lines
- Mark one as selected (most likely to get opened given the prospect's role)

Email 7 subject line should feel like a final note, not a pitch — something quiet and direct.

---

## Step 7: Present for Review — Wait for Confirmation

Show Brian all emails in full. For each:
- Email number
- All 5 subject options with selected one marked
- Full body

Then ask: "Look good? Say **save** to write these to HubSpot."

Do not save anything until Brian confirms.

---

## Step 8: Save to HubSpot

Update the contact record with all generated emails:

| Email # | Subject Property     | Body Property     |
|---------|---------------------|-------------------|
| 1       | ai_email_subject_1  | ai_email_body_1   |
| 2       | ai_email_subject_2  | ai_email_body_2   |
| 3       | ai_email_subject_3  | ai_email_body_3   |
| 4       | ai_email_subject_4  | ai_email_body_4   |
| 5       | ai_email_subject_5  | ai_email_body_5   |
| 6       | ai_email_subject_6  | ai_email_body_6   |
| 7       | ai_email_subject_7  | ai_email_body_7   |

Show Brian a confirmation table before calling the HubSpot update tool. Wait for approval,
then update the contact record in a single API call.

After saving, confirm with a link to the contact record in HubSpot.

---

## OSI Messaging Reference

**Lead with the right angle based on role:**

- Network/Infrastructure Engineer or Architect: TPM cost savings + hardware lifecycle + EOL support
- Director/VP of IT: OpEx reclamation, vendor simplification, budget control
- Data Center / Colo roles: optics, Smartoptics 800G, open line systems, fast fulfillment
- Telecom / Utility Communications: TPM for mission-critical aging gear + optics for fiber networks
- Procurement / Finance: 50 to 80 percent savings vs OEM, Gartner-recognized credibility

**Core proof points (pick 1 to 2 per sequence, not all):**
- 24/7/365 TAC coverage at roughly half OEM pricing (Systain TPM)
- Same-day fulfillment — 6,000+ DIMMs shipped same-day
- Transceivers 1G to 400G, coded for 40-plus OEM platforms including custom builds OEMs will not make
- Largest global Smartoptics partner — 800G transponders in stock
- EOL product support long after OEM walks away
- Privately owned — no quarterly targets, answers to clients only

**Brian's voice — always:**
- Direct, no-nonsense, outcomes over transactions
- Short emails — 3 to 4 paragraphs max, most under 100 words
- First person, specific, no corporate language
- Confident but not aggressive
- Never uses em dashes, en dashes, or hyphens in prose
