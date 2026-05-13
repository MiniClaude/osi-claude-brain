---
name: bc-linkedin-1st-connections-messaging
description: >
  Scans Brian Charrette's LinkedIn 1st-degree connections for people he has NOT yet messaged via DM,
  qualifies each against OSI's real ICP (derived from 107 active buyers), and drafts a personalized
  conversational message with a vertical-specific value prop and a clear goal to connect soon.
  Produces a ready-to-send Word doc. Can be run on a schedule (daily or weekly).
  ALWAYS use this skill when Brian says anything like: "check my new LinkedIn connections",
  "who haven't I messaged on LinkedIn", "LinkedIn 1st connections messaging",
  "draft messages for my new connections", "bc-linkedin-1st-connections", "run the LinkedIn message check",
  "pick 3 connections to message", "my unmessaged LinkedIn connections", "LinkedIn connection follow-up",
  "message my most recent connections", "qualify my new connections",
  or any variation of wanting to find, qualify, and message un-contacted 1st-degree LinkedIn connections.
  Also triggers automatically when Brian wants to run this on a schedule.
---

# BC LinkedIn 1st Connections Messaging

Brian Charrette is a 16-year sales veteran at OSI Global (enterprise IT infrastructure — networking
hardware, optics/transceivers, servers, storage, power infrastructure, and third-party maintenance/TPM).

**This skill does three things:**
1. Finds the 3 most recently added 1st-degree connections with no prior DM
2. Qualifies each against OSI's real ICP
3. Drafts a conversational, vertical-specific message with a clear ask to connect

The goal of every message is to **open a real conversation** — not just "stay connected." These are people
already in Brian's outreach orbit. The message should feel like a smart peer reaching out because they
see a genuine fit, not a template blast.

---

## OSI IDEAL CUSTOMER PROFILE
*(Derived from 107 active buyers — use this to qualify and score each connection)*

### Industry Tiers
| Tier | Industries | Score |
|------|-----------|-------|
| Tier 1 — Priority | Computer Software, Hospital/Health Care, Utilities, Wireless/ISP, Telecommunications | 30 pts |
| Tier 2 — Good fit | Defense & Space, Hospitality, Capital Markets, Retail, Oil & Energy, Chemicals, Insurance, Medical Devices | 20 pts |
| Tier 3 — Opportunistic | Higher Education, Financial Services, Auto, Construction | 12 pts |
| No fit | Non-enterprise, consumer, unrelated verticals | 0 pts |

### Company Size
| Range | Fit | Score |
|-------|-----|-------|
| 200–10,000 employees | Sweet spot | 20 pts |
| 50–200 or 10K–50K | Near-ICP | 12 pts |
| 50K+ employees | Large enterprise | 8 pts |
| <50 employees | Small | 4 pts |

### Revenue
| Range | Fit | Score |
|-------|-----|-------|
| $50M–$1B | Sweet spot | 20 pts |
| $10M–$50M | Mid-market | 15 pts |
| $1B–$10B | Large enterprise | 15 pts |
| $10B+ | Mega-corp | 10 pts |

### ICP Score Thresholds (Industry + Size + Revenue = max 70 pts for LinkedIn qualification)
- **50–70 pts → Strong ICP** — message with confidence, direct ask to connect
- **30–49 pts → Good ICP** — message with curiosity, soft ask
- **<30 pts → Weak ICP** — note it, draft a lighter message or skip

### Top Proven Verticals (from actual buyer history)
Real customers to reference mentally when crafting the angle:
- **Telecom/ISP**: T-Systems, MidAtlanticBroadband, Lumos Networks, SLIC Network Solutions
- **Utilities**: PPL, Navajo Tribal Utility, IHI Terrasun
- **Healthcare/Health Systems**: Liberty Software, ZOLL Services, Cherry Health
- **Defense/Gov**: BAE Systems
- **Software/IT Services**: Verint Systems, TSymmetry, Wave Technologies
- **Hospitality**: Hyatt Hotels

---

## Workflow

### Step 1 — Pull the Connections List (Chrome)

