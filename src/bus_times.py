from datetime import datetime
import dateutil.parser
import json
import os
import requests

BUSES = [
    { "line": "82", "direction_ref": "Luxembourg • Victor Hugo - Poincaré", "bus_stop_reference": 23507 },
    { "line": "163", "direction_ref": "Charlebourg • Porte de Clichy", "bus_stop_reference": 23762 },
    { "line": "164", "direction_ref": "Porte de Champerret", "bus_stop_reference": 23762 }
]

def get_buses_times():
    return list(map(lambda bus_stop: _get_buses_times(bus_stop["line"],
                                                    bus_stop["direction_ref"],
                                                    bus_stop["bus_stop_reference"]), BUSES))

def _get_buses_times(line_number, direction_ref, bus_stop_reference):
    url = f"https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef=STIF:StopPoint:Q:{bus_stop_reference}:"
    response = json.loads(requests.get(url, headers={"apiKey": os.getenv("PRIM_API_KEY")}).text)
    bus_stop_passages = response["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][0]["MonitoredStopVisit"]
    if bus_stop_passages == []:
        first_time_label, second_time_label = "SERVICE", "FINISHED"
    else:
        line_passages = list(filter(lambda passage: passage["MonitoredVehicleJourney"]["DirectionName"][0]["value"] == direction_ref, bus_stop_passages))
        times = list(map(lambda passage: passage["MonitoredVehicleJourney"]["MonitoredCall"]["ExpectedDepartureTime"], line_passages))
        directions = list(map(lambda passage: passage["MonitoredVehicleJourney"]["MonitoredCall"]["DestinationDisplay"][0]["value"], line_passages))
        first_time_label = _time_s_to_minutes_label(times[0])
        if len(line_passages) == 1:
            second_time_label = "Last bus"
        else:
            second_time_label = _time_s_to_minutes_label(times[1])
    return {
        "line_number": line_number,
        "direction": directions[0],
        "times": [first_time_label, second_time_label]
        }

def _time_s_to_minutes_label(time):
    return f"{round((dateutil.parser.isoparse(time) - datetime.now().astimezone()).total_seconds() / 60)} min"