from preprocess.local_checks import *
from Final.TTS_worker import speak
from Processing.analyze_image import llm_response, encode_image
import time
from concurrent.futures import ThreadPoolExecutor
from preprocess.frame_capture_worker import frame_cap, show_frame

def main():
    """Pipeline: frame capture -> local checks -> text-to-speech"""

    executor = ThreadPoolExecutor(max_workers=2)    

    while True:

        frame_cap()

        if (face_check("temp.jpg") and eyes_open_check("temp.jpg") and isnt_blurry("temp.jpg")>30 == False):
            continue

        base64_image = encode_image("temp.jpg")

        with ThreadPoolExecutor(max_workers=1) as executor:
            futures = executor.submit(llm_response,base64_image)
            print("waiting for llm response\n")
            response = futures.result()

        with ThreadPoolExecutor(max_workers=1) as executor:
            futures = executor.submit(speak, response)
            print("waiting for speaking\n")

        print("all done, moving on\n")

        if ("Accepted" in response or "accepted" in response):
            break

    cv2.imshow("Final Frame", frame)
    cv2.waitKey(0)

if __name__ == "__main__":
    result = main()