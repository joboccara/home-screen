from PIL import ImageFont
from font_utils import FONT_LOCATION

class StartScreenWidget:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, pen):
        starting = "Starting..."
        starting_font = ImageFont.truetype(FONT_LOCATION, 30)
        pen.write((0, 0), starting, starting_font, center_x=self.width, center_y=self.height)