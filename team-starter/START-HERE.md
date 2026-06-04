# START HERE

Hey. Andy sent you this folder so you can set up your own version of his "Claude Brain" on your laptop. This is the system he uses for LinkedIn prospecting, outreach sequences, HubSpot task drafting, and every other sales workflow he's wired up.

Once it's set up, your Claude (via Cowork) will know who you are, how OSI sells, and will have all of Andy's skills ready to run for YOU, with your HubSpot owner ID and your name on everything.

Setup takes about 20 minutes. Your Claude will do most of the work. You mostly follow prompts and click things.

---

## What you're about to do (plain English)

1. Put this folder on your computer at `C:\Claude-Brain\`.
2. Open Cowork and point it at that folder.
3. In the chat, paste: **"Read START-HERE.md and set me up."**
4. Claude will walk you through the rest.

That's it. You can stop reading now. The section below this divider is for Claude to execute, not for you.

---

## 🤖 INSTRUCTIONS FOR CLAUDE (Cowork session, new teammate onboarding)

You are helping a new OSI Global teammate set up their personal Claude Brain for the first time. They have never used Git before. They are a salesperson, not a technical person. Be patient, give them copy-pasteable commands, and handle errors as they come up.

**DO NOT skip ahead. Run each phase in order. Wait for user confirmation between phases.**

### Phase 0: Gather their info

Before anything else, ask the teammate for these five pieces of information. Ask them all at once. Store them for use across the whole setup. These will be used to fill in the `[MY_*]` placeholders that appear throughout CLAUDE.md and every skill.

1. **Full name** (e.g., `Mark Metz`)
2. **First name** (e.g., `Mark`)
3. **OSI email** (e.g., `mark@osiglobal.com`)
4. **HubSpot Owner ID**, if they don't know it, tell them: "In HubSpot, click your avatar top right, then Profile & Preferences. The Owner ID is a 9-digit number. If you can't find it, Teams Andy and ask."
5. **GitHub username**, if they don't have a GitHub account yet, tell them to go to github.com right now and create one with their personal email (not OSI email, so the account survives a job change). Wait for them to confirm it's done.

Also compute a sixth value: the "spoken email" for voicemails. Take their OSI email and expand it into spoken form. Example: `mark@osiglobal.com` becomes `mark at osiglobal dot com`. Confirm this with them before continuing.

### Phase 1: Verify they have Git installed

Ask them to open a program called **Git Bash** from their Start menu. If it's there, they're good. Have them type `git --version` in Git Bash and paste the output to confirm.

If Git Bash is NOT installed:
- Tell them to go to https://git-scm.com and click Download for Windows.
- Tell them to run the installer, click Next through every screen (defaults are fine), and when done, open Git Bash from the Start menu.
- Have them paste `git --version` output when ready.

Once Git Bash is confirmed, have them run these two commands in Git Bash, substituting their actual info:

```
git config --global user.email "their-actual-email"
git config --global user.name "Their Full Name"
```

Recommend the email match whatever they used on GitHub.

### Phase 2: Verify the folder is in the right place

Ask the teammate to confirm the Claude Brain folder is at exactly `C:\Claude-Brain\`. It MUST be at the root of C:. Not in Documents, not in Downloads, not inside OneDrive. Exactly `C:\Claude-Brain\`.

Have them open File Explorer, navigate to `C:\Claude-Brain\`, and confirm they see folders named `accounts`, `inbox`, `knowledge`, `outreach`, `people`, `sessions`, `skills`, and files named `CLAUDE.md` and `START-HERE.md`.

If the folder is somewhere else (Downloads, Desktop, etc.), have them cut and paste it to `C:\Claude-Brain\`.

If Cowork is not yet pointing at `C:\Claude-Brain\`, ask them to re-select the folder in Cowork. You won't be able to read the files until Cowork is pointed at the right place.

### Phase 3: Fill in their placeholders across all files

Use your file editing tools to do find-and-replace across every `.md` file in their `C:\Claude-Brain\` folder. Use the values you collected in Phase 0. Replace these tokens EXACTLY (they include the brackets):

| Token | Replace with |
|---|---|
| `[MY_FULL_NAME]` | the teammate's full name |
| `[MY_FIRST_NAME]` | their first name |
| `[MY_EMAIL]` | their OSI email |
| `[MY_EMAIL_SPOKEN]` | their email in spoken form |
| `[MY_HUBSPOT_OWNER_ID]` | their Owner ID |
| `[MY_GITHUB_USERNAME]` | their GitHub username |

After replacing, run a final check by grepping for `[MY_` across the folder. Expected: zero results.

Tell them when it's done: "Your CLAUDE.md and skill files are now personalized to you."

### Phase 4: Create their private GitHub repo

Walk them through this in their browser:

1. Sign in to github.com.
2. Click the green "New" button (or + menu top right → New repository).
3. Repository name: `Claude-Brain`
4. Visibility: **Private**. This is critical. Confirm with them it's set to Private.
5. Do NOT check any of "Add a README", "Add .gitignore", or "Add a license". All three should stay OFF.
6. Click Create repository.
7. Leave the browser on the page that appears next. They'll grab the URL in Phase 5.

### Phase 5: Initialize Git, commit, push

In their Git Bash, guide them through these commands one at a time. Have them paste each command's output back to you so you can catch errors early.

```
cd /c/Claude-Brain
git init
git add .
git commit -m "first commit"
git branch -M main
```

If `git commit` fails with "Please tell me who you are", go back to Phase 1 and re-run the config commands, then retry.

Get the remote URL. Ask the teammate for their GitHub username (you already have it from Phase 0). The URL is `https://github.com/THEIR-USERNAME/Claude-Brain.git`.

```
git remote add origin https://github.com/THEIR-USERNAME/Claude-Brain.git
git push -u origin main
```

### Phase 6: Handle the authentication failure (expected)

The `git push` will ask for a username and password. GitHub does not accept the normal password, they need a Personal Access Token. Walk them through:

1. In their browser, go to https://github.com/settings/tokens
2. Click Generate new token → Generate new token (classic)
3. Note: `Claude-Brain laptop`
4. Expiration: 1 year (or No expiration)
5. Scopes: check the `repo` box only (it's the top one, gets all sub-boxes)
6. Scroll down, click Generate token
7. **COPY THE TOKEN IMMEDIATELY.** It starts with `ghp_` or `github_pat_`. Tell them to paste it into a Notepad window temporarily because GitHub will not show it again.

Back in Git Bash:
- Re-run `git push -u origin main`
- When prompted for Username: their GitHub username.
- When prompted for Password: paste the token (right-click in Git Bash to paste, nothing will appear as they type, that's normal). Hit Enter.

If it succeeds, they'll see `[new branch] main -> main`. Have them refresh their GitHub repo page to confirm files are there.

Tell them to close the Notepad with the token. They don't need to save it.

### Phase 7: Install the skills in Cowork

The folder has skill SOURCES in `skills/` but no packaged `.skill` files (Andy stripped those so they wouldn't ship with his HubSpot IDs).

Now that placeholders are filled in with their info, you need to re-package each skill folder into a `.skill` file and present them for installation.

For each folder under `C:\Claude-Brain\skills\`:
1. Run the packaging tool on the folder.
2. Output the resulting `.skill` file.
3. Use `present_files` to surface the `.skill` for one-click install.
4. Ask the teammate to click "Save skill" on each card.

If you don't have access to the packaging tool, instead tell the teammate: "I can't package the skill files from here. Teams Andy and ask him to send you pre-packaged `.skill` files personalized for you, OR ask him to help you package them in a follow-up Cowork session." For now, the SKILL.md sources are in place and can be read as context even without being packaged skills.

### Phase 8: Teach them the daily habit

Tell them, out loud and clearly:

> Every morning when you open Cowork, first thing: open Git Bash, type `cd /c/Claude-Brain`, then `git pull`. That grabs any updates. Every time you finish a session, in Git Bash: `git add .`, then `git commit -m "what I did today"`, then `git push`. That backs everything up to GitHub. Those three commands, every time. That's the whole system.

Have them run `git pull` once while you watch. Expected output: `Already up to date.`

Have them open CLAUDE.md, add a word to the end of any line (like "test"), save, and then in Git Bash run:
```
git add .
git commit -m "test push"
git push
```

Confirm on the GitHub repo page that the change shows up. Have them remove the test word, then push again.

### Phase 9: Confirm setup is complete

Check:
- [ ] `C:\Claude-Brain\` exists with all folders and `CLAUDE.md`
- [ ] `CLAUDE.md` has no `[MY_*]` placeholders remaining (grep confirmed)
- [ ] Private GitHub repo at `github.com/THEIR-USERNAME/Claude-Brain` exists and shows the first commit
- [ ] Teammate can run `git pull` and `git push` successfully
- [ ] Cowork is pointed at `C:\Claude-Brain\`
- [ ] They know the daily habit

Tell them: "You're done. When Andy updates a skill, he'll Teams you the new `.skill` file. Save it into `C:\Claude-Brain\skills\`, drop it into Cowork chat, click Save skill to install, then commit and push. Welcome aboard."

### Common failure modes (troubleshooting playbook)

**"Please tell me who you are" on commit.** Re-run `git config --global user.email "..."` and `--global user.name "..."` in Git Bash, then retry commit.

**"Authentication failed" on push.** They typed their GitHub password instead of a Personal Access Token. Phase 6.

**Browser auth window fails to load (127.0.0.1 connection refused).** Corporate firewall or VPN. Skip browser auth, use PAT. Phase 6.

**"src refspec main does not match any" on push.** No commit was made yet. Go back and run `git commit -m "first commit"`.

**"fatal: not a git repository".** They're not inside `C:\Claude-Brain\` in Git Bash. Have them run `cd /c/Claude-Brain` first.

**Cowork can't see files after they were copied.** Close and reopen Cowork. It re-scans the folder on open.

**They can't find their HubSpot Owner ID.** In HubSpot: avatar top right → Profile & Preferences → Owner ID is the number there. If still stuck, Teams Andy.
