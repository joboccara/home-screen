from PIL import ImageFont
from font_utils import FONT_LOCATION, REVERSE_FONT_LOCATION, text_height, text_width

class WordOfTheDayWidget:
    FONT_SIZE = 15
    FONT = ImageFont.truetype(FONT_LOCATION, FONT_SIZE)
    REVERSE_FONT = ImageFont.truetype(REVERSE_FONT_LOCATION, FONT_SIZE)
    SPACING = 7

    def __init__(self, word_of_the_day):
        self.words = word_of_the_day.values()
        self.french = word_of_the_day["french"]
        self.english = word_of_the_day["english"]
        self.spanish = word_of_the_day["spanish"]
        self.hebrew = word_of_the_day["hebrew"]

    def draw(self, pen):
        french_y = 0
        pen.write((0, french_y), self.french, self.FONT, center_x=self.width())
        english_y = french_y + + text_height(self.french, self.FONT) + self.SPACING
        pen.write((0, english_y), self.english, self.FONT, center_x=self.width())
        spanish_y = english_y + + text_height(self.english, self.FONT) + self.SPACING
        pen.write((0, spanish_y), self.spanish, self.FONT, center_x=self.width())
        hebrew_y = spanish_y + + text_height(self.spanish, self.FONT) + self.SPACING
        pen.write((0, hebrew_y), self.hebrew, self.REVERSE_FONT, center_x=self.width())

    def width(self):
        return max(text_width(self.french, self.FONT),
                   text_width(self.english, self.FONT),
                   text_width(self.spanish, self.FONT),
                   text_width(self.hebrew, self.REVERSE_FONT))

    def height(self):
        return sum(text_height(self.french, self.FONT),
                   text_height(self.english, self.FONT),
                   text_height(self.spanish, self.FONT),
                   text_height(self.hebrew, self.REVERSE_FONT)) + (len(self.words) - 1) * self.SPACING