---
name: obsidian-vault-sync
description: Daily sync check of OSI-Brain Obsidian vault snapshot
---

Check whether the OSI-Brain vault snapshot is fresh, and notify Brian if it needs to be refreshed.

## Objective
Verify that Memory/vault_sync.md in the OSI-Brain vault is up to date (written today). If it's stale, remind Brian to run the sync script manually.

## Steps

1. Use mcp__Claude_in_Chrome__tabs_context_mcp to get a browser tab (create one if needed).
2. Navigate to http://127.0.0.1:27123/ to confirm Obsidian is open and the Local REST API is running. If the API is unreachable, stop — Obsidian is closed, nothing to do.
3. Read the first 300 characters of Memory/vault_sync.md to check the timestamp:
   ```javascript
   (async () => {
     const K = 'a1a68a2680b43aa49c05f36041c7746c16144a1f5cd70305d4ec7986ac7c8b42';
     const r = await fetch('http://127.0.0.1:27123/vault/Memory/vault_sync.md', {
       headers: { 'Authorization': 'Bearer ' + K }
     });
     const text = await r.text();
     return text.substring(0, 300);
   })()
   ```
4. Parse the date from the "Generated:" line in the snapshot header.
5. If the snapshot was generated today — do nothing. Log: "Vault snapshot is current."
6. If the snapshot is older than 24 hours — notify Brian in the next Cowork session:
   "Your vault snapshot is out of date. Open PowerShell and run:
   cd 'C:\Users\MINI OSI RIG\OneDrive - OSI Hardware\Documents\Claude\Projects\Mini Chamber\OSI-Brain'
   python sync_vault.py"

## Vault API
- Base URL: http://127.0.0.1:27123
- API Key: a1a68a2680b43aa49c05f36041c7746c16144a1f5cd70305d4ec7986ac7c8b42
- Note: the bash sandbox cannot reach Windows localhost — use Chrome javascript tool for all API calls.

## Success criteria
Snapshot timestamp matches today's date, OR Brian has been notified it needs a refresh.