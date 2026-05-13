---
name: mike-kleinman-costar-email-1
description: CoStar sequence — Mike Kleinman Email 1 warm re-engagement
---

Send an email to Mike Kleinman at CoStar Group using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: mkleinman@costar.com and press Tab
5. Click the Subject field and enter exactly: Congrats on the manager role, Mike
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

Mike,

Saw you moved into the Manager of Infrastructure Engineering role. Congratulations. Managing a team is a different job than doing the work yourself, and CoStar's infrastructure footprint is not exactly small right now with Richmond coming online in May.

It's Brian at OSI Global. We've talked before, but I wanted to reach back out now that you're in a position where vendor relationships land differently.

A lot of infrastructure managers I work with are still paying OEM list price for DIMMs and server memory out of habit. We cut memory and server hardware costs by 80 to 90 percent versus OEM pricing. Same performance, fully validated, sourced from Samsung, Micron, and Hynix. We've shipped over 6,000 DIMMs same-day when teams needed to move fast.

Worth 15 minutes to catch up?

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.