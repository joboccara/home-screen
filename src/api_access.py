from datetime import datetime
import json
import requests
from bus_times import get_buses_times
from rain_hour_scraping import scrape_rain_hour
from weather_scraping import scrape_weather
from zmanim_scraping import scrape_zmanim

class ApiAccess:
    def get(self, url, headers):
        response = requests.get(url, headers)
        return json.loads(response.text)

    def get_rain_intensity_by_datetime(self, driver):
        return scrape_rain_hour(driver)

    def get_weather(self, driver):
        return scrape_weather(driver)

    def get_zmanim(self, driver):
        return scrape_zmanim(driver)

    def get_buses_times(self):
        return get_buses_times()
    
class FakeApiAccess:
    def get(self, url, headers):
        if url.startswith("https://api.api-ninjas.com/v1/historicalevents"):
            return [{"year": 1440, "event": "Emperor Gratian elevates Flavius Theodosius at Sirmium to Augustus, and gives him authority over all the eastern provinces of the Roman Empire."}]
        elif url == "https://api.api-ninjas.com/v1/chucknorris":
            return { "joke": "The dinosaurs looked at Chuck Norris the wrong way once. You know what happened to them." } 
        elif url:
            return [ { "fact": "After the Eiffel Tower was built, one person was killed during the installation of the lifts. No one was killed during the actual construction of the tower" } ]
        else:
            return {}

    def get_rain_intensity_by_datetime(self, driver):
        return {
            datetime(1900, 1, 1, 18, 25): 3,
            datetime(1900, 1, 1, 18, 30): 0,
            datetime(1900, 1, 1, 18, 35): 0,
            datetime(1900, 1, 1, 18, 40): 2,
            datetime(1900, 1, 1, 18, 45): 1,
            datetime(1900, 1, 1, 18, 50): 3,
            datetime(1900, 1, 1, 18, 55): 0,
            datetime(1900, 1, 1, 19, 5): 0,
            datetime(1900, 1, 1, 19, 15): 1,
        }

    def get_weather(self, driver):
        return scrape_weather(driver)

    def get_zmanim(self, driver):
        return scrape_zmanim(driver)

    def get_buses_times(self):
        return get_buses_times()