# HubSpot data quality — hard requirements for any contact write

Used by qualification when creating or updating a HubSpot contact for a ✅ Yes verdict.

If any required field is missing or wrong, STOP. Research harder, then retry. Do NOT write a partial record.

## Required fields per save

| Field | Source | Format | Hard/Soft |
|---|---|---|---|
| `firstname`, `lastname` | LinkedIn | As shown | Hard |
| `jobtitle` | LinkedIn top card (authoritative — overwrite stale HubSpot value) | Current title | Hard |
| `company` | LinkedIn | Current employer | Hard |
| `email` | ZoomInfo (verified 80+) or existing HubSpot | Standard | Soft (note "not found" if ZI returns nothing) |
| `phone` | ZoomInfo `phone` (direct dial) or existing HubSpot | `+1 (XXX) XXX-XXXX` for US/CA | Hard format |
| `mobilephone` | ZoomInfo `mobilePhone` ONLY | `+1 (XXX) XXX-XXXX` for US/CA | Hard format. NEVER company switchboard. |
| `city`, `state` | LinkedIn location field | As shown | Hard |
| `hs_timezone` | Andy's 6-bucket from LinkedIn city/state | One of: `us_slash_eastern`, `us_slash_central`, `us_slash_mountain`, `us_slash_pacific`, `us_slash_alaska` (US Alaska), `canada_slash_atlantic` (Canada Atlantic). Outside these six → closest match. Never use city-specific values. | Hard |
| `hs_linkedin_url` | Sales Nav URL (`linkedin.com/sales/lead/[ID]/`) OR `linkedin.com/in/...` | Full URL | Hard |

## Phone format
- US/Canada: `+1 (XXX) XXX-XXXX` — space after `+1`, parens around area code, space, hyphen before last 4.
- Example: `+1 (440) 567-7444`.
- Upgrade existing data: `(416) 353-7591` → `+1 (416) 353-7591`.
- Non-US/CA: `+[country code] [number]`.

## Mobile phone — never violate
- Direct mobile/cell ONLY.
- Never company main / switchboard.
- If ZoomInfo returns no mobile, leave BLANK. Never substitute.

## Job title — always refresh from LinkedIn
HubSpot titles go stale. LinkedIn top card is source of truth. Overwrite even if HubSpot has a value. Fallback if LinkedIn unreachable: ZoomInfo `jobTitle`. Only if neither, leave existing HubSpot value.

## Associated company — always link
Before creating/updating a contact, search HubSpot for the company by name. If found, associate via `associations` parameter. If not in HubSpot, create the company first (owner: 196669355, name from LinkedIn), then associate. Never leave a contact orphaned — unlinked contacts break stagger logic, deal tracking, reporting.

## Pre-write checklist (run before every save)

1. `jobtitle` is current (LinkedIn top card, not HubSpot)
2. `phone` formatted `+1 (XXX) XXX-XXXX` (if US/CA)
3. `mobilephone` formatted OR blank (never HQ)
4. `hs_timezone` set (one of 6 buckets)
5. `hs_linkedin_url` set (full URL)
6. Associated company record exists and linked

If any check fails: FIX or leave the field blank. Do NOT write partial.
