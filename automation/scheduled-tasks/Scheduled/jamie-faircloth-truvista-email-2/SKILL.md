---
name: jamie-faircloth-truvista-email-2
description: Email 2 to Jamie Faircloth (TruVista) — Systain TPM angle
---

Send an email to Jamie Faircloth at TruVista using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: jfaircloth@truvista.biz and press Tab
5. Click the Subject field and enter exactly: Your Cisco SmartNet bill is probably too high
6. Place the cursor in the empty paragraph ABOVE the signature using JavaScript. DO NOT press Ctrl+Home and DO NOT click coordinates in the body area — both land inside Brian's HTML signature table and overwrite the Director of Key Accounts identity block. Use `mcp__Claude_in_Chrome__javascript_tool` with this snippet:

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
    : sel.anchorNode.parentElement && sel.anchorNode.parentElement.closest('#Signature'))),
  cursorAtFirstDiv: sel.anchorNode === firstDiv || (sel.anchorNode && sel.anchorNode.parentElement === firstDiv)
};
```

Verify the return shows `inSignature: false` and `cursorAtFirstDiv: true`. If `inSignature: true`, STOP and notify Brian — do not type or send, the signature will be destroyed.

7. Type the email body exactly as written below (do not type a signature — Brian's HTML signature is already present below the cursor and must remain untouched):

Jamie,

Different angle this week.

A company with 22 years of infrastructure history has hardware that spans generations. Cisco's OEM support on older ASR and NCS platforms gets expensive fast, and when gear hits end of life, their answer is usually a refresh quote, not a maintenance extension.

We run Systain, OSI's third party maintenance service. It covers EOL and legacy Cisco, Juniper, and other platforms with 24/7/365 technical support and next business day replacement SLAs globally. Operators typically cut their maintenance spend by 50 percent or more compared to what they're paying Cisco today.

No forced refresh, no eight week lead times on replacement parts. Just the gear you already trust, kept running.

Worth a quick look if any of your SmartNet renewals are coming up.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.