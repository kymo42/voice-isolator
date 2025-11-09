"""
SpeakerLove - Gaming Voice Chat Audio Processor
Remove speaker/game audio from microphone input for clean voice transmission

For gamers who LOVE using speakers instead of headsets and want clean voice communication
without hearing their own voice or game audio in team chat.

GitHub: https://github.com/yourusername/speakerlove
"""

import numpy as np
import threading
import queue
from collections import deque
import tkinter as tk
from tkinter import ttk, messagebox
import sounddevice as sd
import sys

class SpeakerLove:
    """Core audio processing engine"""
    
    def __init__(self, mic_device, speaker_device, output_device, sample_rate=44100, chunk_size=2048):
        self.mic_device = mic_device
        self.speaker_device = speaker_device
        self.output_device = output_device
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        
        self.running = False
        self.enabled = False
        self.subtraction_strength = 1.0
        self.delay_compensation = 0
        
        self.audio_queue = queue.Queue(maxsize=5)
        self.speaker_queue = queue.Queue(maxsize=5)
        self.output_queue = queue.Queue(maxsize=5)
        
        self.mic_stream = None
        self.speaker_stream = None
        self.output_stream = None
        
    def _mic_callback(self, indata, frames, time, status):
        """Microphone input callback"""
        try:
            audio = indata[:, 0] if indata.ndim > 1 else indata
            try:
                self.audio_queue.put_nowait(audio.copy().astype(np.float32))
            except queue.Full:
                pass
        except Exception as e:
            print(f"Mic callback error: {e}")
    
    def _speaker_callback(self, indata, frames, time, status):
        """Speaker loopback callback"""
        try:
            audio = indata[:, 0] if indata.ndim > 1 else indata
            try:
                self.speaker_queue.put_nowait(audio.copy().astype(np.float32))
            except queue.Full:
                pass
        except Exception as e:
            print(f"Speaker callback error: {e}")
    
    def _output_callback(self, outdata, frames, time, status):
        """Output callback"""
        try:
            try:
                processed = self.output_queue.get(timeout=0.01)
                if outdata.ndim == 1:
                    outdata[:] = processed[:len(outdata)]
                else:
                    outdata[:, 0] = processed[:len(outdata)]
            except queue.Empty:
                outdata[:] = 0
        except Exception as e:
            print(f"Output error: {e}")
            outdata[:] = 0
    
    def process_audio(self):
        """Main processing loop"""
        speaker_buffer = deque(maxlen=10)  # Much smaller buffer for lower latency
        
        while self.running:
            try:
                mic_audio = self.audio_queue.get(timeout=0.1)
                
                # Get latest speaker audio
                try:
                    while True:
                        speaker_audio = self.speaker_queue.get_nowait()
                        speaker_buffer.append(speaker_audio)
                except queue.Empty:
                    pass
                
                if self.enabled and len(speaker_buffer) > 0:
                    # Combine speaker buffer
                    speaker_combined = np.concatenate(list(speaker_buffer))

                    # Apply delay compensation if set
                    if self.delay_compensation != 0:
                        speaker_combined = np.roll(speaker_combined, self.delay_compensation)

                    # Align lengths
                    min_len = min(len(mic_audio), len(speaker_combined))
                    mic_audio = mic_audio[:min_len]
                    speaker_combined = speaker_combined[:min_len]

                    # Subtract: Clean Voice = Microphone - Speaker Audio
                    cleaned = mic_audio - (speaker_combined * self.subtraction_strength)
                    cleaned = np.tanh(cleaned)  # Soft clipping
                else:
                    cleaned = mic_audio

                try:
                    self.output_queue.put_nowait(cleaned)
                except queue.Full:
                    pass
                    
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error: {e}")
    
    def start(self):
        """Start audio streams"""
        try:
            print(f"Starting with: Mic={self.mic_device}, Speaker={self.speaker_device}, Output={self.output_device}")
            
            self.mic_stream = sd.InputStream(
                device=self.mic_device,
                samplerate=self.sample_rate,
                channels=1,
                blocksize=self.chunk_size,
                callback=self._mic_callback
            )
            self.mic_stream.start()
            
            self.speaker_stream = sd.InputStream(
                device=self.speaker_device,
                samplerate=self.sample_rate,
                channels=1,
                blocksize=self.chunk_size,
                callback=self._speaker_callback
            )
            self.speaker_stream.start()
            
            self.output_stream = sd.OutputStream(
                device=self.output_device,
                samplerate=self.sample_rate,
                channels=1,
                blocksize=self.chunk_size,
                callback=self._output_callback
            )
            self.output_stream.start()
            
            self.running = True
            threading.Thread(target=self.process_audio, daemon=True).start()
            
            print("✓ Started successfully")
            return True
            
        except Exception as e:
            print(f"Start error: {e}")
            messagebox.showerror("Error", f"Failed to start:\n{e}")
            self.stop()
            return False
    
    def stop(self):
        """Stop audio"""
        self.running = False
        for stream in [self.mic_stream, self.speaker_stream, self.output_stream]:
            if stream:
                try:
                    stream.stop()
                    stream.close()
                except:
                    pass
        print("✓ Stopped")


