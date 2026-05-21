---
name: scott-warren-dhl-email-2
description: Send follow-up email 2 to Scott Warren at DHL (optics angle) — SENT MANUALLY 4/20 11:46 AM PT after silent fire-no-send
---

Send an email to Scott Warren at DHL using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: scwarren@group.dhl.com and press Tab
5. Click the Subject field and enter exactly: DHL runs a lot of fiber
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

Scott,

Different angle this time.

The same problem shows up on the optics side too. Global logistics infrastructure at DHL's scale means a lot of fiber, a lot of line cards, and a lot of transceiver spend. Most of it goes to the OEM at list price.

We supply optical transceivers from 1G to 400G, coded for Cisco, Juniper, and 40+ other platforms. Compatible, fully tested, and typically 50 to 70 percent below what you're currently paying. We also carry DWDM and custom builds the OEMs won't offer.

If any part of your budget goes toward optics right now, it's probably worth a look.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.