---
name: bill-mcclendon-westlake-email-2
description: Email 2 — Bill McClendon (Westlake) — RECOVERY fire 4/22 11:03 PT (original Tue Apr 21 missed)
---

Send an email to Bill McClendon at Westlake Corporation using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: wmcclendon@westlake.com and press Tab
5. Click the Subject field and enter exactly: RE: Bill, been a while
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

Hi Bill,

A separate thought on the Aruba side. If Westlake is mid-rollout or still sourcing hardware, we keep Aruba gear in stock and can move faster than most distribution channels. We also supply compatible optics and accessories for the switching that typically goes alongside a wireless buildout.

Not pushing. Just want to make sure you know OSI is in the mix if you need a fast turnaround on anything.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.