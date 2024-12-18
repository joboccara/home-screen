from buses_times_widget import BusesTimesWidget
from chuck_norris_widget import ChuckNorrisWidget
from date_time_widget import DateTimeWidget
from fact_widget import FactWidget
from weather_widget import WeatherWidget
from rain_hour_widget import RainHourWidget
from start_screen_widget import StartScreenWidget
from word_of_the_day_widget import WordOfTheDayWidget
from data import Data
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
        self._clear_image(self.image)
        self._paint_start_screen(self.image)
        display_image(self.image)
        while(True):
            try:
                data = Data(self.api_access)
                while(True):
                    self._clear_image(self.image)
                    self._paint(self.image, data.get())
                    display_image(self.image)
                    data.refresh()
                    time.sleep(1)
            except:
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

        middle_spacing = 60
        facts_margin = 10
        facts_spacing = 30

        fact_x = facts_margin
        fact_y = buses_times_y + buses_times_widget.height() + middle_spacing
        fact_width = SCREEN_WIDTH - 2 * facts_margin
        fact_widget = FactWidget(data["fun_facts"], fact_width)
        fact_widget.draw(Pen(image, (fact_x, fact_y)))

        chuck_norris_x = facts_margin
        chuck_norris_y = fact_y + fact_widget.height() + facts_spacing
        chuck_norris_width = SCREEN_WIDTH - 2 * facts_margin
        chuck_norris_widget = ChuckNorrisWidget(data["fun_facts"], chuck_norris_width)
        chuck_norris_widget.draw(Pen(image, (chuck_norris_x, chuck_norris_y)))

        word_of_the_day_widget = WordOfTheDayWidget(data["word_of_the_day"])
        word_of_the_day_x = SCREEN_WIDTH / 2 - word_of_the_day_widget.width() / 2
        word_of_the_day_y = chuck_norris_y + chuck_norris_widget.height() + facts_spacing
        word_of_the_day_widget.draw(Pen(image, (word_of_the_day_x, word_of_the_day_y)))

    def _clear_image(self, image):
        image.paste(Image.new("RGB", image.size, "white"))

    def _paint_start_screen(self, image):
        StartScreenWidget(SCREEN_WIDTH, SCREEN_HEIGHT).draw(Pen(image, (0, 0)))