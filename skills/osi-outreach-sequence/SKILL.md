---
name: osi-outreach-sequence
description: >
  Drafts the 6-email outreach sequence for ONE qualified OSI Global prospect. Reads
  the strategy note + Personal Hook + Fresh Hook from HubSpot, picks sequence type, computes
  Day 1 from same-company stagger metadata, drafts all 6 emails, writes them to the contact's
  HubSpot AI fields (ai_email_subject_1-6 + ai_email_body_1-6), creates a LINKED_IN_CONNECT
  task on Day 1 as Andy's enrollment cue, and appends Excel Tab 1. Triggers when invoked by
  osi-prospect-qualification's handoff on a Yes-with-email verdict.
---

> Source: `C:\Claude-Brain\skills\osi-outreach-sequence\` (Git, github.com/Drrewdy/Claude-Brain). Edit source, repackage, install.

# OSI Outreach Sequence

---

## 🚨 STOP -- DID YOU READ OSI-PROSPECT-QUALIFICATION THIS SESSION? (added 2026-05-08)

This skill handles sequencing only. It does not govern candidate discovery, LinkedIn browsing, or Company Mode search. All of that lives in `osi-prospect-qualification`.

If you are running Company Mode and you have NOT read `C:\Claude-Brain\skills\osi-prospect-qualification\SKILL.md` in this session: **STOP. Read it now. Then proceed.**

**Why this rule exists:** 2026-05-08, a Company Mode run on D.E. Shaw read the outreach skill but not the qualification skill. The Round 0 mandatory card browse was skipped. Matt Kong, Leonardo Palazzo, and Michael De Candia were all missed as a result.

---

## 🛑 HARDWIRED RULE, NO EMPLOYER VERIFICATION, NO SEQUENCE

This skill only runs when invoked via handoff from `osi-prospect-qualification` after a Yes-with-email verdict backed by Path A (full LinkedIn read) or Path B (ZoomInfo + corporate-domain email + dated web-search confirmation). If the strategy note is missing, employer verification is missing, or the verdict was anything other than Yes-with-email: this skill does not run.

---

## 🛑 HARDWIRED RULES

**This skill DOES:**
- Read the strategy note from HubSpot (Personal Hook, Fresh Hook, sequence type)
- Active sequence check (checks if AI fields already populated on the contact)
- Approved Vendor check (`Claude-Brain/approved-vendors.json`)
- Compute Day 1 from same-company stagger metadata
- Draft 6 emails using the formatting standard below
- Write all 12 AI field properties to the HubSpot contact in one call (`ai_email_subject_1-6` + `ai_email_body_1-6`)
- Create a LINKED_IN_CONNECT task on Day 1 (this is Andy's cue to enroll the contact in the HubSpot sequence)
- Append a Tab 1 row to `Claude-Brain/prospects-tracker-new.xlsx`
- Update stagger metadata (`last_day1`, `person_count`)

**This skill DOES NOT:**
- Write to `email-queue.json`. The queue is no longer used for new sequences.
- Compute sendDates or sendTimes. HubSpot sequences handle cadence once enrolled.
- Invoke osi-email-sender. Sending is handled by HubSpot after Andy enrolls.
- Qualify. Verdict is `osi-prospect-qualification`'s job.
- Run on multiple candidates at once. ONE per invocation.
- Navigate to LinkedIn. All context comes from the handoff payload and HubSpot strategy note.
- Ask Andy for approval mid-run. AI field writes and task creation are automatic. Andy approved at session start.
- Stop for `manage_crm_objects` confirmation prompts. ALL calls use `confirmationStatus: "CONFIRMATION_WAIVED_FOR_SESSION"`.

---

## 🛑 STEP -1: TOOL PREFETCH (MANDATORY if not already done this session)

If osi-prospect-qualification already ran its prefetch earlier in this conversation, skip this step.

If running standalone, fire these TWO ToolSearch calls in the same message:

```
ToolSearch({ query: "select:mcp__workspace__bash,mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__search_crm_objects,mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__manage_crm_objects,mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__get_crm_objects,mcp__4ba1185f-93a5-43f3-9910-49e11601259c__enrich_contacts,mcp__4ba1185f-93a5-43f3-9910-49e11601259c__enrich_news", max_results: 6 })
ToolSearch({ query: "select:mcp__Claude_in_Chrome__tabs_context_mcp,mcp__Claude_in_Chrome__navigate,mcp__Claude_in_Chrome__get_page_text,WebSearch,TaskCreate,TaskUpdate", max_results: 6 })
```

---

## 🛑 STEP 0, MANDATORY READ OF DRAFTING RULES

Before drafting any email, **Read `C:\Claude-Brain\playbook\drafting-rules.md` in full**. This is non-negotiable. Do NOT rely on training data.

Also **Read `C:\Claude-Brain\playbook\vertical-intel.md` in full** before drafting. It is the single source for per-vertical lead guidance and the Park Place / Service Express wedge (drafting-rules.md only points to it). Core rule: role and skills decide the lead, not industry. Optics-fit roles get optics in any vertical. Procurement and maintenance-contract owners get TPM in any vertical, banks included.

After reading both, proceed below.

---

## 🛑 HARDWIRED RULE, NO EM-DASHES OR EN-DASHES, EVER

Andy Rule #4 from `CLAUDE.md`. U+2014 (em-dash) and U+2013 (en-dash) are FORBIDDEN everywhere. Use periods to split sentences. Use commas for parenthetical clauses.

---

## 🛑 EMAIL FORMATTING STANDARD (added 2026-05-28)

These rules apply to EVERY email in EVERY sequence. No exceptions.

### Greeting
Every email starts with the prospect's first name and a comma on its own line. NO "Hi". NO "Hello". Just the name.

```
Adam,
```

### Sign-off
Every email ends with a blank line, then "Best," on its own line, then "Andy" on its own line, then a blank line.

```
[last line of body]

