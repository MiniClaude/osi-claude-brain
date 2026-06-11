---
name: hubspot-account-overview-refresh
description: 3x daily refresh of Brian's HubSpot account overview spreadsheet at 6 AM, 12 PM, and 3 PM
---

Refresh the HubSpot account overview spreadsheet for sales owner Brian (HubSpot owner ID: `213536174`, portal ID: `21878985`). This spreadsheet tracks his company accounts by activity status. Only include companies where Brian is currently the owner — any accounts he has removed himself from will be automatically excluded since they no longer match the owner filter.

## Step 1: Compute the cutoff timestamp

Run the following Python to get the timestamp for exactly 1 year ago:

```python
from datetime import datetime, timedelta
cutoff_dt = datetime.now() - timedelta(days=365)
cutoff_ts = int(cutoff_dt.timestamp() * 1000)
print(cutoff_ts)
```

Use this value as `{cutoff_ts}` in all HubSpot queries below.

## Step 2: Query HubSpot data for each tab

Use the `search_crm_objects` HubSpot MCP tool for all queries. Paginate through all results (200 per page, increment offset) until you have retrieved every record.

**Tab 1 — No Order or Deal History:**
- objectType: `companies`
- Filter group 1: `hubspot_owner_id EQ 213536174` AND `recent_deal_close_date NOT_HAS_PROPERTY`
- Filter group 2: `hubspot_owner_id EQ 213536174` AND `recent_deal_close_date LT {cutoff_ts}`
- Properties: `name`, `domain`, `phone`, `recent_deal_close_date`, `recent_deal_amount`

**Tab 2 — No Activity Ever (subset of Tab 1 with zero communication):**
- Filter group 1: `hubspot_owner_id EQ 213536174` AND `recent_deal_close_date NOT_HAS_PROPERTY` AND `hs_last_logged_call_date NOT_HAS_PROPERTY` AND `notes_last_contacted NOT_HAS_PROPERTY`
- Filter group 2: `hubspot_owner_id EQ 213536174` AND `recent_deal_close_date LT {cutoff_ts}` AND `hs_last_logged_call_date NOT_HAS_PROPERTY` AND `notes_last_contacted NOT_HAS_PROPERTY`
- Properties: `name`, `domain`, `phone`, `createdate`

**Tab 3 — Accounts That Have Ordered:**
- Filter: `hubspot_owner_id EQ 213536174` AND `recent_deal_close_date GTE {cutoff_ts}`
- Properties: `name`, `domain`, `phone`, `recent_deal_close_date`, `recent_deal_amount`, `total_revenue`
- Sort by `total_revenue DESCENDING`

**Tab 4 — International (Non-USA):**
- Filter: `hubspot_owner_id EQ 213536174` AND `country HAS_PROPERTY` AND `country NEQ United States`
- Properties: `name`, `country`, `city`, `state`, `domain`, `phone`, `recent_deal_close_date`, `recent_deal_amount`
- Sort by `country ASCENDING`

HubSpot link per company: `https://app.hubspot.com/contacts/21878985/company/{id}`

## Step 3: Build the spreadsheet

Use Python with openpyxl. Find the output path dynamically:

```python
import subprocess
result = subprocess.run(['find', '/sessions', '-name', 'outputs', '-type', 'd'], capture_output=True, text=True)
output_dir = result.stdout.strip().split('\n')[0]
output_path = output_dir + '/account_overview.xlsx'
```

Build the workbook with these tabs in order:

**Tab 1 "No Order or Deal History"**
- Header fill: `1F4E79` (dark blue), white bold Arial 11pt text
- Columns: Company Name, Domain, Phone, Last Deal Closed, Last Deal Amount, HubSpot Link
- Freeze row 1, autofilter

**Tab 2 "No Activity Ever"**
- Header fill: `7B2D8B` (purple), white bold Arial 11pt text
- Columns: Company Name, Domain, Phone, Added to HubSpot, HubSpot Link
- Freeze row 1, autofilter

**Tab 3 "Accounts That Have Ordered"**
- Header fill: `B8860B` (gold), white bold Arial 11pt text
- Columns: Company Name, Domain, Phone, Last Order Date, Last Order $, Total Revenue, HubSpot Link
- Top 10 rows: bold font + gold tint fill `FFF2CC`
- Freeze row 1, autofilter

**Tab 4 "International (Non-USA)"**
- Header fill: `006B6B` (teal), white bold Arial 11pt text
- Columns: Company Name, Country, City/State, Domain, Phone, Last Order Date, Last Order $, HubSpot Link
- Sort by country then company name
- Freeze row 1, autofilter

**Summary tab**
- List each tab name, record count, and today's date

For all tabs: set column widths appropriately, HubSpot links should be clickable hyperlinks using `ws.cell(...).hyperlink`.

## Step 4: Present the file

Save to the output path and present the file to the user using `present_files` so they can open it directly.