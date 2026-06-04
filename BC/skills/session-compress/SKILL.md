---
name: session-compress
description: >
  Compress and summarize the current Claude Cowork/Code session into a TL;DR, delivered inline in chat.
  Produces: what the session was about, key decisions made, things built/done, open items, and a
  "context reload" block the user can paste at the top of a new session to instantly re-orient Claude.

  ALWAYS use this skill when Brian (or any user) says anything like: "compress this chat",
  "compress my session", "TL;DR this session", "summarize this session", "compress this conversation",
  "session compress", "what did we do this session", "give me a summary of this chat",
  "compress recent chat", "recap this session", "session summary", or any variation of wanting
  a compact summary of the current or most recent Claude session. Trigger even if they just say
  "compress" without further context while in a Cowork session.
---

# Session Compress

Your job: read the current session transcript and produce a tight, useful TL;DR inline in chat.
No files, no preamble — just the summary.

## How to get the transcript

1. Call `list_sessions` (limit: 10).
2. Find the session that represents the current conversation. It will be near the top of the list —
   look for the non-child session that is most recently active. If you're running as a subagent,
   the parent session is the one to summarize (the first `is_child: false` entry is usually it).
3. Call `read_transcript` on that session ID with `format: full` and `limit: 100`.
   This gives you the last 100 messages, which is enough for any normal session.

## What to produce

Respond with this exact structure (no extra headers, no intro sentence like "Here's your summary"):

---
## Session TL;DR

**What this was about**
[1–2 sentences. What was the user trying to accomplish?]

**Decisions & conclusions**
- [Each meaningful decision or conclusion reached — skip routine back-and-forth]

**Built / done / sent**
- [Files created, emails sent, HubSpot records updated, reports run, etc. Be specific — filenames, contact names, company names if present]

**Open items / next steps**
- [Anything the user said they'd do next, or that was left unresolved]

**Context reload**
*Paste this at the top of a new session to re-orient Claude:*
> [3–5 dense sentences capturing: who the user is, what they were working on, what was completed,
> what still needs doing, and any key details Claude would need to continue. Write it in second
> person as if briefing Claude: "Brian is a senior IT hardware sales rep at OSI Global..."]
---

## Tips for a good summary

- **Be specific, not generic.** "Created a 7-email sequence for John Smith at Acme Corp" beats "ran an outreach sequence."
- **Skip the meta-chatter.** Don't log things like "user asked a clarifying question" or "Claude confirmed it understood."
- **If the session was short or trivial**, say so — don't pad it. A 3-line TL;DR is fine.
- **If nothing was built/done**, omit that section rather than putting "N/A."
- **The context reload block is the most valuable part** — make it dense enough that a fresh Claude instance could pick up exactly where this one left off.
