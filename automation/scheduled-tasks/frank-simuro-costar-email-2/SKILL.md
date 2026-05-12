---
name: frank-simuro-costar-email-2
description: CoStar sequence — Frank Simuro Email 2 optics/800G angle
---

Send an email to Frank Simuro at CoStar Group using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: fsimuro@costargroup.com and press Tab
5. Click the Subject field and enter exactly: 800G and your AI infrastructure
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

Frank,

Different angle from my last note.

You're deep into AI deployment across CoStar's platforms. That puts real pressure on internal connectivity, especially if you're moving large data sets or building out capacity for the new campus.

We're the largest global partner for Smartoptics and carry 800G transponders in stock. We also code transceivers in-house for 40-plus OEM platforms, including custom DWDM builds the OEMs themselves won't make. If there's a connectivity project in the pipeline, worth comparing what we can do against what you've been quoted.

If optics aren't on your radar right now, no worries.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.