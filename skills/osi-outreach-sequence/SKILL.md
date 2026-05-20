---
name: osi-outreach-sequence
description: >
  Drafts and queues the 6-email outreach sequence for ONE qualified OSI Global prospect. Reads
  the strategy note + Personal Hook + Fresh Hook from HubSpot, picks sequence type, computes
  Day 1 from same-company stagger metadata, drafts all 6 emails, appends them atomically to
  email-queue.json with proper sendDate + sendTime, updates the LINKED_IN_CONNECT task due_date
  to match Email 1, appends Excel Tab 1. Triggers when invoked by osi-prospect-qualification's
  handoff on a Yes-with-email verdict.
---

> Source: `C:\Claude-Brain\skills\osi-outreach-sequence\` (Git, github.com/Drrewdy/Claude-Brain). Cowork `.claude/skills/` is a copy. Edit source, repackage, install.

# OSI Outreach Sequence

---

## 🚨 STOP -- DID YOU READ OSI-PROSPECT-QUALIFICATION THIS SESSION? (added 2026-05-08)

This skill handles sequencing only. It does not govern candidate discovery, LinkedIn browsing, or Company Mode search. All of that lives in `osi-prospect-qualification`.

If you are running Company Mode (finding prospects at a company) and you have NOT read `C:\Claude-Brain\skills\osi-prospect-qualification\SKILL.md` in this session: **STOP. Read it now. Then proceed.**

Do not assume you remember the qualification workflow from training or a prior session. The skill has been updated multiple times. The Round 0 browse-first rule, the profile-scrubbing firms alert, and the stagger ownership rules are all in that file. Reading the outreach skill without reading the qualification skill first produced the D.E. Shaw miss on 2026-05-08 -- three strong VP-level targets gone for months.

**Why this rule exists:** 2026-05-08, a Company Mode run on D.E. Shaw read the outreach skill but not the qualification skill. The Round 0 mandatory card browse (the only viable source for firms where employees scrub their LinkedIn profiles) was skipped in favor of keyword searches, which returned nothing because D.E. Shaw employees deliberately remove all profile content. Matt Kong (VP, Data Center Manager), Leonardo Palazzo (VP, Data Center Management), and Michael De Candia (SVP) were all missed as a result.

---

## 🛑 HARDWIRED RULE, NO EMPLOYER VERIFICATION, NO SEQUENCE

This skill never queues a 6-email sequence on faith of a stale HubSpot record. It only runs when invoked via handoff from `osi-prospect-qualification` after a ✅ Yes-with-email verdict that was backed by Path A (full LinkedIn read) or Path B (ZoomInfo + corporate-domain email + dated web-search confirmation, with explicit `EMPLOYER VERIFICATION:` line in the strategy note).

If the strategy note is missing, employer verification is missing, or the verdict was anything other than Yes-with-email: this skill does not run.

---

## 🛑 HARDWIRED RULES

**This skill DOES:**
- Read the strategy note from HubSpot (Personal Hook, Fresh Hook, sequence type recommendation)
- Active Sequence Check (skip if a live sequence already exists for this contact)
- Approved Vendor check (read `Claude-Brain/approved-vendors.json`)
- Compute Day 1 from same-company stagger metadata in state file
- Draft 6 emails per the cadence and templates below
- Append all 6 to `C:\Claude-Brain\email-queue.json` (atomic `.tmp` + `os.replace`)
- Update the LINKED_IN_CONNECT task's `hs_timestamp` to Email 1 Day 1
- Append a Tab 1 row to `Claude-Brain/prospects-tracker-new.xlsx`
- Update stagger metadata (`last_day1`, `person_count`)

**This skill DOES NOT:**
- Qualify. Verdict is `osi-prospect-qualification`'s job. This skill assumes qualification already produced ✅ Yes-with-email.
- Discover candidates. That's `osi-discovery-sweep`.
- Run on multiple candidates at once. ONE per invocation.
- Navigate to LinkedIn. All prospect context comes from the handoff payload and HubSpot strategy note.
- Ask Andy for approval mid-run. Queue writes and task updates are automatic. Andy approved the batch at session start. Do not ask "ready?" or "proceed?" or display email bodies for review. One confirmation line per queued candidate, nothing else.
- Ask "should I proceed to the next company?" or "ready for Company X?" in a pre-approved batch. The company list was approved at session kickoff. That approval covers ALL companies in the list. When one company is done, immediately start the next. Never pause between companies. **Why this rule exists:** 2026-05-15 — after completing IT-CNP (Company 3 of 10), Claude asked "Should I proceed to Company 4?" instead of starting immediately. The batch was pre-approved at session start. The pause wasted time and violated the no-approval-prompt rule. Fix: batch kickoff approval = blanket approval for all companies in the list, in sequence, without checkpoints.
- Stop for `manage_crm_objects` confirmation prompts. ALL `manage_crm_objects` calls in this skill use `confirmationStatus: "CONFIRMATION_WAIVED_FOR_SESSION"`. Never show a proposed-changes table. Never ask "Approve?". Andy's session kick-off is blanket approval for all HubSpot writes this skill produces. **Why this rule exists:** 2026-05-06, qualification of Andrew Banhidi at Instinet stopped mid-run to show a proposed-changes table for a contact update. Session kick-off ("go") is blanket approval. The tool's own confirmation step is bypassed via `CONFIRMATION_WAIVED_FOR_SESSION` on every call.

---

## 🛑 STEP -1: TOOL PREFETCH (MANDATORY if not already done this session)

If osi-prospect-qualification already ran its Step -1 prefetch earlier in this conversation, skip this step — schemas are already live.

If this skill is running standalone (not following a qualification session), fire these TWO ToolSearch calls in the same message before doing anything else:

```
ToolSearch({ query: "select:mcp__workspace__bash,mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__search_crm_objects,mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__manage_crm_objects,mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__get_crm_objects,mcp__4ba1185f-93a5-43f3-9910-49e11601259c__enrich_contacts,mcp__4ba1185f-93a5-43f3-9910-49e11601259c__enrich_news", max_results: 6 })
ToolSearch({ query: "select:mcp__Claude_in_Chrome__tabs_context_mcp,mcp__Claude_in_Chrome__navigate,mcp__Claude_in_Chrome__get_page_text,WebSearch,TaskCreate,TaskUpdate", max_results: 6 })
```

After both return, all schemas are live. Do not call ToolSearch again during the run.

---

## 🛑 STEP 0, MANDATORY READ OF DRAFTING RULES

Before drafting any email body, subject line, or LinkedIn invite, **Read `C:\Claude-Brain\playbook\drafting-rules.md` in full** and load it into the working context. This file is the single source of truth for:

- Absolute bans (em-dashes, en-dashes, SmartOptics in cold, "we manufacture" claims, credentials openers, banned vocab, dead phrases, hyphens, rule of three, sign-off rules)
- OSI Product Lines and the one-product-line-per-email rule (Surgical Isolation)
- Sequence type to target role mapping
- Key Sales Wedges
- Vertical Intel (telco, banks, consulting, manufacturing, healthcare, Quebec)
- Park Place / Service Express merger wedge
- Personal Hook priority and the "what is NOT a Personal Hook" gate
- Fresh Hook scoring
- Approved Vendor Rule (with verbatim phrasing)
- Email 1 templates (Sample-Offer Network, Sample-Offer Server, Pain-Led)
- Bad Example anti-template (the Christopher Lawrence email that broke 7 rules)
- 6-item self-check
- Brevity word limits per email index

This Step 0 read is non-negotiable. The skill assumes the rules are loaded into context for every email it drafts. Do NOT skip and rely on training data.

After reading drafting-rules.md, proceed to INPUT below.

---

## 🛑 HARDWIRED RULE, NO EM-DASHES OR EN-DASHES, EVER

Andy Rule #4 from `CLAUDE.md`. The Unicode characters at codepoint U+2014 (em-dash) and U+2013 (en-dash) are FORBIDDEN in every body, subject, note, voicemail, LinkedIn message, and task description that this skill produces. The validator at `C:\Claude-Brain\scripts\validate_email.py` rejects any string containing either character at write time. Any drafting session that produces an em-dash is a bug. Period. Use commas to add a clause. Use periods to split sentences. Use parentheses for asides. Never the dash characters. This skill file deliberately does not display the banned glyphs; the validator references them via `chr(0x2014)` and `chr(0x2013)`.

---

## INPUT

Output of `osi-prospect-qualification`'s handoff:
- `hubspotContactId`
- Verdict: must be `yes-with-email`
- Strategy note location (HubSpot note ID associated to the contact)
- Personal Hook (1-2 specific LinkedIn details)
- Fresh hook (30-day news summary + URL, if any)
- Recommended sequence type: one of `Sample-Offer Network`, `Sample-Offer Server`, `Pain-Led TPM`, `Pain-Led DWDM`, `Pain-Led Storage`, `Pain-Led Pre-Owned`
- Company name (for stagger lookup)
- Verified email (the ZoomInfo email that passed domain validation)

If any of these are missing, refuse and log. Don't proceed on partial data.

---

## OUTPUT

After this skill runs on one qualified candidate:
- 6 entries appended to `email-queue.json`, status `pending`, with proper `sendDate` + `sendTime` per cadence
- LINKED_IN_CONNECT task `hs_timestamp` updated to Email 1 Day 1 (skips weekends + holidays)
- Excel Tab 1 row appended (Name | Title | Company | LinkedIn URL | OSI Angle | HubSpot Status | Action | Date Added | Notes)
- `state.stagger[company_name].last_day1` updated to Email 1 Day 1
- `state.stagger[company_name].person_count` incremented

---

## HANDOFF

NONE. After 6 emails are queued and the LI task is updated, this skill exits. Control returns to the caller (typically `osi-prospect-qualification` inline flow).

---

## RELATED SKILLS

- **`osi-prospect-qualification`**, produces the strategy note + verdict that this skill consumes. Hands off here on ✅ Yes-with-email.
- **`osi-discovery-sweep`**, produces the candidates that qualification eventually qualifies for this skill. Two skills upstream.
- **`osi-email-sender`** (separate skill, not orchestrated by runner), fires every 11am-4pm ET weekdays, picks up `pending` entries from `email-queue.json` whose `sendDate <= today` and matching `sendTime`, sends via Outlook.

---

## ACTIVE SEQUENCE CHECK, runs first

Before drafting anything, open `C:\Claude-Brain\email-queue.json`. Match by `to` (email, case-insensitive) OR `prospectName + company`.

**Skip if any matched entry has:**
- `status: "pending"`, OR
- `status: "sent"` with `sendDate` in last 30 calendar days.

`paused-*`, `canceled-*`, `sent` >30 days do NOT block. Note in strategy note this is a re-engagement.

**Behavior:**
- Always skip silently regardless of mode. Log to `overnight-run-log.md` as "skipped-active-sequence". No emails queued for this candidate. Never ask "Override?" -- Andy will review the log and re-run manually if he wants to override.

---

## APPROVED VENDOR RULE

OSI is approved at companies in `Claude-Brain/approved-vendors.json`. Read at sequence-build time. Case-insensitive substring match.

**If matched:**
- Email 1: ONE soft acknowledgment. *"Side note, we're already on your approved vendor list, so no new vendor onboarding if anything ever needs to move fast."*
- One of Email 3 OR Email 4 (Claude picks): one-line reminder. *"Quick reminder we're already approved at [Company] if timing matters."*
- Other emails: silent.

**If not matched:** never mention. Don't invent. Never use "vetted" / "pre-approved" / mention "procurement" in Email 1.

---

## OUTREACH FLOW, per Yes-with-email prospect

Strategy note + LINKED_IN_CONNECT task already exist (qualification produced them). This skill builds the email sequence on top.

### Step 1, Read strategy note + sequence type

🚨 **DO NOT NAVIGATE TO LINKEDIN. EVER. This skill does not touch LinkedIn.** All prospect context (hook, title, company, fresh news) is in the handoff payload and the HubSpot strategy note. Re-reading LinkedIn from here is a token waste and is forbidden. If you find yourself about to open a LinkedIn URL for context, stop. Use what is in the handoff.

Use the handoff payload directly:
- Personal Hook: already in the handoff `Personal Hook:` field. Use as-is. Do not re-derive.
- Fresh hook: already in the handoff `Fresh hook:` field. Use as-is.
- Sequence type: already in the handoff `Recommended sequence:` field.

If the handoff payload is incomplete or missing one of these fields, THEN pull the strategy note from HubSpot (associated to the contact) and read THE PERSONAL HOOK, Fresh hook (30-day news), and THE PLAY sections. This HubSpot read is the fallback, not the default.

The recommended sequence type came in via the handoff. If unsure or unspecified, read `Claude-Brain/playbook/product-lines.md` for the title-to-sequence mapping. Read `Claude-Brain/playbook/vertical-intel.md` for what to lead with by industry.

### Step 2, Compute Day 1 (same-company stagger)

Read `state.stagger[company_name]` from `C:\Claude-Brain\overnight-candidates.json`:

| `person_count` | Day 1 |
|---|---|
| `0` | Next business day (skip weekends + holidays) |
| `1-4` | `last_day1` + 4 business days |
| `5` | `last_day1` + 10 business days (cooling gap) |
| `6+` | `last_day1` + 4 business days |

After scheduling Email 1, update `last_day1` and increment `person_count`. Atomic write to state file.

Why state metadata, not email-queue scan: queue has 500+ entries; state metadata is O(1) and tracks THIS run only.

**Skip weekends + holidays.** Holiday list: `Claude-Brain/holidays.json` (read at runtime). Fallback if missing: US federal holidays + Good Friday + Black Friday + Christmas Eve + New Year's Eve.

### Step 3, Cadence

🚨 **COMPUTE ALL 6 DATES FROM THE FINAL DAY 1 ONLY. Day 1 must be fully resolved from the stagger (Step 2) before any other date is computed. Never compute E2-E6 from an intermediate or pre-stagger Day 1. The most common source of the E1/E2 same-day bug is computing E2 before the stagger pushes E1 forward.**

| Email | sendTime | Offset from Day 1 |
|---|---|---|
| 1 | `4pm` | Day 1 |
| 2 | `11am` | Day 1 + 2 business days |
| 3 | `12pm` | Day 1 + 6 business days |
| 4 | `1pm` | Day 1 + 12 business days |
| 5 | `2pm` | Day 1 + 17 business days |
| 6 | `3pm` | Day 1 + 23 business days |

All offsets are from Day 1. Skip weekends and holidays for every date. Use `holidays.json` (fallback: US federal + Good Friday + Black Friday + Christmas Eve + New Year's Eve).

**Pre-write date order check (MANDATORY before Step 10):**

After computing all 6 dates, verify the following before writing anything to the queue:
1. E1 < E2 < E3 < E4 < E5 < E6 (strictly ascending dates, no ties)
2. No two entries share the same sendDate
3. E2 sendDate is at least 1 business day after E1 sendDate

If any check fails: log to `overnight-run-log.md` with all 6 computed dates, raise an error, and exit without writing to the queue. Do not write a partial or mis-ordered sequence. The monitor's ordering sweep (Step 5.1) is a safety net, not a substitute for correct initial scheduling.

Master `osi-email-sender` fires 11 AM-4 PM ET weekdays. Each window processes queue entries with matching `sendTime`.

🚨 **LinkedIn connection request task in HubSpot MUST match Day 1 exactly.** Set or update the "Sales Nav -- Send connection request" task due date to Day 1 when the sequence is first queued (Step 11). If Day 1 ever changes for any reason, the task date changes with it. These two values are never allowed to diverge.

### Step 4, Duplicate-contact check (MANDATORY before drafting)

Before drafting anything, confirm the `hubspotContactId` in the handoff payload actually exists in HubSpot and is the UNIQUE record for this person:

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

- If exactly one result and it matches the handoff `hubspotContactId`: proceed.
- If one result but the ID does NOT match the handoff: STOP-GATE. The qualification skill created a duplicate. Surface to Andy: `"Duplicate contact detected for <Name> at <Company>. HubSpot has contact <found ID> but handoff says <handoff ID>. Resolve before queuing."` Do not queue.
- If zero results: the handoff contact ID is stale or mis-typed. STOP-GATE. Do not queue.
- If multiple results: STOP-GATE. Surface all IDs to Andy for manual merge before queuing.

### Step 5, Email-pattern verification (MANDATORY before drafting)

Before drafting, verify the prospect's `to:` address against the company's verified email pattern. Algorithm: `knowledge/email-pattern-resolver.md`.

The qualification skill should have populated an EMAIL RESOLUTION block in the contact's strategy note. Read that note. If it says:

- `hubspot-existing` or `verified-pattern` → proceed.
- `dominant-pattern` → proceed but include `"emailResolution": "dominant-pattern"` in each queue entry so the monitor's pre-flight section knows there's no engagement signal yet.
- `manual-required` → STOP. Do NOT draft or queue. Return: `"Pattern signal too weak at <Company>. Andy must verify <email> before queueing."` Do not retry; do not auto-pick.

If the strategy note has NO EMAIL RESOLUTION block (legacy contact, or qualification skipped this step), run the resolver inline now:
1. Search HubSpot for all contacts at the same company.
2. Bucket emails by pattern, score per `email-pattern-resolver.md`.
3. If the prospect's `to:` matches the verified or dominant pattern, proceed.
4. If it doesn't, STOP-GATE. Append entry to a separate `pattern-mismatch-flagged.json` file with the prospect's name, the queued address, the verified pattern, and a recommendation. Surface in pre-flight.

Never draft or queue an entry whose `to:` pattern is `manual-required` OR mismatches a verified company pattern.

### Step 6, Write 6 Emails

**Source of truth for templates, rules, and bad examples:** `C:\Claude-Brain\playbook\drafting-rules.md` (already read in Step 0). The templates below are reference summaries. The full templates, the Bad Example anti-template (Christopher Lawrence breakdown), and the 6-item self-check live in that file.

Hard rules to remember while drafting (full list in drafting-rules.md Section 1):
- No em-dashes or en-dashes (Andy Rule #4 from CLAUDE.md, validator enforces)
- No "SmartOptics" by name in cold (refer to optics as "OSI transceivers")
- No "we manufacture" claim (OSI does NOT manufacture, SmartOptics does)
- No credentials-first openers ("I'm Andy", "I work with", "Hi I'm")
- No hyphens (except in product names like QSFP-DD)
- No "Andy" sign-off (Outlook signature handles it)
- One product line per email (Surgical Isolation)
- Lead with the prospect's pain or hook, not OSI

If the strategy note's Personal Hook is generic geography, thin tenure, or industry alone, ABORT Email 1 and flip the candidate to `pending-needs-hook`. Do not write filler.

#### Email 1 templates (by sequence type)

**Sample-Offer (Network):**
> Hi [First],
>
> I'm just prepping this package for you. I have a box of swag and a pair of sample SFPs to send from the team at OSI Global.
>
> Do you come into the office, or is there a better address to ship it to?

**Sample-Offer (Server):**
> Hi [First],
>
> I'd like to send you a sample DIMM from our current batch. Same spec as what you're running, manufacturer warranty, won't touch your OEM support contract.
>
> Do you come into the office, or is there a better address to ship it to?

**Pain-Led (TPM / DWDM / Storage / Pre-owned):**
3-4 sentences. Lead with their specific pain (role + company). Reference Personal Hook from strategy note. Reference Fresh Hook if it's a strong news signal. One clear ask. No name at bottom.

Subject: short, specific, not spam-flaggable. Examples: `quick question on [their stack]`, `[Company] backbone refresh`, `your [role] team`.

#### Email 2 (RE: same subject as Email 1)

Branches by Email 1 archetype:
- **Sample-offer Email 1:** Email 2 body literally `Any thoughts?`, nothing else.
- **Pain-led Email 1:** 2-3 sentences. Pick ONE move: new data point on same pain / adjacent product line / fresh company signal. End with ONE concrete ask.

The queue body is JUST the new reply text. The sender's Reply flow attaches the prior thread natively (grey divider + From/Sent/To/Subject header + original body). Do NOT include `On X wrote:` placeholders or `>` lines in the queue body. No greeting. No sign-off.

#### Email 3 (new subject, STANDALONE, NO QUOTED THREAD)

Different angle / product line not yet covered. 3-4 sentences. One ask.

🚫 **Body must contain ONLY the new pitch.** No `On <date>, Andy McLean wrote:` separator. No `>` quoted lines. No prior email content of any kind. Email 3 is a fresh-subject standalone touch, it goes through the sender's NEW MAIL flow, which types the queue body verbatim. Anything you put in the body lands in the prospect's inbox exactly as written. Including quoted prior thread is what produced the 2026-04-29 incident where 11 prospects received malformed Email 3s with hand-rolled `On <date>, Andy McLean wrote:` blocks. NEVER do this.

#### Email 4 (new subject, STANDALONE, NO QUOTED THREAD)

Another product line. 3-4 sentences. One ask.

🚫 **Body must contain ONLY the new pitch.** Same rule as Email 3: no quoted thread, no `On <date>, Andy McLean wrote:` separator, no `>` lines, no prior email content. Standalone fresh-subject touch.

#### Email 5 (new subject, STANDALONE, NO QUOTED THREAD)

Another product line. 3-4 sentences. One ask.

🚫 **Body must contain ONLY the new pitch.** Same rule as Email 3. Standalone fresh-subject touch.

#### Email 6, breakup (new subject, STANDALONE, NO QUOTED THREAD)

Clean close, no ask. One sentence. Examples: *"Should I close the file on this one, or is the timing just off?"* or *"No worries if now isn't the right time. Happy to circle back when things shift."*

🚫 **Body must contain ONLY the one breakup sentence.** Same rule as Email 3. Standalone fresh-subject touch. No quoted thread.

### Step 7, 6-ITEM SELF-CHECK (MANDATORY before sanitize and validator)

For every drafted email body, write out answers to these six questions in working context BEFORE calling sanitize and validator. The validator catches strings; this self-check catches semantics the validator can't see.

1. **Does the first sentence reference the prospect, not OSI?** (Email 1 only. Pass = prospect name, role, post, project, company news. Fail = "I'm Andy", "I work with", "I help", any opener that puts OSI before the prospect.)
2. **Is the Personal Hook from the strategy note actually in this email?** (Email 1 only. The hook from THE PERSONAL HOOK section of the strategy note must appear in the body. If the note's hook is generic geography or thin, ABORT and flip candidate to `pending-needs-hook`.)
3. **Is there exactly ONE product line in this email?** (All emails. Surgical Isolation rule. The validator will catch keyword density violations but the drafter must intentionally pick ONE line per email.)
4. **Did I name SmartOptics?** (Cold sequences only. Must be no. The validator catches the string but the drafter should not be reaching for the name in the first place.)
5. **Did I claim OSI manufactures?** (All emails. Must be no.)
6. **Did I sign with "Andy" at the bottom?** (All emails. Must be no. Outlook signature handles it.)

If any answer is wrong, REWRITE before passing to sanitize. Do not paper over with sanitize.

If question 2 fails (no hook or thin hook), do NOT write Email 1. Log to `overnight-run-log.md` and exit. Andy will pull a real hook manually next session. The skill does not write filler.

### Step 8, Sanitize bodies (MANDATORY before validator)

The queue is the source of truth for what gets sent. Every consumer (osi-email-sender, osi-monitor, future Andy edits) trusts the body field as-is. This step makes the body trustworthy. NEVER skip it.

The 2026-04-29 incident happened because sanitization was outsourced to the sender (em-dash strip + quote-strip + double-space-after-period). The chat-session runner skipped those steps and shipped malformed Email 3s. Doing the cleaning at WRITE time fixes that whole class of bug, the body that lands in the queue is the body that ships, no in-flight repair needed.

Run this on every body before it goes into the queue entry. Run it on subjects too.

```python
import re

