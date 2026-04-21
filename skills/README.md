# OSI Skills — Dual-Location Setup

## What's here

This folder contains all 5 OSI sales skills. Each skill has two things:
- A folder (`osi-skill-name/SKILL.md`) — the editable source file
- A `.skill` file (`osi-skill-name.skill`) — the packaged version for Cowork installation

## The two locations

| Location | Purpose |
|---|---|
| `Claude-Brain/skills/` (this folder, OneDrive) | Source of truth. Edit here first. |
| Local Cowork `.claude/skills/` | What shows up as clickable skill tiles in the Cowork UI. Installed by clicking "Save skill" on a presented .skill card. |

## Sync rule

**Changes to either location must be applied to both.**

If returning after days away and OneDrive may have been updated:
1. Tell Claude to check the OneDrive skill versions
2. Claude will re-read, re-package, and re-present the updated `.skill` files
3. Click "Save skill" on each card to reinstall

If editing a skill in a Cowork session:
1. Edit the SKILL.md here in OneDrive
2. Re-package it (`package_skill.py`) and overwrite the `.skill` file here
3. Present via Cowork `present_files` → click "Save skill" to update the local install

## The 5 skills

- `osi-outreach-7email` — Full 7-email cold outreach sequence
- `osi-prospect-qualification` — LinkedIn prospect qualification (Profile Mode + Company Mode)
- `osi-3email-new` — Shorter 3-email first-touch sequence
- `osi-3email-reengagement` — 3-email re-engagement for prospects who went through 7 emails
- `osi-cold-reengagement` — Find cold 1st-degree LinkedIn connections and create HubSpot tasks

## Packaging workflow (for Claude)

```
1. Read SKILL.md from Claude-Brain (SharePoint API for cloud-only files)
2. Edit in /sessions/.../skill_sync/build/{skill-name}/SKILL.md
3. cd /sessions/.../mnt/.claude/skills/skill-creator
4. python3 -m scripts.package_skill /sessions/.../skill_sync/build/{skill} /sessions/.../skill_sync/dist
5. cp dist/*.skill to Claude-Brain/skills/ (delete cloud-only placeholders first if needed)
6. present_files on the .skill files → Andy clicks Save skill
```
