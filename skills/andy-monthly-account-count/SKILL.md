---
name: andy-monthly-account-count
description: >
  Track Brian's HubSpot account ownership over time. How many companies he owns,
  how many were added (net new), reassigned to him, or removed since the last snapshot.
  Generates an interactive HTML dashboard with a count-over-time chart and per-category tables.
  ALWAYS use this skill when Brian says "run account count", "account count report",
  "how many accounts do I have", "show me my account changes", "what changed in my accounts",
  "account tracker", or any variation of wanting to see account ownership growth or changes over time.
---

# Brian Monthly Account Count

Tracks Brian's HubSpot company ownership over time. Total count, net new adds, reassignments in,
and removals. Renders an interactive HTML dashboard with a running chart.

## Key Constants

- **Brian's HubSpot Owner ID**: `213536174`
- **Skill base directory**: wherever this SKILL.md lives (e.g. `.claude/skills/andy-monthly-account-count/`)
- **Snapshots directory**: `snapshots/` (sibling to SKILL.md)
- **Output file**: `Andy_Account_Count_YYYY-MM-DD.html` saved to Brian's workspace folder
- **Today's date property in HubSpot**: use `createdate` to identify net-new records

---

## Execution Flow

### Step 1. Confirm Intent

If Brian says "run account count" or similar, proceed automatically. If he mentions a specific
date range ("since March", "since 4/1"), note it. You will use that date as the comparison point
instead of the last snapshot date.

Tell Brian: "Pulling your current account list from HubSpot and comparing against your last snapshot. Give me a minute."

---

### Step 2. Load Last Snapshot

Read the most recent snapshot file from the `snapshots/` directory.

```python
import json, os
from pathlib import Path
from datetime import datetime

skill_dir = Path(__file__).parent  # adjust path as needed
snapshot_dir = skill_dir / "snapshots"

# Find most recent snapshot
snapshots = sorted(snapshot_dir.glob("*.json"))
if snapshots:
    with open(snapshots[-1]) as f:
        prior_snapshot = json.load(f)
    snapshot_date = snapshots[-1].stem  # e.g. "2026-04-20"
else:
    prior_snapshot = []
    snapshot_date = None
```

If no snapshot exists, this is the **first run**. Skip the diff, just establish the baseline
and tell Brian: "No prior snapshot found. Establishing baseline today. Future runs will show changes."

---

### Step 3. Pull Current Companies from HubSpot

Paginate through ALL companies owned by Brian. Use `after` cursor to get beyond the first 200.

```
search_crm_objects({
  objectType: "companies",
  filterGroups: [{
    filters: [
      { propertyName: "hubspot_owner_id", operator: "EQ", value: "213536174" }
    ]
  }],
  properties: ["name", "createdate", "hubspot_owner_id", "city", "state", "industry"],
  sorts: [{ propertyName: "createdate", direction: "DESCENDING" }],
  limit: 200
})
```

**Pagination is critical.** Brian's book is large. Keep calling with the `after` cursor
until `paging.next` is null. Collect ALL results before proceeding.

Store each company as:
```json
{
  "id": "12345",
  "name": "Acme Corp",
  "createdate": "2026-04-15T14:00:00.000Z",
  "city": "Austin",
  "state": "TX",
  "industry": "Technology"
}
```

---

### Step 4. Compute the Diff

Compare the current list against the prior snapshot to produce three buckets.

**Prior snapshot IDs** (set):
```python
prior_ids = {c["id"] for c in prior_snapshot}
current_ids = {c["id"] for c in current_companies}
snapshot_cutoff = datetime.fromisoformat(snapshot_date) if snapshot_date else None
```

#### Bucket: Added (Net New)
Companies in `current_ids` but NOT in `prior_ids`, **AND** whose `createdate` is AFTER the snapshot date.
These are genuinely new HubSpot records that didn't exist before.

```python
added = [
    c for c in current_companies
    if c["id"] not in prior_ids
    and snapshot_cutoff
    and datetime.fromisoformat(c["createdate"].replace("Z","")) > snapshot_cutoff
]
```

#### Bucket: Reassigned (Transferred to Brian)
Companies in `current_ids` but NOT in `prior_ids`, **AND** whose `createdate` is BEFORE the snapshot date.
These records existed before the snapshot but belonged to another rep. They were transferred to Brian.

```python
reassigned = [
    c for c in current_companies
    if c["id"] not in prior_ids
    and snapshot_cutoff
    and datetime.fromisoformat(c["createdate"].replace("Z","")) <= snapshot_cutoff
]
```

#### Bucket: Removed (Lost Ownership)
Companies in `prior_ids` but NOT in `current_ids`.
These records existed but are no longer owned by Brian (reassigned away, deleted, or owner cleared).

```python
removed = [c for c in prior_snapshot if c["id"] not in current_ids]
```

