# Report Template — Word Doc Structure

Full structure and formatting notes for the bc-account-enrichment Word doc report. Use with the `docx` skill.

## File naming

`/sessions/blissful-magical-hawking/mnt/Technical Projects/bc-enrichment-[company-slug]-[YYYY-MM-DD].docx`

Slug rules: lowercase, spaces → hyphens, strip punctuation. "Smithsonian Institution" → `smithsonian-institution`. "AT&T" → `att`.

## Document settings

- Page size: Letter (8.5 x 11)
- Margins: 1" all sides
- Font: Calibri 11pt body, Calibri 14pt section headers, Calibri 18pt title
- Line spacing: 1.15
- Section breaks between major sections for clean page flow when printed

## Section-by-section spec

### Title block (top of page 1)

```
[Company Name] — OSI Global Account Intel
Generated: [April 21, 2026]
OSI Owner: [Name] [if Bri & Adam Biz, append "(Bri & Adam Biz)"]
```

Title in bold 18pt. Meta line in italic 10pt gray.

### Section 1 — Executive Summary

3–5 sentences in plain prose. No bullets, no headers within the section. Hits:
- Current state of OSI's relationship with the account
- What's changed recently (news, hires, departures, intent)
- The one strategic move Brian should make this week

Example tone: *"Smithsonian has been a lapsed target — no deals since 2022 but we quoted Cisco voice work last July. Three new network hires in the past 90 days suggest a refresh cycle is underway, and ZoomInfo shows intent surging on DWDM and third-party maintenance. The right play is a warm reconnect to Mark Tiamson and a parallel cold into the new VP of Infrastructure."*

### Section 2 — OSI Footprint (HubSpot)

Start with one sentence of context: *"HubSpot shows [total GP] in lifetime GP across [N] deals. Last activity was [date]. Lifecycle stage: [stage]."*

Then two tables:

**Deal history** (sorted by close date, most recent first):
| Deal Name | Amount | GP (iqmargin) | Stage | Close Date |

**Contact history** (sorted by last contacted, most recent first):
| Name | Title | Email | Last Contacted | Owner |

Then a subsection **Recent Activity** with chronological notes from the last 12 months in plain prose. Group by month. Skip if nothing logged.

### Section 3 — Account Signals (ZoomInfo)

Four subsections, each as a short paragraph (no bullets unless listing news headlines):

**Strategic posture** — 2–3 sentences synthesizing `account_research` output. What is this company focused on right now, and what's changed.

**Recent news (last 90 days)** — bulleted list of headlines with dates and source. Cap at 10 items. Format: `[Date] — [Headline] (source)`

**Analyst scoops** — one paragraph summarizing verified project signals from `enrich_scoops`. If there are multiple scoops, list each as its own bullet with the scoop type, date, and one-line summary.

**Intent topics** — single paragraph naming the top 3–5 OSI-relevant topics the account is researching, with relative intensity if available.

### Section 4 — Decision-Makers (LinkedIn Sales Navigator)

Intro sentence with the count: *"Sales Nav returned [N] decision-makers in IT, Engineering, and Operations at [Company]."*

Table:
| Name | Title | Tenure | LI Degree | In HubSpot? | Heat Score |

Sort by Heat Score descending. Bold the top 5 rows.

### Section 5 — Recent Hires (Last 90 Days)

Intro: *"[N] people joined [Company] in the last 90 days in IT/Engineering/Operations roles."*

Table:
| Name | Title | Previous Company | Start Date | LI URL |

If any previous company is a known OSI customer, bold that cell and add a footnote: *"Warm path — [Previous Company] is an active OSI account."*

### Section 6 — Job Changes (Last 6 Months)

Two subsections:

**Departed champions** — HubSpot contacts who no longer show the account on LinkedIn. For each: old title at this account, new company, new title, LI URL. These are outreach opportunities at the new company.

**New arrivals from known employers** — people who joined this account from companies where OSI has connections or existing business. Warm intro potential.

If either subsection is empty, write one sentence noting that and move on.

### Section 7 — Warm Paths (1st-Degree Connections)

One-line intro: *"[N] 1st-degree connections at [Company]."*

Table (no heat score here — warmth is the heat):
| Name | Title | How You Know Them |

"How You Know Them" pulls from LI's relationship hints (shared past employer, shared school, shared group) when visible. If LI shows nothing, leave blank.

### Section 8 — Recommended Plays

The top 3–5 contacts from the Heat Score ranking. For each, a named subsection with a short paragraph:

**[Name], [Title]**
Why they matter. Suggested angle (Systain TPM, Smartoptics optics, memory upgrade, hardware refresh alternative, pro services, specific OEM). One sentence on the opening hook — what recent signal to reference in the first touch.

These are the contacts that get HubSpot tasks in Phase 6.

### Section 9 — Gaps and Open Questions

Plain prose. 2–4 sentences covering:
- What ZI and LI didn't reveal
- Properties that would sharpen the ICP fit if we had them
- Questions for Brian to answer on the next discovery call

### Section 10 — Appendix: Raw Data Summary

Simple table:
| Source | Count |
| ZoomInfo contacts pulled | |
| LinkedIn leads scraped | |
| HubSpot contacts found | |
| HubSpot deals found | |
| New contacts added to HubSpot | |
| Outreach tasks created | |

Plus a final line: *"Full logs: [link to workspace folder or note that raw data was not exported]"*

## Formatting details

- Tables: header row bold, no alternating row shading, thin single-line borders
- Dates: write as `April 21, 2026` in prose, `2026-04-21` in tables, `4/21/26` only when space-constrained
- Money: `$123,456` with comma separators, no cents
- Heat Score: render as `7/10`, bold when ≥8
- LI URLs: hyperlink the name, don't show the full URL in the cell
- Footnotes: use the docx skill's footnote support; keep body text clean

## Prose style

This report is for Brian to read before a meeting or outreach push. Write in direct, specific sentences — the kind of briefing note a sharp analyst would hand over in person. Avoid AI-isms (run through the humanizer mentally as you draft):

- No "landscape," "tapestry," "underscores," "key" as filler
- No rule-of-three lists where two or four items would be more natural
- No em dash chains
- No signposting ("Let's dive into the signals…")
- Opinions are welcome — if something looks like a stretch, say so

## When sections are empty

Don't delete empty sections. Replace their contents with a single line like *"No recent news logged in the last 90 days."* or *"No 1st-degree connections at the account."* This keeps the report structure consistent across accounts and makes gaps obvious at a glance.
