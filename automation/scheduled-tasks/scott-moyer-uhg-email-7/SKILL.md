---
name: scott-moyer-uhg-email-7
description: Email 7 of 7 (breakup / reset) to Scott Moyer at UHG/Optum
---

Send an email to Scott Moyer at UnitedHealth Group / Optum using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: scott.moyer@optum.com and press Tab
5. Click the Subject field and enter exactly: stepping back, door's open
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

I've sent a handful of notes over the past month and you've got real work to do. Last one from me for now.

OSI has the full stack when you need it. Cisco, Juniper, Nokia, Dell, HPE, Aruba, Fortinet. Systain TPM runs at half the OEM cost. Smartoptics in stock from 1G to 800G. Pro services cover everything from data center moves to IMAC work and ITAD pickups.

When the next project lands on your desk, I'd like to be the first call. No pitch or pressure, just a phone number you can use if you want options.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.