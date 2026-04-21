---
name: osi-3email-new
description: >
  Generate a hyper-personalized 3-email new outreach sequence for OSI Global prospects.
  Use this skill when Andy uploads or pastes a LinkedIn profile and wants a shorter outreach
  treatment — for directors, targets where a full sequence is overkill, or when a tighter
  cadence fits better. Triggers on: "3-email sequence," "short sequence," "3 emails for [name],"
  "new outreach 3 emails," or any time Andy drops a profile and asks for outreach without
  specifying a full sequence. Always run this skill before writing any 3-email cold outreach.
---

> **SYNC NOTE:** This skill exists in two locations: `Claude-Brain/skills/osi-3email-new/` (OneDrive — source of truth) and local Cowork `.claude/skills/`. Any edits must be applied to both. If returning after days away, check OneDrive version first and sync local if newer.

# OSI Global 3-Email New Outreach Sequence

## Your job

Andy has given you a LinkedIn profile. This is a first-touch outreach where a shorter sequence is appropriate. Produce the full outreach package: strategy note, call scripts, LinkedIn invite, and individual HubSpot email tasks — each ready to press send.

Read this entire skill before producing any output.

---

## Andy Rules — apply to every output

- No em-dashes (—) anywhere. Not once. Split into two sentences if needed.
- Keep prose tight and direct. No fluff.
- Emails must feel like a human wrote them to one person, not a mass blast.
- Tone: peer-to-peer, not vendor-to-buyer.
- Emails are short. Mobile-friendly. Scannable in 10 seconds.

---

## Active Sequence Check — hard stop before anything else

Before any other work on this prospect, check the email queue. This prevents stacking duplicate sequences on the same person, which wrecks sender reputation and is bad form.

Open `C:\Users\Andy\OneDrive - OSI Hardware\Documents\Claude\Claude-Brain\email-queue.json` using the OneDrive-safe Python read pattern (try local `open(path,'r')` first, fall back to SharePoint MCP on EINVAL). Scan every entry for a match with this prospect:

- Match by `to` field equal to the prospect's email address (case-insensitive), OR
- Match by `prospectName` + `company` both matching the prospect's full name and company (case-insensitive)

**SKIP this prospect entirely if any matched entry has:**
- `status: "pending"` (already enrolled in an active sequence), OR
- `status: "sent"` with a `sendDate` within the last 30 calendar days (sequence recently completed)

Entries with status `paused-*`, `canceled-*`, or older `sent` (>30 days ago) do NOT block. Proceed normally in those cases, but note in the strategy note that a prior sequence completed on [date] so this run is effectively a re-engagement.

**Skip behavior by mode:**

- **Interactive mode:** Tell Andy:
  > SKIPPED: [First Last] at [Company] — [reason: "already enrolled, N emails pending, next send [date]" OR "recent sequence completed [date]"]. Override?

  Wait for explicit "override" from Andy before proceeding. Without override, stop and move on to the next prospect (batch mode) or end (single-prospect mode).

- **Overnight / Auto / Company / Batch modes:** Skip silently. Log the skip to `Claude-Brain/prospects-tracker-new.xlsx` Tab 2 (Company Status) with status `SKIPPED - already enrolled` or `SKIPPED - recent sequence` and the reason in the Notes column. Continue to the next prospect.

This check runs BEFORE HubSpot ownership check, ZoomInfo enrichment, or any research. Fail fast and cheap. Never stack a sequence on top of an active or recently completed one.

---

## Approved Vendor Rule — read list from Claude-Brain file

OSI is an approved vendor at a list of accounts maintained in `Claude-Brain/approved-vendors.json`. Read that file at sequence-build time (OneDrive-safe Python: `open(path,'r')`, fall back to SharePoint MCP on EINVAL) and check if the prospect's company matches any entry (case-insensitive substring match, e.g. "Desjardins Group" matches "Desjardins").

