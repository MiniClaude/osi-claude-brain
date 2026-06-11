---
name: bc-account-enrichment
description: Deep-dive enrichment on a single OSI Global account using ZoomInfo + HubSpot + LinkedIn Sales Navigator. Produces a Word doc intel report, auto-adds new decision-maker contacts to HubSpot, and creates outreach tasks for the hottest new connections. ALWAYS use this skill when Brian says anything like "enrich [company]", "deep dive on [account]", "run bc-account-enrichment on [X]", "pull everything on [account]", "full workup on [company]", "who's new at [account]", "give me the full picture on [X]", "LI Sales Nav pull on [company]", "rebuild my view of [account]", or any variation of wanting a single-account intel package before outreach, a meeting, a QBR, or strategic planning. Triggers on ANY request to go deep on one named account — even if Brian doesn't explicitly say "enrichment."
---

# bc-account-enrichment

Single-account deep-dive enrichment combining ZoomInfo (ZI) intent/news/scoops, HubSpot (HS) history, and LinkedIn Sales Navigator (LI) for decision-makers and job changes. Outputs a Word doc report and auto-updates HubSpot with new contacts and outreach tasks.

## When to use

Use whenever Brian asks for the full picture on one specific named account. This is the deep-dive version of `account-enrichment` (which pulls 5 dormant accounts at a surface level). The trade-off is depth for volume — this skill takes longer but gives Brian everything he needs for a meeting, QBR, or strategic push on a single target.

Do not use for:
- Running multiple accounts at once → use `account-enrichment` instead
- Qualifying a single LinkedIn profile → use `bc-prospect-qualification`
- Writing outreach after enrichment → hand off to `osi-outreach-7email` or `bc-7email-custom` after this skill completes

## Inputs

One of:
- Company name (e.g., "Smithsonian Institution")
- HubSpot company ID
- Company website/domain

If Brian gives an ambiguous name (e.g., "Southwest"), ask which one before proceeding.

## Workflow

Run these phases in order. Each one feeds the next. When something fails (ZI parameter error, LI rate limit, missing contact in HS), note it and keep going — don't halt the whole workflow.

### Phase 1 — HubSpot baseline

Pull everything OSI already knows about the account:

1. Search HubSpot for the company using `mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__search_crm_objects`. Filter on company name or domain.
2. Grab the company record with all relevant properties: lifecycle stage, owner, industry, annual revenue, employee count, created date, last activity date, domain, phone, address.
3. Pull all associated contacts. For each contact: name, title, email, phone, lifecycle stage, last contacted, HS owner.
4. Pull all associated deals. For each deal: name, amount, iqmargin (GP), stage, close date, pipeline, dealstage reason, client_id__cv_name_.
5. Pull recent notes, calls, meetings, emails logged on the company and contacts — last 12 months.
6. Note who the OSI owner is. If it's Brian (ownerId 213536174) or Adam Cooney — flag the account as "Bri & Adam Biz." If it's another rep, flag that and still proceed (Brian may be prepping for a team play).

Save this as the HubSpot baseline — the report leads with it so Brian sees our existing footprint first.

### Phase 2 — ZoomInfo enrichment

Fill in the gaps ZI knows that HubSpot doesn't:

1. `search_companies` to get the ZoomInfo company ID. Use `companyName` + `companyWebsite` for accuracy.
2. `account_research` for a broad orientation pass — use a query like *"User is running deep enrichment on this account for OSI Global sales. Give me current strategic posture, recent initiatives, tech stack, IT priorities, buying signals, and anything that's changed in the last 6 months."*
3. `enrich_news` — last 90 days of company news. Filter on technology, infrastructure, hiring, layoffs, funding, acquisitions.
4. `enrich_scoops` — ZI's analyst-verified project signals (refresh projects, new data centers, cloud migrations, security initiatives).
5. `enrich_intent` — surging topics the account is researching. Focus on OSI-relevant topics: *networking hardware, optical transceivers, DWDM, third-party maintenance, data center, Cisco, Juniper, Aruba, Dell servers, HPE, Smartoptics, colocation, memory upgrades, end-of-life*.
6. `search_contacts` on the company for decision-makers by management level and department:
   - Management levels: `C Level Exec`, `VP Level Exec`, `Director`, `Manager`
   - Departments: IT, Engineering, Operations
   - Return up to 50 contacts. Prioritize these titles: CIO, CTO, VP/Dir of Infrastructure, VP/Dir of Networking, VP/Dir of Data Center, Network Architect, Network Engineer, Sr. Network Engineer, Systems Architect, IT Operations, Manager of Network Operations.

