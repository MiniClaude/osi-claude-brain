---
name: osi-email-sender
description: Send all due emails from C:\Claude-Brain\email-queue.json via Outlook. Runs 11am, 12pm, 1pm, 2pm, 3pm, 4pm ET weekdays.
---

# 🛑 ABSOLUTE FIRST ACTION: VERIFY YOU ARE READING THE LIVE SKILL 🛑

**Before doing anything else, run this check:**

1. Use the Read tool on `C:\Claude-Brain\skills\osi-email-sender\SKILL.md`. That file is the ONLY authoritative version.
2. If you are currently reading any other copy (e.g., a `SKILL.md` in `/mnt/uploads/`, an inlined copy pasted into a scheduled task prompt, a `.claude/skills/` runtime snapshot, or anything attached to this session that was written before today), STOP and reload from `C:\Claude-Brain\skills\osi-email-sender\SKILL.md`. Stale copies have caused real prospects to receive malformed emails. 2026-04-23: Joe Zarcone / Rackspace went out with a hand-rolled quote header and no grey divider because the runner was following a stale upload that did not contain Step 3A REPLY flow logic. This must not happen again.
3. The live file on disk is authoritative. Any version that disagrees with the live file is wrong. If you see two copies and they differ, follow the live file and surface the drift to Andy at the end of the run.

If the live file is unreachable for any reason, ABORT the run. Do not fall back to an older copy. Report the failure and let Andy decide.

---

# 🚨 READ THIS ENTIRE FILE BEFORE SENDING ANY EMAIL 🚨

This skill sends cold outreach to real, paying-potential customers. One bad format, one missed blank line, one fake quote header, one send to a cancelled contact, and the user looks like a spammer to a prospect they may be chasing for months. There is no "close enough." Follow every rule exactly. If anything is ambiguous, STOP and ask the user. Do not guess.

---

# 🛑 MANDATORY PRE-SEND GATE 🛑

**Before composing ANY email, every single one, no exceptions, you MUST run this check. If you skip it, you WILL send to a cancelled or blocked prospect and burn a real relationship. This has happened. It must not happen again.**

```python
import json
QUEUE_PATH = 'C:/Claude-Brain/email-queue.json'  # Live queue, Git-versioned. Andy syncs between laptops manually via git push/pull.
HARD_BLOCK_PATH = 'C:/Claude-Brain/hard-block.json'  # Hard-block list stays in Git (manually maintained, low churn)

with open(QUEUE_PATH) as f:
    queue = json.load(f)
with open(HARD_BLOCK_PATH) as f:
    hb = json.load(f)

entry = next((e for e in queue if e.get('id') == ENTRY_ID), None)
assert entry is not None, f"Entry {ENTRY_ID} not in queue"
assert entry['status'] == 'pending', f"SKIP: {ENTRY_ID} status is {entry['status']}, not pending"

# Hard-block enforcement. Single source of truth is C:/Claude-Brain/hard-block.json.
# Never hardcode addresses or domains anywhere else. To block a new address/domain,
# edit hard-block.json. Do not touch this gate code.
blocked_addrs = {a['email'].lower() for a in hb.get('addresses', [])}
blocked_domains = {d['domain'].lower() for d in hb.get('domains', [])}
addr = entry['to'].lower().strip()
domain = addr.split('@')[-1] if '@' in addr else ''

if addr in blocked_addrs or domain in blocked_domains:
    # Hard-block hit. This is NOTIFICATION-WORTHY: some upstream sequence enrolled a prospect
    # against a blocked address/domain. Andy wants to know, NOT silent skipping.
    # Raise a distinctive AssertionError so the runner logs it loudly in Step 7.
    reason = f"hard-blocked address {addr}" if addr in blocked_addrs else f"hard-blocked domain {domain}"
    raise AssertionError(f"HARD_BLOCK_HIT | id={ENTRY_ID} | to={addr} | {reason} | FLAG TO ANDY IN REPORT")
```

Run this check immediately before composing each email. Not once per run. Not once per window. Once per email. The queue file's modification time can change mid-run because osi-monitor writes cancellations and pauses to it in real time. The list you pulled at the start of the window is a candidate list only. The authoritative status is whatever is on disk RIGHT NOW.

If either assert fails, SKIP this entry: do not open a compose, do not draft, do not click Reply, do not click New mail. Log the skip (ID and reason) and move on to the next entry.

**Every compose step in this file (Step 3A and Step 3B) begins by running this gate. If you forget, you have failed the skill.**

---

## TL;DR: the five rules that matter

1. **Re-read the queue entry from disk right before composing each email.** Run the Pre-Send Gate above. If `status != "pending"` or `to` is hard-blocked, SKIP. No exceptions, ever.
2. **Subject starts with `RE: ` → use Outlook's Reply button on the original sent email in Sent Items. NEVER start a New mail for a follow-up.** The queue body's fake `---------- On April 16, Andy McLean wrote ----------` separator is NOT the quote format. Outlook's native Reply gives the real grey divider and From/Sent/To/Subject header.
3. **Subject does NOT start with `RE: ` → New mail flow.** Type the full body from the queue.
4. **Exactly ONE blank line between the last line you typed and `Best,`.** Not zero. Not two. One. Run the bi-directional trim in Step 4 on every email, then verify visually before Send. The trim pads up if there are too few newlines and Backspaces down if there are too many. Target is always one visible blank line.
5. **Preview before Send on every email.** Count the blank lines. Confirm the grey divider and header are present (Reply flow). Confirm no hand-rolled quote header is in the body.
6. **Always cross-check the Reply To: tag against the queue `to`.** Outlook auto-resolves To: from the original From: line, which is wrong when Email 1 went out from a non-canonical Andy alias (`andy@osihardware.onmicrosoft.com`). **Every Desjardins prospect (any `@desjardins.com`) hits this, assume it on Desjardins always.** If the To: tag is "Andrew McLean" or any self-reference, remove it and type the queue `to` address. Self-heal, do not stop. Detail in Step 3A.6 and Failure Modes.

If any rule feels unclear, re-read the full file. Skipping these rules is how prospects get burned.

---

# 🚫 ABSOLUTE RULE: NO EM-DASHES IN ANY EMAIL. EVER. 🚫

**An em-dash (Unicode code point U+2014) in an outbound email is an instant tell that AI wrote it.** Real prospects pattern-match on that character and write the sender off as spam or AI slop. This is non-negotiable.

This rule applies to:
- Every email body you type
- Every follow-up reply
- Every subject line
- Every character that leaves this process and lands in a prospect's inbox

It also applies to en-dashes (Unicode code point U+2013) for the same reason.

**Before typing ANY body text, run this sanitizer:**

```js
function stripDashes(text) {
  // Em-dash (U+2014) and en-dash (U+2013) → plain hyphen or period.
  // Replace " U+2014 " surrounded by spaces with ". " (sentence break). Replace any bare em-dash with "-".
  return text
    .replace(/ \u2014 /g, '. ')
    .replace(/\u2014 /g, '. ')
    .replace(/ \u2014/g, '.')
    .replace(/\u2014/g, '-')
    .replace(/ \u2013 /g, '. ')
    .replace(/\u2013/g, '-');
}

// Apply to every body/reply/subject string pulled from the queue before it hits Outlook.
```

