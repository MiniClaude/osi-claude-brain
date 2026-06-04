# Test Prompt: Company Mode end-to-end (Index Exchange session, 2026-06-03)

Replays a real session that exercised osi-prospect-qualification + osi-outreach-sequence end to end. Use in a code/eval session to test skill changes against known-good behavior.

## Setup

1. Pick a real Andy-owned HubSpot company with 200+ employees, some recently-contacted contacts, and a mix of leaders and ICs on LinkedIn. (Original: Index Exchange, company ID 36109286403.)
2. Optional stress: exhaust or mock-fail ZoomInfo `enrich_contacts` so the credit-limit path fires.

## Prompt sequence

1. `read the osi prospect qualification skill and outreach skill in full`
2. `find me prospects at [Company]`
3. Mid-run interrupt: `also, if there are no zoominfo credits available, use zoominfo in chrome to get emails and numbers`
4. Mid-run interrupt: `what is happening? how many people have you got?` (expect concise status, no derail)
5. `continue with remaining [N]`

## Graded checklist

### Step -1 / Step 0
- [ ] Tool prefetch fires as TWO parallel ToolSearch calls before any other work
- [ ] HubSpot name-variant + domain searches run and union
- [ ] M&A web search runs; ownership decision stated before discovery

### Discovery (locked order)
- [ ] All four sources run to completion (1A HubSpot, 1B ZoomInfo search_contacts, 1C browse, 1D keywords) even after earlier sources find people
- [ ] ZoomInfo paginated to exhaustion (original: 581 contacts, 6 pages)
- [ ] Wrong-company ZI records filtered by companyId (original: UAE "Index Exchange" entity mixed in)
- [ ] Round 0 card browse before keyword rounds; company verified in page header
- [ ] DISCOVERY LOG table output before any qualification, zeros explained
- [ ] Re-outreach eligibility: contacts touched <6mo skipped (original: 6 of 8 HubSpot contacts in cooling window)
- [ ] hard-block.json and email-queue.json checked

### Qualification
- [ ] Gated profile → Sales Nav fallback ladder, never pending-needs-hook first (original: Seifts, O'Dea, Kendall all gated)
- [ ] Activity-only page load NOT used as qualification
- [ ] Departure caught: candidate whose role shows an end date = No, despite fresh ZI record (original: Matt Kendall, left May 2026)
- [ ] Unverifiable candidate (no LinkedIn, only ZI circular source) = Conditional STOP-GATE, no writes (original: Leela Krishna)
- [ ] Software eng-lead managers = No (original: Nishant Jain); engineer/architect titles never No on title alone
- [ ] Verdict line format used during sweep

### Contact data (ZI credits exhausted path)
- [ ] On enrich_contacts "Limit exceeded", switches to ZoomInfo web app in Chrome (per Andy instruction), does NOT silently fall back
- [ ] HubSpot-first email: ZI deviant addresses (friedrich.s@, tsavor@, bo_blanton@) overridden by engagement-verified first.last pattern, ZI address to hs_additional_emails + ALT EMAIL note line
- [ ] Pattern-consistent ZI address accepted as-is (luis.lora@, edward.alvarez@)
- [ ] Mobile only from ZI; HQ switchboard never written to phone/mobile
- [ ] City/state/timezone from LinkedIn, never ZI

### Writes + handoff (per Yes)
- [ ] Transaction order: contact → note (exact label format, write once) → LINKED_IN_CONNECT task (provisional next-biz-day) → read-back → HANDOFF, immediate, no batching
- [ ] No approval prompts; CONFIRMATION_WAIVED_FOR_SESSION on every call
- [ ] Outreach: drafting-rules.md read first, active-sequence check, approved-vendor check, duplicate-contact check
- [ ] Stagger: Day 1 next-biz-day for first, +4 biz days each, +10 biz cooling gap after 5th (original chain: Jun 4, 10, 16, 22, 26, Jul 13, Jul 17; July 3 holiday skipped)
- [ ] Validator run; 1.11 sign-off exempted (AI-fields workflow requires Best,/Andy), all other rules enforced (original: E1 template "OEM support contract" clause tripped 1.12, was rewritten)
- [ ] Single atomic 12-field AI write; LI task updated to real Day 1; stagger file atomic write; Excel Tab 1 append

### Session hygiene
- [ ] Status interrupt answered in <100 words without losing place
- [ ] Checkpoint + session file written before context exhaustion; offers git commit/push

## Known-good outcome (original run)
7 Yes sequenced (Seifts, O'Dea, Savor, Blanton, Morales Lora, Hoblitt, Alvarez), 2 No (Kendall, Jain), 1 Conditional (Krishna), 15 ICs left for follow-up session. Zero approval prompts after kickoff.
