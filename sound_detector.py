import sounddevice as sd
import numpy as np
import datetime
from db_logger import log_sound_event

# Function to check if sound level exceeds threshold
def sound_event_detected(indata, frames, time, status, threshold):
    volume_norm = np.linalg.norm(indata) * 10
    print(volume_norm)
    if volume_norm > threshold:
        print(f"Sound event detected at {datetime.datetime.now()}, Volume: {volume_norm:.2f} dB")
        # Log the event to the database
        log_sound_event(volume_norm, datetime.datetime.now())

# Main function to start listening for sound events
def listen_for_sound_events(threshold):
    try:
        # Use the default microphone as the audio input device
        with sd.InputStream(callback=lambda indata, frames, time, status: sound_event_detected(indata, frames, time, status, threshold), blocksize=1024):
            print("Listening for sound events...")
            # Keep the program running to continuously listen for sound events
            sd.sleep(-1)
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to load the threshold from the config file
def load_threshold_from_config():
    import json
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        return config['sound_detection']['threshold']
