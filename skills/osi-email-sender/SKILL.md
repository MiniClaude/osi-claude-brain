---
name: osi-email-sender
description: Send all due emails from C:\Claude-Brain\email-queue.json via Outlook. Runs 11am, 12pm, 1pm, 2pm, 3pm, 4pm ET weekdays.
---

# 🚨 READ THIS ENTIRE FILE BEFORE SENDING ANY EMAIL 🚨

This skill sends cold outreach to real, paying-potential customers. One bad format, one missed blank line, and Andy looks like a fool to a prospect he may be chasing for months. There is no "close enough." Follow every rule below exactly. If anything in this file is ambiguous, STOP and ask Andy. Do not guess.

---

## Step 1: Load the queue

Queue file: `C:\Claude-Brain\email-queue.json`

Do not read or write OneDrive. OneDrive is a dead archive.

Select entries where:
- `sendDate` equals today's date (YYYY-MM-DD, ET)
- `sendTime` matches the current hour window: one of `11am`, `12pm`, `1pm`, `2pm`, `3pm`, `4pm`
- `status` equals `pending`

Skip `cancelled` and `sent` entries.

If current hour is outside the six windows, do nothing and log the no-op. Do not dispatch.

---

## Step 2: Formatting rules — NON-NEGOTIABLE

The `body` field in the queue is plain text with `\n\n` between paragraphs. When inserting into Outlook's compose body you MUST preserve that structure as visible blank lines. This is where Claude has screwed up before. Read this section twice.

### Two spaces after every sentence
- Every sentence-ending punctuation mark (`.`, `?`, `!`) must be followed by TWO spaces before the next sentence begins, not one.
- CRITICAL GOTCHA: `document.execCommand('insertText', ...)` COLLAPSES consecutive ASCII spaces back to one when inserting into a contenteditable. Two literal spaces become one space in the rendered email. The fix: the SECOND space must be a non-breaking space (`\u00a0`), not a regular space. The browser will not collapse `\u00a0`, and most mail clients render it identically to a regular space.
- The queue body may have either single or double spacing — the sender is responsible for normalizing to "regular space + non-breaking space". Before inserting any paragraph into the compose body, run this transform on the text:

```js
// First normalize any 2+ ASCII spaces after sentence punctuation back to one, then expand to "space + nbsp" before any capital letter / digit / quote.
text = text
  .replace(/([.?!])  +/g, '$1 ')
  .replace(/([.?!]) (?=[A-Z0-9"'`])/g, '$1 \u00a0');
