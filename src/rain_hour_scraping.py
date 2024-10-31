from datetime import datetime, timedelta
from selenium.webdriver.common.by import By

UL_RAIN_DATA_CLASS_NAME = 'rain-data'
NUMBER_OF_RAIN_DATA_POINTS = 9
DIV_CLASS_NAME_CONTAINING_TIME = 'time'
START_TIME_FORMAT =  "%H : %M"
RAIN_LABELS_INTENSITY = {"Pas de pluie": 0, "Pluie faible": 1, "Pluie modérée": 2, "Pluie forte": 3}
INTERVALS_IN_MINUTES = [0, 5, 10, 15, 20, 25, 30, 40, 50]

def scrape_rain_hour(driver):
    result = {}

    try:
        rain_labels = scrape_rain_labels(driver)
        start_time_label = scrape_start_time_label(driver)
        result = parse_scraped_data(start_time_label, rain_labels)
    except Exception:
        result = {"error": True}
    finally:
        return result

def scrape_rain_labels(driver):
    labels = []
    ul_element = driver.find_element(By.CLASS_NAME, UL_RAIN_DATA_CLASS_NAME)
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")
    for li in li_elements:
        img = li.find_element(By.TAG_NAME, "img")
        if img and img.get_attribute("alt"):
            labels.append(img.get_attribute("alt"))
    return labels

def scrape_start_time_label(driver):
    div_time = driver.find_element(By.CLASS_NAME, DIV_CLASS_NAME_CONTAINING_TIME)
    return div_time.find_element(By.TAG_NAME, "p").text

def parse_scraped_data(start_time_label, rain_labels):
    result = {}
    rain_intensities = parse_rain_labels(rain_labels)
    start_time = datetime.strptime(start_time_label, START_TIME_FORMAT)
    for index, interval_in_minutes in enumerate(INTERVALS_IN_MINUTES):
        time = start_time + timedelta(minutes=interval_in_minutes)
        result[time] = rain_intensities[index]
    return result

def parse_rain_labels(rain_labels):
    if (any(label not in RAIN_LABELS_INTENSITY for label in rain_labels)):
        raise Exception("Unknown rain label")
    return [RAIN_LABELS_INTENSITY.get(rain_label) for rain_label in rain_labels]