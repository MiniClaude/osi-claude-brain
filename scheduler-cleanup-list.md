# Scheduler Cleanup List — 2026-04-30

These tasks can all be safely deleted from the Cowork UI. None are firing — every entry is `enabled=false`. The 7 active `-cmig` tasks below the cleanup list are what's actually running.

How to delete: open Cowork's scheduled tasks panel, find each `taskId` exactly as written, delete.

---

## ✅ KEEP — these 7 are the live, working scheduler (do NOT delete)

1. `morning-skill-sync-cmig` — daily 9am
2. `osi-meeting-followup-cmig` — weekday 10am
3. `osi-overnight-runner-recurring-cmig` — every 2 hrs weekdays except 8am-2pm blackout
4. `osi-overnight-runner-recurring-weekend-cmig` — every 2 hrs Sat/Sun
5. `osi-sequence-monitor-v2-cmig` — weekday 2:15pm
6. `osi-email-sender-v2-cmig` — weekday 11am, 12pm, 1pm, 2pm, 3pm, 4pm
7. `job-change-prospecting-weekly-v2-cmig` — Mondays 2:30pm

---

## 🗑️ DELETE — old v1 versions (replaced by -cmig)

1. `weekend-linkedin-reengagement`
2. `job-change-prospecting-weekly`
3. `osi-sequence-monitor`
4. `osi-email-sender`

---

## 🗑️ DELETE — v2 versions (replaced by -cmig today)

1. `osi-email-sender-v2`
2. `osi-sequence-monitor-v2`
3. `morning-skill-sync`
4. `osi-meeting-followup`
5. `osi-overnight-runner-recurring`
6. `osi-overnight-runner-recurring-weekend`
7. `job-change-prospecting-weekly-v2`
8. `weekend-linkedin-reengagement-v2`

---

## 🗑️ DELETE — one-time tasks already past their fireAt

### Brett Baker / Lippert emails 1-3 (already past, replaced by email-queue.json system)
1. `brett-baker-lippert-email-1` (was 4/16/2026)
2. `brett-baker-lippert-email-2` (was 4/22/2026)
3. `brett-baker-lippert-email-3` (was 4/28/2026)

### Brett Baker / Lippert emails 4-6 (FUTURE-dated but obsolete — email-queue.json replaces this flow)
4. `brett-baker-lippert-email-4` (5/6/2026)
5. `brett-baker-lippert-email-5` (5/13/2026)
6. `brett-baker-lippert-email-6` (5/21/2026)

⚠️ Verify Brett Baker is actually in `email-queue.json` if you want continuity. If yes, these 3 are safe to delete.

### Emergency / delayed sends (past)
7. `emergency-4pm-email-send-2026-04-21`
8. `osi-email-sender-delayed-today` (was 4/21/2026)
9. `osi-email-sender-delayed-2026-04-27`

### Overnight batch one-shots (39 entries, all 4/24-4/28, all past)
10. `osi-overnight-batch-01-fri-1730`
11. `osi-overnight-batch-02-fri-1930`
12. `osi-overnight-batch-03-fri-2130`
13. `osi-overnight-batch-04-fri-2330`
14. `osi-overnight-batch-05-sat-0130`
15. `osi-overnight-batch-06-sat-0330`
16. `osi-overnight-batch-07-sat-0530`
17. `osi-overnight-batch-08-sat-0730`
18. `osi-overnight-batch-09-sat-0930`
19. `osi-overnight-batch-10-sat-1130`
20. `osi-overnight-batch-11-sat-1330`
21. `osi-overnight-batch-12-sat-1530`
22. `osi-overnight-batch-13-sat-1730`
23. `osi-overnight-batch-14-sat-1930`
24. `osi-overnight-batch-15-sat-2130`
25. `osi-overnight-batch-16-sat-2330`
26. `osi-overnight-batch-17-sun-0130`
27. `osi-overnight-batch-18-sun-0330`
28. `osi-overnight-batch-19-sun-0530`
29. `osi-overnight-batch-20-sun-0730`
30. `osi-overnight-batch-21-sun-0930`
31. `osi-overnight-batch-22-sun-1130`
32. `osi-overnight-batch-23-sun-1330`
33. `osi-overnight-batch-24-sun-1530`
34. `osi-overnight-batch-25-sun-1730`
35. `osi-overnight-batch-26-sun-1930`
36. `osi-overnight-batch-27-sun-2130`
37. `osi-overnight-batch-28-sun-2330`
38. `osi-overnight-batch-29-mon-0130`
39. `osi-overnight-batch-30-mon-0330`
40. `osi-overnight-batch-31-mon-0530`
41. `osi-overnight-batch-32-mon-0730-final`
42. `osi-overnight-batch-33-mon-1700`
43. `osi-overnight-batch-34-mon-1900`
44. `osi-overnight-batch-35-mon-2100`
45. `osi-overnight-batch-36-mon-2300`
46. `osi-overnight-batch-37-tue-0100`
47. `osi-overnight-batch-38-tue-0300`
48. `osi-overnight-batch-39-tue-0500-final`

### Discovery one-shots (all 4/24-4/28, all past)
49. `osi-discovery-a-cable-msos`
50. `osi-discovery-b-mixed`
51. `osi-discovery-c-sp-small-telcos`
52. `osi-discovery-d-regional-telcos`
53. `osi-discovery-e-resound-plus-auto`
54. `osi-discovery-resound-oneshot`
55. `osi-discovery-mega-2026-04-27-1410`
56. `osi-discovery-mega-2026-04-27-1440`
57. `osi-discovery-mega-2026-04-28-andy-named-10`
58. `discovery-mega-2026-04-28-1605`

---

## Total

- KEEP: 7
- DELETE: 70

After cleanup, `list_scheduled_tasks` will return 7 entries — your live fleet plus nothing else.