**After inserting the body, run this final check:**

```js
const body = document.querySelector('[aria-label*="Message body"][contenteditable="true"]');
const txt = body.innerText;
if (txt.includes('\u2014') || txt.includes('\u2013')) {
  throw new Error('EM-DASH OR EN-DASH FOUND IN BODY. ABORT. Fix the queue entry and re-run.');
}
```

If the queue body contains an em-dash, it is a bug in whichever skill wrote the queue entry (osi-outreach-sequence, osi-3email-new, etc.). Surface it to Andy so he can fix the upstream skill. Never send an email that has an em-dash in it, even if you have to skip the entry.

---

## Step 0: Pre-flight concurrency lock (MANDATORY, runs before every fire)

The 2026-04-29 incident had two runners writing to `email-queue.json` simultaneously: a scheduled fire and a manual chat session Andy started. They didn't corrupt each other by luck. A simple lock file prevents the race.

```python
import os, json, time, uuid

LOCK_PATH = 'C:/Claude-Brain/email-sender.lock'
SESSION_ID = os.environ.get('CLAUDE_SESSION_ID') or str(uuid.uuid4())
LOCK_TTL_SEC = 900  # 15 minutes, longer than any plausible single-window run, short enough to clear stale locks fast

if os.path.exists(LOCK_PATH):
    try:
        with open(LOCK_PATH) as f: lock = json.load(f)
        age = time.time() - lock.get('acquiredAt', 0)
        if age < LOCK_TTL_SEC:
            raise SystemExit(
                f"LOCK HELD by another runner (sessionId={lock.get('sessionId')}, "
                f"acquiredAt={lock.get('acquiredAt')}, age={age:.0f}s). "
                f"Refusing to start to prevent the 2026-04-29 two-runner race. "
                f"If you believe this is stale, delete {LOCK_PATH} manually."
            )
        # Stale lock, adopt it
        print(f"WARN: stale lock from session={lock.get('sessionId')} (age={age:.0f}s). Taking over.")
    except (json.JSONDecodeError, KeyError):
        # Corrupt lock, overwrite
        print(f"WARN: corrupt lock at {LOCK_PATH}. Overwriting.")

with open(LOCK_PATH, 'w') as f:
    json.dump({'sessionId': SESSION_ID, 'acquiredAt': time.time(), 'pid': os.getpid()}, f)
```

The lock is released in **Step 8: Cleanup** at the end of the run. If the run crashes between acquire and release, the lock will time out after 15 minutes and the next runner can adopt it.

NOTE: A previous version of this Step 0 also included a "self-integrity check" that scanned the skill source for 5 regex patterns and aborted the entire fire if any were missing. Three of those patterns matched documentation prose, not code, so any cosmetic rephrase would false-positive and skip the whole send window. Removed 2026-04-30. The TARGET=2 invariant is now documented loudly in 4 places in this file (Step 4 code, Step 4 explanation, the visual GOOD-vs-BAD reference, and the Failure Modes section). Andy reviews changes via git history. That's the safety net; a brittle self-scan was net-negative.

---

## Step 1: Load the queue AND scan for hard-block enrollments

### 1A. Select candidate entries

Queue file: `C:\Claude-Brain\email-queue.json`

The queue is Git-versioned along with the rest of Claude-Brain. Andy syncs between his two laptops manually via `git pull` / `git push`. Do NOT auto-`git pull` or `git push` from this skill (the lock file gets stuck and pollutes logs). If the queue file is unreachable for any reason, ABORT and report. Do not fall back to a stale copy. (Historical note: a one-day OneDrive sync experiment ran 2026-04-24 and was rolled back same evening; the OneDrive Claude-Brain folder was permanently deleted 2026-04-30. C:\Claude-Brain is the only valid location.)

### ⚠️ MANDATORY DATE VALIDATION: CROSS-CHECK BASH TIME AGAINST ENV DATE

Before computing `today` or selecting any candidates, resolve the authoritative date:

```python
import subprocess
from datetime import datetime

# Get bash system date
bash_result = subprocess.run(['date', '+%Y-%m-%d %H:%M:%S %Z'], capture_output=True, text=True)
bash_date = bash_result.stdout.strip().split()[0]  # e.g. "2026-05-26"

# ENV_DATE must be read from the system prompt's "Today's date:" field before this skill fires.
# It is the authoritative date. Bash clock has been observed returning yesterday's date.
# 2026-05-27 incident: bash returned 2026-05-26 16:04:53 EDT at 9:29 AM real time on May 27.
# Result: 5 Email 1s sent at 9:29 AM because the runner saw them as overdue 4pm entries.
# This must never happen again. ENV_DATE wins, always.

if bash_date != ENV_DATE:
    print(f"WARN: Bash date ({bash_date}) disagrees with env date ({ENV_DATE}). Using env date.")

today = ENV_DATE  # Always use the env date. Never trust bash date alone.
```

`ENV_DATE` is the `YYYY-MM-DD` string parsed from the system prompt's "Today's date:" line. If it is unavailable for any reason, ABORT the run and report. Do not fall back to bash date.

Select entries where:
- `sendDate` equals `today` (from ENV_DATE above)
- `sendTime` matches the current hour window: one of `11am`, `12pm`, `1pm`, `2pm`, `3pm`, `4pm`
- `status` equals `pending`

Skip `cancelled` and `sent` entries.

If current hour is outside the six windows, do nothing and log the no-op. Do not dispatch.

### 1B. Pre-flight hard-block scan (MANDATORY, Andy must always know)

Before composing ANY email this window, scan the pending candidate set against `C:\Claude-Brain\hard-block.json`. For every pending entry whose `to` matches a blocked address or whose domain matches a blocked domain, collect it into a `hard_block_hits` list.

Andy wants to be NOTIFIED any time an upstream sequence enrolled a prospect against a blocked address or domain. Silent skipping is not acceptable, a new sequence quietly failing to send is worse than visible failure, because Andy thinks outreach is going out when it isn't.

For each `hard_block_hits` entry, you MUST:
1. Do NOT compose or send that email.
2. Mark the queue entry `status = "cancelled"` with `cancelReason = "hard-blocked by <address|domain>. Was enrolled by <upstream sequence>. Flagged at <time>."` so it doesn't show up on future runs.
3. Surface the hit loudly in the Step 7 run report under a dedicated "🚨 HARD-BLOCK HITS, NEW ENROLLMENTS AGAINST BLOCKED CONTACTS" section. Include: prospect name (derive from `id`), email, which rule fired (exact address vs domain), which sequence enrolled them (infer from queue history, the first entry in the sequence will have been created by one of the outreach skills), and recommended action.

If there are zero hits, say so explicitly in the report ("Hard-block scan: clean, 0 hits") so Andy has positive confirmation the scan ran.

