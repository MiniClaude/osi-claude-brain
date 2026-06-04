---
name: bc-fiber-intel-sweep
description: |
  Weekly broadband & fiber intelligence sweep for OSI Global sales. Monitors news sources, BEAD/FCC funding data, trade show exhibitor lists, and M&A signals to surface greenfield companies that fit OSI's ICP. Cross-references every discovered company against HubSpot to flag unowned accounts. Outputs a structured weekly digest into Obsidian at Research/Fiber-Broadband-Intel.md and creates HubSpot tasks for Tier 1 targets. Runs on demand or on a Monday morning schedule.

  ALWAYS use this skill when Brian says anything like: "run my fiber digest", "run the fiber sweep", "fiber intel", "broadband sweep", "check fiber news", "what's new in broadband", "fiber greenfield sweep", "run bc-fiber-intel-sweep", "run the intel agent", "fiber monitoring", or any variation of wanting to surface new broadband/fiber companies from news, BEAD, or trade show sources. Also triggers automatically on the Monday 7:00 AM scheduled task.
---

# bc-fiber-intel-sweep

Weekly broadband and fiber intelligence agent for OSI Global. Sweeps 5 source categories, discovers new companies, cross-references HubSpot for greenfield status, scores OSI fit, and writes a structured digest to Obsidian. Hands Brian a ranked list of warm, unworked targets every Monday.

---

## Key Constants

- **Brian's HubSpot Owner ID**: `213536174`
- **Obsidian API**: `http://127.0.0.1:27123` — key stored in memory (`reference_obsidian_api.md`)
- **Obsidian digest target**: `Research/Fiber-Broadband-Intel.md`
- **Obsidian API calls**: Use `mcp__Claude_in_Chrome__javascript_tool` (bash cannot reach localhost)
- **Tab ID**: Get fresh tab via `mcp__Claude_in_Chrome__tabs_context_mcp` before any Obsidian calls

---

## Run Modes

**On demand** — Brian says "run my fiber digest" or similar → run full sweep immediately, report results in chat + update Obsidian.

**Scheduled (Monday 7:00 AM)** — Full sweep runs automatically. Digest appended to Obsidian. No chat interaction needed — skill runs silently and saves output.

---

## Phase 1 — News & Intel Sweep

Search each source category for new company mentions from the **past 7 days**. Use `WebSearch` with targeted queries. For each search, extract company names, key signals, and context.

### 1A — Federal Funding (BEAD / FCC)

Run these searches:
- `BEAD broadband grant awarded 2026 site:ntia.gov OR site:broadbandusa.ntia.gov`
- `BEAD broadband deployment approval state 2026`
- `FCC broadband funding awarded fiber 2026`
- `RDOF rural broadband award construction 2026`

Extract: company/co-op name, state, award amount, project phase, technology (fiber, fixed wireless).

### 1B — Industry News & M&A

Run these searches:
- `fiber broadband expansion news 2026 site:fierce-network.com OR site:lightreading.com OR site:broadbandbreakfast.com`
- `broadband operator acquisition merger 2026`
- `CLEC fiber overbuilder expansion 2026`
- `rural electric cooperative fiber deployment 2026 site:electric.coop OR site:cooperative.com`
- `site:telecomramblings.com fiber metro 2026`
- `site:bbcmag.com broadband provider 2026`

Extract: company names, project signals, funding status, build timeline.

### 1C — Provider & Member Directories

Run these searches periodically (monthly cadence — skip if run in past 30 days):
- `site:fiberbroadband.org member directory 2026`
- `site:tlsn.us member companies`
- `site:broadbandnow.com fiber provider list`

Extract: new company names not previously seen.

### 1D — Trade Show Exhibitors & Attendees

Check for newly published exhibitor/attendee lists:
- `Fiber Connect 2026 exhibitor list site:fiberconnect.fiberbroadband.org`
- `Metro Connect 2026 exhibitor attendee list`
- `ITW 2026 exhibitor list site:internationaltelecomsweek.com`
- `OFC 2026 exhibitor list site:ofcconference.org`

