---
name: bc-salesnav-greenfield
description: >
  Cross-reference a LinkedIn Sales Navigator people-search URL against Brian's HubSpot CRM
  to surface greenfield prospects (people NOT yet in HubSpot) versus people already in the
  CRM. ALWAYS use this skill when Brian pastes a LinkedIn Sales Navigator search URL
  (linkedin.com/sales/search/people) and wants to know who's already in HubSpot vs. who's
  net-new for him to work. Also triggers on phrases like "greenfield search", "Sales Nav
  greenfield", "who's not in my CRM", "cross-reference this Sales Nav list", "is anyone
  here in HubSpot", "find greenfield from this URL", "who can I work from this search",
  or any variation of pasting a Sales Nav search URL with the goal of identifying clean
  prospects he can pursue without stepping on another rep's account or duplicating
  existing CRM contacts. Outputs a clean markdown file Brian uses to manually decide who
  to qualify and add to HubSpot.
---

> **SYNC NOTE — READ BEFORE EDITING:** The source of truth for this skill lives at
> `OSI-Brain\Skills\bc-salesnav-greenfield\SKILL.md` inside Brian's Mini Chamber vault.
> The version installed under `.claude/skills/` is read-only. To change this skill: edit
> the source file, package as a `.skill` file, install it. Never manually edit the
> `.claude/skills/` copy.

# Sales Nav Greenfield Cross-Reference Skill (Brian's version)

Operating principle: surface clean greenfield prospects from a Sales Nav search. No
fabrication, no guessing, no auto-creating HubSpot records. Brian decides who to qualify
and who to add. The skill's job is to deliver a trustworthy, ranked markdown file fast.

---

## ⚠️ CRITICAL RULES

1. **No fabricated people.** Only list people you directly observed on the rendered Sales
   Nav page. If you can't see them, they don't exist for the purposes of this skill.
2. **No HubSpot writes.** Do NOT create contacts, do NOT create tasks, do NOT change
   anything in HubSpot. This skill is read-only against HubSpot. Brian will manually run
   `bc-prospect-qualification` on the people he wants to pursue and add them himself.
3. **First page only.** Process roughly the first 25 results that load on the initial
   Sales Nav page. Do not paginate further unless Brian explicitly asks.
4. **No em-dashes anywhere in the output file.**

---

## Workflow

### Step 1 — Confirm the Sales Nav URL

Brian pastes a Sales Navigator URL that looks like
`https://www.linkedin.com/sales/search/people?query=...`. If the URL is missing or
malformed, ask Brian to paste it again before doing anything else.

Briefly summarize the search filters back to Brian in chat so he can confirm scope before
you spend time. Pull the filter values directly out of the URL — for example:
"Sales Nav search: IT function, headcount 1001+, titles include Network Manager / Director
of IT / System Architect / etc., region Texas. I'll cross-check the first 25 results
against HubSpot. Sound right?"

If anything looks wrong, stop and clarify. Otherwise proceed.

### Step 2 — Navigate to the Sales Nav URL via Claude in Chrome

Use the Claude in Chrome MCP. Preferred tool order:

1. `mcp__Claude_in_Chrome__navigate` to the exact URL Brian pasted.
2. `mcp__Claude_in_Chrome__get_page_text` first — it loads all visible result cards in
   one shot.
3. If `get_page_text` returns weak or partial output, fall back to
   `mcp__Claude_in_Chrome__read_page` with depth 5.

Wait for the result list to render fully before scraping. If Sales Nav shows a login wall
or session-expired screen, stop and tell Brian he needs to log in to LinkedIn in Chrome.
Do not attempt any auth bypass.

### Step 3 — Extract the First Page of Results

For each person card visible on the first page (~25 results), capture:

- **Full name** (exactly as shown). If the result is privacy-blocked and shows only a
  first name + last initial, capture what's there and flag it as `(partial name)` in the
  output.
- **Current title** (exactly as shown).
- **Current company** (exactly as shown).
- **Sales Nav lead URL** (`https://www.linkedin.com/sales/lead/[ID]/...` from the card).
- **Public LinkedIn profile URL** if visible (`linkedin.com/in/...`). If not directly
  visible on the search card, you can leave it blank rather than fabricate.
- **Location** if shown on the card (helpful when multiple people share a name).

Save these to an in-memory list. Keep the original Sales Nav search-result order — that
is the order Brian will scan in the output.

### Step 4 — Cross-Reference Each Person Against HubSpot

For every person captured, run a HubSpot lookup before writing the output. Use the HubSpot
MCP tools available in this session — typically:

- `search_crm_objects` against object type `contacts`
- Match logic: **first name + last name + company name**
- If no match by full name, try a secondary search by `firstname + lastname` only and
  manually verify the company on the returned record.

For each person, classify into one of three buckets:

| Bucket | Rule |
|---|---|
| 🟢 **Greenfield** | No HubSpot contact found matching name + company. Net-new for Brian. |
| 🟡 **In CRM — Brian-owned** | HubSpot contact exists AND owner = Brian Charrette (bc@osihardware.com). |
| 🔴 **In CRM — other rep** | HubSpot contact exists AND owner is someone other than Brian. Capture the owner's name. |

