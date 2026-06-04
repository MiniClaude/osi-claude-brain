# OSI Prospecting System v5, Plug and Play Setup

Hand this to a teammate with the matching file bundle and they are running in under 30 minutes. Built by Andy McLean (OSI Global). Questions: andy@osiglobal.com.

This is v5. The big change from v4: outreach now sends from **HubSpot sequences in the cloud**, not from a laptop running Outlook. That removes the Chrome extension, the Outlook sender, and the scheduled send tasks from your setup. It is simpler and it does not depend on your machine being on.

---

## 1. What you get

A prospecting to pipeline workflow you run by chatting with Claude (Cowork):

1. **Discovery + qualification.** Say "find me prospects at [Company]" and Claude runs four source discovery (HubSpot, ZoomInfo, LinkedIn browse, LinkedIn keywords), reads each profile in full, verifies the person still works there, qualifies against your ICP, and writes a HubSpot strategy note plus a LinkedIn connection task.
2. **Sequencing.** For every qualified Yes with an email, Claude drafts a 6 email cadence and writes all 12 values into the contact's HubSpot AI fields (subjects 1 to 6 and bodies 1 to 6).
3. **You enroll, HubSpot sends.** The LinkedIn task on Day 1 is your cue. When it comes due, you enroll the contact in a HubSpot sequence that pulls those AI fields as tokens. HubSpot sends from the cloud.
4. **Shorter cadences and re-engagement** for directors, second touches, and dormant accounts.

The old laptop based sender still exists for anyone winding down a legacy queue, but a new user does not need it. See Section 9.

---

## 2. The delivery model (read this first, it is the core idea)

```
You: "find me prospects at Acme"
   |
   v
osi-prospect-qualification   ->  verifies employer, qualifies, writes strategy note + LinkedIn task
   |
   v (Yes with email)
osi-outreach-sequence        ->  drafts 6 emails, writes them to the contact's HubSpot AI fields
   |
   v
LinkedIn task comes due (Day 1)  ->  YOUR cue
   |
   v
You enroll the contact in your HubSpot sequence  ->  HubSpot sends emails 1 to 6 from the cloud
```

No queue file to babysit. No Chrome. No scheduled sender. The only manual step is the enroll, and the LinkedIn task tells you exactly when.

---

## 3. Prerequisites