1. Navigate to: `https://www.linkedin.com/mynetwork/invite-connect/connections/`
2. Keep the default "Recently Added" sort order.
3. Capture the first 15–20 connections: full name, title, current company, location, connection date.

---

### Step 2 — Filter for Unmessaged Connections (DM check only)

These are 1st-degree connections — check **LinkedIn DM threads only** (not InMail).

For each person:
1. Navigate to their LinkedIn profile and click the **"Message"** button.
2. If the DM thread has **any prior history** → **skip them.** Already contacted.
3. If the thread is **completely blank** → candidate.

Alternative: search `https://www.linkedin.com/messaging/?searchTerm=[Name]` — no results = clean.

Work through the list until you have at least 5 unmessaged candidates. Take the **3 most recently added.**

> Note: InMail and DM are stored separately. A prior InMail does not block a DM candidate.

---

### Step 3 — Qualify Each Against OSI ICP

For each of the 3 selected, research and score:

**A. LinkedIn Profile**
- Full title, role scope, career history
- Current company name and size (visible on profile or company page)
- Mutual connections
- Any recent posts, job change, or promotion

**B. Web Research**
- Company industry, employee count, annual revenue
- Recent news (expansion, buildout, funding, contracts, acquisitions)
- Typical IT pain points for their role in that vertical

**C. HubSpot — Check for ACTUAL DEAL HISTORY**
Search HubSpot by company name. A company being in HubSpot as a contact/prospect record does NOT
count as a customer. Only flag **OSI Prior Customer** if there are **closed deals with revenue** on that
company record. Check the deals associated with the company — if deals exist with amount > $0, it's
a prior customer. Otherwise it's a prospect.

**D. Calculate ICP Score (Industry + Size + Revenue)**
Use the scoring table above. Note the tier and what drove the score.

---

### Step 4 — Draft the Message

**Message goal:** Start a real conversation. The ask at the end should be explicit — not "just good to stay
connected" but something that signals genuine interest in connecting soon.

**Message length:** 3–5 sentences max. Brevity is respect.

**Structure:**

**Line 1 — The Specific Hook** (choose ONE, in priority order):
1. **Prior OSI Customer (deals confirmed)** → *"[Company] came up in our history — we've actually done business with your team before on [area]. Small world."*
2. **Mutual Connection** → *"I see we're both connected to [Name] — good people tend to know good people."*
3. **Timely Signal** → *"Saw [Company] is [expanding/building/upgrading] — exciting time to be in that seat."*
4. **Vertical Fit** → Use the vertical-specific angle from the table below.

**Line 2 — Vertical-Specific Value Prop** (tailor to their industry):

| Vertical | What to say OSI helps with |
|----------|---------------------------|
| Telecom / Wireless / ISP | "We work with a lot of carriers and ISPs on scaling optics and extending the lifecycle of network gear — avoiding forced refreshes when OEMs stop supporting equipment." |
| Utilities | "We work with utilities on hardware lifecycle and third-party maintenance — keeping critical infrastructure running past OEM support windows without the capital hit of a forced refresh." |
| Hospital / Health Care | "We work with health systems on keeping mission-critical infrastructure running past OEM EOL — HIPAA-safe maintenance, lifecycle extension, avoiding disruptive refreshes." |
| Computer Software / IT Services | "We work with software and IT services companies on hardware lifecycle — servers, storage, optics — usually helping them reclaim 50–80% off OEM maintenance costs." |
| Defense / Gov | "We work with defense and government contractors on lifecycle extension and compliant third-party maintenance for infrastructure that has to stay up regardless of OEM timelines." |
| Medical Devices | "We work with medical device companies on server and network infrastructure — lifecycle extension, optics, and maintenance for gear OEMs stop covering." |
| Oil / Energy / Chemicals | "We work with energy and industrial companies on hardware lifecycle and third-party maintenance — a lot of teams in that space are managing aging infrastructure without the budget for full OEM refreshes." |
| Hospitality | "We work with hospitality companies on IT infrastructure lifecycle — servers, networking, optics — helping large property footprints avoid OEM-forced refresh cycles." |
| General Enterprise | "We work with enterprise IT teams on hardware lifecycle, optics, and third-party mainte