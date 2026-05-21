---
name: skills-github-autopush
description: Weekly auto-sync of Cowork skills + scheduled tasks to GitHub (MiniClaude/osi-claude-skills)
---

You are keeping Brian Charrette's Cowork skills and scheduled tasks backed up to GitHub automatically.

## Objective
Sync the latest Cowork skills AND scheduled tasks to the git repo at C:\Users\Mini\Documents\osi-claude-skills and push to GitHub (MiniClaude/osi-claude-skills).

## Steps

### Step 1 — Copy latest skills to repo
Use bash to copy all skills from the Cowork skills folder to the repo:

```bash
SKILLS_SRC="/sessions/busy-adoring-newton/mnt/.claude/skills"
REPO="/sessions/busy-adoring-newton/mnt/Documents/osi-claude-skills"
cp -r "$SKILLS_SRC"/. "$REPO/skills/"
echo "Skills synced: $(ls $REPO/skills | wc -l) folders"
```

### Step 2 — Copy latest scheduled tasks to repo
```bash
SCHEDULED_SRC="/sessions/busy-adoring-newton/mnt/Documents/Claude/Scheduled"
REPO="/sessions/busy-adoring-newton/mnt/Documents/osi-claude-skills"
mkdir -p "$REPO/scheduled-tasks"
cp -r "$SCHEDULED_SRC"/. "$REPO/scheduled-tasks/"
echo "Scheduled tasks synced: $(ls $REPO/scheduled-tasks | wc -l) folders"
```

### Step 3 — Git add and commit
```bash
cd /sessions/busy-adoring-newton/mnt/Documents/osi-claude-skills
git add -A
git status --short | wc -l
git commit -m "auto-backup $(date +%Y-%m-%d)" || echo "Nothing to commit"
```

### Step 4 — Git push via Chrome
Open Chrome and navigate to https://google.com to get browser focus. Then:
- Open a new tab
- Use the address bar or any available method to open Git Bash
- Run: cd ~/Documents/osi-claude-skills && git push

If git push cannot be automated via Chrome, send an email to bc@osihardware.com via Outlook with subject "⚡ Skills Backup — Push Needed" and body: "Your Cowork skills and scheduled tasks were committed locally but need a manual push. Run: cd ~/Documents/osi-claude-skills && git push"

## Success Criteria
- All skill folders are copied to the repo under /skills/
- All scheduled task folders are copied to the repo under /scheduled-tasks/
- A git commit is made with today's date
- Changes are pushed to GitHub OR Brian is notified by email to push manually

## Notes
- Repo: C:\Users\Mini\Documents\osi-claude-skills
- GitHub: https://github.com/MiniClaude/osi-claude-skills
- Skills source: C:\Users\Mini\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\...\skills
- Scheduled tasks source: C:\Users\Mini\Documents\Claude\Scheduled
- Brian's email: bc@osihardware.com
- If nothing changed since last backup, "nothing to commit" is fine — no email needed