Best,
Andy

```

### Exception: Email 2 on Sample-Offer sequences
When Email 1 was a Sample-Offer (SFPs or DIMMs), Email 2 body is:

```
Any thoughts?

Best,
Andy

```

No greeting. No name at the top. Just "Any thoughts?" followed by the standard sign-off.

### Email 2 on Pain-Led sequences
Has the full standard formatting: first name greeting + substance + Best/Andy sign-off.

---

## INPUT

Output of `osi-prospect-qualification` handoff:
- `hubspotContactId`
- Verdict: must be `yes-with-email`
- Strategy note location (HubSpot note ID associated to the contact)
- Personal Hook (1-2 specific LinkedIn details)
- Fresh hook (30-day news summary + URL, if any)
- Recommended sequence type: one of `Sample-Offer Network`, `Sample-Offer Server`, `Pain-Led TPM`, `Pain-Led DWDM`, `Pain-Led Storage`, `Pain-Led Pre-Owned`
- Company name (for stagger lookup)
- Verified email

If any of these are missing, refuse and log. Don't proceed on partial data.

---

## OUTPUT

After this skill runs on one qualified candidate:
- 12 AI field properties written to the HubSpot contact (`ai_email_subject_1-6` + `ai_email_body_1-6`)
- LINKED_IN_CONNECT task created on Day 1 (Andy's cue to enroll in HubSpot sequence)
- Excel Tab 1 row appended
- `state.stagger[company_name].last_day1` updated to Day 1
- `state.stagger[company_name].person_count` incremented

---

## ACTIVE SEQUENCE CHECK, runs first

Before drafting anything, pull the contact's `ai_email_subject_1` field from HubSpot.

**If populated:** the contact already has a drafted sequence in the AI fields. Tell Andy:
> "Contact already has AI Email Subject 1 populated: `[first 60 chars]...`. Overwrite with a fresh sequence?"

Wait for explicit yes before proceeding. Without that, stop.

**If blank:** proceed without prompting.

---

## APPROVED VENDOR RULE

Read `Claude-Brain/approved-vendors.json`. Case-insensitive substring match on prospect's company.

**If matched:**
- Email 1: ONE soft line. "Side note, we're already on your approved vendor list, so no new vendor onboarding if anything ever needs to move fast."
- Email 3 OR 4 (pick whichever fits): "Quick reminder we're already approved at [Company] if timing matters."
- All other emails: silent.

**If not matched:** never mention it.

---

## OUTREACH FLOW

### Step 1, Read strategy note + sequence type

DO NOT navigate to LinkedIn. All context comes from the handoff payload. Use it directly.

If the handoff payload is incomplete, pull the strategy note from HubSpot and read THE PERSONAL HOOK, Fresh hook, and THE PLAY sections.

Read `Claude-Brain/playbook/product-lines.md` if sequence type is unclear.

### Step 2, Compute Day 1 (same-company stagger)

Read `state.stagger[company_name]` from `C:\Claude-Brain\overnight-candidates.json`:

| `person_count` | Day 1 |
|---|---|
| `0` | Next business day (skip weekends + holidays) |
| `1-4` | `last_day1` + 4 business days |
| `5` | `last_day1` + 10 business days (cooling gap) |
| `6+` | `last_day1` + 4 business days |

Day 1 is the date Andy should enroll the contact in the HubSpot sequence. The LINKED_IN_CONNECT task is due on this date. When Andy sees it in his task queue, that is his cue to enroll.

Skip weekends + holidays. Holiday list: `Claude-Brain/holidays.json`. Fallback: US federal holidays + Good Friday + Black Friday + Christmas Eve + New Year's Eve.

### Step 3, Duplicate-contact check (MANDATORY before drafting)

```
search_crm_objects({
  objectType: "contacts",
  filterGroups: [{filters: [
    {propertyName: "firstname", operator: "EQ", value: "<First>"},
    {propertyName: "lastname",  operator: "EQ", value: "<Last>"}
  ]}],
  properties: ["firstname","lastname","email","company","hs_object_id"]
})
```

- Exactly one result matching handoff ID: proceed.
- ID mismatch: STOP-GATE. Surface duplicate to Andy.
- Zero results: STOP-GATE.
- Multiple results: STOP-GATE. Surface all IDs for manual merge.

### Step 4, Email-pattern verification (MANDATORY before drafting)

Read the EMAIL RESOLUTION block in the contact's strategy note.

- `hubspot-existing` or `verified-pattern`: proceed.
- `dominant-pattern`: proceed, note in output.
- `manual-required`: STOP. Do not draft or write.

If no EMAIL RESOLUTION block exists, run the resolver inline per `knowledge/email-pattern-resolver.md`.

### Step 5, Write 6 Emails

**Source of truth for all drafting rules:** `C:\Claude-Brain\playbook\drafting-rules.md` (read in Step 0).

**Formatting standard for every email** (from EMAIL FORMATTING STANDARD above):
- First line: `[First name],`
- Body paragraphs
- Blank line
- `Best,`
- `Andy`
- Blank line

**Exception:** Email 2 on Sample-Offer sequences = `Any thoughts?` with no greeting, followed by the standard Best/Andy sign-off. No first name at the top.

#### Email 1 (by sequence type)

**Sample-Offer Network:**
```
[First],

