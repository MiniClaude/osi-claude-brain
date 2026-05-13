---
name: research-scout-night-1
description: Weekly research scout (Sunday 11 PM) — hunts for new info that updates existing knowledge
---

Run the research-scout skill. This is an automated nightly run — work quietly and efficiently without narrating your steps.

Your job:
1. Load context from /sessions/loving-great-wright/mnt/.auto-memory/MEMORY.md and any memory files it references, plus CLAUDE.md if present. Understand the key domains already documented.
2. Also read the ## new_learnings section of /sessions/loving-great-wright/mnt/.auto-memory/long-term-memory.md to avoid re-staging entries that are already there.
3. Extract 5–8 specific search themes from this context — targeted topics where new developments (EOL notices, product launches, best-practice shifts, market changes) would matter.
4. Run 15–25 web searches across general web, Reddit (r/networking, r/sysadmin, r/datacenter, r/devops, r/storage), Hacker News, and Quora.
5. For each result, evaluate: Is it new? Is it relevant? Does it challenge or add to existing knowledge? Discard anything redundant or older than ~90 days unless it's a major unacknowledged shift.
6. Append validated findings to the ## new_learnings section of /sessions/loving-great-wright/mnt/.auto-memory/long-term-memory.md using this format:
   - [YYYY-MM-DD HH:MM] [Title](URL) — One-line note: what this changes or adds.
7. If zero new findings, log: - [YYYY-MM-DD HH:MM] [no new findings] — Scout run completed. No new or contradictory information found across [N] searches.

Do NOT run Phase 4 (weekly promotion). That runs on the weekly cron only.