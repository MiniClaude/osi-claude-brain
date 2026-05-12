---
name: obsidian-vault
description: >
  Connect to Brian's Obsidian vault (osi-brian) via the Local REST API. Use this skill whenever
  Brian says "check my vault", "find my notes on", "what do I have on", "search my obsidian",
  "load my vault", "pull up my notes about", "what did I note about", "do I have anything on",
  "check my knowledge base", or any variation of wanting to retrieve or search information in
  Obsidian. Also trigger automatically when working on a task where vault context would clearly
  help — writing outreach for an account, prepping for a meeting, or researching a topic.
  Always run this skill before telling Brian "I don't have context on that."
  Additionally: whenever Brian saves something to Clippings in Obsidian, use this skill to sync
  new clippings to Cowork auto-memory so they're recalled in future sessions without querying
  Obsidian again.
---

# Obsidian Vault Skill

Brian's Obsidian vault (osi-brian) is connected via the Local REST API. This skill lets you
search, read, and browse notes — and keeps Cowork memory in sync with new Clippings.

## Connection Details

- **Base URL**: `http://127.0.0.1:27123`
- **API Key**: `a1a68a2680b43aa49c05f36041c7746c16144a1f5cd70305d4ec7986ac7c8b42`
- **Method**: All API calls go through `mcp__Claude_in_Chrome__javascript_tool` (browser fetch)
- **Important**: The bash sandbox cannot reach Brian's localhost — only Chrome browser tools can.

---

## On Every Skill Invocation: Auto-Load Core Notes

At the start of every skill run, automatically load these three sources into context. They're Brian's
personal and work reference material and should inform everything you do in the session.

### 1. Brian's Kitchen
Personal recipes, cooking notes, food knowledge.
```javascript
(async () => {
  const K = 'a1a68a2680b43aa49c05f36041c7746c16144a1f5cd70305d4ec7986ac7c8b42';
  const r = await fetch("http://127.0.0.1:27123/vault/Brian's%20Kitchen.md", {
    headers: { 'Authorization': 'Bearer ' + K }
  });
  return await r.text();
})()
```

### 2. Mini Prospecting
Brian's personal prospecting notes, targets, and mini outreach tracker.
```javascript
(async () => {
  const K = 'a1a68a2680b43aa49c05f36041c7746c16144a1f5cd70305d4ec7986ac7c8b42';
  const r = await fetch('http://127.0.0.1:27123/vault/Mini%20Prospecting.md', {
    headers: { 'Authorization': 'Bearer ' + K }
  });
  return await r.text();
})()
```

### 3. Knowledge Folder (all files)
OSI product knowledge, ICP, sales playbook, and reference material. Read all files:
`ICP.md`, `OSI-Overview.md`, `Products-Hardware.md`, `Products-Optics.md`,
`Products-Systain.md`, `Sales-Playbook.md`

```javascript
(async () => {
  const K = 'a1a68a2680b43aa49c05f36041c7746c16144a1f5cd70305d4ec7986ac7c8b42';
  const files = ['ICP.md','OSI-Overview.md','Products-Hardware.md','Products-Optics.md','Products-Systain.md','Sales-Playbook.md'];
  const results = {};
  for (const f of files) {
    const r = await fetch('http://127.0.0.1:27123/vault/Knowledge/' + f, {
      headers: { 'Authorization': 'Bearer ' + K }
    });
    results[f] = (await r.text()).substring(0, 2000);
  }
  return JSON.stringify(results);
})()
```

If any of these files are empty, skip them silently — Brian will fill them in over time.

---

## Vault Verification

Before doing any work, confirm the correct vault is open:

```javascript
(async () => {
  const K = 'a1a68a2680b43aa49c05f36041c7746c16144a1f5cd70305d4ec7986ac7c8b42';
  const r = await fetch('http://127.0.0.1:27123/vault/', {
    headers: { 'Authorization': 'Bearer ' + K }
  });
  const data = await r.json();
  const files = data.files || [];
  const expected = ['Accounts/', 'Deals/', 'Knowledge/', 'Meeting-Notes/'];
  const isOsiBrian = expected.every(f => files.includes(f));
  return JSON.stringify({ isOsiBrian, files });
})()
```

If `isOsiBrian` is false, stop and tell Brian: "It looks like a different vault is open in Obsidian.
Please switch to your **osi-brian** vault and try again."

---

## Vault Structure

| Folder | Contents |
|---|---|
| `Accounts/` | Customer and prospect account notes |
| `Contacts/` | Individual contact notes |
| `Deals/` | Active and past deal notes |
| `Knowledge/` | OSI product knowledge, ICP, sales playbook |
| `Meeting-Notes/` | Call and meeting summaries |
| `Research/` | Deep-dives on companies, tech, markets |
| `Outreach/` | Outreach notes and drafts |
| `Memory/` | Personal reference and reminders |
| `Clippings/` | Saved articles — recipes, vendor research, web content |
| `CustomerQuotes/` | Quotes from customer conversations |
| `Templates/` | Note templates |
| `Brian's Kitchen.md` | Personal recipe and cooking notes (root level) |
| `Mini Prospecting.md` | Personal prospecting tracker (root level) |