I'm just prepping this package for you. I have a box of swag and a pair of sample SFPs to send from the team at OSI Global.

Do you come into the office, or is there a better address to ship it to?

Best,
Andy

```

**Sample-Offer Server:**
```
[First],

I'd like to send you a sample DIMM from our current batch. Same spec as what you're running, manufacturer warranty, won't touch your OEM support contract.

Do you come into the office, or is there a better address to ship it to?

Best,
Andy

```

**Pain-Led (TPM / DWDM / Storage / Pre-owned):**
3-4 sentences. Lead with their specific pain. Reference Personal Hook. Reference Fresh Hook if strong. One concrete ask. Pull the pain articulation and the one-line ask from `C:\Claude-Brain\playbook\pain-and-objections.md` (pain by product line).

```
[First],

[Sentence 1: Personal Hook + pain.]
[Sentence 2: One OSI angle addressing that pain. ONE product line.]
[Sentence 3 optional: Fresh hook or data point.]
[Sentence 4: ONE concrete ask.]

Best,
Andy

```

Subject: short, specific. Examples: `[Company] backbone costs`, `quick question on [stack]`, `maintenance at [Company]`.

#### Email 2

**Sample-Offer sequence:**
Subject: `Re: [Email 1 subject]`
Body:
```
Any thoughts?

