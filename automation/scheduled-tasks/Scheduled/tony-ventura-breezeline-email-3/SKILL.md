---
name: tony-ventura-breezeline-email-3
description: Tony Ventura (Breezeline) — Email 3 — DISABLED: email address bounced 2026-04-22
---

Send Email 3 of Brian Charrette's outreach sequence to Tony Ventura at Breezeline.

RECIPIENT: tventura@breezeline.com
SUBJECT: If the timing is off
FROM: bc@osihardware.com

BODY (type this above Brian's existing signature — do NOT modify or delete the signature):
I know ops teams don't always have bandwidth for vendor conversations during a build push.

What I'll say is that the best time to look at a maintenance alternative is before a contract renews, not after. If you've got anything expiring in the next 6 months, that's usually the window where it's easy to compare.

If none of that applies right now, just say so and I'll follow up when it does.

INSTRUCTIONS:
1. Navigate to https://outlook.cloud.microsoft/mail/
2. Click New email (or New message button)
3. Fill in To: tventura@breezeline.com
4. Fill in Subject: If the timing is off
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