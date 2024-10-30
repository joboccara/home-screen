from PIL import Image
import os

class RainHourWidget:
    def draw(self, pen):
        current_path = os.path.dirname(os.path.abspath(__file__))

        light_rain_path = os.path.join(current_path, "images/light-rain.png")
        light_rain = Image.open(light_rain_path).resize((25, 25))
        pen.draw_picture((0, 0), light_rain)

        medium_rain_path = os.path.join(current_path, "images/medium-rain.png")
        medium_rain = Image.open(medium_rain_path).resize((25, 25))
        pen.draw_picture((30, 0), medium_rain)

        heavy_rain_path = os.path.join(current_path, "images/heavy-rain.png")
        heavy_rain = Image.open(heavy_rain_path).resize((25, 25))
        pen.draw_picture((60, 0), heavy_rain)