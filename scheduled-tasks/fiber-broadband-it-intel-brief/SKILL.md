---
name: fiber-broadband-it-intel-brief
description: Weekly fiber/broadband/IT industry intelligence brief — new companies, M&A, data center, AI, trade show intel for OSI prospecting
---

You are running a weekly industry intelligence sweep for Brian Charrette, senior IT hardware sales rep at OSI Global in Santa Barbara, CA. Brian sells networking gear, optics (SFP/QSFP), servers, storage, power infrastructure (APC/Eaton), and TPM to enterprise buyers. His goal: surface net-new prospecting targets BEFORE competitors do — new fiber operators, companies in build phase, M&A activity that creates hardware refresh cycles, and IT decision-makers speaking at shows.

## OBJECTIVE
Produce a concise weekly intel brief covering fiber/broadband, data center, and IT industry news from the past 7 days. Cross-reference new companies against HubSpot to flag greenfield opportunities. Save a Word doc to C:\Users\Mini\Documents\osi-claude-brain\sessions\intel-briefs\

---

## STEP 1 — READ DOCX SKILL
Read C:\Users\Mini\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\f739b7db-6b05-4960-a80a-699458ce501c\f2c37a34-61ab-4aec-859e-9d84203c1e7a\skills\docx\SKILL.md before creating any Word document.

---

## STEP 2 — SCRAPE INDUSTRY NEWS SOURCES

Fetch these URLs and extract company names, headlines, and key signals from the past 7 days:

**Fiber/Broadband:**
- https://bbcmag.com/category/company-news/ma/ (M&A)
- https://bbcmag.com/category/company-news/investment/ (new builds/funding)
- https://bbcmag.com/category/technology/fiber-broadband/ (fiber news)
- https://bbcmag.com/category/company-news/people/ (leadership changes)
- https://www.lightyears.net/ (fiber news)
- https://www.fiercetelecom.com/ (telecom news)
- https://www.lightreading.com/ (telecom/fiber analyst news)
- https://www.lightreading.com/broadband (broadband-specific)

**Data Center / AI / IT:**
- https://www.datacenterknowledge.com/ (data center news)
- https://www.theregister.com/data_centre/ (data center)
- https://www.networkworld.com/ (networking news)
- https://www.cnet.com/tech/services-and-software/data-centers/ (CNET data center)
- https://www.datacenterfrontier.com/ (data center builds and operators)

**Trade Shows — Speaker/Exhibitor/Sponsor Lists (scrape for company names):**
- https://fiberconnect2026.eventscribe.net/biography.asp?bucket=org&pfp=Speakers (FiberConnect 2026 speakers)
- https://www.ntca.org/events (NTCA Rural Telecom)
- https://www.scte.org/events/ (SCTE/ISBE cable/broadband)
- https://www.datacenterworld.com/ (DCW exhibitors)
- https://www.supercomputing.org/ (SC conference)
- https://wispapalooza.com/ (WISPA fixed wireless ISPs — exhibitors and sponsors)
- https://www.mwcbarcelona.com/exhibitors (MWC — mobile/wireless/network gear buyers)
- https://www.connectedamericaforum.com/ (Connected America — broadband operators and rural ISPs)
- https://www.ntca.org/ruraltelecongress (NTCA Rural Telecom Congress exhibitors)

For each source, extract:
- Company name
- What they announced / why they're notable
- Signal type: NEW_BUILD | M&A | LEADERSHIP_CHANGE | FUNDING | NEW_ENTRANT | DATA_CENTER | AI_INFRA | TRADE_SHOW_PRESENCE | FIXED_WIRELESS | RURAL_BROADBAND

---

## STEP 3 — HUBSPOT CROSS-REFERENCE

For each UNIQUE company name found in Step 2, search HubSpot to determine ownership status:
- Use the HubSpot MCP (portal ID: 21878985) search_crm_objects for "companies"
- Search by company name
- Label each: MY_ACCOUNT (Brian owns it, owner ID 213536174) | OTHER_REP | UNOWNED | GREENFIELD (not in HubSpot at all)

Focus on GREENFIELD and UNOWNED — these are the highest-value targets.

---

## STEP 4 — SCORE AND RANK

Score each company 1-10 for OSI fit:
- +3 if they're building new fiber infrastructure (needs optics/switches)
- +3 if they're a data center or AI infrastructure company (needs servers/storage/optics)
- +2 if they had M&A activity (hardware refresh cycle likely)
- +2 if they're a CLEC, ILEC, ISP, WISP, or telecom operator
- +1 if they had a leadership change (new buyers)
- +1 if GREENFIELD or UNOWNED in HubSpot
- +1 if they're a trade show exhibitor or speaker (actively spending budget)

---

## STEP 5 — BUILD THE WORD DOC

Create a Word doc named: `Intel_Brief_[YYYY-MM-DD].docx`
Save to: `C:\Users\Mini\Documents\osi-claude-brain\sessions\intel-briefs\`

Structure:
```
OSI GLOBAL — WEEKLY INTEL BRIEF
Week of [date] | Prepared for Brian Charrette

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 TOP GREENFIELD TARGETS THIS WEEK
━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Top 5-10 companies scored 7+, GREENFIELD/UNOWNED, with: company name, signal, why OSI fits, suggested angle]

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 FIBER & BROADBAND BUILDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━
[New network builds, expansions, BEAD deployments — company, region, scale, HubSpot status]

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤝 M&A ACTIVITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Mergers/acquisitions — who acquired whom, HubSpot status of both, timing]

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏢 DATA CENTER & AI INFRA
━━━━━━━━━━━━━━━━━━━━━━━━━━━
[New DC announcements, AI infrastructure builds, colocation expansions]

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📶 FIXED WIRELESS & RURAL BROADBAND
━━━━━━━━━━━━━━━━━━━━━━━━━━━
[WISPs, rural operators, BEAD-funded builds — WISPAPALOOZA + Connected America intel]

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎤 TRADE SHOW INTEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Notable companies/speakers at FiberConnect 2026, WISPAPALOOZA, Connected America, NTCA, SCTE, MWC, DCW — HubSpot status, suggested action]

━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 LEADERSHIP CHANGES
━━━━━━━━━━━━━━━━━━━━━━━━━━━
[New CTO/IT Director/VP hires at relevant companies — warm outreach window]

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 THIS WEEK'S ACTION ITEMS
━━━━━━━━━━━━━━━━━━━━━━━━━━━
[3-5 specific actions: "Add [Company] to HubSpot and run sequence — GREENFIELD fiber operator in [state]"]
```

---

## STEP 6 — HUBSPOT TASKS (optional, if top targets found)

For any GREENFIELD company scoring 8+, create a HubSpot task for Brian:
- Task type: TODO
- Subject: "Intel Brief — Prospect [Company Name] | [signal]"
- Due: 3 business days from today
- Owner: 213536174
- Note: paste the key signal and suggested outreach angle

---

## OUTPUT
- Confirm the Word doc was saved with a link
- List the top 3 greenfield targets found this week with one-line summaries