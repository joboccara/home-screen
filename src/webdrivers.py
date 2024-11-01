import platform
from selenium import webdriver

WEATHER_URL = "https://meteofrance.com/previsions-meteo-france/neuilly-sur-seine/92200"

def build_weather_page_driver():
    return build_driver(WEATHER_URL)

def build_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if platform.system() == 'Darwin':
        driver = webdriver.Chrome(options=options)
    else:
        driver = webdriver.Chrome(options=options, service=webdriver.ChromeService('/usr/lib/chromium-browser/chromedriver'))

    try:
        driver.get(url)
    except:
        driver.quit()

    return driver
