---
name: bc-4email-warm-reconnect
description: >
  4-email warm reconnect sequence for OSI Global contacts Brian has worked with before but has not talked to in a long time. Goal is to get a meeting to learn about changes and projects at their organization. Queues all 4 emails via the JSON sender, creates a HubSpot CALL task that shows in the daily morning to-do report. ALWAYS use this skill when Brian says anything like: "warm reconnect", "pulse check", "4-email reconnect", "catch up sequence", "haven't talked to in a while", "old contact reconnect", "warm sequence for", "get a meeting with", "check in with old contact", "reconnect with", or pastes a contact name, email, or HubSpot record and mentions it has been a long time since last contact. Trigger any time Brian wants a short reconnect sequence for someone he already knows personally or professionally.
---

# bc-4email-warm-reconnect

A 4-email sequence designed to re-open a relationship with someone Brian already knows, press for a meeting, and learn about what is changing at their organization. Shorter and warmer than cold outreach. Tone is collegial, not sales-y. The goal of every email is to get a reply that turns into a conversation.

All 4 emails go to the JSON queue. The bc-osi-email-sender picks them up at the next PT window on the scheduled send date. A HubSpot CALL task is created on Day 1 so it surfaces in the daily morning report.

---

## Signature Block

Every email body ends with just `Brian` on its own line. The sender appends the canonical signature block automatically:

```
Brian Charrette
Director of Key Accounts
Desk: 805.845.5167 | Cell: 805.682.9358
Systems: HPE / Dell / Cisco UCS / Supermicro / APC
Network: Cisco / Aruba / Juniper / Fortinet / APC / Opengear
Optical: Transceivers / DAC / AOC / Cables / DWDM Line Systems
Service: Systain Third Party Maintenance / Professional Services
```

---

## Step 1: Gather Prospect Info

Extract from what Brian provided:
- Full name
- Email address (required, no email means no sequence)
- Company
- Any context Brian has (last time they talked, what the relationship was, any known projects)
- LinkedIn URL if available

If Brian just pastes a name or email, pull the rest from HubSpot first (Step 2) before asking him.

---

## Step 2: Research

Run these in parallel:

**HubSpot lookup:** Search contacts by email or name. Pull job title, last contacted date, lifecycle stage, any notes. If there is deal history, note it briefly. This tells you how warm the relationship actually is and what OSI has sold them before.

**Web search:** Search the company name + "news" or "projects" for the last 60 days. Look for: leadership changes, acquisitions, new infrastructure investments, budget announcements, office expansions or closures, tech stack changes. One or two concrete recent signals give Email 1 something real to open with.

**OSI angle:** Based on title and company, pick the primary angle for the sequence:
- Network engineer or architect: optics, DWDM, interconnect gear
- IT director or VP: TPM cost savings, vendor simplification, EOL planning
- Procurement: competitive TPM bid, OpEx reduction
- Systems or infrastructure: server memory, EOL coverage, spares

---

## Step 3: Email Cadence

| Email | Send Date | Purpose |
|-------|-----------|---------|
| 1 | Day 1 (scheduled date Brian provides, or next Monday) | Warm hello, reference something current at their org, ask for a meeting |
| 2 | Day 1 + 3 business days | Light follow-up, make sure they saw Email 1, add a second angle |
| 3 | Email 2 send date + 7 calendar days | Third touch, pivot to a specific question about their environment |
| 4 | Email 3 send date + 10 calendar days | Soft close, leave the door open |

All send times: 11am PT (first available sender window).

Weekend and holiday skip: if a computed date lands on a weekend or US federal holiday, move to the next business day.

---

## Step 4: Write the 4 Emails

Brian's voice: direct, casual, no corporate fluff, short enough to read on a phone. Every email has one job.

**Humanizer rules (apply to every email before presenting):**
- No dashes anywhere, not in bodies, not in subject lines. Rewrite compound words without them: "on prem" not "on-prem", "follow up" not "follow-up", "long term" not "long-term"
- No em dashes or en dashes. Split into two sentences if needed.
- No AI vocabulary: no "crucial", "pivotal", "landscape", "underscore", "delve", "showcase", "testament", "enhance", "foster", "garner"
- No rule of three. Break triple lists into prose.
- Vary sentence length. Mix short punchy sentences with longer ones.
- Read it aloud mentally. If it sounds like a press release, rewrite it.

### Email 1: Warm Hello (Day 1)

- Open by referencing something real and current at their org (from research) OR the shared history if nothing current surfaced
- 2 to 3 short paragraphs
- One clear ask: 15 or 20 minutes to catch up
- No pitch. The goal is to reopen the conversation, not sell anything yet.
- End with `Brian`

Example tone: "Hey [Name], I saw [company] is [doing X]. Curious how that's landing on your side. It's been a while since we connected and I'd love to catch up. Worth a quick call this week?"

### Email 2: Did You See My Note (Day 1 + 3 bd)

- Reference the first email without being pushy
- Add one new angle, something different from Email 1, a question about their current environment or a shift in OSI value prop
- 2 short paragraphs
- Soft ask: "still worth a call?"
- End with `Brian`