def sanitize_body(text: str, email_index: int) -> str:
    """
    Sanitize an outreach body before queue write.

    Args:
      text: the raw body string written by the drafter.
      email_index: 1, 2, 3, 4, 5, or 6 (which email in the sequence).

    Returns:
      Cleaned body. Caller asserts the result is non-empty before queue append.
    """
    if text is None:
        return ""

    # 1. Em-dash (U+2014) and en-dash (U+2013): banned by Andy Rule #4.
    #    Replace with sentence breaks or hyphens depending on context.
    #    The banned characters are constructed via chr(codepoint) so this source
    #    file itself contains zero literal em-dashes or en-dashes per Andy Rule #4.
    EM = chr(0x2014)   # em-dash
    EN = chr(0x2013)   # en-dash
    text = (text
        .replace(" " + EM + " ", ". ")
        .replace(EM + " ", ". ")
        .replace(" " + EM, ".")
        .replace(EM, "-")
        .replace(" " + EN + " ", ". ")
        .replace(EN, "-"))

    # 2. Email 3/4/5/6 are STANDALONE fresh-subject touches. Strip any quote
    #    markers and everything after them. Defense-in-depth, the drafter
    #    should never put these in 3+ bodies but if it does, kill them here.
    if email_index >= 3:
        markers = [
            r"\n*\s*-{5,}\s*On .* wrote\s*-{5,}",       # ----- On X wrote -----
            r"\nOn .*,? .* (?:McLean )?(?:wrote|wrote:)",  # On Mon, Andy McLean wrote:
            r"\n>+ ",                                     # > quoted lines
            r"\nFrom: Andrew McLean",                     # Outlook header
        ]
        for m in markers:
            match = re.search(m, text)
            if match:
                text = text[:match.start()].rstrip()
                break

    # 3. Normalize multiple consecutive spaces (NOT newlines) inside lines.
    #    Two-spaces-after-sentence is handled at SEND time via non-breaking
    #    space, so we want exactly one space here.
    text = re.sub(r" {2,}", " ", text)

    # 4. Trim trailing whitespace per line.
    text = "\n".join(line.rstrip() for line in text.split("\n"))

    # 5. Collapse runs of 3+ blank lines down to a single blank line.
    text = re.sub(r"\n{3,}", "\n\n", text)

    # 6. Final assertion, body must be em-dash and en-dash free.
    if EM in text or EN in text:
        raise ValueError(f"sanitize_body left dashes in body. Bug. Text starts: {text[:80]!r}")

    return text.strip()


