---
name: account-monitor
description: Run and refresh the OSI Global HubSpot Account Monitor Excel report (OSI_Account_Monitor.xlsx). This skill re-fetches live data from HubSpot and rebuilds all tabs — No Deal History, No Activity Ever, Customers, Swag Orders, AI Leads, and Open Deals — all filtered to Brian Charrette's owned accounts. ALWAYS use this skill when Brian says anything like "run my report", "run the account monitor", "refresh the report", "rebuild the account report", "update the HubSpot report", "run account monitor", "refresh account monitor", "pull the account report", "update my report", or any variation of wanting to regenerate or refresh the OSI_Account_Monitor.xlsx file.
---

# OSI Global — Account Monitor Report

Rebuild the OSI Account Monitor Excel report by fetching fresh data from HubSpot and running the build script. This skill produces `OSI_Account_Monitor.xlsx` in the Hubspot Accounts workspace folder.

## Key Constants

- **Brian's HubSpot Owner ID**: `213536174`
- **HubSpot Portal ID**: `21878985`
- **Report script**: `build_report.py` in the "Hubspot Accounts" workspace folder
- **Cache directory**: `.cache/` inside the "Hubspot Accounts" folder
- **Output file**: `OSI_Account_Monitor.xlsx` (always overwrites — no date suffix)
- **Swag sequence ID**: `264002941` (the __BC Telecom MASTER 2025 sequence)

---

## Execution Flow

### Step 1 — Confirm Intent

If the user says "run" or "refresh" without specifying which tabs, refresh ALL tabs. If they say something like "just refresh swag orders" or "update customers tab", refresh only those specific tabs and skip the rest.

Briefly tell the user: "Refreshing your HubSpot data and rebuilding the report — give me a few minutes."

---

### Step 2 — Fetch Fresh Data for Each Tab

Fetch data for each tab using `search_crm_objects`. Save each result set to the corresponding cache JSON file inside `.cache/`. All queries filter by `hubspot_owner_id = 213536174`.

#### Tab 1 — No Deal History (`tab1_no_deal_history.json`)

Companies owned by Brian with no deal history at all.

```
search_crm_objects({
  objectType: "companies",
  filterGroups: [{
    filters: [
      { propertyName: "hubspot_owner_id", operator: "EQ", value: "213536174" },
      { propertyName: "first_deal_created_date", operator: "NOT_HAS_PROPERTY" }
    ]
  }],
  properties: ["name", "city", "state", "country", "hs_num_associated_contacts", "industry", "annualrevenue"],
  sorts: [{ propertyName: "hs_num_associated_contacts", direction: "DESCENDING" }],
  limit: 200
})
```

Save results array to `.cache/tab1_no_deal_history.json`.

#### Tab 2 — No Activity Ever (`tab2_no_activity.json`)

Companies owned by Brian with no sales activity and no contact date recorded.

```
search_crm_objects({
  objectType: "companies",
  filterGroups: [{
    filters: [
      { propertyName: "hubspot_owner_id", operator: "EQ", value: "213536174" },
      { propertyName: "notes_last_contacted", operator: "NOT_HAS_PROPERTY" },
      { propertyName: "hs_last_sales_activity_timestamp", operator: "NOT_HAS_PROPERTY" }
    ]
  }],
  properties: ["name", "city", "state", "country", "hs_num_associated_contacts", "createdate"],
  sorts: [{ propertyName: "createdate", direction: "DESCENDING" }],
  limit: 200
})
```

Save results array to `.cache/tab2_no_activity.json`.

#### Tab 3 — Customers (`tab3_customers.json`)

Companies owned by Brian sorted by total deal count (top customers first).

```
search_crm_objects({
  objectType: "companies",
  filterGroups: [{
    filters: [
      { propertyName: "hubspot_owner_id", operator: "EQ", value: "213536174" },
      { propertyName: "num_associated_deals", operator: "GT", value: "0" }
    ]
  }],
  properties: ["name", "city", "state", "country", "num_associated_deals", "industry"],
  sorts: [{ propertyName: "num_associated_deals", direction: "DESCENDING" }],
  limit: 200
})
```

Save results array to `.cache/tab3_customers.json`.

#### Tab 5 — Swag Orders (`tab5_swag.json`)

Contacts who replied to the "RE: Confirming address" swag campaign email (sequence ID 264002941). These are contacts enrolled in the __BC Telecom MASTER 2025 sequence who have confirmed their shipping address.

To identify them: search for incoming email engagements with subject matching "Confirming address" and direction INCOMING_EMAIL. Then look up associated contacts.

**Efficient approach** — search contacts directly enrolled in sequence 264002941:

