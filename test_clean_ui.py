#!/usr/bin/env python3
"""
Quick test to verify the clean UI design is active
"""

import sys
import os

# Add current directory to path so we can import SpeakerLove
sys.path.insert(0, os.getcwd())

try:
    from SpeakerLove import GUI
    import tkinter as tk
    
    print("Successfully imported voice_isolator with clean UI")
    
    # Check if the clean UI methods exist
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    gui = GUI.__new__(GUI)  # Create instance without calling __init__
    
    # Check for clean UI attributes
    has_clean_ui = True
    attributes_to_check = [
        'configure_styles', 'update_status', 
        'status_indicator', 'status_text', 'start_btn'
    ]
    
    for attr in attributes_to_check:
        if not hasattr(gui, attr):
            print(f"Missing attribute: {attr}")
            has_clean_ui = False
    
    if has_clean_ui:
        print("All clean UI attributes present")
        print("Clean UI design is active")
    else:
        print("Clean UI attributes missing")
    
    root.destroy()
    
except ImportError as e:
    print(f"Import error: {e}")
except Exception as e:
    print(f"Error: {e}")