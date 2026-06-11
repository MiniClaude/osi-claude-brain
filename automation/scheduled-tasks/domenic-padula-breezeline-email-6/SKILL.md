---
name: domenic-padula-breezeline-email-6
description: Domenic Padula (Breezeline) — Email 6 — DISABLED: email address bounced 2026-04-22
---

Send Email 6 of Brian Charrette's outreach sequence to Domenic Padula at Breezeline.

RECIPIENT: dpadula@breezeline.com
SUBJECT: Quick yes or no
FROM: bc@osihardware.com

BODY (type this above Brian's existing signature — do NOT modify or delete the signature):
Quick question: are any of your Cisco or Juniper maintenance contracts coming up for renewal in the next 12 months?

If yes, I can show you what the savings look like in about 10 minutes. If no, I'll stop bothering you.

INSTRUCTIONS:
1. Navigate to https://outlook.cloud.microsoft/mail/
2. Click New email (or New message button)
3. Fill in To: dpadula@breezeline.com
4. Fill in Subject: Quick yes or no
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