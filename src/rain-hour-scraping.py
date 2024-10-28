from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://meteofrance.com/previsions-meteo-france/neuilly-sur-seine/92200"
ul_rain_data_class_name = 'rain-data'
number_of_rain_data_points = 9

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

try:
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    ul_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, ul_rain_data_class_name)))
    wait.until(lambda d: len(d.find_elements(By.XPATH, f'//ul[@class="{ul_rain_data_class_name}"]/li')) == number_of_rain_data_points)

    li_elements = ul_element.find_elements(By.TAG_NAME, "li")
    for li in li_elements:
        img = li.find_element(By.TAG_NAME, "img")
        if img and img.get_attribute("alt"):
            print(img.get_attribute("alt"))
finally:
    driver.quit()
