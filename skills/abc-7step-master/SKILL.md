---
name: abc-7step-master
description: "MASTER 7-email OSI Global outreach sequence. Standalone end-to-end: research, HubSpot contact, full Orum call script package (12-opener library, bridge, discovery, objections, voicemail) on the contact note, LinkedIn task synced to Day 1, and 7 emails written to email-queue.json. Master osi-email-sender sweeps the queue at 11am/12pm/1pm/2pm/3pm/4pm PT windows. Self-healing cadence anchored to actual send dates, holiday avoidance, weekend-skip, same-company stagger, dedup. Every send BCCs bc@osihardware.com + 21878985@bcc.hubspot.com for inbox confirmation and HubSpot timeline logging. Replaces bc-7step-w-tracking and bc-osi-outreach-sequence-v2 for new prospect work. ALWAYS use when Brian says 'master sequence', 'run the master', 'abc-7step-master', '7step master', 'build the master on', or pastes a LinkedIn profile, HubSpot contact record, or name + company and wants the full package built and queued."
---

# abc-7step-master — OSI Global Master Outreach Sequence

The master pipeline. One skill, end-to-end: research → qualify → HubSpot contact + call script note + LinkedIn task → 7 emails written, humanized, queued → cadence self-heals as it runs.

**Architectural shifts vs. the prior skills:**
- **JSON queue, not individual scheduled tasks.** All 7 emails write to `email-queue.json`. The master `osi-email-sender` task (already running on a recurring schedule at 11am, 12pm, 1pm, 2pm, 3pm, 4pm Pacific weekdays) sweeps pending entries each window. Machine off at 1pm? The entry sits as `pending` and the next window picks it up. Retry-safe.
- **Self-healing cadence.** Each email's `sendDate` is recalculated relative to the PRIOR email's actual send date when the sender fires it. If Email 2 slips a day, Email 3's gap stays intact instead of compressing.
- **Same-company stagger.** Before assigning Day 1, the skill scans the queue for other pending/sent entries at the same domain and spaces this prospect 4 business days behind the last Day 1 at that company (10 bd for person 6, then back to 4 bd from person 7 forward).
- **Dedup protection.** Active sequence check by `to` email and by `prospectName + company`. Never stack a sequence on an active or recently completed one.
- **Holiday avoidance** plus weekend-skip on every computed date.
- **PT windows** (changed from ET). The master sender runs 11am/12pm/1pm/2pm/3pm/4pm Pacific.
- **Full call script package on the HubSpot contact note** so Orum surfaces it on every dial — opener from the 12-opener library, vertical bridge, tailored discovery questions, objection handling, voicemail, KEYWORDS line.

**Tracking BCCs on every send (Email 1 through Email 7):**
- `bc@osihardware.com` — copy lands in Brian's Outlook inbox so he can confirm sends fired
- `21878985@bcc.hubspot.com` — auto-logs to HubSpot contact timeline

If either address changes, update them in Step 9 (Email 1 live send) AND the queue entry `bcc` field used by the master sender.

---

## Signature Block — Use This Every Time

Outlook auto-signature is inconsistent. Every send (live Email 1 plus everything the master sender fires from the queue) explicitly clears whatever Outlook auto-inserts and types this block instead:

```
Brian Charrette
Director of Key Accounts
Desk: 805.845.5167 | Cell: 805.682.9358
Systems: HPE / Dell / Cisco UCS / Supermicro / APC
Network: Cisco / Aruba / Juniper / Fortinet / APC / Opengear
Optical: Transceivers / DAC / AOC / Cables / DWDM Line Systems
Service: Systain Third Party Maintenance / Professional Services
```

If this ever changes, update it here and propagate to any queue entries already written.

---

## Step 1 — Gather Prospect Info

Ask Brian for or extract from what he pasted:
- Full name
- Title
- Company and domain
- Email address (required — see Step 2a)
- LinkedIn URL if available
- Any context he has (pain points, source, notes)

If Brian pasted a HubSpot contact record or a LinkedIn profile, parse fields directly.

### Step 1a — STOP IF NO EMAIL

This skill drafts and queues 7 emails. No email means no sequence. If neither Brian's input nor a quick ZoomInfo lookup returns a valid email, STOP. Tell Brian and suggest the LinkedIn-only fallback (LINKED_IN_CONNECT task + a second LI message task two weeks later).

### Step 1b — Active Sequence Check (hard stop before any work)

Before researching, writing emails, or touching HubSpot, open the queue:

`C:\Users\Mini\Documents\osi-claude-brain\automation\email-queue.json`

Use the OneDrive-safe pattern: try local `open(path, 'r')` first; on EINVAL fall back to the SharePoint MCP (`mcp__3d844455-*__sharepoint_search` for `email-queue.json`, then `read_resource`).

Scan every entry for a match with this prospect:
- `to` field equals the prospect's email (case-insensitive), OR
- `prospectName` + `company` both match (case-insensitive)

**SKIP if any matched entry has:**
- `status: "pending"` (active sequence), OR
- `status: "sent"` with a `sendDate` in the last 30 calendar days

Entries with status `paused-*`, `canceled-*`, or older `sent` (>30 days) do not block — proceed but note in the call script that this is effectively a re-engagement.

Tell Brian: `SKIPPED: [Name] at [Company] — [reason]. Override?` Wait for explicit "override" to proceed. Without it, stop.

---

## Step 2 — Research the Prospect

Web search the company and the role. Pull what they do, scale, public tech stack, any 30-day news. Decide which OSI pillar leads:

- **Network / telecom / colocation / carrier** → optics + DWDM + supply chain reliability; TPM second
- **Bank / financial institution** → optics, free SFP wedge; never lead TPM (regulated environments often locked to OEM support)
- **Software / cloud / SaaS** → optics, high-density connectivity, lead time
- **Enterprise IT / manufacturing / consulting** → TPM cost savings + EOL coverage
- **Procurement / IT Director / VP** → OpEx reclamation, vendor simplification, competitive TPM bid

Capture 1-2 specific concrete details to weave into Email 1 — recent news, a post they engaged with, a known infrastructure pattern at their company size. Name this the **Personal Hook**. It anchors Email 1, the call script, the voicemail, and the LinkedIn invite.

Also run ONE targeted web search for company news in the last 30 days. ZoomInfo scoops lag by weeks. Capture acquisitions, exec hires, earnings, product launches, buildout announcements, partnerships as the **Fresh Hook**. If nothing surfaces in 30 days, fall back to the Personal Hook alone.

---

## Step 3 — HubSpot Contact + Approved Vendor Check

### Contact lookup / create

Search HubSpot for the contact by email. If found, capture the contact ID, refresh `jobtitle` from LinkedIn (LinkedIn is authoritative — HubSpot titles go stale), reassign `hubspot_owner_id` to `213536174` (Brian) if needed. If not found, create the contact with hard-required fields:

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

### Approved vendor check

Read `OSI-Brain/approved-vendors.json` (OneDrive-safe pattern). Case-insensitive substring match on the prospect's company against `approved_vendor_companies`.

**If match:**
- Email 1 includes ONE soft line acknowledging approved-vendor status. Examples: "Side note — we're already on your approved vendor list, so no new vendor onboarding if anything ever needs to move fast." Or: "For context, we're an approved vendor at [Company] already, so standing up a PO is painless if it comes to that."
- ONE other email (Email 3 or 4 — pick whichever fits the narrative) gets a brief one-line reminder: "Quick reminder we're already approved at [Company] if timing matters."
- No other email mentions it. Never say "vetted" or "pre-approved" — those read as marketing. "Approved vendor" is the term. Never mention "procurement" in Email 1.

**If no match:** never invent it. No mention anywhere.

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

This drives Email 1's lead, the call script's OPENER selection, and the voicemail angle.

---

## Step 5 — Calculate the 7-Email Schedule

### 5a. Same-company stagger (before setting Day 1)

Scan the queue for entries at this company (status `pending` or `sent`). Count how many people at this company are already enrolled.