class GUI:
    """Main GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SpeakerLove - Gaming Audio Processor")
        self.root.geometry("750x600")
        
        self.isolator = None
        
        # Title
        title_frame = ttk.Frame(root)
        title_frame.pack(pady=10)
        ttk.Label(title_frame, text="SpeakerLove", font=("Arial", 18, "bold")).pack()
        ttk.Label(title_frame, text="Remove game/speaker audio from your voice", font=("Arial", 10)).pack()
        ttk.Label(title_frame, text="For gamers who LOVE using speakers instead of headsets", font=("Arial", 9, "italic"), foreground="gray").pack()
        
        # Info frame
        info_frame = ttk.LabelFrame(root, text="How It Works", padding=10)
        info_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        info_text = """
Your Voice + Game Audio → Microphone Input
                    ↓
            Voice Isolator
                    ↓
Clean Voice Only → Discord/Team Chat (they hear only you!)
        """
        ttk.Label(info_frame, text=info_text, font=("Arial", 9), justify=tk.LEFT).pack()
        
        # Devices frame
        dev_frame = ttk.LabelFrame(root, text="Select Audio Devices", padding=10)
        dev_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        ttk.Label(dev_frame, text="Your Microphone:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.mic_var = tk.StringVar()
        self.mic_combo = ttk.Combobox(dev_frame, textvariable=self.mic_var, state="readonly", width=65)
        self.mic_combo.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(dev_frame, text="Game/Speaker Audio:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.speaker_var = tk.StringVar()
        self.speaker_combo = ttk.Combobox(dev_frame, textvariable=self.speaker_var, state="readonly", width=65)
        self.speaker_combo.grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(dev_frame, text="Output (Virtual Mic):").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(dev_frame, text="(Should show Voicemeeter options)", 
                 font=("Arial", 8), foreground="gray").grid(row=2, column=1, sticky=tk.W)
        self.output_var = tk.StringVar()
        self.output_combo = ttk.Combobox(dev_frame, textvariable=self.output_var, state="readonly", width=65)
        self.output_combo.grid(row=3, column=1, sticky=tk.W)
        
        # Control frame
        ctrl_frame = ttk.LabelFrame(root, text="Controls", padding=10)
        ctrl_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        self.start_btn = ttk.Button(ctrl_frame, text="START - Begin Voice Isolation", command=self.toggle)
        self.start_btn.pack(fill=tk.X, pady=10)
        
        self.status_label = ttk.Label(ctrl_frame, text="Status: STOPPED", foreground="red", font=("Arial", 13, "bold"))
        self.status_label.pack()
        
        # Settings frame
        set_frame = ttk.LabelFrame(root, text="Fine-Tuning (Adjust if needed)", padding=10)
        set_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        ttk.Label(set_frame, text="Subtraction Strength (Higher = Remove more game audio):").grid(row=0, column=0, sticky=tk.W)
        self.strength_var = tk.DoubleVar(value=1.0)
        ttk.Scale(set_frame, from_=0.5, to=2.0, variable=self.strength_var, command=self.update_strength).grid(row=0, column=1, sticky=tk.EW)
        self.strength_label = ttk.Label(set_frame, text="1.0", width=5)
        self.strength_label.grid(row=0, column=2, padx=5)

        ttk.Label(set_frame, text="Delay Compensation (samples):").grid(row=1, column=0, sticky=tk.W, pady=(10,0))
        self.delay_var = tk.IntVar(value=0)
        ttk.Spinbox(set_frame, from_=-500, to=500, textvariable=self.delay_var, command=self.update_delay).grid(row=1, column=1, sticky=tk.W)
        self.delay_label = ttk.Label(set_frame, text="0", width=5)
        self.delay_label.grid(row=1, column=2, padx=5)

        set_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=5)
        ttk.Button(button_frame, text="Refresh Devices", command=self.refresh_devices).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Help", command=self.show_help).pack(side=tk.LEFT, padx=5)
        
        self.refresh_devices()
    
    def refresh_devices(self):
        """Load and display devices correctly"""
        try:
            devices = sd.query_devices()
            
            mics = []
            speakers = []
            outputs = []
            
            for i, dev in enumerate(devices):
                name_lower = dev['name'].lower()
                dev_str = f"[{i}] {dev['name']}"
                
                # MICROPHONES: Real mics are typically 1-2 channels input, 0 output
                if dev['max_input_channels'] in [1, 2] and dev['max_output_channels'] == 0:
                    if any(k in name_lower for k in ['microphone', 'mic', 'capture', 'input']):
                        if not any(k in name_lower for k in ['voicemeeter', 'what u hear', 'stereo mix']):
                            mics.append(dev_str)
                
                # LOOPBACK: Has 2+ input channels, 0 output
                if dev['max_output_channels'] == 0 and dev['max_input_channels'] > 0:
                    if any(k in name_lower for k in ['voicemeeter', 'what u hear', 'stereo mix', 'input (']):
                        speakers.append(dev_str)
                
                # OUTPUT: Voicemeeter virtual microphones
                if dev['max_output_channels'] > 0:
                    if any(k in name_lower for k in ['voicemeeter']):
                        outputs.append(dev_str)
                    else:
                        # Also include physical speakers as fallback
                        if any(k in name_lower for k in ['speaker', 'sound mapper']):
                            outputs.append(dev_str)
            
            self.mic_combo['values'] = mics
            self.speaker_combo['values'] = speakers
            self.output_combo['values'] = outputs
            
            if mics:
                self.mic_combo.current(0)
            if speakers:
                stereo_mix_idx = next((i for i, s in enumerate(speakers) if 'stereo mix' in s.lower()), 0)
                self.speaker_combo.current(stereo_mix_idx)
            if outputs:
                # Try to find Voicemeeter Input as default
                voicemeeter_idx = next((i for i, s in enumerate(outputs) if 'voicemeeter input' in s.lower()), 0)
                self.output_combo.current(voicemeeter_idx)
            
            print(f"Found {len(mics)} mics, {len(speakers)} loopbacks, {len(outputs)} outputs")
            
        except Exception as e:
            messagebox.showerror("Error", f"Device refresh failed: {e}")
    
    def update_strength(self, value):
        """Update strength display and value"""
        val = float(value)
        self.strength_label.config(text=f"{val:.2f}")
        if self.isolator:
            self.isolator.subtraction_strength = val

    def update_delay(self):
        """Update delay compensation"""
        val = self.delay_var.get()
        self.delay_label.config(text=str(val))
        if self.isolator:
            self.isolator.delay_compensation = val
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
VOICE ISOLATOR - GAMING SETUP GUIDE

For gamers who use SPEAKERS instead of headsets and want clean voice chat.

SETUP:
1. Install VoiceMeeter: https://vb-audio.com/Voicemeeter/
   - Route your game/app audio through VoiceMeeter
   
2. Select devices in Voice Isolator:
   - Your Microphone: Your physical microphone
   - Game/Speaker Audio: Capture device (Stereo Mix or What U Hear)
   - Output (Virtual Mic): Voicemeeter Input device
   
3. Set Discord/Team Voice Input to: Voicemeeter Input device

4. Click START and adjust slider if needed

RESULT:
- You don't hear your own voice (no echo!)
- Teammates hear only your voice (no game audio!)
- Clean, professional voice communication

For issues or setup help, see the README file.
        """
        messagebox.showinfo("Help", help_text)
    
    def toggle(self):
        """Start/stop"""
        if not self.isolator or not self.isolator.running:
            try:
                mic_str = self.mic_combo.get()
                speaker_str = self.speaker_combo.get()
                output_str = self.output_combo.get()
                
                if not all([mic_str, speaker_str, output_str]):
                    messagebox.showerror("Error", "Please select all three devices")
                    return
                
                try:
                    mic_id = int(mic_str.split('[')[1].split(']')[0])
                    speaker_id = int(speaker_str.split('[')[1].split(']')[0])
                    output_id = int(output_str.split('[')[1].split(']')[0])
                except ValueError:
                    messagebox.showerror("Error", "Invalid device selection")
                    return
                
                self.isolator = SpeakerLove(mic_id, speaker_id, output_id)
                self.isolator.subtraction_strength = self.strength_var.get()
                
                if self.isolator.start():
                    self.isolator.enabled = True
                    self.start_btn.config(text="STOP - End Voice Isolation")
                    self.status_label.config(text="Status: RUNNING", foreground="green")
                else:
                    self.isolator = None
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start: {e}")
        else:
            self.isolator.enabled = False
            self.isolator.stop()
            self.isolator = None
            self.start_btn.config(text="START - Begin Voice Isolation")
            self.status_label.config(text="Status: STOPPED", foreground="red")


def main():
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
