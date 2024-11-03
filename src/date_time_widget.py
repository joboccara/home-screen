from PIL import ImageFont
from datetime import datetime
from font_utils import FONT_LOCATION, REVERSE_FONT_LOCATION, text_height, text_size, text_width
from selenium.webdriver.common.by import By
from webdrivers import build_calj_driver

class DateTimeWidget:
    def __init__(self):
        self.time_string = datetime.now().strftime("%H:%M")
        self.time_font = ImageFont.truetype(FONT_LOCATION, 30)
        self.time_width, self.time_height = text_size(self.time_string, self.time_font)

        self.date_string = datetime.now().strftime("%B, %d")
        self.date_font = ImageFont.truetype(FONT_LOCATION, 15)
        self.date_width, self.date_height = text_size(self.date_string, self.date_font)

        self.zmanim = self._get_zmanim()

    def _get_zmanim(self):
        driver = build_calj_driver()
        try:
            tef_time = self._find_time_from_label(driver, "début tefilin")
            tzet_time = self._find_time_from_label(driver, "tzeit hacokhavim")

            sh_start_label_span = driver.find_element(By.XPATH, "//*[text() = 'allumage avant :']")
            sh_start_time = sh_start_label_span.find_element(By.XPATH, "../../../*[3]/*[1]/*[1]").text
            sh_end_time = sh_start_label_span.find_element(By.XPATH, "../../../*[3]/*[2]/*[1]").text
            par = sh_start_label_span.find_element(By.XPATH, "../../../../../../../*[3]/*[1]/*[2]").text
            
            result = {"tef": tef_time, "tzet": tzet_time, "sh_start": sh_start_time, "sh_end": sh_end_time, "par": par}
        except:
            result = {"error": True}
        finally:
            driver.quit()
            return result

    def _find_time_from_label(self, driver, label):
        tef_label_a = driver.find_element(By.XPATH, f"//*[text() = '{label}']")
        return tef_label_a.find_element(By.XPATH, "../../*[2]").text

    SPACING = 10
    LABEL_TIME_SPACING = 2
    ZMANIM_FONT_SIZE = 10
    ZMANIM_VALUE_FONT = ImageFont.truetype(FONT_LOCATION, ZMANIM_FONT_SIZE)
    ZMANIM_LABEL_FONT = ImageFont.truetype(REVERSE_FONT_LOCATION, ZMANIM_FONT_SIZE)

    def draw(self, pen):
        time_x, time_y = 0, 0
        pen.write((time_x, time_y), self.time_string, self.time_font)

        date_y = self.time_height + self.SPACING
        pen.write((time_x, date_y), self.date_string, self.date_font, center_x=self.time_width)

        TEF_LABEL = "תפ׳ :"[::-1]
        tef_time_x = time_x + self.time_width / 2 - self._value_label_width(self.zmanim["tef"], TEF_LABEL) / 2
        tef_time_y = date_y + self.date_height + self.SPACING
        self._draw_value_label(pen, (tef_time_x, tef_time_y), self.zmanim["tef"], TEF_LABEL)

    def _draw_value_label(self, pen, offset, value, label):
        tef_width = self._value_label_width(value, label)
        pen.write((offset[0], offset[1]), value, self.ZMANIM_VALUE_FONT)
        tef_label_x = offset[0] + text_width(value, self.ZMANIM_VALUE_FONT) + self.LABEL_TIME_SPACING
        pen.write((tef_label_x, offset[1]), label, self.ZMANIM_LABEL_FONT)

    def _value_label_width(self, value, label):
        return text_width(value, self.ZMANIM_VALUE_FONT) + self.LABEL_TIME_SPACING + text_width(label, self.ZMANIM_LABEL_FONT)


    def width(self):
        return max(self.time_width, self.date_width)

    def height(self):
        return self.time_height + self.SPACING + self.date_height