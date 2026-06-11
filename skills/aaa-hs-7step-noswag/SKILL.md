---
name: aaa-hs-7step-noswag
description: "Runs the OSI Global fully-personalized 7-email sequence. All 7 emails are uniquely researched and customized for the prospect — no fixed swag templates. Email 1 is a curiosity/teaser opener, Email 2 is a social proof/peer story touch, Email 3 is a specific pain-point hook, Emails 4-7 follow the standard personalized cadence. Saves all 7 subject + body fields to the HubSpot contact, creates a LINKED_IN_CONNECT task, generates a full Orum call script note, and prints a suggested cadence for manual sending. No queue. No auto-send. ALWAYS use when Brian says 'aaa-hs-7step-noswag', 'noswag sequence', 'no swag', 'fully personalized 7 step', 'all custom emails', 'no swag 7 step', or pastes a contact and wants all 7 emails fully customized on the HubSpot record."
---

# aaa-hs-7step-noswag — OSI Global Fully-Personalized 7-Email Draft to HubSpot

All 7 emails are fully personalized and researched. No fixed templates. Saves all 14 AI field properties to the HubSpot contact, creates a LINKED_IN_CONNECT task, generates an Orum-ready call script note, and prints a suggested cadence. Brian sends manually.

**What this skill does NOT do:**
- Does not write to `email-queue.json`. No queue.
- Does not invoke the `osi-email-sender`. Nothing auto-sends.
- Does not open Chrome or Outlook to fire Email 1 live.

**What this skill DOES do:**
1. Gathers prospect info and looks up or creates the HubSpot contact under Brian's ownership.
2. Checks for an existing draft on the AI fields and warns before overwriting.
3. Researches the prospect thoroughly for all 7 emails.
4. Writes all 7 emails fully personalized in Brian's voice, humanizes them, generates 5 subject options each.
5. Drafts a LinkedIn invite and creates a LINKED_IN_CONNECT task on the contact.
6. Generates a full Orum-ready call script package saved as a HubSpot note.
7. Prints a suggested cadence.
8. On "save," writes all 14 AI field properties in a single call.

---

## Step 1 — Gather Prospect Info

Ask Brian for or extract from what he pasted:
- Full name (capture the first name separately, it is required for the email greeting in Step 5)
- Title
- Company and domain
- Email address (required — see Step 1a)
- LinkedIn URL if available
- Any context (pain points, source, notes)

If Brian pasted a HubSpot contact record or LinkedIn profile, parse fields directly.

### Step 1a — STOP IF NO EMAIL

This skill writes 7 emails to a HubSpot contact record. No email = no contact lookup = nowhere to save. If neither Brian's input nor a quick ZoomInfo lookup returns a valid email, STOP. Tell Brian and suggest the LinkedIn-only fallback (LINKED_IN_CONNECT task + a second LI message task two weeks later).

---

## Step 2 — HubSpot Contact + Draft Check + Approved Vendor Check

### 2a. Contact lookup or create

Use `mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__search_crm_objects` to search HubSpot contacts by email. Pull `ai_email_subject_1` along with the standard fields — Step 2b needs it.

If found, capture the **contact ID**, refresh `jobtitle` from LinkedIn (LinkedIn is authoritative), and reassign `hubspot_owner_id` to `213536174` (Brian) if not already.

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

If `ai_email_subject_1` on the contact already has content, tell Brian:

> Contact already has AI Email Subject 1 populated: `[first 60 chars of existing subject]...`. Overwrite all 7 fields with a fresh sequence?

Wait for an explicit "overwrite", "yes", "refresh", or equivalent. Without that, stop. If blank or brand new, proceed without a prompt.

### 2c. Approved vendor check

Read `C:\Users\Mini\Documents\osi-claude-brain\approved-vendors.json`. Case-insensitive substring match against the `approved_vendor_companies` list. If the file doesn't exist, skip — never invent approved-vendor language.

**If match:** add one soft approved-vendor line to Email 4 (the standard cold intro). Example: "Side note, we're already on your approved vendor list, so no new vendor onboarding if anything ever needs to move fast." One brief reminder in Email 6 or 7. No other mentions. Never say "vetted" or "pre-approved." Never mention "procurement" in Email 4.

**If no match:** never mention it anywhere.

---

