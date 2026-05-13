---
name: bc-greenfield-screening
description: |
  Screen broadband, telecom, and infrastructure companies for greenfield prospects (unowned in HubSpot) and OSI fit. Takes a list or URL of companies, cross-references HubSpot ownership, researches each via web + news + projects, scores by Tier (Size + OSI fit + project phase + growth rate), and outputs a markdown report with key signals and suggested outreach angles. Auto-creates HubSpot contacts and LinkedIn connection request tasks for Tier 1 accounts. ALWAYS use this skill when Brian says "screen these companies", "greenfield screening", "check these accounts", "find prospects from this list", or pastes a company list/URL and wants to identify unowned accounts that fit OSI's ICP for broadband utilities, fiber operators, or infrastructure projects.
---

# bc-greenfield-screening

Screen a list of companies for greenfield prospects (unowned in HubSpot) and rank them by OSI fit. Combines HubSpot ownership verification, deep web research, and automated HubSpot contact/task creation.

## Workflow

### Phase 1 — Parse Input & HubSpot Baseline

1. Accept input as: markdown list, URL (extract company names), or pasted text
2. For each company, search HubSpot: `search_crm_objects` on `companies` with companyName filter
3. Record: HubSpot status (owned/unowned), owner if owned, existing contacts, recent activity
4. Flag unowned accounts as greenfield candidates

### Phase 2 — Deep Research (Web, News, Projects)

For each greenfield company:

1. **Web research** — Run targeted web searches for:
   - Company + "broadband expansion" / "fiber" / "FTTH" / "grant"
   - Company + "network infrastructure" / "IT modernization"
   - Company + latest news (SEC filings if public, recent press releases)
   
2. **Project signals** — Look for:
   - FCC broadband grant awards (BEAD, Emergency Broadband Fund, etc.)
   - Fiber-to-home (FTTH) rollout phases and timelines
   - Network modernization initiatives (5G, 802.11ax, cloud migration)
   - Data center expansion, disaster recovery upgrades
   - Equipment refresh cycles (routers, switches, optical)
   
3. **Growth indicators**:
   - Employee count growth (LinkedIn, web search)
   - Revenue trends (if public)
   - New service announcements
   - Partnership news (infrastructure vendors like Cisco, Juniper, Dell, Aruba, Fortinet, Nokia)

### Phase 3 — OSI Fit Scoring

Tier assignment combines four factors:

**Size (Company Revenue / Employee Count)**
- Tier 1: $50M+ annual revenue OR 500+ employees
- Tier 2: $10–50M OR 100–500 employees
- Tier 3: <$10M OR <100 employees

**OSI Fit (Relevance to OSI's Optics/Infrastructure Stack)**
- Tier 1: Active fiber/broadband/telecom operations; buying optics, memory, servers, networking gear
- Tier 2: Infrastructure-heavy but not primary tech buyer; potential future customer
- Tier 3: Limited infrastructure spend or non-technical focus

**Project Phase (Maturity of Current Initiatives)**
- Tier 1: Active build-out, funded grants, active RFP phase (Phases 2–3 in rollout)
- Tier 2: Planning or early-phase deployment (Phase 1 or concept)
- Tier 3: Early-stage or dormant projects

**Growth Rate (Expansion Momentum)**
- Tier 1: 20%+ YoY growth or major new initiative announced
- Tier 2: 5–20% growth or modest expansion plan
- Tier 3: Flat or negative growth

**Tier 1 = Meet ALL four factors at Tier 1 level**  
**Tier 2 = At least 3 of 4 at Tier 1 OR majority at Tier 2**  
**Tier 3 = Remainder**

### Phase 4 — Markdown Report

Generate report with this structure:

```markdown
# Greenfield Screening Report
**Date:** [Today]
**Total Companies Analyzed:** [N]
**Greenfield (Unowned):** [N]
**Tier 1 Prospects:** [N]

## Tier 1 Prospects (Ready for Outreach)

### [Company Name]
- **Size:** [Employee count, Revenue]
- **HubSpot Status:** Unowned
- **Project Phase:** [FTTH Phase 2 / Fiber Expansion / Network Modernization, etc.]
- **Key Signals:**
  - [Grant award: $X million, awarded [date]]
  - [Timeline: Phases 1-2 complete, Phases 3-4 active]
  - [Technology stack: Cisco/Juniper core, looking for optics supplier]
  - [Growth rate: 25% YoY expansion]
- **OSI Fit:** [Why OSI should win — e.g., "FTTH operator in active expansion; high optics demand during Phase 3 rollout; non-traditional vendor preferred"]
- **Suggested Outreach:**
  - **Angle:** [e.g., "Smart optics supply chain during fiber rollout" OR "Third-party maintenance alternative to incumbent vendor"]
  - **Key Contacts to Target:** [Titles: CIO, VP of Network, Director of Infrastructure, etc.]
  - **Timing:** [Immediate / 90 days / as-needed]

---

## Tier 2 Prospects (Monitor, Outreach in 6 Months)

[Same format, brief]

---

## Tier 3 Prospects (Lower Priority)

[Bulleted list]

---

## Owned Accounts (Excluded)

[List of companies already owned, by rep]

---

## Key Takeaways
- [Highest-priority leads and why]
- [Market trends: e.g., "Grant-funded FTTH ops dominating this list; high buyer intent for Q2–Q3"]
- [Recommended next steps]
```

### Phase 5 — HubSpot Contact & Task Creation

For each Tier 1 company:

1. **Find decision-makers** via web/LinkedIn: CIO, VP of Network/Infrastructure, Director of IT, Network Architect
2. **Create company record** in HubSpot if missing (with industry, size, website, phone)
3. **Create contact records** for 2–3 top decision-makers:
   - Name, title, email (inferred or researched)
   - Assign to Brian (hubspot_owner_id: 213536174)
   - Lifecycle stage: Lead
   - Association: Link to company
4. **Create HubSpot task** for each Tier 1 contact:
   - Task subject: "bc-greenfield-screening: [Name] at [Company] — [Outreach Angle]"
   - Task description: Include the LinkedIn connection message script (tailored to their role and OSI fit)
   - Due date: 3 business days
   - Assigned to: Brian
   - Associated with: Contact + Company

## Why This Workflow

OSI's edge is identifying high-signal prospects early — before competitors surface them, before they've closed on vendors. This skill automates the research grind: it screens 50–100 companies, surfaces the Tier 1s that are actually ready to buy, and dumps them into HubSpot with pre-written LinkedIn scripts. Brian walks in with his next 3–5 target accounts ready to pursue.

## Error Handling

- **Company not found on web:** Still include in report, note as "unverified" or "limited signals"
- **HubSpot search returns no match:** Create new company record
- **Email address not found:** Use inferred format (firstname@company.com) or note as "research required"
- **Project signals unclear:** Flag as "early-stage" rather than omitting; better to research than ignore
- **Owned account:** Log the owner and skip outreach task creation

## Output Files

1. **Markdown report** — saved to `/sessions/[user]/mnt/outputs/bc-greenfield-screening-[date].md`
2. **HubSpot updates** — new contacts created, tasks assigned to Brian
3. **Summary message** — 3-line recap: # prospects screened, # greenfield, # Tier 1, next steps
