from PIL import ImageFont
from font_utils import FONT_LOCATION, text_height, text_width
from next_days_weather_scraping import scrape_next_days_weather

class NextDaysWeatherWidget:
    def __init__(self, api_access, weather_page_driver):
        self.next_days_weather = api_access.get_next_days_weather(weather_page_driver)

    SPACING = 10
    ICON_SIZE = 40

    def draw(self, pen):
        current_y = 0
        current_x = 0
        font = ImageFont.truetype(FONT_LOCATION, 15)
        period_height = text_height(self.next_days_weather[0]["periods_weather"][0]["period"], font)
        for day_weather in self.next_days_weather:
            day_name = day_weather["day_name"]
            day_name_x = current_x + self.ICON_SIZE / 2 - text_width(day_name, font) / 2
            pen.write((day_name_x, current_y), day_weather["day_name"], font)
            period_y = current_y + text_height(day_weather["day_name"], font) + self.SPACING
            for period_weather in day_weather["periods_weather"]:
                period_x = current_x + self.ICON_SIZE / 2 - text_width(period_weather["period"], font) / 2
                pen.write((period_x, period_y), period_weather["period"], font)
                image_y = period_y + period_height + self.SPACING
                pen.draw_picture((current_x, image_y), period_weather["image"].resize((self.ICON_SIZE, self.ICON_SIZE)))
                temperature_x = current_x + self.ICON_SIZE / 2 - text_width(period_weather["temperature"], font) / 2
                temperature_y = image_y + self.ICON_SIZE + self.SPACING
                pen.write((temperature_x, temperature_y), period_weather["temperature"], font)
                current_x += self.ICON_SIZE + self.SPACING