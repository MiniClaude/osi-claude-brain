---
name: stephen-jih-sce-email-2
description: Email 2 of 7 — Systain TPM angle to Stephen Jih at SCE
---

Send an email to Stephen Jih at Southern California Edison using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: stephen.jih@sce.com and press Tab
5. Click the Subject field and enter exactly: The other half of what we do
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

Stephen,

Different angle from my last note.

Beyond optics, we run Systain — OSI's third-party maintenance program. For utilities running large Cisco or Juniper estates, it typically cuts maintenance spend by 50 percent or more compared to OEM support, with 24/7/365 TAC and next business day hardware replacement.

SCE has the kind of infrastructure where EOL gear stays in production by necessity. The OEM walks away from those platforms. We don't.

If any of that matches what you're dealing with, worth a conversation.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.