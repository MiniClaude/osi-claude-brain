---
name: consolidate-memory
description: Nightly memory consolidation — extracts key facts from today's sessions and updates the three memory files
---

You are running the nightly memory consolidation for Brian Charrette (bc@osihardware.com), a senior sales rep at OSI Global.

Your job is to update three persistent memory files based on today's conversation sessions. Follow these steps exactly:

## Step 1 — Read Current Memory State
Read all three memory files:
- /sessions/stoic-epic-hamilton/mnt/.claude/memory/recent-memory.md
- /sessions/stoic-epic-hamilton/mnt/.claude/memory/long-term-memory.md
- /sessions/stoic-epic-hamilton/mnt/.claude/memory/project-memory.md

## Step 2 — Pull Recent Session Transcripts
Use mcp__session_info__list_sessions to list available sessions. Then use mcp__session_info__read_transcript to read any sessions that were active in the past 24 hours. Extract:
- Decisions made (what Brian chose, approved, or rejected)
- New facts learned (about clients, accounts, products, preferences)
- Preferences expressed (tone, format, workflow choices)
- Projects discussed (new work, deadlines, account names, deal stages)
- Deliverables created (files made, documents sent, tasks completed)
- Open threads (things mentioned but unresolved)

## Step 3 — Update recent-memory.md
Rewrite the file with today's date and updated sections:
- Active Context: what Brian is currently working on
- Recent Decisions: key choices from the last 48 hours
- Recent Deliverables: files or tasks completed
- Open Threads: unresolved items

Remove entries older than 48 hours.

## Step 4 — Promote Durable Facts to long-term-memory.md
For each item in the prior recent-memory.md (now ~24hrs old), ask: "Would this still be useful in 2 weeks?"
- If yes, add it to the appropriate section of long-term-memory.md
- If no, discard it
Update the _Last updated_ date.

## Step 5 — Update project-memory.md
- Move completed projects to "Completed (Recent)"
- Add newly mentioned projects with status, why, and next steps
- Update "Key Accounts in Play" with any new account names or deal context
- Add/remove deadline entries
- Archive entries older than 30 days with no activity
Update the _Last updated_ date.

## Step 6 — Output Summary
Print a short summary (3-5 bullets) of what changed across all three files. Keep it concise.

## Rules
- Never delete from long-term-memory.md without good reason — prefer updating or archiving
- When unsure about promotion, add: "Tentative — verify next session"
- Do not store sensitive data (passwords, SSNs, financial account numbers)
- Always update the _Last updated_ date in every file touched