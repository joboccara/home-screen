from PIL import Image, ImageDraw
from font_utils import line_spacing, textheight, wrap_text_to_lines

class Pen:
    def __init__(self, image, offset) -> None:
        self.image = image
        self.draw = ImageDraw.Draw(image)
        self.offset = offset

    def write(self, offset, content, font) -> None:
        self.draw.text((self.offset[0] + offset[0], self.offset[1] + offset[1]), content, font=font, fill=0)

    def write_wrapped(self, offset, content, font, max_width):
        for index, line in enumerate(wrap_text_to_lines(content, font, max_width)):
            line_height = textheight(line, font) + line_spacing(font)
            line_y = index * line_height
            self.write((offset[0], line_y + offset[1]), line, font)
    
    def draw_picture(self, offset, filepath, width, height):
        self.image.paste(Image.open(filepath).resize((width, height)), (self.offset[0] + offset[0], self.offset[1] + offset[1]))
