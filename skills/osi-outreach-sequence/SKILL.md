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

## 🛑 HARDWIRED RULE, RUN INLINE, NO AGENT-TOOL DISPATCHES

This skill is invoked inline from the qualification skill's handoff. Read this SKILL.md into the same context, draft and queue the 6 emails there. The orchestrator must NOT dispatch an `Agent` subagent to run this skill on a scheduled fire, every dispatch spawns a fresh sandbox that re-prompts Andy for folder mount approval. See osi-overnight-runner SKILL.md for the longer explanation. **Why:** 2026-04-29 fire dispatched 8 subagents (qualification + outreach handoffs) and triggered mount prompts before Andy halted the run.

---

## 🛑 HARDWIRED RULE, NO APPROVAL PROMPTS DURING SCHEDULED FIRES

If any tool call triggers an approval prompt during a scheduled-task fire, abort the queue write. Do not proceed. Do not retry. Flip the candidate to `pending-relookup` in `state.candidates` so Andy can review interactively next session. Log to `Claude-Brain/overnight-run-log.md`. No partial queue write.

What this means for personalization and hook research during scheduled fires:
- Personalization hooks come from the strategy note (already written by qualification) plus ZoomInfo `enrich_scoops` / `enrich_news` / `account_research` (already-approved MCP). No `web_fetch` / `WebFetch` / `WebSearch` to arbitrary domains for fresher hooks.
- ZI scoops can be stale. Use what is in the strategy note. The alternative (a prompt overnight) is not acceptable.
- HubSpot reads/writes: allowed.
- Outlook compose / sharepoint reads: allowed only if pre-approved at kickoff.
- Anything that prompts: abort.

Interactive sessions (Andy at keyboard) keep the broader research surface for personalization. The rule fires only when the session is launched by a scheduled task.

**Why this rule exists:** 2026-04-29, Patti Paulo qualification subagent triggered an overnight permission prompt via web_fetch. Outreach-sequence has parallel surface (web research for fresh hooks) that could trigger the same. Inverted rule applied here too: any prompt = abort.

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
- Schedule scheduled tasks (Discovery Mega, Refill, etc.). That's `osi-overnight-runner`.
- Pick the next candidate to process. That's `osi-overnight-runner`.
- Run on multiple candidates at once. ONE per invocation.

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
- Candidate status in `state.candidates` updated to confirm sequence queued

---

## HANDOFF

NONE. After 6 emails are queued and the LI task is updated, this skill exits. The orchestrator (`osi-overnight-runner`) is responsible for moving to the next pending candidate (up to 3 sequences per Processing Recurring fire).

---

## RELATED SKILLS

- **`osi-overnight-runner`**, orchestrator. Invokes this skill via the qualification handoff in Processing fires.
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
- Interactive (Andy at keyboard), ask Andy "Override?".
- Recurring runner, skip silently, log, mark candidate `skipped-active-sequence`, continue. No emails queued for this candidate.

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

Pull the strategy note from HubSpot (associated to the contact). Read:
- THE PERSONAL HOOK
- Fresh hook (30-day news)
- THE PLAY

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

| Email | sendTime | Gap from prior actual send |
|---|---|---|
| 1 | `4pm` |, (Day 1) |
| 2 | `11am` | +2 business days |
| 3 | `12pm` | +4 business days |
| 4 | `1pm` | +6 business days |
| 5 | `2pm` | +5 business days |
| 6 | `3pm` | +6 business days |

Master `osi-email-sender` fires 11 AM-4 PM ET weekdays. Each window processes queue entries with matching `sendTime`.

**Self-healing:** when Email N fires (in the email-sender skill, not here), it recomputes Email N+1's `sendDate` as `N business days after today`. So if a sequence is paused/resumed, the cadence stays correct.

LinkedIn connection request task due Day 1 (skip weekends/holidays).

### Step 4, Write 6 Emails

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

### Step 5, Present for review (Interactive only)

If invoked interactively (Andy at keyboard, single profile pasted):
- Show all 6 + send schedule.
- End with: *"Look it over and say **ready** when you want to send."*
- Stop. Wait for `ready`.

### Step 6, Send + Schedule

**Interactive on `ready`:** open `https://outlook.office.com` in Chrome. New mail → To, subject, body. Do NOT click Send. Tell Andy: *"Email 1 ready in Outlook. Click Send when good, then say **sent**."* On `sent`: confirm Sent Items, queue Emails 2-6.

**Recurring runner:** append all 6 to `email-queue.json`. No Outlook step. The email-sender skill handles actual sending during 11am-4pm windows.