```

Apply per paragraph (after splitting on `\n\n`), so periods at the end of a paragraph aren't touched. Verify in the preview check that `body.innerText.split('Best,')[0]` does not match `/[.?!] [A-Z]/` — a hit means the second space was a regular space and got collapsed.

Do not double-space after abbreviations that don't end a sentence (e.g. `Mr. Fox`, `e.g.`, `U.S.`). The capital-letter-after-space heuristic handles most cases; if the queue body contains an abbreviation followed by a capitalized proper noun mid-sentence, the writer skill should have written it without a trailing space-then-capital pattern. If it didn't, the transform will incorrectly double-space — log it and surface to Andy rather than sending.

### Paragraph spacing
- Every paragraph in the body is separated by a **full blank line** in the final email. Not a single line break. A blank line. If the body has four paragraphs, there are three blank lines between them in the rendered email.
- Mechanically: between every real paragraph, call `document.execCommand('insertParagraph', false)` **twice**. One creates the paragraph break. The second creates the empty paragraph that renders as the blank line.

### Signature spacing — the part that has burned us repeatedly
- There MUST be exactly ONE blank line between the last paragraph of the body and the Outlook auto-signature block (the `Best,` / `Andy McLean` / etc. that Outlook appends).
- The Outlook compose body's signature block ships with TWO leading whitespace-only children stacked above `Best,`. Each one renders as a blank line. So out of the box: 2 blank lines. Adding an extra `insertParagraph` after the last body paragraph: 3 blank lines. Removing both leading whitespace children: 0 blank lines. The correct state is exactly ONE leading whitespace child remaining inside the signature block.
- After inserting the last body paragraph, do NOT call `insertParagraph` again. Then walk into the signature block and trim its leading whitespace-only children down to exactly one. Code pattern:

```js
const kids = [...body.children];
let sigIdx = kids.findIndex(c => (c.textContent || '').includes('Best,'));
const sig = kids[sigIdx];
let leading = 0;
for (const c of sig.children) {
  if ((c.textContent || '').replace(/\u00a0/g, '').trim()) break;
  leading++;
}
while (leading > 1 && sig.firstElementChild && !(sig.firstElementChild.textContent || '').replace(/\u00a0/g, '').trim()) {
  sig.removeChild(sig.firstElementChild);
  leading--;
}
```

After this, the sequence is: last paragraph → ONE empty element → `Best,`. That renders as exactly one blank line above `Best,`. Verified visually on David Thomas / SiFi and Edward Fox / MetTel on 2026-04-21.

### Do NOT type a sign-off
- NEVER type `Best,` or `Andy` or any name at the bottom of the body. Outlook's signature block does that automatically. Typing it creates a doubled sign-off.

### Mandatory preview-before-send check
Before clicking Send on each email, read back `body.innerText.slice(0, 800)` and verify:
- Each paragraph from the queue body appears on its own, separated by exactly one blank line. In `innerText` that shows as `\n\n\n` between paragraphs (the middle `\n` is the blank paragraph) — that's correct.
- The last paragraph is followed by exactly ONE blank line before `Best,`. Count it. Between `?\n` (or whatever the final paragraph ends with) and `Best,`, there should be exactly one empty line. More than one means too many blanks and you must NOT send.
- Two spaces after every sentence-ending `.`, `?`, `!` mid-paragraph. Search the preview for `\. [A-Z]`, `\? [A-Z]`, `\! [A-Z]` — any single hit means you missed the double-space transform. Stop and fix.
- No stray `Andy` typed manually at the end.

If any of those four checks fails, DO NOT SEND. Clear the body, re-insert, and recheck. If still broken after one retry, stop and surface to Andy.

---

## Step 3: Compose and send (one email at a time)

For each due entry:

1. Navigate to `https://outlook.office.com/mail/deeplink/compose?to=<URL-encoded to>&subject=<URL-encoded subject>`.
2. Wait (poll up to ~6 seconds) for the `[aria-label="Message body"][role="textbox"]` element.
3. Verify the To field shows the recipient and the Subject field shows the subject exactly. If either is empty or wrong, stop and surface to Andy — do not fix silently.
4. Place the cursor at position 0 of the body (see Formatting rules).
5. Insert paragraphs following the paragraph spacing rule above. STOP after the last paragraph — do NOT add any extra `insertParagraph` at the end. The signature's own leading gap is already present.
6. Run the preview-before-send check.
7. Click `button[aria-label="Send"]`.
8. Confirm success: compose collapses and a `Go to Inbox` button is the only visible button on that surface. If a dialog appears, stop and read it — do not dismiss blindly.

---

## Step 4: Update the queue

After each successful send, set that entry's `status` to `sent` via a plain Python atomic write:

```python
import json, os, tempfile
path = 'C:/Claude-Brain/email-queue.json'
with open(path) as f: q = json.load(f)
for e in q:
    if e.get('id') == '<id>':
        e['status'] = 'sent'; break
fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix='email-queue.', suffix='.tmp')
with os.fdopen(fd, 'w') as f: json.dump(q, f, indent=2)
os.replace(tmp, path)
```

Never delete the file first. Never use the Write tool for the queue. One atomic write per email (after send), not a single bulk write at the end — if something crashes mid-run, status must be truthful for what was actually sent.

---

## Step 5: Log the run

Append a summary to `C:\Claude-Brain\sessions\session-YYYY-MM-DD.md` (today's date) under a heading for the window that just fired. Include:
- Window (e.g., `4pm ET`)
- Count sent, count skipped, count errored
- List of IDs sent, with any flags or anomalies
- Next scheduled window and how many pending entries it will process

---

## Failure modes to watch for (learned the hard way)

- **Paragraphs mashed together.** If you inserted with a single `insertParagraph` between paragraphs, the output will show `\n` between them in innerText and render as no visible gap. This is wrong. Always two `insertParagraph` calls between paragraphs.
- **Wrong-sized gap before signature.** Out-of-the-box Outlook signature ships with 2 leading blank-line elements above `Best,`. Adding `insertParagraph` after the last body paragraph stacks to 3. Removing both leading blanks collapses to 0. Verified 2026-04-21 on the same window: Josh Harless / Hunter went out with 3 blank lines (extra insertParagraph), Ben Wexler / KeyBank went out with 0 (over-trimmed both leading blanks), David Thomas / SiFi and Edward Fox / MetTel went out correct. Use the trim-to-one code pattern in Step 2 every time. Verify visually in the preview check before Send — count the blank lines.
- **Sending before verifying.** Clicking Send before reading back `innerText` has burned real client outreach. Do the preview check every single time, even if the previous 9 looked fine.
- **Signature dup.** Typing `Andy` at the bottom produces a doubled sign-off. The queue body never contains a sign-off — respect that and insert only what's there.
