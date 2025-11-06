from buses_times_widget import BusesTimesWidget
from date_time_widget import DateTimeWidget
from weather_widget import WeatherWidget
from omer_widget import OmerWidget
from rain_hour_widget import RainHourWidget
from start_screen_widget import StartScreenWidget
from data import Data
from app_logging import logger
from pen import Pen
from PIL import Image
import time

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

class Screen:
    def __init__(self, api_access):
        self.image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        self.api_access = api_access

    def display(self, display_image):
        try:
            self._clear_image(self.image)
            self._paint_start_screen(self.image)
            display_image(self.image)
        except Exception as e:
            logger.error("Initial display failed", exc_info=e)
            raise

        while(True):
            try:
                data = Data(self.api_access)
                while(True):
                    self._clear_image(self.image)
                    self._paint(self.image, data.get())
                    display_image(self.image)
                    data.refresh()
                    time.sleep(1)
            except Exception as e:
                logger.error("Screen refresh failed", exc_info=e)
                time.sleep(20)

    def _paint(self, image, data):
        spacing = 45

        todays_weather = data["weather"]["days_weather"][0]
        todays_weather_widget = WeatherWidget([todays_weather])
        todays_weather_y = 50

        date_time_widget = DateTimeWidget(data["zmanim"])
        date_time_x = SCREEN_WIDTH / 2 - (date_time_widget.width() + spacing + todays_weather_widget.width()) / 2
        date_time_y = todays_weather_y + todays_weather_widget.height() / 2 - date_time_widget.height() / 2
        date_time_widget.draw(Pen(image, (date_time_x, date_time_y)))

        todays_weather_x = date_time_x + date_time_widget.width() + spacing
        todays_weather_widget.draw(Pen(image, (todays_weather_x, todays_weather_y)))

        rain_hour_widget = RainHourWidget(data["weather"]["rain_intensity_by_datetime"])
        rain_hour_x = SCREEN_WIDTH / 2 - rain_hour_widget.width() / 2
        rain_hour_y = max(date_time_y + date_time_widget.height(), todays_weather_y + todays_weather_widget.height()) + spacing
        rain_hour_widget.draw(Pen(image, (rain_hour_x, rain_hour_y)))

        next_days_weather = data["weather"]["days_weather"][1:]
        next_days_weather_widget = WeatherWidget(next_days_weather)
        next_days_weather_x = SCREEN_WIDTH / 2 - next_days_weather_widget.width() / 2
        next_days_weather_y = rain_hour_y + rain_hour_widget.height() + spacing
        next_days_weather_widget.draw(Pen(image, (next_days_weather_x, next_days_weather_y)))

        buses_times_widget = BusesTimesWidget(data["buses_times"])
        buses_times_x = SCREEN_WIDTH / 2 - buses_times_widget.width() / 2
        buses_times_y = next_days_weather_y + next_days_weather_widget.height() + spacing
        buses_times_widget.draw(Pen(image, (buses_times_x, buses_times_y)))

        if data["zmanim"]["omer_day"] != "":
            omer_extra_spacing = 60
            omer_widget = OmerWidget(data["zmanim"]["omer_day"])
            omer_x = SCREEN_WIDTH / 2 - omer_widget.width() / 2
            omer_y = buses_times_y + buses_times_widget.height() + spacing + omer_extra_spacing
            omer_widget.draw(Pen(image, (omer_x, omer_y)))

    def _clear_image(self, image):
        image.paste(Image.new("RGB", image.size, "white"))

    def _paint_start_screen(self, image):
        StartScreenWidget(SCREEN_WIDTH, SCREEN_HEIGHT).draw(Pen(image, (0, 0)))