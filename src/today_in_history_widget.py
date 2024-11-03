from datetime import datetime
from font_utils import FONT_LOCATION, text_size, text_width, text_height, wrapped_text_height
from PIL import ImageFont

class TodayInHistoryWidget:
    def __init__(self, fun_facts, width) -> None:
        self.width = width
        self.fact = fun_facts["today_in_history"]

        if self.fact is not None:
            year = self.fact["year"]
            self.title = f"Today in {year}:"
            self.title_font = ImageFont.truetype(FONT_LOCATION, 15)
            self.title_width, self.title_height = text_size(self.title, self.title_font)

            self.content_font = ImageFont.truetype(FONT_LOCATION, 15)
            self.content = self.fact["event"]

    SPACING = 10

    def draw(self, pen):
        if self.fact is not None:
            pen.write((0, 0), self.title, self.title_font, center_x=self.width)
            
            content_x = 0
            content_y = self.title_height + self.SPACING
            pen.write_wrapped((content_x, content_y),
                              self.content,
                              self.content_font,
                              self.width)

    def height(self):
        if self.fact is None: return 0
        return self.title_height + self.SPACING + wrapped_text_height(self.content, self.content_font, self.width)