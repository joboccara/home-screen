import os

class RainHourWidget:
    def draw(self, pen):
        current_path = os.path.dirname(os.path.abspath(__file__))
        light_rain_path = os.path.join(current_path, "images/light-rain.png")
        pen.draw_picture((0, 0), light_rain_path, 25, 25)