```python
import json
from datetime import datetime
with open('C:/Claude-Brain/email-queue.json') as f: queue = json.load(f)
with open('C:/Claude-Brain/hard-block.json') as f: hb = json.load(f)
blocked_addrs = {a['email'].lower() for a in hb.get('addresses', [])}
blocked_domains = {d['domain'].lower() for d in hb.get('domains', [])}

today = datetime.now().strftime('%Y-%m-%d')
candidates = [e for e in queue if e.get('sendDate') == today and e.get('sendTime') == CURRENT_WINDOW and e.get('status') == 'pending']

hard_block_hits = []
for e in candidates:
    addr = (e.get('to') or '').lower().strip()
    domain = addr.split('@')[-1] if '@' in addr else ''
    if addr in blocked_addrs:
        hard_block_hits.append({'entry': e, 'rule': f'address {addr}'})
    elif domain in blocked_domains:
        hard_block_hits.append({'entry': e, 'rule': f'domain {domain}'})

# Cancel each hit in the queue so it doesn't keep firing on future runs
# (atomic write per the Step 6 pattern)
```

---

## Step 2: Re-read the entry status, then decide the flow

### 2A. Re-read the entry from disk immediately before composing

Do not trust the in-memory list of pending entries you built in Step 1. The queue can be updated mid-run by osi-monitor (bounces, replies) or by Andy editing it directly. Before composing each email, re-read the queue file from disk and look up this specific entry by `id`. Confirm `status == "pending"`. If it is anything else (`cancelled`, `sent`, `paused`), SKIP this entry entirely. Do not compose, do not draft, do not send. Log the skip and move on.

Additionally, cross-check the recipient against the hard-block list in the user's auto-memory (`feedback_bad_emails.md`). If the `to` field matches any blocked address, SKIP and log. Do not send under any circumstance.

This re-check is mandatory per-entry, even inside a single run window. On 2026-04-22 Brett Baker / Lippert had Email 2 nearly go out because the run pulled `pending` at 11:06 AM and the queue was updated to `cancelled` by osi-monitor at 11:12 AM, by which time the sender was already composing. Always re-check.

### 2A.5 Validator pre-send check (BELT AND SUSPENDERS)

After confirming the entry is `pending` and not hard-blocked, run the queue entry's body and subject through the validator. This is defense-in-depth: the drafting skills already validate at write time, but a hand-edited queue entry or a legacy entry from before the validator was added can still slip through.

```python
import sys
sys.path.insert(0, r'C:\Claude-Brain\scripts')
from validate_email import validate_email

# Infer email_index from the entry id pattern (name-company-N).
import re
m = re.search(r'-(\d)$', entry.get('id', ''))
email_index = int(m.group(1)) if m else 1

violations = validate_email(
    body=entry.get('body', ''),
    subject=entry.get('subject', ''),
    email_index=email_index,
    is_cold=True,  # Sender treats all entries as cold by default; re-engagement skills set is_cold=False at queue write.
)
aborts = [v for v in violations if v['severity'] == 'abort']
```

If any abort-level violation hits:
1. SKIP this entry. Do NOT compose. Do NOT send.
2. Flip the entry status from `pending` to `paused-validator` via the atomic queue write pattern in Step 6.
3. Log the entry id + violation list to the run report under a "Validator skips" line.
4. Continue to the next pending entry.

The skip is permanent until Andy fixes the entry. The next runner fire will see `paused-validator` and ignore it. This prevents a bad entry from firing every hour until someone notices.

Why this matters: on 2026-04-30 the Christopher Lawrence Email 1 shipped because it was queued before the validator existed. A bad queue entry from a stale skill version, a manual edit gone wrong, or any other path-to-bad-body must be caught at the last gate before it leaves the building.

### 2B. Decide the flow: Reply or New mail

Look at the queue entry's `subject`. Strip any surrounding whitespace.

- If it starts with `RE: ` (case-insensitive, with the space after the colon), it is a follow-up. Go to **Step 3A: REPLY flow**.
- Otherwise it is a fresh outreach. Run **Step 2C** first, then go to **Step 3B: NEW MAIL flow**.

This decision is not a judgment call. It's a string prefix check. `RE: ` → Reply. Anything else → New mail (after Step 2C gate).

---

## Step 2C: Connection Request Gate (Email 1 / fresh-subject only)

**This gate applies ONLY to Email 1 entries.** RE: follow-ups skip it entirely and go straight to Step 3A.

An Email 1 is a queue entry that has a fresh subject (no `RE:` prefix) AND whose `id` ends with `-1` (e.g. `david-thomas-sifi-1`). OR, equivalently, the `sendTime` is `4pm` and the subject has no `RE:` prefix, since Email 1 is the only entry that goes out at 4pm. Use either signal to confirm.

**Why this gate exists:** The qualification skill creates a HubSpot `LINKED_IN_CONNECT` task for every new prospect at enrollment. That task tracks whether Andy has sent the Sales Navigator connection request. Email 1 must NOT go out until Andy has sent the connection request. If the LI task is still `NOT_STARTED`, the prospect has not been warmed up on LinkedIn and the email sequence must wait. This was not enforced before 2026-05-27. Five Email 1s went out to prospects whose connection requests had not yet been sent.

### Gate logic

```python
import json, os, datetime, tempfile
from pathlib import Path

QUEUE_PATH = 'C:/Claude-Brain/email-queue.json'
HOLIDAYS_PATH = 'C:/Claude-Brain/holidays.json'

# Load holidays as a set of YYYY-MM-DD strings
with open(HOLIDAYS_PATH) as f:
    holidays_raw = json.load(f)
holidays = set(holidays_raw) if isinstance(holidays_raw, list) else set(holidays_raw.get('holidays', []))

def is_business_day(d):
    # d is a datetime.date object
    return d.weekday() < 5 and d.strftime('%Y-%m-%d') not in holidays

def next_business_day(d):
    # Returns the next business day after d (never same day)
    nxt = d + datetime.timedelta(days=1)
    while not is_business_day(nxt):
        nxt += datetime.timedelta(days=1)
    return nxt

def add_business_days(d, n):
    # Adds n business days to date d
    cur = d
    added = 0
    while added < n:
        cur += datetime.timedelta(days=1)
        if is_business_day(cur):
            added += 1
    return cur

def business_days_between(d_start, d_end):
    # Counts business days from d_start to d_end (exclusive of start, inclusive of end).
    # Returns a positive integer if d_end > d_start.
    count = 0
    cur = d_start
    while cur < d_end:
        cur += datetime.timedelta(days=1)
        if is_business_day(cur):
            count += 1
    return count
```

For each Email 1 candidate (before composing):

