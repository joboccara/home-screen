from PIL import ImageFont
from datetime import datetime
from font_utils import FONT_LOCATION, text_size

class DateTimeWidget:
    def __init__(self):
        self.time_string = datetime.now().strftime("%H:%M")
        self.time_font = ImageFont.truetype(FONT_LOCATION, 60)
        self.time_width, self.time_height = text_size(self.time_string, self.time_font)

        self.date_string = datetime.now().strftime("%B, %d")
        self.date_font = ImageFont.truetype(FONT_LOCATION, 20)
        self.date_width, self.date_height = text_size(self.date_string, self.date_font)

    SPACING = 10

    def draw(self, pen):
        time_x, time_y = 0, 0
        pen.write((time_x, time_y), self.time_string, self.time_font)

        date_y = self.time_height + self.SPACING
        pen.write((time_x, date_y), self.date_string, self.date_font, center_x=self.time_width)

    def width(self):
        return max(self.time_width, self.date_width)

    def height(self):
        return self.time_height + self.SPACING + self.date_height