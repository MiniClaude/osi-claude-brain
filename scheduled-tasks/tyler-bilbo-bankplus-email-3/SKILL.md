---
name: tyler-bilbo-bankplus-email-3
description: Send Email 3 to Tyler Bilbo at BankPlus — soft touch (rescheduled from Sat 4/25 to Mon 4/27)
---

Send an email to Tyler Bilbo at BankPlus using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: tylerbilbo@bankplus.net and press Tab
5. Click the Subject field and enter exactly: One more note
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

Tyler,

I'll keep this short.

If the timing is off or the budget conversation isn't happening right now, that's completely fine. I'd rather hear that directly than keep sending notes.

If there's a Cisco contract renewal or a hardware refresh coming up at BankPlus in the next few months, I'm worth calling before it locks in. Happy to put real numbers together.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.