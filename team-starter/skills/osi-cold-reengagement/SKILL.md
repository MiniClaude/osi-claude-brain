---
name: osi-cold-reengagement
description: >
  Find cold 1st-degree LinkedIn connections and create HubSpot InMail tasks to re-engage them.
  Use this skill when the user says "find cold connections," "who haven't I messaged," "find me
  people to reach out to," "LinkedIn re-engagement," "cold connections," or any variation of
  searching existing LinkedIn connections for outreach opportunities. Also triggers when the user
  says "keep going" or "find another one" during a LinkedIn prospecting session.
---

> **SYNC NOTE:** This skill exists in two locations: `C:\Claude-Brain\skills\osi-cold-reengagement\` (Git-versioned, source of truth, backed up at github.com/Drrewdy/Claude-Brain) and the local Cowork `.claude/skills/` mount. Any edits must go into `C:\Claude-Brain\skills\` and be pushed to GitHub. If returning after days away, run `git pull` first to get the latest, then check the local Cowork copy and re-install the `.skill` file if the source has drifted.

# OSI Cold LinkedIn Re-Engagement

## What this skill does

Searches my existing 1st-degree LinkedIn connections for cold prospects who qualify
against OSI's ICP, then creates 2 HubSpot InMail tasks spaced 2 weeks apart with
personalized draft messages saved in the task notes.

Read this entire skill before starting.

---

## The Rules

- No em-dashes (—) anywhere. Split into two sentences instead.
- Keep everything tight and direct.
- Draft messages: peer-to-peer tone, not vendor-to-buyer.
- Never create HubSpot tasks for contacts not owned by Andy McLean, Mark Metz, or John Houston.

---

## Step 1: Search LinkedIn for candidates

Navigate to LinkedIn people search filtered to 1st-degree connections with relevant titles.
Use regular LinkedIn only — not Sales Navigator.

Good search URL:
`https://www.linkedin.com/search/results/people/?network=%5B%22F%22%5D&keywords=network+engineer+infrastructure+director`

Pull 5-8 names from the results. Focus on titles like:
- Network Engineer / Sr Network Engineer
- IT Director / Director of IT
- Director / Sr Director of Network Infrastructure
- Network Architect / Director of Network Architecture
- Manager / Sr Manager IT Network Engineering
- VP of IT / VP of Infrastructure
- Data Center Infrastructure Manager

---

## Step 2: Batch-check HubSpot ownership

Search HubSpot for each candidate before doing any LinkedIn research.

**Hard rule:** Only proceed with contacts owned by:
- [MY_FULL_NAME], owner ID [MY_HUBSPOT_OWNER_ID]
- Mark Metz — owner ID 210187184
- John Houston — owner ID 210187193

Skip anyone owned by another rep. Do not flag it as an issue — just move on silently.

Also note `notes_last_contacted` for each qualifying contact. This determines whether to
check LinkedIn messages in the next step.

---

## Step 3: Check message history (only when needed)

Use this rule to decide whether to check LinkedIn messages:

- **Last contacted 6+ months ago in HubSpot:** Skip LinkedIn message check. HubSpot date
  already confirms they meet the cold threshold. Go straight to qualification.
- **Last contacted within 6 months in HubSpot:** Disqualify immediately. Too recent.
- **No HubSpot record:** Check LinkedIn messaging before proceeding. Navigate to:
  `https://www.linkedin.com/messaging/?searchTerm=[First%20Last]`
  If messaged within 6 months, disqualify and move to the next candidate.

---

## Step 4: Qualify the prospect

Navigate to their LinkedIn profile and skills page. Evaluate against OSI's ICP:

**Target:**
- Title confirms they buy or specify networking/server/storage hardware — not just adjacent to it
- Skills with real endorsements: Cisco, optical networking, DWDM, transceivers, data center
  infrastructure, network design, vendor management for hardware, servers, storage
- Works at a mid-to-large enterprise, carrier, telecom, or regional data center operator
- Not a hyperscaler (Google, Meta, Amazon, ByteDance) — they build custom, OSI can't compete

**Disqualify if:**
- Title is project/program management with no hardware skills
- All skills are project management, Lean Six Sigma, Scrum, supply chain ops — zero networking
- Works at a hyperscaler at scale

**Verdict format:**
- Yes: worth reaching out, brief reason and angle
- No: clear reason why not

If No, move to the next candidate from the search results.

---

## Step 5: Determine the OSI angle

Based on their profile, pick the right play. Do not limit to one if multiple apply:

- **Optics/DWDM:** Network architects, transport engineers, carriers — any Cisco optical,
  DWDM, or 400G signal. Lead with SmartOptics: 30-50% below Ciena/Nokia, ships fast.
- **TPM:** Large enterprise with multi-vendor gear and vendor management skills. Lead with
  40-60% below OEM. Mention Park Place/Service Express merger as competitive context.
- **Compute/DIMMs:** Anyone with server, Dell PowerEdge, Cisco UCS, or infrastructure skills.
  Lead with Samsung/Hynix DIMMs below OEM, manufacturer warranties. DDR4 is a strong play.
- **Storage:** NetApp, SAN, storage infrastructure signals.
- **Pre-Owned Networking:** Cisco/Juniper/Arista environments, Smartnet references.

---

## Step 6: Write the 2 draft messages

**Message 1 (1st LinkedIn Message):**
- Open with something specific to their profile: a title change, a certification, a company
  detail, a skill combination that's unusual
- One clear ask: is it worth a quick conversation?
- Under 300 characters if possible. Always mobile-friendly.
- No em-dashes.

**Message 2 (2nd LinkedIn Message):**
- Different angle than Message 1. If Message 1 was DWDM, pivot to TPM or compute here.
- Or use a market trigger: DIMMs pricing, Park Place/Service Express merger, 400G adoption.
- One clear ask: worth a 15-minute call?
- Keep it short.

---

## Step 7: Create HubSpot tasks

Create 2 tasks on the prospect's contact record:

**Task 1:**
- Subject: "1st LinkedIn Message"
- Type: LINKED_IN_MESSAGE
- Due: today
- Notes: Message 1 draft
- Owner: [MY_HUBSPOT_OWNER_ID]

**Task 2:**
- Subject: "2nd LinkedIn Message"
- Type: LINKED_IN_MESSAGE
- Due: 14 days from today
- Notes: Message 2 draft
- Owner: [MY_HUBSPOT_OWNER_ID]

Use manage_crm_objects to create both tasks in a single call.
Associate both to the contact record.

If the prospect is not in HubSpot, flag this to the user and ask whether to add them first.

---

## After each prospect

Tell the user the verdict, show both draft messages, and confirm the HubSpot tasks were created
with links. Then ask: "Keep going?"

If yes, return to Step 1 and continue from the next candidate in the search results,
or load the next page if the current page is exhausted.
