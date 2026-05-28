---
name: osi-weekly-reengagement
description: Weekly Wednesday re-engagement — searches HubSpot ICP contacts and creates follow-up tasks for Brian
---

Run the osi-weekly-reengagement skill.

This is a standalone weekly automation that runs independently of any other re-engagement tasks.

TRACKER FILE (read and write ONLY this file — never touch any other tracker):
C:\Users\Mini\Documents\Documents\Claude\skills\osi-weekly-reengagement\weekly-reengagement-tracker.json

SKILL FILE (full instructions):
C:\Users\Mini\Documents\Documents\Claude\skills\osi-weekly-reengagement\SKILL.md

Follow the skill instructions exactly:
1. Read the tracker file to get current state (last keyword, last page, processed IDs)
2. Search HubSpot contacts using the current keyword and page
3. For each qualifying contact (not already processed, not recently touched, ICP-relevant title), create a HubSpot follow-up task assigned to Brian Charrette, due in 2 business days
4. Cap at 10 tasks per run
5. Update the tracker file with the new state before exiting
6. Print a run summary

Do NOT read or write any other tracker file. Do NOT modify the weekend automation's files in any way.