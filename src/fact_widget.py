from datetime import datetime
from font_utils import FONT_LOCATION, text_size, text_width, text_height, wrapped_text_height
import os
from PIL import ImageFont

class FactWidget:
    def __init__(self, fun_facts, width) -> None:
        self.width = width
        self.content_font = ImageFont.truetype(FONT_LOCATION, 15)
        self.content = fun_facts["fact"]

    SPACING = 10

    def draw(self, pen):
        pen.write_wrapped((0, 0),
                           self.content,
                           self.content_font,
                           self.width)

    def height(self):
        return wrapped_text_height(self.content, self.content_font, self.width)
    
