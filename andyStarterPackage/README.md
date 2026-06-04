# OSI Prospecting System v5

Interactive LinkedIn prospecting and outreach for OSI Global, run by chatting with Claude (Cowork). Built by Andy McLean. Drops into a teammate's setup in under 30 minutes.

Start with `SETUP.md`. This README is the overview.

## What it does

1. **Discovery + qualification.** Say "find me prospects at [Company]" and Claude runs four source discovery (HubSpot, ZoomInfo, LinkedIn browse, LinkedIn keywords), reads each profile in full, verifies the person still works there, qualifies against OSI's ICP, and writes a HubSpot strategy note plus a LinkedIn connection task.
2. **Sequencing.** For every qualified Yes with an email, Claude drafts a 6 email cadence and writes all 12 values into the contact's HubSpot AI fields.
3. **You enroll, HubSpot sends.** The LinkedIn task on Day 1 is your cue. You enroll the contact in a HubSpot sequence that pulls the AI fields as tokens. HubSpot sends from the cloud. No laptop sender, no Chrome send, no scheduled tasks.

## How it flows

```
You: "find me prospects at Acme"
   |
   v
osi-prospect-qualification   verify employer, qualify, strategy note + LinkedIn task
   |
   v (Yes with email)
osi-outreach-sequence        draft 6 emails, write to contact's HubSpot AI fields
   |
   v
LinkedIn task due (Day 1)    your cue
   |
   v
You enroll in your HubSpot sequence   HubSpot sends emails 1 to 6 from the cloud
```

The run output stays tight: a discovery log, one line per candidate, and an end-of-run recap listing everyone sequenced with their sequence type, enroll date, LinkedIn URL, and a clickable HubSpot contact link. Emails are written to HubSpot, never dumped into the chat.

## Skills in this package

Core:

| Skill | What it does | Trigger |
|---|---|---|
| `osi-prospect-qualification` | Core qualifier. Profile / Company / Auto / Task modes. Full LinkedIn read, ZoomInfo enrichment, HubSpot writes, handoff to sequencing. | "find me prospects at [Company]", paste a LinkedIn URL, "run discovery", "process my enroll tasks" |
| `osi-outreach-sequence` | Drafts the 6 email cadence for one Yes and writes the HubSpot AI fields. | Called automatically by qualification on a Yes |
| `osi-3email-new` | Shorter 3 email cadence for directors or lighter touches. | "3 email sequence for [name]" |
| `osi-3email-reengagement` | 3 email second touch for prospects who already ran a sequence. | "re-engage [name]" |
| `osi-old-customer-reengagement` | 5 email revival for dormant past customers. | "re-engage old customer" |
| `osi-cold-reengagement` | Finds cold first degree LinkedIn connections, makes InMail tasks. | "find cold connections" |
| `osi-job-change-prospecting` | Weekly Sales Nav scan for job changes and new connections. | "run job change search" |
| `osi-email-task-drafts` | Drafts replies for HubSpot email tasks due today. | "run email tasks" |

Legacy (in `skills/legacy/`, only if you are draining an old email queue): `osi-email-sender`, `osi-monitor`, `osi-email2-rewriter`. A new user does not need these. See SETUP Section 9.

## What is in this package

```
osi-prospecting-system-v5/
  README.md                 you are here
  SETUP.md                  step by step install (start here)
  FEEDBACK.md               fill in after setup and send back (SETUP Section 12)
  CLAUDE.md.template         rename to CLAUDE.md, fill in the identity placeholders
  skills/                   core skills (+ legacy/ subfolder)
  playbook/                 drafting rules, product lines, verticals, pain and objections, openers, voice, data quality
  knowledge/                email pattern resolver + the OSI master sales playbook
  scripts/                  validate_email.py (hard stop validator)
  config/                   blank queue + stagger, example block lists, holidays, blank 7 tab tracker
```

## Prerequisites

- Cowork (Claude desktop app)
- HubSpot MCP connector
- ZoomInfo MCP connector (recommended)
- Claude in Chrome extension (for reading LinkedIn during discovery, not for sending)
- Python 3 with openpyxl (`pip install openpyxl --break-system-packages`)
- A working folder at `C:\Claude-Brain\`

## What changed from v4

- Sending moved to HubSpot AI fields and cloud sequences. The Outlook sender, Chrome send dependency, and the three scheduled tasks are out of the core setup (legacy only).
- New HubSpot setup step: create the 12 AI custom properties and a 6 step token based sequence (SETUP Step 3).
- New playbook file `pain-and-objections.md` (pain points, discovery questions, objection handlers, secondary source positioning).
- Vertical logic is role first, not industry first. Optics for engineers, TPM for procurement and contract owners, in any vertical. Added a Software/SaaS vertical.
- Park Place / Service Express wedge consolidated and expanded in `vertical-intel.md`.
- Enroll Task Mode in the qualifier: tag a contact, say "process my enroll tasks."
- Minimal chat output: in Company and Auto Mode, emails and strategy notes are written to HubSpot, never printed in the conversation.
- Run output includes LinkedIn and clickable HubSpot contact URLs next to each sequenced name, plus an end-of-run recap.
- Em-dash ban hardened across the playbook, the skills, and the validator.
- Feedback loop added: `FEEDBACK.md` plus SETUP Section 12.

## Identity placeholders

Personal identity is genericized in the skills and playbook. After copying the files, replace these everywhere (one find and replace each), per SETUP Steps 3 to 4:
- `<<YOUR_NAME>>` your first name (this is your email sign-off too)
- `<<YOUR_EMAIL>>` your work email
- `<<YOUR_HUBSPOT_OWNER_ID>>` your 9 digit HubSpot owner id (critical: until you set this, prospecting would assign contacts to the wrong owner)
- `<<YOUR_HUBSPOT_PORTAL_ID>>` your HubSpot account / portal id (the number in any HubSpot record URL). Builds the clickable contact links in the output.
- `<<YOUR_GITHUB_USERNAME>>` your GitHub username

Questions: Andy McLean, OSI Global.
