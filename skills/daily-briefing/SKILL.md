---
name: daily-briefing
description: Generate a morning sales briefing for any OSI Global rep. Takes a rep name, pulls their full pipeline and recent wins from HubSpot, checks Outlook email activity, and delivers a formatted Word document. Trigger with "morning briefing for [rep name]", "daily brief for [rep]", "prep [rep]'s day", or "start [rep]'s day".
---

# OSI Global — Daily Sales Briefing

Generate a consistent, high-quality morning briefing for any OSI Global sales rep. This skill follows a deterministic workflow against HubSpot CRM and Microsoft Outlook to produce a formatted Word document (.docx) every time.

## Required Input

A rep name. Examples:
- "morning briefing for Nicole Severson"
- "daily brief for Brian Charrette"
- "prep Nicole's day"

If no rep name is provided, ask: "Which rep would you like the morning briefing for?"

---

## Execution Flow — Follow These Steps Exactly

### Step 1: Look Up the Rep in HubSpot

Use `search_owners` with the rep's name.

```
search_owners({ searchQuery: "[rep name]" })
```

Record the `ownerId`. This is the key for all subsequent CRM queries. If no match is found, try a partial name or ask the user to confirm how the name appears in HubSpot.

### Step 2: Pull Open Pipeline (All Active Deals)

Use `search_crm_objects` to get all deals owned by this rep that are NOT closed-won or closed-lost.

```
search_crm_objects({
  objectType: "deals",
  filterGroups: [{
    filters: [
      { propertyName: "hubspot_owner_id", operator: "EQ", value: "[ownerId]" },
      { propertyName: "dealstage", operator: "NOT_IN", values: ["closedwon", "closedlost"] }
    ]
  }],
  properties: ["dealname", "dealstage", "amount", "closedate", "pipeline",
               "hs_lastmodifieddate", "notes_last_updated", "hs_next_step",
               "hubspot_owner_id", "hs_deal_stage_probability"],
  sorts: [{ propertyName: "closedate", direction: "ASCENDING" }],
  limit: 100
})
```

If `total` exceeds the limit, paginate using `offset` to retrieve ALL open deals. Do not present partial data.

### Step 3: Pull Recent Wins (Closed-Won This Year)

```
search_crm_objects({
  objectType: "deals",
  filterGroups: [{
    filters: [
      { propertyName: "hubspot_owner_id", operator: "EQ", value: "[ownerId]" },
      { propertyName: "dealstage", operator: "EQ", value: "closedwon" },
      { propertyName: "closedate", operator: "GTE", value: "[current-year]-01-01" }
    ]
  }],
  properties: ["dealname", "dealstage", "amount", "closedate", "hs_lastmodifieddate"],
  sorts: [{ propertyName: "closedate", direction: "DESCENDING" }],
  limit: 20
})
```

### Step 4: Check Outlook Email Activity

```
outlook_email_search({
  query: "[rep full name]",
  afterDateTime: "[7 days ago]",
  limit: 15
})
```

Note any HubSpot deal notifications, manager check-ins, and deal-related correspondence.

### IMPORTANT: Run Steps 2, 3, and 4 in Parallel

Fire all three queries simultaneously to minimize latency. Do NOT run them sequentially.

---

## Analysis Rules

### Step 5: Categorize Deals

Organize open deals into these time-based buckets:

| Bucket | Rule |
|--------|------|
| **Closing This Week** | Close date within next 7 calendar days |
| **Closing Next 2 Weeks** | Close date 8-14 days out |
| **Closing Later This Month** | Close date in remainder of current month |
| **Big Deal Watch** | Close date next month, especially deals over $25K |

### Step 6: Flag Pipeline Alerts

| Condition | Severity | Label |
|-----------|----------|-------|
| Close date has PASSED (deal still open) | RED | "Close date passed ([date])" |
| No close date + stage is Contract Sent or later | ORANGE | "Contract sent, no close date" |
| No close date + amount > $25K | ORANGE | "No close date, [stage]" |
| Early stage (10% prob) + no close date + large amount | ORANGE | "No close date, 10% stage" |

### Step 7: Calculate Summary Stats

| Stat | Calculation |
|------|-------------|
| **Open Pipeline** | Sum of `amount` across all open deals |
| **Open Deals** | Count of open deals |
| **Closing This Month** | Sum of `amount` for deals with close dates in current month |
| **Won This Month** | Sum of `amount` for deals closed-won in current calendar month |

### Step 8: Determine #1 Priority

Apply this ranking to select the single most important action:

1. **URGENT**: Deal closing today or tomorrow — confirm PO / clear blockers
2. **HIGH**: Deal closing this week at 60%+ probability — push to close
3. **HIGH**: Large deal ($25K+) with notes updated in last 48 hours — maintain momentum
4. **MEDIUM**: Contract sent with no close date — follow up for signature timeline
5. **MEDIUM**: Deal with close date that has passed — clean up or re-commit
6. **LOW**: Largest deal by amount regardless of timeline — keep it on track

