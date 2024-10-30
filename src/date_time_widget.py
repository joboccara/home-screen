from PIL import ImageFont
from datetime import datetime
from font_utils import FONT_LOCATION, textsize

class DateTimeWidget:
    def draw(self, pen):
        time_string = datetime.now().strftime("%H:%M")
        time_font = ImageFont.truetype(FONT_LOCATION, 60)
        time_x, time_y = 0, 0
        pen.text((time_x, time_y), time_string, time_font)

        date_font = ImageFont.truetype(FONT_LOCATION, 20)
        date_string = datetime.now().strftime("%B, %d")
        time_width, time_height = textsize(time_string, time_font)
        date_width, _ = textsize(date_string, date_font)
        date_x = time_x + time_width / 2 - date_width / 2
        spacing = 10
        date_y = time_height + spacing
        pen.text((date_x, date_y), date_string, date_font)

    def width(self):
        time_string = datetime.now().strftime("%H:%M")
        time_font = ImageFont.truetype(FONT_LOCATION, 60)
        time_width, _ = textsize(time_string, time_font)

        date_font = ImageFont.truetype(FONT_LOCATION, 20)
        date_string = datetime.now().strftime("%B, %d")
        date_width, _ = textsize(date_string, date_font)

        return max(time_width, date_width)
