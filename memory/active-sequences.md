# Active Outreach Sequences

**Last updated:** 2026-06-11
**Source:** automation/email-queue.json
**Total queue entries:** 245 (85 sent, 139 skipped-dedup, 17 pending, 4 needs_review)

## Pending Sends (17)

| Contact | Company | Emails left | Next send |
|---------|---------|-------------|-----------|
| hsimpson@buckner.org | Buckner | 5 (emails 3-7) | 2026-06-12 |
| daniel.bloor@thalesgroup.com | Thales Group | 1 (email 3) | 2026-06-15 |
| johnp@sciremc.com | SCI REMC | 5 (emails 3-7) | 2026-06-17 |
| chadmaalis@nuvera.net | Nuvera | 3 (swag 1-3) | 2026-07-21 |
| dan.doughty@lambweston.com | Lamb Weston | 3 (swag 1-3) | 2026-07-21 |

## Needs Review (4, stalled since mid-May)

These email-5 entries have placeholder subjects (`__NEEDS_ORIGINAL_SUBJECT__`) and were never sent:
- vahan.sahagian@constellation.com (Constellation)
- zain.karmally@sscinc.com (SSC Inc)
- jake.rog@graphicpkg.com (Graphic Packaging)
- ksafah@gmail.com (CCM)

Action: fix subjects or cancel. They are reply-threaded "Any thoughts?" bumps.

## Notes
- Emails fire via osi-email-sender at 11am/12pm/1pm/2pm/3pm/4pm ET windows (weekdays only)
- Every send BCCs bc@osihardware.com + 21878985@bcc.hubspot.com
- Hard-block list managed at automation/hard-block.json
- 139 entries marked skipped-dedup are historical, no action needed
