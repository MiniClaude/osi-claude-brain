---
name: osi-meeting-followup
description: >
  Daily 10 AM ET runner that drafts follow-up emails for every Teams meeting Andy had in the last 24 hours.
  Pulls HubSpot Conversations Intelligence AI summary (`hs_call_summary`) for each call, parses the structured
  action items from the matching HubSpot recap email in Outlook, drafts a concise voice-clean follow-up email,
  and writes it to a HubSpot EMAIL task on the primary external contact (creates a new task or updates the
  existing one if found). Triggers on: scheduled task at 10 AM ET weekdays, or manually via "draft my meeting
  follow-ups", "run meeting followup", "what came out of yesterday's calls".
---

> Source: `C:\Claude-Brain\skills\osi-meeting-followup\` (Git, github.com/Drrewdy/Claude-Brain). Cowork `.claude/skills/` is a copy. Edit source, repackage, install.

# OSI Global, Meeting Followup Auto Drafter

---

## 🚦 WHAT THIS SKILL DOES

🛑 **TEAMS MEETINGS ONLY. NEVER VOICEMAILS. NEVER MISSED CALLS.** This skill drafts post-meeting follow-up emails. The trigger is a real recorded conversation with action items, the kind that comes out of a Teams meeting through HubSpot Conversations Intelligence. Voicemails, no-answer dial attempts, and any call without a structured CI summary get **skipped, no task created, no email drafted, nothing**. The follow-up channel for a voicemail is another phone call, not an email. If a future Claude session ever proposes "draft a follow-up email for this voicemail," point it at this section first.

Every weekday morning at 10 AM ET, this skill:

1. Finds all `calls` engagement records owned by Andy (`hubspot_owner_id: 196669355`) that completed between yesterday morning and now.
2. For each call, **verify it is a Teams meeting** (see Step 1.5 below). If not, skip with reason logged.
3. For each qualifying Teams meeting:
   - Pulls the AI-generated summary (`hs_call_summary` property, has Summary, Key notes, Topics discussed)
   - Looks up the matching HubSpot recap email in Andy's Outlook inbox (sender `noreply@notifications.hubspot.com`, subject `Next steps ready: <meeting title>`) and parses the structured **action items** list out of the email body HTML
   - Identifies the primary external contact (the non-OSI attendee)
   - Drafts a 2-3 sentence follow-up email per Andy's voice rules
   - Finds an existing pending EMAIL task on that contact, OR creates a new one (due same day, 12 PM ET)
   - Saves the draft as the task body
   - Saves a markdown copy to `C:\Claude-Brain\meetings\YYYY-MM-DD-<slug>.md`
   - Appends the action items to the meeting's `hs_internal_meeting_notes` so they show in the contact timeline
4. Posts a summary to `C:\Claude-Brain\meeting-followup-log.md` listing every meeting processed and what was drafted.

---

## 🛑 STOP CONDITIONS

- **No call records in the lookback window:** log "No meetings in last business day" and exit clean. (Lookback window = previous business day → now. On Monday this means Friday → now, not Sunday → now. See Step 1.)
- **Call is not a Teams meeting (Step 1.5 fails):** skip. NO email task created. NO draft written. NO call body update. Log reason ("voicemail", "no-answer dial attempt", "no CI summary structure") and move on. This is the most common skip reason and it is correct behavior.
- **Call has no `hs_call_summary` populated:** skip with reason "AI summary not yet ready", likely the recording hasn't finished processing. The next morning's run will pick it up.
- **No primary external contact identified:** skip with reason "internal-only call" (e.g., OSI team standup).
- **Recap email missing in Outlook:** still proceed using just the `hs_call_summary`, degrade gracefully. Note in log.
- **Task body already non-empty AND contains "===":** Andy has already worked on it. Don't overwrite. Append a "===Auto draft alternative===" footer with the new draft so Andy can compare without losing his edits.

---

## 📅 SCHEDULE

Cron: `0 14 * * 1-5` (10 AM Eastern = 14:00 UTC during EDT, 15:00 UTC during EST). Cowork adds ~9 min jitter so this typically fires ~10:09 AM ET. **Weekdays only**, never fires Sat/Sun.

Holidays.json is read at runtime to skip US federal holidays. If today is a holiday, the runner exits clean. The lookback window itself also walks back over weekends and holidays (see Step 1), so the first business day after a long weekend or holiday automatically catches the prior business day's calls.

---

## 🔍 STEP-BY-STEP LOGIC

### Step 1, Find calls since the previous business day

**Business days only.** Weekends do not count as a "yesterday." The lookback window starts at 00:00 UTC of the most recent prior business day (Mon-Fri, skipping weekends and US federal holidays from `holidays.json`) and ends at the current time.

- Tue-Fri run: lookback = previous calendar day (00:00 UTC) → now.
- Monday run: lookback = previous Friday (00:00 UTC) → now. This catches any call that happened Friday after the prior morning's run, plus weekend stragglers (rare but possible).
- Day-after-holiday run: lookback = the most recent non-holiday weekday (00:00 UTC) → now.

```python
from datetime import datetime, timedelta, timezone
import json, pathlib

