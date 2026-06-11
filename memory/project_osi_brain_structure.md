---
name: osi-claude-brain file structure
description: Brian's local machine file structure for osi-claude-brain — one master copy in Documents after 2026-06-11 consolidation
type: project
originSessionId: 867df237-b618-4f56-bba5-17af5aead8c6
---
**Confirmed active path:** `C:\Users\Mini\Documents\osi-claude-brain\`

This is the ONE osi-claude-brain on Brian's master computer. Git-tracked, connected to https://github.com/MiniClaude/osi-claude-brain, fully consolidated 2026-06-11.

**Junctions (pointers, not copies, keep them):**
- `C:\osi-claude-brain` -> points to the Documents folder. Skills reference this short path.
- `sharepoint\` inside the brain -> points to `C:\Users\Mini\OneDrive - OSI Hardware` (company SharePoint files, gitignored, read in place, never commit).

**Skills:** ALL skills live in `skills\` at the brain root (67 skills, consolidated 2026-06-11). The old `BC\skills\` and `andyStarterPackage\` are gone. Superseded copies archived locally at `C:\Users\Mini\Documents\osi-skills-archive-2026-06-11\` and recoverable from git history.

**Deleted duplicates (do not recreate):** `Documents\LordAndy` (history on GitHub branch `archive/lordandy-final-2026-06-11`), `Documents\osi-claude-brain\LordAndy` (emptied, husk folder remains until last session closes), `C:\Claude-Brain\` (Andy's old path, never existed on this machine as active).

**Sync model:** This machine is the master, heavy work happens here. Other machines (server) pull only from MiniClaude/osi-claude-brain. The old Drrewdy/Claude-Brain remote was disconnected 2026-06-11.

**How to apply:** Always use `C:\Users\Mini\Documents\osi-claude-brain\` (or the `C:\osi-claude-brain` junction) for all scripts, automation, file paths, and references. Flag anything pointing to `C:\Claude-Brain\` or LordAndy paths as wrong.

Projects folder:
- `projects\company-enrichment-prospecting\`
- `projects\connecting-two-computers\`
