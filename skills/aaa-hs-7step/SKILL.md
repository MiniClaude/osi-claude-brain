---
name: aaa-hs-7step
description: "Drafts 7 personalized OSI Global outreach emails for a prospect and writes them to the AI Email Subject 1-7 and AI Email Body 1-7 fields on the HubSpot contact. End-to-end: research, contact lookup or create, approved vendor check, 7 humanized emails, 5 subject options per email, a LINKED_IN_CONNECT task on the contact, and a suggested cadence printed in chat for manual sending. No email-queue.json. No auto-send. Brian sends from HubSpot or Outlook on his own schedule. Warns before overwriting an existing AI field set. ALWAYS use when Brian says 'aaa-hs-7step', 'hs 7 step', 'hs 7step', 'aaa hs 7 step', 'draft 7 in hubspot', 'populate AI fields with 7', 'master + hubspot draft', 'save 7 to the contact', or pastes a LinkedIn profile, HubSpot contact, or name + company and wants the full sequence drafted on the contact for manual sending."
---

# aaa-hs-7step — OSI Global 7-Email Draft to HubSpot

Drafts a personalized 7-email outreach sequence for any OSI Global prospect, saves all 7 subjects and bodies to the contact's `ai_email_subject_1-7` and `ai_email_body_1-7` fields, creates a `LINKED_IN_CONNECT` task on the contact, generates a full Orum-ready call script package (voicemail + 12-opener library + bridge + discovery + objections) saved as a HubSpot note, and prints a suggested cadence in chat. Brian sends the emails manually from HubSpot or Outlook on his own schedule.

**What this skill does NOT do:**
- Does not write to `email-queue.json`. There is no queue.
- Does not invoke the `osi-email-sender`. Nothing auto-sends.
- Does not open Chrome or Outlook to fire Email 1 live.
- Does not enforce holiday avoidance or weekend skipping. The cadence is a suggestion Brian follows manually.
- Does not update the local Excel tracker.

**What this skill DOES do:**
1. Researches the prospect (Personal Hook + Fresh Hook + OSI angle).
2. Looks up or creates the HubSpot contact under Brian's ownership.
3. Checks for an existing draft on the AI fields and warns before overwriting.
4. Writes 7 emails in Brian's voice, humanizes them, generates 5 subject line options for each.
5. Drafts a LinkedIn invite under 300 characters and creates a `LINKED_IN_CONNECT` task on the contact, due today.
6. Generates a full Orum-ready call script package — voicemail script + 12-opener live call script — and saves it as a HubSpot note on the contact.
7. Prints a suggested cadence (Day 1 = today, Day 5, Day 11, Day 13, Day 15, Day 19, Day 29) with weekend skipping.
8. On Brian's "save," writes all 14 AI field properties to the contact in a single call.

---

## Step 1 — Gather Prospect Info

Ask Brian for or extract from what he pasted:
- Full name
- Title
- Company and domain
- Email address (required — see Step 1a)
- LinkedIn URL if available
- Any context he has (pain points, source, notes)

If Brian pasted a HubSpot contact record or a LinkedIn profile, parse fields directly.

### Step 1a — STOP IF NO EMAIL

This skill writes 7 emails to a HubSpot contact record. No email means no contact lookup means no place to put the draft. If neither Brian's input nor a quick ZoomInfo lookup returns a valid email, STOP. Tell Brian and suggest the LinkedIn-only fallback (LINKED_IN_CONNECT task + a second LI message task two weeks later).

---

## Step 2 — HubSpot Contact + Draft Check + Approved Vendor Check

### 2a. Contact lookup or create

Use `mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__search_crm_objects` to search HubSpot contacts by email. Pull `ai_email_subject_1` along with the standard fields — Step 2b needs it.

If found, capture the **contact ID**, refresh `jobtitle` from LinkedIn (LinkedIn is authoritative — HubSpot titles go stale), and reassign `hubspot_owner_id` to `213536174` (Brian) if it's not already.

If not found, create the contact with `mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__manage_crm_objects` and these fields:

| Field | Source | Format |
|---|---|---|
| `firstname`, `lastname` | LinkedIn / input | as shown |
| `jobtitle` | LinkedIn (authoritative) | current top-card title |
| `company` | LinkedIn | current employer |
| `email` | input / ZoomInfo | standard |
| `phone` | ZoomInfo direct dial | `+1 (XXX) XXX-XXXX` |
| `mobilephone` | ZoomInfo mobile only — NEVER switchboard | `+1 (XXX) XXX-XXXX` or blank |
| `city`, `state` | LinkedIn | as shown |
| `hs_timezone` | from city/state | one of `us_slash_eastern`, `us_slash_central`, `us_slash_mountain`, `us_slash_pacific`, `us_slash_alaska`, `canada_slash_atlantic` |
| `hs_linkedin_url` | LinkedIn | full URL |
| `hubspot_owner_id` | Brian | `213536174` |

Associate to the company. If the company doesn't exist in HubSpot, create it first with owner `213536174` and link.

### 2b. Active draft check (warn, do NOT hard-block)

If `ai_email_subject_1` on the contact already has content, the contact already has a drafted sequence sitting in the AI fields. Tell Brian:

> Contact already has AI Email Subject 1 populated: `[first 60 chars of existing subject]...`. Overwrite all 7 fields with a fresh sequence?

Wait for an explicit "overwrite", "yes", "refresh", or equivalent. Without that, stop. Do NOT auto-stop the way the old queue-based dedup did — Brian gets the choice every time, because refreshing the draft is a legitimate workflow.

If `ai_email_subject_1` is blank or the contact is brand new, proceed without a prompt.

### 2c. Approved vendor check

Read `C:\Users\Mini\Documents\osi-claude-brain\approved-vendors.json` from local disk. Case-insensitive substring match on the prospect's company against the `approved_vendor_companies` list. If the file doesn't exist, treat as "no match" and skip the approved-vendor language entirely — never invent it.

**If match:**
- Email 1 includes ONE soft line acknowledging approved-vendor status. Examples: "Side note, we're already on your approved vendor list, so no new vendor onboarding if anything ever needs to move fast." Or: "For context, we're an approved vendor at [Company] already, so standing up a PO is painless if it comes to that."
- ONE other email (Email 3 or 4 — pick whichever fits the narrative) gets a brief one-line reminder: "Quick reminder we're already approved at [Company] if timing matters."
- No other email mentions it. Never say "vetted" or "pre-approved" — those read as marketing. "Approved vendor" is the term. Never mention "procurement" in Email 1.

**If no match:** never invent it. No mention anywhere.

---

## Step 3 — Research the Prospect

Web search the company and the role. Pull what they do, scale, public tech stack, any 30-day news. Decide which OSI pillar leads:

- **Network / telecom / colocation / carrier** → optics + DWDM + supply chain reliability; TPM second
- **Bank / financial institution** → optics, free SFP wedge; never lead TPM (regulated environments often locked to OEM support)
- **Software / cloud / SaaS** → optics, high-density connectivity, lead time
- **Enterprise IT / manufacturing / consulting** → TPM cost savings + EOL coverage
- **Procurement / IT Director / VP** → OpEx reclamation, vendor simplification, competitive TPM bid

Capture 1-2 specific concrete details to weave into Email 1 — recent news, a post they engaged with, a known infrastructure pattern at their company size. Name this the **Personal Hook**. It anchors Email 1 and the LinkedIn invite.

Also run ONE targeted web search for company news in the last 30 days. Capture acquisitions, exec hires, earnings, product launches, buildout announcements, partnerships as the **Fresh Hook**. If nothing surfaces in 30 days, fall back to the Personal Hook alone.

---

## Step 4 — Determine Sequence Type

Pick one based on role, title, and vertical:

| Sequence | Target roles | Lead angle |
|---|---|---|
| Network | Network Engineer, Architect, Transport Engineer | Free SFP sample |
| Server | Systems Engineer, Infrastructure Engineer, Server Admin | Free DIMM sample |
| TPM | IT Director, DC Manager, Asset Manager, Procurement, mid-market CIO | OEM cost pain |
| DWDM | Transport Engineer, Optical NE, Network Planner at carrier/CLEC/MSO | Cost vs Ciena/Nokia |
| Storage | Storage Admin, Storage Engineer | Pre-owned NetApp + TPM |
| Pre-owned | Cisco/Juniper/Arista environments | Pre-owned gear + OSI TPM |

This drives Email 1's lead and shapes Emails 2-7's pillar rotation.

---

