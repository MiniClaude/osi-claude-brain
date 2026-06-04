---
name: bc-tradeshow-prospecting
description: Turn any fiber/broadband industry source — a trade show URL, an ISP ranking page, a metro fiber map, or a pasted company list — into a prioritized greenfield pipeline for Brian Charrette at OSI Global. Pulls the operator list, filters to US-only and OSI-fit (strips vendors, construction, media, government), cross-references HubSpot to bucket each company (Tier 1 greenfield, unowned, Brian-owned, or owned-by-other-rep), and deep-enriches the top 3 Tier 1 targets via ZoomInfo (news, scoops, VP/Director-level contacts in Network/Engineering/IT/Ops). Outputs a markdown screening report and a Word doc intel brief, saved to Brian's TradeShows.Internet.Trolling folder. Does NOT write to HubSpot — pure intelligence brief, decisions stay with Brian. ALWAYS use this skill when Brian says any of: "run tradeshow prospecting", "prospect this conference", "screen this list", "greenfield pipeline from [URL]", "intel brief on [conference/directory]", "find me new fiber operators", "screen [URL] for OSI fit", "pull operators from [source]", "use [website] for greenfield prospecting", or pastes a fiber/broadband industry URL (fiberconnect.fiberbroadband.org, broadbandnow.com, telecomramblings.com, lightwaveonline.com, or any similar industry source) and wants to find new customer targets. Trigger automatically when Brian shares a URL or pasted list of fiber/ISP/broadband companies — even if he doesn't explicitly say "run the skill". Don't trigger on single-company requests (use bc-account-enrichment) or LinkedIn profile qualification (use bc-prospect-qualification).
---

# bc-tradeshow-prospecting

End-to-end intelligence brief for new fiber/broadband customer prospecting. Brian feeds a source; the skill returns a prioritized list plus deep enrichment on the top 3 greenfields. No HubSpot writes — Brian makes every CRM decision himself.

## What this skill does (and doesn't)

**Does:**
- Pulls the operator/customer list from any fiber/broadband industry source (conference speaker rosters, ISP directories, metro fiber maps, trade press subscriber lists, pasted company lists).
- Filters to US-only and OSI customer profile (skips vendors/competitors, construction firms, media, consultancies, government bodies).
- Cross-references every name against HubSpot to bucket: Tier 1 greenfield, unowned-in-CRM, Brian-owned, owned-by-other-JAM-rep.
- Deep-enriches the top 3 Tier 1 targets via ZoomInfo: account research, last 90 days of news, scoops, and VP/Director-level decision-makers in Network/Engineering/IT/Operations only.
- Produces two deliverables: a markdown screening report (full list with buckets) and a Word doc intel brief (deep enrichment on the top 3).

**Does NOT:**
- Write to HubSpot. Not companies, not contacts, not tasks. Brian reviews the report and decides what to claim, sequence, or pursue. This is intentional — the skill is intelligence, not CRM automation. If Brian wants to act, he hands off to `bc-account-enrichment` (deeper single-account) or `bc-7step-w-tracking` (sequence kick-off).
- Pull broad market analysis or sector research. This is account-level prospecting only.

## Inputs

Accept any of:
1. **URL to an industry source** — fiber conference site, ISP directory, metro fiber map, trade press page. Examples: `fiberconnect.fiberbroadband.org`, `broadbandnow.com`, `telecomramblings.com/metro-fiber-maps`, `lightwaveonline.com`.
2. **Pasted markdown list or text dump** — Brian sometimes copies pages into chat. Parse whatever structure is present.
3. **Specific source name + segment** — e.g., "BroadbandNow top 100 ISPs", "Fiber Connect 2026 speakers", "Telecom Ramblings Dallas metro fiber providers".

If the input is ambiguous (e.g., a base domain without a section), ask one clarifying question before proceeding.

## Workflow

### Phase 1 — Pull the source

For URLs:
- Use `mcp__workspace__web_fetch` first. Many sources are static HTML and this avoids the Chrome overhead.
- If the page is JS-rendered (eventscribe.net iframes, paginated tables, etc.), fall back to Claude in Chrome. Use `mcp__Claude_in_Chrome__navigate` + `mcp__Claude_in_Chrome__read_page` with `filter: "interactive"` to get the rendered DOM. Save large outputs to a temp file and parse with bash/Python — read_page output >100k tokens will be redirected to file.
- For conference speaker rosters, the bucket-by-organization view (`bucket=org`) is gold — it groups speakers under their employer, so the org name is a clean list-item header right above each person.

For pasted text:
- Parse line by line. Most ranking sources have a recognizable pattern (Name, then numeric ranking, state count, max speed). When unsure, ask Brian to confirm the column meaning before filtering.

### Phase 2 — Filter to OSI customer profile

Strip these categories aggressively. None of them buy OSI's stack:

| Drop | Why |
|---|---|
| Network equipment OEMs | Adtran, Calix, Cisco, Nokia, Juniper, Ciena, Harmonic, Clearfield, Dell, HPE, Aruba, Fortinet — competitors or upstream partners |
| Optics/cable/fiber vendors | Corning, CommScope, AFL, Hexatronic, Prysmian, Sumitomo, Dura-Line, Emtelle |
| Software/test vendors | 3-GIS, IQGeo, COS Systems, VETRO, Praxedo, EXFO, Plume, GLDS, Render Networks, Incognito |
| Construction / installers | Aecon, Circet, Dycom, TAK, UniTek Global, NTI, Michael Baker, Horrocks, Finley Engineering |
| Consultancies / analysts | Cartesian, Recon Analytics, Omdia, Dell'Oro, S&P Global, RVA, CTC Technology |
| Media / press | Light Reading, Fierce Network, Lightwave/Broadband Tech Report, Total Telecom, Broadband Library |
| Government / non-profits / trade orgs | FBA, NTCA, USDA Rural Development, state broadband offices, FTTH Council |

Keep:
- ISPs (regional, ILEC, CLEC, cable+fiber)
- Co-ops (electric or telco)
- Municipal fiber utilities
- Tribal carriers
- Wholesale fiber operators
- Data center + connectivity providers (when paired with fiber)

**US-only filter:** Default. Strip Canadian, EU, LATAM, APAC operators unless Brian explicitly opts in. When checking HubSpot, prefer matches whose `domain` ends in `.com`/`.us` or whose state field matches a US state. When checking ZoomInfo, pass `country="United States"` on `search_companies`/`search_contacts`.

### Phase 3 — HubSpot cross-reference

For each filtered company:

Call `mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__search_crm_objects` on `companies` with the company name as `query`. Request properties: `name, domain, hubspot_owner_id`. Limit 3-5 results so you catch variant records (e.g., "Brightspeed" vs "Brightspeed of Texas").

Bucket the result:

| Bucket | Condition |
|---|---|
| Tier 1 greenfield | Zero results returned — truly new |
| Unowned in HubSpot | Record exists, `hubspot_owner_id` is empty string |
| Brian owns | `hubspot_owner_id == "213536174"` |
| Owned by other JAM rep | Any other owner ID |
| Owned by inactive rep | Owner exists but `isActive: false` (reassignment candidate — flag separately) |

Batch lookups in parallel (10-15 at a time). Resolve owner IDs to rep names with `search_owners` — cache them; the same rep IDs repeat across accounts.

### Phase 4 — Tier the greenfields

Apply OSI fit scoring on the greenfield bucket only. Don't waste cycles tiering owned accounts.

**Tier 1 = strong signal across all four factors:**
- Size: $50M+ revenue or 500+ employees
- OSI fit: active fiber/broadband ops buying optics, memory, servers, networking, power
- Project phase: active build / funded grants / RFP phase visible from news or recent press
- Growth rate: 20%+ YoY or major new initiative announced

**Tier 2 = 3 of 4 at Tier 1 level, or majority Tier 2.**

**Tier 3 = small, unverified, or limited infrastructure spend.**

If a quick web search is needed to score Tier 1 vs Tier 2, use `WebSearch` not Chrome — it's faster. One search per company maximum at this stage; you're tiering, not enriching.

### Phase 5 — Deep enrich top 3 Tier 1

Pick the 3 greenfields with the strongest signal (active build, recent exec move, named project). Each gets the full ZoomInfo treatment:

1. `mcp__4ba1185f-93a5-43f3-9910-49e11601259c__search_companies` — get the ZoomInfo company ID.
2. `account_research` — broad orientation pass.
3. `enrich_news` — last 90 days, all categories.
4. `enrich_scoops` — last 6 months, all topics. Watch for executive moves, hiring plans, funding, partnerships.
5. `search_contacts` — VP/Director only, IT/Engineering/Operations departments only, contactAccuracyScore ≥ 85, requiredFields = email. This is the strict filter Brian asked for — no Manager-level noise. Use department IDs: `5` (IT), `6` (Engineering & Technical), `4` (Operations). Use managementLevel: `C Level Exec,VP Level Exec,Director`.

Skip the intent topic call. ZoomInfo's intent topic vocabulary is unstable and 80% of the value is already in scoops + news.

If ZoomInfo returns no `account_research` data (typical for newer JV entities or private companies), note the gap explicitly in the report. Fall back to news + scoops + web search for the strategic posture section.

### Phase 6 — Output: markdown screening report

Save to: `C:\Users\Mini\Documents\Documents\Claude\OSI-Brain\TradeShows.Internet.Trolling\[source-slug]-Greenfield-Screening.md`

