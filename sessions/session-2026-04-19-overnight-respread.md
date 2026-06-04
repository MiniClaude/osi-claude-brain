# Overnight rebuild, 2026-04-19 to 2026-04-20

## Summary of work done

While Andy slept, the following was completed:

### 1. Four skills updated with new 6-window sendTime assignments

Every skill that writes to `email-queue.json` now assigns the correct `sendTime` per email slot:

- Email 1 → `sendTime: "4pm"`
- Email 2 → `sendTime: "11am"`
- Email 3 → `sendTime: "12pm"`
- Email 4 → `sendTime: "1pm"`
- Email 5 → `sendTime: "2pm"`
- Email 6 → `sendTime: "3pm"`

Files updated:

- `Claude-Brain/skills/osi-outreach-sequence/SKILL.md`
- `Claude-Brain/skills/osi-3email-new/SKILL.md` (3-email cadence preserved, first two gaps 2/4 business days, sendTimes 4pm/11am/12pm)
- `Claude-Brain/skills/osi-3email-reengagement/SKILL.md` (3-email re-engagement, wider gaps 10/12 business days, sendTimes 4pm/11am/12pm)
- `Claude-Brain/skills/osi-old-customer-reengagement/SKILL.md` (5 emails, gaps 5/2/5/8 business days, sendTimes 4pm/11am/12pm/1pm/2pm)

### 2. email-queue.json re-spread

- 60 prospects processed (all `-1` through `-6` entries, total 360 queue entries).
- Email 1s capped at 15 per 4 PM window, spread across Mon Apr 20 / Tue Apr 21 / Wed Apr 22 / Thu Apr 23, exactly 15 per day.
- Every prospect's Emails 2 through 6 recalculated using the new business-day self-healing cadence (2 / 4 / 6 / 5 / 6 business days, each anchored to the prior email's planned fire date).
- sendTime correctly assigned per email slot on every entry.
- File written atomically to OneDrive.

### 3. HubSpot LINKED_IN_CONNECT tasks updated

- 58 of 60 prospects had an existing LINKED_IN_CONNECT task in HubSpot. All 58 had their `hs_timestamp` updated to match the new Email 1 sendDate (noon ET on the Email 1 date).
- 0 failures across 6 batch update calls.
- 2 prospects had NO LINKED_IN_CONNECT task in HubSpot (likely prospected in an earlier session before task-creation was automated):
  - Brett Baker | Lippert
  - Lance Weaver | Rackspace
  - These can be created manually or on next prospecting pass.
- 1 company mismatch worth noting: Henry Jacobsen's HubSpot task shows company "Astound Broadband" but the queue entry says "Grande Communications" (Astound is the parent, same prospect, just parent-company naming in HubSpot). Task was matched and updated correctly.

### 4. New Email 1 fire schedule (Monday through Thursday this week, 4 PM ET)

**Mon Apr 20, 4 PM, 15 prospects:**
Brett Baker (Lippert), Lance Weaver (Rackspace), Roweenza Atangan (Bell Canada), Torrey Crabtree (Big River), Andrew Schnese (Nsight), Marcus Ramirez (GVTC), Ron Holt (Dark Fiber), Renee Carnes (altafiber), Gregory Henry (Armstrong Group), Vito Ciminello (Astound Broadband), Gary Duttenhefer (Consolidated Telcom), Juan Pardo (VTX1), Pete Johnson (Arvig), Kevin Keaveny (Big River), Dave Tofts (EastLink)

**Tue Apr 21, 4 PM, 15 prospects:**
Michael Soileau (LFT Fiber), Clarence Black (Plateau), Hiroyuki Hosono (Docomo Pacific), John Sasser (Sabey), Amre Hamouda (Spectrotel), LuAnn Argenta (Bausch), Etienne Trudel (Desjardins), Kyesun Lee (LG CNS), Josh Harless (Hunter), Ben Wexler (KeyBank), Alex Broque (Hurricane Electric), Joe Zarcone (Rackspace), Jeff Dear (GVTC), Eric Dessureault (Bell Canada), Thomas Prevost (Armstrong Group)

**Wed Apr 22, 4 PM, 15 prospects:**
Thomas Danz (Nsight), Jason McCollough (Armstrong Group), Mike Wills (altafiber), Stephen Wonderling (Armstrong Group), Henry Jacobsen (Grande Communications / Astound), Chris Clinton (VTX1), Noriel Ocampo (Docomo Pacific), Marc Delaune (Desjardins), Jonghwan Kim (LG CNS), David Hortsch (Hunter), Antonio Kida (Rackspace), Mike Fiszlewicz (altafiber), Dan Bradford (Nsight), Ed Martin (altafiber), Kevin Dancs (Spectrotel)

