---
name: osi-email2-rewriter
description: Redraft pain-led Email 2s in the queue before the 11am send window. Pulls that morning's pending pain-led Email 2 entries, reads the matching Email 1 for context, researches the prospect's company for a fresh angle, drafts a 2-3 sentence replacement body with a concrete ask, and after Andy reviews, writes the new body back to the queue atomically. Trigger: scheduled daily 9:30 AM ET weekdays, or manually via "rewrite today's email 2s", "pull the pain-led follow-ups", "redraft email 2".
---

# osi-email2-rewriter

This skill fixes a gap in `osi-outreach-sequence`: for pain-led Email 1s (TPM, DWDM, storage, pre-owned, servers), the sequence writer ships Email 2 as a flat `Any thoughts?`, which is a weak bump for a consultative pitch. This skill rewrites those Email 2s the morning they're due, with Andy's review, before `osi-email-sender` fires at 11 AM.

Sample-offer Email 2s (SFP sample, DIMM sample, shipping question) stay as `Any thoughts?` — that bump is correct for a logistics question. This skill ignores them.

---

## Step 1: Pull today's candidate Email 2s

Read `C:\Claude-Brain\email-queue.json`. Select entries where ALL are true:
- `status == "pending"`
- `sendDate == today (YYYY-MM-DD, ET)`
- `sendTime == "11am"`
- `id` ends with `-2`

For each candidate, find the matching Email 1 by `id` prefix (same base, suffix `-1`). Classify archetype by scanning the Email 1 body for any of: `sample`, `swag`, `come into the office`, `ship it to` → sample-offer (SKIP, no rewrite needed). Otherwise pain-led (REWRITE).

If zero pain-led candidates, report "Nothing to rewrite this window" and stop.

---

## Step 2: For each pain-led Email 2, gather context

For each pain-led candidate:

1. Read Email 1's `body` and `subject` from the queue. That tells you the product pitched and the original pain.
2. Read the prospect's `people/` file and `accounts/` file in Claude-Brain if present. Use that for role, tenure, and company context.
3. Run ONE targeted external lookup for a fresh angle:
   - ZoomInfo scoops on the company (`mcp__...__enrich_scoops` or `search_scoops`) for news within the last 30 days.
   - If ZoomInfo returns nothing useful, one web search: `"[company name] [product line from Email 1]" 2026` — look for build announcements, hires, acquisitions, earnings calls, outages, regulatory filings.
4. Write down the chosen angle as a single sentence: "New [stat / pain / signal]: [what changed or what's true now that wasn't in Email 1]."

Do not spend more than 60 seconds per candidate on research. If nothing fresh surfaces, fall back to an adjacent-product-line angle (see Step 3B).

---

## Step 3: Draft the replacement Email 2 body

Rules:
- 2-3 sentences maximum. No greeting. No sign-off. Outlook signature handles the close.
- Do NOT repeat Email 1's argument verbatim. Reference it implicitly if at all.
- ONE concrete ask at the end. Not "Any thoughts?" Ask for a specific 15 minutes, a sample of a different product, a pointer to the right person, or a direct yes/no on a narrow question.

Pick ONE of three moves:

### 3A. New data point on the same pain
Sharpen Email 1's hook with a fresh stat, customer example, or lead-time number.

Example (Email 1 pitched DWDM):
> Most carriers in active buildout see OEM transport lead times stretch past a quarter by Q3. SmartOptics usually ships in weeks and runs 30 to 50% below Ciena or Nokia. Worth 15 minutes to compare this against what you have on order?

### 3B. Adjacent pain on a related OSI product line
Open a second door in a different OSI category.
- DWDM Email 1 → optics supply, TPM on the transport gear, professional services for the deploy.
- TPM Email 1 → pre-owned gear for spares, DIMMs on the same servers, storage-side TPM.
- Server / DIMM Email 1 → storage (NetApp TPM, pre-owned), pre-owned networking, component spares.
- Storage Email 1 → TPM on the storage OEM, server DIMMs, pre-owned networking.
- Pre-owned networking Email 1 → new Nokia, TPM on what they bought, optics to pair with it.