## Step 5 — Write All 7 Emails

Write every email before doing anything else. Brian's voice: direct, no-nonsense, outcomes over transactions, zero corporate fluff. Short. Mobile-friendly. Scannable in 10 seconds.

Brian sends these manually, so the body in each AI field is the body of the email he'll paste or use as the basis for sending from HubSpot. Do not include any signature block — Brian's own Outlook signature or HubSpot template handles that when he sends.

### Email 1 — Cold Intro (Day 1)
- 3-4 short paragraphs, most under 100 words
- Open with what problem you solve for people in their role
- Reference the Personal Hook or Fresh Hook (something specific from research)
- If approved vendor: include the soft one-line note (see Step 2c)
- One clear ask: 15-minute call
- End body with just `Brian` on its own line

### Email 2 — Different Angle (~Day 5)
- Pivot to a DIFFERENT OSI pillar than Email 1 (optics if Email 1 was TPM, or vice versa)
- Do not repeat what was in Email 1
- 2-3 short paragraphs
- No hard ask — soft "worth a conversation if..."
- End with `Brian`

### Email 3 — Soft Touch (~Day 11)
- Acknowledge the silence without being apologetic
- Reference a pattern you see at companies like theirs (no namedropping)
- Offer an easy out: "if timing is off, just say the word"
- 2-3 short paragraphs
- If approved vendor and you didn't use the reminder in Email 4, use it here
- End with `Brian`

### Email 4 — Swag & Sample SFPs / Address Confirm (~Day 13)

**Subject is ALWAYS** (no personalization, no variation): `Re: Confirming address`

The "Re:" makes it look like a follow-up in their inbox. This is not a literal reply — it's a new email with a manufactured subject.

**Body is ALWAYS the same** (no personalization):

> I'm just prepping this package for you. I have a box of swag and a pair of sample SFPs to send to you from the team here at OSI Global IT.
>
> Do you come into the office? Is that the best address to send it to right now?

End with `Brian`. This email works because it creates a reason to reply that has nothing to do with a sales pitch. If they reply with an address, Brian ships the swag and pauses the remaining touches manually.

### Email 5 — "Any thoughts?" (~Day 15)

ALWAYS the same. This is meant to be a REPLY in the original Email 1 thread when Brian sends it from his inbox.

- Subject saved to `ai_email_subject_5` = `Re: [Email 1 selected subject]` so the field reads cleanly on the contact record
- Body saved to `ai_email_body_5` = `Any thoughts?` — two words only. No greeting, no signature, no additional text.

When Brian sends manually, he should hit Reply on his original Email 1 send so the thread stays intact. The AI field stores the body and the manufactured subject for visibility.

### Email 6 — Pattern Interrupt (~Day 19)
- Single direct yes/no question about their specific environment
- Pick the most relevant from research: EOL gear, contract renewals, optics gaps, DWDM capacity, TPM rate review
- 2-3 sentences only
- "If yes, worth talking. If no, I'll stop bothering you."
- End with `Brian`

### Email 7 — Breakup (~Day 29)
- Short, respectful, leaves the door open
- Acknowledge you've sent several notes, respect their time
- No pitch
- Examples: "Should I close the file on this one, or is the timing just off?" or "No worries if now isn't the right time. Happy to circle back when things shift."
- End with `Brian`

---

## Step 6 — Humanize Every Email

Run every email through this filter before saving to the AI fields. Anything that fails gets rewritten:

- **No AI vocabulary:** remove "crucial," "pivotal," "landscape," "underscore," "delve," "showcase," "testament," "enhance," "foster," "garner"
- **No hyphens** in bodies or subject lines. Rewrite "end-of-life" → "end of life", "24-hour" → "24/7/365", "third-party" → "third party"
- **No em dashes (—)** anywhere. Split into two sentences if needed.
- **No rule of three.** Break triple-item lists into natural prose.
- **No -ing pile-up** at sentence tails. Kill trailing "highlighting our advantage," "ensuring uptime," "reflecting market shifts."
- **No negative parallelisms.** Remove "it's not just X, it's Y."
- **Vary sentence length.** Mix short punchy sentences with longer ones.
- **Use is/are/has** instead of "serves as," "stands as," "functions as."
- **Final read-aloud check.** Mentally read each email aloud. If it sounds like a press release, rewrite.

