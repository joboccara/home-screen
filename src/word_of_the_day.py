from font_utils import reverse_script
from googletrans import Translator
import json
import requests

def get_word_of_the_day():
    english = json.loads(requests.get("https://random-word-api.vercel.app/api?words=1").text)[0]

    translator = Translator()  
    french = translator.translate(english, dest='fr', src='en').text
    spanish = translator.translate(english, dest='es', src='en').text
    hebrew = reverse_script(translator.translate(english, dest='he', src='en').text)

    return {"english": english, "french": french, "spanish": spanish, "hebrew": hebrew}