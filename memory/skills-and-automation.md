# Skills and Automation Reference

**Last updated:** 2026-05-19

## Brain Folder Structure
```
C:\Users\Mini\Documents\osi-claude-brain\
  automation/
    email-queue.json        <- live outreach queue (212 emails as of 2026-05-19)
    hard-block.json         <- blocked addresses / domains (currently empty)
    scheduled-tasks/        <- per-contact and system scheduled task configs
  memory/                   <- THIS folder — persistent cross-session memory
  projects/
    company-enrichment-prospecting/
    connecting-two-computers/
  scripts/                  <- push.bat / pull.bat for GitHub sync
  sessions/                 <- session logs
  skills/                   <- full skill library (see below)
  docs/
  scheduled-tasks/
```

## Bash Mount Path
When using bash tools: `/sessions/<session-id>/mnt/osi-claude-brain/`

## Email Automation
- **Queue file:** `automation/email-queue.json`
- **Sender:** `osi-email-sender` scheduled task — runs 11am/12pm/1pm/2pm/3pm/4pm ET weekdays
- **BCC on every send:** bc@osihardware.com + 21878985@bcc.hubspot.com
- **Hard block:** `automation/hard-block.json`

## Installed Skills (40+)

### Outreach / Sequences
- `abc-7step-master` — MASTER 7-email sequence, full package (HubSpot contact, Orum call script, LinkedIn task, emails queued). Use this for new prospect work.
- `osi-outreach-7email` — 7-email hyper-personalized sequence (manual review flow)
- `bc-7step-w-tracking` — 7-email tracked sequence with BCC (legacy, replaced by abc-7step-master)
- `bc-7email-custom` — 7-email custom cold outreach
- `bc-osi-outreach-sequence-v2` — 6-email automated sequence
- `osi-outreach-sequence` — Standard 7-email sequence
- `aaa-outreach-personalized` — Personalized 7-email with research
- `osi-3email-new` — 3-email new outreach (shorter cadence)
- `osi-3email-reengagement` — 3-email re-engagement (for prospects who went through 7 emails)
- `bc-custom-old-customer` — 7-email dormant customer re-engagement
- `bc-4email-warm-reconnect` — 4-email warm reconnect for known contacts

### Prospecting / Research
- `bc-osi-prospect-qualification-v2` — Qualify LinkedIn profiles against OSI ICP
- `bpc-prospect` — Prospect qualification (alternate)
- `bc-prospect-qualification` — Prospect qualification (original)
- `bc-salesnav-greenfield` — Cross-reference Sales Nav URL vs HubSpot CRM
- `bc-greenfield-nocigs` — Greenfield search with CRM bucketing
- `bc-greenfield-screening` — Screen company lists for greenfield OSI fit
- `bc-account-enrichment` — Deep single-account enrichment (ZoomInfo + LinkedIn + HubSpot)
- `account-enrichment` — Multi-account enrichment (5 dormant accounts)
- `osi-job-change-prospecting` — Weekly LinkedIn job change tracker
- `bc-linkedin-1st-connections-messaging` — Find and message un-contacted LinkedIn 1st connections
- `osi-discovery-sweep` — Per-company overnight prospect discovery

### HubSpot / CRM
- `account-monitor` — Refresh OSI_Account_Monitor.xlsx (full pipeline view)
- `bc-monthly-account-count` — Track HubSpot account ownership over time

### Daily Operations
- `bc-task-alarm` — Daily task alarm: HubSpot tasks + stuck emails + Cowork tasks
- `osi-sequence-monitor` — Monitor active sequence health and HubSpot replies
- `morning-briefing` — Calendar + email + news daily briefing
- `daily-briefing` — Sales briefing for any rep
- `linkedin-response` — Draft LinkedIn messages for new/dormant connections

### Utilities
- `session-compress` — TL;DR summary of current Cowork session
- `consolidate-memory` — Reflective pass over memory files (merge, prune, fix stale)
- `humanizer` — Remove AI writing patterns from text
- `email-meeting-optimizer` — Score and rewrite cold emails for reply rate
- `meeting-notes` — Turn transcripts into action-item summaries
- `obsidian-vault` — Connect to osi-brian Obsidian vault via Local REST API
- `research-assistant` — Deep-dive research + saved document
- `schedule` — Create/update Cowork scheduled tasks
- `skill-creator` — Create, edit, and optimize skills

### Document Tools
- `docx` — Word document creation / editing
- `xlsx` — Excel spreadsheet creation / editing
- `pptx` — PowerPoint deck creation / editing
- `pdf` — PDF manipulation
- `notebooklm` — Google NotebookLM full API access

## Scheduled Tasks Running
- `osi-email-sender` — Daily email queue sweep (ET windows)
- `bc-email-sender` — A/B sender variant
- `bc-linkedin-1st-connections` — LinkedIn connection messaging
- `daily-sequence-monitor` — Sequence health check
- `linkedin-job-change-weekly-report` — Weekly job change prospecting (Mondays)
- `hubspot-daily-accounts` / `hubspot-account-overview-refresh` — Account reports
- `osi-weekly-reengagement` — Weekly re-engagement sweep
- `research-scout-night-1/2/3` + `research-scout-weekly-review` — Overnight research
- `obsidian-vault-reminder` / `obsidian-vault-sync` — Vault sync reminders