The why: prospects can smell AI from a mile away in 2026. Brian's edge over every other rep flooding inboxes with GPT-output is that his emails sound like a person. Lose that and the sequence collapses — and the AI-flagged copy would sit permanently on the HubSpot contact record for everyone to see. Double the reason to get this right.

---

## Step 7 — Subject Lines (5 Options Per Email)

For each email EXCEPT Email 4 (fixed: `Re: Confirming address`) and Email 5 (reply, stored as `Re: [Email 1 subject]`):
- Write 5 subject line options
- Mix: 2-3 professional/catchy + 2 outlandish/unexpected
- No hyphens in subject lines
- Randomly select one of the 5 — that's what gets written to `ai_email_subject_N`
- Present all 5 to Brian with the selected one clearly marked so he can pick a different one if he wants before "save"

---

## Step 8 — LinkedIn Invite Draft + Create LINKED_IN_CONNECT Task

### 8a. Draft the LinkedIn invite

Under 300 characters (LinkedIn hard limit). Personalized: reference role, vertical pain, or the Personal Hook. No pitch. No product names. No "I'd love to tell you about OSI." One sentence plus one short reason to connect.

### 8b. Create the HubSpot task

Using `mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__manage_crm_objects`:

**Task (object type `tasks`):**
- `hs_task_type` = `LINKED_IN_CONNECT`
- `hs_task_subject` = `Send LinkedIn Request — [First Last] | [Company]`
- `hs_task_body` = the literal LinkedIn message draft from 8a (the actual message Brian will send, not a description)
- `hs_task_status` = `NOT_STARTED`
- `hs_timestamp` = today's date in epoch ms (Brian's manual sending starts today by default)
- `hs_task_priority` = `HIGH`
- `hubspot_owner_id` = `213536174`
- Associate to the contact

**Verify after creating:** fetch the task back, read `hs_task_body`, confirm it's a real message addressed to the prospect. If it's a placeholder or description, immediately update with the correct draft.

Confirm in chat: `LinkedIn task created on contact [HubSpot URL] — due today.`

---

## Step 9 — Generate the Full Call Script Package + HubSpot Note

Do this automatically before presenting to Brian. No input needed.

### 9a. Voicemail Script

15 seconds max. One-sentence hook drawn from the Personal Hook. Say you are sending or about to send the email, name the Email 1 subject line, end with Brian's email spelled audibly ("that's bc at osihardware dot com"). No phone number. Present or future tense only ("I'm sending" / "I'm about to send"). Never past tense.

Apply Step 6 humanization rules. Read it aloud mentally — if it sounds like a recording, rewrite it until it sounds like a person leaving a voicemail.

### 9b. Live Call Script (Orum surface)

This is what Orum displays when Brian dials. Build it in memory with every bracket fully substituted using the research from Step 3. **Verify no [Name], [Title], [Company], [Vertical], [Insert], or [Paste...] tokens remain before saving to HubSpot.**

Structure — use this exact format as the HubSpot note body:

---

**VOICEMAIL**
[Fully written voicemail from 9a — no brackets, no tokens]

---

**OPENER LIBRARY — pick the one that fits**

Telco / Service Provider network engineer:
"Hey [First Name], how have you been? It's Brian with OSI Global. We supply ZR and ZR+ coherent optics to carrier teams as a secondary source when Cisco or Lumentum timelines slip. Is that something your team is running into right now?"

Bank / Financial Institution network engineer:
"Hey [First Name], how have you been? It's Brian with OSI Global. We supply certified compatible optics to bank IT teams, mostly for the break-glass scenario where something fails and you can't wait two weeks for OEM. I was going to send a few complimentary SFPs your way. Would that be useful?"

Enterprise IT / Consulting network engineer:
"Hey [First Name], how have you been? It's Brian with OSI Global. We work with enterprise IT teams on third party maintenance, specifically replacing OEM support on Cisco gear that is running fine but coming off warranty. Is that a conversation your team is having right now?"

Manufacturing network engineer:
"Hey [First Name], how have you been? It's Brian with OSI Global. We supply certified compatible optics and networking spares to manufacturing IT teams for the break-glass scenario. I was going to send a few complimentary SFPs so you've got a Plan B on the shelf. Worth it?"

