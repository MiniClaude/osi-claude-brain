---
name: osi-3email-new
description: >
  Generate a hyper-personalized 3-email new outreach sequence for OSI Global prospects.
  Use this skill when Brian uploads or pastes a LinkedIn profile and wants a shorter outreach
  treatment — for directors, targets where 7 emails is overkill, or when a tighter cadence
  fits better. Triggers on: "3-email sequence," "short sequence," "3 emails for [name],"
  "new outreach 3 emails," or any time Brian drops a profile and asks for outreach without
  specifying 7 emails. Always run this skill before writing any 3-email cold outreach sequence.
---

# OSI Global 3-Email New Outreach Sequence

## Your job

Brian has given you a LinkedIn profile. This is a first-touch outreach for a prospect where
a shorter sequence is appropriate. Produce the full outreach package: strategy, call scripts,
LinkedIn invite, and a 3-email sequence. Everything must be specific to this person.

Read this entire skill before producing any output.

---

## Brian Rules — apply to every output

- No em-dashes (—) anywhere. Not once. Split into two sentences if needed.
- Keep prose tight and direct. No fluff.
- Emails must feel like a human wrote them to one person, not a mass blast.
- Tone: peer-to-peer, not vendor-to-buyer.

---

## Step 1: HubSpot Check (do this first, silently)

Before writing anything, search HubSpot for:
1. The prospect's name and current company
2. Each previous employer listed on their profile

Flag any that are existing OSI contacts or companies. If a match exists, note it in the
Strategy section as a warm reference point. Note the HubSpot owner.

---

## Step 2: Produce all outputs in this exact order

---

### 1. Strategy and Fit

**Quick Connect Keywords**
List 6-10 words or phrases to listen for if the cold call gets answered. Spoken signals
that confirm fit. Examples: "Cisco optics," "Smartnet," "network refresh," "400G,"
"server refresh," "DIMMs," "DWDM," "dark fiber," "lead times." Only list ones relevant
to this prospect.

**Previous Employer OSI Client Check**
List each previous employer. Note any that appear in HubSpot as existing OSI contacts
or accounts. State clearly if none found.

**Target Sequences**
List every OSI product line that applies. Do not limit to one. Choose from:
- Optics
- DWDM (Open Line Systems)
- TPM
- Compute and Components (lead with DIMMs)
- Storage
- Pre-Owned and New Networking
- Professional Services (only if strong signal — never lead cold with this)

**The Play**
1-2 sentences. Exactly how to attack this prospect based on their title, company, and
background. Be concrete about what to lead with and why.

**The Personal Hook**
1-2 specific details from their LinkedIn profile: a recent job change, certification, past
company, specific project, or unusual skill. This hook must appear in Email 1 and the
LinkedIn invite.

---

### 2. Live Call Script

Under 30 seconds when spoken aloud. Lead with the specific pain point for their role.
Reference the Personal Hook. Open a conversation, do not pitch.

---

### 3. Voicemail Script

Under 20 seconds. Reference the Personal Hook. Mention an email you are about to send.

---

### 4. LinkedIn Invite

Under 300 characters. Low friction. Focused on networking or benchmarking, not pitching.
Must include the Personal Hook. Do not mention mutual connections.

---

### 5. The 3-Email Sequence

**Cadence**
- Email 1: Day 1
- Email 2: Day 7
- Email 3: Day 21

**Subject line rules**
One subject line across all 3 emails. Emails 2 and 3 use "RE:" prefix.

**Personalization rules**
- Email 1 must open with or directly reference the Personal Hook.
- Emails 2 and 3 should weave in references to their tech stack, career history, or
  company context where it fits naturally.
- Every email must read like it was written for this one person.

**Format rules**
- Short and mobile-friendly. An executive reading on their phone should scan it in 10 seconds.
- One clear ask per email. Never two.
- Do not mention mutual LinkedIn connections anywhere.
- No corporate speak. No "I hope this email finds you well."

**Tone**
Direct, human, peer-to-peer. Brian is reaching out as Brian, not as a company.

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
- Strategy and Fit
- Live Call Script
- Voicemail Script

Use manage_crm_objects (objectType: "notes"), owner 213536174, associated to contact.

**Create a LinkedIn Connection Request task:**
- Subject: "LinkedIn Connection Request"
- Type: LINKED_IN_MESSAGE
- Due: today
- Notes: the LinkedIn invite text (section 4)
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
