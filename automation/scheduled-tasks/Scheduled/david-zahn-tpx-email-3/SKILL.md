---
name: david-zahn-tpx-email-3
description: Email 3 of 7 to David Zahn at TPx — soft touch
---

Send an email to David Zahn at TPx using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: dzahn@tpx.com and press Tab
5. Click the Subject field and enter exactly: I'll keep this short
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

I've sent a couple of notes and haven't heard back. No worries.

One pattern I see at companies running infrastructure at your scale: the pain doesn't always show up in the big refresh cycles. It's the gaps. A transceiver that's four weeks out. A maintenance contract that auto-renews at OEM rates because nobody had time to shop it. A line card that's EOL but still carrying production traffic.

If the timing is off, just say the word and I'll follow up later in the year. If any of that sounds familiar, I'd enjoy the conversation.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.