Director or VP, any vertical:
"Hey [First Name], how have you been? It's Brian with OSI Global. We work with infrastructure leaders on two things mostly: third party maintenance and optical hardware where OEM timelines or costs have become a problem. Is either of those a live conversation for your team?"

Already has TPM — merger wedge:
"Hey [First Name], how have you been? It's Brian with OSI Global. With the Park Place and Service Express merger, a lot of teams have been taking a fresh look at their TPM relationships. Have you had a chance to renegotiate since the merger, or are you still on the same rates?"

Systems / Infrastructure engineer — DIMMs:
"Hey [First Name], how have you been? It's Brian with OSI Global. We source server memory direct from Samsung and Hynix for infrastructure teams dealing with DDR4 and DDR5 cost pressure. Is that on your radar right now?"

Storage engineer / admin:
"Hey [First Name], how have you been? It's Brian with OSI Global. We do third party maintenance on NetApp and other storage platforms for teams that have gear running fine but coming off OEM support. Is that a conversation you're having?"

IT Director — compute and infrastructure:
"Hey [First Name], how have you been? It's Brian with OSI Global. We work with IT leaders on server memory and third party maintenance, mostly for teams carrying OEM costs on infrastructure that has been running fine for years. Is budget pressure on that something you're dealing with?"

Procurement — TPM competitive bid:
"Hey [First Name], how have you been? It's Brian with OSI Global. We make competitive bids on multi-vendor maintenance contracts. A lot of procurement teams are using us to benchmark their current rates, especially since the Park Place and Service Express merger. Would a competitive bid be worth a look for your next cycle?"

Transport engineer / Optical network engineer — DWDM:
"Hey [First Name], how have you been? It's Brian with OSI Global. We supply open line DWDM systems, 30 to 50% below Ciena and Nokia, with no licensing headaches. A few teams have been using us to fill capacity gaps without going back to the OEM. Is that a conversation worth having for your network?"

Network architect — metro or long-haul WDM:
"Hey [First Name], how have you been? It's Brian with OSI Global. We do open architecture DWDM, SmartOptics platform, significantly less rack space and power than traditional Ciena or Nokia boxes, and ships faster. Is that something that fits anything on your roadmap right now?"

---

