from PIL import ImageFont
from datetime import datetime
from font_utils import FONT_LOCATION, REVERSE_FONT_LOCATION, reverse_script, text_height, text_size, text_width

class DateTimeWidget:
    def __init__(self, zmanim):
        self.time_string = datetime.now().strftime("%H:%M")
        self.time_font = ImageFont.truetype(FONT_LOCATION, 30)
        self.time_width, self.time_height = text_size(self.time_string, self.time_font)

        self.date_string = datetime.now().strftime("%B, %d")
        self.date_font = ImageFont.truetype(FONT_LOCATION, 15)
        self.date_width, self.date_height = text_size(self.date_string, self.date_font)

        self.zmanim = zmanim

    SPACING = 10
    LABEL_TIME_SPACING = 6
    PAR_TIME_SPACING = 10
    ZMANIM_FONT_SIZE = 12
    ZMANIM_VALUE_FONT = ImageFont.truetype(FONT_LOCATION, ZMANIM_FONT_SIZE)
    ZMANIM_LABEL_FONT = ImageFont.truetype(REVERSE_FONT_LOCATION, ZMANIM_FONT_SIZE)

    def draw(self, pen):
        time_x, time_y = 0, 0
        pen.write((time_x, time_y), self.time_string, self.time_font)

        date_y = self.time_height + self.SPACING
        pen.write((time_x, date_y), self.date_string, self.date_font, center_x=self.time_width)

        TEF_LABEL = reverse_script("תפ׳ :")
        tef_time_x = time_x + self.time_width / 2 - self._value_label_width(self.zmanim["tef"], TEF_LABEL) / 2
        tef_time_y = date_y + self.date_height + self.SPACING
        self._draw_value_label(pen, (tef_time_x, tef_time_y), self.zmanim["tef"], TEF_LABEL)

        TZET_LABEL = reverse_script("צ׳׳ה :")
        tzet_time_x = time_x + self.time_width / 2 - self._value_label_width(self.zmanim["tzet"], TZET_LABEL) / 2
        tzet_time_y = tef_time_y + text_height(self.zmanim["tef"], self.ZMANIM_VALUE_FONT) + self.SPACING
        self._draw_value_label(pen, (tzet_time_x, tzet_time_y), self.zmanim["tzet"], TZET_LABEL)

        sh_end_width = text_width(self.zmanim["sh_end"], self.ZMANIM_VALUE_FONT)
        par_width = text_width(self.zmanim["par"], self.ZMANIM_LABEL_FONT)
        sh_start_width = text_width(self.zmanim["sh_start"], self.ZMANIM_VALUE_FONT)
        sh_width = sh_end_width + self.PAR_TIME_SPACING \
                   + par_width + self.PAR_TIME_SPACING \
                   + sh_start_width
        sh_end_x = time_x + self.time_width / 2 - sh_width / 2
        sh_end_y = tzet_time_y + text_height(self.zmanim["tzet"], self.ZMANIM_VALUE_FONT) + self.SPACING
        pen.write((sh_end_x, sh_end_y), self.zmanim["sh_end"], self.ZMANIM_VALUE_FONT)
        par_x = sh_end_x + sh_end_width + self.PAR_TIME_SPACING
        pen.write((par_x, sh_end_y), self.zmanim["par"], self.ZMANIM_LABEL_FONT)
        sh_start_x = par_x + par_width + self.PAR_TIME_SPACING
        pen.write((sh_start_x, sh_end_y), self.zmanim["sh_start"], self.ZMANIM_VALUE_FONT)

    def _value_label_width(self, value, label):
        return text_width(value, self.ZMANIM_VALUE_FONT) + self.LABEL_TIME_SPACING + text_width(label, self.ZMANIM_LABEL_FONT)

    def _draw_value_label(self, pen, offset, value, label):
        pen.write((offset[0], offset[1]), value, self.ZMANIM_VALUE_FONT)
        tef_label_x = offset[0] + text_width(value, self.ZMANIM_VALUE_FONT) + self.LABEL_TIME_SPACING
        pen.write((tef_label_x, offset[1]), label, self.ZMANIM_LABEL_FONT)

    def width(self):
        return max(self.time_width, self.date_width)

    def height(self):
        return self.time_height + self.SPACING \
            + self.date_height + self.SPACING \
            + 3 * (text_height(self.zmanim["tef"], self.ZMANIM_VALUE_FONT) + self.SPACING) - self.SPACING