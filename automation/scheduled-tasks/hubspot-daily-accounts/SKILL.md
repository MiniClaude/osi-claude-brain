---
name: hubspot-daily-accounts
description: 3x daily refresh of Brian's HubSpot accounts spreadsheet at 6 AM, 12 PM, and 3 PM
---

You are refreshing a HubSpot accounts spreadsheet for Brian Charrette (HubSpot owner ID: 213536174, account ID: 21878985). 

Your goal is to pull all companies Brian owns in HubSpot and produce a clean, up-to-date Excel spreadsheet saved to the workspace folder.

## Steps

### 1. Fetch all companies owned by Brian (paginate fully)
Use the HubSpot `search_crm_objects` tool with `objectType: companies` and filter `hubspot_owner_id EQ 213536174`. Request these properties: `name, domain, phone, city, state, country, num_associated_deals, num_associated_contacts, notes_last_contacted, hs_num_open_deals, createdate`. Use limit 200 and paginate through ALL results until you have fetched every record.

### 2. Categorize into 4 groups
From the complete list of companies:

- **Tab 1 – No Deal History**: Companies where `num_associated_deals` is null/missing (no deals ever).
- **Tab 2 – No Activity Ever**: Companies where `notes_last_contacted` is null/missing (never contacted by phone or email).
- **Tab 3 – Customers – All Orders**: Companies where `num_associated_deals` > 0, sorted descending by `num_associated_deals`.
- **Tab 4 – International (Non-USA)**: Companies where `country` has a value and is NOT "United States", sorted by country then name.

Run these as targeted HubSpot searches using the appropriate filters:
- Tab 1: filter `num_associated_deals NOT_HAS_PROPERTY`
- Tab 2: filter `notes_last_contacted NOT_HAS_PROPERTY`
- Tab 3: filter `num_associated_deals GT 0`, sort by `num_associated_deals DESCENDING`
- Tab 4: filter `country HAS_PROPERTY` + `country NEQ "United States"`, sort by `country ASCENDING`

Paginate each query until all records are retrieved.

### 3. Build the Excel spreadsheet using openpyxl
Create a file at: `/sessions/exciting-tender-turing/mnt/Daily Accounts/Brian_HubSpot_Accounts.xlsx`

Apply this formatting to all tabs:
- Header row: dark navy fill (#1F4E79), white bold Arial 10pt, centered, frozen
- Alternating row fill: light blue (#D6E4F0) on even rows
- Data font: Arial 9pt
- HubSpot link column: blue underlined hyperlink font, cell text = "View in HubSpot", URL = `https://app.hubspot.com/contacts/21878985/record/0-2/{company_id}`
- Enable auto-filter on all sheets
- Format dates as MM/DD/YYYY

**Tab 1 – No Deal History** columns (widths): Company Name (35), Website/Domain (30), Phone (18), City (18), State (10), Country (18), # Contacts (10), Added to CRM (14), Last Contacted (14), HubSpot Link (16)

**Tab 2 – No Activity Ever** columns: Company Name (35), Website/Domain (30), Phone (18), City (18), State (10), Country (18), # Contacts (10), Added to CRM (14), HubSpot Link (16)

**Tab 3 – Customers – All Orders** columns: Company Name (35), Website/Domain (28), Phone (18), City (18), State (10), Country (18), # Contacts (10), # Deals (9), Open Deals (10), Last Contacted (14), HubSpot Link (16)

**Tab 4 – International (Non-USA)** columns: Country (20), Company Name (35), Website/Domain (28), Phone (18), City (18), State (18), # Contacts (10), # Deals (9), Last Contacted (14), HubSpot Link (16)

### 4. Save and verify
Save the file. Confirm each tab has the correct number of rows and print a summary like:
- Tab 1 – No Deal History: X companies
- Tab 2 – No Activity Ever: X companies
- Tab 3 – Customers – All Orders: X companies
- Tab 4 – International (Non-USA): X companies

## Output
The final file must be saved to: `/sessions/exciting-tender-turing/mnt/Daily Accounts/Brian_HubSpot_Accounts.xlsx`
Overwrite any existing file at that path. The spreadsheet should reflect the current state of HubSpot at the time of the run — archived or reassigned companies will naturally drop off.