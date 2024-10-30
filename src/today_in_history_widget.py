from datetime import datetime
from font_utils import FONT_LOCATION, textsize, textwidth, textheight
import os
from PIL import ImageFont
import random

class TodayInHistoryWidget:
    def __init__(self, api_access) -> None:
        self.api_access = api_access

    def draw(self, pen, width):
        api_url = f"https://api.api-ninjas.com/v1/historicalevents?day={datetime.now().day}&month={datetime.now().month}"
        response = self.api_access.get(api_url, headers={'X-Api-Key': os.getenv("API_NINJAS_API_KEY")}) 
        fact = response[random.randint(0, len(response) - 1)] if len(response) > 0 else None
        if fact is not None:
            self._display_fact(pen, width, fact)

    def _display_fact(self, pen, width, fact):
        year = fact["year"]
        title = f"Today in {year}:"
        title_font = ImageFont.truetype(FONT_LOCATION, 15)
        title_width, title_height = textsize(title, title_font)
        title_x = width / 2 - title_width / 2
        title_y = 0
        pen.write((title_x, title_y), title, title_font)
        
        spacing = 10

        content_x = 0
        content_y = title_y + title_height + spacing
        content_font = ImageFont.truetype(FONT_LOCATION, 15)
        pen.write_wrapped((content_x, content_y),
                          fact["event"],
                          content_font,
                          width)