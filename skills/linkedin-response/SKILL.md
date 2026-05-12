---
name: linkedin-response
description: >
  Draft personalized LinkedIn messages for new 1st-degree connections and re-engage dormant connections. 
  Researches each person (web + HubSpot CRM cross-reference + mutual connections) and outputs ready-to-send 
  messages in Brian Charrette's voice. ALWAYS use this skill when Brian says anything like: "new LinkedIn 
  connections", "draft LinkedIn messages", "LinkedIn responses", "respond to connections", "re-engage old 
  connections", "connections I haven't messaged", "LinkedIn follow-up", "reconnect with connections", 
  "who connected with me", or "message my LinkedIn connections."
---

# LinkedIn Response Skill

Brian Charrette is a 16-year sales veteran at OSI Global (IT infrastructure solutions — hardware, optics,
professional services, Systain TPM). His LinkedIn philosophy is **relationship-first**: warm handshake before 
any business conversation. The goal of every message is to open a human door, not a sales cycle.

---

## Two Modes

### Mode 1: New Connections (default / daily use)
Finds connections added in the past 24 hours, researches each person, and drafts a personalized first-touch message.

**Trigger phrases:** "new connections", "LinkedIn responses today", "draft responses", "who connected with me today"

### Mode 2: Re-engagement Sweep
Finds existing connections with no message activity in 12+ months, drafts a warm check-in.
Cap each batch at **15 people** to keep quality high. If Brian has more, run again the next day.

**Trigger phrases:** "re-engage", "old connections", "haven't messaged", "reconnect", "follow up with connections", "been a while"

---

## Workflow

### Step 1 — Pull Connections from LinkedIn (Chrome)

**New Connections mode:**
1. Navigate to: `https://www.linkedin.com/mynetwork/invite-connect/connections/`
2. Sort by "Recently Added"
3. Identify anyone connected in the past 24 hours
4. For each: capture full name, title, current company, location

**Re-engagement mode:**
1. Navigate to LinkedIn Messages: `https://www.linkedin.com/messaging/`
2. Scan conversations sorted by oldest activity — flag threads with no message in 12+ months
3. Alternatively: `https://www.linkedin.com/search/results/people/?network=%5B%22F%22%5D` sorted by connection date
4. Work through a batch of up to 15 people
5. Capture name, title, company for each

**For every person (both modes):**
- Visit their LinkedIn profile
- Note their full title, current company, and any visible career history
- Note mutual connections (shown on their profile)
- Note any recent posts or job changes that are timely pegs

---

### Step 2 — Research Each Person (run in parallel where possible)

**A. Web Search**
Run: `"[Full Name]" "[Company]"` — look for:
- What their company does (industry, size, tech stack focus)
- Recent company news (funding rounds, data center expansions, network buildouts, acquisitions)
- Their role's typical pain points (a VP of Network Engineering cares about uptime and refresh cycles; a Procurement Director cares about lead times and budget)

**B. HubSpot CRM Cross-Reference**
Search HubSpot for:
- Their **current company** name
- Any **previous companies** visible on their LinkedIn profile

