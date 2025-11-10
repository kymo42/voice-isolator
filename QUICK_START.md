# Quick Start Guide - SpeakerLove

## 🚀 5-Minute Setup

### Step 1: Install Virtual Audio Cable (3 minutes)
1. Download **VB-Audio VoiceMeeter**: https://vb-audio.com/Voicemeeter/
2. Install and restart your PC
3. Open VoiceMeeter after restart

### Step 2: Configure VoiceMeeter (1 minute)
1. In VoiceMeeter, set **Hardware Out 1** to your speakers
2. Set **Hardware Out 2** to **VoiceMeeter AUX** (this captures speaker audio)
3. Set application audio output to go through VoiceMeeter

### Step 3: Run SpeakerLove (1 minute)
```
Double-click: run.bat
```

OR from command prompt:
```bash
cd C:\Users\0\SpeakerLove
python SpeakerLove.py
```

### Step 4: Select Devices
- **Microphone**: Your physical microphone
- **Speaker Loopback**: Microphone (Voicemeeter Aux) or Stereo Mix
- **Output Virtual Mic**: Any available output (e.g., Speakers)

### Step 5: Use in Your App
Set Discord/Teams/Zoom to use your **Output Virtual Mic** as input

## ✅ Test It
1. Click **Start Voice Isolation**
2. Play YouTube video or music
3. Speak into mic
4. Adjust **Subtraction Strength** slider until speaker audio disappears
5. Your voice should be isolated!

## 🎚️ Fine-Tuning
- **Slider too low**: Speaker audio still comes through → increase
- **Slider too high**: Your voice gets removed → decrease
- **Sweet spot**: Usually 0.8-1.2

## ⚠️ Common Issues

| Problem | Solution |
|---------|----------|
| No audio output | Check devices selected + app microphone settings |
| Speaker audio still plays | Increase Subtraction Strength slider |
| Your voice is quiet/removed | Decrease Subtraction Strength slider |
| No "Speaker Loopback" option | Install VoiceMeeter, then refresh devices |

## 📖 Full Setup
For detailed setup with diagrams, see: **README.md**

---

**That's it!** You now have real-time speaker output removal from your microphone. 🎉