### Step 6.5, Email-pattern verification (MANDATORY before queue write)

Before any queue entries are appended, verify the prospect's `to:` address against the company's verified email pattern. Algorithm: `knowledge/email-pattern-resolver.md`.

The qualification skill should have populated an EMAIL RESOLUTION block in the contact's strategy note. Read that note. If it says:

- `hubspot-existing` or `verified-pattern` → proceed.
- `dominant-pattern` → proceed but include `"emailResolution": "dominant-pattern"` in each queue entry so the monitor's pre-flight section knows there's no engagement signal yet.
- `manual-required` → STOP. Do NOT append to queue. Return: `"Pattern signal too weak at <Company>. Andy must verify <email> before queueing."` Do not retry; do not auto-pick.

If the strategy note has NO EMAIL RESOLUTION block (legacy contact, or qualification skipped this step), run the resolver inline now:
1. Search HubSpot for all contacts at the same company.
2. Bucket emails by pattern, score per `email-pattern-resolver.md`.
3. If the prospect's `to:` matches the verified or dominant pattern, proceed.
4. If it doesn't, STOP-GATE. Append entry to a separate `pattern-mismatch-flagged.json` file with the prospect's name, the queued address, the verified pattern, and a recommendation. Surface in pre-flight.

Never queue an entry whose `to:` pattern is `manual-required` OR mismatches a verified company pattern.

### Step 6.6, 6-ITEM SELF-CHECK (MANDATORY before sanitize and validator)

For every drafted email body, write out answers to these six questions in working context BEFORE calling sanitize and validator. The validator catches strings; this self-check catches semantics the validator can't see.