def sanitize_subject(subject: str) -> str:
    """Sanitize the subject line. Same dash rules. Subjects are never quoted."""
    if subject is None:
        return ""
    EM = chr(0x2014)
    EN = chr(0x2013)
    subject = (subject
        .replace(" " + EM + " ", ", ")
        .replace(EM, "-")
        .replace(" " + EN + " ", ", ")
        .replace(EN, "-"))
    subject = re.sub(r"\s+", " ", subject).strip()
    if EM in subject or EN in subject:
        raise ValueError(f"sanitize_subject left dashes. Bug. Subject: {subject!r}")
    return subject


# Apply to every email in the sequence before queue append.
for i, email in enumerate(emails, start=1):
    email["body"]    = sanitize_body(email["body"], i)
    email["subject"] = sanitize_subject(email["subject"])
    if not email["body"]:
        raise ValueError(f"Email {i} body is empty after sanitization. Stopping. ID will be {email.get('id')}.")
```

If `sanitize_body` raises (em-dash or en-dash leaked through, or a body went empty after stripping a quote marker), STOP the entire queue write. Do NOT append a partial sequence. Do NOT use the MCP Write tool for the queue. Surface the error to Andy with the offending email index and ID. Andy fixes the drafter and re-runs.

The sender's defense-in-depth (Step 3B.4 mandatory pre-insertion strip) stays in place but is now redundant for properly-written entries. Belt and suspenders.

### Step 9, Validator (MANDATORY before queue append)

After sanitize succeeds, run the hard-stop validator on every email in the sequence BEFORE any entry is written to the queue. Single import, one call per email.

```python
import sys
sys.path.insert(0, r'C:\Claude-Brain\scripts')
from validate_email import validate_or_raise