def previous_business_day_start(now_utc: datetime) -> datetime:
    holidays = set()
    try:
        holidays = set(json.loads(pathlib.Path(r"C:\Claude-Brain\holidays.json").read_text()).get("us_federal", []))
    except Exception:
        pass
    d = now_utc.date() - timedelta(days=1)
    # Walk back over weekends and holidays
    while d.weekday() >= 5 or d.isoformat() in holidays:
        d -= timedelta(days=1)
    return datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=timezone.utc)

now = datetime.now(timezone.utc)
window_start = previous_business_day_start(now)
```

HubSpot search:
```
search_crm_objects({
  objectType: "calls",
  filterGroups: [{filters: [
    {propertyName: "hubspot_owner_id", operator: "EQ", value: "196669355"},
    {propertyName: "hs_timestamp", operator: "GTE", value: window_start.isoformat()},
    {propertyName: "hs_timestamp", operator: "LT", value: now.isoformat()}
  ]}],
  properties: ["hs_call_title", "hs_call_summary", "hs_call_has_transcript",
               "hs_call_recording_url", "hs_call_disposition", "hs_timestamp",
               "hs_call_duration"]
})
```

**Why business days:** weekend runs are skipped by cron (`* * 1-5`), so a Monday run is the first pass after Friday's calls. If we used a strict 24-hour window on Monday, we would only look at Sunday (always empty) and miss every Friday afternoon meeting. Calls already processed on Friday are deduped by HubSpot task search in Step 5 (existing tasks with `===` markers get an "Auto draft alternative" footer instead of a fresh draft), so reprocessing Friday on Monday is safe.

### Step 1.5, Verify the call is a Teams meeting (HARD GATE)

**This is a hard gate. If the call fails any of these checks, skip it. Do not draft. Do not create or update tasks. Do not append to call body. Log the skip reason and move to the next call.**

A call qualifies as a Teams meeting only if **all** of the following are true:

1. `hs_call_summary` exists AND contains the structured Conversations Intelligence HTML markers: `<h5>Summary</h5>`, `<h5>Key notes</h5>`, AND `<h5>Topics discussed</h5>`. Voicemails get a flat plain-text summary like `"Voicemail to [name]. [One sentence.]"` with no `<h5>` headers. Real Teams meetings get the structured CI block.
2. The summary text does NOT begin with (case-insensitive) `"Voicemail"`, `"Left voicemail"`, `"Left a voicemail"`, `"No answer"`, or `"No conversation"`.
3. `hs_call_duration` is greater than 60000 (60 seconds in milliseconds). Voicemails and dial attempts are typically 0 or under 60s. Real meetings are minutes long. This is a backup check; the structured-summary check above is the primary signal.

```python
def is_teams_meeting(call_props: dict) -> tuple[bool, str]:
    summary = (call_props.get("hs_call_summary") or "").strip()
    if not summary:
        return False, "no AI summary yet"
    # Plain-text voicemail summaries
    lower = summary.lower().lstrip("<p>").lstrip()
    voicemail_prefixes = ("voicemail", "left voicemail", "left a voicemail", "no answer", "no conversation")
    if lower.startswith(voicemail_prefixes):
        return False, f"voicemail summary (starts with {lower[:30]!r})"
    # Structured CI markers, primary signal
    required_markers = ("<h5>Summary</h5>", "<h5>Key notes</h5>", "<h5>Topics discussed</h5>")
    if not all(m in summary for m in required_markers):
        return False, "no structured CI summary (missing <h5> markers, likely a voicemail or short dial)"
    # Duration backup
    try:
        duration_ms = int(call_props.get("hs_call_duration") or "0")
    except (ValueError, TypeError):
        duration_ms = 0
    if duration_ms < 60000:
        return False, f"duration {duration_ms}ms < 60s threshold (likely voicemail or aborted call)"
    return True, "qualifies as Teams meeting"
