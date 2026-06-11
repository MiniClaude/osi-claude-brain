---
name: nidal-naser-sandc-email-3
description: Email 3 to Nidal Naser at S&C Electric — soft touch
---

Send an email to Nidal Naser at S&C Electric Company using Outlook. Follow these steps exactly:

1. Navigate to https://outlook.office.com in Chrome
2. If a login screen appears, stop and notify the user
3. Click New mail
4. In the To field, enter: nidal.naser@sandc.com and press Tab
5. Click the Subject field and enter exactly: most network managers wait too long
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

Haven't heard back, which usually means timing is off or the inbox got full.

What I see a lot with network managers at manufacturers is that the TPM and optics conversation gets pushed aside until there's a contract renewal or a failure event. By then the OEM is already quoting renewal rates and the leverage is gone.

If now isn't the right time, just say the word. Happy to circle back in a few months.

8. Click Send
9. Confirm the email was sent and report back

Do not modify the email body in any way.