- Cowork (Claude desktop app) installed.
- HubSpot MCP connector configured with your account.
- ZoomInfo MCP connector (strongly recommended for contact enrichment).
- Claude in Chrome extension (used for reading LinkedIn profiles during discovery, not for sending).
- Python 3 with openpyxl (`pip install openpyxl --break-system-packages`) for the Excel tracker.
- A working folder at `C:\Claude-Brain\`.

---

## 4. Install, step by step

### Step 1: Create the folder and git repo
```
C:\Claude-Brain\
```
```bash
cd C:\Claude-Brain
git init
git remote add origin https://github.com/<<YOUR_GITHUB_USERNAME>>/Claude-Brain.git
```

### Step 2: Drop in the bundle
Copy the package contents into `C:\Claude-Brain\`:
- `skills/` to `C:\Claude-Brain\skills\`
- `playbook/` to `C:\Claude-Brain\playbook\`
- `knowledge/` to `C:\Claude-Brain\knowledge\`
- `scripts/` to `C:\Claude-Brain\scripts\`
- `config/*` to the matching files at the root (`holidays.json`, `hard-block.json`, `approved-vendors.json`, `do-not-auto-prospect.json`, `overnight-candidates.json`, `prospects-tracker-new.xlsx`)
- `CLAUDE.md.template` to `C:\Claude-Brain\CLAUDE.md` (rename, then fill in the placeholders)

Create the empty log file:
```bash
echo "" > C:\Claude-Brain\overnight-run-log.md
```

### Step 3: Set up HubSpot AI fields (this is the v5 step v4 did not have)
This is what makes cloud sending work. Do it once in HubSpot.

1. Create 12 custom contact properties (single line text is fine):
   - `ai_email_subject_1` ... `ai_email_subject_6`
   - `ai_email_body_1` ... `ai_email_body_6`
   Use these exact internal names. The outreach skill writes to them by name.
2. Build a HubSpot sequence with 6 steps. In each step, set the subject and body to the matching token, for example `{{contact.ai_email_subject_1}}` and `{{contact.ai_email_body_1}}` for step 1, and so on through step 6.
3. Set your own step delays in the sequence (the qualification skill staggers WHO you enroll and WHEN, HubSpot handles the per step cadence once enrolled).

Now when Claude writes the AI fields and you enroll the contact, HubSpot renders the stored emails and sends them.

### Step 4: Fill in the identity placeholders
Open `C:\Claude-Brain\CLAUDE.md` and replace every `<<...>>`. Then run the same find and replace across the `skills/` and `playbook/` folders, because these appear in the skill files too:
- `<<YOUR_NAME>>` (also your email sign-off), `<<YOUR_EMAIL>>`, `<<your_role>>`
- `<<YOUR_HUBSPOT_OWNER_ID>>` (HubSpot: avatar top right, Profile and Preferences, Owner ID). Critical: until this is set, prospecting would assign contacts to the wrong owner.
- `<<YOUR_HUBSPOT_PORTAL_ID>>` (your HubSpot account / portal id, the number in any HubSpot URL like `app.hubspot.com/contacts/<this number>/...`). Used to build the clickable contact links in the run output.
- `<<YOUR_GITHUB_USERNAME>>`

### Step 5: Fill in the three config lists
- `hard-block.json`: addresses that must never be emailed.
- `approved-vendors.json`: companies where you are already an approved vendor.
- `do-not-auto-prospect.json`: companies to keep out of Auto Mode (still prospectable by name).

### Step 6: Install the skills in Cowork
This package ships the two skills that ARE the system. Drag both `.skill` files in `C:\Claude-Brain\skills\` into a Cowork chat to install:
1. `osi-prospect-qualification.skill` (find, qualify, write the HubSpot strategy note + LinkedIn task)
2. `osi-outreach-sequence.skill` (draft the 6 emails, write them to the HubSpot AI fields)
Open a fresh session and confirm both appear in the skills list. That is everything you need to run the full find-to-emails loop.

Optional extras exist (shorter 3 email cadence, re-engagement, job-change scan) but are deliberately not in this package to keep it simple. Ask Andy for them once you are comfortable with the core two.

### Step 7: Verify Python + openpyxl
```bash
python3 -c "import openpyxl; print('ok')"
```
If it fails: `pip install openpyxl --break-system-packages`

### Step 8: Smoke test on one prospect
1. Open a Cowork chat.
2. Say: "find me prospects at [one company]."
3. Watch the chain: LinkedIn read, qualification, ZoomInfo enrichment, HubSpot strategy note + LinkedIn task, then the outreach skill writes the AI fields.
4. Expect this confirmation line: `AI fields written: [First Last] | [Sequence type] | Enroll by YYYY-MM-DD`.
5. In HubSpot, open the contact and confirm the 12 AI fields are populated and the LinkedIn task exists on the Day 1 date.
6. Enroll that contact in your HubSpot sequence and confirm step 1 renders the stored subject and body.

If that runs clean, you are live.

---

## 5. How to run it day to day

- **Named company:** "find me prospects at Acme Corp." Full four source discovery, qualifies everyone, writes AI fields for each Yes.
- **Several companies:** "find me prospects at Acme, Beta, and Gamma." Runs each in turn without stopping.
- **Single prospect:** paste a LinkedIn URL. Qualifies and sequences that one person.
- **Auto Mode:** "run discovery" or "sweep my accounts." Pulls your coldest owned accounts from the Company Pipeline tab, pre checks each, shows a clean list, then runs Company Mode on each.
- **Enroll tasks (Task Mode):** tag a contact in HubSpot with a to do task named "Enroll in sequence" (full 6 email) or "3 email sequence" (shorter), then say "process my enroll tasks." Claude qualifies each and writes the AI fields.
- **Re-engagement:** "re-engage [name]" for someone who already ran through a sequence months ago.

Your one manual step every time: when a LinkedIn task comes due, enroll that contact in the HubSpot sequence. That is the whole sending workflow.

---

## 6. The playbook (this is where your selling lives)

Claude reads these before drafting anything. Edit them to fit your company:
- `playbook/drafting-rules.md`: voice, email structure, banned phrases, the absolute em-dash ban. Mandatory read for the drafter.
- `playbook/product-lines.md`: your product lines and the role to sequence map.
- `playbook/vertical-intel.md`: what to lead with by industry, plus the competitive wedge. Role and skills decide the lead, not industry.
- `playbook/pain-and-objections.md`: pain points and a discovery question per product line, the objection handler bank, and the secondary source positioning. Lead with pain.
- `playbook/opener-library.md`: cold call openers.
- `playbook/voice-rules.md`: tone and the banned AI vocabulary filter.
- `knowledge/email-pattern-resolver.md`: how Claude resolves the right email address.

---

## 7. The em-dash rule (do not skip)

No em-dashes. Not in any email, subject, note, or script. Ever. The drafting rules state it up front, the voice rules repeat it, and `scripts/validate_email.py` hard stops any draft that contains one. If you fork the playbook, keep this rule intact. It is the difference between copy that reads human and copy that reads like a machine.

---

## 8. Customizing for your own company

- Product lines: edit `playbook/product-lines.md`.
- Email 1 templates: edit `skills/osi-outreach-sequence/SKILL.md`.
- Voice: edit `playbook/voice-rules.md`.
- Openers: edit `playbook/opener-library.md`.
- Verticals and wedges: edit `playbook/vertical-intel.md`.
- Pain and objections: edit `playbook/pain-and-objections.md`.
- ICP and disqualifiers: edit the THREE-POINT QUALIFICATION CHECK and DISQUALIFIERS sections in `skills/osi-prospect-qualification/SKILL.md`.

---

## 9. Optional, legacy laptop sending (most new users skip this)

An older model sent emails from a laptop via Outlook web, driven by three scheduled tasks (`osi-email2-rewriter`, `osi-email-sender`, `osi-monitor`). It is not in this package on purpose. A new user does not need it. The AI fields path in Sections 2 to 5 is the supported workflow. If you are ever migrating an existing email queue, ask Andy for the legacy skills.

---

## 10. Troubleshooting

- **AI fields are not populating:** confirm the 12 custom properties exist with the exact internal names in Step 3, and that your HubSpot owner ID in CLAUDE.md is correct.
- **HubSpot sequence sends a blank or a literal token:** the property name in the sequence token does not match the property Claude wrote to. Re check the internal names.
- **Validator raises an error:** the draft hit a hard rule (em-dash, banned vocabulary, a manufacturer claim). Read the error and fix the draft.
- **ZoomInfo returns no contacts:** a NO_MATCH is not a verification failure. The qualification skill falls back to LinkedIn by name and company.
- **Excel update fails:** confirm openpyxl is installed. Excel failures are logged, they do not block the AI field write.

---

## 11. What changed from v4

- **Sending moved to HubSpot AI fields and cloud sequences.** The Outlook sender, the Chrome send dependency, and the three scheduled tasks are no longer part of the core setup.
- **New HubSpot setup step:** create the 12 AI custom properties and a 6 step token based sequence (Step 3).
- **New playbook file:** `pain-and-objections.md` (pain points, discovery questions, objection handlers, secondary source positioning).
- **Vertical logic is role first, not industry first.** Optics for engineers, TPM for procurement and contract owners, in any vertical including banks. Added a Software/SaaS vertical.
- **Park Place / Service Express wedge consolidated and expanded** in `vertical-intel.md` (single source).
- **Enroll Task Mode** in the qualification skill: tag a contact and say "process my enroll tasks."
- **Em-dash ban hardened** across the playbook, the skills, and the validator.

---

## 12. Send feedback (please do this, it makes the next install easier)

When you finish, send a short feedback report back to Andy. The easiest and most useful way: in the SAME Cowork session you used to set this up, paste this prompt:

> "Read our entire setup conversation from the start. Fill in FEEDBACK.md honestly and specifically: total time, time per step, what errored, what was confusing, what was missing from the package, whether the smoke test passed on the first try, and the single change that would have made this easiest. Be blunt."

Claude has the whole session, so it can give a precise account of where you actually got stuck, better than memory. Save the filled `FEEDBACK.md` and send it back to Andy. He feeds it into the system and the next version fixes whatever tripped you.

If you would rather fill it by hand, open `FEEDBACK.md` and answer the questions as you go.

---

Built by Andy McLean (OSI Global). Questions: andy@osiglobal.com.