#### Summary counts:
```
Total (now):     len(current_companies)
Prior total:     len(prior_snapshot)
Added:           len(added)
Reassigned in:   len(reassigned)
Removed:         len(removed)
Net change:      len(current_companies) - len(prior_snapshot)
```

---

### Step 5. Save New Snapshot

Write today's full company list to `snapshots/YYYY-MM-DD.json`.

```python
today = datetime.now().strftime("%Y-%m-%d")
with open(snapshot_dir / f"{today}.json", "w") as f:
    json.dump(current_companies, f, indent=2)
```

Keep all historical snapshots. Do NOT delete old ones.

---

### Step 6. Build the HTML Dashboard

Generate a self-contained HTML file. Output to Brian's workspace folder as
`Andy_Account_Count_YYYY-MM-DD.html`.

#### Dashboard Structure

```
┌─────────────────────────────────────────────────────────┐
│  Brian Monthly Account Count. April 20, 2026             │
│  Compared against: April 17, 2026 snapshot              │
├────────┬──────────┬─────────────┬──────────┬────────────┤
│ Total  │  Added   │ Reassigned  │ Removed  │ Net Change │
│ 1,218  │   +12    │     +4      │    -2    │    +14     │
├─────────────────────────────────────────────────────────┤
│  [Count-over-time line chart. One point per snapshot]   │
├─────────────────────────────────────────────────────────┤
│  Added (12)        │  Reassigned (4)  │  Removed (2)   │
│  ─────────────     │  ─────────────   │  ──────────    │
│  Company · State   │  Company · State │  Company name  │
│  ...               │  ...             │  ...           │
└─────────────────────────────────────────────────────────┘
```

#### Styling Guidelines
- Background: `#0f1117` (near-black)
- Primary accent: `#3b82f6` (blue) for Added and Total
- Reassigned accent: `#f59e0b` (amber)
- Removed accent: `#ef4444` (red)
- Net change: green if positive, red if negative
- Font: `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- Metric cards: rounded corners, subtle border, large number, small label
- Table rows: alternating subtle shade for readability
- Chart: use Chart.js from cdnjs for the count-over-time line

#### Chart Data
The count-over-time chart uses all saved snapshots as data points. For each snapshot file
in the `snapshots/` directory, read the record count. Plot date (x) vs. total count (y).
This gives Brian a visual trend line showing growth over time.

If only one snapshot exists (today's baseline), show a single point with a note
"Add more runs to see the trend."

#### HTML Template
The dashboard must be fully self-contained (no external dependencies except Chart.js CDN).
Embed all data inline as JavaScript constants. Use responsive layout (works on laptop screen).

```html
<!-- Key JS constants to embed -->
const SNAPSHOT_DATE = "2026-04-17";
const TODAY = "2026-04-20";
const TOTAL_NOW = 1218;
const PRIOR_TOTAL = 1214;
const ADDED = [...]; // array of {name, city, state, industry, createdate}
const REASSIGNED = [...];
const REMOVED = [...];
const CHART_DATA = [{date: "2026-04-17", count: 1214}, {date: "2026-04-20", count: 1218}];
```

---

### Step 7. Present Results

After the HTML is saved, present the file link plus a quick summary:

```
✅ Account count report built.

[View Andy_Account_Count_2026-04-20.html](computer://...path...)

📊 As of today vs. April 17 snapshot:
- Total: 1,218 companies (was 1,214)
- Added (net new): +12
- Reassigned to you: +4
- Removed / lost: -2
- Net change: +14
```

If this was the first run (no prior snapshot), say:
```
✅ Baseline established. 1,214 companies as of today.
No diff to show yet. Run "account count" again next week to see changes.
```

---

## Snapshot File Format

Each snapshot is a JSON array of company objects:

```json
[
  {
    "id": "12345678",
    "name": "Acme Corp",
    "createdate": "2026-01-15T10:30:00.000Z",
    "city": "Austin",
    "state": "TX",
    "industry": "Technology"
  },
  ...
]
```

Snapshots live in `snapshots/YYYY-MM-DD.json`. Always keep all historical snapshots for the chart.

---

## Error Handling

- **Pagination stalls / partial results**: If a pagination call returns 0 after showing non-zero
  earlier, retry once before stopping. Note the actual count returned in the summary.
- **No internet / HubSpot timeout**: Abort and tell Brian. Do not write a snapshot from partial data.
- **Snapshot directory missing**: Create it automatically.
- **File already open in browser**: Save as `_v2` suffix if the primary file is locked.
- **First run (no snapshots)**: Establish baseline only, no diff needed.

---

## Notes on the ZoomInfo Integration

Brian's "net new" companies often include records auto-created by HubSpot's ZoomInfo integration
(source = `INTEGRATION`, detail = `ZoomInfo by DiscoverOrg`). These appear in the Added bucket
because their `createdate` is recent. This is expected behavior. They represent real new records
in Brian's ownership, even if he didn't personally prospect them. If Brian wants to filter these out,
add a note but don't do so by default.
