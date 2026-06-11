---
name: apex-lawrence-broadnax-balyasny
description: Send congrats email to Lawrence Broadnax at Balyasny Asset Management
---

Send an email via Outlook web (Chrome automation) to lbroadnax@bamfunds.com.

Subject: Saw the move to Balyasny

Body:
Lawrence,

Congrats on the Balyasny move. Hedge fund IT is a different animal than clearing, but the network engineering fundamentals travel.

Quick note: we do a lot of work with financial services shops on optics (1G to 400G including DWDM), memory, and hardware lifecycle extension, usually 50-80% under list. If Balyasny has any of those thorns, I'd like to be on your short list.

No pitch, just putting my name in front of you at the new spot.

Brian

Steps:
1. Get Chrome tab context (tabs_context_mcp).
2. Navigate active tab to https://outlook.office.com/mail/deeplink/compose
3. Wait 3 seconds.
4. Click the To field at coordinate (400, 181), type lbroadnax@bamfunds.com, press Enter.
5. Click subject at (400, 293), type subject.
6. Use javascript_tool to find div[aria-label="Message body"][contenteditable="true"] and set innerHTML with the body above wrapped in div tags with br spacing.
7. Click Send button at (54, 138).
8. Verify "You may now close this window" appears.
9. Log a note on HubSpot contact 464348 (Lawrence Broadnax) documenting the send.