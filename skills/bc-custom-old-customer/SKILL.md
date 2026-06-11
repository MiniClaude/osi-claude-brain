---
name: bc-custom-old-customer
description: >
  Build and fully automate a 7-email re-engagement sequence for a dormant OSI Global customer —
  someone who previously bought hardware, optics, cables, servers and storage, power infrastructure,
  or TPM and has gone quiet. ALWAYS use this skill when Brian says "BC Custom Old Customer",
  "run the old customer sequence", "revive this account", "re-engage old customer", "pulse check
  on old account", or pastes a HubSpot contact record for a dormant existing customer and wants
  outreach built. This skill researches the account through ZoomInfo intent, scoops, recent news,
  and a LinkedIn job change check, then writes 7 emails that each lead with a different real OSI
  partnership story (Smart Optics, APC/Eaton, DDR4/DDR5 memory, Aruba/Fortinet, TPM, pro services,
  Nokia, Dell/HPE). Tone is warm reconnect and strategic advisor — not a hardware salesperson
  checking in. Brian reviews everything, and on "run" Email 1 goes out immediately via Outlook
  and the remaining 6 are scheduled automatically.
---

# OSI Global — Old Customer Re-engagement Sequence

Generates and fully automates a 7-email re-engagement sequence for a dormant customer that has
previously purchased across one or more OSI pillars. The goal is to reopen the relationship and
reposition Brian as a strategic solutions advisor, not a hardware vendor waiting for a PO.

Brian reviews everything first. When he says "run", Email 1 goes out immediately and the rest
schedule automatically over 28 days.

---

## Step 1: Gather Prospect and Account Info

Ask Brian to paste or provide:
- Contact full name
- Title
- Company and domain
- Email address
- What OSI has sold them historically (pillar buckets are enough: hardware, optics, cables, servers and storage, power, TPM, pro services)
- How long since last contact and any context on why the relationship went quiet

If Brian pastes a HubSpot contact record, extract fields directly. If he is thin on history, do
not press — the research step will fill most gaps.

---

## Step 2: Research the Account — Strategic Re-entry

This is the most important step in the skill. Brian wants to walk back in the door as a solutions
expert, which means he needs a reason to show up that is not "just checking in."

Run these three research passes in parallel where possible:

### 2a — ZoomInfo Intent and Scoops
Use the ZoomInfo MCP to pull:
- `enrich_intent` or `search_intent` on the company domain — surface active intent topics, especially anything touching networking, infrastructure, data center, optical, wireless, security, power, cloud migration, storage refresh, AI buildout
- `enrich_scoops` or `search_scoops` on the company — pull recent scoops on IT projects, budget cycles, hiring plans, tech stack changes
- `account_research` if available for a consolidated view

Capture the 2 or 3 strongest signals. These become the backbone of Email 1.

### 2b — Recent News and Company Announcements
Use web search for the company name plus terms like:
- "press release" OR "announces" OR "expansion" OR "data center" OR "acquires"
- "layoffs" OR "restructuring" OR "funding" OR "earnings"
- Any mention of new AI, cloud, colocation, or infrastructure initiatives
- Leadership changes, especially CIO, CTO, VP of Infrastructure, Director of Network

Note 1 or 2 specific items that are genuinely relevant to an IT conversation.

### 2c — LinkedIn Job Change Check
Before writing anything, verify the contact is still at the company and still in a relevant role.
If they have moved on, stop and tell Brian — the sequence should either be redirected to their
new company or handed to someone else at the original account.

---

## Step 3: Map the Story Rotation

Each email leads with a different real OSI partnership or pillar story. The contact may or may
not have bought these specific lines from OSI before — the point is to show range and reposition
Brian as someone who can solve across the full stack.

Lock in this distribution before writing:

