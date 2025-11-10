# SpeakerLove - Gaming Audio Processor

Clean voice communication for gamers who LOVE using speakers instead of headsets.

## What It Does

**SpeakerLove** removes game/speaker audio from your microphone input so your teammates hear only your voice during gaming.

### Perfect For:
- 🎮 Gamers who use **speakers instead of headsets**
- 💬 Playing games with minimal background noise (not in public)
- 👥 Team-based games (Discord, Team chat, in-game voice)
- 🎯 Competitive gaming where voice quality matters

### How It Works:

```
Your Microphone + Game Audio → SpeakerLove → Clean Voice Only
                                    ↓
                          Discord/Team Chat receives
                          just your voice (no game!)
```

## Requirements

1. **Windows 10/11**
2. **VB-Audio VoiceMeeter** (Free) - For virtual audio routing
3. **Microphone**
4. **Speakers** (obviously!)
5. **Python 3.7+** (if running from source) OR just use the .exe

## Installation

### Option 1: Use the .exe (Easiest)
1. Download `SpeakerLove.exe` from the releases
2. Double-click to run
3. Follow setup instructions below

### Option 2: Run from Python
```bash
python SpeakerLove.py
```

## Setup Instructions

### Step 1: Install VoiceMeeter (5 minutes)

1. Download from: https://vb-audio.com/Voicemeeter/
2. Install and **restart your PC**
3. This creates virtual audio devices needed for SpeakerLove

### Step 2: Route Your Game Audio Through VoiceMeeter

**Windows 11:**
1. Settings → Sound → Volume mixer → "App volume and device preferences"
2. For your game (Discord, browser, etc.):
   - Output device → Set to "VoiceMeeter Virtual Input"
3. Do this for ANY app that outputs audio

**Windows 10:**
1. Right-click speaker icon → Sound settings
2. Volume mixer → Find your game/app
3. Change output to "VoiceMeeter Virtual Input"

### Step 3: Run SpeakerLove

1. Run `SpeakerLove.exe` (or `python SpeakerLove.py`)
2. The GUI will open

### Step 4: Select Audio Devices

**Your Microphone:**
- Pick your actual microphone (usually "Microphone (Sound Blaster...)" or similar)

**Game/Speaker Audio (Loopback):**
- Select one of:
  - "What U Hear (Sound Blaster...)" 
  - "Stereo Mix (Conexant...)"
  - Any "Input (Voicemeeter...)" option

**Output (Virtual Mic):**
- **Important:** Select a "Voicemeeter" option (e.g., "[46] Voicemeeter Input")
- This is where your CLEAN voice goes (NOT to speakers!)
- This prevents you from hearing your own voice

### Step 5: Click START

1. Click "START - Begin Voice Isolation"
2. Wait for status to turn **GREEN "RUNNING"**
3. If error: Try different loopback device

### Step 6: Configure Discord/Game

Set your voice chat input device to the **same Voicemeeter option** you selected in SpeakerLove:

**Discord:**
- User Settings → Voice & Video
- Microphone: Select your Voicemeeter device
- Microphone Volume: Comfortable level
- Test microphone

**In-Game Voice Chat:**
- Settings → Audio → Microphone
- Select same Voicemeeter device

### Step 7: Test

1. Start a game with voice chat enabled
2. Play game audio (music, effects, etc.)
3. Speak into your microphone
4. Ask a teammate: "Do you hear my voice?"
5. Check: **You should NOT hear yourself through speakers**
6. Teammates should hear: **Only your voice, no game audio**

## Troubleshooting

### Issue: Loopback dropdown is empty
**Solution:** Install/restart VoiceMeeter or enable Stereo Mix in Windows Sound settings

### Issue: Output dropdown doesn't show Voicemeeter
**Solution:** 
- Make sure VoiceMeeter is fully installed
- Restart SpeakerLove

### Issue: Can't hear game audio through speakers
**Solution:**
1. Make sure game output is set to "VoiceMeeter Virtual Input" in Windows Sound settings
2. Check VoiceMeeter is configured to output to your speakers
3. Check game audio settings

### Issue: Still hearing your own voice through speakers
**Solution:**
1. Double-check Output device is set to Voicemeeter (not [13] or speakers!)
2. If already correct, try different Voicemeeter option in Output dropdown

### Issue: SpeakerLove won't start (RED error)
**Solution:**
1. Refresh devices
2. Try different Loopback option
3. Try different Output option
4. Ensure you selected ALL three devices

## Fine-Tuning

**Subtraction Strength Slider:**
- **1.0** (default): Perfect for most games
- **Lower (0.5-0.8)**: If your voice sounds too quiet
- **Higher (1.5-2.0)**: If teammates still hear game audio

Adjust while running for real-time testing!

## FAQ

**Q: Can I use this without VoiceMeeter?**
A: You could use Stereo Mix or Virtual Audio Cable, but VoiceMeeter is free and reliable.

**Q: Does this add much latency?**
A: No, typically 20-50ms - imperceptible during voice chat.

**Q: Can I use this for streaming?**
A: Yes! Set your streaming software's microphone to the Voicemeeter output device.

**Q: What if I want to hear myself sometimes?**
A: Just select speakers as the Output device instead of Voicemeeter (but you'll hear yourself).

**Q: Does this work with Valorant/CS2/Fortnite/etc?**
A: Yes! Works with ANY game that lets you select a microphone device.

**Q: Can I use this in public?**
A: Not recommended. Works best in quiet environments (home) with minimal ambient noise besides game audio.

## How It Works (Technical)

1. **Captures microphone** (your voice + game audio)
2. **Captures speaker output** (game audio being played)
3. **Subtracts** speaker audio from microphone
4. **Math:** Clean Voice = Microphone - Speaker Audio
5. **Outputs** only your clean voice to a virtual microphone
6. **Discord/Game** receives from the virtual mic

No AI or magic - just audio mathematics!

## Performance

- **CPU Usage:** 5-15% on modern systems
- **Memory:** ~100MB
- **Latency:** 20-50ms
- **Audio Quality:** Full fidelity (44.1kHz or 48kHz)

## License

Free and open source

## GitHub

https://github.com/kymo42/SpeakerLove

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues:
1. Check the Troubleshooting section
2. Verify VoiceMeeter is installed
3. Try refreshing devices
4. Check device selection

## Credits

Built for gamers who prefer speakers to headsets and want clean team communication.

---

**Enjoy crystal-clear voice communication!** 🎮🎤