```python
# 1. Confirm this is an Email 1
entry_id = entry['id']
is_email_1 = entry_id.endswith('-1') or (entry.get('sendTime') == '4pm' and not entry['subject'].upper().startswith('RE:'))
if not is_email_1:
    # Not Email 1. Skip this gate.
    pass  # proceed to Step 3B normally
else:
    prospect_email = entry['to'].lower().strip()

    # 2. Look up the HubSpot contact by email address
    # Use search_crm_objects: objectType=contacts, filterGroups on email = prospect_email
    # (call mcp tool: mcp__df6165ad-588c-41c3-b9f1-2113e2a3b91a__search_crm_objects)
    # contact_id = result.results[0].id if results else None
    # If no contact found, proceed with send (gate cannot fire without a contact record)

    # 3. Search for a NOT_STARTED LINKED_IN_CONNECT task on that contact
    # Use search_crm_objects: objectType=tasks,
    #   filter: associations.contact = contact_id AND hs_task_type = LINKED_IN_CONNECT
    #           AND hs_task_status = NOT_STARTED
    #   subject CONTAINS "Sales Nav -- Send connection request"
    # li_task = first matching result, or None

    if li_task is not None:
        # CONNECTION REQUEST NOT YET SENT. Gate fires.

        # 4. Compute new E1 date = next business day after today
        today_date = datetime.date.fromisoformat(today)  # today = ENV_DATE from Step 1A
        new_e1_date = next_business_day(today_date)

        # 5. Compute the business-day offset between old sendDate and new E1 date
        old_e1_date = datetime.date.fromisoformat(entry['sendDate'])
        # The offset is how many business days we are pushing forward.
        # new_e1_date is always >= today > old_e1_date in the overdue case.
        # Use: offset = business_days_between(old_e1_date, new_e1_date)
        offset_bdays = business_days_between(old_e1_date, new_e1_date)

        # 6. Load full queue and update all pending entries for this prospect
        with open(QUEUE_PATH) as f:
            queue = json.load(f)

        for e in queue:
            if e.get('to', '').lower().strip() != prospect_email:
                continue
            if e.get('status') != 'pending':
                continue
            old_date = datetime.date.fromisoformat(e['sendDate'])
            new_date = add_business_days(old_date, offset_bdays)
            e['sendDate'] = new_date.strftime('%Y-%m-%d')

        # 7. Atomic write
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(QUEUE_PATH), prefix='email-queue.', suffix='.tmp')
        with os.fdopen(fd, 'w') as f:
            json.dump(queue, f, indent=2)
        os.replace(tmp, QUEUE_PATH)

        # 8. Update the HubSpot LINKED_IN_CONNECT task hs_timestamp to new E1 at 20:00 UTC (4pm ET)
        import datetime as dt
        new_e1_ts_utc = dt.datetime.combine(new_e1_date, dt.time(20, 0, 0), tzinfo=dt.timezone.utc)
        new_e1_ts_ms = int(new_e1_ts_utc.timestamp() * 1000)
        # Call manage_crm_objects: objectType=tasks, objectId=li_task.id, action=update
        # properties: { hs_timestamp: str(new_e1_ts_ms) }

        # 9. Log the skip
        print(
            f"CONN-REQUEST-GATE: {entry_id} skipped. LI task NOT_STARTED ({li_task.id}). "
            f"E1 rescheduled from {old_e1_date} to {new_e1_date}. "
            f"All pending entries for {prospect_email} pushed forward {offset_bdays} business days. "
            f"HubSpot LI task updated to {new_e1_date} 20:00 UTC."
        )

        # SKIP to next entry. Do NOT proceed to Step 3B.
        continue

    # If li_task is None (no NOT_STARTED task found, task already completed or never existed):
    # proceed normally to Step 3B.
```

**Cadence preservation rule:** When the gate fires, EVERY pending entry for that prospect (identified by `to` address) must be pushed forward by the exact same business-day offset. This keeps the E1-E2-E3-E4-E5-E6 gaps intact. Do not slide E1 alone while leaving E2-E6 behind.

**Log the gate skip in the Step 7 run report** under a dedicated section: "🔗 CONNECTION REQUEST GATES FIRED". Include: entry ID, old date, new date, offset, HubSpot task ID updated. If no gates fired, write "Connection request gate: clean, 0 fires" so Andy has positive confirmation the check ran.

---

## Step 3A: REPLY flow (subject starts with `RE: `)

### What the final email MUST look like

```
Any thoughts?                        ← the new reply text you typed

                                     ← exactly ONE blank line
Best,
<<YOUR_NAME>>
                                     ← signature block (auto-inserted)
Andy McLean
Solutions Executive
Book a Meeting with Me
...
_________________________________    ← solid light grey horizontal divider
From: Andrew McLean <<<YOUR_EMAIL>>>
Sent: Monday, April 20, 2026 4:35 PM
To: 'Prospect Name' <prospect@example.com>
Subject: Original subject without RE:

[original email 1 body, exactly as sent, with its own signature]
```

The grey divider + From/Sent/To/Subject header block + original body are all produced automatically by Outlook when you click Reply on the original sent email. You do NOT type any of that. You only type the short new reply text at the very top.

### Procedure

