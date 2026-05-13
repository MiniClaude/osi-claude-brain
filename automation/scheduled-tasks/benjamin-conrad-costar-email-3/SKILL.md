---
name: benjamin-conrad-costar-email-3
description: CoStar sequence — Benjamin Conrad Email 3 soft touch
---

Send an email to Benjamin Conrad at CoStar Group using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: bconrad@costar.com and press Tab
5. Click the Subject field and enter exactly: Timing might be off
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

I know your inbox is not short on vendor email. I've sent a couple of notes and haven't heard back. No hard feelings.

I see this a lot with directors who just stepped into a bigger role. The first six months are mostly triage.

If you want, just reply and tell me when to check back. Otherwise I'll reach out again in a few months. Either way, no pressure from my end.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.