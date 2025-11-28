# SpeakerLove AI - Gaming Audio Processor

**Clean voice communication for gamers who LOVE using speakers instead of headsets.**

Powered by **AI noise reduction** to automatically remove game audio, music, and background noise in real-time.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## What It Does

**SpeakerLove** uses AI-powered noise reduction to filter your microphone input. It learns what background noise sounds like and removes it (game explosions, music, keyboard clicks) while preserving your voice.

### Perfect For:
- 🎮 Gamers who use **speakers instead of headsets**
- 💬 Playing games with background noise
- 👥 Team-based games (Discord, Teams, in-game voice)
- 🎵 Removing music and game audio from voice chat

## Quick Start

**Simply double-click `SpeakerLove_Launch.bat`**

That's it! The launcher will:
- ✅ Check if Python is installed
- ✅ Auto-install dependencies if needed
- ✅ Start the application

*Manual method:* You can also run `python SpeakerLove.py` if you installed dependencies manually.

## Requirements

1. **Windows 10/11**
2. **Python 3.8+** - [Download here](https://www.python.org/downloads/)
3. **VB-Audio VoiceMeeter** (Free) - [Download here](https://vb-audio.com/Voicemeeter/)

## Installation

### Step 1: Install Python
- Download Python 3.8 or newer from [python.org](https://www.python.org/downloads/)
- **IMPORTANT:** Check "Add Python to PATH" during installation

### Step 2: Install VoiceMeeter
- Download and install VoiceMeeter from [vb-audio.com](https://vb-audio.com/Voicemeeter/)
- Restart your computer after installation

### Step 3: Download SpeakerLove
```bash
git clone https://github.com/kymo42/SpeakerLove.git
cd SpeakerLove
```

### Step 4: Run SpeakerLove
Double-click `SpeakerLove_Launch.bat` - it will automatically install dependencies on first run.

## Setup Guide

### Configure Audio Routing

1. **Launch SpeakerLove**
   - Double-click `SpeakerLove_Launch.bat`

2. **Select Devices:**
   - **Microphone**: Your physical microphone
   - **Output**: VoiceMeeter Input (virtual device)

3. **Configure Your Voice Chat App** (Discord/Teams/etc)
   - Set **Input Device** to: **VoiceMeeter Output**

4. **Start AI Isolation**
   - Click "START AI ISOLATION"
   - **First 2 seconds**: The AI learns background noise (stay quiet or let game audio play)
   - **After that**: Active noise filtering begins

### How It Works

```
[Your Mic] → [SpeakerLove AI] → [VoiceMeeter Input] → [Discord/Teams]
                    ↓
            Removes game audio,
            music, keyboard noise
```

## Features

- ✨ **Real-time AI noise reduction**
- 🎯 **Learns your environment** - adapts to your specific background noise
- 🚀 **Low latency** - typically 20-50ms
- 💻 **Simple GUI** - easy device selection
- 🔧 **No complex configuration** - just select devices and start

## Troubleshooting

### "Missing Requirements" Error
Run this command in the SpeakerLove folder:
```bash
pip install -r requirements.txt
```

### No Audio Output
- Make sure you selected **VoiceMeeter Input** as the output device
- Check that your voice chat app is using **VoiceMeeter Output** as input

### Hearing Yourself / Echo
- Do NOT select your speakers as the output device in SpeakerLove
- Output should always be a virtual device (VoiceMeeter Input)

### Poor Noise Reduction
- When you click "START", stay quiet for 2 seconds so the AI can learn background noise
- Or let your game audio play for 2 seconds to learn that noise profile
- Restart the isolation to re-learn if your environment changes

## Manual Installation

If the launcher doesn't work:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python SpeakerLove.py
```

## Dependencies

- `numpy` - Audio processing
- `sounddevice` - Audio I/O
- `noisereduce` - AI noise reduction
- `scipy` - Signal processing

## Technical Details

- **Sample Rate**: 48kHz (optimal for voice)
- **Chunk Size**: 2048 samples
- **Noise Reduction**: Spectral gating with adaptive learning
- **Latency**: ~43ms (2048/48000)

## License

MIT License - See [LICENSE](LICENSE) file for details

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## Support

Having issues? [Open an issue](https://github.com/kymo42/SpeakerLove/issues) on GitHub.

---

**Made with ❤️ for gamers who love speakers**
