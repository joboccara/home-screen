from datetime import datetime
from datetime import timedelta
from webdrivers import build_calj_driver, build_weather_page_driver

class Data:
    def __init__(self, api_access):
        self._api_access = api_access
        weather_page_driver = build_weather_page_driver()
        calj_driver = build_calj_driver()

        self._refreshers = [
            Refresher(timedelta(minutes=10), self.weather_refresh),
            Refresher(timedelta(minutes=21), self.zmanim_refresh),
            Refresher(timedelta(hours=12), self.fun_facts_refresh),
            Refresher(timedelta(seconds=50), self.buses_times_refresh)
        ]
        self._data = {
            "weather_page_driver": weather_page_driver,
            "calj_driver": calj_driver,
            }
        self.refresh()

    def get(self):
        return self._data

    def refresh(self):
        for refresher in self._refreshers:
            refresher.refresh(self._data)

    def close(self):
        self._data["weather_page_driver"].quit()
        self._data["calj_driver"].quit()

    def weather_refresh(self, data):
        data["weather_page_driver"].refresh()
        data["weather"] = self._api_access.get_weather(data["weather_page_driver"])
        data["rain_intensity_by_datetime"] = self._api_access.get_rain_intensity_by_datetime(data["weather_page_driver"])

    def zmanim_refresh(self, data):
        data["calj_driver"].refresh()
        data["zmanim"] = self._api_access.get_zmanim(data["calj_driver"])

    def fun_facts_refresh(self, data):
        data["fun_facts"] = self._api_access.get_fun_facts()

    def buses_times_refresh(self, data):
        data["buses_times"] = self._api_access.get_buses_times()

class Refresher:
    def __init__(self, period, refresh):
        self._period = period
        self._refresh = refresh
        self._last_updated = None

    def refresh(self, data):
        if self._last_updated is None or datetime.now() > self._last_updated + self._period:
            self._last_updated = datetime.now()
            print(datetime.now(), self._refresh.__name__)
            self._refresh(data)

