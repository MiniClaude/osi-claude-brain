## 2026-04-27 10:30 AM ET run
- Initial fire used 24h window (Sun 2026-04-26 -> now): no calls. Exit clean.
- Skill updated post-fire to use **previous business day** window (Mon->Fri, skipping weekends + holidays). Source `skills/osi-meeting-followup/SKILL.md` edited, `.skill` repackaged, source-vs-package diff verified.
- Re-checked Fri 2026-04-24 -> now with the new window: 3 calls (Hurricane Electric, Fatbeam, AppGate) already processed Friday (markdown files present, tasks created). Not re-drafting to avoid polluting Andy's existing task bodies. Tomorrow's run will use Mon->now and catch anything fresh.

## 2026-04-28 2026-04-28 14:14 UTC run (osi-meeting-followup)
- Window: 2026-04-27 00:00 UTC -> 2026-04-28 14:07 UTC
- Calls returned by HubSpot search: 23
- Skill ceiling: 5 calls per fire. Prioritized real-conversation calls and voicemails where Andy promised follow up; skipped declines, internal/wrong-recipient, retired contacts.

### Processed (5)
- Stellar Broadband (Richard Laing, COO) -- existing task 108743650470 body UPDATED with draft. Action item: send Smart Optics portfolio.
- OEC Fiber (Trenton McVicker, Mgr TV/Network Ops) -- new same day task 108802402100 created. Action items: 3-4 month engineer call + add OSI to eval list.
- TNS Inc (Joe Kennedy, SVP Global Infra) -- new same day task 108785071250 created. Voicemail, no recap action items.
- Kal Karran (VP Network Access Mgmt) -- new same day task 108795384836 created (HIGH priority). FLAG: email on file kkarran4153453152@gmail.com looks malformed.
- Lingo Communications (John Lachance, Sr SE) -- new same day task 108793495105 created. Voicemail.

### Skipped (18)
- Ryan Bell, Deo Rajkumar (x2) -- declined, no follow up appropriate.
- John Aker -- retired, gave referral (Brian Woodbury); no follow up to John.
- Meraz Nasir -- voicemail, summary suggests wrong-recipient confusion.
- John F Novak, Kenneth Dutton, Tim Liford, Colin Vesper, Charles Kelley, Samuel Price -- voicemails, lower priority within 5/fire ceiling.
- Chadd Giles, Justin Pastore, Christian Henn, Andrew Hinegardner, Patrick O'Donnell, Christopher Lawrence, Josh Nelson -- no AI summary populated yet (skill rule: skip 'AI summary not yet ready'; tomorrow's run picks up if still in window).

### Notes
- Recap email parsing: Richard Laing and Trenton McVicker had structured Action items in HubSpot recap email; voicemails (Joe / Kal / John) had no structured items, drafted from hs_call_summary only.
- Meeting notes were appended to hs_call_body on all 5 records (initial attempt at hs_internal_meeting_notes failed - property does not exist; switched to hs_call_body).
- Markdown copies saved to C:\Claude-Brain\meetings\.

## 2026-04-29 14:10 UTC run (osi-meeting-followup)
- Window: 2026-04-28 00:00 UTC -> 2026-04-29 14:07 UTC (Tue -> now)
- Calls returned by HubSpot search: 3

### Processed (1)
- FITI / Foxsemicon (Ambrose "Yepu" Wang, ambrose.yp.wang@foxsemicon.com) -- existing pending task 108872543370 ("follow up on Lenovo Server Request") had empty body; UPDATED with auto draft + action items footer. Call ID 108833325853. KC Killoran was on the call too. Action items captured: Andy to send quote doc + Lenovo quote to KC, KC to price warranty + send Dell/HPE quotes, Wang to resend server requirements.

### Skipped (2)
- Lamar Horton (call 108836793928) -- duration 0, no AI summary populated. Outbound dial attempt with no conversation.
- Francis Gradel (call 108836300305) -- duration 0, no AI summary populated. Outbound dial attempt with no conversation.

