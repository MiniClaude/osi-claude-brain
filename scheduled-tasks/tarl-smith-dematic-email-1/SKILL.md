---
name: tarl-smith-dematic-email-1
description: Email 1 of 7 to Tarl Smith at Dematic — SENT MANUALLY Apr 16, disabled
---

Send an email to Tarl Smith at Dematic using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: tarl.smith@dematic.com and press Tab
5. Click the Subject field and enter exactly: What your Azure dashboard doesn't show
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

Tarl,

Most FinOps work starts and stops at the cloud console. But for companies running hybrid environments like Dematic, a significant piece of total infrastructure spend sits on-prem: networking gear, servers, and maintenance contracts that don't show up in your Azure cost reports but absolutely affect the full picture.

OSI Global works with IT and cloud teams at large enterprises to cut that on-prem layer by 50 to 80%, through third-party maintenance on EOL gear, hardware lifecycle extension, and fast fulfillment when something fails unexpectedly.

Worth 15 minutes to see if there's overlap with what you're already working on?

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.