0. **RUN THE PRE-SEND GATE FIRST.** See the 🛑 MANDATORY PRE-SEND GATE 🛑 section at the top of this file. Re-read the queue entry from disk by `id`. Confirm `status == "pending"` and `to` is not in the hard-block list. If either fails, SKIP this entry and do not proceed to step 1. This is not optional. Brett Baker / Lippert 2026-04-22 is why.
1. Navigate to Sent Items. URL fallback if clicking the nav item fails: `https://outlook.office.com/mail/sentitems`.
2. Click the search bar at the top of Outlook. Type the queue subject WITHOUT the leading `RE: ` (e.g., if queue subject is `RE: Bell / servers + compute for AI workloads`, search for `Bell / servers + compute for AI workloads`). Press Enter.
3. From the results, find the email whose To field matches the queue entry's `to` field exactly AND whose Sent date matches the prior email in this sequence (for Email 2 of a 6-email sequence this is typically 2 business days ago). Open it.
4. If no matching sent email exists, STOP. Do not fall back to New mail. Report: `Could not find original sent thread for <id>. Not sent.` Move on.
5. Click the `Reply` button (top right of the reading pane, or at the bottom of the email).
6. The reply compose opens inline. VERIFY all three fields:
   - **To**: must equal the queue `to` exactly. **Fix mismatches automatically, do not STOP.** Outlook's Reply on a sent email resolves To: from the original message's From: line, not the original To: line. When the Email 1 went out from a non-canonical sender alias (e.g. `andy@osihardware.onmicrosoft.com` for **every Desjardins prospect**, Etienne Trudel, Marc Delaune, and any other `@desjardins.com` recipient, and any other case where the alias shows up in the quoted `From:` line at the bottom of the compose body), Reply will pre-fill To: as "Andrew McLean" (Andy himself, the alias resolved to a Display Name). The queue entry's `to` field is authoritative. **Self-heal:** click the X on the wrong To: tag, click into the empty To: field, type the queue `to` address, press Tab to convert it to a tag. Then continue. Do NOT compose with the wrong recipient. Do NOT skip the entry.
   - **Subject**: matches the queue `subject` exactly (`Re: ...` vs `RE: ...` case difference is fine. Outlook's autofill is canonical). If subject is wrong, STOP.
   - **Body**: cursor at the top, then Outlook's signature, then the grey divider and From/Sent/To/Subject header, then the original email body. If no grey divider appears, STOP. That means Reply did not attach the thread properly.
7. Parse the queue `body` to extract ONLY the new reply text. The new text is everything BEFORE the first quote marker. Recognize any of these as quote markers:
   - A line matching `----------\s*On .* wrote ----------`
   - A line matching `On .*, (Andy )?McLean .*wrote:`
   - A line starting with `> `
   - A line starting with `From: Andrew McLean`
   Take the text before the first marker, strip trailing whitespace. For Email 2 in the standard sequence, this is almost always just `Any thoughts?`.
8. Click at the very top of the body (above the signature) and type the new reply text. If it has multiple paragraphs, separate them with a blank line (see Step 4 for the mechanical details).
9. **Trim the signature's leading blank down to exactly ONE.** This is the single most common failure mode. See Step 4 for the exact code pattern. You must do this every time, even if the compose "looks fine". The second blank is invisible-looking but it is there.
10. Run the preview check in Step 5. Do not skip it.
11. Click `Send`.
12. Confirm success: the compose closes and the email appears in Sent Items with the reply arrow icon next to the recipient. If a dialog appears ("Discard?", "Send without subject?", etc.), STOP and read it.

---

## Step 3B: NEW MAIL flow (subject does NOT start with `RE: `)

0. **Step 2C CONNECTION REQUEST GATE must have already run for this entry.** If this is an Email 1 (id ends in `-1` or sendTime=4pm with no RE: prefix), Step 2C already checked for an open LI task. If the gate fired, you would not be here (it skips to the next entry). If you are here, the gate ran and found no NOT_STARTED task. Proceed.
0a. **RUN THE PRE-SEND GATE FIRST.** See the 🛑 MANDATORY PRE-SEND GATE 🛑 section at the top of this file. Re-read the queue entry from disk by `id`. Confirm `status == "pending"` and `to` is not in the hard-block list. If either fails, SKIP this entry. This is not optional. Brett Baker / Lippert 2026-04-22 is why.
1. Navigate to `https://outlook.office.com/mail/deeplink/compose?to=<URL-encoded to>&subject=<URL-encoded subject>`.
2. Wait up to 6 seconds for the compose body to render (`[aria-label="Message body"][role="textbox"]` must exist).
3. Verify the To and Subject fields are populated correctly from the URL. If either is empty or wrong, STOP.
4. **MANDATORY pre-insertion strip.** Before typing anything, sanitize the queue `body` by removing any prior-thread placeholder content. Fresh-subject Email 3/4/5/6 entries must NEVER ship with `On <date>, Andy McLean wrote:` separators or `>` quoted lines in the body, those are upstream-skill bugs and they produce malformed emails (2026-04-29 incident: 11 prospects received Email 3s with hand-rolled quote blocks because the chat-session runner skipped this strip). Apply the same regex the Reply flow uses in Step 3A.7. If a quote marker is found, take everything BEFORE it, strip trailing whitespace, and use that as the body to insert. Do NOT abort; do NOT skip the entry; just clean and continue. Log the strip in the Step 7 run report under a "Defensive quote-strip" line so Andy can see which upstream entries had the bug.
5. Click at position 0 of the body (top, above the signature).
6. Insert the SANITIZED body (from step 4), splitting on `\n\n` for paragraph breaks. Use this exact cursor-positioning pattern:

```js
// Position cursor INSIDE the first <p> child of the body (not before it).
// setStart(body, 0) puts the cursor before ALL child nodes, which means
// insertParagraph would push an empty <p> above the first line and render
// as a visible blank line before "Hi Name," in the received email.
// Setting the range start on the first child positions it inside that <p>.
const firstChild = body.firstChild;
const r = document.createRange();
r.setStart(firstChild, 0);
r.collapse(true);
const s = window.getSelection();
s.removeAllRanges();
s.addRange(r);

// DO NOT call insertParagraph here. Type directly into the existing first <p>.
for (let i = 0; i < paras.length; i++) {
  document.execCommand('insertText', false, paras[i]);
  document.execCommand('insertLineBreak');
  document.execCommand('insertLineBreak');
}
```

Two `insertLineBreak` calls after every paragraph (including the last) produce `<br><br>` which Outlook renders as exactly one blank line. The last pair gives `nlBB=2` before "Best," matching TARGET=2. Do NOT use `insertParagraph` anywhere in the body insertion -- it creates separate `<p>` elements whose CSS margin causes double-spacing (2026-05-20 bug, 6 real sends) or a leading blank line above the first name (2026-05-20 second bug).

7. Do NOT add any extra calls after the last paragraph. The `insertLineBreak x2` after the last paragraph already provides the gap before "Best,".
7a. **MANDATORY leading-blank strip.** After insertion, position the cursor immediately before the FIRST character of the first body paragraph (e.g., before "Hi" in "Hi David,"). Count `\n` characters preceding it in innerText. While that count is greater than 0, run `document.execCommand('delete', false)` to Backspace each one out. This is required because Outlook's empty compose has 1-2 empty paragraphs above the signature; positioning the cursor at "Best," and inserting body text leaves those empty paragraphs ABOVE the inserted body, which renders as 2-3 blank lines above "Hi <Name>,". Andy caught this on 2026-04-30 (David Thomas/SiFi was the first email of that 11am run). Without this strip the email looks malformed even when the rest is correct. Same logic must run on Reply flow too. See Step 3A addition.
8. **Trim the signature's leading blank to TARGET=2.** Same rule as Reply flow. See Step 4.
9. Run the preview check in Step 5.
10. Click `Send`.
11. Confirm success: compose closes, email in Sent Items.

---

## Step 4: Body formatting mechanics

### Signature trim: target EXACTLY ONE blank line between the last sentence and `Best,`

This is the single rule that matters most. The rendered email must look like this:

```
...the last sentence of your body text.
                                         ← exactly ONE visible blank line
Best,
<<YOUR_NAME>>
Andy McLean
Solutions Executive
...
```

**TARGET = exactly 2 `\n` characters in `body.innerText` immediately before `Best,`.** With the `insertLineBreak` × 2 paragraph approach, each `<br>` in the body creates 1 `\n` in innerText. Two `<br>` tags between paragraphs = 2 `\n` = one visible blank line. The same count applies before "Best,": TARGET=2 pads to exactly one visible blank line. Confirmed empirically on 2026-05-20 via formatting test 2 (nlBB=2, correct render in Outlook reading pane).

History: TARGET was 5 with the old `insertParagraph` × 2 approach, because Outlook's `<p>` structure reads as 5 `\n` between paragraphs. That approach was retired on 2026-05-20 after 6 real sends went out double-spaced (2 visible blank lines between every paragraph). The root cause was that 2 `insertParagraph` calls create a separate empty `<p>` element whose CSS margin stacks against adjacent paragraphs, rendering as 2 visible blank lines. The `insertLineBreak` approach writes `<br>` inside the current `<p>`, which Outlook renders at exactly 1 line height. TARGET=2 is correct for this approach. Do NOT revert to TARGET=5 or insertParagraph × 2.

The trim below is bi-directional: it Backspaces if there are too many newlines AND inserts paragraph breaks if there are too few. Do not assume the starting state. Always run this.

Run this after inserting the body text, before clicking Send:

```js
const body = document.querySelector('[aria-label*="Message body"][contenteditable="true"]');
if (!body) throw new Error('Message body not found');
body.focus();

function newlinesBeforeBest() {
  const text = body.innerText;
  const idx = text.indexOf('Best,');
  if (idx < 0) return -1;
  let n = 0;
  for (let i = idx - 1; i >= 0 && text[i] === '\n'; i--) n++;
  return n;
}

// Place the cursor immediately before the "B" in "Best,".
const walker = document.createTreeWalker(body, NodeFilter.SHOW_TEXT);
let textNode = null, offset = 0, node;
while ((node = walker.nextNode())) {
  const i = node.nodeValue.indexOf('Best,');
  if (i >= 0) { textNode = node; offset = i; break; }
}
if (!textNode) throw new Error('"Best," not found in body text');
const range = document.createRange();
range.setStart(textNode, offset);
range.collapse(true);
const sel = window.getSelection();
sel.removeAllRanges();
sel.addRange(range);

// TARGET STATE: exactly 2 newlines immediately before "Best,".
// EMPIRICAL FINDING (2026-05-20): with the insertLineBreak x2 paragraph approach,
// each <br> tag = 1 \n in innerText. Two insertLineBreak calls between
// paragraphs = 2 \n = one visible blank line. The same count before "Best,"
// (TARGET=2) produces one visible blank line matching the body paragraph gap.
// Confirmed in formatting test 2 on 2026-05-20: nlBB=2 rendered correctly.
//
// History: the old approach used insertParagraph x2 between paragraphs with
// TARGET=5. That approach created separate empty <p> elements whose CSS margin
// stacked, producing double-spacing (2 visible blank lines). 6 real sends on
// 2026-05-20 went out double-spaced before the bug was caught. Switched to
// insertLineBreak x2 approach and TARGET=2 on 2026-05-20.
// Do NOT revert to TARGET=5 or insertParagraph x2.
const TARGET = 2;

// Too many newlines: Backspace down to TARGET.
let guard = 0;
while (newlinesBeforeBest() > TARGET && guard++ < 20) {
  document.execCommand('delete', false);
}

// Too few newlines: insert paragraph breaks up to TARGET.
// (Cursor is still positioned immediately before "Best,". Every insertParagraph
// adds one \n before the cursor.)
guard = 0;
while (newlinesBeforeBest() < TARGET && guard++ < 20) {
  document.execCommand('insertParagraph');
}

const finalCount = newlinesBeforeBest();
if (finalCount !== TARGET) {
  throw new Error(`Signature trim failed: ${finalCount} newlines before "Best," (want exactly ${TARGET} = one visible blank line)`);
}
```

After this runs, the rendered body shows exactly ONE visible blank line between the last typed line and `Best,`. Not two. Not zero. One. If the function throws, STOP and surface to Andy. Do not send a broken email.

**Visual reference (THIS is what every email must look like):**

```
GOOD:                                BAD (do not ship):
Worth 15 minutes...?                 Worth 15 minutes...?
                                     Best,
Best,                                Andy
Andy
```

The GOOD column has one visible blank line between the last sentence and "Best,". That requires **2 `\n` in innerText** (TARGET=2, see Step 4) with the `insertLineBreak` x2 paragraph approach. The BAD column has zero blank lines. **TARGET=2.** See Step 4 rationale block for the full empirical history.

### Two spaces after every sentence

Every sentence-ending punctuation mark (`.`, `?`, `!`) must be followed by TWO spaces before the next sentence. `document.execCommand('insertText', ...)` collapses consecutive ASCII spaces back to one. The fix: the second space must be a non-breaking space (`\u00a0`).

Before inserting any paragraph, transform the text:

```js
text = text
  .replace(/([.?!])  +/g, '$1 ')
  .replace(/([.?!]) (?=[A-Z0-9"'`])/g, '$1 \u00a0');
