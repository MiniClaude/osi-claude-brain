---
name: osi-outreach-7email
description: >
  Generate a full hyper-personalized 7-email outreach sequence for OSI Global sales prospecting.
  Use this skill whenever Brian uploads or pastes a LinkedIn profile and wants outreach drafted —
  whether he says "write a sequence," "do the full outreach," "run the sequence prompt," or just
  drops a profile screenshot or text. Also triggers for phrases like "build me the emails," "full
  sequence," "7-email," or "outreach for [name]." Always run this skill before writing any cold
  outreach email sequence.
---

# OSI Global Hyper-Personalized 7-Email Sequence

## Your job

Brian has given you a LinkedIn profile. Your job is to produce every piece of outreach he needs to approach this person: the strategy, the call scripts, a LinkedIn invite, and a full 7-email sequence. Everything must be specific to this person — not generic.

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

Flag any that are existing OSI contacts or companies. If a match exists, note it in the Strategy section as a warm reference point.

---

## Step 2: Produce all outputs in this exact order

---

### 1. Strategy and Fit

**Quick Connect Keywords**
List 6-10 words or phrases to listen for if the cold call gets answered. These are spoken signals that confirm fit. Examples: "Cisco optics," "Smartnet," "network refresh," "400G," "server refresh," "DIMMs," "DWDM," "dark fiber," "lead times." Only list ones relevant to this prospect's profile and likely environment.

**Previous Employer OSI Client Check**
List each previous employer. Note any that appear in HubSpot as existing OSI contacts or accounts. If none found, state that clearly.

**Target Sequences**
List every OSI product line that applies to this prospect. Do not limit to one. Choose from:
- Optics
- DWDM (Open Line Systems)
- TPM
- Compute and Components (lead with DIMMs)
- Storage
- Pre-Owned and New Networking
- Professional Services (only if there is a strong signal — never lead cold with this)

**The Play**
1-2 sentences. How to attack this prospect based on their specific title, company, and background. Be concrete about what to lead with and why.

**The Personal Hook**
1-2 specific details from their LinkedIn profile that will anchor the outreach. This could be a recent job change, a certification, a past company, a specific project they mentioned, or an unusual skill. This hook must appear in Email 1 and the LinkedIn invite.

---

### 2. Live Call Script

Under 30 seconds when spoken aloud. Lead with the specific pain point for their role. Reference the Personal Hook. Do not pitch — open a conversation.

---

### 3. Voicemail Script

Punchy, under 20 seconds. Reference the Personal Hook. Mention an email you are about to send.

---

### 4. LinkedIn Invite

Under 300 characters. Low friction. Focused on networking or benchmarking, not pitching. Must include the Personal Hook. Do not mention mutual connections.

---

### 5. The 7-Email Sequence

Follow all rules below before writing a single email.

**Cadence**
- Email 1: Day 1
- Email 2: Day 4
- Email 3: Day 9
- Email 4: Day 14
- Email 5: Day 21
- Email 6: Day 30
- Email 7: Day 45

**Subject line rules**
- Emails 1, 2, 3 share the same subject line. Emails 2 and 3 use "RE:" prefix.
- Emails 4 and 5 share a second subject line.
- Emails 6 and 7 share a third subject line.
- Three total subject lines across the sequence.

**Personalization rules**
- Email 1 must open with or directly reference the Personal Hook.
- Later emails should weave in references to their likely tech stack, career history, or company context where it fits naturally.
- Every email must read like it was written specifically for this one person.

**Format rules**
- Keep every email short and mobile-friendly. An IT executive reading on their phone should be able to scan it in 10 seconds.
- No bullet-point overload. Prose preferred.
- One clear ask per email. Never two.
- Do not mention mutual LinkedIn connections anywhere in the sequence.

**Tone**
Direct, human, peer-to-peer. Brian is reaching out as Brian, not as a company. No corporate speak, no "I hope this email finds you well."

---

## DWDM and Smartoptics — use these talking points when DWDM is a target sequence

Lead with:
- **Cost**: 30-50% below Ciena and Nokia. Minimal licensing fees.
- **Space and power**: Significant reduction vs. traditional DWDM platforms.
- **Simplicity**: Easier to deploy and manage. Simplified sparing vs. traditional pluggables.
- **Lead times**: Ships faster than OEMs and commodity vendors.
- **Pedigree**: Backed by original engineering core. Not a grey market product.

---

## OSI Product Lines — reference when building the sequence

1. **Optics** - SmartOptics-manufactured transceivers, private-labeled. Sample offer is the opening wedge.
2. **DWDM and Open Line Systems** - SmartOptics DCP platform, 30-50% below Ciena/Nokia.
3. **Compute and Components** - Dell/HP servers, DIMMs (Samsung/Hynix/Micron). Lead with DIMMs. DDR4 significantly cheaper than DDR5 for workloads that do not need it.
4. **Storage** - NetApp TPM, pre-owned storage, server components.
5. **TPM** - 40-60% below OEM. Multi-vendor (Cisco, Dell, HP, NetApp, Juniper, Arista). Mention Park Place/Service Express merger as a competitive talking point.
6. **Pre-Owned and New Networking** - Pre-owned Cisco/Juniper/Arista (tested, OSI TPM available). New Nokia (authorized partner).
7. **Professional Services** - Only raise this if there is a strong signal. Never lead cold with it.

---

## Output format

Present all 6 sections clearly labeled and in order. Use headers. Keep each section self-contained so Brian can copy any piece independently and send it without editing.

---

## Step 6: Save to HubSpot (do this automatically after producing the output)

After generating all sections, create a HubSpot note on the prospect's contact record containing sections 1, 2, and 3:
- Strategy and Fit (full section)
- Live Call Script
- Voicemail Script

Use the manage_crm_objects tool to create a note (objectType: "notes") associated to the contact. Owner: Brian Charrette (hubspot_owner_id: 213536174).

If the prospect is not yet in HubSpot, flag this to Brian and ask whether to add them before saving the note.

Never use em-dashes in the note content. Replace any em-dash with a period or split into two sentences.

Also create a second HubSpot task:
- Subject: "LinkedIn Connection Request"
- Type: LINKED_IN_MESSAGE
- Due: today
- Notes: the LinkedIn invite text (section 4)
- Owner: Brian Charrette (213536174)
- Associated to the same contact record