Use this structure (keep tables tight, don't pad):

```markdown
# [Source Name] — Greenfield Screening Report
**Source:** [URL or description]
**Date:** [YYYY-MM-DD]
**Owner:** Brian Charrette (213536174)
**Filter:** US-only; OSI customer profile (ISPs/co-ops/munis/tribal/wholesale fiber/data centers). [N] vendor/construction/media entries stripped.

## Summary
| Bucket | Count |
|---|---|
| Tier 1 Greenfield | N |
| Tier 2 Greenfield | N |
| Unowned in HubSpot (claim) | N |
| Reassignment candidates (inactive owner) | N |
| Brian already owns | N |
| Owned by other JAM reps | N |

## Tier 1 Greenfield — Hit First
[One subsection per company: Coverage, Why, OSI angle, Outreach target title]

## Tier 2 Greenfield — Worthwhile Adds
[Table format]

## Unowned in HubSpot — Claim Immediately
[Table: Company | HubSpot ID | Note]

## Reassignment Candidates
[Table: Company | Inactive Owner | Why it matters]

## Brian Already Owns
[Table: Company | Note (refresh angle / show plan)]

## Owned by Other JAM Reps — Skip / Coordinate
[Table: Company | Owner]

## Recommended Next Steps
[3-5 numbered actions, concrete]
```

### Phase 7 — Output: Word doc intel brief

Build via the `docx` skill (or directly with the `docx` npm package — see template in the past session for structure). Save to the same TradeShows folder as `[source-slug]-Enrichment-[Top3Names].docx`.

Structure per account (one section each, page break between):

1. HubSpot baseline (greenfield/unowned/etc + any existing record)
2. Strategic posture & recent news (from account_research, news, scoops)
3. Active buying signals (call out any named project, exec change, grant, RFP)
4. Top decision-makers table (Name, Title, ZI score, Department, Has email?)
5. Recommended plays (3-4 bullets — who to target first, what angle to lead with)

Close with a "Next Actions" section listing concrete steps but **explicitly do not propose HubSpot writes**. Suggest: "Run bc-7step-w-tracking on [Name] with [angle]" — but the actual decision and CRM action stays with Brian.

### Phase 8 — Deliver

Reply in chat with:
- `computer://` links to both files
- A 5-line recap: source pulled, # screened, # Tier 1 greenfield, top finding (the single hottest signal), recommended next step
- Offer to hand off to `bc-account-enrichment` (for deeper single-account work) or `bc-7step-w-tracking` (for sequence start) — but don't invoke either automatically

## Conventions Brian relies on

- **Owner ID:** Brian's hubspot_owner_id is `213536174`. HubSpot portal `21878985`.
- **Workspace folder:** Always save outputs to `C:\Users\Mini\Documents\Documents\Claude\OSI-Brain\TradeShows.Internet.Trolling`. This is locally stored; files persist across sessions.
- **Tone in the deliverables:** Direct, action-oriented. Brian's preference is concise prose, no filler, no disclaimers, no AI-style hedge language. Tables over paragraphs when listing companies. Bullets over walls of text for outreach angles.
- **Top decision-maker definition:** VP/Director-level only, Information Technology / Engineering & Technical / Operations departments only. No Managers, no other departments. This is a deliberate signal-vs-noise tradeoff Brian asked for.
- **OSI products to reference in plays:** Optics (SFP+/QSFP/DWDM, especially Nokia/Cisco/Adtran/Calix-compatible), servers/storage (Dell/HPE refresh), DDR4/DDR5 memory, power (APC/Eaton at huts/POPs/substations), TPM (third-party maintenance on aging gear), pro services. Match the angle to whatever signal surfaced in enrichment.

## Error handling

- **Empty page / JS-rendered iframe:** Fall back from `web_fetch` → Chrome `navigate` + `read_page`. If Chrome can't reach the content (login wall, anti-bot), tell Brian and ask if he can log in manually in his Chrome tab.
- **Pasted list with unclear columns:** Ask Brian once which column is the company name and which (if any) are speed/state/coverage. Don't guess wrong and waste a screen pass.
- **HubSpot search returns lots of unrelated matches:** When `query` is generic (e.g., "Spectrum"), tighten with a domain filter or skip — note as "manual verification needed" in the report rather than mis-bucketing.
- **ZoomInfo company ID returns no data on `account_research`:** Common for JV entities (Gigapower-style). Note it explicitly, lean harder on news + scoops + web.
- **Conference site behind login:** Ask Brian to log in his Chrome tab, then resume.

## What this skill replaces (workflow that used to be manual)

This skill collapses what was previously a 4-step manual chain:
1. Open the source URL → pull the company list by hand.
2. Run `bc-greenfield-screening` on the list → markdown bucketing.
3. Pick the top 3 → run `bc-account-enrichment` on each.
4. Realize you forgot the US-only filter halfway through and start over.

Now: one command, one report, one Word doc. US-only enforced. No HubSpot writes by design — Brian wants the intel, not auto-CRM.

## Why no HubSpot writes

This was a deliberate choice during skill design. The earlier `bc-greenfield-screening` flow auto-created HubSpot records for Tier 1 targets. Brian found that the screen+enrich step is the high-judgment moment, and he'd rather review the intel and decide which records to create than have them appear pre-populated. Keeping the CRM as a human decision keeps the data clean and gives Brian a useful gate between "intel" and "commitment."

If a future version wants to add HubSpot writes back in, do it as an explicit second pass (e.g., "create records for the 3 accounts I approved") rather than baking it into the main flow.
