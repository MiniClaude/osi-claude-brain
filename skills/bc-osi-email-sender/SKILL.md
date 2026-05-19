---
name: bc-osi-email-sender
description: A/B TEST VERSION of osi-email-sender. Send all due emails from C:\Users\Mini\Documents\osi-claude-brain\automation\email-queue.json via Outlook with bi-directional signature trim, em-dash/en-dash sanitizer, OneDrive-synced queue, externalized hard-block.json, mandatory pre-flight hard-block scan, and ET send windows. ONLY trigger this skill when the user explicitly says "run bc-osi email sender", "bc-osi-email-sender", "run the BC sender", "run the new sender", "test the new sender", "A/B sender", or invokes /bc-osi-email-sender. Do NOT auto-trigger on generic phrases like "send my emails", "run the queue", or "send due emails" — those route to the legacy osi-email-sender. Runs 11am, 12pm, 1pm, 2pm, 3pm, 4pm ET weekdays.
---

# 🛑 ABSOLUTE FIRST ACTION: VERIFY YOU ARE READING THE LIVE SKILL 🛑

**Before doing anything else, run this check:**

1. Use the Read tool on `C:\Users\Mini\Documents\osi-claude-brain\skills\osi-email-sender\SKILL.md`. That file is the ONLY authoritative version.
2. If you are currently reading any other copy (e.g., a `SKILL.md` in `/mnt/uploads/`, an inlined copy pasted into a scheduled task prompt, a `.claude/skills/` runtime snapshot, or anything attached to this session that was written before today), STOP and reload from `C:\Users\Mini\Documents\osi-claude-brain\skills\osi-email-sender\SKILL.md`. Stale copies have caused real prospects to receive malformed emails. 2026-04-23: Joe Zarcone / Rackspace went out with a hand-rolled quote header and no grey divider because the runner was following a stale upload that did not contain Step 3A REPLY flow logic. This must not happen again.
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
QUEUE_PATH = 'C:/Users/Mini/Documents/osi-claude-brain/automation/email-queue.json'  # Live queue on OneDrive (real-time sync across laptops). Moved from C:/Users/Mini/Documents/osi-claude-brain/ on 2026-04-24.
HARD_BLOCK_PATH = 'C:/Users/Mini/Documents/osi-claude-brain/automation/hard-block.json'  # Hard-block list stays in Git (manually maintained, low churn)

with open(QUEUE_PATH) as f:
    queue = json.load(f)
with open(HARD_BLOCK_PATH) as f:
    hb = json.load(f)

entry = next((e for e in queue if e.get('id') == ENTRY_ID), None)
assert entry is not None, f"Entry {ENTRY_ID} not in queue"
assert entry['status'] == 'pending', f"SKIP: {ENTRY_ID} status is {entry['status']}, not pending"

# Hard-block enforcement. Single source of truth is C:/Users/Mini/Documents/osi-claude-brain/automation/hard-block.json.
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

## Step 1: Load the queue AND scan for hard-block enrollments

### 1A. Select candidate entries

Queue file: `C:\Users\Mini\Documents\osi-claude-brain\automation\email-queue.json`

Moved to OneDrive on 2026-04-24 specifically so the queue auto-syncs in real time between Andy's two laptops. OneDrive is the live sync mechanism for this ONE file. The rest of Claude-Brain still lives in Git at `C:\Users\Mini\Documents\osi-claude-brain\`. Do not read or write any `C:\Users\Mini\Documents\osi-claude-brain\automation\email-queue.json` path. If the OneDrive path is unreachable, ABORT. Do not fall back to Git.

Select entries where:
- `sendDate` equals today's date (YYYY-MM-DD, ET)
- `sendTime` matches the current hour window: one of `11am`, `12pm`, `1pm`, `2pm`, `3pm`, `4pm`
- `status` equals `pending`

Skip `cancelled` and `sent` entries.

If current hour is outside the six windows, do nothing and log the no-op. Do not dispatch.

### 1B. Pre-flight hard-block scan (MANDATORY — Andy must always know)

Before composing ANY email this window, scan the pending candidate set against `C:\Users\Mini\Documents\osi-claude-brain\automation\hard-block.json`. For every pending entry whose `to` matches a blocked address or whose domain matches a blocked domain, collect it into a `hard_block_hits` list.

Andy wants to be NOTIFIED any time an upstream sequence enrolled a prospect against a blocked address or domain. Silent skipping is not acceptable — a new sequence quietly failing to send is worse than visible failure, because Andy thinks outreach is going out when it isn't.