```

**Why this rule exists:** on 2026-04-28 the runner created email follow-up tasks for three voicemails (John Lachance / Lingo, Joe Kennedy / TNS, Kal Karran). Andy never asked for follow-up emails on voicemails, the next channel after a voicemail is another call, not an email. The skill spec did not have an explicit Teams-only filter; it drafted on every call with any AI summary. The three bad tasks were closed manually on 2026-04-29 and this hard gate was added the same day. If a future Claude session ever proposes loosening this, point it at this section first.

### Step 2, For each call, find associated contacts

Use `search_crm_objects({objectType: "contacts", filterGroups: [{associatedWith: [{objectType: "calls", operator: "EQUAL", objectIdValues: [callId]}]}]})` to get attendees. Filter out OSI domain emails (`@osiglobal.com`), primary contact is the non-OSI one. If multiple non-OSI contacts on a call, use the one whose company matches the meeting title best, then fall back to the first.

### Step 3, Find recap email in Outlook

Search Outlook for sender `noreply@notifications.hubspot.com` with subject `Next steps ready: <call_title>`. The call title and email subject should match exactly.

```
outlook_email_search({
  sender: "noreply@notifications.hubspot.com",
  query: "Next steps ready: " + call_title,
  afterDateTime: window_start.isoformat(),
  limit: 5
})
```

Then `read_resource` with the email URI to get the full body. Parse the action items list from the HTML, they are inside the `<b>Action items:</b> <ul><li>...</li></ul>` block.

### Step 4, Draft the email

Read **`C:\Claude-Brain\playbook\voice-rules.md`** before drafting any email. Apply hard rules: no em-dashes, no hyphens, no "Andy" sign-off, no banned vocab.

Format:
```
[First name],

