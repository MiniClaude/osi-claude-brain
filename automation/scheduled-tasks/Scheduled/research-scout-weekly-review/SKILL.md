---
name: research-scout-weekly-review
description: Weekly review — promotes confirmed patterns from new_learnings into main memory files
---

Run the weekly knowledge promotion pass for the research-scout system.

This is the weekly review cron. Your job is to review the staging area, promote confirmed patterns into permanent memory, and clear what's been promoted.

Steps:

1. **Read the staging area**: Load /sessions/loving-great-wright/mnt/.auto-memory/long-term-memory.md — specifically the ## new_learnings section. Count the entries.

2. **Read existing memory**: Load /sessions/loving-great-wright/mnt/.auto-memory/MEMORY.md and any memory files it references. Understand what's already documented so you don't duplicate it.

3. **Identify confirmed patterns**: Look for 2+ entries in new_learnings that point to the same underlying trend, shift, or fact. These are "confirmed" — multiple independent sources found the same thing. Isolated single-source findings can stay in staging for another week.

4. **Promote confirmed patterns**: For each confirmed pattern:
   - Determine the appropriate memory type: user (about the user/their context), feedback (how to approach work), project (ongoing work/goals), or reference (where to find things)
   - Write or update the corresponding memory file in /sessions/loving-great-wright/mnt/.auto-memory/
   - Use the standard frontmatter format:
     ```
     ---
     name: [descriptive name]
     description: [one-line description]
     type: [user|feedback|project|reference]
     ---
     [memory content with **Why:** and **How to apply:** lines]
     ```
   - Add or update the pointer in MEMORY.md: `- [Title](file.md) — one-line hook`

5. **Move promoted entries to knowledge_base**: Cut the promoted entries from ## new_learnings and paste them into ## knowledge_base in long-term-memory.md, adding a note like: `(promoted to memory: [filename] on YYYY-MM-DD)`.

6. **Leave unpromoted entries alone**: Single-source or unconfirmed findings stay in ## new_learnings for the next weekly cycle.

7. **Log the run**:
   Append to ## new_learnings:
   `- [YYYY-MM-DD] Weekly review: reviewed [N] entries, promoted [N] patterns to memory, retained [N] entries for next cycle.`

8. **Brief summary**: At the end, output a 2–3 sentence summary of what was promoted and what's still pending. This is the only output you produce — the user will see it as the task completion notification.