For each `hard_block_hits` entry, you MUST:
1. Do NOT compose or send that email.
2. Mark the queue entry `status = "cancelled"` with `cancelReason = "hard-blocked by <address|domain>. Was enrolled by <upstream sequence>. Flagged at <time>."` so it doesn't show up on future runs.
3. Surface the hit loudly in the Step 7 run report under a dedicated "🚨 HARD-BLOCK HITS — NEW ENROLLMENTS AGAINST BLOCKED CONTACTS" section. Include: prospect name (derive from `id`), email, which rule fired (exact address vs domain), which sequence enrolled them (infer from queue history — the first entry in the sequence will have been created by one of the outreach skills), and recommended action.

If there are zero hits, say so explicitly in the report ("Hard-block scan: clean, 0 hits") so Andy has positive confirmation the scan ran.

```python
import json
from datetime import datetime
with open('C:/Users/Mini/Documents/osi-claude-brain/automation/email-queue.json') as f: queue = json.load(f)
with open('C:/Users/Mini/Documents/osi-claude-brain/automation/hard-block.json') as f: hb = json.load(f)
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

### 2B. Decide the flow: Reply or New mail

Look at the queue entry's `subject`. Strip any surrounding whitespace.

- If it starts with `RE: ` (case-insensitive, with the space after the colon), it is a follow-up. Go to **Step 3A: REPLY flow**.
- Otherwise it is a fresh outreach. Go to **Step 3B: NEW MAIL flow**.

This decision is not a judgment call. It's a string prefix check. `RE: ` → Reply. Anything else → New mail.

---

## Step 3A: REPLY flow (subject starts with `RE: `)

### What the final email MUST look like

```
Any thoughts?                        ← the new reply text you typed

                                     ← exactly ONE blank line
Best,
Andy
                                     ← signature block (auto-inserted)
Andy McLean
Solutions Executive
Book a Meeting with Me
...
_________________________________    ← solid light grey horizontal divider
From: Andrew McLean <andy@osiglobal.com>
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
6. The reply compose opens inline. VERIFY all three fields are pre-populated correctly:
   - **To**: matches the queue `to` exactly. If not, STOP.
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

0. **RUN THE PRE-SEND GATE FIRST.** See the 🛑 MANDATORY PRE-SEND GATE 🛑 section at the top of this file. Re-read the queue entry from disk by `id`. Confirm `status == "pending"` and `to` is not in the hard-block list. If either fails, SKIP this entry. This is not optional. Brett Baker / Lippert 2026-04-22 is why.
1. Navigate to `https://outlook.office.com/mail/deeplink/compose?to=<URL-encoded to>&subject=<URL-encoded subject>`.
2. Wait up to 6 seconds for the compose body to render (`[aria-label="Message body"][role="textbox"]` must exist).
3. Verify the To and Subject fields are populated correctly from the URL. If either is empty or wrong, STOP.
4. Click at position 0 of the body (top, above the signature).
5. Insert the full queue `body`, splitting on `\n\n` for paragraph breaks. Between paragraphs insert one `insertParagraph` call followed by another `insertParagraph` call. The first ends the paragraph, the second creates the blank line between paragraphs.
6. Do NOT add an extra `insertParagraph` after the last paragraph. The signature already has a leading gap above it.
7. **Trim the signature's leading blank down to exactly ONE.** Same rule as Reply flow. See Step 4.
8. Run the preview check in Step 5.
9. Click `Send`.
10. Confirm success: compose closes, email in Sent Items.

---

## Step 4: Body formatting mechanics

### Signature trim: target EXACTLY ONE blank line between the last sentence and `Best,`

This is the single rule that matters most. The rendered email must look like this:

```
...the last sentence of your body text.
                                         ← exactly ONE visible blank line
Best,
Andy
Andy McLean
Solutions Executive
...
```

Andy updated his Outlook signature on 2026-04-23 to remove one leading blank line. With the new signature, the mechanical target is **exactly 1 `\n` character in `body.innerText` immediately before `Best,`**. That single `\n` is the paragraph break between the last body sentence and the signature block. Outlook's paragraph margin between those two elements IS the one visible blank line Andy wants. Adding an extra `\n` (making it 2) creates a second visible blank line, which is what has been happening and what Andy does not want. Target 1, never 2, never 0.

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

// TARGET STATE: exactly 1 newline immediately before "Best,".
// That renders as exactly one visible blank line between the last body sentence and Best,
// (Outlook's paragraph-margin CSS provides the visible gap; we do not need a second \n).
const TARGET = 1;

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

