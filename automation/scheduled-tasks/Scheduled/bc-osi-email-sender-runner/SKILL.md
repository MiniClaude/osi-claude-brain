---
name: bc-osi-email-sender-runner
description: Recurring sender — runs bc-osi-email-sender at 11am, 12pm, 1pm, 2pm, 3pm, 4pm ET weekdays to process due email-queue.json entries.
---

run bc-osi-email-sender

Process the queue at C:\Claude-Brain\email-queue.json for the current ET window (11am, 12pm, 1pm, 2pm, 3pm, or 4pm). Send all due emails via Outlook in Chrome with the Pre-Send Gate, em-dash sanitizer, bi-directional signature trim, and hard-block enforcement per the skill's SKILL.md. Log the run to C:\Claude-Brain\sessions\session-YYYY-MM-DD.md.

If skill is not registered or queue file is unreachable, ABORT and notify Brian — do NOT fall back to any older sender.