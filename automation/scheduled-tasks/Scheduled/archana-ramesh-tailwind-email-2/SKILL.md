---
name: archana-ramesh-tailwind-email-2
description: Email 2 — Archana Ramesh (TailWind) — RECOVERY test-fire 4/22 11:03:30 PT
---

Send an email to Archana Ramesh at TailWind Voice and Data using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: aramesh@tailwindvoiceanddata.com and press Tab
5. Click the Subject field and enter exactly: When your usual channel is out of stock
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

Hey Archana,

Didn't hear back so I'll try a different angle.

If TailWind is deploying structured cabling or connectivity solutions for clients, optics are likely part of the picture. We code transceivers for 40+ platforms: Cisco, Juniper, Aruba, Dell and others. We carry everything from 1G to 400G, and we do custom builds that OEMs won't make: extended distances, dual coded twinax, DWDM coded as standard SFPs when the platform doesn't natively accept them.

The point isn't to replace your current sources. It's to have someone who can fill gaps fast when your usual channel comes up short.

If that's ever a problem for your team, worth a quick conversation.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.