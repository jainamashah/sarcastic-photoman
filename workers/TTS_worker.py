from gtts import gTTS
from io import BytesIO
import pygame
import time
import queue  # Add this import

pygame.mixer.init()

def speak_worker(text_queue, frame_lock, latest_frame, processed_frame):
    while True:
        try:
            text = text_queue.get(timeout=1)  # Wait for new text (adjust timeout as needed)
            if text is None:  # Sentinel value to stop the worker
                break
            print("LLM Response:", text, "\n")
            pygame.mixer.music.stop()  # Stop any ongoing playback
            tts = gTTS(text, lang="en")
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            pygame.mixer.music.load(fp)
            pygame.mixer.music.play()
            # Wait for speech to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            # After speech, update processed_frame to latest_frame
            with frame_lock:
                processed_frame[0] = latest_frame[0]
        except queue.Empty:
            continue  # No new text yet, keep waiting


