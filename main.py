import sound_detector
import time
from db_logger import create_database_structure

if __name__ == "__main__":
    try:
        print(f"Loading Threshold from config")
        threshold = sound_detector.load_threshold_from_config()
        print(f"Threshold: {threshold}")
    except Exception as e:
        print(f"Failed to load threshold from config: {e}") 

    try:
        print("Initializing Database")
        if not create_database_structure():
            exit(2)
    except Exception as e:
        print(f"Failed to initialize database: {e}")

    try:
        while True:
            sound_detector.listen_for_sound_events(threshold=threshold)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Service interrupted. Exiting...")