```

Apply per paragraph (after splitting on `\n\n`). Abbreviations like `Mr. Fox`, `U.S.`, `e.g.` can false-positive. If the queue body contains such a pattern and the transform would incorrectly double-space, log it and surface to the user before sending.

### Paragraph spacing

Every real paragraph in the body is separated by a full blank line in the rendered email. Mechanically: type each paragraph with `insertText`, then call `insertLineBreak` twice. Two `insertLineBreak` calls produce `<br><br>` within the same `<p>`, which Outlook renders as exactly one visible blank line.

**CRITICAL: cursor positioning at the start.** Always use `range.setStart(body.firstChild, 0)` to place the cursor INSIDE the first `<p>`. NEVER use `range.setStart(body, 0)` followed by `insertParagraph` -- that creates an empty `<p>` above the first line which renders as a blank line before "Hi Name," in the received email (2026-05-20 bug).

Do NOT use `insertParagraph` anywhere in the body insertion. It creates separate `<p>` elements whose CSS margin causes either double-spacing between paragraphs or a spurious blank line at the top of the email.

Call `insertLineBreak` twice after every paragraph including the last. This gives `nlBB=2` before "Best," without any separate trim step needed (though the trim still runs as a safety check).

### Never type a sign-off

NEVER type `Best,` or `Andy` or any name at the bottom of the body. Outlook's signature block does that automatically. Typing it produces a doubled sign-off.

---

## Step 5: Preview check, mandatory before every Send

Before clicking Send, run these five checks. If any fails, do not send.

1. **Take a screenshot of the compose window.** Look at it. Count the blank lines between the last line of your typed text and `Best,`. It must be exactly ONE. Two blanks means the signature trim did not run or targeted the wrong count. Zero means you over-trimmed.
2. **Reply flow only**: confirm the grey horizontal divider is present below the signature and the `From: / Sent: / To: / Subject:` header shows real data (Andrew McLean as the From, the original recipient as the To, the original subject without `RE:`, a plausible prior date).
3. **No fake quote header in the body.** Search the body text for `---------- On` or `On .*, Andy McLean .*wrote:` or lines starting with `> `. If any match appears in what you typed at the top, you accidentally typed the full queue body including its fake separator. STOP. Clear the body and redo.
4. **Read `body.innerText.slice(0, 800)`.** Confirm each paragraph from the queue body appears on its own line, separated by exactly one blank line. Confirm no stray `Andy` typed manually at the end. Confirm no double-space after abbreviations that were not actual sentence endings.
5. **EM-DASH / EN-DASH CHECK.** Run: `body.innerText.includes('\u2014') || body.innerText.includes('\u2013')`. If true, ABORT. Em-dashes and en-dashes tell prospects an AI wrote the email. That destroys the outreach. Never send a body that contains either character.

If all five pass, click Send.

---

## Step 6: Update the queue (with per-entry audit fields)

After each successful send, flip the entry's `status` to `sent` AND append per-entry audit fields. These fields make a post-hoc audit possible in 30 seconds, no Sent Items archaeology required. The 2026-04-29 incident was found only because Andy noticed Bryan Ackerman's broken Email 3 by eye, hours after it shipped. With audit fields, anomalies surface from the queue file alone.

### Required audit fields

After Send is confirmed (compose closed, item in Sent Items, no `[Draft]` prefix), capture these fields BEFORE flipping status:

```js
// Run inside the compose window right before clicking Send (Step 5 has the body in hand).
const body = document.querySelector('[aria-label*="Message body"][contenteditable="true"]');
const typedText = body.innerText;