### Notes
- Did NOT touch task 108342758531 ("Get a call with KC on the calendar") on Ambrose -- that task already has substantial Andy-reviewed draft body. Different topic (calendar request vs. post-call follow up).
- Used hs_call_body for AI meeting notes (hs_internal_meeting_notes still does not exist on calls -- carrying forward yesterday's workaround).
- Markdown copy: C:\Claude-Brain\meetings\2026-04-28-fiti-foxsemicon.md

## 2026-04-29 16:36 UTC -- post-fire cleanup + skill patch (HARD GATE)
Andy flagged: yesterday's run created email follow-up tasks on three VOICEMAILS (Lachance/Lingo, Kennedy/TNS, Karran). Skill was supposed to be Teams meetings only. It was not enforcing that.

Closed out the three bad tasks (status COMPLETED with auto-close note in body, since HubSpot blocks DELETED via API):
- 108793495105 (John Lachance / Lingo)
- 108785071250 (Joe Kennedy / TNS)
- 108795384836 (Kal Karran)

Patched `C:\Claude-Brain\skills\osi-meeting-followup\SKILL.md`:
- Added top-of-file hard rule: TEAMS MEETINGS ONLY. NEVER VOICEMAILS.
- Added Step 1.5 hard gate: must have structured CI markers (`<h5>Summary</h5>`, `<h5>Key notes</h5>`, `<h5>Topics discussed</h5>`), summary must NOT start with "voicemail/no answer/no conversation", and duration must be > 60s. All three checks must pass.
- Added stop condition entry. Added "Why this rule exists" pointer for future Claude sessions.

Repackaged `osi-meeting-followup.skill`. Source-vs-package diff verified clean.

## 2026-04-30 19:15 UTC run (osi-meeting-followup)
- Window: 2026-04-29 00:00 UTC -> 2026-04-30 19:10 UTC (previous business day -> now)
- Calls returned by HubSpot search: 17
- Step 1.5 Teams-meeting hard gate applied to all 17.

### Processed (2)
- **Desjardins** (Julien L'Ecuyer, Consultant detailed architecture - Network and Security) -- existing email task 108897240111 body UPDATED with draft. Action items: send transceiver lineup with model specs, third party maintenance details, OSI procurement contacts; follow up in two weeks. Markdown: 2026-04-29-desjardins.md.
- **Stratus Networks** (Ben Russell, CTO) -- existing email task 105278268837 (HIGH, "Ask Thomas for quote and send to Ben") body UPDATED with draft and due date bumped from 12:00 UTC to 16:00 UTC (12 PM ET) per skill spec. Action items: refreshed quote with barrel splice case filter swap on Galesburg, Brimfield rack mounted, datasheet/dimensions, SFB lead time, Ben + Tom Pruitt finalize 100G optics. Markdown: 2026-04-29-stratus-networks.md.

### Skipped (15) -- gate breakdown
- **Voicemails / dial attempts under 60s duration (10):** Atta Meer (0s), Ilya Knizhnik (4s), Joel Emter (29s structured-summary voicemail), Ryan Boyle (2s), Dimitar Petrovski (34s structured-summary voicemail), Bob Hancock (40s structured-summary voicemail), Daniel Windheim (22s structured-summary voicemail), Josh Young (29s no summary), Scott Albert (0s), Ed Martin x2 (0s and 6s "inactive number"), Lance Weaver (7s "voicemail box not set up"). All correctly gated -- voicemails are next-channel-is-another-call, not email.
- **No AI summary yet (3):** Christophe Desmars (75s but summary not populated), Jacob Britt (68s but summary not populated), Gary Chaney (today, recording probably still processing). Tomorrow's window catches them if summaries land.

### Notes
- Used hs_call_body for AI meeting notes on both processed calls (hs_internal_meeting_notes still does not exist on calls; carrying forward established workaround).
- All voice-rules.md checks applied to drafts: no em-dashes, no word-internal hyphens (rack mounted, splice case, third party, follow up), no banned vocab, no -ing pile-ups at sentence ends, no rule of three, no "Andy" sign-off, 3-4 sentences each.
- Step 1.5 hard gate (added 2026-04-29) worked as designed. Joel Emter, Bob Hancock, Daniel Windheim all had structured-CI summaries but failed duration check (< 60s). Pre-gate behavior would have drafted email follow-ups on those voicemails -- exactly the regression we patched out yesterday.

## 2026-05-04 14:30 UTC run (osi-meeting-followup)
- Window: 2026-05-02 00:00 UTC -> 2026-05-04 14:30 UTC (Mon run, lookback = Fri)
- Calls returned by HubSpot search: 0
- No meetings on Friday 2026-05-02. Exit clean.

## 2026-05-05 14:09 UTC run (osi-meeting-followup)
- Window: 2026-05-04 00:00 UTC -> 2026-05-05 14:09 UTC (previous business day -> now)
- Calls returned by HubSpot search: 8
- Step 1.5 Teams-meeting hard gate applied to all 8.

### Processed (0)
- No qualifying Teams meetings.

### Skipped (8) -- gate breakdown
- **Voicemails / dial attempts under 60s duration (8):** David Christian (31s, left voicemail), Chris Vainrib (37s, key notes confirm "voicemail message"), Ron Bauer (9s, forwarded to voicemail system, missing Key notes/Topics markers), David Dahl/109139327848 (39s, "left a message"), David Dahl/109139272113 (11s, automated IVR, missing Key notes marker), Steven Larson (36s, outbound reach-out description, 36s < 60s), Shawn Hillard (27s, no AI summary), Steve Pragaspathy (23s, "was unavailable to take the call").
- All correctly gated per Step 1.5. No email tasks created.

## 2026-05-07 14:12 UTC run (osi-meeting-followup)
- Window: 2026-05-06 00:00 UTC -> 2026-05-07 14:12 UTC (previous business day -> now)
- Calls returned by HubSpot search: 2
- Step 1.5 Teams-meeting hard gate applied to both.

### Processed (0)
- No qualifying Teams meetings.

### Skipped (2) -- gate breakdown
- **Orum Call with Daniel Hulse** (109249302181, 2026-05-06 20:00 UTC) -- duration 0ms < 60s threshold, no AI summary. Orum auto-dialer attempt with no conversation.
- **Orum Call with Ziad Nasser** (109217976608, 2026-05-06 08:02 UTC) -- duration 0ms < 60s threshold, no AI summary. Orum auto-dialer attempt with no conversation.

### Notes
- Both calls correctly gated per Step 1.5. No email tasks created.

## 2026-05-08 14:10 UTC run (osi-meeting-followup)
- Window: 2026-05-07 00:00 UTC -> 2026-05-08 14:10 UTC (previous business day -> now)
- Calls returned by HubSpot search: 0
- No meetings on Thursday 2026-05-07. Exit clean.

## 2026-05-11 14:10 UTC run (osi-meeting-followup)
- Window: 2026-05-08 00:00 UTC -> 2026-05-11 14:10 UTC (Mon run, lookback = Fri)
- Calls returned by HubSpot search: 0
- No meetings on Friday 2026-05-08 (or over the weekend). Exit clean.

## 2026-05-12 14:10 UTC run (osi-meeting-followup)
- Window: 2026-05-11 00:00 UTC -> 2026-05-12 14:10 UTC (previous business day -> now)
- Calls returned by HubSpot search: 0
- No meetings on Monday 2026-05-11. Exit clean.

## 2026-05-13 14:10 UTC run (osi-meeting-followup)
- Window: 2026-05-12 00:00 UTC -> 2026-05-13 14:10 UTC (previous business day -> now)
- Calls returned by HubSpot search: 0
- No meetings on Tuesday 2026-05-12. Exit clean.

## 2026-05-20 14:10 UTC run (osi-meeting-followup)
- Window: 2026-05-19 00:00 UTC -> 2026-05-20 14:10 UTC (previous business day -> now)
- Calls returned by HubSpot search: 0
- No meetings on Tuesday 2026-05-19. Exit clean.

## 2026-05-26 14:09 UTC run (osi-meeting-followup)
- Window: 2026-05-25 00:00 UTC -> 2026-05-26 14:09 UTC (previous business day -> now)
- Calls returned by HubSpot search: 0
- No meetings on Monday 2026-05-25. Exit clean.

## 2026-05-01 14:05 UTC run (osi-meeting-followup)
- Window: 2026-04-30 00:00 UTC -> 2026-05-01 14:02 UTC (previous business day -> now)
- Calls returned by HubSpot search: 2
- Step 1.5 Teams-meeting hard gate applied to both.

### Processed (1)
- **Amundi** (Jeremy Fornasiero, Head of Windows Server, Storage, Virtualization and Datacenters) -- existing email task 108879161722 body UPDATED with draft. Subject renamed from "follow up after meeting" to "Email Jeremy Fornasiero, follow up on Amundi proposal review"; priority bumped from NONE to MEDIUM; due date left at 2026-05-04 12:00 UTC (Monday, in-spec). Action items: OSI side -- Ann Morris to provide taxes and duties estimate plus offsite shredding security and chain of custody detail. Amundi side -- Jeremy to send photos for CoreSite and 365 sites, line up site surveys, confirm shredding option, return with proposal decision (expected end of next week, may include PO). Markdown: 2026-05-01-amundi.md.

### Skipped (1)
- **Gary Chaney call** (108969292079, 2026-04-30) -- no AI summary populated and no duration metadata. Same skip as yesterday's run. Likely a quick dial that did not produce a CI summary; if a summary lands later it will appear in the next run's window.

### Notes
- Used hs_call_body for AI meeting notes on the Amundi call. hs_internal_meeting_notes property still does not exist on calls -- skill spec Step 6 still references the wrong property name. Carrying forward established workaround. Carrying forward warning for skill-spec patch.
- Voice-rules.md applied: no em-dashes, no word-internal hyphens (offsite, follow up, third party variants not used here), no banned vocab, no -ing pile-ups at sentence ends, no "Andy" sign-off, 4 sentences total.
- Today's Amundi call happened at 9 AM ET; recap email landed at 9:27 AM ET; runner picked it up cleanly at 10 AM ET fire.
