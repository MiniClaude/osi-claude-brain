# Automation

Stores email queue files, scheduled task configs, and sequence templates.

## Files

| File | Purpose |
|------|---------|
| `email-queue.json` | Active outreach email queue (used by osi-email-sender skill) |
| `hard-block.json` | Domains/emails that should NEVER be contacted |
| `sequence-templates/` | Saved email sequence templates |

## Important

`email-queue.json` changes every time emails are sent/scheduled. 
Run `scripts/push.bat` at the end of each day to back it up.
