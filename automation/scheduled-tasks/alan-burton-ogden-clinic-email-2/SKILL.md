---
name: alan-burton-ogden-clinic-email-2
description: Email 2 of 7 — Alan Burton, Ogden Clinic — Optics angle
---

Send an email to Alan Burton at Ogden Clinic using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: alan.burton@ogdenclinic.com and press Tab
5. Click the Subject field and enter exactly: Your Cisco optics budget is someone else's bonus check
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

Alan,

Different angle from my last note.

We supply transceivers for every major platform — Cisco, Aruba, Juniper, Fortinet — from 1G to 100G. Coded in-house, same specs as OEM, 70-90% off list. We also do custom builds that OEMs won't touch, including dual-coded cables for multi-vendor environments.

Across 23 locations, that math gets interesting fast. If you're stocking gear for new sites or running into supply gaps, it's worth a look.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.