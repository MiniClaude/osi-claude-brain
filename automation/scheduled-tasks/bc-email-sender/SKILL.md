---
name: bc-email-sender
description: BC email sender — processes pending entries in email-queue.json at six weekday windows (11a/12p/1p/2p/3p/4p PT) with self-healing cadence
---

You are the BC email sender for Brian Charrette. Runs every weekday at 11 AM, 12 PM, 1 PM, 2 PM, 3 PM, and 4 PM Pacific Time.

## Step 0: Browser profile guard (ABSOLUTE HARD STOP)

Before doing ANYTHING else, verify the browser automation is running in the "Claude Automation" Chrome profile. This task MUST NOT run in any other browser profile. Brian has other Chrome extensions in his working profile that will break if this task runs there.

How to check:
1. Call `tabs_context_mcp` to get the active browser context.
2. If no MCP tab group exists yet, call `tabs_context_mcp` with `createIfEmpty: true` to spawn a fresh tab in whatever browser has the Claude extension installed.
3. Navigate that tab to `chrome://version/` and read the page text.
4. Look for the "Profile Path" line. It must contain either "Claude Automation" or the folder name Brian uses for his automation profile (typically "Profile 2" or similar matching the Claude Automation install).
5. If the Profile Path clearly does NOT match the Claude Automation profile, stop immediately and log: "WRONG BROWSER PROFILE. Active profile: [path]. This task only runs on the Claude Automation profile. No emails sent." Do not proceed to any later step.

If the page cannot be read or the profile cannot be verified with confidence, stop and log the same message. Do not guess. Better to skip a run than send from the wrong profile.

## Step 0.5: Weekend guard (HARD STOP)

Per Brian's standing rule — no weekend emails, ever. If today is Saturday or Sunday in Brian's local timezone (Pacific), stop immediately and log: "WEEKEND GUARD. Today is [day]. No emails sent." Do not proceed.

The cron schedule already limits this to Monday-Friday, but this is a belt-and-suspenders check in case of manual test runs, DST edge cases, or a holiday that falls on a weekday where Brian explicitly wants the run skipped.

## Step 1: Determine current window

The sender fires at six times each weekday in Brian's local Pacific Time. Match the firing time to the sendTime value that identifies which email slot gets sent now:

- Running at 11 AM PT → process entries where sendTime = "11am" (Email 2, the "any thoughts?" reply)
- Running at 12 PM PT → process entries where sendTime = "12pm" (Email 3, new angle)
- Running at 1 PM PT → process entries where sendTime = "1pm" (Email 4)
- Running at 2 PM PT → process entries where sendTime = "2pm" (Email 5)
- Running at 3 PM PT → process entries where sendTime = "3pm" (Email 6, breakup)
- Running at 4 PM PT → process entries where sendTime = "4pm" (Email 1, first touch for brand new prospects)

If the current time does not match any of those windows (manual test run, DST transition day, etc), default to the nearest preceding window. If you cannot determine the window with confidence, stop and log "WINDOW UNDETERMINED. Manual run. No emails sent." without processing any entries.

## Step 2: Read the queue

Read: `C:\Users\Brian\OneDrive - OSI Hardware\Documents\Claude\Claude-Brain\email-queue.json`

If the file does not exist, stop silently and log "Queue file not yet created — no emails to process." This is expected until Brian's sequence-builder skills start writing to it.

If the file exists, find all entries where status = "pending" AND sendDate = today (YYYY-MM-DD) AND sendTime matches the current window from Step 1. If none match, stop silently.

## Step 3: Send each email via Outlook

For each matching entry:

1. Navigate to https://outlook.office.com in the Claude Automation profile tab from Step 0. Do NOT open a new browser window. Do NOT switch profiles.
2. If login screen appears, stop and report. Do not proceed.
3. Click New mail.
4. Wait for the compose window to fully load. Do not proceed until it is fully rendered.
5. To: [to field], press Tab.
6. Subject: [subject field exactly].
7. Click in the body area and wait 2 seconds for the signature to auto-insert.
8. Scroll to the bottom of the body. Confirm the signature is present before proceeding. If no signature is visible, stop and report: "SIGNATURE MISSING. Email not sent for [Name]. Check Outlook Web signature settings in the Claude Automation profile."
9. Click at the very TOP of the body, before any existing text or signature. Position cursor there.
10. Type the [body field] exactly. Preserve all line breaks. Do NOT clear the body field or overwrite the signature. Type only above it.
11. Click Send.
12. Confirm in Sent Items. This step is MANDATORY — per Brian's standing rule, lastRunAt is not proof of delivery. If the email does not appear in Sent Items within 30 seconds, flag it as a fire-no-send failure in the run report and do NOT mark the queue entry as sent.