Extract: company names from exhibitor lists. Flag companies exhibiting at fiber/broadband shows as high-intent signals.

### 1E — GitHub / Open Data

If Brian has flagged any GitHub repos or public datasets (BEAD award data, FCC Form 477, state broadband maps), check for new data:
- Search for recently updated broadband datasets: `site:github.com broadband ISP data 2026`
- Check NTIA BEAD dashboard for state-level updates

---

## Phase 2 — Company Dedup & Normalization

1. Compile all discovered company names into a single list
2. Remove duplicates (normalize variants: "GoNetspeed" = "Go Netspeed", "AT&T Fiber" = "AT&T", etc.)
3. Remove companies already processed in previous sweeps (check existing Obsidian digest entries)
4. Target list: aim for **10–30 net-new companies per sweep**

---

## Phase 3 — HubSpot Greenfield Check

For each company on the net-new list, run a HubSpot lookup:

```
search_crm_objects({
  objectType: "companies",
  filterGroups: [{
    filters: [{ propertyName: "name", operator: "CONTAINS_TOKEN", value: "[company name]" }]
  }],
  properties: ["name", "hubspot_owner_id", "hs_num_associated_contacts", "notes_last_contacted"],
  limit: 5
})
```

Label each company:
- **GREENFIELD** — not in HubSpot at all → high priority
- **UNOWNED** — in HubSpot, no owner assigned → medium priority, claim it
- **BRIAN'S ACCOUNT** — owned by Brian (hubspot_owner_id: 213536174) → skip outreach task, flag for review
- **OTHER REP** — owned by another rep → note the owner, do not pursue

Only GREENFIELD and UNOWNED companies move forward to scoring.

---

## Phase 4 — OSI Fit Scoring

Score each GREENFIELD / UNOWNED company on four factors. Assign Tier 1 / 2 / 3.

### Scoring Factors

**Company Size**
- Tier 1: Serves 5,000+ subscribers OR 100+ employees OR $10M+ revenue
- Tier 2: 500–5,000 subscribers OR 25–100 employees
- Tier 3: Small co-op or startup, <500 subscribers

**OSI Product Fit**
- Tier 1: Active fiber/FTTH/DWDM operator — buying optics, SFP/QSFP, transceivers, servers, power, TPM
- Tier 2: Infrastructure-heavy but primarily wireless or hybrid — partial fit
- Tier 3: Early stage, no clear hardware spend signal

**Project Phase / Urgency**
- Tier 1: Active build-out, funded grant, Phase 2–3 deployment underway — buying NOW
- Tier 2: Grant awarded but pre-construction, or Phase 1 planning
- Tier 3: Early concept, unfunded, or dormant

**Growth / Expansion Signal**
- Tier 1: New award, M&A activity, expansion announcement, or trade show presence in past 90 days
- Tier 2: Growth signals 90–365 days old
- Tier 3: No recent signal

**Tier assignment:**
- **Tier 1** = 3–4 factors at Tier 1 level → Queue for immediate outreach
- **Tier 2** = 2 factors at Tier 1 OR majority at Tier 2 → Monitor, outreach in 60–90 days
- **Tier 3** = Remainder → Watch list only

---

## Phase 5 — Write Obsidian Digest Entry

Append a new weekly digest entry to `Research/Fiber-Broadband-Intel.md` using the Obsidian REST API.

### Step 1 — Read current file

```javascript
(async () => {
  const K = 'f6e58142e450d6e7447193fe5b13efb0a138c2a8b7790c6c6c52b2370dad684c';
  const r = await fetch('http://127.0.0.1:27123/vault/Research/Fiber-Broadband-Intel.md', {
    headers: { 'Authorization': 'Bearer ' + K }
  });
  return await r.text();
})()
```

### Step 2 — Prepend new digest entry

Build the digest entry using this template, then prepend it after the `## Weekly Digest` header:

```markdown
### Week of [YYYY-MM-DD]
*Sweep ran [date] | [N] sources checked | [N] companies discovered | [N] greenfield | [N] Tier 1*

#### Tier 1 — Ready for Outreach
| Company | State | Signal | HubSpot | Suggested Angle |
|---|---|---|---|---|
| [Name] | [State] | [BEAD $XM / M&A / Exhibitor Fiber Connect] | GREENFIELD | [Optics / TPM / Power] |

#### Tier 2 — Monitor
| Company | State | Signal | HubSpot |
|---|---|---|---|
| [Name] | [State] | [Signal] | GREENFIELD / UNOWNED |

#### Sources Hit This Week
[List of sources that returned new data]

---
```

### Step 3 — Write updated file back

```javascript
(async () => {
  const K = 'f6e58142e450d6e7447193fe5b13efb0a138c2a8b7790c6c6c52b2370dad684c';
  const newContent = `[full updated file content]`;
  const r = await fetch('http://127.0.0.1:27123/vault/Research/Fiber-Broadband-Intel.md', {
    method: 'PUT',
    headers: { 'Authorization': 'Bearer ' + K, 'Content-Type': 'text/markdown' },
    body: newContent
  });
  return r.status;
})()
```

---

## Phase 6 — HubSpot Tasks for Tier 1

For each Tier 1 GREENFIELD company:

1. **Create company record** if not already in HubSpot:
```
manage_crm_objects({
  action: "create",
  objectType: "companies",
  properties: {
    name: "[company]",
    industry: "Telecommunications",
    hubspot_owner_id: "213536174",
    description: "[signal from sweep]"
  }
})
```

2. **Create a task** for Brian to research and enroll:
```
manage_crm_objects({
  action: "create",
  objectType: "tasks",
  properties: {
    hs_task_subject: "bc-fiber-intel: [Company] — [Signal] — Enroll in sequence",
    hs_task_body: "Tier 1 greenfield from fiber intel sweep [date]. Signal: [what triggered it]. Suggested angle: [optics/TPM/power]. Check LinkedIn for IT/Network contacts, then run master sequence.",
    hs_timestamp: "[3 business days from now in ms]",
    hubspot_owner_id: "213536174",
    hs_task_type: "TODO"
  }
})
```

---

## Phase 7 — Chat Summary

After completing all phases, report to Brian:

```
Fiber Intel Sweep — [date]
━━━━━━━━━━━━━━━━━━━━━━━━
Sources checked: [N]
Companies discovered: [N]
Greenfield (not in HubSpot): [N]
Tier 1 (ready to work): [N]
HubSpot tasks created: [N]
Obsidian digest: Updated ✓

Tier 1 highlights:
• [Company] — [state] — [signal, e.g. "$4.2M BEAD award, Phase 2 fiber build"]
• [Company] — [state] — [signal]
• [Company] — [state] — [signal]

Say "run master sequence on [company]" to kick off outreach on any of these.
```

---

## Error Handling

- **Obsidian not running**: Save digest as Word doc to outputs folder instead. Note the error in chat.
- **HubSpot rate limit**: Batch company lookups 10 at a time with a brief pause between batches.
- **No new companies found**: Still write a digest entry noting the sweep ran and sources checked. Never silently skip.
- **Source blocks scraping**: Fall back to web search headline extraction rather than full page read.
- **API key stale**: Prompt Brian for new Obsidian key, update memory file at `reference_obsidian_api.md`.

---

## OSI ICP Quick Reference

Primary targets for fiber/broadband vertical:
- **Fiber operators** (CLECs, ILECs doing FTTH): optics (SFP/QSFP/DWDM), servers, memory, power (APC/Eaton)
- **Rural electric co-ops** building fiber: same stack, often first-time buyers — high value
- **BEAD/RDOF grant recipients**: actively spending federal money on infrastructure
- **Overbuilders** (GoNetspeed, Metronet, Wyyerd type): aggressive expansion = high volume optics + hardware
- **Competitive fiber** (Brightspeed, Consolidated, Ziply): network refresh = TPM + optics + memory upgrade cycles
- **Data center / colo operators** near fiber routes: DWDM, Smartoptics DCP, power

Not a fit: pure wireless ISPs with no fiber plant, pure software/SaaS companies, non-infrastructure co-ops.
