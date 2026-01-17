import cv2
import sys
import time
import threading

def camera_worker(running, frame_lock, latest_frame):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while running: 
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            continue
        with frame_lock:
            latest_frame[0] = frame
    
    cap.release()
