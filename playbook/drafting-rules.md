# OSI Drafting Rules, Single Source of Truth

**Read this file inline as Step 0 before drafting ANY outbound copy.** Email body, subject, LinkedIn invite, LinkedIn InMail, voicemail script, call opener, anything that goes to a prospect.

This file replaces scattered references to:
- `playbook/voice-rules.md` (consolidated here)
- `playbook/product-lines.md` (consolidated here)
- `playbook/vertical-intel.md` (consolidated here)
- `knowledge/OSI-Sales-Playbook.md` (drafting-relevant subset consolidated here)

The validator at `C:\Claude-Brain\scripts\validate_email.py` enforces the absolute bans below at write time. Any drafted body that fails validation aborts the queue write.

---

## SECTION 1, ABSOLUTE BANS (validator aborts on hit)

These are hard stops. The validator scans every body and subject before queue write. If any pattern below is present, the write is aborted and the candidate flips to `pending-relookup` for manual review. No partial queue writes. No "fix it next session." The bad email never ships.

### 1.1 NO em-dashes or en-dashes, ever
The Unicode characters at codepoint U+2014 (em-dash) and U+2013 (en-dash) are banned in every body, subject, note, task description, voicemail, and LinkedIn message. Use periods to split sentences. Use commas for parenthetical clauses. Use hyphens only inside the allowlisted product names (Section 1.7). This file deliberately does not show the banned characters as literals; the validator references them via `chr(0x2014)` and `chr(0x2013)`.

This is Andy Rule #4 from `CLAUDE.md`. It is non-negotiable. The validator will refuse to write the queue entry if either character is present.

### 1.2 NO "SmartOptics" by name in cold outreach
Refer to optics as "OSI transceivers" or "our optics." NEVER name SmartOptics in Email 1 through Email 6 of any cold sequence, NEVER in cold LinkedIn invites, NEVER in cold call openers, NEVER in voicemails.

The only time SmartOptics is named is when the prospect asks directly, or pushes back on the product, AND the conversation has already established a relationship. None of those conditions are met during cold outreach. The validator bans the string in cold drafts.

Why: OSI private-labels these transceivers under the OSI brand. Naming the manufacturer in cold outreach commoditizes our offer and tells the prospect to go shop SmartOptics direct. Hold the brand back until they ask.

### 1.3 NO "we manufacture" claim
OSI does NOT manufacture optics. SmartOptics manufactures, OSI private-labels. Claiming OSI manufactures is factually wrong and the validator bans the phrase. Forbidden strings: "we manufacture", "manufactured by us", "OSI manufactures", "we make our own optics".

Acceptable framing: "we source," "we supply," "our optics line," "our transceivers."

### 1.4 NO credentials-first openers
The first sentence of Email 1 (and any cold LinkedIn message) references the PROSPECT, not OSI. Lead with their pain, their post, their company news, or their role. Never lead with who you are or what OSI does.

The validator bans these opener patterns at the start of Email 1 bodies:
- `^I'm Andy` / `^I am Andy`
- `^I'm with OSI` / `^I am with OSI`
- `^I'm at OSI` / `^I am at OSI`
- `^I work with` (when followed by a generic role description)
- `^I help` / `^I assist` (when followed by a generic role description)
- `^Hi, I'm` / `^Hi I'm`
- `^I wanted to reach out`
- `^I'm reaching out`

Email 2 through Email 6 have their own templates and do not use these openers either.

### 1.5 NO banned vocab
The validator scans for and rejects: crucial, pivotal, landscape, underscore, delve, showcase, testament, enhance, foster, garner, leverage (as a verb), unlock, supercharge, revolutionize, seamless, robust, holistic, synergy, cutting-edge, best-in-class, world-class.

If a synonym is needed, write plain English. "Important" instead of "crucial." "Highlight" instead of "showcase." "Use" instead of "leverage." Etc.

### 1.6 NO dead phrases
The validator bans these phrases in any body:
- "worth a conversation"
- "would this be worth"
- "worth 15 minutes"
- "worth a few minutes"
- "quick overview"
- "brief overview"
- "circle back" (in cold; OK in re-engagement context where prior contact existed)
- "touch base"
- "ping you"
- "pick your brain"
- "hop on a call"
- "jump on a call"

Replace with concrete asks: "Do you come into the office, or is there a better address to ship to?" or "Open to a 10-minute call Tuesday or Thursday?" or "If your team is up for renewal in the next 90 days, I can run a benchmark."

