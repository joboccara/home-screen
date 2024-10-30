from PIL import ImageFont
from datetime import datetime
from font_utils import FONT_LOCATION, textsize, textwidth, textheight

class TodayInHistoryWidget:
    def draw(self, pen, width):
        year = 1440
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
        pen.write_wrapped(pen,
                          (content_x, content_y),
                          "Emperor Gratian elevates Flavius Theodosius at Sirmium to Augustus, and gives him authority over all the eastern provinces of the Roman Empire.",
                          content_font,
                          width)