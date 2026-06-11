---
name: aaa-outreach-personalized
description: >
  Build and fully automate a personalized 7-email outreach sequence for any OSI Global prospect.
  ALWAYS use this skill when Brian says "run a sequence", "outreach sequence", "AAA outreach",
  "personalized outreach", "set up emails for", "automate outreach to", "build a sequence for",
  or pastes a LinkedIn profile, contact info, or HubSpot record and wants outreach drafted or sent.
  This skill qualifies the prospect, researches via web + HubSpot, picks the right sequence type,
  writes 7 personalized emails, generates a call script and voicemail, creates HubSpot tasks,
  schedules everything automatically, and builds a Word doc summary. No ZoomInfo required.
---

# AAA Outreach Personalized

Generates and fully automates a personalized 7-email outreach sequence for any OSI Global prospect.
Brian reviews everything first. When he says "run", Email 1 goes out immediately and the rest schedule automatically.

Read this entire skill before producing any output.

---

## QUALIFICATION GATE — hard stop before anything else

Before writing a single word of outreach, review the prospect's full career history, current title, and company.

Ask yourself: "Why would this person care about TPM, optics, DIMMs, or DWDM?" Write that sentence. If it cannot be written with confidence, stop and tell Brian why, then ask if he wants to proceed anyway.

Roles that qualify: Network Engineer, Network Architect, Transport Engineer, Systems Engineer, Infrastructure Engineer, IT Director, DC Manager, IT Asset Manager, Procurement, CIO/CTO, Storage Admin, Storage Engineer, Optical Network Engineer.

Roles that don't qualify: Marketing, HR, Finance (unless procurement-adjacent), Sales, Legal, PR.

---

## Step 1: Gather Prospect Info

Ask Brian to provide or paste:
- Full name and title
- Company and domain
- Email address
- Any context (pain points, how he found them, notes)

If Brian pastes a HubSpot contact record or LinkedIn profile, extract all fields directly from it.

---

## Step 2: HubSpot Check

Search HubSpot by name and current company.

**OWNERSHIP CHECK — hard stop:**
If the contact is found and the hubspot_owner_id is NOT 213536174 (Brian):
> **OWNED BY ANOTHER REP:** [First Last] at [Company] is already in HubSpot owned by [rep name]. Do you want to proceed?

Wait for Brian's explicit instruction before continuing.

If contact is found and owned by Brian, note the existing record ID and any deal history — reference it when personalizing emails.

---

## Step 3: Research the Prospect

Use web search to research the company and the person's role. Look for:
- What the company does, their scale, tech stack if public
- Recent news: funding, acquisitions, data center buildouts, leadership changes
- OEM refresh signals, cost-cutting, vendor consolidation language
- 1-2 specific concrete details to weave into Email 1 so it feels researched, not templated

**Same-company stagger rule:** Check HubSpot and existing scheduled tasks for other contacts at the same company. If outreach is already running for someone there within the last 20 business days, push Day 0 out by 4 business days from the most recent sequence start at that company.

---

## Step 4: Determine Sequence Type

Based on role, title, and company — pick the best fit:

| Sequence     | Target Roles                                              | Lead Angle                          |
|---|---|---|
| Network      | Network Engineer, Architect, Transport Engineer           | Free SFP sample + optics supply chain |
| Server       | Systems Engineer, Infrastructure Engineer, Server Admin   | Free DIMM sample                    |
| TPM          | IT Director, DC Manager, IT Asset Manager, Procurement, CIO (mid-market) | OEM cost pain / EOL risk |
| DWDM         | Transport Engineer, Optical NE, Network Planner at carrier/CLEC/MSO | Cost vs Ciena/Nokia |
| Storage      | Storage Admin, Storage Engineer                          | Pre-owned NetApp + TPM              |
| Pre-owned    | Anyone managing Cisco/Juniper/Arista environments        | Pre-owned gear + OSI TPM            |

Note the sequence type — it drives Email 1's opener and the OSI pillar emphasis throughout.

---

## Step 5: Calculate Dates

Day 0 = today (the day Brian says "run").

