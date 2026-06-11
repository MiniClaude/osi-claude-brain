---
name: lenny-cordisco-fusion-email-2
description: Email 2 to Lenny Cordisco at Fusion Worldwide — hardware sourcing angle — SENT MANUALLY 4/20 12:04 PM PT after silent fire-no-send
---

Send an email to Lenny Cordisco at Fusion Worldwide using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: lcordisco@fusionww.com and press Tab
5. Click the Subject field and enter exactly: The sourcing side of the same problem
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

Lenny,

Different angle from my last note.

Fusion's growth pace means you're probably adding hardware faster than any OEM can prioritize your account. Lead times are unpredictable, allocation is tight, and the list price doesn't move.

We carry new and refurbished Cisco, Juniper, HPE, and Dell across all lifecycle stages. Ready inventory means we can usually turn around orders that would take weeks through normal channels. If Fusion has had any lead time issues in the past year, it's worth knowing we exist.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.