from preprocess.local_checks import *
from workers.TTS_worker import speak_worker
from Processing.analyze_image import llm_response, encode_image
import time
from concurrent.futures import ThreadPoolExecutor
from workers.camera_worker import camera_worker
from workers.processing_worker import raw_display_worker, processed_display_worker
import threading
import queue  # Add this import

def main():
    """Pipeline: frame capture -> local checks -> text-to-speech"""

    # Shared state
    frame_lock = threading.Lock()
    latest_frame = None
    running = True

    # Queue for text to speak (ensures sequential processing)
    text_queue = queue.Queue()

    # Start speak_worker in its own thread
    speak_thread = threading.Thread(target=speak_worker, args=(text_queue,))
    speak_thread.start()

    # Camera capture loop (simplified for clarity)
    cap = cv2.VideoCapture(0)  # Assuming cv2 is imported
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    try:
        while running:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                continue

            with frame_lock:
                latest_frame = frame

            # Analyze the frame (you may want to throttle this, e.g., every few seconds)
            if latest_frame is not None:
                # Encode and get LLM response
                cv2.imwrite("temp.jpg",latest_frame)
                encoded_image = encode_image("temp.jpg")  # Save frame to temp file if needed
                response = llm_response(encoded_image)
                text_queue.put(response)  # Send to speak_worker (blocks if queue is full, but unlikely)

            # Display workers (run in executor as before)
            with ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(raw_display_worker, latest_frame, running, frame_lock)
                executor.submit(processed_display_worker, latest_frame, running, frame_lock)

            time.sleep(0.1)  # Adjust loop speed

    finally:
        running = False
        text_queue.put(None)  # Signal speak_worker to stop
        speak_thread.join()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()