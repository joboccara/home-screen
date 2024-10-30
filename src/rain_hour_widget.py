from datetime import datetime
import os
from PIL import Image, ImageFont
from font_utils import FONT_LOCATION, text_height, text_width

class RainHourWidget:
    ICON_SIZE = 25
    ICON_SPACING = 5
    DASH = "-"

    def draw(self, pen):
        rain_intensity_by_datetime = self._fetch_rain_intensity_by_datetime()
        self._draw_rain_images(pen, rain_intensity_by_datetime)
        self._draw_time_labels(pen, rain_intensity_by_datetime, offset_y=self.ICON_SIZE + self.ICON_SPACING)

    def _draw_rain_images(self, pen, rain_intensity_by_datetime):
        light_rain, medium_rain, heavy_rain = self._rain_images()
        dash_font = ImageFont.truetype(FONT_LOCATION, 15)
        for index, rain_intensity in enumerate(rain_intensity_by_datetime.values()):
            x = (self.ICON_SIZE + self.ICON_SPACING) * index
            y = 0
            if rain_intensity == 0:
                dash_x = x + self.ICON_SIZE / 2 - text_width(self.DASH, dash_font) / 2
                dash_y = y + self.ICON_SIZE / 2 - text_height(self.DASH, dash_font) / 2
                pen.write((dash_x, dash_y), self.DASH, dash_font)
            elif rain_intensity == 1:
                pen.draw_picture((x, y), light_rain)
            elif rain_intensity == 2:
                pen.draw_picture((x, y), medium_rain)
            elif rain_intensity == 3:
                pen.draw_picture((x, y), heavy_rain)

    def _draw_time_labels(self, pen, rain_intensity_by_datetime, offset_y):
        minutes_font = ImageFont.truetype(FONT_LOCATION, 10)
        for index, datetime in enumerate(rain_intensity_by_datetime.keys()):
            minute_label = datetime.strftime("%H:%M" if index == 0 else "%M")
            x = self.minute_label_x(index, minute_label, minutes_font)
            y = offset_y
            pen.write((x, y), minute_label, minutes_font)
        # first_datetime = next(iter(rain_intensity_by_datetime.keys()))
        # first_label_minutes_x = self.minute_label_x(0, first_datetime.strftime("%M"), minutes_font)
        # first_label_hour = f"{first_datetime.strftime("%H")}:"
        # first_label_hour_x = first_label_minutes_x - text_width(first_label_hour, minutes_font)
        # pen.write((first_label_hour_x, offset_y), first_label_hour, minutes_font)

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

    def _fetch_rain_intensity_by_datetime(self):
        return {
            datetime(1900, 1, 1, 18, 25): 3,
            datetime(1900, 1, 1, 18, 30): 0,
            datetime(1900, 1, 1, 18, 35): 0,
            datetime(1900, 1, 1, 18, 40): 2,
            datetime(1900, 1, 1, 18, 45): 1,
            datetime(1900, 1, 1, 18, 50): 3,
            datetime(1900, 1, 1, 18, 55): 0,
            datetime(1900, 1, 1, 19, 5): 0,
            datetime(1900, 1, 1, 19, 15): 1,
        }