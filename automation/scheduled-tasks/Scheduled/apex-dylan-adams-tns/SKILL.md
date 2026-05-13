---
name: apex-dylan-adams-tns
description: Send congrats email to Dylan Adams at TNS
---

Send an email via Outlook web (Chrome automation) to dadams@tnsi.com.

Subject: New role at TNS

Body:
Dylan,

Saw you landed at TNS. Congrats on the move.

TNS has a serious network footprint, and a lot of what OSI does (optics, transceivers, Smartoptics open line systems, DIMMs) lines up with that world. If you hit a lead-time wall or an OEM tries to force a refresh, I'd rather be the first call than the third.

Good to reconnect.

Brian

Steps:
1. Get Chrome tab context (tabs_context_mcp).
2. Navigate active tab to https://outlook.office.com/mail/deeplink/compose
3. Wait 3 seconds.
4. Click the To field at coordinate (400, 181), type dadams@tnsi.com, press Enter.
5. Click subject at (400, 293), type subject.
6. Use javascript_tool to find div[aria-label="Message body"][contenteditable="true"] and set innerHTML with the body above wrapped in div tags with br spacing.
7. Click Send button at (54, 138).
8. Verify "You may now close this window" appears.
9. Log a note on HubSpot contact 464726 (Dylan Adams) documenting the send.