from datetime import datetime
import json
import os
import random
import requests
import chuck_norris_facts

API_KEY = os.getenv("API_NINJAS_API_KEY")

def get_fun_facts():
    today_in_history_url = f"https://api.api-ninjas.com/v1/historicalevents?day={datetime.now().day}&month={datetime.now().month}"
    response = _fetch(today_in_history_url)
    today_in_history = response[random.randint(0, len(response) - 1)] if len(response) > 0 else None

    chuck_norris = chuck_norris_facts.get_fact()

    facts_url = "https://api.api-ninjas.com/v1/facts"
    fact = _fetch(facts_url)[0]["fact"]

    return {
        "today_in_history": today_in_history,
        "chuck_norris": chuck_norris,
        "fact": fact
        }

def _fetch(url):
    return json.loads(requests.get(url, headers={'X-Api-Key': API_KEY}).text)