**Send schedule:**
- Email 1: Day 0
- Email 2: Day 0 + 4
- Email 3: Day 0 + 10
- Email 4: Day 0 + 12
- Email 5: Day 0 + 14
- Email 6: Day 0 + 18
- Email 7: Day 0 + 28

All emails send at **9:00 AM Pacific**. Skip weekends — if a date lands on Saturday or Sunday, push to Monday.

**Pacific offset:** April through October = -07:00 / November through March = -08:00

---

## Step 6: Write All 7 Emails

Write every email before doing anything else. Use Brian's voice throughout: direct, no-nonsense, outcomes over transactions, zero corporate fluff. Short emails — 3 to 4 paragraphs max, most under 100 words. First person, specific, no corporate language.

---

### Email 1 — Cold Intro (Day 0)

**Network or Server sequence** — use the sample offer as the opener:

Network:
> Hi [First Name],
>
> I'm just prepping this package for you. I have a box of swag and a pair of sample SFPs to send from the team at OSI Global.
>
> Do you come into the office, or is there a better address to ship it to?

Server:
> Hi [First Name],
>
> I'd like to send you a sample DIMM from our current batch. Same spec as what you're running, manufacturer warranty, won't touch your OEM support contract.
>
> Do you come into the office, or is there a better address to ship it to?

**TPM, DWDM, Storage, Pre-owned sequences** — write a pain-led opener:
- 3 to 4 sentences max
- Open with the specific problem people in their role face at their company size
- Reference 1 concrete detail from research (company news, company scale, tech stack)
- One clear ask at the end: 15-minute call or quick question

Outlook signature handles the sign-off — do not add name/contact manually.

---

### Email 2 — Different Angle (Day 4)

Pivot to a different OSI capability than Email 1. If Email 1 was TPM, lead with optics or hardware. If Email 1 was optics, try TPM or DIMMs.

- 2 to 3 short paragraphs
- Do not repeat what was in Email 1
- Soft ask — "worth a conversation if..."
- Subject: RE: [same subject as Email 1] — this reads as a reply in their inbox

---

### Email 3 — Soft Touch (Day 10)

- Acknowledge the silence without being apologetic
- Reference a pattern you see at companies like theirs — without namedropping
- Offer an easy out: "if timing is off, just say the word"
- New subject line
- 2 to 3 short paragraphs

---

### Email 4 — Swag and Address Confirm (Day 12)

Subject is always: **Re: Confirming address**

Body is always the same — do not personalize or change it:

> I'm just prepping this package for you. I have a box of swag and a pair of sample SFPs to send to you from the team here at OSI Global IT.
>
> Do you come into the office? Is that the best address to send it to right now?

Outlook signature handles the sign-off — do not add name/contact manually.

This email works because it creates a reason to reply that has nothing to do with a sales pitch. If they reply with an address, pause all remaining scheduled tasks and follow up on the shipment.

---

### Email 5 — "Any thoughts?" (Day 14)

This email is always the same. Send as a REPLY to Email 1's thread — not a new email.

Body: **Any thoughts?**

Nothing else. No greeting, no signature, no additional text. The subject inherits from Email 1's thread.

---

### Email 6 — Pattern Interrupt (Day 18)

Ask one direct yes/no question about their specific environment. EOL gear, contract renewals, optics gaps — pick the most relevant one based on research and sequence type.

- 2 to 3 sentences only
- "If yes, worth talking. If no, I'll stop bothering you."
- New subject line

---

### Email 7 — Breakup (Day 28)

Short, respectful, leaves the door open. No pitch. Just close the loop and give them an easy way back in.

Examples:
- "Should I close the file on this one, or is the timing just off?"
- "No worries if now isn't the right time. Happy to circle back when things shift."

Outlook signature handles the sign-off. New subject line.

---

## Step 7: Humanize Every Email

Apply these rules to every email before finalizing:

