from preprocess.local_checks import *
from workers.TTS_worker import speak_worker
from Processing.analyze_image import llm_response, encode_image, analysis_worker
import time
from concurrent.futures import ThreadPoolExecutor
from workers.camera_worker import camera_worker
from workers.processing_worker import raw_display_worker, processed_display_worker
import threading
import queue
import cv2  # Add this import

def main():
    """Pipeline: frame capture -> local checks -> text-to-speech"""

    # Shared state
    frame_lock = threading.Lock()
    latest_frame = [None]  # Use list for mutability
    processed_frame = [None]  # Frame being analyzed/displayed
    running = True

    # Queue for text to speak (ensures sequential processing)
    text_queue = queue.Queue()

    # Start speak_worker in its own thread
    speak_thread = threading.Thread(target=speak_worker, args=(text_queue, frame_lock, latest_frame, processed_frame))
    speak_thread.start()

    # Start camera and display workers in executor
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.submit(camera_worker, running, frame_lock, latest_frame)
        executor.submit(raw_display_worker, latest_frame, running, frame_lock)
        executor.submit(processed_display_worker, processed_frame, running, frame_lock)
        executor.submit(analysis_worker, running, frame_lock, latest_frame, processed_frame, text_queue)

        # Wait for threads to finish (they run while running is True)
        while running:
            time.sleep(1)  # Keep main thread alive

    # Cleanup
    running = False
    text_queue.put(None)
    speak_thread.join()

if __name__ == "__main__":
    main()