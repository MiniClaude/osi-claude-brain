---
name: nidal-naser-sandc-email-2
description: Email 2 — Nidal Naser (S&C) — RECOVERY fire 4/22 11:12 PT (original Tue Apr 21 missed)
---

Send an email to Nidal Naser at S&C Electric Company using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: nidal.naser@sandc.com and press Tab
5. Click the Subject field and enter exactly: RE: after 23 years at Nokia
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

Hi Nidal,

A different angle from my last note. Optics are the other place I see manufacturers routinely overpay.

If S&C is running Cisco or Juniper across the global sites, there's a good chance you're paying OEM rates for transceivers you don't need to. We code them in house for 40 plus platforms, custom builds included, at a fraction of list price. Same specs, same performance, works in your existing fabric.

Worth a look if optics show up anywhere in your plans for this year.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.