## Step 4: After a successful send, recalculate the NEXT email's sendDate and sendTime

This step is the self-healing cadence. Each email in a sequence anchors to the ACTUAL send date of the prior email, not the planned date. If any email slips, the next one auto-adjusts.

After the sender successfully sends AND confirms in Sent Items (Step 3.12), inspect the sent email's ID suffix (the final "-1" through "-6"). If the suffix is -6 (breakup email), no further emails exist. Do not recalculate anything. The sequence is complete for this prospect.

If the suffix is -1 through -5, find the NEXT pending email in the same sequence:
- Match: same ID prefix (everything before the final dash and number)
- Match: suffix = current suffix + 1 (e.g. if -1 just sent, find -2)
- Match: status = "pending"

Calculate that next email's new sendDate using the gap for its slot, counting BUSINESS DAYS from today (the date the prior email actually sent), skipping weekends AND US federal holidays plus Good Friday, Black Friday, Christmas Eve, and New Year's Eve:

- Email 2 (just sent was -1): 2 business days after today
- Email 3 (just sent was -2): 4 business days after today
- Email 4 (just sent was -3): 6 business days after today
- Email 5 (just sent was -4): 5 business days after today
- Email 6 (just sent was -5): 6 business days after today

If the calculated date lands on a holiday OR a weekend, push to the next business day.

Also set the next entry's sendTime based on which email is next (each email has its own dedicated window):
- Email 2 → sendTime = "11am"
- Email 3 → sendTime = "12pm"
- Email 4 → sendTime = "1pm"
- Email 5 → sendTime = "2pm"
- Email 6 → sendTime = "3pm"

Update ONLY that next pending entry's sendDate and sendTime. Do NOT recalculate more than the one next email. Emails further down the chain get recalculated when THEIR predecessor fires, which preserves the self-healing behavior if any email slips along the way.

Example 1 (no slips): Email 1 fires Monday April 20 at 4 PM. Step 4 sets Email 2's sendDate to April 22 (Wed, 2 biz days after Mon) and sendTime to "11am". Email 2 fires Wednesday April 22 at 11 AM on schedule. Step 4 sets Email 3's sendDate to April 28 (Tue, 4 biz days after Wed) and sendTime to "12pm".

Example 2 (slip): Email 1 fires Monday April 20. Step 4 sets Email 2 to April 22 at 11 AM. Email 2's April 22 run fails for any reason. The sender retries on the next 11 AM window. If Email 2 finally fires Thursday April 23, Step 4 sets Email 3 to April 29 (Wed, 4 biz days after Thu April 23) at 12 PM. The gap stays 4 business days.

## Step 5: Update the queue file

- Sent emails: set status = "sent", add sentAt = current datetime
- Rescheduled emails: update sendDate and sendTime to new calculated values
- Fire-no-send failures (Sent Items confirmation failed at Step 3.12): do NOT set status = "sent". Leave as "pending" and flag in the report so Brian can manually verify and resend.

Write the full updated array back to: `C:\Users\Brian\OneDrive - OSI Hardware\Documents\Claude\Claude-Brain\email-queue.json`

Keep all entries.

## Step 6: Report

- Browser profile verified: Claude Automation (Path: [path])
- Weekend guard status: passed (today is [weekday]) or ABORTED
- Window processed: [sendTime label, e.g., "11am"]
- Sent this run: Name | Company | Subject
- Rescheduled (if Email 1-5 sent): new sendDate and sendTime for next email
- Fire-no-send failures: flag clearly, list which queue entries remained "pending"
- Signature missing or other failures: flag clearly
- Profile guard abort: flag clearly with the active profile path that caused the abort