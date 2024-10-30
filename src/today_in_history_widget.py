from PIL import ImageFont
from datetime import datetime
from font_utils import FONT_LOCATION, textsize, textwidth, textheight

def wrap_text_to_lines(text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        current_line_with_word = f"{current_line} {word}".strip()
        this_seems_to_need_an_adjustment_i_dont_know_why = 20
        if textwidth(current_line_with_word, font) <= max_width - this_seems_to_need_an_adjustment_i_dont_know_why:
            current_line = current_line_with_word
        else:
            lines.append(current_line)
            current_line = word
    if current_line != "":
        lines.append(current_line)
    return lines

def write_wrapped(pen, offset, text, font, max_width):
    line_spacing = font.size / 3
    for index, line in enumerate(wrap_text_to_lines(text, font, max_width)):
        line_height = textheight(line, font) + line_spacing
        line_y = index * line_height
        pen.text((offset[0], line_y + offset[1]), line, font)

class TodayInHistoryWidget:
    def draw(self, pen, width):
        year = 1440
        title = f"Today in {year}:"
        title_font = ImageFont.truetype(FONT_LOCATION, 15)
        title_width, title_height = textsize(title, title_font)
        title_x = width / 2 - title_width / 2
        title_y = 0
        pen.text((title_x, title_y), title, title_font)
        
        spacing = 10
 
        content_x = 0
        content_y = title_y + title_height + spacing
        content_font = ImageFont.truetype(FONT_LOCATION, 15)
        write_wrapped(pen,
                      (content_x, content_y),
                      "Emperor Gratian elevates Flavius Theodosius at Sirmium to Augustus, and gives him authority over all the eastern provinces of the Roman Empire.",
                      content_font,
                      width)