```
search_crm_objects({
  objectType: "contacts",
  filterGroups: [{
    filters: [
      { propertyName: "hs_latest_sequence_enrolled", operator: "EQ", value: "264002941" },
      { propertyName: "address", operator: "HAS_PROPERTY" }
    ]
  }],
  properties: ["firstname", "lastname", "email", "company", "address", "city", "state", "zip", "hs_latest_sequence_enrolled_date"],
  sorts: [{ propertyName: "hs_latest_sequence_enrolled_date", direction: "DESCENDING" }],
  limit: 200
})
```

Save results array to `.cache/tab5_swag.json`.

> **Note**: The above returns the 200 most recently enrolled contacts who have an address on file — these are the people who responded to the swag address confirmation. If Brian wants the full historical list (2,200+), paginate through all results.

#### Tab 6 — AI Leads (`tab6_ai_leads.json`)

Companies owned by Brian with ZoomInfo intent signals (the `buy_intent` property is set).

```
search_crm_objects({
  objectType: "companies",
  filterGroups: [{
    filters: [
      { propertyName: "hubspot_owner_id", operator: "EQ", value: "213536174" },
      { propertyName: "buy_intent", operator: "HAS_PROPERTY" }
    ]
  }],
  properties: ["name", "city", "state", "country", "industry", "buy_intent"],
  sorts: [{ propertyName: "name", direction: "ASCENDING" }],
  limit: 20
})
```

Save results array to `.cache/tab6_ai_leads.json`.

#### Tab 9 — Open Deals (`tab9_open_deals.json`)

Brian's currently active (non-closed) deals.

```
search_crm_objects({
  objectType: "deals",
  filterGroups: [{
    filters: [
      { propertyName: "hubspot_owner_id", operator: "EQ", value: "213536174" },
      { propertyName: "dealstage", operator: "NOT_IN", values: ["closedwon", "closedlost"] }
    ]
  }],
  properties: ["dealname", "amount", "dealstage", "closedate", "client_id__cv_name_"],
  sorts: [{ propertyName: "closedate", direction: "ASCENDING" }],
  limit: 200
})
```

Save results array to `.cache/tab9_open_deals.json`.

---

### Step 3 — Save Cache Files

For each tab, write the `results` array from the HubSpot response to the appropriate JSON file in the `.cache/` directory. The build script reads these files directly. Use Python to write the files:

```python
import json
from pathlib import Path

cache_dir = Path("/sessions/.../mnt/Hubspot Accounts/.cache")

# Example for tab1:
with open(cache_dir / "tab1_no_deal_history.json", "w") as f:
    json.dump(results, f, indent=2)
```

Repeat for each tab that was refreshed.

---

### Step 4 — Run the Build Script

Once all cache files are saved, run the build script:

```bash
cd "/sessions/.../mnt/Hubspot Accounts"
python3 build_report.py
```

The script will:
- Read all `.cache/*.json` files
- Build a formatted Excel workbook with all 6 tabs
- Save to `OSI_Account_Monitor.xlsx` (overwriting any previous version)
- Print record counts and cache status

If the script throws a `PermissionError` on the output file (it happens if the Excel file is currently open in Excel), either ask Brian to close it, or save temporarily as `OSI_Account_Monitor_temp.xlsx` and instruct him to close and retry.

---

### Step 5 — Present the File

After a successful build, present the file:

```
✅ Report rebuilt with fresh data.

[View OSI_Account_Monitor.xlsx](computer:///sessions/.../mnt/Hubspot%20Accounts/OSI_Account_Monitor.xlsx)

Tabs refreshed:
- Tab 1 – No Deal History: [N] companies
- Tab 2 – No Activity Ever: [N] companies
- Tab 3 – Customers: [N] companies (sorted by deal count)
- Tab 5 – Swag Orders: [N] contacts (most recent respondents)
- Tab 6 – AI Leads: [N] companies with ZoomInfo intent
- Tab 9 – Open Deals: [N] active deals
```

---

## Tab Reference

| Tab | Name | Object Type | Key Filter | Sort |
|-----|------|-------------|------------|------|
| 1 | No Deal History | companies | owner=Brian, no deals | contacts desc |
| 2 | No Activity Ever | companies | owner=Brian, no activity | createdate desc |
| 3 | Customers | companies | owner=Brian, deals > 0 | num_deals desc |
| 5 | Swag Orders | contacts | sequence=264002941, has address | enrolled_date desc |
| 6 | AI Leads | companies | owner=Brian, buy_intent set | name asc |
| 9 | Open Deals | deals | owner=Brian, not closed | closedate asc |

## Error Handling

- **File locked**: If `OSI_Account_Monitor.xlsx` is open in Excel, ask Brian to close it and retry, or offer to save as a temp file.
- **HubSpot timeout**: Retry the failed tab's fetch once. If it continues to fail, skip that tab and note it in the output.
- **Empty results**: If a tab returns 0 records, that's valid — write an empty array `[]` to the cache file and the build script will produce an empty (headers-only) tab.
- **Wrong workspace path**: The path to the Hubspot Accounts folder varies by session. Use `os.path.abspath` or check the current working directory to confirm the correct path before running the script.
