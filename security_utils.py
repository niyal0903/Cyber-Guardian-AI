import cv2
import os
import time
import numpy as np
import sounddevice as sd

# Sirf Intruder ki photo save karne ke liye
def capture_intruder(frame):
    folder = "Intruder_Logs"
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    file_path = os.path.join(folder, f"intruder_{timestamp}.jpg")
    cv2.imwrite(file_path, frame)
    return file_path

# Voice/Silence check karne ke liye (Acoustic Fingerprint)
def check_voice_presence(duration=3):
    fs = 44100
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    
    # Sound level (RMS) check karo
    rms = np.sqrt(np.mean(recording**2))
    
    # Agar silence hai (RMS < 0.01) ya wrong voice hai
    if rms < 0.01:
        return "SILENCE"
    else:
        # Yahan Pitch calculation logic (Simplified for now)
        return "VOICE_DETECTED"