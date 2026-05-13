---
name: scott-warren-dhl-email-3
description: Send follow-up email 3 to Scott Warren at DHL (social proof, soft touch) — rescheduled from Sat 4/25 to Mon 4/27 to avoid weekend
---

Send an email to Scott Warren at DHL using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: scwarren@group.dhl.com and press Tab
5. Click the Subject field and enter exactly: Quick note
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

Didn't hear back, so I'll keep this short.

Global enterprise architects I've worked with usually tell me one of two things when I reach out: timing is off, or they've already looked at alternatives and made their call. Either way is fine.

If it's the former and there's a contract renewal or refresh coming up, I'm worth a quick call before it locks in. If it's the latter, no problem at all.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.