from datetime import datetime
from font_utils import FONT_LOCATION, text_size, text_width, text_height, wrapped_text_height
import os
from PIL import ImageFont

class ChuckNorrisWidget:
    def __init__(self, api_access, width) -> None:
        self.width = width
        api_url = "https://api.api-ninjas.com/v1/chucknorris"
        response = api_access.get(api_url, headers={'X-Api-Key': os.getenv("API_NINJAS_API_KEY")}) 
        self.content_font = ImageFont.truetype(FONT_LOCATION, 15)
        self.content = response["joke"]

    SPACING = 10

    def draw(self, pen):
        pen.write_wrapped((0, 0),
                           self.content,
                           self.content_font,
                           self.width)

    def height(self):
        return wrapped_text_height(self.content, self.content_font, self.width)
    