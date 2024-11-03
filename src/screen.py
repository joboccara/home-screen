from buses_times_widget import BusesTimesWidget
from chuck_norris_widget import ChuckNorrisWidget
from date_time_widget import DateTimeWidget
from fact_widget import FactWidget
from weather_widget import WeatherWidget
from today_in_history_widget import TodayInHistoryWidget
from rain_hour_widget import RainHourWidget
from pen import Pen
from PIL import Image
from webdrivers import build_calj_driver, build_weather_page_driver

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

class Screen:
    def __init__(self, api_access):
        self.image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        self.api_access = api_access

    def display(self, display_image):
        while(True):
            data = self._init_data()
            try:
                while(True):
                    self._clear_image(self.image)
                    self._paint(self.image, data)
                    display_image(self.image)
                    self._refresh_data(data)
            finally:
                self._close_data(data)

    def _init_data(self):
        weather_page_driver = build_weather_page_driver()
        calj_driver = build_calj_driver()
        return {
            "weather_page_driver": weather_page_driver,
            "weather": self.api_access.get_weather(weather_page_driver),
            "rain_intensity_by_datetime": self.api_access.get_rain_intensity_by_datetime(weather_page_driver),
            "calj_driver": calj_driver,
            "zmanim": self.api_access.get_zmanim(calj_driver),
            "fun_facts": self.api_access.get_fun_facts()
            }

    def _refresh_data(self, data):
        data["weather_page_driver"].refresh()
        data["weather"] = self.api_access.get_weather(data["weather_page_driver"])
        data["rain_intensity_by_datetime"] = self.api_access.get_rain_intensity_by_datetime(data["weather_page_driver"])
        data["calj_driver"].refresh()
        data["zmanim"] = self.api_access.get_zmanim(data["calj_driver"])
        data["fun_facts"] = self.api_access.get_fun_facts()

    def _close_data(self, data):
        data["weather_page_driver"].quit()
        data["calj_driver"].quit()

    def _paint(self, image, data):
        spacing = 45

        todays_weather = data["weather"][0]
        todays_weather_widget = WeatherWidget(self.api_access, [todays_weather])
        todays_weather_y = 50

        date_time_widget = DateTimeWidget(data["zmanim"])
        date_time_x = SCREEN_WIDTH / 2 - (date_time_widget.width() + spacing + todays_weather_widget.width()) / 2
        date_time_y = todays_weather_y + todays_weather_widget.height() / 2 - date_time_widget.height() / 2
        date_time_widget.draw(Pen(image, (date_time_x, date_time_y)))

        todays_weather_x = date_time_x + date_time_widget.width() + spacing
        todays_weather_widget.draw(Pen(image, (todays_weather_x, todays_weather_y)))

        today_in_history_margin = 10
        today_in_history_x = today_in_history_margin
        today_in_history_y = max(date_time_y + date_time_widget.height(), todays_weather_y + todays_weather_widget.height()) + spacing
        today_in_history_width = SCREEN_WIDTH - 2 * today_in_history_margin
        today_in_history_widget = TodayInHistoryWidget(data["fun_facts"], today_in_history_width)
        today_in_history_widget.draw(Pen(image, (today_in_history_x, today_in_history_y)))

        rain_hour_widget = RainHourWidget(data["rain_intensity_by_datetime"])
        rain_hour_x = SCREEN_WIDTH / 2 - rain_hour_widget.width() / 2
        rain_hour_y = today_in_history_y + today_in_history_widget.height() + spacing
        rain_hour_widget.draw(Pen(image, (rain_hour_x, rain_hour_y)))

        next_days_weather = data["weather"][1:]
        next_days_weather_widget = WeatherWidget(self.api_access, next_days_weather)
        next_days_weather_x = SCREEN_WIDTH / 2 - next_days_weather_widget.width() / 2
        next_days_weather_y = rain_hour_y + rain_hour_widget.height() + spacing
        next_days_weather_widget.draw(Pen(image, (next_days_weather_x, next_days_weather_y)))

        chuck_norris_x = today_in_history_margin
        chuck_norris_y = next_days_weather_y + next_days_weather_widget.height() + spacing
        chuck_norris_width = SCREEN_WIDTH - 2 * today_in_history_margin
        chuck_norris_widget = ChuckNorrisWidget(data["fun_facts"], chuck_norris_width)
        chuck_norris_widget.draw(Pen(image, (chuck_norris_x, chuck_norris_y)))

        buses_times_widget = BusesTimesWidget()
        buses_times_x = SCREEN_WIDTH / 2 - buses_times_widget.width() / 2
        buses_times_y = chuck_norris_y + chuck_norris_widget.height() + spacing
        buses_times_widget.draw(Pen(image, (buses_times_x, buses_times_y)))

        fact_x = today_in_history_margin
        fact_y = buses_times_y + buses_times_widget.height() + spacing
        fact_width = SCREEN_WIDTH - 2 * today_in_history_margin
        fact_widget = FactWidget(data["fun_facts"], fact_width)
        fact_widget.draw(Pen(image, (fact_x, fact_y)))

    def _clear_image(self, image):
        image.paste(Image.new("RGB", image.size, "white"))