- **Email 1 — Smart Optics / Open Line Systems** (flagship credibility — largest global Smart Optics partner, 800G transponders, open line systems, 40+ OEM platforms)
- **Email 2 — APC and Eaton Power Infrastructure** (often overlooked, rarely pitched by hardware resellers, a clear "we do more than boxes" signal)
- **Email 3 — Memory DIMMs, DDR4 and DDR5** (same day 6,000 plus DIMM shipment proof point, 80 to 90 percent off OEM, Samsung Micron Hynix sourcing)
- **Email 4 — Swag and Sample SFPs / Address Confirm** (FIXED content, see Step 4)
- **Email 5 — "Any thoughts?"** (FIXED content, reply in thread, see Step 4)
- **Email 6 — Aruba and Fortinet** (wireless and security pulse check, tied to a direct yes or no question)
- **Email 7 — TPM plus Professional Services plus full breadth** (strategic close — mention Nokia, Dell, HPE, Cisco, Juniper coverage, Systain TPM, IMAC, ITAD, pro services — one partner for the full lifecycle)

Nokia gets woven into Email 1 or Email 7 as part of the open network narrative. Dell and HPE
show up in Email 7 as part of the full breadth close.

---

## Step 4: Write the 7-Email Sequence

Write all 7 emails before doing anything else. Use Brian's voice throughout: direct, no corporate
fluff, outcomes over transactions, confident but not aggressive, first person. Short emails. 3 to
4 paragraphs max, most under 120 words.

Critical tone rules for this specific skill:
- **Do not say "checking in"** — ever. That phrase is banned in this sequence.
- **Do not apologize for the silence** — acknowledge it, do not grovel.
- **Position Brian as a strategic advisor** — he is not asking for a meeting to "see where we can help." He is bringing a point of view.
- **Reference the research** — ZoomInfo intent, scoops, or news findings should show up in Email 1 and ideally Email 2.
- **Do not list past purchases** — the contact knows what they bought. Speak to where they are going, not where they have been.

### Email 1 — Strategic Re-entry (Day 0)
- Open with a specific observation from the research (intent topic, scoop, recent news)
- Transition into the Smart Optics or open line systems angle — lead with a short story or proof point ("we are the largest global Smart Optics partner, 800G in stock, 40 plus OEM platforms coded")
- Tie it back to something relevant at their company
- One clear ask: 20 minute call to compare notes on where their optical and network roadmap is heading
- 3 to 4 short paragraphs
- Outlook signature handles the sign off — do not include name or contact at the end

### Email 2 — Different Angle: Power (Day 4)
- Pivot hard. Most resellers never talk power.
- Lead with the APC and Eaton partnership story — OSI supplies power infrastructure alongside the networking and compute stack, which means fewer vendors, one throat to choke
- Tie to any power or data center signal from the research if possible
- 2 to 3 short paragraphs
- Soft close: "worth a conversation if your power stack is showing its age"

### Email 3 — Memory Play (Day 10)
- Lead with the DDR4 and DDR5 memory story — the same day 6,000 plus DIMMs shipment, 80 to 90 percent off OEM list, Samsung Micron Hynix sourcing, validation process, logged test reports
- Angle it as "most IT teams do not know they are overpaying 10 times for memory until someone shows them"
- Acknowledge the silence once, matter of fact, then redirect forward
- 2 to 3 short paragraphs
- Give them an easy out: "if timing is off, just say the word"

### Email 4 — Swag and Sample SFPs / Address Confirm (Day 12)
- Subject is always: **Re: Confirming address** (new email, not a literal reply — the subject makes it look like a follow up)
- Body is always the same — do not personalize or change it:

> I'm just prepping this package for you. I have a box of swag and a pair of sample SFPs to send to you from the team here at OSI Global IT.
>
> Do you come into the office? Is that the best address to send it to right now?

- Outlook signature handles the sign off
- If they reply with an address, pause all remaining scheduled tasks and follow up on the shipment

### Email 5 — "Any thoughts?" (Day 14)
- This email is ALWAYS the same: reply in original thread, two words only
- Body: **Any thoughts?**
- Nothing else. No greeting, no signature, no additional text.
- This is sent as a REPLY to Email 1's thread, not a new email

### Email 6 — Aruba and Fortinet Pulse Check (Day 18)
- Lead with a direct yes or no question tied to wireless or security
- Frame the Aruba and Fortinet angle — OSI moves real volume on both, compatible optics for both, TPM coverage for both
- If research surfaced anything about their wireless footprint, cloud security, or zero trust plans, tie it in
- 2 to 3 sentences plus the question
- "If yes, worth 15 minutes. If no, I will stop crowding your inbox."