**RECOMMENDED OPENER FOR THIS PROSPECT**
[Pick the single best-fit opener from the library above based on Step 3 research. State it again fully, with the prospect's actual first name substituted in. One sentence explaining why you picked it.]

---

**BRIDGE**
"The reason I'm reaching out is [one sentence from Email 1 cold intro — the core value prop for their role and vertical]. I sent you an email about this — subject line was [Email 1 selected subject]. Did you get a chance to see it?"

---

**DISCOVERY QUESTIONS** (pick 2-3 that fit the vertical)
- "What's your current source for optics when you have a lead time issue or something fails unexpectedly?"
- "Are you on an OEM support contract for your Cisco gear, or have you looked at third party maintenance?"
- "When your DDR4 or DDR5 memory needs come up, are you going direct to Dell or HPE, or do you have another source?"
- "Have you looked at open line DWDM as an alternative to Ciena or Nokia for your next capacity add?"
- "Is your TPM provider still Park Place or Service Express, or did you move somewhere else after the merger?"
- "What does your hardware refresh cycle look like right now — are you mid-cycle or coming up on a decision?"

---

**OBJECTION HANDLERS**
"We already have a vendor for that" → "Totally understand. Most of our best customers have OEM or a primary vendor. We work as a secondary source — faster lead times, lower cost, no disruption to what's already working. Worth keeping a number on file for the next time timing or cost becomes an issue?"

"Send me an email / I'll look at your email" → "Already did — subject was [Email 1 selected subject]. I'll make sure it didn't land in spam. Is [email address] still the best place to reach you?"

"Not interested" → "Fair enough. Is it timing, or is this genuinely not a fit for your team right now?" [If timing: "Got it. When would be a better time to circle back?"] [If not a fit: "No worries at all. Thanks for being straight with me."]

"Too busy right now" → "I'll be quick. One question: is [core pain point from opener] something that's come up for your team in the last six months? If yes, worth 15 minutes. If no, I'll leave you alone."

---

**VOICEMAIL (if no answer)**
[Repeat the voicemail from 9a here for quick reference during the call]

---

### 9c. Save as HubSpot Note

Using `mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__manage_crm_objects`, create a note (object type `notes`) on the contact:

- `hs_note_body` = the full call script text from 9b (voicemail through objection handlers)
- `hs_timestamp` = today's date in epoch ms
- `hubspot_owner_id` = `213536174`
- Associate to the contact

**Token verification before saving:** scan the note body for any remaining bracket tokens — [Name], [First Name], [Title], [Company], [Vertical], [Insert], [Paste...], or similar. If any exist, substitute them with the actual prospect data before saving. A note with unresolved tokens is worse than no note.

Confirm in chat: `Call script note saved to contact [HubSpot URL].`

---

## Step 10 — Print Suggested Cadence

Print a simple table Brian can follow when sending manually. Use these gaps from today, with weekend skipping applied (if a date lands on Saturday or Sunday, push to the next Monday). Do NOT enforce holidays — Brian uses his judgment when he sends.

| # | Suggested day | Date (today + N days, weekend-skipped) | Notes |
|---|---|---|---|
| 1 | Today | [today's date, weekday] | Cold intro. Send first. |
| 2 | +4 business days | [date] | Different angle. |
| 3 | +6 bd after Email 2 | [date] | Soft touch. |
| 4 | +2 bd after Email 3 | [date] | Re: Confirming address. |
| 5 | +2 bd after Email 4 | [date] | "Any thoughts?" reply in the original thread. |
| 6 | +4 bd after Email 5 | [date] | Pattern interrupt. |
| 7 | +10 bd after Email 6 | [date] | Breakup. |

Total span: ~28 business days. The dates are a guide — Brian sends when he sends. If he pauses the sequence partway through (prospect replies, holiday week, etc.), he just resumes from where he is.

**BCC reminder for manual sends:** when sending from Outlook, BCC `bc@osihardware.com` (puts a copy in his inbox so he can confirm it fired) and `21878985@bcc.hubspot.com` (auto-logs the email to the HubSpot contact timeline). If he sends from HubSpot's native send UI, the timeline log happens automatically and only the inbox BCC matters.

---

## Step 11 — Present for Review — Wait for "Save"

After Steps 1-10 complete, present everything to Brian in one block:

1. **Prospect summary** — name, title, company, OSI angle, sequence type, approved vendor Y/N, HubSpot contact ID + URL
2. **Suggested cadence table** from Step 10
3. **All 5 subject line options per email** (Emails 1, 2, 3, 6, 7) with the selected one marked. Email 4 fixed (`Re: Confirming address`). Email 5 stored as `Re: [Email 1 subject]`.
4. **Full body of every email** — exactly what will land in `ai_email_body_N`
5. **LinkedIn invite text** with character count under 300
6. **Confirmation that the LinkedIn task was created** (link to the contact)
7. **Voicemail script** from Step 9a
8. **Recommended opener** from Step 9b (the single best-fit opener with the prospect's name substituted in)
9. **Confirmation that the call script note was saved** (link to the contact)
10. **What "save" will do** — write all 14 AI field properties to the contact in one call

**Stop. Do not write to HubSpot AI fields yet. Wait.**

End with: `Look it over and say **save** when you're ready.`

---

## Step 12 — On "Save" — Write 14 Properties to HubSpot AI Fields

When Brian says "save" (or any clear go-ahead: "looks good", "ship it", "do it", "overwrite"):

Use `mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__manage_crm_objects` with an `update` request on the contact ID captured in Step 2a. Write all 14 properties in a single call so the contact never sits in a half-populated state:

| Email # | Subject property | Body property |
|---|---|---|
| 1 | `ai_email_subject_1` | `ai_email_body_1` |
| 2 | `ai_email_subject_2` | `ai_email_body_2` |
| 3 | `ai_email_subject_3` | `ai_email_body_3` |
| 4 | `ai_email_subject_4` | `ai_email_body_4` |
| 5 | `ai_email_subject_5` | `ai_email_body_5` |
| 6 | `ai_email_subject_6` | `ai_email_body_6` |
| 7 | `ai_email_subject_7` | `ai_email_body_7` |

**Rules for the field values:**
- Subjects are the SELECTED subject from the 5 options. For Email 4, exactly `Re: Confirming address`. For Email 5, exactly `Re: [Email 1 selected subject]`.
- Bodies are the EXACT email body Brian will send. No signature block — his own Outlook sig or HubSpot template handles that at send time.

**Overwrite policy:** if Brian got the "overwrite?" prompt in Step 2b and said yes, write straight over the old values. Otherwise the fields were blank and this is a clean first write.

**Verify after write:** fetch the contact back and confirm `ai_email_subject_1` matches the selected Email 1 subject and `ai_email_body_1` matches what was drafted. If either is blank or doesn't match, retry once. If it still fails, tell Brian which fields didn't write so he can fix them by hand on the contact.

### 12a. Confirm

Confirm in chat:
- `HubSpot AI fields populated: ai_email_subject_1-7 + ai_email_body_1-7 on contact [HubSpot URL].`
- `LinkedIn task created and due today.`
- `Call script note on contact — voicemail + 12-opener library + bridge + discovery + objections.`
- `Suggested cadence above — send manually starting today.`
- `No queue, no auto-send. Your call when to fire each email.`

---

## OSI Messaging Reference (for writing the emails)

### OSI Product Lines

1. **Optics** — SmartOptics transceivers, private-labeled. Free sample is the opening wedge.
2. **DWDM and Open Line Systems** — SmartOptics DCP platform, 30-50% below Ciena/Nokia. Ships fast.
3. **Compute and Components** — DIMMs from Samsung / Hynix / Micron. Lead with DIMMs.
4. **Storage** — NetApp TPM, pre-owned storage.
5. **TPM** — 40-60% below OEM. Multi-vendor. Gartner-recognized, privately owned, no PE.
6. **Pre-Owned and New Networking** — Pre-owned Cisco/Juniper/Arista. New Nokia authorized.
7. **Professional Services** — Strong signal only. Never lead cold.

### Vertical Intelligence — Cheat Sheet

**Telco / service providers:** lead optics + supply chain reliability. Do NOT open free SFPs at scale. TPM rarely the opener at engineer level — sits at director.

**Banks / large financial:** lead optics, free SFP wedge works at engineer level. Do NOT lead TPM (regulated, often locked to OEM). Park Place / Service Express merger wedge if they have known TPM.

**Professional services / consulting:** TPM viable opener. Lead pain, not price. Free optics also works.

**Manufacturing:** free optics as break-glass insurance. TPM for aging Cisco gear.

**Healthcare:** TPM with documented SLAs. DIMMs for server refresh. Gartner-recognized + privately owned + no PE matters here.

### TPM Positioning

**Unknown if they have TPM:**
- Banks: optics opener, TPM is second conversation
- Consulting: TPM can open, lead with pain not savings %
- Manufacturing / enterprise: TPM strong, aging gear + OEM EOL is the hook

**Known TPM provider (Park Place, Service Express, Curvature):**
> "With the Park Place and Service Express merger, a lot of teams have been taking a fresh look at their TPM relationships. Have you had a chance to renegotiate since the merger, or are you still on the same rates?"

### DWDM / SmartOptics Talking Points

- Cost: 30-50% below Ciena and Nokia. Minimal licensing.
- Space + power: significant reduction vs. traditional DWDM platforms.
- Simplicity: easier to deploy, simplified sparing vs. traditional pluggables.
- Lead times: ships faster than OEMs and commodity vendors.
- Pedigree: backed by original engineering core. Not grey market.

---

## Brian's Voice — Always

- Direct, no-nonsense, outcomes over transactions
- Short emails — 3-4 paragraphs max, most under 100 words
- First person, specific, no corporate language
- Confident but not aggressive
- Never uses em dashes, en dashes, or hyphens in prose
- Never uses AI vocabulary (see Step 6)

---

## Why this skill exists

`aaa-hubspot-7-step` wrote 7 emails to the contact's AI fields and stopped there. Useful, but no research enrichment, no LinkedIn task, no call script, no suggested cadence — Brian had to remember to do each of those manually.

`abc-7step-master` did all of that plus the full queue + auto-send. Powerful, but the auto-send half doesn't fit Brian's current workflow when he wants to draft into HubSpot and send manually.

`aaa-hs-7step` is the right middle: the research, the contact create, the approved vendor wedge, the 7 humanized emails, the LinkedIn task, the full Orum-ready call script package saved as a HubSpot note, the cadence suggestion, and the field write. No queue, no auto-send. Brian owns the send.