# Each email in the sequence is validated. is_cold=True for cold sequences.
# Re-engagement skills pass is_cold=False and allow_circle_back=True.
for i, email in enumerate(emails, start=1):
    validate_or_raise(
        body=email['body'],
        subject=email['subject'],
        email_index=i,
        is_cold=True,           # cold sequence; re-engagement skills override this
        allow_circle_back=False, # cold sequence; re-engagement skills override this
        company_name=company_name,
        sequence_type=sequence_type,
    )
```

`validate_or_raise` checks all 11 hard-stop rules from `playbook/drafting-rules.md` Section 1 plus the word-count limits from Section 14. If any abort-level violation hits, it raises `ValueError` with the full violation list. The skill MUST NOT catch this exception and continue. Let it propagate, log to `overnight-run-log.md`, and exit. The candidate flips to `pending-relookup` so Andy reviews next session.

Rules the validator enforces (codified mirror of drafting-rules.md):
- 1.1 No em-dashes or en-dashes anywhere
- 1.2 No "SmartOptics" by name in cold body or subject
- 1.3 No "we manufacture" / "manufactured by us" / "OSI manufactures" / "we make our own optics"
- 1.4 No credentials-first openers in Email 1 ("I'm Andy", "I work with", "I help", "Hi I'm", "I wanted to reach out", "I'm reaching out")
- 1.5 No banned vocab (crucial, pivotal, delve, showcase, leverage, foster, etc.)
- 1.6 No dead phrases ("worth a conversation", "worth 15 minutes", "quick overview", "circle back" in cold, "touch base", "pick your brain", "hop on a call")
- 1.7 No hyphens in bodies except inside the product-name allowlist (QSFP-DD, Wi-Fi, Tier-1, etc.)
- 1.10 No negative parallelisms ("It's not just X, it's Y")
- 1.11 No "Andy" sign-off
- 1.12 One product line per email (Surgical Isolation, keyword density check)
- 14 Word-count limit per email index

If the validator raises:
1. Log timestamp + violation list to `Claude-Brain/overnight-run-log.md`.
2. Do NOT write any partial queue entries. Do NOT proceed to Step 10.
3. Exit cleanly. Surface the violation to Andy if running interactively.

The validator is also called by `osi-email-sender` at send time as belt-and-suspenders. So even if a queue entry was hand-edited and bypassed the write-time validator, the sender refuses to send it.

### Step 10, Write to queue

Build 6 entries in memory, then append atomically. DO NOT display email bodies in chat. DO NOT ask Andy to say "ready." DO NOT open Outlook. The email-sender skill handles actual sending during 11am-4pm windows.

#### Entry format

Path: `C:\Claude-Brain\email-queue.json`

```json
{
  "id": "[firstname]-[lastname]-[company-slug]-[N]",
  "prospectName": "[First Last]",
  "company": "[Company]",
  "to": "[email]",
  "subject": "[subject, sanitized]",
  "body": "[sanitized body. Email 1: full new-pitch. Email 2 (RE: subject): just the new reply text, sender's Reply flow attaches prior thread natively. Emails 3/4/5/6: ONLY the new pitch, NEVER any quoted thread. ALL bodies are em-dash and en-dash free per sanitize_body in Step 8.]",
  "sendDate": "YYYY-MM-DD",
  "sendTime": "[4pm/11am/12pm/1pm/2pm/3pm]",
  "status": "pending",
  "addedDate": "YYYY-MM-DD",
  "emailResolution": "[hubspot-existing | verified-pattern | dominant-pattern]"
}
```

`emailResolution` is required on every entry. The monitor's pre-flight uses it to distinguish strong vs weak signal at queue time.

#### Atomic write

```python
import json, os
QUEUE = r'C:\Claude-Brain\email-queue.json'
with open(QUEUE, 'r') as f: queue = json.load(f)
existing_ids = {e.get("id") for e in queue}
queue.extend([e for e in new_entries if e["id"] not in existing_ids])
tmp = QUEUE + '.tmp'
with open(tmp, 'w') as f: json.dump(queue, f, indent=2)
os.replace(tmp, QUEUE)
```

Do NOT use the MCP Write tool for the queue. Step 8 sanitize must have run on every entry in `new_entries` before this code runs. If the write fails, retry once, then log and exit. Do NOT proceed on a stale queue.

After the write succeeds, output exactly one confirmation line and nothing else:

`Queued: [First Last] | [Sequence type] | Day 1 [YYYY-MM-DD]`

Move immediately to the next candidate or exit. Displaying email bodies in chat burns tokens, causes context overflow on multi-candidate sweeps, and adds no value.

### Step 11, Sync Sales Nav Connection Request Task in HubSpot

🚨 **HARDWIRED RULE: The "Sales Nav -- Send connection request" task due date MUST equal Email 1 sendDate. Always. No exceptions. If no such task exists, CREATE IT.**

Search HubSpot for a task on this contact where `hs_task_subject` contains "Sales Nav -- Send connection request":

**Task found, NOT_STARTED:** update `hs_timestamp` to Email 1 Day 1 at 20:00 UTC (4pm ET).

**Task found, COMPLETED:** leave it. Log: "Sales Nav connect already completed — LinkedIn arm may have fired ahead of schedule."

**No task found:** CREATE the task now. Fields:
- Subject: `Sales Nav -- Send connection request to [First Name] [Last Name]`
- Due date: Email 1 Day 1 at 20:00 UTC (4pm ET)
- Type: `TODO`
- Owner: Andy (HubSpot owner ID 196669355)
- Body: `Day 1 LinkedIn connection request. Email 1 goes out at 4pm same day.`

Never leave this step incomplete. A queued sequence with no Sales Nav task means the LinkedIn arm of the cadence is silently broken. If the HubSpot write fails, log to `overnight-run-log.md` as `linkedin-task-sync-failed` but still keep the 6 emails in the queue.

**This step also applies to any reschedule.** Any time Email 1's sendDate changes, come back here and re-run this step. The task date always mirrors Email 1.

### Step 12, Update stagger metadata + state

Update `state.stagger[company_name]`:
- `last_day1`: today's just-computed Day 1
- `person_count`: incremented by 1

Atomic write.

Update stagger metadata confirms the sequence is queued for this candidate. Log completion to `overnight-run-log.md`.

### Step 13, Append Excel Tab 1

`Claude-Brain/prospect