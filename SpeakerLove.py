"""
SpeakerLove - Gaming Voice Chat Audio Processor
AI-Powered Noise Suppression for Clean Voice Transmission

For gamers who LOVE using speakers instead of headsets.
Uses noise reduction to remove game audio and background noise.

GitHub: https://github.com/kymo42/SpeakerLove
"""

import numpy as np
import threading
import queue
import tkinter as tk
from tkinter import ttk, messagebox
import sounddevice as sd
import sys
import os

# Try to import noise reduction library
try:
    import noisereduce as nr
    AI_AVAILABLE = True
    IMPORT_ERROR = None
    print("✓ Noise Reduction Library Loaded")
except ImportError as e:
    AI_AVAILABLE = False
    IMPORT_ERROR = str(e)
    print(f"Noise reduction import failed: {e}")

class SpeakerLove:
    """Core audio processing engine using noise reduction"""
    
    def __init__(self, mic_device, output_device, sample_rate=48000, chunk_size=2048):
        self.mic_device = mic_device
        self.output_device = output_device
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        
        self.running = False
        self.enabled = False
        
        self.audio_queue = queue.Queue(maxsize=20)
        self.output_queue = queue.Queue(maxsize=20)
        
        self.mic_stream = None
        self.output_stream = None
        
        # For noise profile learning
        self.noise_profile = None
        self.learning_frames = []
        self.learning_mode = True
        self.frames_to_learn = 10  # Learn from first 10 frames

    def _mic_callback(self, indata, frames, time, status):
        """Microphone input callback"""
        if status:
            print(f"Mic status: {status}")
        try:
            self.audio_queue.put_nowait(indata.copy().astype(np.float32))
        except queue.Full:
            pass
    
    def _output_callback(self, outdata, frames, time, status):
        """Output callback"""
        if status:
            print(f"Output status: {status}")
        try:
            data = self.output_queue.get_nowait()
            # Ensure we fill the buffer
            if len(data) < len(outdata):
                outdata[:len(data)] = data
                outdata[len(data):] = 0
            else:
                outdata[:] = data[:len(outdata)]
        except queue.Empty:
            outdata[:] = 0
    
    def process_audio(self):
        """Main processing loop"""
        while self.running:
            try:
                # Get audio chunk
                mic_audio = self.audio_queue.get(timeout=1.0)
                
                if self.enabled and AI_AVAILABLE:
                    try:
                        # Learn noise profile from first few frames
                        if self.learning_mode and len(self.learning_frames) < self.frames_to_learn:
                            self.learning_frames.append(mic_audio.copy())
                            if len(self.learning_frames) >= self.frames_to_learn:
                                # Build noise profile from collected frames
                                noise_sample = np.concatenate(self.learning_frames)
                                self.noise_profile = noise_sample
                                self.learning_mode = False
                                print("✓ Noise profile learned - AI active")
                            cleaned = mic_audio  # Pass through while learning
                        elif self.noise_profile is not None:
                            # Apply noise reduction
                            cleaned = nr.reduce_noise(
                                y=mic_audio.flatten(),
                                sr=self.sample_rate,
                                y_noise=self.noise_profile.flatten(),
                                stationary=False,
                                prop_decrease=1.0
                            )
                            # Reshape to match input
                            cleaned = cleaned.reshape(-1, 1)
                        else:
                            cleaned = mic_audio
                        
                    except Exception as e:
                        print(f"Noise reduction error: {e}")
                        cleaned = mic_audio
                else:
                    cleaned = mic_audio

                self.output_queue.put_nowait(cleaned)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Process Error: {e}")
    
    def start(self):
        """Start audio streams"""
        try:
            print(f"Starting with: Mic={self.mic_device}, Output={self.output_device}")
            
            self.mic_stream = sd.InputStream(
                device=self.mic_device,
                samplerate=self.sample_rate,
                channels=1,
                blocksize=self.chunk_size,
                callback=self._mic_callback
            )
            self.mic_stream.start()
            
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
        for stream in [self.mic_stream, self.output_stream]:
            if stream:
                try:
                    stream.stop()
                    stream.close()
                except:
                    pass
        print("✓ Stopped")


