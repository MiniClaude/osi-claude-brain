# OSI Skills, Dual-Location Setup

## What's here

This folder contains the OSI sales skills. Each skill has two things:
- A folder (`osi-skill-name/SKILL.md`). This is the editable source file.
- A `.skill` file (`osi-skill-name.skill`). This is the packaged version for Cowork installation.

## The two locations

| Location | Purpose |
|---|---|
| `C:\Claude-Brain\skills\` (this folder, Git-versioned, backed up at github.com/Drrewdy/Claude-Brain) | Source of truth. Edit here first. |
| Local Cowork `.claude/skills/` | What shows up as clickable skill tiles in the Cowork UI. Installed by clicking "Save skill" on a presented .skill card. |

## Sync rule

**Changes to either location must be applied to both.**

If returning to the other laptop and the source may have changed:
1. Run `git pull` in `C:\Claude-Brain\` to pull the latest skill sources from GitHub.
2. Tell Claude to check whether the packaged `.skill` files match the updated SKILL.md sources.
3. Claude will re-read, re-package, and re-present any changed `.skill` files.
4. Click "Save skill" on each card to reinstall.

If editing a skill in a Cowork session:
1. Edit the SKILL.md here in `C:\Claude-Brain\skills\[skill]\`.
2. Re-package it (`package_skill.py`) and overwrite the `.skill` file here.
3. Present via Cowork `present_files`, then click "Save skill" to update the local install.
4. `git add .`, then `git commit -m "skill: update [skill-name]"`, then `git push` so the other laptop can pull.

## The skills

- `osi-outreach-sequence`. Full 6-email automated outreach sequence.
- `osi-prospect-qualification`. LinkedIn prospect qualification (Profile Mode + Company Mode).
- `osi-3email-new`. Shorter 3-email first-touch sequence.
- `osi-3email-reengagement`. 3-email re-engagement for prospects who went through a prior sequence.
- `osi-cold-reengagement`. Find cold 1st-degree LinkedIn connections and create HubSpot tasks.
- `osi-old-customer-reengagement`. 5-email re-engagement for dormant former customers.
- `osi-email-task-drafts`. Auto-draft replies for due HubSpot email tasks.
- `osi-monitor`. Daily sequence monitor (bounces, replies, auto-pause).
- `osi-job-change-prospecting`. Weekly LinkedIn job-change and new-connection prospecting.

## Packaging workflow (for Claude)

```
1. Read SKILL.md from C:\Claude-Brain\skills\{skill}\SKILL.md
2. Edit in /sessions/.../skill_sync/build/{skill-name}/SKILL.md
3. cd /sessions/.../mnt/.claude/skills/skill-creator
4. python3 -m scripts.package_skill /sessions/.../skill_sync/build/{skill} /sessions/.../skill_sync/dist
5. cp dist/*.skill to C:\Claude-Brain\skills\
6. present_files on the .skill files, the user clicks Save skill
7. git add . && git commit -m "skill: update {skill-name}" && git push
```
