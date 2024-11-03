from PIL import ImageFont
from font_utils import FONT_LOCATION, text_height, text_width

class BusesTimesWidget:
    SPACING = 25
    LINE_DIRECTION_SPACING = 3
    LINE_TIMES_SPACING = 7
    TIMES_SPACING = 10
    LINE_FONT = ImageFont.truetype(FONT_LOCATION, 15)
    DIRECTION_FONT = ImageFont.truetype(FONT_LOCATION, 10)
    TIMES_FONT = LINE_FONT
    def __init__(self, buses_times):
        self._buses_times = buses_times

    def draw(self, pen):
        current_x = 0
        for bus_times in self._buses_times:
            self._draw_bus_times(pen, current_x, bus_times)
            current_x += self._bus_times_width(bus_times) + self.SPACING

    def width(self):
        return sum(list(map(lambda bus_times: self._bus_times_width(bus_times) + self.SPACING, self._buses_times))) - self.SPACING

    def height(self):
        return max(list(map(self._bus_times_height, self._buses_times)))

    def _draw_bus_times(self, pen, offset_x, bus_times):
        line_height = text_height(bus_times["line_number"], self.LINE_FONT)
        line_direction_height = line_height \
                                + self.LINE_DIRECTION_SPACING \
                                + text_height(bus_times["direction"], self.DIRECTION_FONT)
        line_x = offset_x + text_width(bus_times["direction"], self.DIRECTION_FONT) - text_width(bus_times["line_number"], self.LINE_FONT)
        line_y = self.height() / 2 - line_direction_height / 2
        pen.write((line_x, line_y), bus_times["line_number"], self.LINE_FONT)
        
        direction_y = line_y + line_height + self.LINE_DIRECTION_SPACING
        pen.write((offset_x, direction_y), bus_times["direction"], self.DIRECTION_FONT)

        current_x = offset_x + text_width(bus_times["direction"], self.DIRECTION_FONT) + self.LINE_TIMES_SPACING
        pen.write((current_x, 0), bus_times["times"][0], self.TIMES_FONT)
        second_time_y = text_height(bus_times["times"][1], self.TIMES_FONT) + self.TIMES_SPACING
        pen.write((current_x, second_time_y), bus_times["times"][1], self.TIMES_FONT)

    def _bus_times_width(self, bus_times):
        return text_width(bus_times["direction"], self.DIRECTION_FONT) \
            + self.LINE_TIMES_SPACING \
            + max(list(map(lambda time: text_width(time, self.TIMES_FONT), bus_times["times"])))

    def _bus_times_height(self, bus_times):
        return text_height(bus_times["times"][0], self.TIMES_FONT) \
              + self.TIMES_SPACING \
              + text_height(bus_times["times"][1], self.TIMES_FONT)