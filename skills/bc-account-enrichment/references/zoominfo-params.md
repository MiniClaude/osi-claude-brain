# ZoomInfo Parameter Reference

Valid field values for ZoomInfo MCP calls. ZI is strict about enum values — if a call fails with a parameter error, the value is almost always malformed or unsupported. Use `lookup` with the field name to get the current valid set before retrying.

## Management Level (`managementLevel`)

Used in `search_contacts` to filter by seniority. These are the exact strings ZI accepts:

- `C Level Exec` — CIOs, CTOs, CEOs, CFOs, CISOs, etc.
- `VP Level Exec` — VPs and SVPs
- `Director` — Directors and Sr. Directors
- `Manager` — Managers, Sr. Managers
- `Non Manager` — individual contributors; useful for hands-on Network Engineer / Architect roles that don't have management level set

For OSI enrichment, the primary filter stack is `C Level Exec`, `VP Level Exec`, `Director`, `Manager`. Add `Non Manager` only when we need senior ICs like Principal Network Architects who often lack a management tag.

## Department (`department`)

- `Information Technology` — core OSI target
- `Engineering` — covers Network Engineering, Systems Engineering, DevOps, SRE
- `Operations` — covers Data Center Operations, NetOps, IT Ops
- `Finance` — for procurement/AP contacts when we need the buying side
- `Executive` — overlaps with C Level Exec; useful when the target has title but no explicit department tag

Primary filter for enrichment: `Information Technology`, `Engineering`, `Operations`.

## Job Title Keywords (`jobTitle`)

ZI's `jobTitle` field matches on substring. OR-join these for OSI decision-maker pulls:

- network
- infrastructure
- data center
- architect
- systems
- cloud
- security
- telecommunications
- operations
- IT

Avoid generic terms like `engineer` or `manager` alone — too noisy.

## Intent Topics (`enrich_intent`)

ZI's intent topic list is curated. Request the full list with `lookup` if unsure. OSI-relevant topics that exist in ZI:

- Networking Hardware
- Optical Transceivers
- DWDM / Wavelength Division Multiplexing
- Network Switches
- Data Center Infrastructure
- Third-Party Maintenance
- IT Asset Disposition
- Cisco (various product lines)
- Juniper Networks
- Aruba Networks / HPE
- Dell EMC Servers
- HPE ProLiant
- Memory / DRAM
- Colocation Services
- Fiber Optic Cabling
- Network Monitoring
- Refurbished IT Hardware

If a topic returns empty, try a broader term. Intent data is signal-based and some topics simply aren't tracked for smaller accounts.

## Company Size (`employeeCount`, `revenue`)

OSI ICP favors 1,000+ employees and $1B+ revenue, but do not filter these out at the ZI level when enriching a specific named account — we want the account data regardless of size. Size filters are for prospecting, not enrichment.

## News Categories (`enrich_news`)

- `Acquisition`
- `Layoffs`
- `Funding`
- `Product Launch`
- `Partnership`
- `Hiring`
- `Leadership Change`
- `Office Opening`
- `Technology Adoption`

For enrichment, pull the last 90 days across all categories — the report should surface whatever's relevant without pre-filtering.

## Scoops (`enrich_scoops`)

Scoops are analyst-verified project signals. No parameter tuning needed — just call it on the ZI company ID and ZI returns what's available. Common scoop types OSI cares about:

- Infrastructure refresh / upgrade projects
- Data center build or expansion
- Cloud migration
- Security initiative / Zero Trust rollout
- Network modernization
- New office or site opening
- M&A integration

## Common parameter errors and fixes

- `"Senior Manager"` → use `Manager` (ZI doesn't have a Senior Manager tier)
- `"Vice President"` → use `VP Level Exec`
- `"IT"` as department → use `Information Technology` (full spelling)
- `"C-Level"` or `"C-Suite"` → use `C Level Exec` (spaces, no hyphen)
- `"Data Center"` as department → no such department; use `Operations` and filter on jobTitle keyword
- `companyWebsite: "www.example.com"` → strip www, use `example.com`

## Fallback pattern

If `search_contacts` returns 0 results with a tight filter, relax in this order:

1. Drop jobTitle keywords, keep managementLevel + department
2. Drop department, keep managementLevel only
3. Expand managementLevel to include `Non Manager`
4. Last resort: drop all filters except companyId — get everyone ZI has at the account, then filter in the report generation phase
