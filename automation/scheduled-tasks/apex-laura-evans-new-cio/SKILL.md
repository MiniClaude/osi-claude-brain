---
name: apex-laura-evans-new-cio
description: Send congrats email to Laura Evans at Post Acute Analytics (new CIO)
---

Send an email via Outlook web (Chrome automation) to levans@paanalytics.com.

Subject: Congrats on the CIO seat

Body:
Laura,

Saw you're now CIO at Post Acute Analytics. Congrats, well deserved.

Different company, same offer: if you're standing up or maturing infrastructure at PAA and want a neutral party to pressure-test OEM quotes, extend hardware lifecycles, or pull in TPM instead of renewing SmartNet, my team is set up for exactly that. We've been doing it 16 years and we don't carry quota pressure because OSI is privately held.

Happy to be a resource whether it leads anywhere or not. Good to see you in the CIO chair.

Brian

Steps:
1. Get Chrome tab context (tabs_context_mcp).
2. Navigate active tab to https://outlook.office.com/mail/deeplink/compose
3. Wait 3 seconds.
4. Click the To field at coordinate (400, 181), type levans@paanalytics.com, press Enter.
5. Click subject at (400, 293), type subject.
6. Use javascript_tool to find div[aria-label="Message body"][contenteditable="true"] and set innerHTML with the body above wrapped in div tags with br spacing.
7. Click Send button at (54, 138).
8. Verify "You may now close this window" appears.
9. Log a note on HubSpot contact 464580 (Laura Evans) documenting the send, and also check if a new contact record for Post Acute Analytics needs to be created.