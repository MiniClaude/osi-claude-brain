---
name: bc-greenfield-nocigs
description: >
  Cross-reference a LinkedIn Sales Navigator people-search URL against Brian's HubSpot CRM. Labels each person: GREENFIELD (not in HubSpot), MY ACCOUNT OK (Brian owns the company), [Rep Name]'s Account (another rep owns it), or UNOWNED (in HubSpot, no owner). Outputs a bucketed markdown report with rep names (not IDs) and company variant matching. ALWAYS use when Brian pastes a linkedin.com/sales/search/people URL or says: "greenfield search", "Sales Nav greenfield", "who's not in my CRM", "cross-reference this Sales Nav list", "find greenfield from this URL", "who can I work from this search", "bc-Greenfield-NoCigs", "no cigs", or any variation of wanting to know who in a Sales Nav search is already in HubSpot vs. net-new. Trigger any time a Sales Nav URL appears — even without an explicit question.
---

# bc-Greenfield-NoCigs (v2 — Enhanced Variant & Rep Name Matching)

You are helping Brian Charrette (bc@osihardware.com), a senior sales rep at OSI Global, identify which people in a LinkedIn Sales Navigator search are truly "greenfield" — meaning the **company is available for Brian to work** (either owned by him or unowned in HubSpot) AND the person is not yet a contact in HubSpot.

> **Critical definition — GREENFIELD means TWO things must both be true:**
> 1. The person is NOT already a contact in HubSpot
> 2. Their company is either owned by Brian OR unowned/not yet in HubSpot
>
> A person at Oracle, SAIC, Lockheed Martin, or CrowdStrike who isn't in HubSpot is NOT greenfield if another rep owns that company. The company availability check is mandatory for every single person, regardless of whether the contact exists.

---

## Step 0: Confirm the Sales Nav URL

If Brian has not yet pasted a Sales Nav URL, ask him for one now. The URL should look like:
`https://www.linkedin.com/sales/search/people?...`

If he has already pasted it (in this message or earlier in the conversation), proceed immediately.

---

## Step 1: Navigate and Scrape LinkedIn Sales Navigator

Use Claude in Chrome to navigate to the URL. LinkedIn Sales Navigator renders cards dynamically — use the `salesApiLeadSearch` API approach:
1. Navigate to the URL and let it load.
2. Start network request tracking (`read_network_requests`) to capture the `salesApiLeadSearch` API call.
3. Use `javascript_tool` to fetch the API response directly from the browser session and store it in `window._liData`.
4. Extract all 25 people: Full Name, Current Title, Current Company, Sales Nav profile URL.

If login is required, stop and tell Brian he needs to be logged in.

---

## Step 2: Resolve Brian's HubSpot Owner ID & Set Up Rep Name Lookup

Call `search_owners` with email "bc@osihardware.com" once at the start. Store the `ownerId` — you'll compare every company's `hubspot_owner_id` against this number throughout the run.

**Important: For Step 3a, you'll also need a mapping of owner IDs to rep names.** When you encounter an `hubspot_owner_id` that's NOT Brian's and NOT null, call `search_owners` with that `ownerId` to look up the owner's name. Cache these lookups so you don't repeat them.

---

## Step 3: Check EVERY Company First, Then the Contact

This is the core of the skill. For each of the 25 people, you must check **both** the company AND the contact. Do these in parallel batches of 5 for speed.

### 3a. Look up the company in HubSpot (with variant matching)

Search by company name using a **three-tier approach** to handle legal entity variations:

**Tier 1: Exact/fuzzy match by company name**
- Use `search_crm_objects` (object type: `companies`) searching by the company name from LinkedIn.
- If found, record company ID and owner info. Stop here.

**Tier 2: Company name variants (if Tier 1 found nothing)**
- Generate common variants: remove LLC/Inc/Corp/Ltd/Co. suffixes, try without them
- Example: "CBTS" + "CBTS Technology Solutions LLC", "CBTS Inc", etc.
- Search HubSpot for each variant. Stop at first match.
- Why this matters: CBTS (standalone) wouldn't find "CBTS Technology Solutions LLC" on exact match, but variant matching catches it.

**Tier 3: Domain/website matching (if Tiers 1-2 found nothing)**
- Extract domain from LinkedIn profile (if visible) or infer from company name
- Search HubSpot companies by `website` field containing that domain
- Example: LinkedIn shows "cbts.com" → search HubSpot for companies with website containing "cbts.com"

**Company outcomes (after checking all 3 tiers):**
- **Company NOT in HubSpot after all 3 tiers** → Company is available. Proceed to contact check (Step 3b).
- **Company found, `hubspot_owner_id` = Brian's ID (213536174)** → ✅ Brian's account. Proceed to contact check (Step 3b).
- **Company found, `hubspot_owner_id` = someone else** → ⚠️ OTHER REP'S ACCOUNT. Look up the owner name via `search_owners` using that `ownerId` and label with their NAME (not ID, e.g., "Andy M." not "204059656"). **Skip the contact check — this person is off-limits regardless.**
- **Company found, `hubspot_owner_id` = null/blank** → 🔲 UNOWNED. Proceed to contact check (Step 3b).

