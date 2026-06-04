---
name: aaa-hs-7step-swag
description: "Runs the OSI Global swag-first 7-email sequence. Emails 1-3 are fixed swag / address-confirm touches (RE: Confirming address). Emails 4-7 are fully personalized to the prospect. Saves all 7 subject + body fields to the HubSpot contact, creates a LINKED_IN_CONNECT task, generates a full Orum call script note, and prints a suggested cadence for manual sending. No queue. No auto-send. ALWAYS use when Brian says 'aaa-hs-7step-swag', 'swag sequence', 'swag first', 'swag 7 step', 'send the swag emails', 'swag outreach', or pastes a contact and wants the address-confirm swag sequence drafted on the HubSpot record."
---

# aaa-hs-7step-swag — OSI Global Swag-First 7-Email Draft to HubSpot

Emails 1-3 are fixed swag / address-confirm touches. Emails 4-7 are fully personalized. Saves all 14 AI field properties to the HubSpot contact, creates a LINKED_IN_CONNECT task, generates an Orum-ready call script note, and prints a suggested cadence. Brian sends manually.

**What this skill does NOT do:**
- Does not write to `email-queue.json`. No queue.
- Does not invoke the `osi-email-sender`. Nothing auto-sends.
- Does not open Chrome or Outlook to fire Email 1 live.

**What this skill DOES do:**
1. Gathers prospect info and looks up or creates the HubSpot contact under Brian's ownership.
2. Checks for an existing draft on the AI fields and warns before overwriting.
3. Writes Emails 1-3 as fixed swag/address-confirm content (no personalization needed).
4. Researches the prospect for Emails 4-7: Personal Hook, Fresh Hook, OSI angle.
5. Writes Emails 4-7 fully personalized in Brian's voice, humanizes them, generates 5 subject options each.
6. Drafts a LinkedIn invite and creates a LINKED_IN_CONNECT task on the contact.
7. Generates a full Orum-ready call script package saved as a HubSpot note.
8. Prints a suggested cadence.
9. On "save," writes all 14 AI field properties in a single call.

---

## Step 1 — Gather Prospect Info

Ask Brian for or extract from what he pasted:
- Full name (capture the first name separately, it is required for the email greetings in Steps 3 and 6)
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

**If match:** add one soft approved-vendor line to Email 4 (the first personalized email). Example: "Side note, we're already on your approved vendor list, so no new vendor onboarding if anything ever needs to move fast." One brief reminder in Email 6 or 7. No other mentions. Never say "vetted" or "pre-approved." Never mention "procurement" in Email 4.

**If no match:** never mention it anywhere.

---

## Step 3 — Write Emails 1-3 (Fixed Swag Content)

Emails 1-3 are always the same. No personalization. No research needed. Write exactly as specified below.

### Email 1 — Address Confirm / Swag Intro

**Subject (fixed — no options, no variation):**
`RE: Confirming address`

**Body (fixed swag text, with first-name greeting):**
> Hi [First Name],
>
> I'm just prepping this package for you. I have a box of swag and a pair of sample SFPs to send to you from the team here at OSI Global IT.
>
> Do you come into the office? Is that the best address to send it to right now?
>
> Best,

The first line `Hi [First Name],` uses the prospect's ACTUAL first name from the HubSpot `firstname` field, substituted before sending. Never leave the literal `[First Name]` token and never send `Hi ,`. The rest of the body is fixed exactly as shown.

The "RE:" makes it look like a follow-up in their inbox. This is not a literal reply — it's a new email with a manufactured subject. If they reply with an address, Brian ships the swag and pauses the remaining touches manually.

### Email 2 — "Any thoughts?"

**Subject (fixed — no options, no variation):**
`RE: Confirming address`

**Body (fixed, exact text, NO greeting by design):**
> Any thoughts?
>
> Best,

Email 2 stays bare with no first-name greeting. It rides the Email 1 thread as a terse one-line nudge. Do NOT add `Hi [First Name],` here.

Short by design. Rides the Email 1 thread visually.

### Email 3 — Follow-up on Missed Email

**Subject (fixed — no options, no variation):**
`RE: Confirming address`

**Body (fixed swag text, with first-name greeting):**
> Hi [First Name],
>
> Not sure if you missed my email below, so I am following up on it. No big deal, but wanted to make sure! I have a box of swag and SFP samples to send to you…
>
> Cheers!

The first line `Hi [First Name],` uses the prospect's ACTUAL first name, substituted before sending. Never leave the literal token and never send `Hi ,`. The rest of the body is fixed exactly as shown.

---

## Step 4 — Research the Prospect (for Emails 4-7)

Web-search the company and role. Pull what they do, scale, public tech stack, any 30-day news. Decide which OSI pillar leads:

- **Network / telecom / colocation / carrier** → optics + DWDM + supply chain reliability; TPM second
- **Bank / financial institution** → optics, free SFP wedge; never lead TPM
- **Software / cloud / SaaS** → optics, high-density connectivity, lead time
- **Enterprise IT / manufacturing / consulting** → TPM cost savings + EOL coverage
- **Procurement / IT Director / VP** → OpEx reclamation, vendor simplification, competitive TPM bid

