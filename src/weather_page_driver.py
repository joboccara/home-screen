import platform
from selenium import webdriver

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
    except:
        driver.quit()

    return driver
