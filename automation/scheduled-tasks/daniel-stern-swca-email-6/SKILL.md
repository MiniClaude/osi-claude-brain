---
name: daniel-stern-swca-email-6
description: Email 6 of 7 — Daniel Stern, SWCA Environmental — Pattern interrupt
---

Send an email to Daniel Stern at SWCA Environmental Consultants using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, STOP and notify Brian via a notification — do not attempt to send the email. Also create a todo in the task list titled "Outlook session expired — resend Daniel Stern Email 6" so Brian can recover manually.
3. Click New mail
4. In the To field, enter: daniel.stern@swca.com and press Tab
5. Click the Subject field and enter exactly: Do you have any gear OEM no longer supports?
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

Daniel,

Direct question: do you have any networking or server gear that's hit end of life and is no longer covered by OEM support?

If yes, we should talk. If no, I'll stop reaching out.

8. Click Send
9. Verify the email appears in Outlook Sent Items within the last 2 minutes. If it is not found, report failure and stop.
10. Confirm the email was sent and report back.

Do not modify the email body in any way.