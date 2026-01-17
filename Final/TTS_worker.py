from gtts import gTTS
from io import BytesIO
import pygame
import time

openAI_API_key = "----"

pygame.mixer.init()

def speak(text):
    pygame.mixer.music.stop()
    tts = gTTS(text, lang="en")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    speech_time = sleep_time = 0.4 + (len(text.split()) / 2.5)
    time.sleep(speech_time)

# Example usage
# speak("Smile a little")
# speak("Perfect")


