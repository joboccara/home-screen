from datetime import datetime
import os
from PIL import Image, ImageFont
from font_utils import FONT_LOCATION, text_height, text_width

class RainHourWidget:
    ICON_SIZE = 25
    ICON_SPACING = 5
    TITLE_SPACING = 20
    DASH = "-"
    NO_RAIN_LABEL = "No rain in the hour"
    TITLE = "Rain in the hour:"
    TITLE_FONT = ImageFont.truetype(FONT_LOCATION, 15)

    def __init__(self, api_access, weather_page_driver):
        self.rain_intensity_by_datetime = api_access.get_rain_intensity_by_datetime(weather_page_driver)

    def draw(self, pen):
        if self.rains_in_the_hour():
            title_height = text_height(self.TITLE, self.TITLE_FONT)
            title_x = 0
            pen.write((0, 0), self.TITLE, self.TITLE_FONT, center_y=self.height())
            offset_x = text_width(self.TITLE, self.TITLE_FONT) + self.TITLE_SPACING
            self._draw_rain_images(pen, self.rain_intensity_by_datetime, offset_x)
            self._draw_time_labels(pen, self.rain_intensity_by_datetime, offset_x, offset_y=self.ICON_SIZE + self.ICON_SPACING)
        else:
            pen.write((0, 0), self.NO_RAIN_LABEL, self.TITLE_FONT, center_x=self.width())

    def width(self):
        if self.rains_in_the_hour():
            title_width = text_width(self.TITLE, self.TITLE_FONT)
            rain_images_width = len(self.rain_intensity_by_datetime.items()) * (self.ICON_SIZE + self.ICON_SPACING) - self.ICON_SPACING
            return title_width + self.TITLE_SPACING + rain_images_width
        else:
            return text_width(self.NO_RAIN_LABEL, self.TITLE_FONT)

    def height(self):
        if self.rains_in_the_hour():
            return self.ICON_SIZE
        else:
            return text_height(self.NO_RAIN_LABEL, self.TITLE_FONT)

    def rains_in_the_hour(self):
        return any(value != 0 for value in self.rain_intensity_by_datetime.values())

    def _draw_rain_images(self, pen, rain_intensity_by_datetime, offset_x):
        light_rain, medium_rain, heavy_rain = self._rain_images()
        dash_font = ImageFont.truetype(FONT_LOCATION, 15)
        for index, rain_intensity in enumerate(rain_intensity_by_datetime.values()):
            x = offset_x + (self.ICON_SIZE + self.ICON_SPACING) * index
            y = 0
            if rain_intensity == 0:
                pen.write((x, y), self.DASH, dash_font, center_x=self.ICON_SIZE, center_y=self.ICON_SIZE)
            elif rain_intensity == 1:
                pen.draw_picture((x, y), light_rain)
            elif rain_intensity == 2:
                pen.draw_picture((x, y), medium_rain)
            elif rain_intensity == 3:
                pen.draw_picture((x, y), heavy_rain)

    def _draw_time_labels(self, pen, rain_intensity_by_datetime, offset_x, offset_y):
        minutes_font = ImageFont.truetype(FONT_LOCATION, 10)
        for index, datetime in enumerate(rain_intensity_by_datetime.keys()):
            minute_label = datetime.strftime("%H:%M" if index == 0 else "%M")
            x = offset_x + self.minute_label_x(index, minute_label, minutes_font)
            y = offset_y
            pen.write((x, y), minute_label, minutes_font)

    def minute_label_x(self, index, minute_label, minutes_font):
        return index * (self.ICON_SIZE + self.ICON_SPACING) + self.ICON_SIZE / 2 - text_width(minute_label, minutes_font) / 2

    def _rain_images(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        light_rain_path = os.path.join(current_path, "images/light-rain.png")
        light_rain = Image.open(light_rain_path).resize((self.ICON_SIZE, self.ICON_SIZE))
        medium_rain_path = os.path.join(current_path, "images/medium-rain.png")
        medium_rain = Image.open(medium_rain_path).resize((self.ICON_SIZE, self.ICON_SIZE))
        heavy_rain_path = os.path.join(current_path, "images/heavy-rain.png")
        heavy_rain = Image.open(heavy_rain_path).resize((self.ICON_SIZE, self.ICON_SIZE))
        return [light_rain, medium_rain, heavy_rain]