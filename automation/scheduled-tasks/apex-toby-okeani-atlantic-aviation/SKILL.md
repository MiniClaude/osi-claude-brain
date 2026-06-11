---
name: apex-toby-okeani-atlantic-aviation
description: Send congrats email to Toby Okeani at Atlantic Aviation (procurement)
---

Send an email via Outlook web (Chrome automation) to toby.okeani@atlanticaviation.com.

Subject: Congrats on the Atlantic Aviation role

Body:
Toby,

Congrats on the Mgr Procurement seat at Atlantic Aviation. Different industry, but procurement problems tend to rhyme.

If IT hardware shows up in your scope (networking, servers, storage, memory, optics), OSI gives you a privately-held alternative to the big OEMs, usually 50-80% under list with the same components. Happy to be a reference quote source even if we never transact.

Good luck in the new role.

Brian

Steps:
1. Get Chrome tab context (tabs_context_mcp).
2. Navigate active tab to https://outlook.office.com/mail/deeplink/compose
3. Wait 3 seconds.
4. Click the To field at coordinate (400, 181), type toby.okeani@atlanticaviation.com, press Enter.
5. Click subject at (400, 293), type subject.
6. Use javascript_tool to find div[aria-label="Message body"][contenteditable="true"] and set innerHTML with the body above wrapped in div tags with br spacing.
7. Click Send button at (54, 138).
8. Verify "You may now close this window" appears.
9. Log a note on HubSpot contact 464878 (Toby Okeani) documenting the send.