Every real paragraph in the body is separated by a full blank line in the rendered email. Mechanically: between two real paragraphs, call `insertParagraph` twice. One ends the current paragraph, the second creates the empty paragraph that renders as the blank line.

Do NOT call `insertParagraph` after the last real paragraph. The signature's leading blank provides the gap.

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

## Step 6: Update the queue

After each successful send, set that entry's `status` to `sent` via a plain Python atomic write:

```python
import json, os, tempfile
path = 'C:/Users/Mini/Documents/osi-claude-brain/automation/email-queue.json'
with open(path) as f: q = json.load(f)
for e in q:
    if e.get('id') == '<id>':
        e['status'] = 'sent'; break
fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix='email-queue.', suffix='.tmp')
with os.fdopen(fd, 'w') as f: json.dump(q, f, indent=2)
os.replace(tmp, path)
```

Never delete the file first. Never use the Write tool for the queue. One atomic write per email, not a single bulk write at the end. If something crashes mid-run, status must be truthful for what actually went out.

---

## Step 7: Log the run

Append a summary to `C:\Users\Mini\Documents\osi-claude-brain\sessions\session-YYYY-MM-DD.md` under a heading for the window that just fired. Include:
- Window (e.g., `11am ET`)
- Count sent, count skipped, count errored
- List of IDs sent, with any flags or anomalies
- Next scheduled window and how many pending entries it will process

### 🚨 Hard-block hits section (mandatory, even when empty)

Every run report MUST include a "Hard-block scan" section. This is how Andy knows whether upstream sequences are enrolling prospects against blocked contacts.

Format:

```
🚨 HARD-BLOCK SCAN
Status: <clean | N hits>

If hits:
  - <Prospect name> (<email>) — rule: <address|domain> — enrolled by: <upstream sequence, inferred from queue history> — action: cancelled all remaining entries in that sequence
```

This is the piece Andy explicitly asked for on 2026-04-23: notify on every blocked enrollment. Never bury a hard-block hit inside aggregate counts. Always call it out by name with context so Andy can go upstream and stop the enrolling skill from doing it again.

---

## Failure modes (learned the hard way, don't repeat these)

- **Hand-rolled quote headers (2026-04-22).** Brett Baker / Lippert was left sitting as a draft in Sent Items, and Lance Weaver / Rackspace went out to a real prospect, both with the entire queue body typed into a New mail compose including a fake `---------- On April 16, Andy McLean wrote ----------` separator. No grey divider. No real From/Sent/To/Subject header. The original body was retyped instead of quoted natively. It looks like spam. Root cause: sender ignored Step 2 and went straight to New mail for every entry. For `RE: ` subjects the ONLY correct flow is Step 3A. New mail is for fresh subjects only.
- **Wrong-sized gap before signature.** The target is ALWAYS exactly one visible blank line between the last typed sentence and `Best,`. Mechanically, exactly 2 newlines in `innerText` immediately before `Best,`. The Step 4 trim is bi-directional. It pads up or Backspaces down to that target regardless of what Outlook's signature block starts with. On 2026-04-23 Andy removed a leading blank from his signature, so the starting newline count is now smaller than it used to be. If you see a one-way trim that only Backspaces, it will under-trim and fail the assert. Always use the bi-directional version. Historical context: Josh Harless / Hunter went out with too many blanks, Ben Wexler / KeyBank went out with zero (over-trimmed), Noriel Ocampo / DOCOMO on 2026-04-22 shipped with four. Those were all one-way trims or skipped trims. Do not repeat them.
- **Paragraphs mashed together.** If you insert with a single `insertParagraph` between paragraphs, `innerText` shows a single `\n` between them and the rendered email has no visible gap. Always two `insertParagraph` calls between paragraphs.
- **Sending before verifying.** Clicking Send before running the preview check has burned real prospect outreach multiple times. Do the preview check every single email, even if the previous 9 looked fine.
- **Signature dup.** Typing `Best,` or `Andy` at the bottom of the body produces a doubled sign-off. The queue body never contains a sign-off. Respect that and insert only what's there.
- **Draft left in Sent Items on a failed Send.** If the Send click is intercepted by a Discard dialog, the compose closes without actually sending but leaves a `[Draft]` entry in Sent Items. After every Send, confirm the Sent Items item does NOT have the `[Draft]` prefix before marking the queue entry as `sent`.