### 3b. Look up the contact in HubSpot (only for available companies)

Only run this step if Step 3a determined the company is available (Brian's, unowned, or not in HubSpot).

Use `search_crm_objects` (object type: `contacts`) filtering by `firstname` + `lastname`. If the name is common, also filter by company name to narrow results.

**Contact outcomes (combined with company result):**
- **Contact NOT found + Company is Brian's** → 🟢 GREENFIELD (new person, Brian's account)
- **Contact NOT found + Company unowned or not in HubSpot** → 🟢 GREENFIELD (fully net-new)
- **Contact IS found + Company is Brian's** → ✅ MY ACCOUNT (already tracked by Brian — not greenfield, but worth knowing)
- **Contact IS found + Company unowned** → 🔲 UNOWNED (contact already in CRM, company up for grabs)

> **Why the company check comes first:** Brian could have hundreds of people on a Sales Nav page who aren't in HubSpot as contacts, but whose companies are owned by other reps. Calling those "greenfield" wastes Brian's time and causes territory conflicts. The company owner is the gate — if the company is off-limits, the person is off-limits, period.

---

## Step 4: Build the Output Report

Once all 25 people are labeled, assemble a markdown report in this exact structure:

```
# Greenfield Report — [Search Description or URL snippet]
**Date:** [Today's date]
**Results scraped:** [N] people from page [X]

---

## 🟢 GREENFIELD — Not in HubSpot ([count])
These people are completely new — no contact record exists in CRM.

| Name | Title | Company | LinkedIn |
|------|-------|---------|----------|
| Jane Doe | Network Engineer | Acme Corp | [Profile](url) |

---

## ✅ MY ACCOUNTS — OK to Work ([count])
These people are in HubSpot and their company is assigned to Brian.

| Name | Title | Company | LinkedIn |
|------|-------|---------|----------|

---

## 🔲 UNOWNED — No Account Owner ([count])
These people are in HubSpot but their company has no assigned owner. Fair game — but verify before outreach.

| Name | Title | Company | LinkedIn |
|------|-------|---------|----------|

---

## ⚠️ OTHER REPS' ACCOUNTS ([count])
These people's companies are owned by another rep. Do not pursue without checking first.

| Name | Title | Company | Rep Name | LinkedIn |
|------|-------|---------|----------|----------|
| John Smith | IT Director | BigCo | Andy M. | [Profile](url) |

---

## Summary
- 🟢 Greenfield: X
- ✅ My Accounts OK: X
- 🔲 Unowned: X
- ⚠️ Other Reps: X
- **Total checked:** X
```

**Important:** In the "⚠️ OTHER REPS' ACCOUNTS" table, use the rep's **NAME** (e.g., "Andy M.") instead of owner ID (e.g., "204059656").

---

## Step 5: Save and Present the Report

1. Save the report as a `.md` file to Brian's workspace:
   `C:\Users\MINI OSI RIG\OneDrive - OSI Hardware\Documents\Claude\OSI-Brain\BC Enrichment\Greenfield_[SearchName]_[YYYY-MM-DD].md`

2. Provide the `computer://` link so Brian can open it.

3. In your chat response, give Brian a quick plain-text summary — just the counts and a one-line observation (e.g., "12 greenfield, 6 mine, 4 other reps, 3 unowned").

4. Add a note if any corrections were made (e.g., "Note: CBTS caught by variant matching, moved from greenfield to Other Reps").

---

## Step 6: Offer the Next Page

After presenting results, ask:
> "Want me to pull the next page too?"

If yes, navigate to the next page of results (click the Next button in Chrome) and repeat from Step 1. Append results to the same report file, clearly marking them as `Page 2`, `Page 3`, etc.

---

## Important Notes

**Company variant matching:** ALWAYS run all 3 tiers (exact, variants, domain) even if early tiers find nothing. This prevents false greenfields like "CBTS" when "CBTS Technology Solutions LLC" is already in HubSpot.

**Rep name lookup:** Cache owner ID → rep name mappings so you don't call `search_owners` multiple times for the same rep. If a rep name can't be found, fall back to "Rep [OwnerID]" in the report.

**Ambiguous names:** If a contact search returns multiple results with the same name, pick the one whose current company best matches the Sales Nav company. If still ambiguous, note the person as `⚠️ AMBIGUOUS MATCH — verify manually` and treat as found (flag it, don't call greenfield).

**Speed tip:** HubSpot lookups can be batched in groups — don't wait for one to finish before starting the next if you can parallelize. Check every single person; don't skip anyone to save time.

**Domain extraction:** When extracting domain from LinkedIn, look for email domain, company website, or company URL in the profile. If none visible, try parsing the company name (e.g., "Acme Tech" → "acmetech.com" is a reasonable guess, but only use this as a last resort — prioritize visible domain/website data).
