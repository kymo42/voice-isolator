# How to Push to GitHub

Follow these steps to push Voice Isolator to your GitHub account.

## Prerequisites

1. GitHub account (create at https://github.com if needed)
2. Git installed on your computer
3. Local Voice Isolator repository (you already have this!)

## Step 1: Create a Repository on GitHub

1. Go to https://github.com/new
2. Enter repository name: `voice-isolator`
3. Enter description: "Gaming audio processor - Remove speaker/game audio from microphone for clean voice chat"
4. Choose "Public" (so others can use it)
5. **Do NOT** initialize with README (we already have one)
6. Click "Create repository"

## Step 2: Get Your Repository URL

After creating, GitHub shows you commands. Your repository URL will look like:
```
https://github.com/YOUR_USERNAME/voice-isolator.git
```

Copy this URL.

## Step 3: Add Remote and Push

Open Command Prompt in the Voice Isolator folder:

```bash
cd C:\Users\0\VoiceIsolator
git remote add origin https://github.com/YOUR_USERNAME/voice-isolator.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 4: Verify

1. Go to your GitHub repository URL
2. You should see all the files uploaded
3. README.md should display as the main page

## What Gets Uploaded

✅ **Uploaded:**
- voice_isolator.py (main application)
- README.md (main documentation)
- SETUP_GUIDE.md (detailed setup instructions)
- LICENSE (MIT license)
- requirements.txt (Python dependencies)
- .gitignore (git configuration)

✅ **Also included (for reference):**
- All the troubleshooting guides and notes we created

## Using the .exe on GitHub

The compiled .exe is in the `dist` folder:
- `dist/voice_isolator.exe` - Ready to run (no Python needed!)

Users can download just this one file and run it directly.

## Sharing Your Project

Once on GitHub, you can share:
- Main link: `https://github.com/YOUR_USERNAME/voice-isolator`
- Direct .exe link: `https://github.com/YOUR_USERNAME/voice-isolator/raw/main/dist/voice_isolator.exe`

## Making It Official

To make it even more visible:

1. Add topics:
   - Gaming
   - Audio
   - Voice
   - Microphone
   - Discord

2. Add a GitHub release:
   - Go to "Releases" tab
   - Click "Create a new release"
   - Tag: `v1.0.0`
   - Title: "Voice Isolator v1.0 - Initial Release"
   - Upload `dist/voice_isolator.exe`

3. Enable Discussions (optional):
   - Settings → Features → Check "Discussions"
   - Users can ask questions

## Future Updates

To update your repository:

```bash
cd C:\Users\0\VoiceIsolator
git add -A
git commit -m "Description of changes"
git push origin main
```

## Common Issues

**"fatal: 'origin' already exists"**
- You already added the remote
- Skip the `git remote add` step

**"Permission denied (publickey)"**
- You need SSH keys set up
- Or use HTTPS (recommended for beginners)
- Use your GitHub username and personal access token as password

**Files not showing up**
- Make sure you did `git push`
- Check the correct branch (should be `main`)
- Refresh the GitHub page

---

That's it! Your Voice Isolator is now on GitHub and ready for others to find and use! 🚀