Best,
Andy

```

**Pain-Led sequence:**
Subject: `Re: [Email 1 subject]`
2-3 sentences. ONE move: new data point on same pain / adjacent signal. End with ONE concrete ask (a real question, not a passive statement).

```
[First],

[New data point or signal.]
[Concrete ask ending with a question mark.]

Best,
Andy

```

#### Email 3 (new subject, STANDALONE)

Different product line. 3-4 sentences. One ask.

```
[First],

[Body. New product line only. No quoted thread, no prior email reference.]

Best,
Andy

```

🚫 No quoted thread. No `On <date>, Andy wrote:`. No `>` lines.

#### Email 4 (new subject, STANDALONE)

Another product line. Same structure as Email 3.

🚫 No quoted thread.

#### Email 5 (new subject, STANDALONE)

Another product line. Same structure as Email 3.

🚫 No quoted thread.

#### Email 6, breakup (new subject, STANDALONE)

One sentence. Clean close. No ask.

```
[First],

Should I close the file on this one, or is the timing just off?

Best,
Andy

```

🚫 No quoted thread.

### Step 6, 6-ITEM SELF-CHECK (MANDATORY before sanitize)

For every email body, answer these six questions before sanitizing:

1. Does the first line after the greeting reference the prospect, not OSI? (Email 1 only)
2. Is the Personal Hook from the strategy note in this email? (Email 1 only. If hook is thin, ABORT and flip to `pending-needs-hook`)
3. Is there exactly ONE product line in this email?
4. Did I name SmartOptics? (must be no for cold)
5. Did I claim OSI manufactures? (must be no)
6. Does every email end with the sign-off: blank line, "Best,", "Andy", blank line? (All 6 emails including "Any thoughts?" Email 2. No exceptions.)

If any answer is wrong, rewrite before sanitizing.

### Step 7, Sanitize bodies (MANDATORY before validator)

Run `sanitize_body(text, email_index)` on every body and `sanitize_subject(subject)` on every subject before writing to HubSpot. See the sanitize functions in the previous version of this skill for the full implementation. Key operations:
- Strip em-dashes and en-dashes
- Strip quoted thread markers from emails 3-6 (defense-in-depth)
- Normalize spaces
- Trim trailing whitespace

If sanitize raises (dashes leaked through or body went empty): STOP. Do not write anything. Surface the error to Andy.

### Step 8, Validator (MANDATORY before HubSpot write)

Run `validate_or_raise` on every email per `C:\Claude-Brain\scripts\validate_email.py`.

**NOTE on rule 1.11 (sign-off ban):** The validator was written for the old email-queue workflow where Outlook appended the signature. In the new HubSpot AI fields workflow, "Best, Andy" is explicitly required in the body. The validator's 1.11 sign-off check does NOT apply to this skill. All other rules apply unchanged.

If the validator raises on any other rule: log to `overnight-run-log.md`, do NOT write any AI fields, flip candidate to `pending-relookup`.

### Step 9, Write 12 AI Field Properties to HubSpot

Build all 12 field values in memory (6 subjects + 6 bodies). Write in a SINGLE `manage_crm_objects` update call. Never write partial.

```json
{
  "ai_email_subject_1": "[subject]",
  "ai_email_body_1": "[full body with formatting]",
  "ai_email_subject_2": "[subject]",
  "ai_email_body_2": "[full body]",
  "ai_email_subject_3": "[subject]",
  "ai_email_body_3": "[full body]",
  "ai_email_subject_4": "[subject]",
  "ai_email_body_4": "[full body]",
  "ai_email_subject_5": "[subject]",
  "ai_email_body_5": "[full body]",
  "ai_email_subject_6": "[subject]",
  "ai_email_body_6": "[full body]"
}
```

After write succeeds, output exactly one confirmation line:

`AI fields written: [First Last] | [Sequence type] | Enroll by [Day 1 date] | LinkedIn: [hs_linkedin_url] | HubSpot: https://app.hubspot.com/contacts/21878985/record/0-1/[hubspotContactId]`

