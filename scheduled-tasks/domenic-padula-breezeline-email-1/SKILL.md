---
name: domenic-padula-breezeline-email-1
description: Domenic Padula (Breezeline) — Email 1: Cold intro
---

Send Email 1 of Brian Charrette's outreach sequence to Domenic Padula at Breezeline.

RECIPIENT: dpadula@breezeline.com
SUBJECT: Quick question about your maintenance contracts
FROM: bc@osihardware.com

BODY (type this above Brian's existing signature — do NOT modify or delete the signature):
Running a DOCSIS 4.0 upgrade and a fiber expansion at the same time puts a lot of pressure on the operational budget. New build gets the capital, but the mature infrastructure still needs support — and OEM contracts don't get cheaper when you're also managing a parent company reorganization.

I work with IT directors at regional broadband operators to cut maintenance costs on the existing environment, typically 50% or more compared to Cisco, Juniper, or HPE pricing. Same SLA, 24/7/365 TAC, Level 2 and Level 3 engineers on every call.

We also handle optics for any speed tier — 10G through 400G, coded for your platforms, sometimes same day. If you've got contracts coming up for renewal or gaps in coverage, worth 15 minutes to see if the math makes sense.

INSTRUCTIONS:
1. Navigate to https://outlook.cloud.microsoft/mail/
2. Click New email (or New message button)
3. Fill in To: dpadula@breezeline.com
4. Fill in Subject: Quick question about your maintenance contracts
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