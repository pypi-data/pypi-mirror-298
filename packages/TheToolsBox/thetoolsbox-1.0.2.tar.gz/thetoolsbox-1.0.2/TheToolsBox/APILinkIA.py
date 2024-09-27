import requests
from gtts import gTTS
import os

def textToSpeach (text,model = 'Google',langage = 'fr'):
    if model == 'Google':
        textSpeech = gTTS(text=text, lang=langage, slow=False)
        textSpeech.save("Test1.mp3")
        os.popen("Test1.mp3")

