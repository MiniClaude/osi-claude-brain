---
name: tarl-smith-dematic-email-2
description: Email 2 of 7 to Tarl Smith at Dematic — optical/connectivity angle
---

Send an email to Tarl Smith at Dematic using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: tarl.smith@dematic.com and press Tab
5. Click the Subject field and enter exactly: High-bandwidth connectivity without the OEM markup
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

Tarl,

Different angle.

FinOps reviews almost always catch cloud compute and storage waste. What they rarely flag is the physical network layer, the transceivers and optical gear moving data between your on-prem infrastructure and your Azure environment.

We provide optical solutions from 1G through 400G, certified across 40+ OEM platforms, including custom builds your standard suppliers won't offer. Significant cost difference vs. OEM pricing, and we keep inventory ready so deployment doesn't slow your rollouts.

If that layer has room to optimize, worth a look.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.