### 1.7 NO hyphens in bodies (allowlist below)
Voice rule from `playbook/voice-rules.md`. Bodies and subjects use plain English without hyphens. Examples:
- "third party" not "third-party"
- "end of life" not "end-of-life"
- "multi vendor" not "multi-vendor"
- "24/7/365" not "24-hour"
- "long term" not "long-term"
- "real time" not "real-time"

Hyphens are allowed ONLY inside this product-name allowlist:
- `400G`, `800G`, `100G`, `40G`, `10G`, `1G` (no hyphens, just identifiers)
- `DDR4`, `DDR5`, `DDR3` (no hyphens)
- `SFP+`, `SFP28`, `QSFP28`, `QSFP-DD`, `QSFP-DD800` (the DD form factor uses one hyphen)
- `Wi-Fi` (only when needed, "wireless" preferred)
- `ZR/ZR+` (slash, not hyphen)
- `Tier-1`, `Tier-2`, `Tier-3` (only when describing telco tiers; otherwise use "Tier 1")

The validator allows hyphens inside these tokens and rejects hyphens elsewhere.

### 1.8 NO rule of three
Three-item lists feel templated. Break into prose or pick the strongest two.

Bad: "We deliver speed, scale, and savings."
Good: "We ship in weeks at 30 to 50 percent below Ciena."

### 1.9 NO -ing pile-ups at sentence ends
Banned trailing constructions: "ensuring uptime," "highlighting our advantage," "reflecting market shifts," "delivering value," "driving outcomes."

These read like press releases. Replace with active verbs or sentence breaks.

### 1.10 NO negative parallelisms
Banned: "It's not just X, it's Y." "Not only A but also B." "Less of X, more of Y."

These are LinkedIn-influencer cadence. Andy doesn't talk like that.

### 1.11 NO "Andy" sign-off
The Outlook signature handles the sign-off. Typing "Andy" or "Best, Andy" or "Thanks, Andy" at the bottom of an email body produces a doubled signature. Bodies end at the last content sentence.

### 1.12 ONE product line per email (Surgical Isolation)
Andy Rule #2 from `CLAUDE.md`. Each email body covers exactly one OSI product line. Email 1 = one line. Email 3 = a different line. Email 4 = another different line. Within a single email, do not lump optics with TPM, do not lump DIMMs with storage, do not list product lines.

The validator checks for product-line keyword density. If two or more distinct product-line keyword clusters appear in one body, the write aborts.

---

## SECTION 2, OSI PRODUCT LINES

Every prospect is evaluated against all 7 lines. Pick ONE per email.

1. **Optics** , OSI transceivers (private-labeled, NEVER name the manufacturer in cold). Sample offer is the opening wedge for any network engineer or architect.
2. **DWDM and Open Line Systems** , 30 to 50 percent below Ciena and Nokia. Ships in weeks. Less rack space, less power, simpler to deploy.
3. **Compute and Components** , Dell and HP servers (authorized partner). DIMMs are the lead play right now (Samsung, Hynix, Micron, manufacturer warranties, below OEM). DDR4 significantly cheaper than DDR5 for workloads that don't need DDR5. Lead with DIMMs first, server refresh second.
4. **Storage** , pre-owned NetApp and enterprise storage gear, paired with OSI TPM. Cost and availability play.
5. **TPM** , Gartner-recognized, privately owned, no PE, 40 to 60 percent below OEM. Multi-vendor (Cisco, Dell, HP, NetApp, Juniper, Arista).
6. **Pre-Owned and New Networking Gear** , pre-owned Cisco, Juniper, Arista (tested, OSI TPM available, no SmartNet). New Nokia (authorized partner).
7. **Professional Services** , deployment, network design, migration. Second-conversation topic ONLY. Never lead cold.

### Authorized partner status (factual)
- OSI IS a Dell, HP, and Nokia authorized partner.
- OSI is NOT a Cisco partner. Cannot provide SmartNet or DNA licensing.
- OSI is a SmartOptics channel partner (the manufacturer relationship; NEVER named in cold).

---

## SECTION 3, SEQUENCE TYPE TO TARGET ROLE MAPPING