## Step 3 — Research the Prospect (for all 7 emails)

Web-search the company and role. Pull what they do, scale, public tech stack, any 30-day news. Decide which OSI pillar leads:

- **Network / telecom / colocation / carrier** → optics + DWDM + supply chain reliability; TPM second
- **Bank / financial institution** → optics, free SFP wedge; never lead TPM
- **Software / cloud / SaaS** → optics, high-density connectivity, lead time
- **Enterprise IT / manufacturing / consulting** → TPM cost savings + EOL coverage
- **Procurement / IT Director / VP** → OpEx reclamation, vendor simplification, competitive TPM bid

Capture:
- **Personal Hook** — 1-2 specific concrete details about this person's role, company, or background to weave into Email 1
- **Fresh Hook** — one targeted web search for 30-day company news. If nothing in 30 days, fall back to Personal Hook alone
- **Social Proof Angle** — identify a comparable company or vertical peer that would resonate (e.g., "another regional carrier," "a similar-sized bank," "a manufacturing shop in [region]"). Do NOT name actual customer names unless Brian has already confirmed publicly referenceable accounts.
- **Specific Pain Hook** — one focused technical or business pain point highly likely for their exact role and company size (e.g., lead time gaps, EOL gear, TPM renewal pressure, optics sourcing)

---

## Step 4 — Determine Sequence Type

| Sequence | Target roles | Lead angle |
|---|---|---|
| Network | Network Engineer, Architect, Transport Engineer | Free SFP sample |
| Server | Systems Engineer, Infrastructure Engineer, Server Admin | Free DIMM sample |
| TPM | IT Director, DC Manager, Asset Manager, Procurement, mid-market CIO | OEM cost pain |
| DWDM | Transport Engineer, Optical NE, Network Planner at carrier/CLEC/MSO | Cost vs Ciena/Nokia |
| Storage | Storage Admin, Storage Engineer | Pre-owned NetApp + TPM |
| Pre-owned | Cisco/Juniper/Arista environments | Pre-owned gear + OSI TPM |

---

## Step 5 — Write All 7 Emails (Fully Personalized)

Brian's voice: direct, no-nonsense, outcomes over transactions, zero corporate fluff. Short. Mobile-friendly. Scannable in 10 seconds. No signature block, Brian's Outlook sig or HubSpot template handles that.

