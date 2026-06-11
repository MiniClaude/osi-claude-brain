# System Setup Reference (2026-06-11 Consolidation)

Read this if anything about git, Obsidian, or folder layout is confusing. This is the day everything was consolidated.

## The Layout (only 3 folders matter)

| Path | What | Backup |
|------|------|--------|
| `C:\Users\Mini\Documents\osi-claude-brain` | THE system: CLAUDE.md, skills (all 67 in `skills\`), automation, email queue, memory, playbooks | GitHub `MiniClaude/osi-claude-brain` |
| `C:\Users\Mini\Documents\OSI-Notes` | THE Obsidian vault: notes, wiki, Knowledge, Accounts, Clippings | Nightly 9pm task mirrors it into the repo (`obsidian-vault-backup\`) which pushes to GitHub |
| `C:\Users\Mini\Documents\osi-skills-archive-2026-06-11` | Safety archive: superseded skills, 436 old task folders, 173 rescued files | Delete after a few weeks if nothing is missed |

`C:\osi-claude-brain` is a junction (shortcut) to the Documents repo. Keep it; skills reference that path.
`sharepoint\` inside the repo is a gitignored junction to `OneDrive - OSI Hardware`. Read company files through it; they never get committed.

## Git Workflow

- This machine is the MASTER. Work here, push from here.
- Remote: `https://github.com/MiniClaude/osi-claude-brain.git` (the old Drrewdy/Claude-Brain is disconnected forever; its history is preserved in this repo's merge history and branch `archive/lordandy-final-2026-06-11`).
- "OSI Brain Auto Push" Windows task commits and pushes daily at 3:30pm. Manual: `git add -A; git commit -m "..."; git push` from the repo.
- Other machines (server): one-time `git remote set-url origin https://github.com/MiniClaude/osi-claude-brain.git`, then `git pull` to stay current. They pull only, never push.

## Obsidian

- Vault = `Documents\OSI-Notes`. NOT in OneDrive, NOT a git repo, on purpose: a git resync once hollowed out the old vault and polluted the graph. Never run git inside the vault.
- Local REST API: `http://127.0.0.1:27123`, key in `skills/obsidian-vault/SKILL.md`. Works directly from PowerShell. Serves whichever vault is open in Obsidian.
- Old vaults (OneDrive OSI-Brain, Desktop backups) were deleted 2026-06-11 after rescuing unique files to the archive's `pre-delete-rescue\`. OneDrive online recycle bin held them for ~93 days from that date.

## Scheduled Automation (all verified 2026-06-11)

- `morning-brain-sync` — weekdays 7am, loads memory into chat
- `osi-email-sender` — weekdays 11am-4pm ET windows, sends queue, refreshes `memory/active-sequences.md` after each run
- `obsidian-vault-backup` — weekdays 9pm, mirrors vault into repo + pushes
- "OSI Brain Auto Push" (Windows Task Scheduler) — daily 3:30pm repo push

## Recovery Procedures

- **File missing from repo:** `git log --all --oneline -- "path/to/file"` then `git checkout <commit> -- "path/to/file"`. Or browse GitHub history.
- **Note missing from vault:** check `osi-skills-archive-2026-06-11\pre-delete-rescue\`, then the nightly `obsidian-vault-backup\` folder in the repo, then GitHub.
- **Locked folder that won't delete:** the Claude app keeps running in the system tray after the window closes; quit from the tray, then delete. A chat session whose working directory is inside a folder locks that folder for the session's life.
- **Old per-contact sequence contacts:** review list with HubSpot links and send counts at `Company Enrichment/prospecting/archived-sequence-contacts-2026-06-11.md` (73 contacts, all completed, none active).

## Active queue as of 2026-06-11

5 contacts pending: Buckner, Thales, SCI REMC, Nuvera (July swag), Lamb Weston (July swag). Everything else sent/completed.