| Sequence | Target roles | Lead angle |
|---|---|---|
| Sample-Offer Network | Network Engineer / Architect / Transport Engineer | Free SFP sample |
| Sample-Offer Server | Systems / Infrastructure / Server Admin | Free DIMM sample |
| Pain-Led TPM | IT Director / DC Manager / IT Asset Manager / Procurement / mid-market CIO | OEM cost pain, vendor consolidation |
| Pain-Led DWDM | Transport / Optical NE / Network Planner at carrier, CLEC, MSO | Cost vs Ciena and Nokia, lead time |
| Pain-Led Storage | Storage Admin / Storage Engineer | Pre-owned NetApp plus TPM |
| Pain-Led Pre-Owned | Cisco, Juniper, Arista environments | Pre-owned plus OSI TPM |

Strategy note headers use these labels: `Call - Network`, `Call - Server`, `Call - TPM`, `Call - DWDM`, `Call - Storage`, `Call - Networking`.

---

## SECTION 4, KEY SALES WEDGES

Use these as Email 1 frames (one per email per Surgical Isolation):

- **Lead time advantage** , the top objection-handler vs anonymous factory importers and OEM backlogs.
- **Grey market vs engineered product** , our optics come from an engineering organization, not commodity factories.
- **400G upgrade path** , many accounts still running 100G with no plan, lead with the cost-controlled path forward.
- **Vendor-agnostic / multi-vendor support** , one TPM contract covering Cisco, Dell, HP, NetApp, Juniper, Arista.
- **Park Place / Service Express merger wedge** , see Section 6.
- **VMware / Broadcom licensing squeeze** , 3 to 5x license increases, position OSI savings as found money to offset.
- **AI infrastructure tailwind** , GPU buildouts under-fund the network. Use only when there's confirmed AI signal on the prospect's profile or company.
- **Energy cost / power efficiency** , SmartOptics draws less power and less rack space than incumbent DWDM. Use only with DC operators.

---

## SECTION 5, VERTICAL INTEL

### Telco / Service Provider
Companies: T-Mobile, AT&T, Verizon, Comcast, Lumen, Zayo, Cox, Charter.
Lead: optics, ZR/ZR+ coherent, DWDM open line systems.
Pain: OEM lead times stalling 400G and 800G core refreshes.
Do NOT: open with free SFPs at scale. Telcos deal in volume. Lead with supply chain reliability and technical credibility.
TPM note: rarely the engineer-level opener. Decisions sit at director.

### Large Banks / Financial Institutions
Companies: BofA, Citi, JPMorgan, Goldman, Wells Fargo, BNY, Morgan Stanley.
Lead: optics. Free SFP offer is the right foot in the door.
Do NOT: lead with TPM. Banks usually have TPM already (Park Place, Service Express, Curvature, Iron Bow). The engineer rarely controls the maintenance contract.
TPM as upsell only after relationship exists. Ask about non-critical gear (branch switches, test labs, dev environments, gear coming off SmartNet).
"VP" at banks is a job grade, not a seniority indicator. Verify with skills + trajectory before treating as decision-maker.

### Professional Services / Consulting
Companies: KPMG, Deloitte, EY, PwC, Accenture.
Lead: TPM is viable as opener. Cost-sensitive, less regulatory-constrained than banks.
Frame: lead with pain, not "we save 40 to 60 percent." Focus on SmartNet costs on gear running fine for years.
Also strong: free optics for break-glass sparing.

### Manufacturing
Companies: Forest River, Precision Castparts, Koch, PACCAR.
Lead: free optics as break-glass insurance. Limited budgets, high uptime requirements, small IT staff.
Also strong: TPM for aging Cisco gear past OEM support.

### Healthcare
Companies: hospital systems, health networks, pharma.
Lead: uptime and compliance. TPM with documented SLAs. DIMMs for refresh.
Differentiator: privately owned, no PE pressure. Engineering continuity matters here.

### Quebec / French-Canadian financial institutions
Companies: Desjardins, National Bank of Canada, Caisse Desjardins, Hydro-Quebec, Bell Canada, Videotron, Cogeco.
Search keywords are bilingual. See `osi-prospect-qualification` for French keyword list.
ZoomInfo is unreliable for these companies. Their keyword matching returns branch network and distribution roles, not IT. Use LinkedIn directly.

---

## SECTION 6, PARK PLACE / SERVICE EXPRESS MERGER WEDGE

Use when prospect is currently with Park Place, Service Express, Curvature, or Iron Bow.

**Conversation opener (verbatim, Andy-defensible):**
> "With the Park Place and Service Express merger, a lot of teams have been taking a fresh look at their TPM relationships. Have you had a chance to renegotiate since the merger, or are you still on the same rates?"