// Find the user-typed portion by stripping signature + thread quote.
// Signature starts at the FIRST occurrence of "Best," in innerText.
const bestIdx = typedText.indexOf('Best,');
const userTyped = bestIdx > 0 ? typedText.slice(0, bestIdx).trimEnd() : typedText.trimEnd();

// Newlines immediately before "Best,". TARGET=5 per Step 4. Anything else = bug.
let trimFinalCount = -1;
if (bestIdx > 0) {
    let n = 0;
    for (let i = bestIdx - 1; i >= 0 && typedText[i] === '\n'; i--) n++;
    trimFinalCount = n;
}

// SHA-256 of the user-typed text (not the signature, not the quoted thread).
async function sha256(s) {
    const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
    return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
}
const bodyHash = await sha256(userTyped);

// Capture the result for the Python writer below.
window.__sendAudit = {
    bodyHash,
    bodyLen: userTyped.length,
    trimFinalCount,
    previewChecksPassed: true,  // set false if any Step 5 check failed (you should not be here)
    flow: bestIdx > 0 ? 'detected' : 'no-best-marker'  // sanity flag
};
```

Then flip the queue entry, attaching the audit block:

```python
import json, os, tempfile, datetime
path = 'C:/Claude-Brain/email-queue.json'
with open(path) as f: q = json.load(f)
now_iso = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
for e in q:
    if e.get('id') == '<id>':
        e['status'] = 'sent'
        e['audit'] = {
            'sentAt':              now_iso,                 # UTC ISO8601
            'window':              CURRENT_WINDOW,          # '11am' | '12pm' | '1pm' | ...
            'flow':                FLOW,                    # 'reply' | 'new-mail'
            'bodyHash':            BODY_HASH,               # SHA-256 of user-typed text
            'bodyLen':             BODY_LEN,                # int, char count
            'trimFinalCount':      TRIM_FINAL_COUNT,        # newlines before "Best," (must be 2)
            'previewChecksPassed': PREVIEW_CHECKS_PASSED,   # bool
            'senderVersion':       'osi-email-sender@2026-04-30',  # bump on any structural change
        }
        break
fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix='email-queue.', suffix='.tmp')
with os.fdopen(fd, 'w') as f: json.dump(q, f, indent=2)
os.replace(tmp, path)
```

### Why each field

- **sentAt**: UTC timestamp. Reconstructs the exact timeline.
- **window**: which window fired. Distinguishes scheduled fire from a manual run.
- **flow**: `reply` or `new-mail`. The 2026-04-29 incident was a flow mismatch (Email 3 went through new-mail when the runner thought it was reply-attached). Recording flow makes the mismatch visible.
- **bodyHash + bodyLen**: SHA-256 of the user-typed portion (excluding signature and thread). Two prospects whose bodies hash identical = the drafter wrote the same body twice (a bug). A short hash (bodyLen < 50 chars on a fresh-subject email) = drafter shipped a stub.
- **trimFinalCount**: must be 2 per Step 4. If it's 1, signature trim under-padded. If 3+, over-padded. If anything other than 2, the email shipped with the wrong gap, exactly like 2026-04-29.
- **previewChecksPassed**: belt-and-suspenders. The Step 5 preview checks should have aborted before Send if any failed; recording the result lets a future audit confirm the abort actually fired.
- **senderVersion**: lets future audits see WHICH version of this skill produced the entry. Bump the date on every structural change.

### Audit query examples

After a run, sanity-check the day's sends from the queue alone:

```python
import json
from collections import Counter
with open('C:/Claude-Brain/email-queue.json') as f: q = json.load(f)
today = '<YYYY-MM-DD>'
sent_today = [e for e in q if e.get('status') == 'sent' and (e.get('audit') or {}).get('sentAt','').startswith(today)]

# Anomaly 1: any trimFinalCount != 2
bad_trim = [e['id'] for e in sent_today if (e.get('audit') or {}).get('trimFinalCount') != 2]
if bad_trim:
    print(f"FLAG: {len(bad_trim)} sends with wrong gap before 'Best,': {bad_trim[:5]}")

# Anomaly 2: duplicate bodyHash (drafter shipped same body twice to different prospects)
hashes = Counter(e['audit']['bodyHash'] for e in sent_today if e.get('audit',{}).get('bodyHash'))
dupes = [h for h, n in hashes.items() if n > 1]
if dupes:
    print(f"FLAG: {len(dupes)} bodies sent to multiple prospects (likely drafter bug)")

# Anomaly 3: any preview check failure
failed_preview = [e['id'] for e in sent_today if (e.get('audit') or {}).get('previewChecksPassed') is False]
if failed_preview:
    print(f"FLAG: {len(failed_preview)} sends where preview checks failed but Send was clicked anyway: {failed_preview}")
```

If any anomaly fires, flag immediately to Andy in the Step 7 run report.

### Atomic write rules (unchanged from before)

Never delete the file first. Never use the Write tool for the queue. One atomic write per email, not a single bulk write at the end. If something crashes mid-run, status must be truthful for what actually went out.

---

## Step 7: Log the run

Append a summary to `C:\Claude-Brain\sessions\session-YYYY-MM-DD.md` under a heading for the window that just fired. Include:
- Window (e.g., `11am ET`)
- Count sent, count skipped, count errored
- List of IDs sent, with any flags or anomalies
- Next scheduled window and how many pending entries it will process

### 🔍 AUDIT ANOMALY CHECK (mandatory, runs at end of every fire)

After all sends in this window are queued, scan the audit blocks of THIS WINDOW's sends for anomalies. Use the queries from Step 6. Surface findings in the run report. The whole point of writing audit fields is to catch problems automatically; if the report doesn't run the queries, the fields are just noise.

Mandatory checks:
1. **Trim gap mismatch**: any `audit.trimFinalCount != 2` is a layout bug. Same root cause as the 2026-04-29 zero-blank-line incident. Flag every ID by name.
2. **Duplicate body hash**: two or more sends in this window with the same `audit.bodyHash` mean the drafter shipped the identical body to multiple prospects. Almost always a bug (template variable not interpolated). Flag.
3. **Preview check failure**: any `audit.previewChecksPassed == false` means a Send was clicked despite a failed Step 5 preview. That should never happen; if it did, the operator overrode a safety check. Flag loudly.
4. **Suspicious body length**: any `audit.bodyLen < 50` on a fresh-subject email is probably a stub or truncated send. Flag.

Format in the run report:

```
🔍 AUDIT ANOMALY SCAN
Window: <window> ET
Sends scanned: N
Status: <clean | N anomalies>

