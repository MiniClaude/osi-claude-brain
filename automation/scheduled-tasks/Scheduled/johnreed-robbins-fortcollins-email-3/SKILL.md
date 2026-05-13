---
name: johnreed-robbins-fortcollins-email-3
description: Email 3 of 7 — John Reed Robbins III, Fort Collins Connexion (soft touch)
---

Send an email to John Reed Robbins III at Fort Collins Connexion using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: jrrobbins@fcgov.com and press Tab
5. Click the Subject field and enter exactly: Still here when the timing is right
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

Two notes and nothing back — completely get it. Building fiber into mountain communities isn't exactly a job with a lot of slack in the schedule.

I keep seeing the same thing at municipal broadband networks in active expansion: optics procurement becomes a scramble once the buildout pace outpaces the OEM supply chain. I'd rather be a resource before that point than after.

If the timing isn't right, say the word and I'll leave you alone.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.