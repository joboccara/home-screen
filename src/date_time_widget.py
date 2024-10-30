from PIL import ImageFont
from datetime import datetime
from font_utils import FONT_LOCATION, textsize

class DateTimeWidget:
    def __init__(self):
        self.time_string = datetime.now().strftime("%H:%M")
        self.time_font = ImageFont.truetype(FONT_LOCATION, 60)
        self.time_width, self.time_height = textsize(self.time_string, self.time_font)

        self.date_string = datetime.now().strftime("%B, %d")
        self.date_font = ImageFont.truetype(FONT_LOCATION, 20)
        self.date_width, _ = textsize(self.date_string, self.date_font)

    def draw(self, pen):
        time_x, time_y = 0, 0
        pen.text((time_x, time_y), self.time_string, self.time_font)

        date_x = time_x + self.time_width / 2 - self.date_width / 2
        spacing = 10
        date_y = self.time_height + spacing
        pen.text((date_x, date_y), self.date_string, self.date_font)

    def width(self):
        return max(self.time_width, self.date_width)

