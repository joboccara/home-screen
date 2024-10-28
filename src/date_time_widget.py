from PIL import ImageFont
from datetime import datetime
from font_location import FONT_LOCATION

class DateTimeWidget:
    def draw(self, pen):
        time_string = datetime.now().strftime("%H:%M")
        font = ImageFont.truetype(FONT_LOCATION, 30)
        pen.text((0, 0), time_string, font=font)