### Email 3: Specific Question (Email 2 + 7 days)

- Drop the pleasantries. Get right to a direct question about their environment.
- One specific, relevant question based on their title and the OSI angle: EOL gear coming off warranty, optics refresh cycle, TPM contract renewal window, memory costs, etc.
- 2 to 3 sentences only
- "If yes, worth 15 minutes. If no, just say the word."
- End with `Brian`

### Email 4: Soft Close (Email 3 + 10 days)

- Acknowledge you have sent a few notes, respect their time
- Leave the door wide open, no pressure
- One sentence that makes it easy to reply even just to say "not now"
- Examples: "Should I close the file on this one, or is timing just off?" or "No worries if now is not the right time. Happy to circle back when things shift."
- End with `Brian`

---

## Step 5: Subject Lines

For each email, write 3 subject line options:
- 1 professional and direct
- 1 casual or curiosity-driven
- 1 unexpected or pattern-interrupting

Randomly select one per email. Present all 3 with the selected one marked so Brian can swap if he wants.

No dashes in subject lines.

---

## Step 6: Present for Review

Show Brian in one block:
1. Prospect summary: name, title, company, OSI angle, last contact date from HubSpot
2. The send schedule table (all 4 emails, dates, 11am PT)
3. Subject line options per email with selected one marked
4. Full body of every email

Stop. Do not write to the queue yet. Wait for Brian to say "run" or give a clear go-ahead.

---

## Step 7: On "Run"

When Brian says "run", "send it", "looks good", or any clear go-ahead:

### 7a: Write all 4 emails to the queue

Queue file: `C:\Claude-Brain\email-queue.json`

Use the OneDrive-safe Python pattern:
```python
import json, os

QUEUE = r'C:\Claude-Brain\email-queue.json'

try:
    with open(QUEUE, 'r') as f:
        queue = json.load(f)
except (OSError, ValueError):
    raise SystemExit("FALLBACK: use SharePoint MCP to fetch queue, then continue")
```

If the local open fails, search SharePoint for `email-queue.json` using the Microsoft 365 MCP, fetch the most recently modified version, and parse the JSON from the response.

Build 4 entries. Each entry:

```json
{
  "id": "[firstname]-[lastname]-[company-slug]-[N]",
  "prospectName": "First Last",
  "company": "Company Name",
  "to": "prospect@company.com",
  "bcc": "bc@osihardware.com, 21878985@bcc.hubspot.com",
  "subject": "[selected subject line]",
  "body": "[full email body, no signature]",
  "sendDate": "YYYY-MM-DD",
  "sendTime": "11am",
  "sendTimeZone": "PT",
  "replyMode": false,
  "status": "pending",
  "addedDate": "YYYY-MM-DD",
  "sequenceId": "[firstname]-[lastname]-[company-slug]",
  "emailNumber": 1,
  "cadenceGap": null,
  "priorEmailId": null
}
```

cadenceGap values: Email 1 = null, Email 2 = 3, Email 3 = 7, Email 4 = 10
priorEmailId: null for Email 1, then the id of the prior email for 2, 3, 4

Dedup before appending: scan existing queue for entries with the same `id`. If any match, skip them.

Atomic write:
```python
tmp = QUEUE + '.tmp'
with open(tmp, 'w') as f:
    json.dump(queue, f, indent=2)
os.replace(tmp, QUEUE)
```

If the local write fails, output the full updated JSON to a Python append script saved to the outputs folder and tell Brian to run it.

### 7b: Create HubSpot CALL task

Using `manage_crm_objects` (object type `tasks`):

- `hs_task_type`: `CALL`
- `hs_task_subject`: `Call [First Name] [Last Name] | [Company] | warm reconnect seq`
- `hs_task_body`: One-line note with the OSI angle and the Email 1 subject line. Example: "Sent warm reconnect Email 1 re: [hook]. Goal: 15 min catch-up to learn about changes and projects. Seq: 4 emails thru [Email 4 date]."
- `hs_task_status`: `NOT_STARTED`
- `hs_timestamp`: Email 1 send date in epoch milliseconds
- `hs_task_priority`: `HIGH`
- `hubspot_owner_id`: `213536174`
- Associate to the contact via associations with `associationTypeId: 204`

This task shows in Brian's daily morning report to-do list on Day 1.

### 7c: Confirm

Report back:
- `4 emails queued for [Name] at [Company].`
- Schedule: Email 1 [date], Email 2 [date], Email 3 [date], Email 4 [date], all 11am PT.
- `HubSpot CALL task created, due [Day 1 date]. Shows in morning report.`
- `BCC tracking on all 4: bc@osihardware.com + HubSpot timeline.`

---

## Notes

- If Brian does not give a specific Day 1 date, default to the next Monday.
- If Brian provides a send date that is a weekend or holiday, bump to the next business day and tell him.
- If the contact is already in an active sequence in the queue (status: pending entries in the last 30 days), flag it and ask before proceeding.
- This is a warm sequence, not cold outreach. Emails should feel like a person who actually knows the contact, not a template. Use any shared history from HubSpot notes or context Brian provides.