If any ZI call fails with a parameter error, use `lookup` to get the valid field values, then retry. Don't give up on ZI data — it's the backbone of this skill.

### Phase 3 — LinkedIn Sales Navigator pull (Chrome automation)

Sales Nav is the only way to get real-time decision-maker lists, recent hires, job changes, and mutual connections. Brian has to be logged in — if Chrome navigates to a login page, stop and tell him to log in first.

Run these four sub-pulls via Claude in Chrome. Use `browser_batch` where possible to reduce round trips.

**3a. Decision-makers by role** — Sales Nav Lead Search at the company. Filter:
- Current Company: [the account]
- Function: Information Technology, Engineering, Operations
- Seniority: Manager, Director, VP, CXO
- Geography: matches account footprint
- Title keywords: network, infrastructure, data center, architecture, systems, security, cloud, IT

Scrape up to 50 leads. Capture name, title, location, current tenure, LinkedIn URL, connection degree (1st/2nd/3rd+).

**3b. Recent hires (last 90 days)** — Sales Nav Lead Search with same company filter + "Past 90 days" tenure filter. These are the people reshaping the stack. Capture the same fields as 3a, plus previous company.

**3c. Job changes (last 6 months)** — Sales Nav has a "changed jobs" filter at the Account level. Also cross-reference the contacts from HubSpot (Phase 1) — search each one on LinkedIn and check if they still show the account as current employer. Flag anyone who left (departed champion = outreach opportunity at their new company). Flag anyone new to the account from somewhere else (potential warm intro via their prior employer).

**3d. Mutual connections + 1st-degree at the account** — Search the company page's "People" tab filtered to 1st-degree connections. These are warm paths. For each 1st-degree connection at the account, capture name, title, how you know each other if visible (shared company, school, group).

### Phase 4 — Cross-reference and score

Merge the three data sources:

1. **HubSpot ∩ ZoomInfo ∩ LinkedIn** — contacts who exist in all three. These are our best-known people. No action needed.
2. **LinkedIn/ZI ∩ NOT HubSpot** — decision-makers or recent hires who aren't in our CRM. These are the top priorities to add.
3. **HubSpot ∩ NOT LinkedIn (still current)** — contacts in HS who no longer show the account on LI. These have likely left. Flag for "job change" outreach at their new company.
4. **1st-degree LI connections ∩ NOT HubSpot** — warm paths we haven't captured. Highest-priority adds.

Score each new contact on a simple 1–10 heat scale:
- Title fit to OSI ICP (Network/Infra/DC/CIO/CTO): +3
- Recent hire (<90 days): +2
- 1st-degree connection: +3
- Job change in last 6 months: +1
- Present in ZI with verified work email: +1

Top 3–5 highest-scored new contacts become the outreach tasks in Phase 6.

### Phase 5 — Generate Word doc report

Use the `docx` skill to build the report. Save to `/sessions/blissful-magical-hawking/mnt/Technical Projects/bc-enrichment-[company-slug]-[YYYY-MM-DD].docx`.

Follow this exact structure:

```
# [Company Name] — OSI Global Account Intel
**Generated:** [Date]
**OSI Owner:** [Owner name + note if Bri & Adam Biz]

## 1. Executive Summary
3-5 sentence plain-language take. What's the state of the relationship, what's changed, and what should Brian do next.

## 2. OSI Footprint (HubSpot)
- Deal history table (name, amount, iqmargin, stage, close date)
- Contact history table (name, title, last contacted, owner)
- Total GP to date, last activity date, lifecycle stage
- Recent notes/calls summary (last 12 months, chronological)

## 3. Account Signals (ZoomInfo)
- **Strategic posture:** synthesis from account_research
- **Recent news** (last 90 days): bulleted headlines with dates
- **Analyst scoops:** verified project signals
- **Intent topics surging:** OSI-relevant topics the account is researching

## 4. Decision-Makers (LinkedIn Sales Navigator)
Table: Name | Title | Tenure | LI Degree | In HubSpot? | Heat Score

## 5. Recent Hires (Last 90 Days)
Table: Name | Title | Previous Company | Start Date | LI URL

## 6. Job Changes (Last 6 Months)
- **Departed champions** (left the account): name, old title, new company, new title
- **New arrivals from known employers** (warm intro opportunities)

## 7. Warm Paths — 1st-Degree Connections
List every 1st-degree connection at the account with their title and any visible relationship context.

## 8. Recommended Plays
Top 3–5 highest-scored new contacts — the ones HubSpot tasks will be created for. Brief rationale for each. Suggested angle (Systain TPM, Smartoptics optics, memory upgrade, hardware refresh alternative, etc.).

## 9. Gaps and Open Questions
What we don't know. What to verify on the next call. Anything ZI/LI didn't reveal.

## 10. Appendix — Raw Data Summary
Counts: # ZI contacts, # LI leads pulled, # HS contacts, # deals, # new contacts added to HS, # tasks created.
```

### Phase 6 — HubSpot updates and tasks

Auto-create the following in HubSpot. Use `manage_crm_objects` and require user confirmation per its tool guidance (the tool will prompt).

1. **New contact records** — for every LinkedIn/ZI decision-maker who isn't in HubSpot and has a verifiable work email. Required fields: firstname, lastname, email, jobtitle, hubspot_owner_id (Brian's: 213536174), lifecyclestage=lead, plus the company association.
2. **Outreach tasks** — one task for each of the top 3–5 new contacts from Phase 4 scoring. Task subject: *"bc-account-enrichment: reach out to [Name] at [Company] — [angle]"*. Due in 3 business days. Assigned to Brian.
3. **Company record update** — update last_enrichment_date (or add a note if that property doesn't exist) with today's date and a link reference to the generated Word doc.

Confirm all CRM writes in a batch before executing. Brian can say "yes" or "skip tasks" or list specific names.

## Output

1. **Word doc report** in `/sessions/blissful-magical-hawking/mnt/Technical Projects/` — linked with `computer://` URL so Brian can open directly.
2. **HubSpot updates** — new contacts added, tasks created, company record updated.
3. **Summary message** — 5-line recap: account name, OSI GP history, # new contacts added, # tasks created, file link.

## Why this skill matters

OSI's edge is relationship depth — we show up, own the problem, finish the job. That only works if Brian walks into a meeting with a full picture. This skill compresses what would be 2–3 hours of manual research across three platforms into a structured, repeatable workflow that feeds straight into HubSpot and produces a doc Brian can actually use.

## Error handling

- **ZoomInfo parameter errors** — use `lookup` with fieldName to get valid values, retry.
- **LinkedIn login required** — stop Phase 3, tell Brian to log in, resume from Phase 3a when he confirms.
- **Sales Nav rate limits** — LinkedIn throttles aggressive scraping. If a page shows a rate-limit message, pause 30–60 seconds and retry once. If it hits again, note the partial data in the report and continue.
- **HubSpot company not found** — ask Brian if he wants a new company record created, or if he wants to proceed with ZI + LI only.
- **Contact lookup returns no email** — still add to the report, but skip creating the HubSpot contact (we need a verified work email to add).

## References

- `references/linkedin-sales-nav-playbook.md` — URL patterns, filter config, scrape strategy
- `references/zoominfo-params.md` — valid field values that commonly trip up ZI calls
- `references/hubspot-properties.md` — OSI-specific property names (iqmargin, client_id__cv_name_, etc.) and owner IDs
- `references/report-template.md` — full Word doc structure with formatting notes
