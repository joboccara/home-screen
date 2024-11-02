from PIL import ImageFont
from font_utils import FONT_LOCATION, text_height, text_width

class WeatherWidget:
    def __init__(self, api_access, next_days_weather):
        self.next_days_weather = next_days_weather

    ICON_SIZE = 40
    ICON_SPACING = 10
    DAY_SPACING = 10
    PERIODS_FONT = ImageFont.truetype(FONT_LOCATION, 12)
    TEMPERATURE_FONT = ImageFont.truetype(FONT_LOCATION, 15)

    def draw(self, pen):
        current_y = 0
        current_x = 0
        for day_weather in self.next_days_weather:
            pen.write((current_x, current_y), day_weather["day_name"], self.PERIODS_FONT, center_x=self.ICON_SIZE)
            period_y = current_y + text_height(day_weather["day_name"], self.PERIODS_FONT) + self.ICON_SPACING
            for period_weather in day_weather["periods_weather"]:
                pen.write((current_x, period_y), period_weather["period"], self.PERIODS_FONT, center_x=self.ICON_SIZE)
                image_y = period_y + self._period_height() + self.ICON_SPACING
                pen.draw_picture((current_x, image_y), period_weather["image"].resize((self.ICON_SIZE, self.ICON_SIZE)))
                temperature_y = image_y + self.ICON_SIZE + self.ICON_SPACING
                pen.write((current_x, temperature_y), period_weather["temperature"], self.TEMPERATURE_FONT, center_x=self.ICON_SIZE)
                current_x += self.ICON_SIZE + self.ICON_SPACING
            current_x += self.DAY_SPACING

    def width(self):
        return sum(list(map(lambda day_weather: len(day_weather["periods_weather"]) * (self.ICON_SIZE + self.ICON_SPACING),
                            self.next_days_weather))) - self.ICON_SPACING + len(self.next_days_weather) * self.DAY_SPACING - self.DAY_SPACING

    def height(self):
        return self._day_name_height() + self.ICON_SPACING + \
               self._period_height() + self.ICON_SPACING + \
               self.ICON_SIZE + self.ICON_SPACING + self._temperature_height()

    def _day_name_height(self):
        return text_height(self.next_days_weather[0]["day_name"], self.PERIODS_FONT);

    def _period_height(self):
        return text_height(self.next_days_weather[0]["periods_weather"][0]["period"], self.PERIODS_FONT)

    def _temperature_height(self):
        return text_height(self.next_days_weather[0]["periods_weather"][0]["temperature"], self.PERIODS_FONT)