class GUI:
    """Main GUI with clean, minimal design"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SpeakerLove AI - Noise Suppression")
        self.root.geometry("500x450")
        self.root.configure(bg="#FFFFFF")
        
        # Configure custom styles
        self.configure_styles()
        
        self.isolator = None
        
        # Main container
        main_frame = tk.Frame(root, bg="#FFFFFF")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Title section
        title_frame = tk.Frame(main_frame, bg="#FFFFFF")
        title_frame.pack(pady=(0, 25))
        
        tk.Label(title_frame, text="SpeakerLove AI",
                font=("Segoe UI", 24, "bold"),
                fg="#4A90E2", bg="#FFFFFF").pack()
        
        tk.Label(title_frame, text="AI-Powered Voice Isolation",
                font=("Segoe UI", 12),
                fg="#5A5A5A", bg="#FFFFFF").pack()
        
        # Status indicator
        status_frame = tk.Frame(main_frame, bg="#FFFFFF")
        status_frame.pack(pady=(0, 20))
        
        self.status_indicator = tk.Frame(status_frame, width=12, height=12, bg="#E0E0E0")
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 10))
        self.status_indicator.pack_propagate(False)
        
        self.status_text = tk.Label(status_frame, text="STOPPED",
                                   font=("Segoe UI", 11, "bold"),
                                   fg="#CC0000", bg="#FFFFFF")
        self.status_text.pack(side=tk.LEFT)
        
        # Device selection
        device_frame = tk.Frame(main_frame, bg="#FFFFFF")
        device_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Microphone
        tk.Label(device_frame, text="Microphone",
                font=("Segoe UI", 10, "bold"),
                fg="#2C2C2C", bg="#FFFFFF").pack(anchor=tk.W)
        
        self.mic_var = tk.StringVar()
        self.mic_combo = ttk.Combobox(device_frame, textvariable=self.mic_var,
                                     state="readonly", font=("Segoe UI", 9))
        self.mic_combo.pack(fill=tk.X, pady=(5, 12))
        
        # Output
        tk.Label(device_frame, text="Output (Virtual Mic)",
                font=("Segoe UI", 10, "bold"),
                fg="#2C2C2C", bg="#FFFFFF").pack(anchor=tk.W)
        
        self.output_var = tk.StringVar()
        self.output_combo = ttk.Combobox(device_frame, textvariable=self.output_var,
                                        state="readonly", font=("Segoe UI", 9))
        self.output_combo.pack(fill=tk.X, pady=(5, 0))
        
        # Controls
        control_frame = tk.Frame(main_frame, bg="#FFFFFF")
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.start_btn = tk.Button(control_frame,
                                  text="START AI ISOLATION",
                                  command=self.toggle,
                                  font=("Segoe UI", 11, "bold"),
                                  bg="#4A90E2", fg="#FFFFFF",
                                  relief="flat", bd=0, pady=12,
                                  cursor="hand2")
        self.start_btn.pack(fill=tk.X)
        
        # Bottom buttons
        button_frame = tk.Frame(main_frame, bg="#FFFFFF")
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Refresh Devices",
                  command=self.refresh_devices,
                  style="Clean.TButton").pack(side=tk.LEFT)
        
        ttk.Button(button_frame, text="Help",
                  command=self.show_help,
                  style="Clean.TButton").pack(side=tk.RIGHT)
        
        self.refresh_devices()
        
        if not AI_AVAILABLE:
            error_msg = f"Noise reduction failed to load.\n\nError: {IMPORT_ERROR}\n\nPlease run: pip install -r requirements.txt"
            messagebox.showwarning("Missing Requirements", error_msg)
    
    def configure_styles(self):
        """Configure custom ttk styles for clean design"""
        style = ttk.Style()
        
        # Combobox style
        style.configure("TCombobox",
                       fieldbackground="#FFFFFF",
                       background="#E0E0E0",
                       bordercolor="#5A5A5A",
                       lightcolor="#FFFFFF",
                       darkcolor="#5A5A5A",
                       arrowcolor="#4A90E2")
        
        # Button style
        style.configure("Clean.TButton",
                       background="#FFFFFF",
                       foreground="#2C2C2C",
                       bordercolor="#E0E0E0",
                       lightcolor="#FFFFFF",
                       darkcolor="#E0E0E0",
                       focuscolor="#4A90E2",
                       focusthickness=2)
    
    def refresh_devices(self):
        """Load and display devices correctly"""
        try:
            devices = sd.query_devices()
            
            mics = []
            outputs = []
            
            for i, dev in enumerate(devices):
                name_lower = dev['name'].lower()
                dev_str = f"[{i}] {dev['name']}"
                
                # MICROPHONES
                if dev['max_input_channels'] > 0:
                    if any(k in name_lower for k in ['microphone', 'mic', 'capture', 'input']):
                        if not any(k in name_lower for k in ['voicemeeter', 'what u hear', 'stereo mix']):
                            mics.append(dev_str)
                
                # OUTPUT: Voicemeeter virtual microphones
                if dev['max_output_channels'] > 0:
                    if any(k in name_lower for k in ['voicemeeter']):
                        outputs.append(dev_str)
                    else:
                        # Also include physical speakers as fallback
                        if any(k in name_lower for k in ['speaker', 'sound mapper']):
                            outputs.append(dev_str)
            
            self.mic_combo['values'] = mics
            self.output_combo['values'] = outputs
            
            if mics:
                self.mic_combo.current(0)
            if outputs:
                # Try to find Voicemeeter Input as default
                voicemeeter_idx = next((i for i, s in enumerate(outputs) if 'voicemeeter input' in s.lower()), 0)
                self.output_combo.current(voicemeeter_idx)
            
            print(f"Found {len(mics)} mics, {len(outputs)} outputs")
            
        except Exception as e:
            messagebox.showerror("Error", f"Device refresh failed: {e}")
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
SPEAKERLOVE AI - SETUP GUIDE

1. Install VoiceMeeter: https://vb-audio.com/Voicemeeter/
   
2. Select devices:
   - Microphone: Your physical microphone
   - Output: Voicemeeter Input device
   
3. Set Discord/Game Voice Input to: Voicemeeter Input device

4. Click START AI ISOLATION
   - First few seconds: Learning background noise
   - After that: Active noise filtering

The AI will automatically filter out game audio and background noise.
        """
        messagebox.showinfo("Help", help_text)
    
    def update_status(self, running, success=True):
        """Update the status indicator and text"""
        if running:
            if success:
                self.status_indicator.config(bg="#00C851")  # Green
                self.status_text.config(text="RUNNING", fg="#00C851")
                self.start_btn.config(text="STOP ISOLATION", bg="#CC0000")
            else:
                self.status_indicator.config(bg="#FFB347")  # Orange
                self.status_text.config(text="ERROR", fg="#FF6B35")
                self.start_btn.config(text="START AI ISOLATION", bg="#4A90E2")
        else:
            self.status_indicator.config(bg="#E0E0E0")  # Gray
            self.status_text.config(text="STOPPED", fg="#CC0000")
            self.start_btn.config(text="START AI ISOLATION", bg="#4A90E2")
    
    def toggle(self):
        """Start/stop"""
        if not self.isolator or not self.isolator.running:
            try:
                mic_str = self.mic_combo.get()
                output_str = self.output_combo.get()
                
                if not all([mic_str, output_str]):
                    messagebox.showerror("Error", "Please select both devices")
                    return
                
                try:
                    mic_id = int(mic_str.split('[')[1].split(']')[0])
                    output_id = int(output_str.split('[')[1].split(']')[0])
                except ValueError:
                    messagebox.showerror("Error", "Invalid device selection")
                    return
                
                self.isolator = SpeakerLove(mic_id, output_id)
                self.isolator.enabled = True
                
                if self.isolator.start():
                    self.update_status(running=True, success=True)
                else:
                    self.isolator = None
                    self.update_status(running=False, success=False)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start: {e}")
                self.update_status(running=False, success=False)
        else:
            self.isolator.enabled = False
            self.isolator.stop()
            self.isolator = None
            self.update_status(running=False, success=True)


def main():
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()