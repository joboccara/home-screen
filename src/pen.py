from PIL import ImageDraw
from font_utils import textwidth, textheight

class Pen:
    def __init__(self, image, offset) -> None:
        self.draw = ImageDraw.Draw(image)
        self.offset = offset

    def write(self, offset, content, font) -> None:
        self.draw.text((self.offset[0] + offset[0], self.offset[1] + offset[1]), content, font=font, fill=0)

    def write_wrapped(self, offset, content, font, max_width):
        line_spacing = font.size / 3
        for index, line in enumerate(wrap_text_to_lines(content, font, max_width)):
            line_height = textheight(line, font) + line_spacing
            line_y = index * line_height
            self.write((offset[0], line_y + offset[1]), line, font)


def wrap_text_to_lines(text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        current_line_with_word = f"{current_line} {word}".strip()
        if textwidth(current_line_with_word, font) <= max_width:
            current_line = current_line_with_word
        else:
            lines.append(current_line)
            current_line = word
    if current_line != "":
        lines.append(current_line)
    return lines