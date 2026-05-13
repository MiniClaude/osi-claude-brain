---
name: neal-hickey-hexion-email-3
description: Send Email 3 to Neal Hickey (Hexion Inc) - 7-email tracked sequence
---

Send Email 3 of the Neal Hickey (Hexion) sequence via Outlook in Chrome with BCC tracking.

To: neal.hickey@hexion.com
BCC: bc@osihardware.com, 21878985@bcc.hubspot.com
Subject: One more thought

Steps:
1. Get tab via tabs_context_mcp (createIfEmpty true). Navigate to https://outlook.office.com/mail/. Wait 3s, screenshot.
2. If sign-in screen appears, STOP. Notify Brian and create a todo "Outlook session expired — resend Neal Hickey Email 3 manually". Do not proceed.
3. Use find tool with query "New mail button" and click it. Wait 2s.
4. Click To field at coordinate (900, 158). Type: neal.hickey@hexion.com
5. Click Bcc field at coordinate (900, 207). Type: bc@osihardware.com, 21878985@bcc.hubspot.com
6. Click Subject field at coordinate (900, 235). Type: One more thought
7. Click in body area at coordinate (900, 300). Press Ctrl+Home to position cursor at the very TOP of the body — ABOVE Outlook's auto-signature.
8. CRITICAL: Do NOT use Ctrl+A+Delete. Do NOT type your own signature. Outlook's auto-signature is already in the body and will appear correctly below your typed body.
9. Type the body exactly as written below — body only, no signature:

Neal,

One thing I've noticed working with operations teams at manufacturing companies like yours—when equipment hits that 8-10 year mark, the support costs usually spike before they level off.

Not trying to push anything on you. But if you're looking at hardware spend projections for next year, TPM could cut that line item in half. And no more waiting for OEM support on legacy equipment.

Worth a conversation if you're in planning mode.

Brian

10. Use find tool with query "Send button to send the current email message" and click it. Wait 4s.
11. Click Sent Items in the left sidebar (around coordinate 82, 373). Wait 2s. Screenshot.
12. Verify the email to neal.hickey@hexion.com with subject "One more thought" appears in Sent Items, sent within last 5 min. If not found, report failure.
13. Confirm and report.