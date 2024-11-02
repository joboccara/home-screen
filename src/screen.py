from buses_times_widget import BusesTimesWidget
from chuck_norris_widget import ChuckNorrisWidget
from date_time_widget import DateTimeWidget
from fact_widget import FactWidget
from weather_widget import WeatherWidget
from today_in_history_widget import TodayInHistoryWidget
from rain_hour_widget import RainHourWidget
from pen import Pen
from PIL import Image
from webdrivers import build_weather_page_driver

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

def generate_screen_image(api_access):
    image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
    date_time_widget = DateTimeWidget()
    date_time_x = SCREEN_WIDTH / 2 - date_time_widget.width() / 2
    date_time_y = 50
    date_time_widget.draw(Pen(image, (date_time_x, date_time_y)))

    spacing = 50

    today_in_history_margin = 10
    today_in_history_x = today_in_history_margin
    today_in_history_y = date_time_y + date_time_widget.height() + spacing
    today_in_history_width = SCREEN_WIDTH - 2 * today_in_history_margin
    today_in_history_widget = TodayInHistoryWidget(api_access, today_in_history_width)
    today_in_history_widget.draw(Pen(image, (today_in_history_x, today_in_history_y)))

    weather_page_driver = build_weather_page_driver()
    next_days_weather = api_access.get_next_days_weather(weather_page_driver)
    try:
        rain_hour_widget = RainHourWidget(api_access, weather_page_driver)
        rain_hour_x = SCREEN_WIDTH / 2 - rain_hour_widget.width() / 2
        rain_hour_y = today_in_history_y + today_in_history_widget.height() + spacing
        rain_hour_widget.draw(Pen(image, (rain_hour_x, rain_hour_y)))

        next_days_weather_widget = WeatherWidget(api_access, next_days_weather)
        next_days_weather_x = SCREEN_WIDTH / 2 - next_days_weather_widget.width() / 2
        next_days_weather_y = rain_hour_y + rain_hour_widget.height() + spacing
        next_days_weather_widget.draw(Pen(image, (next_days_weather_x, next_days_weather_y)))
    finally:
        weather_page_driver.quit()

    chuck_norris_x = today_in_history_margin
    chuck_norris_y = next_days_weather_y + next_days_weather_widget.height() + spacing
    chuck_norris_width = SCREEN_WIDTH - 2 * today_in_history_margin
    chuck_norris_widget = ChuckNorrisWidget(api_access, chuck_norris_width)
    chuck_norris_widget.draw(Pen(image, (chuck_norris_x, chuck_norris_y)))

    buses_times_widget = BusesTimesWidget()
    buses_times_x = SCREEN_WIDTH / 2 - buses_times_widget.width() / 2
    buses_times_y = chuck_norris_y + chuck_norris_widget.height() + spacing
    buses_times_widget.draw(Pen(image, (buses_times_x, buses_times_y)))

    fact_x = today_in_history_margin
    fact_y = buses_times_y + buses_times_widget.height() + spacing
    fact_width = SCREEN_WIDTH - 2 * today_in_history_margin
    fact_widget = FactWidget(api_access, fact_width)
    fact_widget.draw(Pen(image, (fact_x, fact_y)))

    return image