---

## Search the Vault

Use when Brian asks about any topic, account, contact, or concept.

> ⚠️ Search requires **POST** method with the query as a URL parameter.

```javascript
(async () => {
  const K = 'a1a68a2680b43aa49c05f36041c7746c16144a1f5cd70305d4ec7986ac7c8b42';
  const query = "YOUR_SEARCH_TERM";
  const r = await fetch(`http://127.0.0.1:27123/search/simple/?query=${encodeURIComponent(query)}&contextLength=200`, {
    method: 'POST',
    headers: { 'Authorization': 'Bearer ' + K }
  });
  const data = await r.json();
  return JSON.stringify(data.map(h => ({ file: h.filename, context: h.matches?.[0]?.context }))).substring(0, 3000);
})()
```

## Read a Specific Note

```javascript
(async () => {
  const K = 'a1a68a2680b43aa49c05f36041c7746c16144a1f5cd70305d4ec7986ac7c8b42';
  const path = 'Folder/Note-Name.md'; // adjust path — do NOT encode slashes
  const r = await fetch('http://127.0.0.1:27123/vault/' + path, {
    headers: { 'Authorization': 'Bearer ' + K }
  });
  return (await r.text()).substring(0, 4000);
})()
```

> ⚠️ Do NOT use `encodeURIComponent` on the full path — it will encode the `/` and break the request.
> Only encode spaces: replace spaces with `%20` manually if needed.

## List a Folder

```javascript
(async () => {
  const K = 'a1a68a2680b43aa49c05f36041c7746c16144a1f5cd70305d4ec7986ac7c8b42';
  const r = await fetch('http://127.0.0.1:27123/vault/Folder/', {
    headers: { 'Authorization': 'Bearer ' + K }
  });
  return JSON.stringify(await r.json());
})()
```

---

## Clippings → Auto-Memory Sync

When Brian saves new content to the Clippings folder, sync it to Cowork auto-memory so future
sessions can recall it without querying Obsidian. Run this whenever Brian mentions adding a
clipping, or at the start of a session if it hasn't been run recently.

### Step 1: Get current Clippings list
```javascript
(async () => {
  const K = 'a1a68a2680b43aa49c05f36041c7746c16144a1f5cd70305d4ec7986ac7c8b42';
  const r = await fetch('http://127.0.0.1:27123/vault/Clippings/', {
    headers: { 'Authorization': 'Bearer ' + K }
  });
  return JSON.stringify(await r.json());
})()
```

### Step 2: Check which clippings are already in auto-memory
Read the memory index at `/sessions/dazzling-awesome-euler/mnt/.auto-memory/MEMORY.md` to see
what clippings have already been synced. Look for entries with `[clipping]` in the description.

### Step 3: For each new clipping, read it and save to auto-memory
For each file in Clippings not yet in memory, read its content and write a memory file:

- Save to: `/sessions/dazzling-awesome-euler/mnt/.auto-memory/clipping_<slug>.md`
- Use this frontmatter format:
```markdown
---
name: <title of the clipping>
description: [clipping] <one-line summary of what it contains>
type: reference
---

<key content from the clipping — summarized to 200-300 words, not verbatim>
Source: <original URL if present in the note>
```

Then add a pointer line to `MEMORY.md`:
```
- [<title>](clipping_<slug>.md) — [clipping] <one-line hook>
```

### Step 4: Confirm sync
Tell Brian which new clippings were added to memory, e.g.:
"Synced 3 new clippings to memory: Sourdough Bread, Cinnamon Roll Recipe, Juniper Pathfinder Tool."

---

## Error Handling

- **Fetch fails / connection refused**: Obsidian is probably closed. Tell Brian: "Make sure Obsidian is open with the Local REST API plugin enabled."
- **401 Unauthorized**: API key was regenerated. Ask Brian for the new key.
- **Empty file**: Skip silently, note that the file exists but has no content yet.
- **[BLOCKED] from javascript tool**: The file content may contain tracking URLs or cookie text that trips the security filter. Try navigating Chrome directly to the file URL and using `get_page_text` instead.

---

## Smart Triggering

Don't wait to be asked. If Brian is:
- Writing outreach for a company → search `Accounts/` for that company first
- Prepping for a meeting → check `Meeting-Notes/` for prior calls
- Asking about a contact → search `Contacts/` by name
- Researching a product or vendor → check `Knowledge/` and `Research/` before the web
- Asking about a recipe → check `Brian's Kitchen.md` and `Clippings/`
- Working on prospecting → load `Mini Prospecting.md`

Lead with vault context. It's faster and more personal than generic research.
