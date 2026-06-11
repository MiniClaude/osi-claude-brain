---
name: brett-colvin-ogden-clinic-email-6
description: Email 6 of 7 — Brett Colvin, Ogden Clinic — Pattern interrupt
---

Send an email to Brett Colvin at Ogden Clinic using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: brett.colvin@ogdenclinic.com and press Tab
5. Click the Subject field and enter exactly: Are you running any EOL Cisco gear right now?
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

Brett,

Direct question: are you running any Cisco or HP gear that's hit end of life?

If yes, there's a good chance we can help you keep it covered at half the OEM maintenance cost, or replace it at 50-80% off list. If no, I'll stop reaching out.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.