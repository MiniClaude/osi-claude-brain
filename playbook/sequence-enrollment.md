# Sequence Enrollment and Connection-Request Routing

Identity: Brian Charrette. HubSpot Owner ID 213536174. Portal ID 21878985.

This file is the routing reference for aaa-pq-6-9-26 and osi-outreach-sequence. It restates the matrix those skills follow. If the skill body and this file ever disagree, the skill body wins.

## Route by email + phone

"Has phone" means a real direct dial or cell number. The company switchboard or any (HQ) line never counts as a phone.

| Verdict | Email | Phone | Action |
|---|---|---|---|
| Yes | Yes | any | HANDOFF to osi-outreach-sequence. It drafts the 6 emails, writes the AI fields, and enrolls the contact in the matched `Brian - AI` sequence. The connection request is step 1 INSIDE the sequence. No standalone connection task. |
| Yes | No | Yes | Do NOT hand off. Enroll in the matched `Sniper CALLS` sequence AND create the standalone connection task. |
| Yes | No | No | Do NOT hand off. Create the standalone connection task PLUS 2 LinkedIn InMail tasks. |

## Sequence matching by SEQUENCE label

The SEQUENCE line in the strategy note picks the family:
- Network -> `Brian - AI Network` (email path) or `Sniper CALLS Network` (calls path)
- DWDM -> `Brian - AI DWDM` or `Sniper CALLS DWDM`
- Server/Storage -> `Brian - AI Server/Storage` or `Sniper CALLS Server/Storage`
- TPM -> `Brian - AI TPM` or `Sniper CALLS TPM`

## Standalone connection task (calls-only and no-email-no-phone paths only)

Housekeeping: if an existing NOT_STARTED `LINKED_IN_CONNECT` task exists, mark it COMPLETED first.
- Subject: `Sales Nav -- Send connection request -- [First Last] | [Company]`
- Type: `LINKED_IN_CONNECT` (never `LINKED_IN_MESSAGE`, never `TODO`)
- Due: next business day at 4 PM ET (no stagger)
- Notes: the CONNECTION INVITE text from the strategy note, raw message only
- Owner: 213536174

Email paths get NO standalone connection task. The connection request is step 1 inside the `Brian - AI` sequence, and osi-outreach-sequence types the CONNECTION INVITE into that step-1 task note at enrollment.

## 2 LinkedIn InMail tasks (no-email-no-phone path)

Duplicate check: if a NOT_STARTED or IN_PROGRESS `LINKED_IN_MESSAGE` task exists, skip both.
- Task 1: `LINKED_IN_MESSAGE`, subject `1st LI -- [First Last] | [Company]`, due 7 days. Note: 1st LI message, 3 sentences max.
- Task 2: `LINKED_IN_MESSAGE`, subject `2nd LI -- [First Last] | [Company]`, due 21 days. Note: 2nd LI message, 1 to 2 sentences.

## Chrome enroll procedure (Sniper CALLS, and email paths via osi-outreach-sequence)

1. Open the contact record in HubSpot (portal 21878985).
2. Click More, then Enroll in sequence.
3. Pick the matched sequence from the table above.
4. Set the start date (email paths use the stagger Day 1 computed by osi-outreach-sequence; calls paths use the default start, no stagger).
5. Click Start sequence.
6. Verify the "Successfully enrolled" banner. No banner means the enroll did not take: log `enroll-failed`, flag the person, do not mark done.

## Verification (Step 3.5, mandatory)

- Standalone connection task: fetch it back by `hs_object_id`. Confirm it exists, `hs_task_type` is `LINKED_IN_CONNECT`, associated to the contact. Fail means ABORT, flip to `pending-relookup`, log.
- Sequence enrollment: the "Successfully enrolled" banner is the verification. No banner means log `enroll-failed` and flag.

Every write uses `confirmationStatus: "CONFIRMATION_WAIVED_FOR_SESSION"`. No mid-run approval prompts.