- **No AI vocabulary**: remove "crucial," "pivotal," "landscape," "underscore," "delve," "showcase," "testament," "enhance," "foster," "garner"
- **No hyphens**: rewrite hyphenated phrases ("end of life" not "end-of-life", "24/7/365" not "24-hour")
- **No em dashes**: replace with commas or periods
- **No rule of three**: break up triple-item lists into natural prose
- **No -ing pileup**: avoid "highlighting," "ensuring," "reflecting," "contributing to" tacked onto sentences
- **No negative parallelisms**: avoid "it's not just X, it's Y"
- **Vary sentence length**: mix short punchy sentences with longer ones
- **Use "is/are/has"** instead of "serves as," "stands as," "functions as"
- **Read every email aloud mentally** — if it sounds like a press release, rewrite it

After applying, do a final check: "What makes this obviously AI-generated?" Fix whatever you find.

---

## Step 8: Generate Subject Lines

For each email EXCEPT Email 4 (fixed: "Re: Confirming address") and Email 5 (reply, inherits Email 1 subject):
- Write 5 subject line options
- Mix: 2 to 3 professional/direct + 2 unexpected/pattern-interrupt
- No hyphens in subject lines
- Randomly select one of the 5 for use when sending
- Present all 5 to Brian with the selected one clearly marked

---

## Step 9: Write Call Script and Voicemail

Format exactly:

```
SEQUENCE TYPE: [Network / Server / TPM / DWDM / Storage / Pre-owned]
HOOK: [Company news or personal trigger in one sentence. If nothing: none — using library opener]
OPENER: [Full opener from library below, or custom if HOOK is populated]
VM: [One line. Under 20 seconds. Phone at start and end. References Email 1 subject. Ends: "I'm sending you something this afternoon — subject line is [subject]. Worth a look. [phone]"]
```

### Call Opener Library

**Network Engineer — Telco / Service Provider**
"Hey [Name], how have you been? It's Brian with OSI Global. We supply ZR and ZR+ coherent optics to carrier teams as a secondary source when Cisco or Lumentum timelines slip. Is that something your team is running into right now?"

**Network Engineer — Bank / Financial Institution**
"Hey [Name], how have you been? It's Brian with OSI Global. We supply certified compatible optics to bank IT teams, mostly for the break-glass scenario where something fails and you can't wait two weeks for OEM. I was going to send a few complimentary SFPs your way. Would that be useful?"

**Network Engineer — Enterprise / Consulting**
"Hey [Name], how have you been? It's Brian with OSI Global. We work with enterprise IT teams on third party maintenance, specifically replacing OEM support on Cisco gear that is running fine but coming off warranty. Is that a conversation your team is having right now?"

**Network Engineer — Manufacturing**
"Hey [Name], how have you been? It's Brian with OSI Global. We supply certified compatible optics and networking spares to manufacturing IT teams for the break-glass scenario. I was going to send a few complimentary SFPs so you've got a Plan B on the shelf. Worth it?"

**Director or VP — Any Vertical**
"Hey [Name], how have you been? It's Brian with OSI Global. We work with infrastructure leaders on two things mostly: third party maintenance and optical hardware where OEM timelines or costs have become a problem. Is either of those a live conversation for your team?"

**TPM Wedge — Prospect Already Has TPM (Park Place / Service Express)**
"Hey [Name], how have you been? It's Brian with OSI Global. With the Park Place and Service Express merger, a lot of teams have been taking a fresh look at their TPM relationships. Have you had a chance to renegotiate since the merger, or are you still on the same rates?"

**Systems / Infrastructure Engineer — DIMMs**
"Hey [Name], how have you been? It's Brian with OSI Global. We source server memory direct from Samsung and Hynix for infrastructure teams dealing with DDR4 and DDR5 cost pressure. Is that on your radar right now?"

**Storage Engineer / Admin**
"Hey [Name], how have you been? It's Brian with OSI Global. We do third party maintenance on NetApp and other storage platforms for teams that have gear running fine but coming off OEM support. Is that a conversation you're having?"

**IT Director — Compute and Infrastructure**
"Hey [Name], how have you been? It's Brian with OSI Global. We work with IT leaders on server memory and third party maintenance, mostly for teams carrying OEM costs on infrastructure that has been running fine for years. Is budget pressure on that something you're dealing with?"

