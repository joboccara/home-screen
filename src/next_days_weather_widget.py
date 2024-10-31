from PIL import ImageFont
from font_utils import FONT_LOCATION, text_height, text_width
from next_days_weather_scraping import scrape_next_days_weather

class NextDaysWeatherWidget:
    def __init__(self, api_access, weather_page_driver):
        self.next_days_weather = api_access.get_next_days_weather(weather_page_driver)

    ICON_SIZE = 40
    ICON_SPACING = 10
    DAY_SPACING = 10

    def draw(self, pen):
        current_y = 0
        current_x = 0
        periods_font = ImageFont.truetype(FONT_LOCATION, 12)
        temperature_font = ImageFont.truetype(FONT_LOCATION, 15)
        period_height = text_height(self.next_days_weather[0]["periods_weather"][0]["period"], periods_font)
        for day_weather in self.next_days_weather:
            pen.write((current_x, current_y), day_weather["day_name"], periods_font, center_x=self.ICON_SIZE)
            period_y = current_y + text_height(day_weather["day_name"], periods_font) + self.ICON_SPACING
            for period_weather in day_weather["periods_weather"]:
                pen.write((current_x, period_y), period_weather["period"], periods_font, center_x=self.ICON_SIZE)
                image_y = period_y + period_height + self.ICON_SPACING
                pen.draw_picture((current_x, image_y), period_weather["image"].resize((self.ICON_SIZE, self.ICON_SIZE)))
                temperature_y = image_y + self.ICON_SIZE + self.ICON_SPACING
                pen.write((current_x, temperature_y), period_weather["temperature"], temperature_font, center_x=self.ICON_SIZE)
                current_x += self.ICON_SIZE + self.ICON_SPACING
            current_x += self.DAY_SPACING

    def width(self):
        return sum(list(map(lambda day_weather: len(day_weather["periods_weather"]) * (self.ICON_SIZE + self.ICON_SPACING),
                            self.next_days_weather))) - self.ICON_SPACING + len(self.next_days_weather) * self.DAY_SPACING - self.DAY_SPACING