If a match is found → flag as **OSI Customer Match** (this becomes the lead angle in the message — it's the most powerful hook available).

---

### Step 3 — Draft the Message

Every message follows this structure. Keep it to **3–5 sentences max**. Brevity is respect.

**Line 1 — The Specific Hook (choose one, in priority order):**

1. **OSI Customer Match** → "I noticed you came from [Company] — we've worked with their team on [networking/optics/maintenance]. Small world."
2. **Mutual Connection** → "I see we're both connected to [Name] — good people tend to know good people."
3. **Timely Company Peg** → "Saw [Company] is expanding their [network/data center footprint] — exciting time to be there."
4. **Role + Vertical Overlap** → "As a [title] in [industry], you're probably navigating the same [hardware lifecycle / lead time / OEM refresh] pressures a lot of the teams we work with are dealing with."

**Line 2 — Who Brian Is (brief, not a pitch):**
> "I've been with OSI Global for 16 years — we work with enterprise and telco teams on infrastructure lifecycle, optics, and third-party maintenance. Mostly helping people avoid unnecessary refreshes and get more runway out of what they already own."

For re-engagement, replace with:
> "Wanted to check in — it's been a while since we connected and I realized I'd never properly followed up."

**Line 3 — The Open Door:**
> "Happy to be a resource if anything infrastructure-related ever crosses your desk — or just good to stay connected either way."

---

### Tone Rules — These Are Non-Negotiable

**Hard banned phrases — do not use any of these under any circumstances:**
- "I wanted to reach out" / "Wanted to reach out"
- "I hope this message finds you well" / "Hope this finds you well"
- "Touching base" / "circling back"
- "Synergy"
- "Leverage" (as a verb)
- "At the end of the day"
- "Game-changer"
- "I'd love to connect" / "I'd love to chat"
- "Pick your brain"
- "Thanks for connecting!" (cliché opener)

The reason these matter: Brian has been doing this for 16 years. These phrases mark someone as a template-sender. Brian's value is that he sounds like a real person who actually did their homework.

**The open door line (Line 3) must NOT pitch a product.** It should genuinely just open a door. Compare:

❌ Wrong: "If anything comes up on the capex side or you're facing OEM constraints, I'd rather you think of us first."
✅ Right: "Happy to be a resource if anything infrastructure-related ever crosses your desk — or just good to stay connected either way."

The wrong version is a soft pitch. The right version is an open door. The difference matters because recipients can feel it.

**Brian's voice is:** Direct. Warm. Does-his-homework. Candid without being blunt. He sounds like someone who's been in the industry long enough to skip the fluff — but genuinely likes people.

**Never pitch a product by name in message 1.** No "Systain", no "Smartoptics", no "50-80% savings." Save those for when there's actually a conversation.

**Re-engagement tone:** Acknowledge the gap naturally without over-apologizing. If there's a timely peg (job change, company news), use it to make the outreach feel relevant rather than random. If nothing obvious exists, a simple "realized I'd never properly followed up" is better than a forced hook.

---

### Example Messages (reference these for tone calibration)

**New Connection — OSI Customer Match:**
> "Sarah — I noticed Lumen came up in our system; we've actually worked with your team before on network infrastructure. Small world. I've been with OSI Global for 16 years — we help enterprise and telco teams extend hardware lifecycle, navigate optics, and manage support for gear OEMs have stopped covering. Happy to be a resource if anything infrastructure-related comes up — or just good to stay connected."

**New Connection — No CRM match, telco vertical:**
> "Great to connect. As a network architect at a carrier, you're probably dealing with the same OEM refresh pressure and EOL timeline headaches a lot of the teams we work with navigate. I've been with OSI Global 16 years helping enterprise and telco teams get more runway out of their infrastructure without the forced upgrades. Happy to be a resource if that ever becomes a conversation."

**Re-engagement — Company news peg:**
> "I see Flexential has been expanding their fiber footprint — good timing to be in that seat. It's been a while since we connected and I realized I'd never properly followed up. I'm still at OSI Global, still focused on the same things — optics, hardware lifecycle, maintenance for gear OEMs don't want to touch anymore. If infrastructure ever crosses your radar, I'm happy to be a resource."

**Re-engagement — No specific peg:**
> "It's been a while since we connected — I was looking through my network and realized I'd never properly followed up with you. I'm still at OSI Global focused on enterprise infrastructure. If that ever becomes relevant — hardware refresh, optics, third-party maintenance — I'd rather you think of us than go searching. Either way, good to stay connected."

---

### Step 4 — Assemble the Output Document

Use the **docx skill** to produce a formatted Word document.

**Save to:** `/sessions/.../mnt/Claude/LinkedIn_Messages_[YYYYMMDD].docx`

**Document structure:**

```
Title: LinkedIn Messages — [Date]
Subtitle: [New Connections — Last 24 Hours] OR [Re-engagement Batch — [Date]]

---

[PERSON NAME] — [Title] at [Company]

RESEARCH SUMMARY
• Company: [what they do, industry, notable facts]
• OSI Customer Match: YES — Account: [name] / NO
• Mutual Connections: [names, or "none visible"]
• Key Angle: [the most compelling hook for this person]

DRAFTED MESSAGE
[Ready-to-copy message]

────────────────────────────────────────────
```

**Prioritize OSI Customer Matches at the top of the document** — those are the highest-value connections to message first.

If there are 0 new connections found, note that clearly and confirm the timeframe checked.

---

## OSI Vertical Hooks (fallback reference)

When no specific hook is available, use the person's vertical to anchor Line 1:

| Vertical | Natural angle |
|---|---|
| Telecom / Carrier | Lifecycle extension, optical scale, TPM for EOL gear |
| Colocation / Data Center | 400G/800G readiness, optics, ITAD |
| Financial Services | Compliance-safe maintenance, hardware reliability, NBD SLAs |
| Software / SaaS / Hyperscaler | Avoiding OEM cost inflation at scale |
| Healthcare / Gov | Lifecycle stabilization, TPM for mission-critical environments |
| General Enterprise | Hardware lifecycle, avoiding forced refreshes, cost reclamation |

---

## Key OSI Facts for Message Context

- 50-80% savings off OEM pricing
- Gartner-recognized for hardware, optics, and TPM
- Largest global Smartoptics partner (800G transponders)
- Systain TPM: 24x7x365 TAC, NBD/4-hour SLAs, covers EOL gear
- Offices in SF, LA, Phoenix, Dallas, Denver, NYC, Sacramento, Amsterdam
- Proven multi-country deployment experience

---

## Handling Edge Cases

**Chrome / LinkedIn not accessible:**
If Chrome browser tools are unavailable, say: "LinkedIn browser access isn't available right now. You can either reconnect the Chrome extension or paste a list of the connections you want me to draft for (name, title, company) and I'll handle all the research and drafting from there." Do not just fail silently.

**Can't find the person's LinkedIn profile or it's private:**
Note in output: "Profile limited — drafted based on connection request info only" and write a more generic but still warm message using whatever name/title was visible.

**HubSpot search returns no results:**
Skip the CRM angle — don't force it. Move to web research or vertical hook.

**Person appears to be in an unrelated field (not IT/tech):**
Still draft a warm message — OSI's TPM and hardware lifecycle services reach into healthcare, finance, and government too. Focus on relationship over pitch.

**Re-engagement: person changed companies since connecting:**
This is actually a great hook — "I see you moved to [new company] — congrats on the transition." Research the new company through HubSpot too.
