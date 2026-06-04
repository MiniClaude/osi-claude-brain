---
name: bc-3email-swag-json
description: >-
  Draft and queue a 3-email SWAG offering (complimentary SmartOptics SFPs / address-confirm) for any OSI Global
  prospect and write all 3 emails to email-queue.json so the osi-email-sender / bc-osi-email-sender sweeps and
  sends them on schedule. Use this when a prospect is already in another sequence and cannot be enrolled again in
  HubSpot, or any time Brian wants a short swag-first touch through the JSON queue instead of HubSpot AI fields.
  No HubSpot sequence enrollment. No auto-send. Queue only. ALWAYS use when Brian says "swag 3 email",
  "3 email swag", "swag offer", "send swag to [name]", "queue the swag 3", "swag sequence in json",
  "3 email swag offering", "bc-3swag", or pastes a contact and asks for a short swag offering through the queue.
---

# bc-3email-swag-json - 3-Email Swag Offering to the JSON Queue

Short swag-first sequence that offers complimentary SmartOptics SFPs and confirms a shipping address.
All 3 emails are written to email-queue.json (the same queue the sender sweeps). Nothing auto-sends.
This is the JSON-queue alternative to a HubSpot sequence. Use it when a prospect is already enrolled
somewhere and cannot be enrolled again.

Owner of everything: Brian Charrette (hubspot_owner_id 213536174).

## Queue file - sole source
C:\Users\Mini\Documents\osi-claude-brain\email-queue.json

Do not read or write any other queue location. If the file cannot be reached, STOP and tell Brian the
queue is not accessible from this session (it lives on his machine); offer to set up a scheduled task that
writes it in his normal environment instead.

---

## Step 1 - Gather prospect info

Extract from what Brian pasted, or ask for: full name, title, company, and a valid business email.

STOP IF NO EMAIL. The queue sends email, so an address is required. If neither Brian's input nor a quick
ZoomInfo lookup returns a valid corporate email, STOP and suggest a LinkedIn-only fallback instead.

Email rules:
- Use the corporate domain. Never use a personal domain (gmail, yahoo, hotmail, outlook.com, icloud, aol, proton, etc.).
- Watch for stale/legacy domains after a rebrand (e.g. an acquired company's dead domain). One web search to
  confirm the current corporate domain if unsure.

## Step 2 - Read the queue and dedup

1. READ C:\Users\Mini\Documents\osi-claude-brain\email-queue.json. Use an existing entry as the template -
   match its EXACT schema and field names. Do not invent fields.
2. DEDUP: if this prospect (match by email) already has pending entries with the swag subjects below, STOP and
   do not add duplicates. Report what is already queued and exit.

## Step 3 - Pick the start date and spacing

- Default start date: next business day, unless Brian gives one ("start Jul 14", "one week after the 7-step ends", etc.).
- Default spacing from the start date: Day 0 / +3 business days / +5 business days.
- Skip weekends and US holidays. Push any landing on a weekend/holiday to the next business day.
- Compute the three actual send dates before writing.

## Step 4 - Draft the 3 swag emails

Brian's voice: direct, short, no corporate fluff. No em dashes, no en dashes, no hyphens in prose. No AI
vocabulary ("crucial", "leverage", "landscape", "enhance", etc.). Body opens with the first name on its own
line followed by a comma, and ends with Brian on its own line. Lightly personalize the opener to the
prospect's role/vertical if there is an obvious hook; otherwise use the templates as-is.

Email 1 - subject: Confirming address
[First name],

We put together a small package of complimentary SmartOptics SFPs for a few [role/vertical] we'd like to get in front of. I'd like to send one your way, no strings.

Can you confirm the best shipping address at [Company], or a better one if you'd rather it go elsewhere?

Brian

Email 2 - subject: RE: Confirming address
[First name],

Circling back on the optics sample. Still happy to drop a few complimentary SFPs in the mail so you've got break glass spares on the shelf.

Just need an address to send them to. Where's best?

Brian

Email 3 - subject: RE: Confirming address
[First name],

Last one on the swag. If you send me an address I'll get the SFPs out this week. If it's easier to grab 10 minutes and talk through [relevant OSI angle: optics / DWDM / TPM] instead, happy to do that too.

Either way, just say the word.

Brian

Substitute every bracket with real content before writing. No bracket tokens may remain.

## Step 5 - Write the 3 entries to the queue

Append 3 entries to email-queue.json matching the existing schema, with:
- prospect name, company, email
- the subject and body for each of the 3 emails
- the computed send date for each (Day 0 / +3 bd / +5 bd)
- status = pending (use whatever the existing entries use for "not yet sent")
- owner = Brian (213536174)
- BCC on every send: bc@osihardware.com AND 21878985@bcc.hubspot.com

Save the file.

## Step 6 - Confirm. No auto-send.

Report to Brian: prospect name, the 3 send dates, the subjects, and the file path. State clearly that nothing
was sent. The osi-email-sender / bc-osi-email-sender sweeps the queue and sends on its own schedule.

Never invoke a sender. Never enroll the prospect in a HubSpot sequence. Queue only.

---

## Notes

- This skill is the swag-first short cousin of aaa-hs-7step-swag, but it writes to the JSON queue instead of
  HubSpot AI fields, and it is 3 emails instead of 7.
- If Brian wants this to also create a LINKED_IN_CONNECT task or an Orum call-script note on the HubSpot
  contact, he can say so and that can be layered on, but the default is queue only.
- Swag = complimentary SmartOptics SFPs (break-glass spares). The wedge is "confirm your address so I can mail
  them," which opens a reply thread without a hard pitch.
