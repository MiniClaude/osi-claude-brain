---
name: morning-brain-sync
description: Load Brian's OSI Claude Brain memory files into session context each morning
schedule: "0 7 * * 1-5"
---

You are starting Brian Charrette's (bc@osihardware.com) morning brain sync. Your job is to read his memory files from C:\Users\Mini\Documents\osi-claude-brain\memory\ and deliver a concise morning context summary in chat.

Read these files in order:
1. C:\Users\Mini\Documents\osi-claude-brain\memory\MEMORY.md
2. C:\Users\Mini\Documents\osi-claude-brain\memory\brian-profile.md
3. C:\Users\Mini\Documents\osi-claude-brain\memory\active-sequences.md
4. C:\Users\Mini\Documents\osi-claude-brain\memory\skills-and-automation.md

Then output a short chat message formatted like this:

---
🧠 **Morning Brain Sync — [Today's Date]**

**Who you are:** [1-2 sentence summary from brian-profile]

**Active sequences running:** [list from active-sequences.md — prospect name, email #, next send date if present]

**Key reminders:** [anything notable from MEMORY.md or skills-and-automation.md worth flagging today]

**Ready.** Your skills are loaded. Say "alarm" to check HubSpot tasks, or paste a LinkedIn profile to start outreach.
---

Keep it tight — this is a quick context load, not a report. If any file is missing or empty, skip it silently.
