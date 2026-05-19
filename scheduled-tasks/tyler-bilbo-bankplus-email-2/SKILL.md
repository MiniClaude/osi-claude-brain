---
name: tyler-bilbo-bankplus-email-2
description: Send Email 2 to Tyler Bilbo at BankPlus — optics angle — SENT MANUALLY 4/20 12:00 PM PT after silent fire-no-send
---

Send an email to Tyler Bilbo at BankPlus using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: tylerbilbo@bankplus.net and press Tab
5. Click the Subject field and enter exactly: The other thing network engineers at banks usually care about
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

Tyler,

Different angle this week.

Beyond maintenance contracts, a lot of network engineers at banks are also dealing with transceiver costs. Every switch port, every uplink, every SAN connection — the OEM charges list price on optics even when the hardware underneath it has been fully depreciated.

We supply SFPs, QSFPs, and other optical modules coded for Cisco and other platforms at 50 to 70 percent off OEM pricing. Fully tested, compatible, and we certify them in your environment before anything goes on the shelf.

If that's a line item that shows up in your budget, probably worth 15 minutes.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.