---
name: scott-moyer-uhg-email-3
description: Email 3 of 7 (soft touch) to Scott Moyer at UHG/Optum
---

Send an email to Scott Moyer at UnitedHealth Group / Optum using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: scott.moyer@optum.com and press Tab
5. Click the Subject field and enter exactly: UHG probably overpays by a factor of two
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

Quiet on my end and likely yours. Network managers at health systems of any real size get 30 cold emails a day, so I expect silence unless I hit a nerve.

The pattern I see over and over with teams your size: a ton of capex gets spent refreshing gear that still has years of runway, and a ton of opex gets burned on OEM support that does not scale with headcount cuts. Most teams do not know there is a different way until someone shows them the math.

If timing is off, just say the word and I'll close the loop.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.