Capture 1-2 specific concrete details to weave into Email 4 — this is the **Personal Hook**. Also run one targeted web search for 30-day company news (**Fresh Hook**). If nothing in 30 days, fall back to Personal Hook alone.

---

## Step 5 — Determine Sequence Type (for Emails 4-7)

| Sequence | Target roles | Lead angle |
|---|---|---|
| Network | Network Engineer, Architect, Transport Engineer | Free SFP sample |
| Server | Systems Engineer, Infrastructure Engineer, Server Admin | Free DIMM sample |
| TPM | IT Director, DC Manager, Asset Manager, Procurement, mid-market CIO | OEM cost pain |
| DWDM | Transport Engineer, Optical NE, Network Planner at carrier/CLEC/MSO | Cost vs Ciena/Nokia |
| Storage | Storage Admin, Storage Engineer | Pre-owned NetApp + TPM |
| Pre-owned | Cisco/Juniper/Arista environments | Pre-owned gear + OSI TPM |

---

## Step 6 — Write Emails 4-7 (Fully Personalized)

Brian's voice: direct, no-nonsense, outcomes over transactions, zero corporate fluff. Short. Mobile-friendly. Scannable in 10 seconds. No signature block, Brian's Outlook sig or HubSpot template handles that.

🚨 **GREETING: Emails 4, 5, 6, and 7 each open with the prospect's real first name.** Every personalized email starts with `Hi [First Name],` on its own line, where [First Name] is the prospect's ACTUAL first name from the HubSpot `firstname` field (or LinkedIn / Brian's input), substituted into the text BEFORE writing the body. NEVER leave a literal `[First Name]` token and NEVER write an empty `Hi ,`. If the first name is blank or unknown, STOP and resolve it (re-read the HubSpot contact, the LinkedIn profile, or ask Brian) before writing. After the greeting line, continue with the email's opening sentence below. (Email 2 is the only exception in this sequence: it stays bare per Step 3.)

### Email 4 — Cold Intro / OSI Value Prop (first personalized touch)

- 3-4 short paragraphs, most under 100 words
- Open with what problem you solve for people in their role
- Reference the Personal Hook or Fresh Hook (something specific from research)
- If approved vendor: include the soft one-line note (see Step 2c)
- One clear ask: 15-minute call
- End body with just `Brian` on its own line

Generate 5 subject line options. Mix: 2-3 professional/catchy + 2 outlandish/unexpected. No hyphens. Randomly select one; mark it clearly so Brian can choose a different one before "save."

### Email 5 — Different Angle

- Pivot to a DIFFERENT OSI pillar than Email 4 (optics if Email 4 was TPM, or vice versa)
- Do not repeat what was in Email 4
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

## Step 7 — Humanize Emails 4-7

Run every personalized email through this filter. Anything that fails gets rewritten:

- **No AI vocabulary:** remove "crucial," "pivotal," "landscape," "underscore," "delve," "showcase," "testament," "enhance," "foster," "garner"
- **No hyphens** in bodies or subject lines. Rewrite "end-of-life" → "end of life", "third-party" → "third party"
- **No em dashes (—)** anywhere. Split into two sentences if needed.
- **No rule of three.** Break triple-item lists into natural prose.
- **No -ing pile-up** at sentence tails.
- **No negative parallelisms.** Remove "it's not just X, it's Y."
- **Vary sentence length.** Mix short punchy sentences with longer ones.
- **Use is/are/has** instead of "serves as," "stands as," "functions as."
- **First-name greeting check.** Confirm Emails 4-7 each begin with `Hi [actual first name],` using the prospect's real first name. Reject any that open with `Hi ,`, a blank greeting, or a literal `[First Name]` or `[Name]` token. Confirm Emails 1 and 3 also carry the substituted first-name greeting, and that Email 2 stays bare. Fix before continuing.
- **Final read-aloud check.** If it sounds like a press release, rewrite.

---

## Step 8 — LinkedIn Invite Draft + Create LINKED_IN_CONNECT Task

### 8a. Draft the LinkedIn invite

Under 300 characters (LinkedIn hard limit). Personalized: reference role, vertical pain, or the Personal Hook. No pitch. No product names. One sentence plus one short reason to connect.

### 8b. Create the HubSpot task

Using `mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__manage_crm_objects`:

- `hs_task_type` = `LINKED_IN_CONNECT`
- `hs_task_subject` = `Send LinkedIn Request — [First Last] | [Company]`
- `hs_task_body` = the literal LinkedIn message draft from 8a
- `hs_task_status` = `NOT_STARTED`
- `hs_timestamp` = today's date in epoch ms
- `hs_task_priority` = `HIGH`
- `hubspot_owner_id` = `213536174`
- Associate to the contact

**Verify after creating:** fetch the task back, confirm `hs_task_body` is the actual message (not a placeholder). If it's a placeholder, update immediately.

Confirm in chat: `LinkedIn task created on contact [HubSpot URL] — due today.`

---

## Step 9 — Generate Full Call Script Package + HubSpot Note

Do this automatically before presenting to Brian.

### 9a. Voicemail Script

15 seconds max. One-sentence hook from the Personal Hook. Reference the Email 4 subject line (the first personalized email — that's what Brian referenced on the call, not the swag email). End with Brian's email spelled audibly ("that's bc at osihardware dot com"). No phone number. Present or future tense only. Apply humanization rules.

### 9b. Live Call Script (Orum surface)

Fully written — no bracket tokens remaining. Substitute every [Name], [Title], [Company], [Vertical] with actual prospect data before saving.

Structure:

---

**VOICEMAIL**
[Fully written voicemail from 9a — no brackets]

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
[Repeat the voicemail from 9a here for quick reference]

---

### 9c. Save as HubSpot Note

Using `mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__manage_crm_objects`, create a note on the contact:

- `hs_note_body` = full call script text from 9b
- `hs_timestamp` = today's date in epoch ms
- `hubspot_owner_id` = `213536174`
- Associate to the contact

**Token verification before saving:** scan for any remaining bracket tokens ([Name], [First Name], [Title], [Company], [Vertical], etc.). Substitute with actual prospect data. A note with unresolved tokens is worse than no note.

Confirm in chat: `Call script note saved to contact [HubSpot URL].`

---

## Step 10 — Print Suggested Cadence

Use these gaps from today with weekend skipping (Saturday or Sunday → push to next Monday):

| # | Suggested day | Date | Notes |
|---|---|---|---|
| 1 | Today | [today's date, weekday] | Swag intro — "RE: Confirming address" |
| 2 | +2 business days | [date] | "Any thoughts?" |
| 3 | +2 bd after Email 2 | [date] | Follow-up on missed email |
| 4 | +3 bd after Email 3 | [date] | Cold intro / OSI value prop (personalized) |
| 5 | +4 bd after Email 4 | [date] | Different angle (personalized) |
| 6 | +4 bd after Email 5 | [date] | Pattern interrupt (personalized) |
| 7 | +10 bd after Email 6 | [date] | Breakup (personalized) |

Total span: ~25 business days. Dates are a guide — Brian sends when he sends.

**BCC reminder:** when sending from Outlook, BCC `bc@osihardware.com` and `21878985@bcc.hubspot.com`. If sending from HubSpot native UI, only the inbox BCC matters.

---

## Step 11 — Present for Review — Wait for "Save"

Present everything to Brian in one block:

1. **Prospect summary** — name, title, company, OSI angle, sequence type, approved vendor Y/N, HubSpot contact ID + URL
2. **Suggested cadence table** from Step 10
3. **Emails 1-3** — fixed swag content (confirm the exact text is shown; no subject line options needed since they're fixed)
4. **Emails 4-7** — 5 subject line options each with selected one marked; full body of each email
5. **LinkedIn invite text** with character count under 300
6. **Confirmation that the LinkedIn task was created** (link to contact)
7. **Voicemail script** from Step 9a
8. **Recommended opener** from Step 9b (the single best-fit with prospect's actual first name)
9. **Confirmation that the call script note was saved** (link to contact)
10. **What "save" will do** — write all 14 AI field properties to the contact in one call

**Stop. Do not write to HubSpot AI fields yet. Wait.**

End with: `Look it over and say **save** when you're ready.`

---

## Step 12 — On "Save" — Write 14 Properties to HubSpot AI Fields

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
- Emails 1-3 subjects: all exactly `RE: Confirming address`
- Emails 1-3 bodies: exact fixed text from Step 3
- Emails 4-7 subjects: the selected subject from the 5 options
- Emails 4-7 bodies: the exact personalized body

**Verify after write:** fetch the contact back and confirm `ai_email_subject_1` = `RE: Confirming address` and `ai_email_body_1` matches the fixed swag text. Also confirm the first-name greeting landed: `ai_email_body_1`, `ai_email_body_3`, and `ai_email_body_4` through `ai_email_body_7` each open with the prospect's real first name (a `Hi [First Name],` line) with no empty `Hi ,` and no unsubstituted `[First Name]` token, and `ai_email_body_2` stays bare (`Any thoughts?`, no greeting). If blank or wrong, retry once. If still fails, tell Brian which fields didn't write.

### 12a. Confirm

Confirm in chat:
- `HubSpot AI fields populated: ai_email_subject_1-7 + ai_email_body_1-7 on contact [HubSpot URL].`
- `LinkedIn task created and due today.`
- `Call script note on contact — voicemail + 12-opener library + bridge + discovery + objections.`
- `Suggested cadence above — send manually starting today.`
- `No queue, no auto-send. Your call when to fire each email.`

---

## OSI Messaging Reference (for Emails 4-7)

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
- Never uses AI vocabulary (see Step 7)

---

## Why this skill exists

`aaa-hs-7step-swag` flips the sequence. Instead of leading with a personalized cold intro, it opens with three low-pressure address-confirm / swag touches (Emails 1-3). If the prospect engages on the swag thread, Brian ships and pauses. If not, the sequence transitions into fully personalized OSI value prop emails (4-7). Same HubSpot AI field workflow as `aaa-hs-7step` — no queue, no auto-send, Brian owns the send.
