---
name: johnreed-robbins-fortcollins-email-2
description: Email 2 of 7 — John Reed Robbins III, Fort Collins Connexion (DWDM/Smartoptics angle)
---

Send an email to John Reed Robbins III at Fort Collins Connexion using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: jrrobbins@fcgov.com and press Tab
5. Click the Subject field and enter exactly: RE: Connexion's Larimer County buildout
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

Hi John Reed,

One more angle, given your Nokia background — open line DWDM.

We're the largest global Smartoptics partner. Their platform runs 30 to 50% below Nokia and Ciena pricing, significantly less rack space and power, and no licensing headaches. A few municipal and rural fiber teams have been using them to fill capacity without going back to the OEM for every increment.

If DWDM is part of the Connexion architecture or roadmap, worth a conversation.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.