### Email 7 — Strategic Close with Full Breadth (Day 28)
- Do not call this a breakup. Call it a reset.
- Short, respectful, leaves the door open
- Weave in the full breadth of what OSI actually is: Nokia, Dell, HPE, Cisco, Juniper hardware; Systain TPM at 24/7/365; professional services including IMAC, ITAD, data center relocations; the full stack with one point of contact
- Close with: "whenever the next project lands on your desk, I would like to be the first call. No pitch, no pressure, just a phone number."
- Outlook signature handles the sign off

---

## Step 5: Humanize Every Email

Apply these rules to every email before finalizing:

- **No AI vocabulary**: remove "crucial," "pivotal," "landscape," "underscore," "delve," "showcase," "testament," "enhance," "foster," "garner," "leverage" (as a verb), "seamless," "robust," "cutting edge"
- **No hyphens**: rewrite any hyphenated phrases (e.g. "end of life" not "end-of-life", "24/7/365" not "24-hour", "same day" not "same-day")
- **No em dashes**: replace with commas or periods
- **No rule of three**: break up any triple item lists into natural prose
- **No -ing pileup**: avoid "highlighting," "ensuring," "reflecting," "contributing to" tacked onto sentences
- **No negative parallelisms**: avoid "it's not just X, it's Y"
- **Vary sentence length**: mix short punchy sentences with longer ones
- **Use "is/are/has"** instead of "serves as," "stands as," "functions as"
- **No "just checking in"** — banned phrase in this skill
- **No "circling back"** — also banned
- **Read every email aloud mentally** — if it sounds like a press release, rewrite it

After applying, do a final check: "What makes this obviously AI generated?" Fix whatever you find.

---

## Step 6: Generate Subject Lines

For each email EXCEPT Email 4 (fixed subject: "Re: Confirming address") and Email 5 (reply,
inherits original subject):
- Write 5 subject line options per email
- Mix: 2 or 3 professional and catchy, 2 outlandish and unexpected
- No hyphens in subject lines
- **Pick one at random and commit to it.** Do not ask Brian which to use. Claude chooses at will, the same way bc-7email-custom does. Use actual randomness across runs so the same sequence does not always get the "safe" choice.
- Present all 5 to Brian with the selected one clearly marked (bold + "SELECTED") so he can see the full set, but the pick is already made and locked for send

For this skill specifically, bias subject lines toward curiosity and strategic framing rather
than urgency. Examples of direction: "a different angle on your optical spend", "the power
side of your stack", "how much are you paying for memory", "wireless pulse check", "one more
before I close the loop".

If Brian explicitly tells you to swap a subject line after seeing the set, honor that. Otherwise
the random pick stands.

---

## Step 7: Present for Review — Wait for "Run"

After completing Steps 1 through 6, present everything to Brian:

1. **Research summary** — 3 to 5 bullets on what the ZoomInfo intent, scoops, news, and LinkedIn check surfaced. This is what gives the sequence its legs, so show it.
2. **Story distribution** — confirm which partnership story leads each email
3. **All 7 emails in full** — for each: email number, day in sequence, 5 subject lines with selected one marked, full body
4. **Proposed send schedule as a table**

**Stop completely. Do not send. Do not schedule. Wait.**

End with: "Look it over and say **run** when you're ready."

---

## Step 8: On "Run" — Send Email 1 Immediately, Then Schedule the Rest

When Brian says "run" (or any clear go ahead like "send it", "looks good", "do it"):

### 8a — Send Email 1 Right Now via Chrome

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

### 8b — Schedule Emails 2 Through 7

After Email 1 is confirmed sent, use `mcp__scheduled-tasks__create_scheduled_task` to schedule
the remaining 6. Day 0 is today (the day Brian said "run").