For every match, capture: HubSpot contact ID, HubSpot contact URL, owner name, last
activity date if available. Use `search_owners` to resolve owner IDs to names.

**Partial-name handling.** If Sales Nav showed only a first name + last initial, do NOT
assume "no match" if HubSpot returns nothing. Note the limitation in the output and let
Brian decide whether to dig.

**Common-name handling.** If multiple HubSpot contacts share the same first + last name,
use the company match to disambiguate. If still ambiguous, flag the person as
`⚠️ Ambiguous` and let Brian resolve.

### Step 5 — Write the Markdown Output

Save to:
`SalesNav_Greenfield_[YYYY-MM-DD]_[HHMM].md` in the outputs folder.

Use this exact structure. No em-dashes anywhere.

```
# Sales Nav Greenfield Report
**Run date:** [Day, Month DD, YYYY HH:MM ET]
**Sales Nav search:** [one-sentence plain-English description of the filters from the URL]
**Source URL:** [paste the full Sales Nav URL Brian provided]
**Results processed:** [N] of first page
**Summary:** [X] greenfield, [Y] Brian-owned, [Z] owned by other reps

---

## 🟢 Greenfield (Net-New for Brian)

These people are not in HubSpot and are clean targets for outreach.

| # | Name | Title | Company | Location | Sales Nav | LinkedIn |
|---|------|-------|---------|----------|-----------|----------|
| 1 | [Name] | [Title] | [Company] | [Location] | [Sales Nav URL] | [/in/ URL] |
| 2 | ... | | | | | |

---

## 🟡 In CRM — Brian-owned

These already exist in your HubSpot under your ownership. Use as warm reactivation, not new outreach.

| # | Name | Title | Company | HubSpot Contact | Last Activity |
|---|------|-------|---------|-----------------|---------------|
| 1 | [Name] | [Title] | [Company] | [HubSpot URL] | [Date] |

---

## 🔴 In CRM — Owned by Another Rep

Do NOT outreach without checking with the rep. Listed here for awareness.

| # | Name | Title | Company | Owner | HubSpot Contact | Last Activity |
|---|------|-------|---------|-------|-----------------|---------------|
| 1 | [Name] | [Title] | [Company] | [Rep Name] | [HubSpot URL] | [Date] |

---

## ⚠️ Ambiguous / Needs Manual Check

Privacy-blocked names, partial-name matches, or multiple HubSpot records with the same name where company didn't disambiguate.

| # | Name (as shown) | Title | Company | Why flagged |
|---|------|-------|---------|-------------|
| 1 | [Tim W.] | [Network Architect] | [Acme Corp] | Privacy-blocked, partial last name |

---

## Recommended Next Steps

1. Pick the most interesting greenfield rows above.
2. Run them through `bc-prospect-qualification` to confirm OSI fit before outreach.
3. For confirmed Yes verdicts, manually create the HubSpot contact (with LinkedIn URL) and run a sequence.
4. For 🔴 other-rep rows where activity is stale (90+ days) and the contact is not a customer, consider requesting the account.
```

### Step 6 — Chat Summary

After saving the file, give Brian a short chat summary:

- How many people were on the Sales Nav page (and confirm it was first-page only)
- Bucket counts: greenfield / Brian-owned / other-rep / ambiguous
- The 3 to 5 most promising greenfield rows by title fit (call out new-to-role signals if visible)
- Any auth or scraping issues encountered
- File link to the markdown output

Keep the summary short. The markdown file is the deliverable — don't duplicate it in chat.

---

## Edge Cases & Error Handling

- **Sales Nav login wall or session expired.** Stop. Tell Brian to log in. Do not retry
  automatically more than once.
- **Page text comes back empty or as JS placeholders.** Wait a few seconds, retry
  `get_page_text` once, then fall back to `read_page` depth 5. If still empty, tell Brian
  the page didn't render and offer to retry.
- **HubSpot MCP unavailable or rate-limited.** Capture all the people from Sales Nav, then
  output the markdown with a clearly marked "HubSpot lookup failed — all rows are unverified"
  banner at the top, and skip the bucketing.
- **Fewer than 25 results on the page.** That's fine. Process whatever rendered. Note the
  actual count in the summary.
- **More than 25 results visible (Sales Nav loaded extra cards via scroll).** Cap at 25
  unless Brian explicitly said "process all" or "go deeper".
- **A person's company on Sales Nav differs from their company in HubSpot.** That usually
  means a job change. Flag in the Ambiguous section with note "Company mismatch with
  HubSpot — possible job change".

---

## What This Skill Is NOT

- It is not a replacement for `bc-prospect-qualification`. This skill does NOT score OSI
  fit. It only tells Brian who's clean to work.
- It is not an account-enrichment skill. It does not pull existing HubSpot contacts at the
  same companies, does not create tasks, and does not run on a schedule.
- It is not a writer of outreach. After Brian picks the greenfield rows he wants to
  pursue, he'll run those through other skills (qualification → sequence builder).

---

## Quality Bar

Before finishing, ask:

- Did I actually navigate to the Sales Nav URL and read the rendered page, or did I guess?
- Is every name in the markdown a real person Brian can click through to right now?
- Did I check HubSpot for every person, or did I skip some?
- Are the bucket counts in the summary accurate?
- Would Brian open this file and immediately know who to work first?