Thanks for the time on [day, e.g., "Friday"]. [One sentence summarizing what is on OSI's side based on the action items.] [One sentence on what is on their side.]

[Closing line, "Easy to keep moving the moment X lands" or "Happy to add anything else that surfaced".]
```

Keep total length 3-5 sentences. No bullet points (voice rules say break three-item lists into prose).

### Step 5, Find or create the email task

Search for existing task on the contact:
```
search_crm_objects({
  objectType: "tasks",
  filterGroups: [{
    filters: [
      {propertyName: "hs_task_status", operator: "EQ", value: "NOT_STARTED"},
      {propertyName: "hs_task_type", operator: "EQ", value: "EMAIL"}
    ],
    associatedWith: [{objectType: "contacts", operator: "EQUAL", objectIdValues: [contactId]}]
  }],
  properties: ["hs_task_subject", "hs_task_body", "hs_timestamp"]
})
```

**If a task exists** with empty/generic body (no `===` markers, less than 200 chars):
- Update `hs_task_body` to the draft + footer with source attribution.

**If a task exists with substantial body** (Andy has already worked on it):
- Append `<p>---<br>Auto draft alternative (run YYYY-MM-DD):</p><p>[draft]</p>` to the existing body. Don't overwrite.

**If no task exists:**
- Create a new EMAIL task on the contact, due today at 12 PM ET (16:00 UTC during EDT, 17:00 UTC during EST), priority MEDIUM, owner Andy.

Footer template appended to every draft:
```
---
Source: HubSpot AI summary + recap from <date> <meeting title> call (call ID <id>).
Action items captured: <bullet list>
```

### Step 6, Update meeting body for timeline visibility

Append AI notes to the meeting record's `hs_internal_meeting_notes`:

```
=== AI MEETING NOTES (HubSpot Conversations Intelligence, <date>) ===

Summary: <summary text>

Key notes:
- ...

Action items:
- ...

Topics discussed: <list>

Outcome: <disposition>. Follow up email task on <contact name>, due <date> (task ID <id>).

Recording + transcript: HubSpot call record <id> (Review Next Steps tab).
```

### Step 7, Save markdown copy

`C:\Claude-Brain\meetings\YYYY-MM-DD-<company-slug>.md` with full notes (see `2026-04-24-fatbeam.md` as the template).

### Step 8, Append summary line to log

`C:\Claude-Brain\meeting-followup-log.md`:

```
## 2026-04-26 10:09 AM ET run
- Fatbeam (Gavin Budd), task 108441848957 updated, draft saved
- Hurricane Electric (Alex Broque), task 108369456792 updated, draft saved
- AppGate (Antonio Villa, collective), task 108696977752 created with draft
```

---

## 🛡️ SAFETY RULES

- **Never overwrite a non-empty task body without a fallback.** If Andy has typed his own draft into a task, append the auto draft as an alternative, don't replace.
- **Never mention "Andy" in the email sign-off.** Outlook signature handles it.
- **No em-dashes anywhere.** Mechanical scrub before write.
- **No word-internal hyphens.** Use the same replacement table as `osi-outreach-sequence` (pre-owned → pre owned, multi-vendor → multi vendor, third-party → third party, Gartner-recognized → Gartner recognized, etc.).
- **No banned vocab:** crucial, pivotal, landscape, underscore, delve, showcase, testament, enhance, foster, garner.
- **3-5 sentences max.** Tight prose, no fluff.

---

## 🧪 MANUAL INVOCATION

When Andy types "draft my meeting follow-ups" or "run meeting followup":
1. Run the same logic, but expand the lookback window to include any call from the last 7 days (not just yesterday).
2. Show Andy a one-line summary per call before writing tasks ("Found X calls. Draft and save? (y/n)").
3. On confirmation, execute and report.

This lets Andy catch up after travel or weekends.

---

## 📓 STATE / LOGGING

State file: `C:\Claude-Brain\meeting-followup-state.json`
```json
{
  "last_run": "2026-04-26T14:09:00Z",
  "calls_processed": ["108618951070", "108630952269", "108640001290"],
  "tasks_created": [{"task_id": "108696977752", "contact": "Antonio Villa", "company": "AppGate"}]
}
```

State file is informational. Recurring runner does NOT use it for dedup, instead it uses HubSpot task search to detect existing tasks. State is just a diagnostic trail.

---

## 🔄 PERMISSIONS / TOOL USE

- HubSpot: `search_crm_objects` (calls, contacts, tasks), `manage_crm_objects` (tasks create/update, meetings update). Andy approves on first fire of the recurring task.
- Outlook: `outlook_email_search`, `read_resource` (mail URIs). Read-only. Approved on first fire.
- File writes: bash + Python for markdown files and state file. Already approved.

No external network access needed beyond these tools. No web searches in this skill.

---

## 🔁 INTEROP

- **Coexists with the HubSpot Workflow safety net.** The workflow auto-creates an EMAIL task on every meeting with outcome=Completed (placeholder body "Send follow-up. AI draft is on the meeting record's Review tab."). This skill then enriches that task body with the actual drafted email when it runs at 10 AM. If Cowork is asleep or this runner fails, the workflow's task at least exists so Andy isn't blind.
- **Does NOT touch outreach sequences.** The 6-email outreach queue (`osi-outreach-sequence`) is for cold prospects. This skill is for post-meeting follow-up only.
- **Does NOT run during overnight outreach.** Different lane, different cadence.

---

## ⚠️ KNOWN LIMITATIONS

- The AI-drafted follow-up email body that HubSpot itself produces is NOT exposed via the standard CRM API. We use `hs_call_summary` (which IS exposed) plus the recap email in Outlook to compose our own draft. This is by design, Andy's voice rules wouldn't match HubSpot's generic AI draft anyway.
- The full transcript text is not exposed via the CRM API (`hs_call_has_transcript` flag is, transcript body is not). If you need the transcript, click the call record's Review tab in HubSpot, the link is in the markdown copy.
- Action item parsing depends on HubSpot's recap email format. If HubSpot changes the email template, the parser may need an update. Detected by: log entries showing "0 action items captured" on calls that should have them.

---

## 🛠️ MAINTENANCE

If Andy's voice rules change (new banned vocab, new sign-off rule), update both this skill AND `osi-outreach-sequence` AND `voice-rules.md` together. They share the rules.

If Andy's HubSpot owner ID ever changes (re-org, new instance), update the constant in this skill.
