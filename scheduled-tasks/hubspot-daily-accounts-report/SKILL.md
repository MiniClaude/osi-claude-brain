---
name: hubspot-daily-accounts-report
description: Rebuild the 10-tab Brian_HubSpot_Accounts.xlsx from HubSpot data every night at midnight
---

You are rebuilding a multi-tab Excel report for Brian Cosi at OSI Global IT. Your goal is to pull fresh data from HubSpot and write a complete, up-to-date spreadsheet to:

C:\Users\MINI OSI RIG\OneDrive - OSI Hardware\Documents\Claude\Projects\Daily Accounts\Brian_HubSpot_Accounts.xlsx

**HubSpot credentials:**
- Owner ID: 213536174
- Account/Portal ID: 21878985
- Use the HubSpot MCP (mcp__673387d1-50bc-483b-9636-bb1020757258) for all CRM queries.

**Use the xlsx skill** to build the spreadsheet. Read /sessions/[current-session]/mnt/.claude/skills/xlsx/SKILL.md before writing any code.

---

## The Tabs to Build

**Tab  – No Deal History**
Query all HubSpot company records owned by Owner ID 213536174 that have NEVER had a deal or order. Paginate through all results. Columns: Company Name, Website, Last Activity Date, Headcount, City, State, Country, HubSpot Company ID.

**Tab  – No Activity Ever**
From Brian's owned accounts, find companies with zero logged activity (no emails, calls, meetings, or notes ever recorded). Columns: Company Name, Website, Create Date, Headcount, City, State.

**Tab  – Customers**
All owned accounts that have at least one closed-won deal or any deal history. Sort by number of deals descending. Columns: Company Name, Website, Deal Count, Total Deal Value, Last Activity Date, Headcount.

**Tab  – ZoomInfo Intent**
Use the Systain/enrichment MCP (mcp__90689f47-cc2b-40ac-a66a-4d20181db673) to search for intent signals on Brian's owned accounts using search_intent. Focus on telecom, networking, IT infrastructure, hardware topics. If the intent API returns no results, fall back to listing Brian's highest-engagement CRM accounts (most recent activity, most deals) as a proxy. Columns: Company Name, Website, Intent Topic, Intent Score/Signal, Last Activity.

**Tab  – Company News**
Use WebSearch to research the top 25 most notable companies in Brian's owned accounts. Search for recent news (mergers, acquisitions, IT projects, growth, layoffs). Write a 2–3 sentence summary per company. Columns: Company Name, Website, News Summary, Source URL.

**Tab  – High-Growth Not in CRM**
Use WebSearch to identify fast-growing companies any verticle  make sure to include telecom, networking, data center, AI or IT infrastructure sectors that are NOT already in Brian's HubSpot ID 213536174. Good targets: AI infrastructure companies, hyperscalers, defense tech, large network operators. Provide 50 companies. Columns: Company Name, Website, Why They're Interesting, Estimated Size.

**Tab – Follow-Up Plan**
Query HubSpot contacts enrolled in sequences named "__BC Telecom MASTER 2025"  if they have replied to emails with subject "RE: Confirming address".  Generate a list of these contacts

**Tab  – Open Deals**
All open (non-closed) deals owned by Owner ID 213536174. Sort by deal value descending. Columns: Deal Name, Company, Deal Stage, Amount, Close Date, Create Date, HubSpot Deal ID.



---

## Output requirements
- Use the xlsx skill (openpyxl) to write the file.
- Each tab should have a bold header row, frozen top row, and auto-fit column widths.
- Save the file to the exact path above, overwriting any existing file.
- After saving, confirm success and summarize row counts for each tab.
- If HubSpot pagination is needed, use after/offset parameters to fetch ALL records (not just first page).