**Task ID format:** `[firstname]-[lastname]-[company-slug]-oldcust-email-[N]`
Example: `jane-smith-acme-oldcust-email-2`

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
4. Find the oldest email sent to [EMAIL ADDRESS] — that is the original re-engagement email
5. Open it and click Reply
6. Clear any auto populated body text (keep the signature if it appears)
7. Type only: Any thoughts?
8. Do not add any greeting, additional text, or change the subject line
9. Click Send
10. Confirm the reply was sent and report back
```

Set `notifyOnCompletion: true` on all tasks.

---

## Step 9: Build the Word Doc

Read the docx SKILL.md at `/sessions/gracious-affectionate-euler/mnt/.claude/skills/docx/SKILL.md`
and build a Word document with:

- Title: [Prospect Name] — [Company] Re-engagement Sequence
- Subtitle: Old Customer Revival, 7 emails, 28 day cadence, automated via Outlook
- Research summary section (ZoomInfo intent topics, scoops, news findings, LinkedIn status)
- Story distribution table (email number, lead partnership story)
- For each email: heading with email number plus send date plus timing note, all 5 subject lines with selected one marked, full email body
- Final section: sequence schedule summary table (email number, date, subject)
- Font: Calibri 11pt throughout
- Save to: `/sessions/gracious-affectionate-euler/mnt/ Email/[lastname]-[company]-oldcust-sequence.docx`

---

## Step 10: Confirm and Hand Off

Present Brian with:
1. Link to the Word doc
2. The full schedule table (all 7 emails, dates, subjects)
3. Note: if the prospect replies at any point, delete the remaining scheduled tasks from the Cowork Scheduled sidebar

---

## OSI Partnership and Proof Point Reference

Use these stories and proof points across the sequence. Pick the right one for each email per
the Step 3 distribution, and weave them into Brian's voice — do not recite them.

**Smart Optics and Open Line Systems (Email 1 anchor):**
- Largest global Smart Optics partner
- 800G transponders in stock
- Optical transceivers 100MB through 800G in QSFP, QSFP-DD, CFP, XFP, SFP
- Coded for 40 plus OEM platforms, including custom builds OEMs will not make (10G copper optics, extended distances, multi platform twinax, DWDM coded as SFP+ ER/ZR, 100G CFP ER coded as LR)
- DCP-M, DCP-R, DCP-F, DCP-1203, DCP-108 product families
- Point to point WDM, passive filters, in line amplification, 100G and 400G DWDM
- CWDM and DWDM multiplexers up to 80 DWDM channels over dark fiber

**APC and Eaton Power Infrastructure (Email 2 anchor):**
- Full UPS, PDU, rack power, and cooling support
- One vendor for network, compute, storage, and power
- Rare positioning — most resellers will not quote power

**Memory DIMMs DDR4 and DDR5 (Email 3 anchor):**
- 6,000 plus DIMMs shipped same day as proof of inventory depth
- 16GB, 32GB, 64GB, 128GB, 256GB capacities
- OEM branded and approved (OEM equivalent, functionally identical, no logo)
- 80 to 90 percent off OEM list — example: 64GB DIMM listing at $6,000 supplied at a fraction
- Samsung, Micron, Hynix sourcing
- Validation process with logged test reports

**Aruba and Fortinet (Email 6 anchor):**
- Full wireless refresh and lifecycle support on Aruba
- Fortinet firewall sourcing and TPM coverage
- Compatible optics coded for both
- Systain TPM covers both when OEM walks away

**Systain TPM and Professional Services (Email 7 anchor):**
- Systain 24/7/365 TAC, Level 2 and Level 3 engineers answer calls
- NBD, 4 hour, and 4 hour with tech onsite SLAs globally
- 50 percent plus maintenance cost reduction vs OEM
- EOL product support after OEM walks
- Hybrid strategy for coverage where VARs cannot reach
- Professional Services: data center relocations, smart hands, IMAC, ITAD, wireless deployment, staff augmentation, structured cabling
- Gartner recognized

**Full Breadth (Email 7 weave in):**
- Hardware: Cisco, Juniper, Aruba (HPE), Fortinet, Brocade, F5, Dell, HPE, Nokia
- Servers: IBM pSeries iSeries xSeries, SUN/Oracle, HPE ProLiant, Dell PowerEdge, Cisco UCS, Supermicro
- Storage: EMC, NetApp, IBM, HDS, HPE, Infinidat
- Privately owned, no quarterly earnings pressure, answers to clients

**Brian's voice — always:**
- Direct, no nonsense, outcomes over transactions
- Short emails, 3 to 4 paragraphs max, most under 120 words
- First person, specific, no corporate language
- Candid: if something is not relevant, say so
- Confident but not aggressive
- Strategic advisor, not order taker
