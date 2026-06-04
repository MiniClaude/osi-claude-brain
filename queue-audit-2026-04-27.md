# Queue Audit, 2026-04-27

Read-only sweep of the 712 pending entries (128 distinct prospects, 51 distinct companies, 50 unique email domains) in `email-queue.json` against HubSpot signal. Run after the John Lubeck dupe was caught at Midco.

**Method:** every queued `to:` was matched against HubSpot primary emails (all 128 returned a hit, so no orphan addresses). Then the 5 unverified-employer companies plus the top 5 high-volume domains were deep-scanned for dupes, pattern mismatches, and bounce history.

## Summary verdict

- **3 confirmed problems**, at least one prospect needs the queue swapped or canceled before send.
- **2 likely problems**, pattern mismatch warrants verification, may be ZoomInfo guesses.
- **1 domain-wide concern**, altafiber.com showing 8 bounces across 11 contacts (-80 score). Pattern is technically `firstname.lastname` but the domain itself appears unreliable. cinbell.com (legacy Cincinnati Bell) is the safer route.

## Confirmed problems, act before next send

### 1. Sarah Frisbie / altafiber, KNOWN BOUNCER, in queue
- HubSpot id 46214249386
- Queued `to: sarah.frisbie@altafiber.com`
- HubSpot shows `hs_email_bounce: 2` on this exact address
- Recommendation: cancel her sequence (6 entries) OR swap to `sarah.frisbie@cinbell.com` if she still works there. Verify employer first per the 2026-04-26 rule.

### 2. Ron Beerman / altafiber, KNOWN BOUNCER, in queue
- HubSpot id 3732051
- Queued `to: ron.beerman@altafiber.com`
- HubSpot shows `hs_email_bounce: 2` on this exact address
- Recommendation: cancel sequence OR swap to `ron.beerman@cinbell.com` if he still works there. Verify employer first.

### 3. Jeff Shields / Midcontinent, DUPE in HubSpot
- Two HubSpot contacts both at @midco.com:
  - id 217792447652, primary `jeff.shields@midco.com` (newer, ZoomInfo-pattern)
  - id 563898, primary `jeffrey.shields@midco.com` (older)
- Queue is sending to the newer dupe. Midco's verified pattern is `firstname.lastname`. The longer-form `jeffrey.shields` is more likely the working address.
- Recommendation: merge in HubSpot (jeffrey wins as primary, jeff.shields goes to `hs_additional_emails`), then swap queue `to: jeffrey.shields@midco.com`.

## Likely problems, verify before send

### 4. Eric Tijerina / Midcontinent, pattern mismatch
- HubSpot id 215131323140
- Queued `to: etijerina@midco.com`
- Midco's 22 contacts at @midco.com use `firstname.lastname` (john.lubeck, brad.janzen, derek.rieckmann, etc.). Only one other Midco contact uses `firstinitial+lastname`.
- ZoomInfo pattern guess. Likely correct address is `eric.tijerina@midco.com`.
- Recommendation: confirm with Eric or a quick LinkedIn check, then swap.

### 5. Joseph Vandecoevering / Hunter, possible nickname
- HubSpot id 214588201863
- Queued `to: joev@hunterfiber.com`
- Hunter's 15 contacts at @hunterfiber.com use `firstinitial+lastname` (dwindheim, dhortsch, jharless, etc.).
- `joev@` is `firstinitial+lastinitial+v`, looks like a personal preference (Joe + V) not a company-pattern address. Andy's gut: this is probably right because Joseph likely goes by Joe and the address may reflect that.
- Recommendation: probably fine. If concerned, verify on LinkedIn or via the company directory.

## Domain-wide observations

### altafiber.com, fragile domain
- 11 HubSpot contacts at @altafiber.com, 4 of them have bounced (timothy.nkansah, sarah.frisbie, ron.beerman, eric.brunner). Score: -80.
- The post-rebrand domain may not be fully provisioned. Brad Arthur and Ed Martin (in our queue) use `@cinbell.com` and that domain is clean (16 contacts, only 1 bounce).
- Recommendation when prospecting at altafiber: prefer `@cinbell.com` if the contact has historic email there; only use `@altafiber.com` after verifying via LinkedIn or web that the rebrand reached this person.

### Midco / Midcontinent, verified pattern is `firstname.lastname`
- 22 contacts, dominant pattern `firstname.lastname` (95%+).
- ZoomInfo's `firstinitial+lastname` guesses for this domain are wrong.
- Going forward: prospecting flow should construct `firstname.lastname@midco.com`.

### S&P Global, `firstname.lastname` dominant
- 17 contacts, dominant pattern `firstname.lastname@spglobal.com`.
- A few exceptions (`atapia@`, `guruprasad.r@`), possibly collisions or special cases.
- Going forward: default to `firstname.lastname`.

### Vero Networks, verified pattern is `firstinitial+lastname`
- 11 contacts, dominant pattern `firstinitial+lastname@veronetworks.com` (90%+).
- Queue is hitting that pattern correctly for all 4 prospects (jnelson, rbauer, nbryan, nmcginn).

### OEC Fiber, mixed patterns
- 8 contacts: 4 use `firstname` (david@, michael@, joe@, casey@), 4 use `firstname.lastname`.
- The "firstname only" pattern works for short common names. `firstname.lastname` for ambiguity.
- Queue: Trenton McVicker uses `trenton.mcvicker@`, others use the firstname form. Both look reasonable.

### Fidelity Communications, `firstname.lastname` pattern
- 6 contacts, all use `firstname.lastname@fidelitycommunications.com`. Clean.

### agoc.com (Armstrong Group), verified pattern is `firstinitial+lastname`
- 77 contacts, 71 use `firstinitial+lastname` (92%). Strong pattern.
- All 11 queued agoc addresses match.

### Rackspace, `firstname.lastname` dominant
- 67 contacts, 49 use `firstname.lastname` with 3 actual opens (score +3, verified by engagement).
- Some legacy/admin addresses (no-name, accountspayable, etc.) inflate other patterns.
- All queued rackspace addresses look correct.

### Hunter Communications, `firstinitial+lastname`
- 17 contacts, 15 use the pattern. Clean.

### Resound Networks, split between `firstname.lastname` and `firstname` only
- 14 contacts, 8 firstname.lastname + 4 firstname-only (jay@, chadd@, cole@, etc.)
- Founders/early hires likely got `firstname@` short addresses; later hires got `firstname.lastname`.
- Queue mix looks consistent with that.

## What's not yet verified

40 lower-volume domains were not deep-scanned. The email-match audit confirmed all 128 queued addresses exist in HubSpot as primaries. So the remaining risk is "primary in HubSpot is itself a bad ZoomInfo guess that happened months ago and was never corrected." For higher confidence on those, either:
- Run the full 11-batch domain sweep, or
- Wait for the new osi-monitor pre-flight section to flag them as they come up.

## Recommendation

Cancel or swap items 1, 2, and 3 before next send. Verify items 4 and 5. Domain-wide observations should feed the new pattern resolver as historical priors.
