# Email Pattern Resolver

Single source of truth for resolving the right email address for a prospect. Every skill that creates HubSpot contacts, queues emails, or runs pre-flight checks should follow this exact algorithm. ZoomInfo is enrichment, not authority, the authority is HubSpot's engagement signal at the same company.

## Why this exists

ZoomInfo returns pattern-guessed emails (often `firstinitial+lastname@domain`) that are frequently wrong because:
- ZoomInfo guesses based on a single observation, not on what actually delivers.
- Companies change email conventions over time; ZoomInfo's data goes stale.
- HubSpot already holds primary emails that humans typed, sent to, and got replies from. That's ground truth.

A 2026-04-27 incident: ZoomInfo gave `jlubeck@midco.com` for John Lubeck. HubSpot already had him at `john.lubeck@midco.com`. The prospecting flow created a dupe and queued 6 emails to the wrong address. This algorithm prevents that.

---

## Step 1, HubSpot-first contact lookup

Before any new contact creation or any queue write:

1. Search HubSpot contacts by `firstname + lastname + company`. Match by company name OR company domain.
2. If exactly one match → use that contact. Use its `email` field as the send target. Done, skip Step 2.
3. If multiple matches → flag for manual review. Do NOT create a new record. Do NOT queue an email.
4. If zero matches → continue to Step 2.

Do not search HubSpot by the ZoomInfo-supplied email alone. ZoomInfo's email may be wrong, return zero hits, and falsely indicate "new contact" when one already exists under a different address.

---

## Step 2, Verified company pattern

When no existing HubSpot contact matches, derive the company's verified email pattern from engagement signals (NOT from the most-common stored format).

### Pull contacts at the same company

Search HubSpot for all contacts whose `company` field matches the target. Pull these properties:
- `email`
- `hs_email_replies_total`
- `hs_email_open`
- `hs_email_bounce`
- `hs_email_bad_address`
- `hs_email_last_reply_date`
- `hs_email_last_open_date`

### Bucket contacts by pattern

Identify the email's local-part shape:
- `firstname.lastname` → e.g. `john.lubeck@`
- `firstinitial+lastname` → e.g. `jlubeck@`
- `firstname` → e.g. `john@`
- `firstname_lastname` → e.g. `john_lubeck@`
- `lastname.firstname` → e.g. `lubeck.john@`
- `firstinitiallastnameinitial` → e.g. `jl@`
- `other` → catch-all

Use the contact's `firstname`/`lastname` properties to test which shape its `email` matches. Skip contacts where shape can't be determined.

### Score each pattern

For each pattern bucket, compute:
- **+5** per contact in the bucket with `hs_email_replies_total > 0`
- **+1** per contact with `hs_email_open > 0` and no replies
- **−10** per contact with `hs_email_bounce > 0` or `hs_email_bad_address = true`
- **0** for contacts with no engagement signal at all

Apply a recency decay on opens and replies: any signal older than 12 months counts at ¼ weight (use `hs_email_last_reply_date` / `hs_email_last_open_date`).

### Pick the verified pattern

- If the highest-scoring pattern has `score >= +5` AND beats every other pattern by at least 5 points → it's verified. Use this pattern to construct the prospect's email.
- If no pattern reaches +5 OR top two are within 5 points of each other → **insufficient signal**. Fall back to Step 3.

---

## Step 3, Fallback when engagement signal is missing

When Step 2 says insufficient signal:

1. Look at ALL contacts at the company in HubSpot.
2. If ≥60% of them share one pattern → use that pattern (the original "dominant pattern" rule).
3. If no pattern dominates OR fewer than 5 contacts exist at the company → mark as **manual verification required**. Do NOT auto-pick. Surface to Andy in the pre-flight summary.

---

## Step 4, Handling the ZoomInfo alt email

When ZoomInfo gives an email that differs from the chosen address (whether HubSpot match in Step 1 or constructed from verified pattern in Step 2):

1. Add the ZoomInfo email to the contact's `hs_additional_emails` field (semicolon-separated if multiple already exist).
2. Prepend a single line at the top of the contact's strategy notes / about field:
   > `ALT EMAIL <YYYY-MM-DD>: ZoomInfo lists <zoominfo-email>. Using <chosen-email>. Pattern check: <pattern-name> verified by <N replies, M opens, K bounces>.`
3. Do NOT change the primary email. The HubSpot primary or constructed verified address wins.

This way Andy sees the alternate option at the top of the contact whenever he reviews before sending, without it leaking into the prospect-facing email body.

---

## Output format for any caller

Every skill that runs this resolver should produce one line per prospect:

```
Resolved <Name> / <Company>:
  email = <chosen-address>
  source = <hubspot-existing | verified-pattern | dominant-pattern | manual-required>
  pattern = <firstname.lastname | jinitial+lastname | etc>
  signal = <N replies, M opens, K bounces over X contacts>
  alt = <zoominfo-email or none>
```

Anything that resolves to `manual-required` MUST be flagged in the daily monitor and never auto-queued.

---

## Pre-flight risk surfaces

The osi-monitor skill uses this resolver to flag any pending queue entry where:
- The `to:` address pattern doesn't match the company's verified pattern.
- The `to:` address shares a pattern with an address that bounced at the same company in the last 30 days.
- Anyone at the same company has replied in the last 7 days (whether to us or otherwise).

Each gets surfaced in a "PRE-FLIGHT RISKS" section so Andy can swap or hold before send.