**Procurement — TPM Competitive Bid**
"Hey [Name], how have you been? It's Brian with OSI Global. We make competitive bids on multi-vendor maintenance contracts. A lot of procurement teams are using us to benchmark their current rates, especially since the Park Place and Service Express merger. Would a competitive bid be worth a look for your next cycle?"

**Transport Engineer / Optical NE — DWDM**
"Hey [Name], how have you been? It's Brian with OSI Global. We supply open line DWDM systems, 30 to 50% below Ciena and Nokia, with no licensing headaches. A few teams have been using us to fill capacity gaps without going back to the OEM. Is that a conversation worth having for your network?"

**Network Architect — Metro or Long-Haul WDM**
"Hey [Name], how have you been? It's Brian with OSI Global. We do open architecture DWDM — Smartoptics platform — significantly less rack space and power than traditional Ciena or Nokia boxes, and ships faster. Is that something that fits anything on your roadmap right now?"

**Cold Call Rules:**
- Always open with "How have you been?" — 6.6x baseline meeting rate
- State a clear reason for calling
- End with a question about their world — never "Is now a good time?"
- Voicemails: under 20 seconds, phone at start AND end, always reference "sending this afternoon" since Email 1 sends at 9 AM

---

## Step 10: Write LinkedIn Invite

Under 300 characters. Low friction. No pitch. Must reference something specific from their profile or company. Do not mention mutual connections.

---

## Step 11: Present for Review — Wait for "Run"

After completing Steps 1 through 10, present everything to Brian:

For each email show:
- Email number, day in sequence, and proposed send date
- All 5 subject line options with the randomly selected one clearly marked
- Full email body

Then show:
- Call script and voicemail
- LinkedIn invite text
- Proposed send schedule as a table

**Stop completely. Do not send. Do not schedule. Wait.**

End with: "Look it over and say **run** when you're ready."

---

## Step 12: On "Run" — Send Email 1 Immediately, Then Schedule the Rest

When Brian says "run" (or any clear go-ahead — "send it", "looks good", "do it"):

### 12a — Send Email 1 Right Now via Chrome

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify Brian
3. Click New mail
4. In the To field, type the prospect's email address and press Tab
5. Click the Subject field and type the selected subject line exactly
6. Click in the body area above the signature and type the email body exactly as written
7. Click Send
8. Confirm the email was sent before moving on

HubSpot Sales extension is installed — the send logs automatically to HubSpot.

### 12b — Schedule Emails 2 Through 7

After Email 1 is confirmed sent, use `mcp__scheduled-tasks__create_scheduled_task` to schedule the remaining 6.

**Task ID format:** `[firstname]-[lastname]-[company-slug]-email-[N]`
Example: `jane-smith-acme-email-2`

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

**Task prompt for Email 4 (swag / address confirm):**

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

## Step 13: Create HubSpot Tasks

### Create or update contact record

If the contact doesn't exist in HubSpot, create it. Required fields: first name, last name, job title, company, email, phone (if known), LinkedIn URL.

Owner: 213536174 (Brian Charrette)

### Create strategy note

objectType: "notes", owner 213536174, associated to the contact.

Format exactly:

```
SEQUENCE TYPE: [Network / Server / TPM / DWDM / Storage / Pre-owned]

QUICK CONNECT KEYWORDS
[5-8 spoken trigger words from their profile]

CALL SCRIPT
OPENER: [full opener from library]
VM: [one line, under 20 seconds, phone at start and end]

THE PLAY
[One tight paragraph: why they qualify, the hook, the attack angle. Include any relevant deal history from HubSpot if found.]
```

No em-dashes anywhere in the note.

### Create LinkedIn Connection Request task

- Subject: "Sales Nav -- Send connection request -- [First Last] | [Company]"
- Type: LINKED_IN_CONNECT
- Due: Day 0
- Notes: LinkedIn invite text from Step 10
- Owner: 213536174

Check for an existing connection request task first. Skip if one already exists.

---

## Step 14: Build the Word Doc

