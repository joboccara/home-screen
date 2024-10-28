from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://meteofrance.com/previsions-meteo-france/neuilly-sur-seine/92200"
UL_RAIN_DATA_CLASS_NAME = 'rain-data'
NUMBER_OF_RAIN_DATA_POINTS = 9
DIV_CLASS_NAME_CONTAINING_TIME = 'time'
START_TIME_FORMAT =  "%H : %M"
RAIN_LABELS_INTENSITY = {"Pas de pluie": 0, "Pluie faible": 1, "Pluie modérée": 2, "Pluie forte": 3}

def scrape_rain_hour():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    result = {}

    try:
        driver.get(URL)
        rain_labels = scrape_rain_labels_when_displayed(driver)
        start_time_label = scrape_start_time_label(driver)
        result = parse_scraped_data(rain_labels, start_time_label)
    except Exception:
        result = {"error": True}
    finally:
        driver.quit()
        return result

def scrape_rain_labels_when_displayed(driver):
    wait = WebDriverWait(driver, 10)
    ul_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, UL_RAIN_DATA_CLASS_NAME)))
    wait.until(lambda d: len(d.find_elements(By.XPATH, f'//ul[@class="{UL_RAIN_DATA_CLASS_NAME}"]/li')) == NUMBER_OF_RAIN_DATA_POINTS)

    labels = []
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")
    for li in li_elements:
        img = li.find_element(By.TAG_NAME, "img")
        if img and img.get_attribute("alt"):
            labels.append(img.get_attribute("alt"))
    return labels

def scrape_start_time_label(driver):
    div_time = driver.find_element(By.CLASS_NAME, DIV_CLASS_NAME_CONTAINING_TIME)
    return div_time.find_element(By.TAG_NAME, "p").text

def parse_scraped_data(rain_labels, start_time_label):
    return { "start_time": datetime.strptime(start_time_label, START_TIME_FORMAT),
            "rain_intensities": parse_rain_labels(rain_labels) }

def parse_rain_labels(rain_labels):
    return [RAIN_LABELS_INTENSITY.get(rain_label) for rain_label in rain_labels]

print(scrape_rain_hour())