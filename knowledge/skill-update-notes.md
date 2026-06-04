# Skill Update Notes

## osi-prospect-qualification, Pending Update (2026-04-13)

### IT Procurement / Sourcing, Add as Primary TPM Target

Andy flagged: IT Procurement roles are primary decision-makers or co-signers on TPM contracts. They've been missed in searches. Apply this going forward in every TPM-targeted company search.

**Add to Priority Titles list in Step 1:**
- IT Category Manager
- IT Vendor Manager
- Strategic Sourcing Manager (IT or Technology category)
- Procurement Manager / Director (Technology or Hardware categories)
- IT Sourcing Manager

**Rule to add:**
> TPM NOTE: Anyone in IT Sourcing, IT Procurement, or Strategic Sourcing with a hardware or infrastructure category is a direct decision-maker or co-signer on TPM contracts. These roles often own or co-own vendor selection, contract negotiation, and renewal cycles. Search for them explicitly at every TPM target. Do not skip sourcing/procurement titles just because they don't have "IT" or "Network" in the title, check whether their category covers IT hardware or maintenance contracts.

**Action:** Run skill-creator to push this change to .claude/skills/osi-prospect-qualification/SKILL.md via the plugin.

---

### Systems Engineer, Add as TPM Target Title (2026-04-13)

Andy flagged: Systems Engineer titles should be included. At mid-market companies, Senior/Lead Systems Engineers often own or co-own the hardware they manage and are direct paths to TPM conversations.

**Add to Priority Titles list in Step 1:**
- Systems Engineer / Senior Systems Engineer / Lead Systems Engineer
- Infrastructure Engineer / Senior Infrastructure Engineer
- Network Administrator / Senior Network Administrator
- Systems Administrator / Senior Systems Administrator

**Rule to add:**
> TITLE BREADTH NOTE: When searching for TPM prospects, cast wide on the discovery side. Use judgment on qualification, do not filter people out based on title alone. A Senior Systems Engineer at a 500-person company may own every piece of hardware in the building. Search for engineer-level titles in addition to Director/VP/Manager titles, especially at smaller or mid-market companies. The title is a starting point; skills and trajectory determine the verdict.

---

### Expanded Title List, Full TPM Discovery Set (2026-04-13)

All titles below should be searched in Sales Navigator and web searches when prospecting for TPM targets. This replaces the narrower original list.

**INFRASTRUCTURE / DATA CENTER (highest priority for TPM):**
- Data Center Manager / Data Center Director / DC Operations Manager
- Data Center Engineer
- IT Asset Manager / IT Asset Director
- Head of IT Infrastructure / Head of Infrastructure
- Infrastructure Operations Manager
- Senior Infrastructure Engineer / Lead Infrastructure Engineer

**NETWORK / SYSTEMS OPERATIONS:**
- NOC Manager / Network Operations Center Manager
- Network Operations Manager
- Network Administrator / Senior Network Administrator
- Systems Administrator / Senior Systems Administrator
- Systems Engineer / Senior Systems Engineer / Lead Systems Engineer
- Infrastructure Engineer / Senior Infrastructure Engineer
- Telecom Manager / Telecommunications Engineer / Communications Manager

**STORAGE / COMPUTE:**
- Storage Administrator / Storage Engineer / Storage Manager
- Virtualization Engineer / VMware Administrator / VMware Engineer
- Compute Engineer / Server Administrator / Senior Server Administrator

**VENDOR / CONTRACT MANAGEMENT:**
- IT Vendor Manager / Vendor Management Manager
- IT Contract Manager / Technology Contract Manager
- IT Asset Manager (also listed above, high priority)
- IT Category Manager
- IT Sourcing Manager
- Strategic Sourcing Manager (IT or Technology category)
- Procurement Manager / Director (Technology or Hardware categories)

**OPERATIONS / MANAGEMENT (broader):**
- Technology Manager / IT Manager
- Head of IT
- IT Operations Manager / Director of IT Operations
- Service Delivery Manager (IT)
- ITIL Service Manager

