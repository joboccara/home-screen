from datetime import datetime
import dateutil.parser
import json
from PIL import ImageFont
from font_utils import FONT_LOCATION, text_height, text_width
import os
import requests

class BusesTimesWidget:
    SPACING = 20
    LINE_DIRECTION_SPACING = 3
    LINE_TIMES_SPACING = 10
    TIMES_SPACING = 10
    LINE_FONT = ImageFont.truetype(FONT_LOCATION, 15)
    DIRECTION_FONT = ImageFont.truetype(FONT_LOCATION, 10)
    TIMES_FONT = LINE_FONT
    BUSES = [
        { "line": "82", "direction": "Luxembourg", "bus_stop_reference": 23507 },
        { "line": "163", "direction": "Porte de Clichy", "bus_stop_reference": 23762 },
        { "line": "164", "direction": "Porte de Champerret", "bus_stop_reference": 23762 }
    ]

    def __init__(self):
        self._buses_times = list(map(lambda bus_stop: self._get_bus_times(bus_stop["line"],
                                                                          bus_stop["direction"],
                                                                          bus_stop["bus_stop_reference"]), self.BUSES))

    def _get_bus_times(self, line_number, direction, bus_stop_reference):
        url = f"https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef=STIF:StopPoint:Q:{bus_stop_reference}:"
        response = json.loads(requests.get(url, headers={"apiKey": os.getenv("PRIM_API_KEY")}).text)
        bus_stop_passages = response["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][0]["MonitoredStopVisit"]
        if bus_stop_passages == []:
            first_time_label, second_time_label = "SERVICE", "FINISHED"
        else:
            line_passages = list(filter(lambda passage: passage["MonitoredVehicleJourney"]["MonitoredCall"]["DestinationDisplay"][0]["value"] == direction, bus_stop_passages))
            times = list(map(lambda passage: passage["MonitoredVehicleJourney"]["MonitoredCall"]["ExpectedDepartureTime"], line_passages))
            first_time_label = self._time_s_to_minutes_label(times[0])
            if "CallNote" in line_passages[0]["MonitoredVehicleJourney"]["MonitoredCall"].keys() and \
              line_passages[0]["MonitoredVehicleJourney"]["MonitoredCall"]["CallNote"][0]["value"] == "Dernier BUS":
                second_time_label = "Last bus"
            else:
                second_time_label = self._time_s_to_minutes_label(times[1])
        return {
            "line_number": line_number,
            "direction": direction,
            "times": [first_time_label, second_time_label]
            }

    def _time_s_to_minutes_label(self, time):
        return f"{round((dateutil.parser.isoparse(time) - datetime.now().astimezone()).total_seconds() / 60)} min"

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
        line_y = self.height() / 2 - line_direction_height / 2
        pen.write((offset_x, line_y), bus_times["line_number"], self.LINE_FONT)
        
        direction_y = line_y + line_height + self.LINE_DIRECTION_SPACING
        pen.write((offset_x, direction_y), bus_times["direction"], self.DIRECTION_FONT)

        current_x = offset_x + text_width(bus_times["line_number"], self.LINE_FONT) + self.LINE_TIMES_SPACING
        pen.write((current_x, 0), bus_times["times"][0], self.TIMES_FONT)
        second_time_y = text_height(bus_times["times"][1], self.TIMES_FONT) + self.TIMES_SPACING
        pen.write((current_x, second_time_y), bus_times["times"][1], self.TIMES_FONT)

    def _bus_times_width(self, bus_times):
        return text_width(bus_times["line_number"], self.LINE_FONT) \
            + self.LINE_TIMES_SPACING \
            + max(list(map(lambda time: text_width(time, self.TIMES_FONT), bus_times["times"])))

    def _bus_times_height(self, bus_times):
        return text_height(bus_times["times"][0], self.TIMES_FONT) \
              + self.TIMES_SPACING \
              + text_height(bus_times["times"][1], self.TIMES_FONT)