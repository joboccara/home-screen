from PIL import ImageDraw

class Pen:
    def __init__(self, image, offset) -> None:
        self.draw = ImageDraw.Draw(image)
        self.offset = offset

    def write(self, offset, content, font) -> None:
        self.draw.text((self.offset[0] + offset[0], self.offset[1] + offset[1]), content, font=font, fill=0)