from date_time_widget import DateTimeWidget
from pen import Pen
from PIL import Image

def generate_screen_image():
    SCREEN_WIDTH = 480
    SCREEN_HEIGHT = 800
    image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
    date_time_x = SCREEN_WIDTH / 2 - DateTimeWidget().width() / 2
    DateTimeWidget().draw(Pen(image, (date_time_x, 50)))
    return image