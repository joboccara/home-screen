import os

class RainHourWidget:
    def draw(self, pen):
        current_path = os.path.dirname(os.path.abspath(__file__))
        light_rain_path = os.path.join(current_path, "images/light-rain.png")
        pen.draw_picture((0, 0), light_rain_path, 25, 25)
        medium_rain_path = os.path.join(current_path, "images/medium-rain.png")
        pen.draw_picture((0, 0), medium_rain_path, 60, 25)
        heavy_rain_path = os.path.join(current_path, "images/heavy-rain.png")
        pen.draw_picture((0, 0), heavy_rain_path, 100, 25)