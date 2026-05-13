# Git Setup Guide — Start Here
*Written for Brian. No tech experience required.*

---

## The Big Picture (3rd Grade Version)

Think of GitHub like a **magic locker at school.**

- Your work lives in the locker (GitHub cloud)
- You can grab your stuff from ANY computer, anytime
- Every time you save, it takes a snapshot — so you can always go back
- Nobody can mess up your stuff because it's all backed up

Your "locker" is called a **repository** (repo for short). We're going to create one called `osi-claude-brain`.

---

## STEP 1 — Find Your GitHub Username

1. Open your browser and go to **github.com**
2. Click your **profile picture** in the top-right corner
3. Your username shows up right below your photo (looks like `@yourname`)
4. Write it down — you'll need it in Step 3

---

## STEP 2 — Create Your Repo on GitHub

1. Go to **github.com** and log in
2. Click the **"+"** button in the top-right corner → **"New repository"**
3. Fill it out like this:

   | Field | What to type |
   |-------|-------------|
   | Repository name | `osi-claude-brain` |
   | Description | My Claude skills and automation hub |
   | Public / Private | **Private** ← important! |
   | Initialize with README | Leave **unchecked** |

4. Click **"Create repository"**
5. GitHub will show you a page with setup commands — **leave that tab open**

---

## STEP 3 — Set Up Git on This Computer

Open **PowerShell** (search "PowerShell" in the Start menu) and paste these commands one at a time. Hit Enter after each one.

**Tell Git who you are:**
```powershell
git config --global user.name "Brian Charrette"
git config --global user.email "bc@osihardware.com"
```

**Tell Git to use a simple credential helper (so you don't type your password every time):**
```powershell
git config --global credential.helper manager
```

---

## STEP 4 — Connect This Folder to GitHub

In PowerShell, navigate to your Claude folder:
```powershell
cd "C:\Users\MINI OSI RIG\OneDrive - OSI Hardware\Documents\Claude\Projects\GitHub"
```

Initialize git in this folder:
```powershell
git init
git branch -M main
```

Connect it to your GitHub repo (replace YOUR_USERNAME with your actual username from Step 1):
```powershell
git remote add origin https://github.com/YOUR_USERNAME/osi-claude-brain.git
```

---

## STEP 5 — First Push (Upload Everything to GitHub)

```powershell
git add -A
git commit -m "First upload — OSI Claude Brain"
git push -u origin main
```

When it asks for your **username and password**:
- Username = your GitHub username
- Password = a **Personal Access Token** (NOT your GitHub password — see below)

### Getting a Personal Access Token (PAT)

GitHub doesn't let you use your real password anymore. Use a token instead:

1. Go to **github.com → Settings** (click your profile pic → Settings)
2. Scroll all the way down → click **"Developer settings"**
3. Click **"Personal access tokens"** → **"Tokens (classic)"**
4. Click **"Generate new token (classic)"**
5. Name it: `osi-claude-brain`
6. Set expiration: **No expiration** (or 1 year)
7. Check the box next to **"repo"** (gives full repo access)
8. Click **"Generate token"**
9. **COPY THE TOKEN NOW** — you can't see it again!
10. Paste it as your "password" when git asks

---

## STEP 6 — Setting Up a Second Computer

On your other computer(s), do Steps 3, then run this instead of Steps 4-5:

```powershell
# Navigate to where you want the folder to live
cd "C:\Users\YOUR_USERNAME\Documents"

# Clone (download) your repo
git clone https://github.com/YOUR_GITHUB_USERNAME/osi-claude-brain.git

# Go into the folder
cd osi-claude-brain
```

Done. You now have everything on that computer.

---

## Daily Workflow — Just 2 Clicks

| When | Do this |
|------|---------|
| End of work session / made changes | Double-click `scripts\push.bat` |
| Starting work on a different computer | Double-click `scripts\pull.bat` |
| Want to see what changed | Double-click `scripts\status.bat` |

---

## Emergency Cheat Sheet

| What you want to do | Command |
|---------------------|---------|
| Save everything to GitHub | `git add -A` then `git commit -m "note"` then `git push` |
| Get latest from GitHub | `git pull` |
| See what changed | `git status` |
| See your save history | `git log --oneline` |
| Undo last save (before pushing) | `git reset HEAD~1` |

---

## Troubleshooting

**"Permission denied" or "Authentication failed"**
→ Your Personal Access Token may have expired. Make a new one (Step 5 above).

**"Everything up to date" when pushing**
→ Nothing changed since your last push. That's fine!

**"Merge conflict"**
→ Two computers edited the same file. Call Claude for help — this is fixable.

**Can't find PowerShell**
→ Press `Windows key + R`, type `powershell`, press Enter.

---
*Last updated: May 2026*
