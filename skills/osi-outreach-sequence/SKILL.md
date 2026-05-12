---
name: osi-outreach-sequence
description: >
  Build and fully automate a 7-email cold outreach sequence for any OSI Global prospect.
  ALWAYS use this skill when Brian says "run a sequence", "outreach sequence", "set up emails for",
  "automate outreach to", "build a sequence for", or pastes a HubSpot contact record or LinkedIn
  profile and wants emails sent automatically. This skill writes all 7 emails, humanizes them,
  picks random subject lines, presents everything for Brian's review, then on "run" sends Email 1
  immediately via Outlook and schedules the remaining 6 automatically. It replaces any manual
  email drafting or HubSpot sequence building.
---

# OSI Global Outreach Sequence

Generates and fully automates a personalized 7-email outreach sequence for any prospect.
Brian reviews everything first. When he says "run", Email 1 goes out immediately and the rest schedule automatically.

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
- Outlook signature handles the sign-off — do not include name/contact at the end

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

- Outlook signature handles the sign-off — do not add name/contact manually
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
- Outlook signature handles the sign-off

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

## Step 6: Present for Review — Wait for "Run"

After completing Steps 1 through 5, present all 7 emails to Brian in full. For each email show:
- Email number and day in the sequence
- All 5 subject line options with the selected one clearly marked
- Full email body

Then show the proposed send schedule as a table.

**Stop completely. Do not send. Do not schedule. Wait.**

End with: "Look it over and say **run** when you're ready."

---

## Step 7: On "Run" — Send Email 1 Immediately, Then Schedule the Rest

When Brian says "run" (or any clear go-ahead like "send it", "looks good", "do it"):

### 7a — Send Email 1 Right Now via Chrome

Send Email 1 immediately using Outlook in the browser. No scheduling — send it live right now:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify Brian
3. Click New mail
4. In the To field, type the prospect's email address and press Tab
5. Click the Subject field and type the selected subject line exactly
6. Click in the body area above the signature and type the email body exactly as written
7. Click Send
8. Confirm the email was sent before moving on to scheduling

HubSpot Sales extension is installed in this browser — the send logs automatically to HubSpot.

### 7b — Schedule Emails 2 Through 7

After Email 1 is confirmed sent, use `mcp__scheduled-tasks__create_scheduled_task` to schedule the remaining 6. Day 0 is today (the day Brian said "run").

**Task ID format:** `[firstname]-[lastname]-[company-slug]-email-[N]`
Example: `jane-smith-acme-email-2`

**Timing (9:00 AM Pacific — use -07:00 offset April through October, -08:00 November through March):**
- Email 2: Day 0 + 4 days, 9:00 AM
- Email 3: Day 0 + 10 days, 9:00 AM
- Email 4: Day 0 + 12 days, 9:00 AM
- Email 5: Day 0 + 14 days, 9:00 AM (reply in original thread)
- Email 6: Day 0 + 18 days, 9:00 AM
- Email 7: Day 0 + 28 days, 9:00 AM

**Task prompt for Emails 2, 3, 6, 7 (new emails):**

```
Send an email to [NAME] at [COMPANY] using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: [EMAIL ADDRESS] and press Tab
5. Click the Subject field and enter exactly: [SUBJECT LINE]
6. Click in the body area above the signature and type the following exactly:

[EMAIL BODY]

7. Click Send
8. Confirm the email was sent and report back

Do not modify the email body in any way.
```

**Task prompt for Email 4 (swag/address confirm):**

```
Send an email to [NAME] at [COMPANY] using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: [EMAIL ADDRESS] and press Tab
5. Click the Subject field and enter exactly: Re: Confirming address
6. Click in the body area above the signature and type the following exactly:

I'm just prepping this package for you. I have a box of swag and a pair of sample SFPs to send to you from the team here at OSI Global IT.

Do you come into the office? Is that the best address to send it to right now?

7. Click Send
8. Confirm the email was sent and report back
```

**Task prompt for Email 5 ("Any thoughts?" — reply in original thread):**

```
Send a reply to [NAME] at [COMPANY] using Outlook. This must be a REPLY in the original thread, not a new email.

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Go to Sent Items
4. Find the oldest email sent to [EMAIL ADDRESS] — that is the original cold outreach
5. Open it and click Reply
6. Clear any auto-populated body text (keep the signature if it appears)
7. Type only: Any thoughts?
8. Do not add any greeting, additional text, or change the subject line
9. Click Send
10. Confirm the reply was sent and report back
```

Set `notifyOnCompletion: true` on all tasks.

---

## Step 8: Build the Word Doc

Read the docx SKILL.md at `/sessions/focused-clever-keller/mnt/.claude/skills/docx/SKILL.md` and build a Word document with:

- Title: [Prospect Name] — [Company] Outreach Sequence
- Subtitle: role, 7-email sequence, 28-day cadence, automated via Outlook
- For each email: heading with email number + send date + timing note, all 5 subject lines with selected one marked, full email body
- Final section: sequence schedule summary table (email number, date, subject)
- Font: Calibri 11pt throughout
- Save to: `/sessions/focused-clever-keller/mnt/ Email/[lastname]-[company]-sequence.docx`

---

## Step 9: Confirm and Hand Off

Present Brian with:
1. Link to the Word doc
2. The full schedule table (all 7 emails, dates, subjects)
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