- Persons 1-5 at the same company: Day 1 = **4 business days** after the most recent Day 1 at that company (or next business day if you're the first).
- Person 6: Day 1 = **10 business days** after person 5's Day 1. One-time cooling gap to let the receiving domain's rolling-velocity window reset.
- Persons 7+: back to **4 business days** after the most recent Day 1.

### 5b. Base cadence (gaps from prior email's planned send)

| # | Day | Gap from prior | Type | Send window |
|---|---|---|---|---|
| 1 | Day 1 (next business day per 5a) | — | Cold intro | 4pm PT |
| 2 | Day 1 + 4 bd | +4 bd | Different angle | 11am PT |
| 3 | Email 2 + 6 bd | +6 bd | Soft touch | 12pm PT |
| 4 | Email 3 + 2 bd | +2 bd | Swag/SFP address confirm | 1pm PT |
| 5 | Email 4 + 2 bd | +2 bd | "Any thoughts?" reply | 2pm PT |
| 6 | Email 5 + 4 bd | +4 bd | Pattern interrupt | 3pm PT |
| 7 | Email 6 + 10 bd | +10 bd | Breakup | 4pm PT |

Total length: ~28 business days from Day 1 to Email 7 if nothing slips.

### 5c. Weekend + holiday skip — applied to every date

No email is ever allowed on Saturday, Sunday, or a US federal/B2B-observed holiday.

**Holidays — never send:**

US federal (observed nearest weekday): New Year's Day, MLK Day (3rd Mon Jan), Presidents Day (3rd Mon Feb), Memorial Day (last Mon May), Juneteenth (Jun 19), Independence Day (Jul 4), Labor Day (1st Mon Sep), Columbus Day (2nd Mon Oct), Veterans Day (Nov 11), Thanksgiving (4th Thu Nov), Christmas (Dec 25).

Also skip: Good Friday, Black Friday (day after Thanksgiving), Christmas Eve (Dec 24), New Year's Eve (Dec 31).

**2026 hardcoded:** Jan 1 Thu, Jan 19 Mon, Feb 16 Mon, **Apr 3 Fri (Good Friday)**, **May 25 Mon**, **Jun 19 Fri**, **Jul 3 Fri**, **Sep 7 Mon**, Oct 12 Mon, Nov 11 Wed, **Nov 26 Thu**, **Nov 27 Fri**, **Dec 24 Thu**, **Dec 25 Fri**, **Dec 31 Thu**

**2027 hardcoded:** **Jan 1 Fri**, Jan 18 Mon, Feb 15 Mon, **Mar 26 Fri**, **May 31 Mon**, **Jun 18 Fri**, **Jul 5 Mon**, **Sep 6 Mon**, Oct 11 Mon, Nov 11 Thu, **Nov 25 Thu**, **Nov 26 Fri**, **Dec 24 Fri**, **Dec 31 Fri**

If a computed date lands on a weekend or holiday, push to the next business day. Recompute subsequent emails from the shifted anchor (self-healing rule below already handles this when the sender fires).

### 5d. Self-healing cadence (the key v2 mechanic)

At creation time, write all 7 entries to the queue with provisional `sendDate` values from 5b applied through 5c. But when the master sender fires Email N, it must update Email N+1's `sendDate` to `[gap from table 5b] business days after today's actual fire date`, skipping weekends/holidays.

That means: if Email 2 fires a day late because the 11am PT window was missed and got picked up at 12pm next day, Email 3's `sendDate` shifts forward a day automatically. The gap from the table stays intact instead of compressing. The queue is the living schedule, not a frozen plan.

This is the responsibility of the master `osi-email-sender` task, not this skill. This skill writes the provisional dates and trusts the sender to recompute as it goes. As a hard backstop, the sender also enforces a one-email-per-person-per-day rule: if any entry for a given `to` address already has `status: "sent"` and `sendDate` matching today, all other pending entries for that address are skipped until tomorrow. This means a sequence that is weeks behind will catch up at most one email per person per day -- never three in a row.

### 5e. Print the schedule for review

Before going further, print the proposed schedule as a table with both the raw cadence day AND the final weekday-+holiday-shifted date AND the send window. Brian should be able to visually confirm zero dates fall on Sat/Sun/holiday before he says "run."

---

## Step 6 — Write All 7 Emails

Write every email before doing anything else. Brian's voice: direct, no-nonsense, outcomes over transactions, zero corporate fluff. Short. Mobile-friendly. Scannable in 10 seconds.

### Email 1 — Cold Intro (Day 1)
- 3-4 short paragraphs, most under 100 words
- Open with what problem you solve for people in their role
- Reference the Personal Hook or Fresh Hook (something specific from research)
- If approved vendor: include the soft one-line note (see Step 3)
- One clear ask: 15-minute call
- End body with just `Brian` on its own line — the queue entry's send pipeline clears Outlook's auto-sig and appends the canonical signature block automatically

### Email 2 — Different Angle (Email 1 + 4 bd)
- Pivot to a DIFFERENT OSI pillar than Email 1 (optics if Email 1 was TPM, or vice versa)
- Do not repeat what was in Email 1
- 2-3 short paragraphs
- No hard ask — soft "worth a conversation if..."
- End with `Brian`

### Email 3 — Soft Touch (Email 2 + 6 bd)
- Acknowledge the silence without being apologetic
- Reference a pattern you see at companies like theirs (no namedropping)
- Offer an easy out: "if timing is off, just say the word"
- 2-3 short paragraphs
- If approved vendor and you didn't use the reminder in Email 4, use it here
- End with `Brian`

### Email 4 — Swag & Sample SFPs / Address Confirm (Email 3 + 2 bd)

**Subject is ALWAYS** (no personalization, no variation): `Re: Confirming address`

The "Re:" makes it look like a follow-up in their inbox. This is not a literal reply — it's a new email with a manufactured subject.

**Body is ALWAYS the same** (no personalization):

> I'm just prepping this package for you. I have a box of swag and a pair of sample SFPs to send to you from the team here at OSI Global IT.
>
> Do you come into the office? Is that the best address to send it to right now?

End with `Brian`. This email works because it creates a reason to reply that has nothing to do with a sales pitch. If they reply with an address, Brian pauses the remaining queue entries manually (set status to `paused-shipping` in the queue) and ships.

### Email 5 — "Any thoughts?" (Email 4 + 2 bd)

ALWAYS the same. This is a REPLY in the original Email 1 thread, not a new email.

- Subject: inherits from the reply (the master sender will detect this entry's `replyMode: true` flag and reply to the oldest sent email to this address)
- Body: `Any thoughts?` — two words only. No greeting, no signature, no additional text.

### Email 6 — Pattern Interrupt (Email 5 + 4 bd)
- Single direct yes/no question about their specific environment
- Pick the most relevant from research: EOL gear, contract renewals, optics gaps, DWDM capacity, TPM rate review
- 2-3 sentences only
- "If yes, worth talking. If no, I'll stop bothering you."
- End with `Brian`

### Email 7 — Breakup (Email 6 + 10 bd)
- Short, respectful, leaves the door open
- Acknowledge you've sent several notes, respect their time
- No pitch
- Examples: "Should I close the file on this one, or is the timing just off?" or "No worries if now isn't the right time. Happy to circle back when things shift."
- End with `Brian`

---

## Step 7 — Humanize Every Email

Run every email through this filter before queueing. Anything that fails gets rewritten:

- **No AI vocabulary:** remove "crucial," "pivotal," "landscape," "underscore," "delve," "showcase," "testament," "enhance," "foster," "garner"
- **No hyphens** in bodies or subject lines. Rewrite "end-of-life" → "end of life", "24-hour" → "24/7/365", "third-party" → "third party"
- **No em dashes (—)** anywhere. Split into two sentences if needed.
- **No rule of three.** Break triple-item lists into natural prose.
- **No -ing pile-up** at sentence tails. Kill trailing "highlighting our advantage," "ensuring uptime," "reflecting market shifts."
- **No negative parallelisms.** Remove "it's not just X, it's Y."
- **Vary sentence length.** Mix short punchy sentences with longer ones.
- **Use is/are/has** instead of "serves as," "stands as," "functions as."
- **Final read-aloud check.** Mentally read each email aloud. If it sounds like a press release, rewrite.

The why: prospects can smell AI from a mile away in 2026. Brian's edge over every other rep flooding inboxes with GPT-output is that his emails sound like a person. Lose that and the whole sequence collapses.

---

## Step 8 — Subject Lines

For each email EXCEPT Email 4 (fixed: `Re: Confirming address`) and Email 5 (reply, inherits original subject):
- Write 5 subject line options
- Mix: 2-3 professional/catchy + 2 outlandish/unexpected
- No hyphens in subject lines
- Randomly select one of the 5 for the queue entry
- Present all 5 to Brian with the selected one clearly marked

---

## Step 9 — Generate the Full Call Script Package + HubSpot Note + LinkedIn Task

Do this automatically before presenting to Brian. No input needed.

### 9a. Voicemail Script

15 seconds max. One-sentence hook drawn from the Personal Hook. Say you are sending or about to send the email, name the Email 1 subject line, end with Brian's email spelled audibly ("that's bc at osihardware dot com"). No phone number. Present or future tense only ("I'm sending" / "I'm about to send"). Never past.

Apply Step 7 humanization. Read it aloud — if it sounds like a recording, rewrite.

### 9b. Live Call Script (Orum surface)

This is what Orum displays when Brian dials. Build it in memory with every bracket fully substituted. Verify no `[Name]`, `[Title]`, `[Company]`, `[Vertical]`, `[Insert]`, or `[Paste...]` tokens remain before sending to HubSpot.

**Structure — use this exact format as `hs_note_body`:**

```
CALL SCRIPT — [Full Name] @ [Company]
[Title] | [Vertical]
OSI Angle: [Primary angle from Step 4]
KEYWORDS: [5-8 spoken trigger words to listen for]
HOOK: [Fresh Hook one-liner with source URL, or Personal Hook one-liner, or "none — using library opener"]
---

VOICEMAIL (~15 sec — use if no answer):
"[Full voicemail script from 9a, fully written out]"


OPENER (from 12-opener library — select by role/vertical):
"[Full opener verbatim from the OPENER LIBRARY below — substitute [Name]]"


BRIDGE (one sentence, tied to their role/vertical pain):
"[One sentence reason for calling tied to their specific role and vertical, anchored to the Personal Hook]"


DISCOVERY (pick best 2 based on OSI angle):
Q1: [Tailored discovery question for this role and OSI angle]
Q2: [Tailored discovery question for this role and OSI angle]


OBJECTION HANDLING:
- "Send me info" → "Happy to — what's the most relevant piece for where you are right now? I'd rather send you one useful thing than a brochure."
- "We have a vendor" → "Totally — I'm not asking to replace anyone today. Most of our best relationships started as a second opinion on one project. Is there one area where you'd want that?"
- "Not interested" → "Fair enough. Quick question before I let you go — is it timing, or just not in the roadmap at all? I'd rather not bug you if it's the latter."
- "We're under contract" → "Got it — when does that renew? I'd rather be in your ear three months before than three days after."
- "We use OEMs" → "That's most of our customers before they switch. What does your renewal cycle look like?"


CLOSE:
"I'm not trying to do a full pitch on a cold call — but would it make sense to find 20 minutes to compare notes? Worst case you get a second opinion, best case we find something worth looking at."


Brian's direct: 805.682.9358
Best callback: mornings PT
---
```

#### OPENER LIBRARY — 12 openers, pick the one that fits

**Telco / Service Provider network engineer**
> "Hey [Name], how have you been? It's Brian with OSI Global. We supply ZR and ZR+ coherent optics to carrier teams as a secondary source when Cisco or Lumentum timelines slip. Is that something your team is running into right now?"

**Bank / Financial Institution network engineer**
> "Hey [Name], how have you been? It's Brian with OSI Global. We supply certified compatible optics to bank IT teams, mostly for the break-glass scenario where something fails and you can't wait two weeks for OEM. I was going to send a few complimentary SFPs your way. Would that be useful?"

**Enterprise IT / Consulting network engineer**
> "Hey [Name], how have you been? It's Brian with OSI Global. We work with enterprise IT teams on third party maintenance, specifically replacing OEM support on Cisco gear that is running fine but coming off warranty. Is that a conversation your team is having right now?"

**Manufacturing network engineer**
> "Hey [Name], how have you been? It's Brian with OSI Global. We supply certified compatible optics and networking spares to manufacturing IT teams for the break-glass scenario. I was going to send a few complimentary SFPs so you've got a Plan B on the shelf. Worth it?"

**Director or VP, any vertical**
> "Hey [Name], how have you been? It's Brian with OSI Global. We work with infrastructure leaders on two things mostly: third party maintenance and optical hardware where OEM timelines or costs have become a problem. Is either of those a live conversation for your team?"

**Already has TPM — merger wedge**
> "Hey [Name], how have you been? It's Brian with OSI Global. With the Park Place and Service Express merger, a lot of teams have been taking a fresh look at their TPM relationships. Have you had a chance to renegotiate since the merger, or are you still on the same rates?"

**Systems / Infrastructure engineer — DIMMs**
> "Hey [Name], how have you been? It's Brian with OSI Global. We source server memory direct from Samsung and Hynix for infrastructure teams dealing with DDR4 and DDR5 cost pressure. Is that on your radar right now?"

**Storage engineer / admin**
> "Hey [Name], how have you been? It's Brian with OSI Global. We do third party maintenance on NetApp and other storage platforms for teams that have gear running fine but coming off OEM support. Is that a conversation you're having?"

**IT Director — compute and infrastructure**
> "Hey [Name], how have you been? It's Brian with OSI Global. We work with IT leaders on server memory and third party maintenance, mostly for teams carrying OEM costs on infrastructure that has been running fine for years. Is budget pressure on that something you're dealing with?"

**Procurement — TPM competitive bid**
> "Hey [Name], how have you been? It's Brian with OSI Global. We make competitive bids on multi-vendor maintenance contracts. A lot of procurement teams are using us to benchmark their current rates, especially since the Park Place and Service Express merger. Would a competitive bid be worth a look for your next cycle?"

**Transport engineer / Optical network engineer — DWDM**
> "Hey [Name], how have you been? It's Brian with OSI Global. We supply open line DWDM systems, 30 to 50% below Ciena and Nokia, with no licensing headaches. A few teams have been using us to fill capacity gaps without going back to the OEM. Is that a conversation worth having for your network?"

**Network architect — metro or long-haul WDM**
> "Hey [Name], how have you been? It's Brian with OSI Global. We do open architecture DWDM, SmartOptics platform, significantly less rack space and power than traditional Ciena or Nokia boxes, and ships faster. Is that something that fits anything on your roadmap right now?"

### 9c. LinkedIn Connection Request

Under 300 characters (LinkedIn hard limit). Personalized: reference role, vertical pain, or the Personal Hook. No pitch. No product names. No "I'd love to tell you about OSI." One sentence + one short reason to connect.

### 9d. Write the HubSpot Note + LINKED_IN_CONNECT Task

Using `mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__manage_crm_objects`:

**Note (object type `notes`):**
- `hs_note_body` = the fully-substituted call script package from 9b. Must be >=500 chars and contain the prospect's actual name. NO bracket tokens.
- `hs_timestamp` = current epoch ms
- `hubspot_owner_id` = `213536174`
- Associate to the contact via `associations` with `associationTypeId: 202`

**Task (object type `tasks`):**
- `hs_task_type` = `LINKED_IN_CONNECT`
- `hs_task_subject` = `Send LinkedIn Request — [First Last] | [Company]`
- `hs_task_body` = the literal LinkedIn message draft from 9c (not a description)
- `hs_task_status` = `NOT_STARTED`
- `hs_timestamp` = Email 1's Day 1 date in epoch ms (synchronizes LinkedIn invite with Email 1's send day)
- `hs_task_priority` = `HIGH`
- `hubspot_owner_id` = `213536174`
- Associate to the contact

**Verify after creating the task:** fetch it back, read `hs_task_body`, confirm it's a real message addressed to the prospect. If it's a placeholder or description, immediately update with the correct draft.

Confirm in chat: `HubSpot note added (call script + voicemail). LinkedIn task created, due [Day 1 date].`

---

## Step 10 — Present for Review — Wait for "Run"

After Steps 1-9 complete, present everything to Brian in one block:
1. Prospect summary (name, title, company, OSI angle, sequence type, approved vendor Y/N)
2. The schedule table from Step 5e — all 7 emails, send dates, send windows (Pacific), zero weekends/holidays
3. All 5 subject line options per email (Emails 1, 2, 3, 6, 7) with the selected one marked. Email 4 fixed. Email 5 is a reply.
4. Full body of every email
5. Voicemail script
6. Live call script package (full 9b structure)
7. LinkedIn invite text (character count under 300)

**Stop. Do not write to the queue. Do not send. Wait.**

End with: `Look it over and say **run** when you're ready.`

---

## Step 11 — On "Run" — Send Email 1 Live, Queue the Rest

When Brian says "run" (or any clear go-ahead: "send it", "looks good", "do it"):

### 11a. Pre-flight: Outlook session must be live

Open Chrome and navigate to `https://outlook.office.com`. If a sign-in screen appears, STOP and tell Brian: `Chrome Outlook session is expired — sign in before I run this sequence.` Do not proceed until the session is live. This prevents the silent-failure mode where browser automation fires but nothing actually sends.

### 11b. Send Email 1 right now via Chrome

1. In the open Outlook tab, click **New mail**
2. In the **To** field, type the prospect's email and press Tab
3. Click **Bcc** to reveal the BCC field, then type exactly: `bc@osihardware.com, 21878985@bcc.hubspot.com` and press Tab. Confirm both pills appear before continuing.
4. Click the **Subject** field and type the selected Email 1 subject exactly
5. Click in the body area. Press Ctrl+A then Delete to clear any Outlook auto-signature.
6. Type the Email 1 body exactly as written. Press Enter twice. Type the canonical signature block from the top of this skill.
7. Click **Send**
8. Confirm the email appears in Sent Items within 2 minutes. If not, report failure and stop.

### 11c. Update LINKED_IN_CONNECT task `hs_timestamp`

Email 1 just fired live, so Day 1 is locked in as TODAY. If 9d wrote the task with Email 1's planned Day 1, that's already correct. If for any reason Day 1 shifted (Brian ran on a different day than planned), call `manage_crm_objects` updateRequest on the task and set `hs_timestamp` to today.

### 11d. Write Emails 2-7 to the queue

Open `C:\Users\Mini\Documents\osi-claude-brain\automation\email-queue.json` using the OneDrive-safe Python pattern (try local `open(path, 'r')`, fall back to SharePoint MCP on EINVAL — see Queue Write Pattern below).

Build 6 new entries (Emails 2 through 7). Each entry:

```json
{
  "id": "[firstname]-[lastname]-[company-slug]-[N]",
  "prospectName": "First Last",
  "company": "Company Name",
  "to": "prospect@company.com",
  "bcc": "bc@osihardware.com, 21878985@bcc.hubspot.com",
  "subject": "[selected subject line, or 'Re: Confirming address' for #4, or empty for #5]",
  "body": "[full email body, no signature — sender appends the canonical block]",
  "sendDate": "YYYY-MM-DD",
  "sendTime": "11am | 12pm | 1pm | 2pm | 3pm | 4pm",
  "sendTimeZone": "PT",
  "replyMode": false,
  "status": "pending",
  "addedDate": "YYYY-MM-DD (today)",
  "sequenceId": "[firstname]-[lastname]-[company-slug]",
  "emailNumber": 2,
  "cadenceGap": 4,
  "priorEmailId": "[firstname]-[lastname]-[company-slug]-1"
}
```

**Special fields:**
- Email 4: `subject: "Re: Confirming address"`, `replyMode: false`, fixed body from Step 6 Email 4.
- Email 5: `replyMode: true`, `subject: ""` (sender will reply to the oldest Sent Item to this address), `body: "Any thoughts?"`, no signature appended.
- `cadenceGap` is the business-day gap from the prior email (4, 6, 2, 2, 4, 10). The sender uses this to recompute Email N+1's `sendDate` when it fires Email N (self-healing).
- `priorEmailId` lets the sender find the anchor email when recomputing.

**Dedup before append:** scan the existing queue for entries with the same `id`. If any match, do not append duplicates. This prevents accidental double-enrollment if the skill is re-run on the same prospect.

### Queue Write Pattern (OneDrive-safe, no permission prompts)

```python
import json, os

QUEUE = r'C:\Users\Mini\Documents\osi-claude-brain\automation\email-queue.json'

# Read existing
try:
    with open(QUEUE, 'r') as f:
        queue = json.load(f)
except (OSError, ValueError):
    # Cloud-only file — fall back to SharePoint MCP fetch, parse JSON string into `queue`
    raise SystemExit("FALLBACK: use SharePoint MCP to fetch current queue, then continue")

new_entries = [ ... ]  # 6 entry dicts for Emails 2-7

# Dedup by id
existing_ids = {e.get("id") for e in queue}
to_add = [e for e in new_entries if e["id"] not in existing_ids]
queue.extend(to_add)

# Atomic write
tmp = QUEUE + '.tmp'
with open(tmp, 'w') as f:
    json.dump(queue, f, indent=2)
os.replace(tmp, QUEUE)
```

Do NOT use the MCP Write tool — its prior-Read requirement breaks on cloud-only files. Do NOT delete the file first — cowork delete permission doesn't reliably carry across scheduled sessions.

### 11e. Confirm

Confirm in chat:
- `Email 1 sent to [prospect@email] at [HH:MM PT] with BCC tracking.`
- `6 emails queued (Emails 2-7), Day 1 + 4 / +6 / +2 / +2 / +4 / +10 bd cadence.`
- `Master osi-email-sender picks up at the next PT window matching each entry's sendTime.`
- `LinkedIn task synced to Day 1 (today): [date].`
- `Call script + voicemail live on HubSpot contact — Orum will surface on next dial.`

---

## Step 12 — Save Markdown Reference File

Use the Write tool to save `[lastname]-[company]-sequence.md` to Brian's Email folder. Include the schedule table at the top, then each email with all 5 subject options (where applicable) and full body. Append the full call script package. This is Brian's reference — not the docx skill, plain markdown.

---

## Step 13 — Excel Tracker Update

File: `C:\Users\MINI OSI RIG\OneDrive - OSI Hardware\Documents\Claude\OSI-Brain\prospects-tracker-new.xlsx`

### Tab 1 — Prospects

Append one row:

Name | Title | Company | LinkedIn URL | OSI Angle | HubSpot Status | Action | Date Added | Notes

- HubSpot Status: `Brian — HubSpot ID [id]`
- Action: `Pursue — master sequence live`
- Notes: Personal Hook + sequence type in 1-2 sentences

### Tab 2 — Company Status (if running multi-prospect batch)

One row per company per run. Status: Completed / Partial / Not Started. Skip Tab 2 for one-off interactive runs on a single prospect.

OneDrive-safe Python: `openpyxl.load_workbook` on local path first; on EINVAL fetch bytes via SharePoint MCP, load with `load_workbook(BytesIO(bytes))`, edit, save to local path via `wb.save(QUEUE_PATH)`.

---

## Step 14 — Confirm and Hand Off

Present Brian with:
1. Link to the saved markdown reference
2. The final schedule table — confirm zero dates on Sat/Sun/holiday
3. Note: if the prospect replies at any point, mark remaining queue entries `status: "paused-replied"` (Brian can do this manually or via a one-liner Python script)

---

## OSI Product Lines — Reference

1. **Optics** — SmartOptics transceivers, private-labeled. Free sample is the opening wedge.
2. **DWDM and Open Line Systems** — SmartOptics DCP platform, 30-50% below Ciena/Nokia. Ships fast.
3. **Compute and Components** — DIMMs from Samsung / Hynix / Micron. Lead with DIMMs.
4. **Storage** — NetApp TPM, pre-owned storage.
5. **TPM** — 40-60% below OEM. Multi-vendor. Gartner-recognized, privately owned, no PE.
6. **Pre-Owned and New Networking** — Pre-owned Cisco/Juniper/Arista. New Nokia authorized.
7. **Professional Services** — Strong signal only. Never lead cold.

---

## Vertical Intelligence — Cheat Sheet

**Telco / service providers:** lead optics + supply chain reliability. Do NOT open free SFPs at scale. TPM rarely the opener at engineer level — sits at director.

**Banks / large financial:** lead optics, free SFP wedge works at engineer level. Do NOT lead TPM (regulated, often locked to OEM). Park Place / Service Express merger wedge if they have known TPM.

**Professional services / consulting:** TPM viable opener. Lead pain, not price. Free optics also works.

**Manufacturing:** free optics as break-glass insurance. TPM for aging Cisco gear.

**Healthcare:** TPM with documented SLAs. DIMMs for server refresh. Gartner-recognized + privately owned + no PE matters here.

---

## TPM Positioning

**Unknown if they have TPM:**
- Banks: optics opener, TPM is second conversation
- Consulting: TPM can open, lead with pain not savings %
- Manufacturing / enterprise: TPM strong, aging gear + OEM EOL is the hook

**Known TPM provider (Park Place, Service Express, Curvature):**
> "With the Park Place and Service Express merger, a lot of teams have been taking a fresh look at their TPM relationships. Have you had a chance to renegotiate since the merger, or are you still on the same rates?"

---

## DWDM / SmartOptics Talking Points

- Cost: 30-50% below Ciena and Nokia. Minimal licensing.
- Space + power: significant reduction vs. traditional DWDM platforms.
- Simplicity: easier to deploy, simplified sparing vs. traditional pluggables.
- Lead times: ships faster than OEMs and commodity vendors.
- Pedigree: backed by original engineering core. Not grey market.

---

## Cold Call Opener Rules — Reference

1. Open with "How have you been?" — 6.6x baseline meeting rate.
2. State a clear reason for calling.
3. End with a question about their world. Never "Is now a good time?"
4. Never ask "Is now a good time?"
5. Voicemails: 15 seconds max. No phone number. End with Brian's email spelled audibly ("that's bc at osihardware dot com"). Always present or future tense. Never past.

---

## Why this skill is the master

bc-7step-w-tracking gave us BCC tracking, weekend-skip, signature management, the swag/SFP and "Any thoughts?" moves, and standalone end-to-end ergonomics. Its weakness was hardcoded scheduled tasks — fragile when the machine was off or Outlook expired, and zero collision protection across in-flight sequences.

bc-osi-outreach-sequence-v2 gave us the queue, self-healing cadence, same-company stagger, holiday avoidance, and the full Orum-ready call script package. Its weakness was the rigid handoff requirement — couldn't run on its own.

abc-7step-master inherits all the strengths of both. It is the only skill Brian needs for new prospect outreach going forward.

