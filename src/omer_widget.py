from PIL import ImageFont
from font_utils import FONT_LOCATION, REVERSE_FONT_LOCATION, reverse_script, text_height, text_width

class OmerWidget:
    SPACING = 25
    FONT_SIZE = 100
    DAY_FONT = ImageFont.truetype(FONT_LOCATION, FONT_SIZE)
    LABEL_FONT = ImageFont.truetype(REVERSE_FONT_LOCATION, FONT_SIZE)
    OMER_LABEL = reverse_script("עומר")
    def __init__(self, omer_day):
        self.omer_day = omer_day

    def draw(self, pen):
        day_x = 0
        pen.write((day_x, 0), self.omer_day, self.DAY_FONT)
        omer_x = day_x + text_width(self.omer_day, self.DAY_FONT) + self.SPACING
        pen.write((omer_x, 0), self.OMER_LABEL, self.LABEL_FONT)

    def width(self):
        return text_width(self.omer_day, self.DAY_FONT) + self.SPACING + text_width(self.OMER_LABEL, self.LABEL_FONT)

    def height(self):
        return max(
            text_height(self.omer_day, self.DAY_FONT),
            text_height(self.OMER_LABEL, self.LABEL_FONT)
        )