**OSI competitive positioning vs Park Place / Service Express:**
- Privately owned. No PE margin pressure on rates or staffing.
- No M&A disruption. Engineering team is intact.
- Gartner-recognized.
- Multi-vendor: Cisco, Dell, HP, NetApp, Juniper, Arista.
- Will competitive-bid against the existing provider.

**Andy-defensible framing:**
> "The merger between Park Place and Service Express has a lot of PE money behind it. That changes the priorities of a support organization. The focus moves from SLAs to margins. We hit 98 percent of our SLAs in 2025, we spare transparently, and if you decommission hardware mid-contract we give you a credit for the time left. We are not going to reorganize around a fund's exit timeline."

Rules:
- Do NOT position against other TPM providers on price. Don't say "we're cheaper than Park Place."
- The angle is service risk, not price.
- 98 percent SLA figure is 2025 data. Verify annually.

---

## SECTION 7, PERSONAL HOOK PRIORITY

Email 1 leads with the Personal Hook. The hook lives in the strategy note (built by `osi-prospect-qualification`). The drafter consumes it and writes the first sentence around it.

### Hook priority (qualification builds, drafting consumes)
1. **Recent post / repost / comment in last 3 to 6 months** (strongest)
2. **Recent job change or certification**
3. **Past company that's an OSI customer**
4. **Specific named project on their profile** (named system, named buildout, named refresh)
5. **Unusual skill combo** (e.g., DWDM + Storage Engineering + Vendor Management)

### What is NOT a Personal Hook
- Generic geography. "BNY's Pittsburgh footprint is significant" is filler, not a hook.
- Job title alone. "Saw you're a Senior Network Engineer" is not a hook.
- Tenure alone. "Saw you've been at the company for 5 years" is not a hook.
- Company size or industry alone. "Big bank" is not a hook.

### Hook quality gate
If the strategy note's Personal Hook is one of the "NOT a Personal Hook" cases, the drafter ABORTS Email 1 and flips the candidate to `pending-needs-hook` in `state.candidates`. Andy reviews next session and either pulls a real hook from LinkedIn or marks the candidate as no-hook-available.

The drafter does NOT write Email 1 with a thin hook.

---

## SECTION 8, FRESH HOOK SCORING

Qualification runs ONE web search per Yes verdict for company news in the last 30 days.