Use Glob to find the current docx SKILL.md: `/sessions/*/mnt/.claude/skills/docx/SKILL.md` — read it and follow its instructions to build a Word document with:

- Title: [Prospect Name] — [Company] Outreach Sequence
- Subtitle: [Title], 7-email sequence, 28-day cadence, automated via Outlook
- For each email: heading with email number + send date + timing note, all 5 subject lines with selected one marked, full email body
- Call script section: opener + voicemail
- LinkedIn invite text
- Final section: sequence schedule summary table (email number, date, subject line selected)
- Font: Calibri 11pt throughout

Save to the Cowork outputs folder. Use Glob to find it: `/sessions/*/mnt/outputs/` — save as `Email/[lastname]-[company]-sequence.docx`

---

## Step 15: Confirm and Hand Off

Present Brian with:
1. Link to the Word doc
2. The full schedule table (all 7 emails, dates, subjects selected)
3. Reminder: if the prospect replies at any point, delete the remaining scheduled tasks from the Cowork Scheduled Tasks sidebar

---

## OSI Messaging Reference

### Lead with the right pillar by role

- Network/Infrastructure Architect, Network Engineer → TPM cost savings + hardware lifecycle + EOL support + optics supply chain
- Director/VP of IT → OpEx reclamation, vendor simplification, budget control
- Data Center / Colo roles → optics, Smartoptics 800G, open line systems, fast fulfillment
- Procurement / Finance → 50 to 80% savings vs OEM, Gartner-recognized credibility

### Core proof points (pick 1 to 2 per sequence — not all of them)

- 24/7/365 TAC coverage at roughly half of OEM pricing (Systain TPM)
- Same-day fulfillment — 6,000+ DIMMs shipped same-day
- Transceivers 1G to 400G, coded for 40+ OEM platforms, including custom builds OEMs won't make
- Largest global Smartoptics partner — 800G transponders in stock
- EOL product support long after OEM walks away
- Privately owned — no quarterly targets, no investor pressure, answers to clients only

---

## Vertical Intelligence

### Telco and Service Providers
Lead with optics. Do not open with free SFPs at engineer level — lead with supply chain reliability instead. TPM is rarely the opener here.

### Large Banks and Financial Institutions
Lead with optics. Free SFP offer works well. Do not lead with TPM. If they have a known TPM provider, use the Park Place / Service Express merger wedge.

### Professional Services and Consulting
TPM is a viable opener. Lead with pain, not price. Free optics also works.

### Manufacturing
Free optics as break-glass insurance. TPM for aging Cisco gear.

### Healthcare
TPM with documented SLAs. DIMMs for server refresh. Gartner-recognized and privately owned matters here.

### Enterprise IT (General)
All pillars apply. Lead with whichever matches the strongest signal from research — if EOL gear is visible, TPM. If network buildout is visible, optics.

---

## TPM Positioning

**Unknown if they have TPM:**
- Banks: optics opener, TPM is the second conversation
- Consulting: TPM can open, lead with pain not savings percentage
- Manufacturing / enterprise: TPM is strong, aging gear and OEM end-of-life is the hook

**Known TPM provider (Park Place, Service Express, Curvature):**
Use the merger wedge: "With the Park Place and Service Express merger, a lot of teams have been taking a fresh look at their TPM relationships. Have you had a chance to renegotiate since the merger, or are you still on the same rates?"

---

## DWDM and Smartoptics Talking Points

- Cost: 30 to 50% below Ciena and Nokia, with minimal licensing fees
- Space and power: significant reduction vs traditional DWDM platforms
- Simplicity: easier to deploy and manage
- Lead times: ships faster than OEMs
- Pedigree: backed by original engineering core, not grey market
- OSI is the largest global Smartoptics partner — 800G transponders in stock

---

## Brian's Voice — Always

- Direct, no-nonsense, outcomes over transactions
- Short emails — 3 to 4 paragraphs max, most under 100 words
- First person, specific, no corporate language
- Candid: if something isn't relevant, say so
- Confident but not aggressive
- Peer-to-peer tone — not vendor-to-buyer
