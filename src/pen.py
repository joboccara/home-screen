from PIL import ImageDraw
from font_utils import line_spacing, text_height, text_width, wrap_text_to_lines

class Pen:
    def __init__(self, image, offset) -> None:
        self.image = image
        self.draw = ImageDraw.Draw(image)
        self.offset = offset

    def write(self, offset, content, font, center_x=0, center_y=0) -> None:
        offset_x = int(self.offset[0]) + int(offset[0])
        offset_y = int(self.offset[1]) + int(offset[1])
        if center_x > 0:
            write_x = offset_x + center_x / 2 - text_width(content, font) / 2
        else:
            write_x = offset_x
        if center_y > 0:
            write_y = offset_y + center_y / 2 - text_height(content, font) / 2
        else:
            write_y = offset_y
        self.draw.text((write_x, write_y), content, font=font, fill=0)

    def write_wrapped(self, offset, content, font, max_width):
        for index, line in enumerate(wrap_text_to_lines(content, font, max_width)):
            line_height = text_height(line, font) + line_spacing(font)
            line_y = index * line_height
            self.write((offset[0], line_y + int(offset[1])), line, font)
    
    def draw_picture(self, offset, image):
        self.image.paste(image, (int(self.offset[0]) + int(offset[0]), int(self.offset[1]) + int(offset[1])))
