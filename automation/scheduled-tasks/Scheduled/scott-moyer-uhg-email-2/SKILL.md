---
name: scott-moyer-uhg-email-2
description: Email 2 — Scott Moyer (UHG) — RECOVERY fire 4/22 11:15 PT (original Tue Apr 21 missed)
---

Send an email to Scott Moyer at UnitedHealth Group / Optum using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: scott.moyer@optum.com and press Tab
5. Click the Subject field and enter exactly: the 800G question nobody's asking you
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

Different angle this time. We move a lot of optics through Optum style environments. OSI is the largest global Smartoptics partner, and we code transceivers in house for 40 plus platforms including every Cisco, Arista, Juniper, and Nokia box your teams run. 1G to 400G today, 800G in stock right now if you are planning ahead. Same day fulfillment as a rule, not an exception.

Where it matters for a network this size: we will certify optics inside your fabric before you pay for them. If they do not work, we do not ship. Zero risk trial.

If you have a DWDM refresh, a dark fiber build, or a lease cost problem staring at you, worth a conversation.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.