**If the prospect's company matches an approved-vendor entry:**
- **Email 1:** Include ONE line acknowledging approved-vendor status. Soft, peer-to-peer phrasing. Examples:
  - "Side note — we're already on your approved vendor list, so no new vendor onboarding if anything ever needs to move fast."
  - "For context, we're an approved vendor at [Company] already, so standing up a PO is painless if it comes to that."
- **ONE other email — Email 3 or Email 4 — Claude picks whichever fits the narrative:** Brief reminder. One line. Example: "Quick reminder we're already approved at [Company] if timing matters."
- **All other emails:** Do NOT mention approved-vendor status.

**If the prospect's company does NOT match the approved-vendor list:**
- Do NOT mention approved-vendor status anywhere in the sequence. Do not invent it.

**Phrasing rules:**
- Never "vetted" or "pre-approved" — sounds like marketing. "Approved vendor" is the term.
- Never mention "procurement" in Email 1 — telegraphs the sales motion. Just note we're on the list.

To add a company to the approved-vendor list, Andy edits `Claude-Brain/approved-vendors.json` directly and adds the company name to `approved_vendor_companies`.

---

## Step 1: HubSpot Check (silently)

Search HubSpot for the prospect's name and current company. Note the owner. Only create tasks if owned by Andy McLean (196669355), Mark Metz (210187184), or John Houston (210187193).

If contact is owned by another rep, flag it and wait for Andy's instruction before proceeding.

---

## Step 2: Determine contact data available

| Data available | Email tasks | Call tasks | VM + call script in notes |
|---|---|---|---|
| Email + phone | Yes | Yes | Yes |
| Email only | Yes | No | No |
| Phone only | No | Yes | Yes |
| Neither | No | No | No |

**EVERYONE regardless of data:**
- LinkedIn connection request task — always created
- Strategy and Fit note — always saved to HubSpot

---

## Step 3: Produce all outputs in this exact order

---

### 1. Strategy and Fit

**Quick Connect Keywords**
6-10 spoken trigger words to listen for on a call. Only ones relevant to this prospect.

**Previous Employer OSI Client Check**
List previous employers. Note HubSpot matches. State clearly if none found.

**Target Sequences**
List every OSI product line that applies. Choose from: Optics, DWDM, TPM, Compute and Components (lead DIMMs), Storage, Pre-Owned and New Networking, Professional Services (strong signal only).

**The Play**
1-2 sentences. Concrete attack plan based on title, company, background.

**The Personal Hook**
1-2 specific details from their LinkedIn: recent job change, certification, past company, project, or unusual skill. Must appear in Email 1 and LinkedIn invite.

---

### 2. Live Call Script

**Skip entirely if no phone number available.**

Format exactly as below — no paragraphs, no extra text:

