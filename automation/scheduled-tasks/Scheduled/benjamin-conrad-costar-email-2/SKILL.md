---
name: benjamin-conrad-costar-email-2
description: CoStar sequence — Benjamin Conrad Email 2 optics angle
---

Send an email to Benjamin Conrad at CoStar Group using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: bconrad@costar.com and press Tab
5. Click the Subject field and enter exactly: A question about your fiber infrastructure
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

Benjamin,

Different angle from my last note.

CoStar's infrastructure footprint is growing fast. A campus bringing on 3,500 people means more switching, more fiber, more connectivity requirements. If you're running into lead time issues on transceivers or looking at DWDM for expanded capacity, that's an area where we move a lot faster than OEM channel.

We code transceivers in-house for 40-plus platforms and carry custom builds that OEMs won't make, including DWDM solutions coded to work in environments that don't natively accept DWDM technology. Speeds from 1G up to 400G.

If that's a current project, worth a conversation. If not, no pressure.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.