---
name: brian-hudson-fortcollins-email-2
description: Email 2 — Brian Hudson (Fort Collins) — SENT MANUALLY 4/22 11:38 AM PT
---

Send an email to Brian Hudson at City of Fort Collins using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: brhudson@fcgov.com and press Tab
5. Click the Subject field and enter exactly: The maintenance cost on a growing network
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

Hey Brian,

Different angle from my last note — this one's about the gear you already have.

As Connexion's network grows, so does the OEM maintenance bill. We provide third-party maintenance through Systain — 24/7/365 TAC coverage, next business day hardware replacement, and support for EOL equipment the OEM stopped covering. For a municipal network managing costs carefully, the savings versus OEM typically land around 50%.

If you have gear coming up on support renewal or equipment the OEM has already declared End of Life, worth a conversation.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.