**Rule to add to SKILL.md:**
> DISCOVERY vs. QUALIFICATION: The title list is for FINDING people, not disqualifying them. Cast wide on discovery. A Senior Systems Engineer at a 300-person company may own more hardware than a VP at a 5,000-person company. Once a profile is found, qualify holistically: title + trajectory + skills. Never skip a profile just because the title sounds junior, check what they actually own and influence.

> DATA CENTER MANAGER / IT ASSET MANAGER PRIORITY: These two titles are the most underrated TPM buyers. Data Center Managers own the physical gear. IT Asset Managers own the lifecycle of every asset that goes under a TPM contract. Search for both explicitly at every TPM company.

---

### DWDM / Optical Buyer Titles, Add to Discovery Set (2026-04-13)

Andy confirmed: Transport Engineer and DWDM/optical titles were missing from the discovery list. These are the primary buyers for SmartOptics DCP open line systems and optical transceivers. Add as a named section in Step 1 and the "Who Buys What" table.

**Add to Priority Titles in Step 1:**
- Transport Engineer / Senior Transport Engineer / Optical Transport Engineer
- Transport Network Engineer / DWDM Engineer / WDM Engineer
- Optical Network Engineer / IP/Optical Engineer
- Network Planning Engineer / Capacity Planning Engineer
- Optical Network Architect

**Update "Who Buys What", DWDM / Open Line Systems section:**
> Best-fit companies: carriers, CLECs, regional ISPs, cable MSOs, wholesale bandwidth providers, large colo operators. A Network Planning Engineer who is capacity-constrained on an existing DWDM system is a warm lead. SmartOptics DCP platform is 30-50% below Ciena/Nokia and ships in weeks.

**Rule to add:**
> DWDM NOTE: When prospecting at carriers, CLECs, MSOs, or colo operators, add Transport Engineer, DWDM Engineer, Optical Network Engineer, Network Planning Engineer, and Capacity Planning Engineer to the search. These are the people who design the optical layer and spec the platform. If they are capacity-constrained or running Ciena/Nokia gear, SmartOptics is a direct alternative. A planner sizing new wavelengths = warm lead regardless of exact title.

**APPLIED:** Changes above have already been pushed to `Claude-Brain/skills/osi-prospect-qualification/SKILL.md` on 2026-04-13.

---

### "Who Buys What", TPM Section Expanded with Full Buyer Descriptions (2026-04-13)

Andy confirmed the full set of TPM buyer titles with context for why each one matters. All added to the "Who Buys What" section with inline descriptions. Key additions:

- **Data Center Manager**, physically owns the gear, closer to TPM decisions than a VP two levels up
- **IT Asset Manager**, manages lifecycle of every asset under TPM. Most underrated buyer. Search explicitly.
- **NOC Manager**, knows exactly what's running, what's aging, what support costs
- **Storage Administrator / Storage Engineer**, owns NetApp/EMC gear, often missed because "Engineer" gets overlooked
- **Virtualization Engineer / VMware Administrator**, at smaller companies, often IS the infrastructure team
- **Head of IT / Head of Infrastructure**, 200-1,000 person companies, full decision authority with no VP/Director title
- **Technology Manager / IT Manager**, actual decision-maker at smaller orgs
- **IT Vendor Manager / IT Contract Manager**, at larger orgs, literally signs the TPM contract
- **Telecom Manager**, owns voice/data network infrastructure

**Rule added:** "TOP TWO for TPM: Data Center Manager and IT Asset Manager. Both are direct buyers that most reps miss entirely. Always search for these titles explicitly."

**APPLIED:** Changes pushed directly to `Claude-Brain/skills/osi-prospect-qualification/SKILL.md` on 2026-04-13.

---

### Search Approach Clarification (2026-04-13)

The title list is for DISCOVERY (finding people in Sales Nav / web search), not for DISQUALIFICATION. Once a profile is found, qualification is holistic: title + trajectory + skills. Cast wide on search, be precise on qualification.

