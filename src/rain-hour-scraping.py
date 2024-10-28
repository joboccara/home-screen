from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://meteofrance.com/previsions-meteo-france/neuilly-sur-seine/92200"
ul_rain_data_class_name = 'rain-data'
number_of_rain_data_points = 9
div_class_name_containing_time = 'time'
start_time_format =  "%H : %M"

def scrape_rain_hour():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    result = { "rain_labels": [] }

    try:
        driver.get(url)
        result["rain_labels"] = scrape_rain_labels_when_displayed(driver)

        div_time = driver.find_element(By.CLASS_NAME, div_class_name_containing_time)
        start_time_s = div_time.find_element(By.TAG_NAME, "p").text
        result["start_time"] = datetime.strptime(start_time_s, start_time_format)
    finally:
        driver.quit()
        return result

def scrape_rain_labels_when_displayed(driver):
    wait = WebDriverWait(driver, 10)
    ul_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, ul_rain_data_class_name)))
    wait.until(lambda d: len(d.find_elements(By.XPATH, f'//ul[@class="{ul_rain_data_class_name}"]/li')) == number_of_rain_data_points)

    labels = []
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")
    for li in li_elements:
        img = li.find_element(By.TAG_NAME, "img")
        if img and img.get_attribute("alt"):
            labels.append(img.get_attribute("alt"))
    return labels


print(scrape_rain_hour())