- **LinkedIn URL:** use the contact's `hs_linkedin_url` (the profile read during qualification). If it is blank, write `LinkedIn: none on record`.
- **HubSpot URL:** build it from the portal id `21878985` and the `hubspotContactId` you just wrote to. This is a clickable link straight to the contact record.
- If a Company Mode run prints an end-of-run recap of everyone sequenced, each name in that recap carries these same two URLs.

Do NOT display email bodies in chat. Do NOT ask "ready?". Move immediately to Step 10.

### Step 10, Create LINKED_IN_CONNECT Task

🚨 **Task type is ALWAYS `LINKED_IN_CONNECT`. NEVER `TODO`.** A TODO task does not appear in the LinkedIn Sales Navigator task queue.

Search HubSpot for an existing "Sales Nav -- Send connection request" task on this contact:

**Found, NOT_STARTED:** update `hs_timestamp` to Day 1 at 20:00 UTC. Also fix `hs_task_type` to `LINKED_IN_CONNECT` if currently `TODO`.

**Found, COMPLETED:** leave it. Log: "Sales Nav connect already completed."

**Not found:** CREATE:
- Subject: `Sales Nav -- Send connection request -- [First Last] | [Company]`
- Due date: Day 1 at 20:00 UTC (4pm ET)
- Type: `LINKED_IN_CONNECT`
- Owner: 196669355
- Body: the actual LinkedIn invite message Andy will send (under 300 chars, references Personal Hook, no pitch)

This task is Andy's cue. When it appears due in his task queue, he enrolls the contact in the HubSpot sequence and sends Email 1. The task date and enrollment date are always the same.

If write fails: log `linkedin-task-sync-failed` to `overnight-run-log.md`. AI fields stay written (they are the authoritative record).

### Step 11, Update Stagger Metadata

Update `state.stagger[company_name]` in `C:\Claude-Brain\overnight-candidates.json`:
- `last_day1`: Day 1 computed in Step 2
- `person_count`: incremented by 1

Atomic write (read full file, modify in memory, write to `.tmp`, `os.replace`).

### Step 12, Append Excel Tab 1

`Claude-Brain/prospects-tracker-new.xlsx`, Tab 1.

Columns: Name | Title | Company | LinkedIn URL | OSI Angle | HubSpot Status | Action | Date Added | Notes

---

## FAILURE MODES, never silent

Every failure logs to `Claude-Brain/overnight-run-log.md` with timestamp + reason:

- Strategy note missing: log, mark `yes-with-email-strategy-missing`, do NOT write AI fields.
- Active sequence check: AI fields already populated and Andy did not confirm overwrite: log, stop.
- AI field write fails: retry once, then log + exit.
- LINKED_IN_CONNECT task fails: log `linkedin-task-sync-failed`, keep AI fields written.
- Excel append fails: log warning, do NOT block the field write. Excel is a tracker, not source of truth.
- Stagger metadata write fails: retry once. If still fails, log and continue with defaulted Day 1.
- Validator raises: log violation list, do NOT write any AI fields, flip to `pending-relookup`.

---

## RULES (index)

Quality gates in order: Step 0 (drafting-rules.md), Step 3 (duplicate check), Step 4 (email pattern), Step 6 (self-check), Step 7 (sanitize), Step 8 (validator). None skippable.

Hard constraints: one candidate per invocation, 6 emails only, single atomic AI field write (Step 9), LINKED_IN_CONNECT task always on Day 1 (Step 10).

Sign-off rule: "Best, Andy" on every single email. No exceptions. Including "Any thoughts?" Email 2.

Greeting rule: first name + comma only. No "Hi". No "Hello".