KEYWORDS: [5-8 spoken trigger words including technical terms and any news-driven triggers]
HOOK: [Company news or personal trigger in one sentence. If nothing: none — using library opener]
OPENER: [Full opener from OPENER LIBRARY, or custom if HOOK is populated]
VM: [One line. 15 seconds max. One-sentence hook. "I'm sending you something right now, subject line is [Email 1 subject]." Ends with Andy's email: "that's andy at osiglobal dot com." No phone number. Present or future tense only. Never past tense.]

#### OPENER LIBRARY

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

**Already has TPM — merger wedge**
"Hey [Name], how have you been? It's Andy with OSI Global. With the Park Place and Service Express merger, a lot of teams have been taking a fresh look at their TPM relationships. Have you had a chance to renegotiate since the merger, or are you still on the same rates?"

**Systems / Infrastructure engineer — DIMMs**
"Hey [Name], how have you been? It's Andy with OSI Global. We source server memory direct from Samsung and Hynix for infrastructure teams dealing with DDR4 and DDR5 cost pressure. Is that on your radar right now?"

**Storage engineer / admin**
"Hey [Name], how have you been? It's Andy with OSI Global. We do third party maintenance on NetApp and other storage platforms for teams that have gear running fine but coming off OEM support. Is that a conversation you're having?"

**IT Director — compute and infrastructure**
"Hey [Name], how have you been? It's Andy with OSI Global. We work with IT leaders on server memory and third party maintenance, mostly for teams carrying OEM costs on infrastructure that has been running fine for years. Is budget pressure on that something you're dealing with?"

**Procurement — TPM competitive bid**
"Hey [Name], how have you been? It's Andy with OSI Global. We make competitive bids on multi-vendor maintenance contracts. A lot of procurement teams are using us to benchmark their current rates, especially since the Park Place and Service Express merger. Would a competitive bid be worth a look for your next cycle?"

**Transport engineer / Optical network engineer — DWDM**
"Hey [Name], how have you been? It's Andy with OSI Global. We supply open line DWDM systems, 30 to 50% below Ciena and Nokia, with no licensing headaches. A few teams have been using us to fill capacity gaps without going back to the OEM. Is that a conversation worth having for your network?"

**Network architect — metro or long-haul WDM**
"Hey [Name], how have you been? It's Andy with OSI Global. We do open architecture DWDM, SmartOptics platform, significantly less rack space and power than traditional Ciena or Nokia boxes, and ships faster. Is that something that fits anything on your roadmap right now?"

---

### 3. Voicemail Script

**Skip entirely if no phone number available.**

One voicemail. Never two. 15 seconds max. Reference hook. Name Email 1 subject line. End with Andy's email address spelled audibly ("that's andy at osiglobal dot com"). No phone number. Always present or future tense ("I'm sending" or "I'm about to send"). Never past tense.

"Hey [Name], Andy with OSI Global. [One sentence hook]. I'm sending you something right now, subject line is [Email 1 subject]. That's andy at osiglobal dot com."

---

### 4. LinkedIn Invite

Under 300 characters. Low friction. No pitch. Must include Personal Hook. No mutual connections.

---

### 5. The 3-Email Sequence

**Cadence (business days, self-healing — each email anchors to prior email's actual send date):**

| # | Send date | Send window | Type |
|---|---|---|---|
| 1 | Day 1 (next business day) | 4 PM ET (sendTime: "4pm") | Email |
| 2 | 2 business days after Email 1 actual send | 11 AM ET (sendTime: "11am") | Email |
| 3 | 4 business days after Email 2 actual send | 12 PM ET (sendTime: "12pm") | Email |

**Subject line rules:**
- Email 1: You decide. Short, specific, relevant to their world. Never generic or flaggable as spam.
- Email 2: RE: same subject as Email 1.
- Email 3: New subject line. Do not continue the RE: thread. Fresh and specific.

**Email 1 (Day 1, 4 PM ET) — 1st Touch**
Personalized to this specific person. Reference the Personal Hook. Short — 3-4 sentences. One clear ask. No corporate speak.

**Email 2 (2 business days after Email 1 actual send, 11 AM ET) — Sequence Email**
Body: "Any thoughts?"

Then quoted Email 1 below in standard reply format:
> On [Email 1 actual send date], Andy McLean wrote:
> [Full Email 1 text]

No greeting. No sign-off. Just "Any thoughts?" and the quote.

**Email 3 (4 business days after Email 2 actual send, 12 PM ET) — Sequence Email**
New subject line. Different angle from Email 1. Introduce a relevant pain point or OSI product line not covered yet. Short — 3-4 sentences. One ask.

Quote Email 2 below in standard reply format.

**Send-window assignments for the email-queue.json entries:**
- Email 1: `sendTime: "4pm"`
- Email 2: `sendTime: "11am"`
- Email 3: `sendTime: "12pm"`

The master osi-email-sender task runs every weekday at 11 AM, 12 PM, 1 PM, 2 PM, 3 PM, and 4 PM Eastern. Each fire window processes queue entries whose `sendTime` matches that window. The 3-email sequence uses the same window architecture as the 6-email sequence.

---

## DWDM / SmartOptics talking points

- Cost: 30-50% below Ciena and Nokia. Minimal licensing fees.
- Space and power: Significant reduction vs. traditional DWDM platforms.
- Simplicity: Easier to deploy and manage.
- Lead times: Ships faster than OEMs.
- Pedigree: Backed by original engineering core. Not grey market.

---

## OSI Product Lines

1. **Optics** — SmartOptics transceivers. Sample offer is the opening wedge.
2. **DWDM and Open Line Systems** — SmartOptics DCP, 30-50% below Ciena/Nokia.
3. **Compute and Components** — DIMMs from Samsung/Hynix/Micron. Lead with DIMMs.
4. **Storage** — NetApp TPM, pre-owned storage.
5. **TPM** — 40-60% below OEM. Multi-vendor. Gartner-recognized, privately owned, no PE.
6. **Pre-Owned and New Networking** — Pre-owned Cisco/Juniper/Arista. New Nokia authorized.
7. **Professional Services** — Strong signal only. Never lead cold.

---

## VERTICAL INTELLIGENCE

### Telco and Service Providers
Lead with optics. Do NOT open with free SFPs. TPM rarely the opener at engineer level.

### Large Banks and Financial Institutions
Lead with optics. Free SFP offer works. Do NOT lead with TPM. If known TPM, use Park Place/Service Express merger wedge.

### Professional Services and Consulting
TPM viable opener. Lead with pain not price. Free optics also works.

### Manufacturing
Free optics as break-glass insurance. TPM for aging Cisco gear.

### Healthcare
TPM with documented SLAs. DIMMs for server refresh. Gartner-recognized, privately owned, no PE matters here.

---

## COLD CALL OPENER RULES (Gong, 300M+ calls)

1. Open with "How have you been?" — 6.6x baseline meeting rate.
2. State a clear reason for calling.
3. End with a question about their world. Never "Is now a good time?"
4. Never ask "Is now a good time?"
5. Skip "Have you heard our name tossed around?"
6. Tone over words. Warm, confident, peer-to-peer.
7. Voicemails: 15 seconds max. No phone number. End with Andy's email address spelled audibly ("that's andy at osiglobal dot com"). Always present or future tense ("I'm sending" or "I'm about to send"). Never past tense.

---

## TPM POSITIONING RULES

**Unknown if they have TPM:**
- Banks: optics opener, TPM is second conversation
- Consulting: TPM can open, lead with pain not savings %
- Manufacturing/enterprise: TPM strong, aging gear and OEM end-of-life is the hook

**Known TPM provider:**
Merger wedge: "With the Park Place and Service Express merger, a lot of teams have been taking a fresh look at their TPM relationships. Have you had a chance to renegotiate since the merger, or are you still on the same rates?"

---

## Step 6: Save to HubSpot automatically

### Task housekeeping — always do this first

When a prospect is being processed and they have an existing `LINKED_IN_CONNECT` task in HubSpot (the "Sales Nav -- Send connection request" task that triggered this sequence):

1. **Mark the existing task COMPLETED.** Set `hs_task_status` = `COMPLETED` on that task via `manage_crm_objects` updateRequest. This removes it from Andy's open task queue.

2. **Create a NEW `LINKED_IN_CONNECT` task** scheduled for Day 1 (the date Email 1 fires). Use the standard subject format: `Sales Nav -- Send connection request -- [First Last] | [Company]`. Owner: 196669355. Notes: the LinkedIn invite text. This surfaces the connection request on Andy's task queue the morning of Day 1 so he can send the LinkedIn invite the same day Email 1 fires.

Do this for EVERY prospect regardless of whether they had an existing task or not (if no existing task, just create the new one).

---


### Create or update contact record

### Data quality — HARD REQUIREMENTS (do not skip)

Every contact written to HubSpot MUST have these fields populated correctly. If any are missing or wrong, STOP — do not write the record. Research harder, then retry.

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
- US and Canada numbers: `+1 (XXX) XXX-XXXX` — with the space after `+1`, parentheses around area code, space before first block, hyphen before last 4.
- Example: `+1 (440) 567-7444`
- If existing HubSpot data has `(416) 353-7591` without country code, UPGRADE it to `+1 (416) 353-7591` when you write.
- Non-US/CA: use `+[country code] [number]` appropriate to the region.

**Mobile phone rule — never violate:**
- `mobilephone` holds the person's DIRECT mobile/cell ONLY.
- NEVER put a company main/switchboard number in `mobilephone`.
- If ZoomInfo returns no mobile, leave `mobilephone` BLANK. Do not substitute.

**Pre-write checklist — run BEFORE every contact save:**
1. jobtitle is current (pulled from LinkedIn top card, not HubSpot)
2. phone formatted `+1 (XXX) XXX-XXXX` (if US/CA)
3. mobilephone formatted OR blank (not HQ number)
4. hs_timezone set (one of the 6 buckets)
5. hs_linkedin_url set (full URL)
6. Associated company record exists and is linked

If any check fails, FIX IT or leave the field blank. Do NOT write a partial record.

---


### LinkedIn & association rules — apply on every contact save

**Job title — always refresh from LinkedIn (authoritative).**
Even if HubSpot already has a `jobtitle` value, pull the current title from the prospect's LinkedIn profile top card and overwrite. HubSpot titles go stale; LinkedIn is source of truth. Fallback order if LinkedIn is unreachable (closed profile, URL broken, private): use the ZoomInfo enriched `jobTitle` field. Only if neither is available, leave the existing HubSpot value alone.

**Associated company — always link on contact creation.**
Before creating or updating a contact, search HubSpot for the company by name (`search_crm_objects` objectType=COMPANY, `query` = company name). If found, associate the contact to that company record via the `associations` parameter in `manage_crm_objects.createRequest` or `updateRequest`. If the company is not found in HubSpot, create a new company record first (owner: 196669355, name: company name from LinkedIn) and then associate the contact to it.

Never leave a contact orphaned from its company. Unlinked contacts break same-company stagger logic, deal tracking, and reporting.


Required fields: first name, last name, job title, company, email (if found), phone (if found), city, state, timezone (hs_timezone), LinkedIn URL (hs_linkedin_url — regular linkedin.com/in/ URL).

Timezone values (6-bucket): us_slash_eastern / us_slash_central / us_slash_mountain / us_slash_pacific / us_slash_alaska (US Alaska) / canada_slash_atlantic (Canada Atlantic). Outside these six, use the closest matching bucket.

### Strategy and Fit note — EVERYONE

objectType: "notes", owner 196669355, associated to contact.

Note format (exact structure):

QUICK CONNECT KEYWORDS
[6-10 keywords, one line]

LIVE CALL SCRIPT (omit entire section if no phone number)
OPENER: [full opener from library]
VM: [one line, 15 seconds max. One-sentence hook. "I'm sending you something right now, subject line is [Email 1 subject]." Ends with Andy's email: "that's andy at osiglobal dot com." No phone number. Present or future tense only. Never past tense.]

THE PLAY
[One tight paragraph: why they qualify + the hook + the attack plan. Only include Previous Employer OSI Client Check if a HubSpot match is found. Skip it entirely if no matches.]

--- EMAIL SEQUENCE ---
Email 1 - Day 1 - [Date] - Subject: [subject]
[full email body]

Email 2 - Day 3 - [Date] - Subject: RE: [subject]
Any thoughts?
---------- On [Date], Andy McLean wrote ----------
[Email 1 quoted]

Email 3 - Day 7 - [Date] - Subject: [new subject]
[full email body + thread]

Never use em-dashes anywhere in the note.

### LinkedIn Connection Request task — EVERYONE

Subject: "Sales Nav -- Send connection request -- [First Last] | [Company]"
Type: LINKED_IN_CONNECT, due Day 1 (same date as Email 1 / 1st Touch), owner 196669355.
Notes: LinkedIn invite text.
Check for existing task first. If exists, skip.

### If no email AND no phone — LinkedIn tasks only

Task 1: LINKED_IN_MESSAGE, "1st LI — [First Last] | [Company]", due 7 days.
Task 2: LINKED_IN_MESSAGE, "2nd LI — [First Last] | [Company]", due 21 days.
Check for existing tasks first. If exist, skip.
