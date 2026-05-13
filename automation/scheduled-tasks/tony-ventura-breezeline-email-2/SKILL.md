---
name: tony-ventura-breezeline-email-2
description: Tony Ventura (Breezeline) — Email 2 — DISABLED: email address bounced 2026-04-22
---

Send Email 2 of Brian Charrette's outreach sequence to Tony Ventura at Breezeline.

RECIPIENT: tventura@breezeline.com
SUBJECT: Transceivers for whatever speed you're running
FROM: bc@osihardware.com

BODY (type this above Brian's existing signature — do NOT modify or delete the signature):
Different angle from my last note.

On the optics side, we code transceivers for 40+ OEM platforms, 1G through 400G. If you're in the middle of DOCSIS 4.0 upgrades or pushing fiber deeper into the network, we can usually get compatible optics faster and at significantly less than OEM pricing.

We also build configurations OEMs won't make — extended distances, multi-platform twinax, DWDM coded as standard SFPs for platforms that don't natively support it. For ops teams managing gear across multiple markets, that flexibility can close a lot of procurement gaps.

Happy to talk specifics if there's a lead time problem or sourcing gap right now.

INSTRUCTIONS:
1. Navigate to https://outlook.cloud.microsoft/mail/
2. Click New email (or New message button)
3. Fill in To: tventura@breezeline.com
4. Fill in Subject: Transceivers for whatever speed you're running
5. Place the cursor in the empty paragraph ABOVE the signature using JavaScript via `mcp__Claude_in_Chrome__javascript_tool`. DO NOT press Ctrl+Home and DO NOT click coordinates in the body — both land inside Brian's HTML signature table and destroy the identity block. Use this snippet:

```js
const bodyEl = document.querySelector('div[aria-label="Message body"]');
const firstDiv = bodyEl.children[0];
bodyEl.focus();
const range = document.createRange();
range.setStart(firstDiv, 0);
range.collapse(true);
const sel = window.getSelection();
sel.removeAllRanges();
sel.addRange(range);
return {
  inSignature: !!(sel.anchorNode && (sel.anchorNode.nodeType === 1
    ? sel.anchorNode.closest('#Signature')
    : sel.anchorNode.parentElement && sel.anchorNode.parentElement.closest('#Signature')))
};
```

Verify `inSignature: false`. Then type the email body exactly as written (do not type a signature — the HTML signature is already present below the cursor).
6. Review that To, Subject, and Body look correct
7. Click Send

This email has been pre-approved by Brian Charrette as part of a planned outreach sequence he authorized.