---
name: jason-steele-bbw-email-7
description: Email 7 of 7 to Jason Steele at Bath & Body Works — breakup
---

Send an email to Jason Steele at Bath & Body Works using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com/mail/deeplink/compose in Chrome
2. If a login screen appears, stop and notify the user
3. In the To field, enter: jasteele@bbw.com and press Tab
4. Click the Subject field and enter exactly: Closing the loop
5. Place the cursor in the empty paragraph ABOVE the signature using JavaScript. DO NOT press Ctrl+Home and DO NOT click coordinates in the body area — both land inside Brian's HTML signature table and overwrite the Director of Key Accounts identity block. Use `mcp__Claude_in_Chrome__javascript_tool` with this snippet:

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

6. Type the email body exactly as written below (do not type a signature — Brian's HTML signature is already present below the cursor and must remain untouched):

Jason — I've sent a few notes over the past month. I don't want to be noise in your inbox so I'll leave it here.

If you ever run into a situation where you need hardware fast, a maintenance contract on gear your OEM won't touch, or an outside opinion on a refresh cycle, I'm easy to find. Happy to reconnect whenever the timing is right.

7. Click Send
8. Confirm the email was sent and report back

Do not modify the email body in any way.