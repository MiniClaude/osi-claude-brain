---
name: mike-kleinman-costar-email-2
description: CoStar sequence — Mike Kleinman Email 2 EOL/SAN/TPM angle
---

Send an email to Mike Kleinman at CoStar Group using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: mkleinman@costar.com and press Tab
5. Click the Subject field and enter exactly: EOL on your VMware or SAN stack?
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

Mike,

Different angle from my last note.

Given your background on VMware and SAN, you probably know exactly which pieces of your storage environment are heading toward end of support. OEM maintenance on that gear past the initial contract is usually two to three times what it should be.

Our Systain TPM covers networking and server/storage assets at 50 percent or more below OEM pricing, with 24/7/365 TAC and next business day or 4-hour hardware replacement. We also support gear after OEM pulls the plug, which matters a lot when you're running a mature environment you don't want to refresh yet.

If any SAN or server maintenance contracts are coming up for renewal, worth a quick look at what a third-party option would actually cost.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.