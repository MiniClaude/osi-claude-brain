---
name: tony-ventura-breezeline-email-4
description: Tony Ventura (Breezeline) — Email 4 — DISABLED: email address bounced 2026-04-22
---

Send Email 4 of Brian Charrette's outreach sequence to Tony Ventura at Breezeline.

RECIPIENT: tventura@breezeline.com
SUBJECT: Re: Confirming address
FROM: bc@osihardware.com

BODY (type this above Brian's existing signature — do NOT modify or delete the signature):
I'm just prepping this package for you. I have a box of swag and a pair of sample SFPs to send to you from the team here at OSI Global IT.

Do you come into the office? Is that the best address to send it to right now?

INSTRUCTIONS:
1. Navigate to https://outlook.cloud.microsoft/mail/
2. Click New email (or New message button)
3. Fill in To: tventura@breezeline.com
4. Fill in Subject: Re: Confirming address
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