Example (Email 1 pitched TPM, pivoting to DIMMs):
> Also, since we source Samsung / Hynix / Micron DIMMs direct at manufacturer warranty and well below OEM, if any of your refresh is landing on Dell or HP servers where DDR4 still works, there's real budget in that line item. Want me to price out a sample config for one of your clusters?

### 3C. Company signal that surfaced since Email 1
Use the fresh external angle from Step 2.

Example (Email 1 pitched DWDM to a regional carrier, signal is a federal grant announcement):
> Saw Plateau's new NTIA middle-mile award for the New Mexico fiber rings came in last week. Timing lines up with where SmartOptics open-line DWDM usually saves regional carriers most. Worth 15 minutes before you finalize the transport vendor?

---

## Step 4: Present drafts to Andy for review

Output a concise block per candidate in chat. Format:

```
[ID]  ·  [First Name] @ [Company]  ·  sendTime 11am [sendDate]
Email 1 pitched: [one-line summary of Email 1's pain/product]
Angle chosen: [3A new data / 3B adjacent / 3C fresh signal — one line]
Draft:
[The 2-3 sentence body]
```

Keep each block under 8 lines. All candidates in one message, not one per.

Then ask: "Approve all / approve [IDs] / edit [ID] with [new text] / skip [ID] (sends as 'Any thoughts?')."

Do not touch the queue until Andy responds.

---

## Step 5: Write approved bodies back to the queue

For each approved (or Andy-edited) entry, construct the new `body` field as:

```
[approved reply text]

---------- On [Email 1 sendDate formatted "Month DD"], Andy McLean wrote ----------
[Full Email 1 body text]
```

The quote marker line anchors parsing in osi-email-sender — the sender uses native Outlook Reply at send time and the quote block Outlook auto-generates replaces this fake quote. The fake quote in the queue body is a parse anchor only.

Atomic write, one entry at a time:

```python
import json, os, tempfile
path = 'C:/Claude-Brain/email-queue.json'
with open(path) as f: q = json.load(f)
for e in q:
    if e.get('id') == '<id>':
        e['body'] = '<new body>'
        e['email2RewrittenAt'] = '<ISO datetime>'
        break
fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix='email-queue.', suffix='.tmp')
with os.fdopen(fd, 'w') as f: json.dump(q, f, indent=2)
os.replace(tmp, path)
```

Never use the Write tool for the queue. Never delete first. One atomic write per rewritten entry.

For "skip" entries, do not touch the queue — the existing `Any thoughts?` body stays.

---

## Step 6: Log the run

Append to `C:\Claude-Brain\sessions\session-YYYY-MM-DD.md` under an "Email 2 rewrite" heading:
- Candidates pulled: count + IDs
- Approved / edited / skipped per ID
- Any research that surfaced noteworthy signals worth escalating to a call task

---

## Failure modes to watch

- **Queue changed mid-flight.** Between presenting drafts and writing back, `osi-monitor` or Andy may have cancelled an entry. Re-read the entry's status right before writing; if not `pending`, skip the write and log it.
- **Email 1 not found in queue.** If you cannot find the matching `-1` entry, fall back to using the Email 2's own subject (strip `RE: `) plus any context from `people/` files. If still nothing, skip the rewrite for that entry and leave `Any thoughts?` — do NOT invent a pain or company signal.
- **Research came up empty.** Use 3B (adjacent product line) rather than skipping. Fabricating a fake "recent news" signal is worse than a generic product pivot.
- **More than 6 candidates in one window.** That's a lot of drafting. Present all of them in one message anyway — Andy will bulk-approve. Do not silently defer any; if he runs out of time he'll tell you to skip the rest.
- **Fabricated stats.** If you claim "DDR4 softened 15%", you must have a source. If you cannot cite one mentally, rephrase softer: "DDR4 pricing has kept drifting lower" instead of a false hard number. Andy represents these numbers on calls.

---

## When NOT to run

- Weekends. No 11am send window fires.
- US federal holidays when the sender is off.
- If `osi-email-sender` is disabled or the queue file is locked / unreadable.

If run manually by Andy mid-day (after the 11am send has fired), report "11am window already fired today — next candidates will be for tomorrow 11am" and list tomorrow's pain-led candidates so Andy can draft them ahead.
