from date_time_widget import DateTimeWidget
from today_in_history_widget import TodayInHistoryWidget
from rain_hour_widget import RainHourWidget
from pen import Pen
from PIL import Image

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

    rain_hour_x = 50
    rain_hour_y = today_in_history_y + today_in_history_widget.height() + spacing
    RainHourWidget().draw(Pen(image, (rain_hour_x, rain_hour_y)))

    return image