### Strong fresh hooks (use as Email 1 angle)
- Acquisition or merger (theirs or a competitor's)
- Senior exec hire (CIO, CTO, VP Infrastructure, VP Network)
- Earnings beat or miss (use carefully, not as primary hook)
- Product launch
- Buildout announcement (data center, network expansion)
- Strategic partnership

### Weak fresh hooks (omit, do NOT write filler)
- Awards
- Charity announcements
- Generic PR
- Random press releases
- Blog posts
- Marketing campaigns
- Sustainability reports

If no strong fresh hook is found, OMIT. Do NOT write filler like "BNY recently announced strong Q3 earnings" unless that earnings news genuinely connects to infrastructure spend.

---

## SECTION 9, APPROVED VENDOR RULE

Read `C:\Claude-Brain\approved-vendors.json` at draft time. Case-insensitive substring match against the prospect's company name.

### If matched
- **Email 1**: ONE soft acknowledgment. Verbatim phrasing: "Side note, we're already on your approved vendor list, so no new vendor onboarding if anything ever needs to move fast."
- **One of Email 3 OR Email 4** (drafter picks): brief reminder. Verbatim phrasing: "Quick reminder we're already approved at [Company] if timing matters."
- All other emails: silent.

### If NOT matched
- NEVER mention approved vendor status.
- NEVER use "vetted", "pre-approved", "pre-vetted", or "procurement" in Email 1.
- Don't invent a relationship that doesn't exist.

---

## SECTION 10, EMAIL 1 TEMPLATES

Three archetypes. Pick by sequence type (handed off from qualification).

### Template A, Sample-Offer (Network)
```
Hi [First],

[ONE-SENTENCE PERSONAL HOOK from strategy note. Reference what you actually saw on their profile or a strong fresh signal.]

I'd like to send you a couple of OSI transceivers to test in your environment. No commitment, no pitch. If they perform the way we say they do, the conversation takes care of itself.

Do you come into the office, or is there a better address to ship to?
```

### Template B, Sample-Offer (Server)
```
Hi [First],

[ONE-SENTENCE PERSONAL HOOK.]

I'd like to send you a sample DIMM from our current batch. Same spec as what you're running, manufacturer warranty, won't touch your OEM support contract.

Do you come into the office, or is there a better address to ship to?
```

### Template C, Pain-Led (TPM, DWDM, Storage, Pre-owned)
3 to 4 sentences. Lead with their specific pain (role + company + Personal Hook). Reference Fresh Hook only if strong. ONE clear ask. No name at bottom.

Structure:
```
Hi [First],

[Sentence 1: Personal Hook + their pain.]
[Sentence 2: One concrete OSI angle that addresses that pain. ONE product line.]
[Sentence 3 (optional): Fresh hook tie-in OR a specific data point.]
[Sentence 4: ONE concrete ask, not "worth a conversation."]
```

---

## SECTION 11, BAD EXAMPLE, NEVER WRITE LIKE THIS

The Christopher Lawrence email below shipped on 2026-04-30 and broke 7 rules in 95 words. Use as anti-template. Every Email 1 is mentally checked against this before write.

```
Christopher,

I'm Andy McLean at OSI Global. I work with IT infrastructure managers at large financial institutions on two areas where OEM pricing tends to be painful: transceivers and third party maintenance.

We manufacture SmartOptics transceivers at 80 to 90 percent below Cisco OEM list, and we do multi vendor TPM covering Cisco, Dell, NetApp, HP, and Arista at 40 to 60 percent below OEM rates.

BNY's Pittsburgh infrastructure footprint is significant. Happy to drop a sample optics box or run a quick TPM benchmark to show you the delta.

Worth 15 minutes?
```

What's wrong:
1. **Opens with "I'm Andy McLean at OSI Global"**. Credentials before pain. Section 1.4 violation.
2. **Names "SmartOptics" in cold**. Section 1.2 violation.
3. **Claims "we manufacture SmartOptics transceivers"**. Factually wrong. Section 1.3 violation.
4. **Two product lines (optics and TPM) crammed into one email**. Section 1.12 (Surgical Isolation) violation.
5. **"BNY's Pittsburgh infrastructure footprint is significant"**. Generic geography, not a Personal Hook. Section 7 violation.
6. **"Worth 15 minutes?"**. Dead phrase. Section 1.6 violation.
7. **Two pricing claims stacked**. Credentials dump, not pain-led.

The validator catches violations 1, 2, 3, 4, and 6 at write time. The 6-item self-check (Section 12) catches 5 and 7.

---

## SECTION 12, 6-ITEM SELF-CHECK

Before passing any email body to the validator, the drafter answers these six questions in writing in the working context:

1. Does the first sentence reference the prospect, not OSI?
2. Is the Personal Hook from the strategy note actually in this email?
3. Is there exactly ONE product line in this email?
4. Did I name SmartOptics? (must be no for cold outreach)
5. Did I claim OSI manufactures? (must be no)
6. Did I sign with "Andy" at the bottom? (must be no, Outlook signature handles it)

If any answer is wrong, rewrite before validating. The validator catches strings; this self-check catches semantics.

---

## SECTION 13, VOICE AND HUMANIZATION

- **Peer-to-peer**, not vendor-to-buyer. Andy reaches out as Andy, not as a company.
- **Short**. Mobile-friendly. Scannable in 10 seconds.
- **Tight prose**. No fluff.
- **Vary sentence length**. Mix short punchy with longer.
- **Use is, are, has** instead of "serves as," "stands as," "functions as."
- **Read-aloud check**. If it sounds like a press release, rewrite.
- **No emoji** in any cold outreach.
- **No exclamation marks** unless quoting someone.
- **No questions stacked**. One question per email maximum.

---

## SECTION 14, BREVITY LIMITS

- Email 1: under 90 words.
- Email 2 (RE: thread): under 50 words.
- Email 3 to 5 (standalone): under 80 words each.
- Email 6 (breakup): one or two sentences.
- LinkedIn invite: under 300 characters.
- LinkedIn InMail: under 600 characters, 3 sentences max.
- Voicemail: 15 seconds max, one sentence + hook + sign-off.

The validator counts words and aborts if any email exceeds its limit.

---

## SECTION 15, WHAT THIS FILE ENFORCES vs WHAT THE SKILL ENFORCES

This file holds the RULES. Each drafting skill holds the WORKFLOW (when to draft, what to do with the output, how to wire into the queue, scheduling, stagger calc, atomic writes, etc.).

The drafting skill calls this file. The drafting skill calls the validator. The drafting skill is responsible for the 6-item self-check happening. This file is responsible for being the single source of truth for what the rules ARE.

If a rule needs to change, change it here. The skills inherit automatically because they read this file at Step 0.
