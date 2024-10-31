from PIL import ImageFont
from font_utils import FONT_LOCATION, text_height, text_width
from next_days_weather_scraping import scrape_next_days_weather

class NextDaysWeatherWidget:
    def __init__(self, api_access, weather_page_driver):
        self.next_days_weather = api_access.get_next_days_weather(weather_page_driver)

    ICON_SIZE = 40
    SPACING = 10

    def draw(self, pen):
        current_y = 0
        current_x = 0
        font = ImageFont.truetype(FONT_LOCATION, 15)
        period_height = text_height(self.next_days_weather[0]["periods_weather"][0]["period"], font)
        for day_weather in self.next_days_weather:
            pen.write((current_x, current_y), day_weather["day_name"], font, center_x=self.ICON_SIZE)
            period_y = current_y + text_height(day_weather["day_name"], font) + self.SPACING
            for period_weather in day_weather["periods_weather"]:
                pen.write((current_x, period_y), period_weather["period"], font, center_x=self.ICON_SIZE)
                image_y = period_y + period_height + self.SPACING
                pen.draw_picture((current_x, image_y), period_weather["image"].resize((self.ICON_SIZE, self.ICON_SIZE)))
                temperature_y = image_y + self.ICON_SIZE + self.SPACING
                pen.write((current_x, temperature_y), period_weather["temperature"], font, center_x=self.ICON_SIZE)
                current_x += self.ICON_SIZE + self.SPACING

    def width(self):
        return sum(list(map(lambda day_weather: len(day_weather["periods_weather"]) * (self.ICON_SIZE + self.SPACING),
                            self.next_days_weather))) - self.SPACING