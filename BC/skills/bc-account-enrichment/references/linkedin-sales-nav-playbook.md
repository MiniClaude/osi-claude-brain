# LinkedIn Sales Navigator Playbook

How to pull decision-makers, recent hires, job changes, and mutual connections from Sales Navigator via Claude in Chrome automation.

## Prerequisites

- Brian must be logged into Sales Navigator (sales.linkedin.com) in Chrome.
- Use `mcp__Claude_in_Chrome__tabs_context_mcp` first to find or create a tab.
- Prefer `browser_batch` to chain navigate → find → scrape in one round trip.

## URL patterns

### Account search (starting point for a single company)
`https://www.linkedin.com/sales/search/company?query=(keywords:[COMPANY_NAME_URL_ENCODED])`

### Account page (after selecting a company)
`https://www.linkedin.com/sales/company/[COMPANY_SALES_NAV_ID]`

### Lead search filtered to a company with role + seniority filters
Build the URL by applying filters in the UI first, then capture the URL. Example structure:
```
https://www.linkedin.com/sales/search/people?query=(filters:List(
  (type:CURRENT_COMPANY,values:List((id:[COMPANY_ID],selectionType:INCLUDED))),
  (type:FUNCTION,values:List((id:13,selectionType:INCLUDED),(id:25,selectionType:INCLUDED))),
  (type:SENIORITY_LEVEL,values:List((id:130,selectionType:INCLUDED),(id:120,selectionType:INCLUDED)))
))
```

LinkedIn changes filter IDs periodically. Safer approach: navigate to the company, click "Show all people at [Company]", then apply filters interactively via the `find` + `computer` tools, then scrape the result URL.

## Filter reference

### Seniority (most common for OSI targets)
- CXO (C-suite)
- VP
- Director
- Manager
- Senior (individual contributor, stop here — below this is noise)

### Function
- Information Technology
- Engineering
- Operations

### Title keywords (use the "Current title" field, OR-joined)
- network
- infrastructure
- data center
- architect / architecture
- systems
- security
- cloud
- IT
- telecommunications

### Tenure at current company (for recent hires)
- Less than 1 year → filters to <12 months
- For 90-day pulls, apply "Less than 1 year" and manually filter by start date in scrape logic

## Scrape strategy

Lead search results show ~25 per page. For each result card, extract:
- Full name
- Current title
- Company
- Location
- Years at current company (shown as "X yrs Y mos" or "Joined [month] [year]")
- Connection degree (1st, 2nd, 3rd+) — critical for warm path scoring
- LinkedIn profile URL

Use `get_page_text` for a first pass. If the text view loses structure, fall back to `read_page` with `filter: "interactive"` to grab the anchor tags, then pair with the text.

**Pagination:** click "Next" or append `&page=N` to the URL. Cap at 2 pages (50 results) unless Brian asks for more — beyond that, the data quality drops and rate limits kick in.

## Job change detection (Phase 3c)

Sales Navigator has a "Past Company" filter and a "Changed jobs in past 90 days" saved filter at the Account level. Also:

1. For each HubSpot contact (from Phase 1), search their name on LinkedIn.
2. Open their profile, check current company.
3. If current company != the account we're enriching → they left. Capture their new company, new title, date of change if visible.
4. Flag these in the report under "Departed champions."

For incoming new hires from known accounts (warm intro opportunity): check each recent hire's "Previous experience" section. If they came from an OSI customer or a company where Brian has connections, flag it.

## Mutual connections / 1st-degree

On the company page:
1. Click "People" tab.
2. Apply "1st connections" filter.
3. Scrape the resulting list — these are the warm paths.

For each 1st-degree: capture how Brian knows them if LinkedIn shows it (shared school, shared past employer, shared group). That context goes in the report.

## Rate limit handling

LinkedIn throttles aggressive scraping. Signs:
- Page shows "We've reached LinkedIn's search limit" or similar banner
- Pagination buttons disabled
- Profile loads return CAPTCHA

If any of these appear:
1. Pause 60 seconds.
2. Retry once.
3. If it hits again, note partial data in the report and stop Phase 3. Don't burn Brian's account.

## What NOT to do

- Don't scrape facial images or bulk profile photos. Compliance risk + violates the harmful_content_safety rules.
- Don't attempt to bypass CAPTCHAs. Full stop.
- Don't log into LinkedIn on Brian's behalf. He handles login.
- Don't send connection requests or InMails from this skill. Outreach is handled by separate skills.
