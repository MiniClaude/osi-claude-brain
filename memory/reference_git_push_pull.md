---
name: Git push/pull for osi-claude-brain
description: How Brian manually pushes and pulls the osi-claude-brain repo to/from GitHub
type: reference
originSessionId: 29d15efc-1913-4764-b304-0fe4a9ef6538
---
## Repo location
`~/Documents/osi-claude-brain` (i.e. `C:\Users\Mini\Documents\osi-claude-brain`)
Remote: `git@github.com:MiniClaude/osi-claude-brain.git`

## To push (after auto-backup runs)
Open **Git Bash** and run one line at a time:

```bash
cd ~/Documents/osi-claude-brain
rm -f .git/index.lock   # only if you see a lock error
git add -A && git commit -m "auto-backup 2026-05-20" && git push
```

## To pull (on a new or secondary computer)
```bash
cd ~/Documents/osi-claude-brain
git pull
```

## Notes
- The `skills-github-autopush` scheduled task handles copying files into the repo automatically, but **cannot push** (no SSH keys in the sandbox). Brian pushes manually from Git Bash.
- If git errors with "index.lock exists", run `rm -f .git/index.lock` first — it's always a stale lock, no real process is running.
- LF/CRLF warnings on Windows are harmless.
- Paste commands one at a time in Git Bash — bracket paste mode (`^[[200~`) garbles multi-line pastes.
- Memory files are NOT yet synced to this repo — skills and scheduled tasks are, memory is not (AppData only).
