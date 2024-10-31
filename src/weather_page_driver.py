import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://meteofrance.com/previsions-meteo-france/neuilly-sur-seine/92200"

def build_weather_page_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if platform.system() == 'Darwin':
        driver = webdriver.Chrome(options=options)
    else:
        driver = webdriver.Chrome(options=options, service=webdriver.ChromeService('/usr/lib/chromium-browser/chromedriver'))

    try:
        driver.get(URL)
        # wait_for_page_load(driver)
    except:
        driver.quit()

    return driver

UL_RAIN_DATA_CLASS_NAME = "rain-data"
NUMBER_OF_RAIN_DATA_POINTS = 9

def wait_for_page_load(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, UL_RAIN_DATA_CLASS_NAME)))
    wait.until(lambda d: len(d.find_elements(By.XPATH, f'//ul[@class="{UL_RAIN_DATA_CLASS_NAME}"]/li')) == NUMBER_OF_RAIN_DATA_POINTS)