1. **Does the first sentence reference the prospect, not OSI?** (Email 1 only. Pass = prospect name, role, post, project, company news. Fail = "I'm Andy", "I work with", "I help", any opener that puts OSI before the prospect.)
2. **Is the Personal Hook from the strategy note actually in this email?** (Email 1 only. The hook from THE PERSONAL HOOK section of the strategy note must appear in the body. If the note's hook is generic geography or thin, ABORT and flip candidate to `pending-needs-hook`.)
3. **Is there exactly ONE product line in this email?** (All emails. Surgical Isolation rule. The validator will catch keyword density violations but the drafter must intentionally pick ONE line per email.)
4. **Did I name SmartOptics?** (Cold sequences only. Must be no. The validator catches the string but the drafter should not be reaching for the name in the first place.)
5. **Did I claim OSI manufactures?** (All emails. Must be no.)
6. **Did I sign with "Andy" at the bottom?** (All emails. Must be no. Outlook signature handles it.)

If any answer is wrong, REWRITE before passing to sanitize. Do not paper over with sanitize.

If question 2 fails (no hook or thin hook), do NOT write Email 1. Flip the candidate to `pending-needs-hook` in `state.candidates` (atomic write per the rule above), log to `overnight-run-log.md`, and exit. Andy will pull a real hook manually next session. The skill does not write filler.

### Step 6.7, Sanitize bodies (MANDATORY before validator)

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

### Step 6.8, Validator (MANDATORY before queue append)

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
1. Atomic write candidate status to `pending-relookup` in `state.candidates`.
2. Log timestamp + violation list to `Claude-Brain/overnight-run-log.md`.
3. Do NOT write any partial queue entries. Do NOT proceed to Step 7.
4. Exit cleanly.

The validator is also called by `osi-email-sender` at send time as belt-and-suspenders. So even if a queue entry was hand-edited and bypassed the write-time validator, the sender refuses to send it.

### Step 7, email-queue.json entry format

Path: `C:\Claude-Brain\email-queue.json`

```json
{
  "id": "[firstname]-[lastname]-[company-slug]-[N]",
  "prospectName": "[First Last]",
  "company": "[Company]",
  "to": "[email]",
  "subject": "[subject, sanitized]",
  "body": "[sanitized body. Email 1: full new-pitch. Email 2 (RE: subject): just the new reply text, sender's Reply flow attaches prior thread natively. Emails 3/4/5/6: ONLY the new pitch, NEVER any quoted thread. ALL bodies are em-dash and en-dash free per sanitize_body in Step 6.7.]",
  "sendDate": "YYYY-MM-DD",
  "sendTime": "[4pm/11am/12pm/1pm/2pm/3pm]",
  "status": "pending",
  "addedDate": "YYYY-MM-DD",
  "emailResolution": "[hubspot-existing | verified-pattern | dominant-pattern]"
}
```

`emailResolution` is required on every new entry. The monitor's pre-flight uses it to know which queue entries had strong vs weak signal at queue time.

#### Atomic queue write

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

Do NOT use the MCP Write tool for the queue. The sanitize step in 6.7 must have run on every entry in `new_entries` before this code runs.

### Step 8, Re-spread (sync per-email scheduled tasks if any)

If there are per-email scheduled tasks for this prospect (older architecture used these, current architecture uses the email-sender skill to fire 11am-4pm windows directly), list them via `mcp__scheduled-tasks__list_scheduled_tasks` and update via `update_scheduled_task` to match new `sendDate + sendTime`. Re-list and diff at the end.

In the current architecture this is usually a no-op (the email-sender skill reads `email-queue.json` directly).

### Step 9, Update LINKED_IN_CONNECT due_date

Find the existing LINKED_IN_CONNECT task on the contact (qualification created it with provisional due_date). `manage_crm_objects` updateRequest, set `hs_timestamp` to Email 1 Day 1 (skip weekends/holidays).

This synchronizes: LinkedIn invite due Day 1 + Email 1 fires Day 1 4pm + first call attempt Day 1 + voicemail Day 1 if no answer. All Day 1.

### Step 10, Update stagger metadata + state

Update `state.stagger[company_name]`:
- `last_day1`: today's just-computed Day 1
- `person_count`: incremented by 1

Atomic write.

Update candidate status in `state.candidates` to confirm sequence queued. Optional flag like `outreach_queued_at: [timestamp]`.

### Step 11, Append Excel Tab 1

`Claude-Brain/prospects-tracker-new.xlsx`, Tab 1.

Columns: Name | Title | Company | LinkedIn URL | OSI Angle | HubSpot Status | Action | Date Added | Notes

Tab 2 is the wrap-up phase (handled by `osi-overnight-runner` at run end), not per-prospect.

---

## FAILURE MODES, never silent

Every failure logs to `Claude-Brain/overnight-run-log.md` with timestamp + reason:

- Strategy note missing → log alert, mark candidate `yes-with-email-strategy-missing`, do NOT queue.
- Active sequence check returns a hit → log "skipped-active-sequence", mark candidate, exit.
- email-queue.json write fails → retry once, then log + exit. Do NOT proceed on stale queue.
- LINKED_IN_CONNECT update fails → mark candidate `yes-with-email-linkedin-task-incomplete`. Still keep the 6 emails in the queue (queue is authoritative).
- Excel append fails → log warning, do NOT block the queue. Excel is a tracker, not the source of truth.
- Stagger metadata write fails → retry once. If still fails, log and continue with a defaulted Day 1 (next business day) but flag for manual review.

---

## RULES

- **Step 0 mandatory: read `C:\Claude-Brain\playbook\drafting-rules.md` in full before drafting anything.** Single source of truth for product lines, voice rules, branding rules, dead phrases, hook priority, and the Bad Example anti-template.
- **Step 6.6 mandatory: 6-item self-check** before sanitize and validator. Catches semantics the validator can't see (hook quality, lead-with-pain, one product line).
- **Step 6.8 mandatory: validator** (`C:\Claude-Brain\scripts\validate_email.py`) on every body and subject before queue append. ValueError on abort-level violation, no partial queue write.
- Only invoked after `osi-prospect-qualification` returns ✅ Yes-with-email + verified employer.
- One candidate per invocation. Never sweep.
- 6 emails per qualified candidate. Never more, never fewer.
- email-queue.json writes are always atomic (`.tmp` + `os.replace`).
- LINKED_IN_CONNECT task `hs_timestamp` always synced to Email 1 Day 1.
- Same-company stagger always read from `state.stagger`, never from email-queue scan.
- Skip weekends + holidays for all dates (sendDate, LINKED_IN_CONNECT due, etc.).
- No em-dashes, no en-dashes, no "Andy" sign-off, no banned vocab, no dead phrases, no SmartOptics in cold, no "we manufacture" claim, no credentials openers, one product line per email. Validator enforces. See drafting-rules.md.
- Approved Vendor mention: only if `approved-vendors.json` matches. Never invent. Verbatim phrasing in drafting-rules.md Section 9.
- Active Sequence Check is non-negotiable, always run first before drafting anything.
- If anything in the input handoff is missing, refuse cleanly. Don't proceed on partial data.
- If the Personal Hook is generic geography or thin, flip candidate to `pending-needs-hook` and exit. Never write filler.
