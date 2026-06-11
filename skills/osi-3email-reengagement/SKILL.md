---
name: osi-3email-reengagement
description: >
  Generate a hyper-personalized 3-email re-engagement sequence for OSI Global prospects
  who have already been through a 7-email sequence. Use this skill when Brian uploads a
  LinkedIn profile and indicates this is a second-touch outreach, 6-7 months after the
  original sequence. Triggers on: "re-engagement," "second touch," "circle back,"
  "went through the 7 emails," "re-engage [name]," or any time Brian uploads a profile
  and mentions it has been months since last contact. Always research recent company news
  before writing. Always run this skill before writing any re-engagement outreach.
---

# OSI Global 3-Email Re-Engagement Sequence

## Your job

Brian has given you a LinkedIn profile. This person has already been through a 7-email
sequence 6-7 months ago and did not respond. They know who OSI is. Your job is to re-open
the door with fresh angles, not re-introduce the company. Produce the full outreach package:
strategy, call scripts, LinkedIn message, and 3 emails. Everything must feel new and timely.

Read this entire skill before producing any output.

---

## Brian Rules — apply to every output

- No em-dashes (—) anywhere. Not once. Split into two sentences if needed.
- Keep prose tight and direct. No fluff.
- Emails must feel like a human wrote them to one person, not a mass blast.
- Tone: peer-to-peer. They have heard Brian's name before. Acknowledge time has passed
  without being awkward about it.

---

## Step 1: Research (do this before writing anything)

**HubSpot Check**
Search HubSpot for the prospect and their current company. Pull any existing notes
on this contact to understand what was sent previously. Note the HubSpot owner.


**Company News Research**
Search the web for recent news about the prospect's company. Look for:
- Funding rounds, acquisitions, or mergers
- New data center buildouts or infrastructure announcements
- Leadership changes (new CTO, CIO, VP of Infrastructure)
- Network modernization or cloud migration projects
- Cost-cutting or vendor consolidation news
- Any 400G, DWDM, or server refresh announcements

This research feeds the hook in Email 1. If no news is found, fall back to a market
trigger (DIMMs pricing, Park Place/Service Express merger, 400G adoption trends).

---

## Step 2: Produce all outputs in this exact order

---

### 1. Strategy and Fit

**Quick Connect Keywords**
List 6-10 words or phrases to listen for on a call. Spoken signals that confirm fit.
Only list ones relevant to this prospect and their current situation.

**Previous Employer OSI Client Check**
List previous employers. Note any HubSpot matches. State clearly if none found.

**What Was Sent Before**
Summarize what OSI product lines were targeted in the original sequence based on any
HubSpot notes. If notes are unavailable, infer from their profile and title.

**New Angles for Re-Engagement**
Identify 1-2 product lines or talking points that were NOT the primary focus last time.
This sequence should feel different, not like a repeat.

**Target Sequences**
List the OSI product lines to lead with this time. Choose from:
- Optics
- DWDM (Open Line Systems)
- TPM
- Compute and Components (lead with DIMMs)
- Storage
- Pre-Owned and New Networking
- Professional Services (only if strong signal)

**The Play**
1-2 sentences. How to re-approach this prospect with a fresh angle. Be specific about
what has changed (company news, market shift, new product) that makes this worth sending.

**The Personal Hook**
A timely trigger from research: company news, a recent LinkedIn post, a job change,
a market event. This must feel current. Do not reuse the hook from the original sequence.

---

### 2. Live Call Script

Under 30 seconds. Reference something new and timely. Do not re-introduce OSI — they
already know who Brian is. Open a conversation, do not pitch.

---

### 3. Voicemail Script

Under 20 seconds. Reference the new hook. Mention an email on its way.

---

### 4. Re-Engagement Message (LinkedIn or Email)

Under 300 characters if LinkedIn. Short and timely. Reference the new hook.
Do not mention it has been months since last contact — just lead with the new angle.
Do not mention mutual connections.

---

### 5. The 3-Email Sequence

**Cadence**
- Email 1: Day 1
- Email 2: Day 14
- Email 3: Day 30

**Subject line rules**
One subject line across all 3 emails. Emails 2 and 3 use "RE:" prefix.
The subject line should reference something new and specific, not a generic opener.

**Rules for re-engagement tone**
- Do not re-introduce OSI or explain what they do. The prospect has seen 7 emails.
- Do not acknowledge the previous sequence directly.
- Lead with something new: company news, a market trigger, a pricing window, a product
  update. Make them feel like this outreach is timely, not persistent.
- Email 3 is a clean close. No ask. Leave the door open with a single sentence.

**Format rules**
- Short and mobile-friendly.
- One clear ask per email. Never two.
- Do not mention mutual LinkedIn connections.
- No corporate speak.

**Tone**
Direct, human. Slightly warmer than a cold first touch — they know the name — but not
presumptuous. No "as I mentioned before" or references to the previous outreach.

---

## DWDM and Smartoptics — use when DWDM is a target sequence

- Cost: 30-50% below Ciena and Nokia. Minimal licensing fees.
- Space and power: Significant reduction vs. traditional DWDM platforms.
- Simplicity: Easier to deploy and manage. Simplified sparing vs. traditional pluggables.
- Lead times: Ships faster than OEMs and commodity vendors.
- Pedigree: Backed by original engineering core. Not a grey market product.

---

## OSI Product Lines

1. **Optics** - SmartOptics transceivers. Sample offer is the opening wedge.
2. **DWDM and Open Line Systems** - SmartOptics DCP platform, 30-50% below Ciena/Nokia.
3. **Compute and Components** - Dell/HP servers, DIMMs (Samsung/Hynix/Micron). Lead with
   DIMMs. DDR4 significantly cheaper than DDR5 for workloads that do not need it.
4. **Storage** - NetApp TPM, pre-owned storage, server components.
5. **TPM** - 40-60% below OEM. Multi-vendor (Cisco, Dell, HP, NetApp, Juniper, Arista).
   Mention Park Place/Service Express merger as a competitive talking point.
6. **Pre-Owned and New Networking** - Pre-owned Cisco/Juniper/Arista. New Nokia.
7. **Professional Services** - Only raise if strong signal. Never lead cold.

---

## Step 6: Save to HubSpot automatically after producing output

**Create a note** on the prospect's contact record containing sections 1, 2, and 3:
- Strategy and Fit (including new angles and what was sent before)
- Live Call Script
- Voicemail Script

Use manage_crm_objects (objectType: "notes"), owner 213536174, associated to contact.

**Create a Re-Engagement Message task:**
- Subject: "Re-Engagement LinkedIn Message"
- Type: LINKED_IN_MESSAGE
- Due: today
- Notes: the re-engagement message text (section 4)
- Owner: 213536174

**Create 2 follow-up tasks:**
- Task 1: "1st LinkedIn Message" — LINKED_IN_MESSAGE — due today
- Task 2: "2nd LinkedIn Message" — LINKED_IN_MESSAGE — due 2 weeks from today
- Notes on each: the relevant email draft

If the prospect is not in HubSpot, flag this to Brian before creating anything.
Never use em-dashes in any HubSpot content.

---

## Output format

Present all 5 sections clearly labeled and in order. Keep each section self-contained
so Brian can copy any piece and use it without editing.
