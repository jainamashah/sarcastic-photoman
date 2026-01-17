import cv2
import sys
import time
import threading

def raw_display_worker(latest_frame, running, frame_lock):

    while running:
        with frame_lock:
            if latest_frame is None:
                continue
            frame = latest_frame.copy()

        cv2.imshow("Raw Camera Feed", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            running = False
            break

def processed_display_worker(latest_frame, running, frame_lock):

    while running:
        with frame_lock:
            if latest_frame is None:
                continue
            frame = latest_frame.copy()

        # ===== PROCESSING HERE TO UNDISTORT FISHEYE ===== #
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)

        cv2.imshow("Processed Camera Feed", edges)

        if cv2.waitKey(1) & 0xFF == 27:
            running = False
            break

    cv2.destroyAllWindows()