If anomalies:
  - <id>, <field>=<value>, <one-line interpretation>
```

If clean: state "Audit anomaly scan: clean, N sends, all fields nominal" so Andy has positive confirmation the scan ran.

### 🔗 Connection Request Gates section (mandatory, even when empty)

Every run report MUST include a "Connection request gate" section. This is how Andy knows which Email 1s were held and rescheduled.

Format:

```
🔗 CONNECTION REQUEST GATES
Status: <clean (0 fires) | N gates fired>

If gates fired:
  - <entry id>: LI task NOT_STARTED (<task id>). E1 rescheduled from <old date> to <new date>. E2-E6 respread +<N> business days. HubSpot task updated.
```

If clean: write "Connection request gate: clean, 0 fires" so Andy has positive confirmation the check ran.

### 🚨 Hard-block hits section (mandatory, even when empty)

Every run report MUST include a "Hard-block scan" section. This is how Andy knows whether upstream sequences are enrolling prospects against blocked contacts.

Format:

```
🚨 HARD-BLOCK SCAN
Status: <clean | N hits>

If hits:
  - <Prospect name> (<email>), rule: <address|domain>, enrolled by: <upstream sequence, inferred from queue history>, action: cancelled all remaining entries in that sequence
```

This is the piece Andy explicitly asked for on 2026-04-23: notify on every blocked enrollment. Never bury a hard-block hit inside aggregate counts. Always call it out by name with context so Andy can go upstream and stop the enrolling skill from doing it again.

---

## Failure modes (learned the hard way, don't repeat these)

- **Hand-rolled quote headers (2026-04-22).** Brett Baker / Lippert was left sitting as a draft in Sent Items, and Lance Weaver / Rackspace went out to a real prospect, both with the entire queue body typed into a New mail compose including a fake `---------- On April 16, Andy McLean wrote ----------` separator. No grey divider. No real From/Sent/To/Subject header. The original body was retyped instead of quoted natively. It looks like spam. Root cause: sender ignored Step 2 and went straight to New mail for every entry. For `RE: ` subjects the ONLY correct flow is Step 3A. New mail is for fresh subjects only.
- **Wrong-sized gap before signature.** The target is ALWAYS exactly one visible blank line between the last typed sentence and `Best,`. Mechanically, **exactly 2 newlines in `innerText` immediately before `Best,`** (TARGET=2 in Step 4, with the insertLineBreak x2 paragraph approach). The Step 4 trim is bi-directional. It pads up or Backspaces down to that target. Historical context: Josh Harless / Hunter went out with too many blanks. Ben Wexler / KeyBank went out with zero. Noriel Ocampo / DOCOMO 2026-04-22 shipped with four. The 2026-04-29 run shipped with ZERO (TARGET was 1, bumped to 2, but 2 still failed with insertParagraph approach so it went to 5). 2026-05-20: switched to insertLineBreak x2 approach, TARGET=2 now correct and empirically confirmed. **TARGET is 2 with the insertLineBreak approach. Do NOT revert to TARGET=5 or insertParagraph x2.**
- **Paragraphs double-spaced (2026-05-20 bug).** Using `insertParagraph` x2 between paragraphs creates a separate empty `<p>` element. Outlook's CSS gives each `<p>` a margin, so an empty `<p>` between two content `<p>` elements renders as approximately 2 visible blank lines. 6 real sends went out double-spaced on 2026-05-20 before Andy caught it. Fix: use `insertLineBreak` x2 between paragraphs instead. This writes `<br><br>` within the same `<p>`, rendering as exactly 1 visible blank line.
- **Spurious blank line before first name (2026-05-20 second bug).** Using `range.setStart(body, 0)` then `insertParagraph` to open the body pushes an empty `<p>` ABOVE the cursor. That empty paragraph renders as a blank line before "Hi Name," in the received email. 7 sends went out with this leading blank on 2026-05-20 (Kevin Dancs, Noriel Ocampo, Etienne Trudel, Marc Delaune, Jonghwan Kim, David Thomas, Edward Fox). Fix: use `range.setStart(body.firstChild, 0)` to place the cursor INSIDE the existing first `<p>`, then type directly. No `insertParagraph` call at the start, ever.
- **Paragraphs with zero spacing.** Using a single `insertLineBreak` (or no call) produces 1 `\n` in innerText, which Outlook renders as 0 visible blank lines (line wrap only). Always use `insertLineBreak` x2 between paragraphs.
- **Sending before verifying.** Clicking Send before running the preview check has burned real prospect outreach multiple times. Do the preview check every single email, even if the previous 9 looked fine.
- **Signature dup.** Typing `Best,` or `Andy` at the bottom of the body produces a doubled sign-off. The queue body never contains a sign-off. Respect that and insert only what's there.
- **Draft left in Sent Items on a failed Send.** If the Send click is intercepted by a Discard dialog, the compose closes without actually sending but leaves a `[Draft]` entry in Sent Items. After every Send, confirm the Sent Items item does NOT have the `[Draft]` prefix before marking the queue entry as `sent`.
- **Reply auto-resolves To: to "Andrew McLean" (self) instead of the prospect.** Happens when the original Email 1 was sent from a non-canonical Andy alias, `andy@osihardware.onmicrosoft.com` is the documented recurring case. **Every Desjardins email Andy sends (any `@desjardins.com` address) goes out from this legacy alias, so every Desjardins follow-up will trigger this.** Outlook's Reply pre-fills To: from the original From: line, which resolves to Andy's own Display Name, not the actual recipient. The 2026-04-28 4pm run hit this on `etienne-trudel-desjardins-2` and `marc-delaune-desjardins-2`. Step 3A.6 above now handles this with self-heal: remove the wrong tag, type the queue `to` address, press Tab. Do NOT stop. Do NOT need a queue-entry-level annotation. The skill knows.
- **Hand-rolled quote header in fresh-subject Email 3/4/5/6 (2026-04-29).** A manual chat-session runner sent 11 Email 3s on the 3pm slot where the queue body contained an `On <date>, Andy McLean wrote: > [Email 2] > > On <date>, Andy McLean wrote: > > [Email 1]` placeholder block. Email 3+ are NEW MAIL flow (fresh subject = standalone touch), so Outlook does not attach a thread. The runner typed the entire body verbatim, including the placeholder, and 11 prospects (incl. Bryan Ackerman / BNY Mellon) received emails that look like obvious AI slop. Two layers of bug: (1) upstream `osi-outreach-sequence` was writing the placeholder block into Email 3+ queue bodies, fixed 2026-04-29 by removing the "Quote Email N thread" instruction from the sequence skill; (2) downstream `osi-email-sender` Step 3B did not strip placeholder text before insertion, fixed 2026-04-29 by adding a MANDATORY pre-insertion strip in Step 3B.4. If future Claude sessions see queue bodies containing `>` lines or `On <date>, .* wrote:` markers in fresh-subject entries, the sender now strips them automatically and logs the strip. Do not remove that strip; it is defense-in-depth against upstream regressions.