### Step 9: Generate 5 Suggested Actions

Each action must name the specific deal, explain what to do, and state why now. Prioritize by urgency and dollar value.

---

## Output: Word Document (.docx)

CRITICAL: The output MUST be a Word document. Use the `docx` npm package (install locally with `npm install docx` if needed).

### Document Sections (in this exact order)

1. **Header** — "Good Morning, [Rep First Name]" + date line
2. **#1 Priority Banner** — Orange-highlighted box with the most urgent action
3. **Stats Row** — 4-column layout: Open Pipeline | Open Deals | Closing This Month | Won This Month
4. **Closing This Week** — Table: Deal, Amount, Stage, Close Date, Action
5. **Closing Next 2 Weeks** — Table: Deal, Amount, Stage, Close Date
6. **Closing Later This Month** — Table: Deal, Amount, Stage, Close Date
7. **Big Deal Watch** — Table for next month + note about the largest opportunity
8. **Pipeline Alerts** — Table: Deal, Amount, Alert (color-coded), Action
9. **Recent Wins** — Table: Deal, Amount, Closed date + YTD wins note
10. **Suggested Actions** — Numbered list of 5 actions with rationale

### Formatting Specifications

| Property | Value |
|----------|-------|
| Page size | US Letter: 12240 x 15840 DXA |
| Margins | 1 inch all sides (1440 DXA) |
| Font | Arial throughout |
| Default text size | 12pt (size: 24 in docx-js) |
| Title size | 20pt (size: 40) |
| Section header size | 13pt (size: 26) |
| Table header | Bold, white text on dark background (#2D3436) |
| Table text | 10pt (size: 20) |

### Color Scheme

| Element | Color |
|---------|-------|
| Headers / accents | Blue #0984E3 |
| "Decision Maker" stage | Purple #6C5CE7 |
| "Contract Sent" stage | Blue #0984E3 |
| "Qualified to Buy" stage | Orange #E17055 |
| Wins / positive stats | Green #00B894 |
| Warnings | Orange #E17055 |
| Critical alerts | Red #D63031 |
| Alert row background | #FFF8F0 |
| Stats background | #F5F6FA |
| Body text | Dark #2D3436 |
| Secondary text | Gray #636E72 |

### Page Header/Footer

- Header (right-aligned, italic, gray): "OSI Global — Sales Briefing"
- Footer (centered): "Page [N]"

### File Naming and Location

File name: `[Rep_First]_[Rep_Last]_Briefing_[YYYY-MM-DD].docx`

Save to the workspace output folder so the user can access it immediately.

---

## OSI Global Reference Data

### HubSpot Portal

Portal ID: **21878985**

Deal URL pattern:
```
https://app.hubspot.com/contacts/21878985/record/0-3/[deal_id]
```

Include a clickable HubSpot link for every deal mentioned in the briefing.

### Deal Stage Mapping

| Stage ID | Display Name | Probability |
|----------|-------------|-------------|
| qualifiedtobuy | Qualified to Buy | 10% |
| contractsent | Contract Sent | 60% |
| 31940385 | Decision Maker | 80% |
| closedwon | Closed Won | 100% |
| closedlost | Closed Lost | 0% |

If you encounter a stage ID not in this table, display the raw ID and flag it.

---

## What NOT To Do

- Do NOT search ZoomInfo, Apollo, Clay, or other enrichment tools for rep information. The rep is an internal OSI employee — always look them up via HubSpot `search_owners`.
- Do NOT ask the user for meetings, deals, or pipeline info. Pull everything from HubSpot and Outlook automatically.
- Do NOT output as HTML, Markdown, or plain text. Always produce a .docx Word document.
- Do NOT present partial pipeline data. If total exceeds query limit, paginate to get all records.
- Do NOT skip the stats calculations. Always compute and display the four summary numbers.
- Do NOT use web search to find the rep. They are in HubSpot.

---

## Quick Mode

If the user says "quick brief for [rep]" or "tldr [rep]", produce an abbreviated text version (no Word doc):

```
# Quick Brief | [Rep Name] | [Date]

#1: [Priority action]
Pipeline: $[X] open across [N] deals
Closing this month: $[X]
Won this month: $[X]

Alerts:
- [Alert 1]
- [Alert 2]

Do Now: [Single most important action]
```

## End of Day Mode

If the user says "wrap up [rep]'s day" or "end of day for [rep]":

1. Pull deals modified today (hs_lastmodifieddate = today)
2. Check for new closed-won deals today
3. Summarize pipeline changes and suggest tomorrow's focus
4. Output as text in conversation (no Word doc)

---

## Related Skills

- **call-prep** — Deep meeting preparation for a specific call
- **call-summary** — Process notes after calls
- **account-research** — Research a company before first meeting
- **pipeline-review** — Full pipeline health analysis across all deals
