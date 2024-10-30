from datetime import datetime
from font_utils import FONT_LOCATION, textsize, textwidth, textheight, wrapped_text_height
import os
from PIL import ImageFont
import random

class TodayInHistoryWidget:
    def __init__(self, api_access, width) -> None:
        self.width = width
        api_url = f"https://api.api-ninjas.com/v1/historicalevents?day={datetime.now().day}&month={datetime.now().month}"
        response = api_access.get(api_url, headers={'X-Api-Key': os.getenv("API_NINJAS_API_KEY")}) 
        self.fact = response[random.randint(0, len(response) - 1)] if len(response) > 0 else None

        if self.fact is not None:
            year = self.fact["year"]
            self.title = f"Today in {year}:"
            self.title_font = ImageFont.truetype(FONT_LOCATION, 15)
            self.title_width, self.title_height = textsize(self.title, self.title_font)

            self.content_font = ImageFont.truetype(FONT_LOCATION, 15)
            self.content = self.fact["event"]

    SPACING = 10

    def draw(self, pen):
        if self.fact is not None:
            title_x = self.width / 2 - self.title_width / 2
            title_y = 0
            pen.write((title_x, title_y), self.title, self.title_font)
            
            content_x = 0
            content_y = title_y + self.title_height + self.SPACING
            pen.write_wrapped((content_x, content_y),
                              self.content,
                              self.content_font,
                              self.width)

    def height(self):
        if self.fact is None: return 0
        return self.title_height + self.SPACING + wrapped_text_height(self.content, self.content_font, self.width)