**Thu Apr 23, 4 PM, 15 prospects:**
Jim Weinheimer (Rackspace), Brad Arthur (altafiber), Lawrence Edmond (Nitel), Mark DePollo (ITHAKA), Scott Albert (Hunter), Walt Wollny (Hurricane Electric), Reid Fishler (Hurricane Electric), Jan Brooks (Rackspace), Eric Aitken (Rackspace), Valerie Kalti (altafiber), Robert Nance (Hunter), Tina Rahaim (Rackspace), Dimitar Petrovski (Rackspace), Daniel Windheim (Hunter), Kelly Cochran (Hurricane Electric)

(Order is roughly original queue order, so earliest-added prospects fire first.)

---

## ⚠️ What Andy still needs to do on the Mon-Thu laptop

**NOTHING fires until Andy re-enables the OSI Email Sender task.** It is currently disabled. That's intentional, do not re-enable until the three fixes below are done.

### Checklist to run when you're back at the Mon-Thu laptop

1. **Replace the Instructions field completely.** The previous paste didn't save correctly (UI cache issue). Select all existing text in Instructions, delete, paste the full corrected version from the Sunday night chat history (the one starting `You are the OSI email sender. Runs every weekday at 11 AM, 12 PM, 1 PM, 2 PM, 3 PM, and 4 PM Eastern Time.`). Save.

2. **Update the Repeats field.** It still shows `~At 10:00 AM and 04:00 PM, Monday through Friday`. Change it to fire at 6 times each weekday: **11 AM, 12 PM, 1 PM, 2 PM, 3 PM, 4 PM Eastern Time**. Whatever the UI format allows (cron, multi-time picker, plain English). Save. The "Next run" field should change from whatever it says now to show the nearest upcoming window.

3. **Verify both changes took effect.** After save:
   - Instructions field should start with `You are the OSI email sender. Runs every weekday at 11 AM, 12 PM...`
   - Instructions Step 4 should say `Also set the next entry's sendTime based on which email is next` (NOT the old "Leave its sendTime as 10am" line)
   - Repeats should show 6 fire times
   - Next run should be the nearest upcoming window (if you're doing this mid-day, it'll be whatever window comes next)

4. **Re-enable the task.** Toggle Active back on.

5. **Optional smoke test.** Run the task manually once from the Scheduled Tasks panel. It should return either "no entries for this window" (if the current time doesn't match a scheduled window exactly) or actually process any entries due right now. Either is a success signal.

### After re-enable, what fires when

Since today is Monday April 20, 2026:

- **11 AM, 12 PM, 1 PM, 2 PM, 3 PM today**: no entries match (no Email 2-6 for today's date in the queue). Sender returns "nothing to send" each window. Safe.
- **4 PM today**: 15 Email 1 entries match (sendDate 2026-04-20, sendTime "4pm"). Sender processes them one at a time, sends via Outlook, after each one updates Email 2's sendDate to April 22 and sendTime to "11am".
- **Tue 4 PM**: 15 more Email 1s.
- **Wed 11 AM**: first wave of Email 2s from Monday's cohort (15 emails).
- **Wed 4 PM**: 15 more Email 1s.
- **Thu 4 PM**: last 15 Email 1s.
- **Fri 11 AM**: Email 2s from Tuesday's cohort.
- And so on. Each day has distinct emails at each window, max 15 per window, no burst.

### Known gaps / things to address later

- **Brett Baker and Lance Weaver** have NO LINKED_IN_CONNECT task in HubSpot. They were prospected in an earlier session before task creation was automated. If you want the coordinated LinkedIn workflow for them, create tasks manually (Sales Nav -- Send connection request -- Brett Baker | Lippert, due 4/20; and same for Lance on 4/20). Both have Email 1 fire Monday 4 PM, so ideally the tasks should be created before then.
- **Henry Jacobsen**, HubSpot shows company "Astound Broadband" but queue says "Grande Communications." Task was still matched and updated (same person). No action needed but flagging in case the company name affects anything else.
- **Sender prompt**, the Sunday night fix was only partial. The full replacement is still pending.

---

## Files modified

- `Claude-Brain/skills/osi-outreach-sequence/SKILL.md`
- `Claude-Brain/skills/osi-3email-new/SKILL.md`
- `Claude-Brain/skills/osi-3email-reengagement/SKILL.md`
- `Claude-Brain/skills/osi-old-customer-reengagement/SKILL.md`
- `Claude-Brain/email-queue.json` (all 360 entries rewritten with new cadence and sendTimes)
- 58 HubSpot LINKED_IN_CONNECT task records (hs_timestamp updated)
