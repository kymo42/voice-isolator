#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
List all available audio devices on the system.
Helps identify which device numbers to use in SpeakerLove.
"""

import sounddevice as sd

def main():
    print("=" * 80)
    print("AUDIO DEVICES ON THIS SYSTEM")
    print("=" * 80)
    print()
    
    devices = sd.query_devices()
    
    print("INPUT DEVICES (Microphones):")
    print("-" * 80)
    input_count = 0
    for i, dev in enumerate(devices):
        if dev['max_input_channels'] > 0:
            channels = dev['max_input_channels']
            sr = dev['default_samplerate']
            latency = dev['default_low_input_latency']
            print(f"  [{i}] {dev['name']}")
            print(f"      Channels: {channels}, Sample Rate: {sr}Hz, Latency: {latency*1000:.1f}ms")
            input_count += 1
    
    if input_count == 0:
        print("  (No input devices found)")
    
    print()
    print("OUTPUT DEVICES (Speakers, Virtual Devices):")
    print("-" * 80)
    output_count = 0
    for i, dev in enumerate(devices):
        if dev['max_output_channels'] > 0:
            channels = dev['max_output_channels']
            sr = dev['default_samplerate']
            latency = dev['default_low_output_latency']
            
            # Highlight potential speaker loopback devices
            is_loopback = any(keyword in dev['name'].lower() for keyword in 
                             ['stereo mix', 'loopback', 'what u hear', 'voicemeeter', 'virtual'])
            marker = " <- LIKELY LOOPBACK" if is_loopback else ""
            
            print(f"  [{i}] {dev['name']}{marker}")
            print(f"      Channels: {channels}, Sample Rate: {sr}Hz, Latency: {latency*1000:.1f}ms")
            output_count += 1
    
    if output_count == 0:
        print("  (No output devices found)")
    
    print()
    print("=" * 80)
    print("RECOMMENDATIONS:")
    print("=" * 80)
    
    # Find best input
    input_devices = [(i, dev) for i, dev in enumerate(devices) if dev['max_input_channels'] > 0]
    if input_devices:
        best_input = max(input_devices, key=lambda x: x[1]['max_input_channels'])
        print(f"[OK] Recommended Microphone: [{best_input[0]}] {best_input[1]['name']}")
    
    # Find loopback
    loopback_devices = [(i, dev) for i, dev in enumerate(devices) 
                       if dev['max_output_channels'] > 0 and 
                       any(keyword in dev['name'].lower() for keyword in 
                           ['stereo mix', 'loopback', 'what u hear', 'voicemeeter'])]
    if loopback_devices:
        print(f"[OK] Speaker Loopback: [{loopback_devices[0][0]}] {loopback_devices[0][1]['name']}")
    else:
        print("[WARNING] Speaker Loopback: NOT FOUND - Install VB-Audio VoiceMeeter")
    
    # Find output
    output_devices = [(i, dev) for i, dev in enumerate(devices) if dev['max_output_channels'] > 0]
    if output_devices:
        # Prefer non-loopback output
        regular_output = [(i, dev) for i, dev in output_devices 
                         if not any(keyword in dev['name'].lower() for keyword in 
                                   ['loopback', 'stereo mix'])]
        if regular_output:
            best_output = regular_output[0]
        else:
            best_output = output_devices[0]
        print(f"[OK] Output Device: [{best_output[0]}] {best_output[1]['name']}")
    
    print()
    print("USAGE IN VOICE ISOLATOR:")
    print("-" * 80)
    print("1. Open SpeakerLove: python voice_isolator.py")
    print("2. Select the recommended devices above")
    print("3. If loopback not found, install VoiceMeeter first")
    print()

if __name__ == "__main__":
    main()