🚨 **GREETING: every email opens with the prospect's real first name.** Every one of the 7 emails starts with `Hi [First Name],` on its own line, where [First Name] is the prospect's ACTUAL first name from the HubSpot `firstname` field (or LinkedIn / Brian's input). Substitute the real name into the text BEFORE writing the body. NEVER leave a literal `[First Name]` token in the email, and NEVER write an empty greeting like `Hi ,`. If the first name is blank or unknown, STOP and resolve it (re-read the HubSpot contact, the LinkedIn profile, or ask Brian) before writing any email. After the greeting line, continue with the email's opening sentence described below.

### Email 1 — Curiosity / Teaser Opener

- 2-3 very short paragraphs, under 80 words total
- Open with one sentence that names the exact problem or situation specific to their role and vertical — not a generic intro
- Reference the Personal Hook or Fresh Hook (something specific from research)
- No pitch, no product names yet — just prove you know their world
- End with one micro-question that invites a one-word reply (e.g., "Is that on your radar right now?" or "Does that sound familiar?")
- End body with just `Brian` on its own line

Generate 5 subject line options. Mix: 2-3 professional/catchy + 2 outlandish/unexpected. No hyphens. Randomly select one; mark it clearly so Brian can choose a different one before "save."

### Email 2 — Social Proof / Peer Story

- 3-4 short paragraphs, most under 100 words
- Open with a brief reference to a comparable company type or vertical peer that faced the same issue (do NOT name specific customer unless publicly referenceable — use "a [regional carrier / bank / manufacturer] similar to [Company]")
- Describe what the peer was dealing with and what changed (lead times, OEM cost, EOL gaps, TPM renewal)
- Connect it naturally to what Brian does at OSI and why it's relevant to this prospect
- One clear soft ask: "Worth a quick call to see if it applies to your setup?"
- End with `Brian`

Generate 5 subject line options. Mix professional and unexpected. Randomly select one; mark it.

### Email 3 — Specific Pain Point / Direct Challenge

- 2-3 short paragraphs
- Open by naming a specific operational or financial pain point that is highly likely for their role, vertical, and company size (from research in Step 3)
- Be specific — reference their tech stack, gear type, or business context if visible
- Offer one concrete thing OSI does that directly addresses that pain
- No ask beyond "is this worth 15 minutes?" or similar
- If approved vendor match and not yet used: include one soft approved-vendor line here (see Step 2c)
- End with `Brian`

Generate 5 subject line options. Mix professional and unexpected. Randomly select one; mark it.

### Email 4 — Cold Intro / OSI Value Prop (standard personalized touch)

- 3-4 short paragraphs, most under 100 words
- Open with what problem you solve for people in their role
- Reference a detail from research
- If approved vendor and not already used in Email 3: include the soft one-line note here
- One clear ask: 15-minute call
- End body with just `Brian` on its own line

Generate 5 subject line options. Mix: 2-3 professional/catchy + 2 outlandish/unexpected. No hyphens. Randomly select one; mark it clearly so Brian can choose a different one before "save."

### Email 5 — Different Angle

- Pivot to a DIFFERENT OSI pillar than Email 4 (optics if Email 4 was TPM, or vice versa)
- Do not repeat what was in Emails 1-4
- 2-3 short paragraphs
- No hard ask — soft "worth a conversation if..."
- End with `Brian`

Generate 5 subject line options. Select one randomly; mark it.

### Email 6 — Pattern Interrupt

- Single direct yes/no question about their specific environment
- Pick the most relevant from research: EOL gear, contract renewals, optics gaps, DWDM capacity, TPM rate review
- 2-3 sentences only
- "If yes, worth talking. If no, I'll stop bothering you."
- If approved vendor and not yet used the reminder, add it here briefly
- End with `Brian`

Generate 5 subject line options. Select one randomly; mark it.

### Email 7 — Breakup

- Short, respectful, leaves the door open
- Acknowledge you've sent several notes, respect their time
- No pitch
- Examples: "Should I close the file on this one, or is the timing just off?" or "No worries if now isn't the right time. Happy to circle back when things shift."
- End with `Brian`

Generate 5 subject line options. Select one randomly; mark it.

---

## Step 6 — Humanize All 7 Emails

Run every email through this filter. Anything that fails gets rewritten:

- **No AI vocabulary:** remove "crucial," "pivotal," "landscape," "underscore," "delve," "showcase," "testament," "enhance," "foster," "garner"
- **No hyphens** in bodies or subject lines. Rewrite "end-of-life" → "end of life", "third-party" → "third party"
- **No em dashes (—)** anywhere. Split into two sentences if needed.
- **No rule of three.** Break triple-item lists into natural prose.
- **No -ing pile-up** at sentence tails.
- **No negative parallelisms.** Remove "it's not just X, it's Y."
- **Vary sentence length.** Mix short punchy sentences with longer ones.
- **Use is/are/has** instead of "serves as," "stands as," "functions as."
- **First-name greeting check.** Confirm every email body begins with `Hi [actual first name],` using the prospect's real first name. Reject any email that opens with `Hi ,`, a blank greeting, or a literal `[First Name]` or `[Name]` token. Fix before continuing.
- **Final read-aloud check.** If it sounds like a press release, rewrite.

---

## Step 7 — LinkedIn Invite Draft + Create LINKED_IN_CONNECT Task

### 7a. Draft the LinkedIn invite

Under 300 characters (LinkedIn hard limit). Personalized: reference role, vertical pain, or the Personal Hook. No pitch. No product names. One sentence plus one short reason to connect.

### 7b. Create the HubSpot task

Using `mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__manage_crm_objects`:

- `hs_task_type` = `LINKED_IN_CONNECT`
- `hs_task_subject` = `Send LinkedIn Request — [First Last] | [Company]`
- `hs_task_body` = the literal LinkedIn message draft from 7a
- `hs_task_status` = `NOT_STARTED`
- `hs_timestamp` = today's date in epoch ms
- `hs_task_priority` = `HIGH`
- `hubspot_owner_id` = `213536174`
- Associate to the contact

**Verify after creating:** fetch the task back, confirm `hs_task_body` is the actual message (not a placeholder). If it's a placeholder, update immediately.

Confirm in chat: `LinkedIn task created on contact [HubSpot URL] — due today.`

---

## Step 8 — Generate Full Call Script Package + HubSpot Note

Do this automatically before presenting to Brian.

### 8a. Voicemail Script

15 seconds max. One-sentence hook from the Personal Hook. Reference the Email 4 subject line. End with Brian's email spelled audibly ("that's bc at osihardware dot com"). No phone number. Present or future tense only. Apply humanization rules.

### 8b. Live Call Script (Orum surface)

Fully written — no bracket tokens remaining. Substitute every [Name], [Title], [Company], [Vertical] with actual prospect data before saving.

Structure:

---

**VOICEMAIL**
[Fully written voicemail from 8a — no brackets]

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
[Pick the single best-fit opener from the library. State it fully with the prospect's actual first name substituted in. One sentence explaining why you picked it.]

---

**BRIDGE**
"The reason I'm reaching out is [one sentence from Email 4 — the core value prop for their role and vertical]. I sent you an email about this — subject line was [Email 4 selected subject]. Did you get a chance to see it?"

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

"Send me an email / I'll look at your email" → "Already did — subject was [Email 4 selected subject]. I'll make sure it didn't land in spam. Is [email address] still the best place to reach you?"

"Not interested" → "Fair enough. Is it timing, or is this genuinely not a fit for your team right now?" [If timing: "Got it. When would be a better time to circle back?"] [If not a fit: "No worries at all. Thanks for being straight with me."]

"Too busy right now" → "I'll be quick. One question: is [core pain point from opener] something that's come up for your team in the last six months? If yes, worth 15 minutes. If no, I'll leave you alone."

---

**VOICEMAIL (if no answer)**
[Repeat the voicemail from 8a here for quick reference]

---

### 8c. Save as HubSpot Note

Using `mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__manage_crm_objects`, create a note on the contact:

- `hs_note_body` = full call script text from 8b
- `hs_timestamp` = today's date in epoch ms
- `hubspot_owner_id` = `213536174`
- Associate to the contact

**Token verification before saving:** scan for any remaining bracket tokens ([Name], [First Name], [Title], [Company], [Vertical], etc.). Substitute with actual prospect data. A note with unresolved tokens is worse than no note.

Confirm in chat: `Call script note saved to contact [HubSpot URL].`

---

## Step 9 — Print Suggested Cadence

Use these gaps from today with weekend skipping (Saturday or Sunday → push to next Monday):

| # | Suggested day | Date | Notes |
|---|---|---|---|
| 1 | Today | [today's date, weekday] | Curiosity/teaser opener |
| 2 | +2 business days | [date] | Social proof / peer story |
| 3 | +2 bd after Email 2 | [date] | Specific pain point / direct challenge |
| 4 | +3 bd after Email 3 | [date] | Cold intro / OSI value prop |
| 5 | +4 bd after Email 4 | [date] | Different angle |
| 6 | +4 bd after Email 5 | [date] | Pattern interrupt |
| 7 | +10 bd after Email 6 | [date] | Breakup |

Total span: ~25 business days. Dates are a guide — Brian sends when he sends.

**BCC reminder:** when sending from Outlook, BCC `bc@osihardware.com` and `21878985@bcc.hubspot.com`. If sending from HubSpot native UI, only the inbox BCC matters.

---

## Step 10 — Present for Review — Wait for "Save"

Present everything to Brian in one block:

1. **Prospect summary** — name, title, company, OSI angle, sequence type, approved vendor Y/N, HubSpot contact ID + URL
2. **Suggested cadence table** from Step 9
3. **Emails 1-7** — 5 subject line options each with selected one marked; full body of each email
4. **LinkedIn invite text** with character count under 300
5. **Confirmation that the LinkedIn task was created** (link to contact)
6. **Voicemail script** from Step 8a
7. **Recommended opener** from Step 8b (the single best-fit with prospect's actual first name)
8. **Confirmation that the call script note was saved** (link to contact)
9. **What "save" will do** — write all 14 AI field properties to the contact in one call

**Stop. Do not write to HubSpot AI fields yet. Wait.**

End with: `Look it over and say **save** when you're ready.`

---

## Step 11 — On "Save" — Write 14 Properties to HubSpot AI Fields

When Brian says "save" (or any clear go-ahead: "looks good", "ship it", "do it", "overwrite"):

Use `mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__manage_crm_objects` with an `update` on the contact ID from Step 2a. Write all 14 properties in a single call:

| Email # | Subject property | Body property |
|---|---|---|
| 1 | `ai_email_subject_1` | `ai_email_body_1` |
| 2 | `ai_email_subject_2` | `ai_email_body_2` |
| 3 | `ai_email_subject_3` | `ai_email_body_3` |
| 4 | `ai_email_subject_4` | `ai_email_body_4` |
| 5 | `ai_email_subject_5` | `ai_email_body_5` |
| 6 | `ai_email_subject_6` | `ai_email_body_6` |
| 7 | `ai_email_subject_7` | `ai_email_body_7` |

**Field value rules:**
- All 7 subjects: the selected subject from the 5 generated options for each email
- All 7 bodies: the exact personalized body for each email

**Verify after write:** fetch the contact back and confirm `ai_email_subject_1` is populated and `ai_email_body_1` matches the written content. Also confirm each `ai_email_body_N` opens with the prospect's real first name (a `Hi [First Name],` greeting) and contains no empty `Hi ,` and no unsubstituted `[First Name]` or `[Name]` token. If blank or wrong, retry once. If still fails, tell Brian which fields didn't write.

### 11a. Confirm

Confirm in chat:
- `HubSpot AI fields populated: ai_email_subject_1-7 + ai_email_body_1-7 on contact [HubSpot URL].`
- `LinkedIn task created and due today.`
- `Call script note on contact — voicemail + 12-opener library + bridge + discovery + objections.`
- `Suggested cadence above — send manually starting today.`
- `No queue, no auto-send. Your call when to fire each email.`

---

## OSI Messaging Reference (for all 7 emails)

### OSI Product Lines

1. **Optics** — SmartOptics transceivers, private-labeled. Free sample is the opening wedge.
2. **DWDM and Open Line Systems** — SmartOptics DCP platform, 30-50% below Ciena/Nokia. Ships fast.
3. **Compute and Components** — DIMMs from Samsung / Hynix / Micron.
4. **Storage** — NetApp TPM, pre-owned storage.
5. **TPM** — 40-60% below OEM. Multi-vendor. Gartner-recognized, privately owned, no PE.
6. **Pre-Owned and New Networking** — Pre-owned Cisco/Juniper/Arista. New Nokia authorized.
7. **Professional Services** — Strong signal only. Never lead cold.

### Vertical Intelligence — Cheat Sheet

**Telco / service providers:** lead optics + supply chain reliability. TPM rarely the opener at engineer level.

**Banks / large financial:** lead optics, free SFP wedge at engineer level. Do NOT lead TPM. Park Place / Service Express merger wedge if they have known TPM.

**Professional services / consulting:** TPM viable opener. Lead pain, not price.

**Manufacturing:** free optics as break-glass insurance. TPM for aging Cisco gear.

**Healthcare:** TPM with documented SLAs. DIMMs for server refresh. Gartner-recognized + privately owned + no PE matters here.

### TPM Positioning

**Known TPM provider (Park Place, Service Express, Curvature):**
> "With the Park Place and Service Express merger, a lot of teams have been taking a fresh look at their TPM relationships. Have you had a chance to renegotiate since the merger, or are you still on the same rates?"

### DWDM / SmartOptics Talking Points

- Cost: 30-50% below Ciena and Nokia. Minimal licensing.
- Space + power: significant reduction vs. traditional DWDM platforms.
- Lead times: ships faster than OEMs and commodity vendors.

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

`aaa-hs-7step-noswag` is the fully-personalized version of the 7-step sequence. Unlike `aaa-hs-7step-swag` (which opens with three fixed address-confirm swag templates), this skill writes all 7 emails from scratch based on prospect research. Email 1 is a curiosity/teaser opener, Email 2 is a social proof peer story, Email 3 is a specific pain-point challenge — then Emails 4-7 follow the standard personalized cadence (value prop, different angle, pattern interrupt, breakup). Use this when the swag hook isn't the right opener, when Brian is targeting a senior buyer, or when he wants maximum personalization across the full sequence. Same HubSpot AI field workflow — no queue, no auto-send, Brian owns the send.
