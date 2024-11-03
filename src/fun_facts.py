from datetime import datetime
import json
import os
import random
import requests

def get_fun_facts():
    api_key = os.getenv("API_NINJAS_API_KEY")
    today_in_history_url = f"https://api.api-ninjas.com/v1/historicalevents?day={datetime.now().day}&month={datetime.now().month}"
    response = json.loads(requests.get(today_in_history_url, headers={'X-Api-Key': api_key}).text)
    today_in_history = response[random.randint(0, len(response) - 1)] if len(response) > 0 else None

    chuck_norris_url = "https://api.api-ninjas.com/v1/chucknorris"
    response = json.loads(requests.get(chuck_norris_url, headers={'X-Api-Key': api_key}).text)
    chuck_norris = response["joke"]

    return {
        "today_in_history": today_in_history,
        "chuck_norris": chuck_norris
        }

