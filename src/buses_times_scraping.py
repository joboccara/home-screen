from selenium.webdriver.common.by import By
from webdrivers import build_buses_times_page_driver

LINES = [
    {"number": "82", "direction": "Luxembourg"},
    {"number": "163", "direction": "Porte de Clichy"},
    {"number": "163", "direction": "Porte de Champerret"}
]

def scrape_buses_times():
    driver = build_buses_times_page_driver()
    no_cookies_button = driver.find_element(By.ID, "popin_tc_privacy_button_3")
    no_cookies_button.click()
    return list(map(lambda line_number: _scrape_bus_times(driver, line_number), LINES))

def _scrape_bus_times(driver, line):
    line_img_all_directions = driver.find_elements(By.XPATH, f"//img[@alt='Ligne {line["number"]}']")
    line_img = next(img for img in line_img_all_directions if img.find_element(By.XPATH, "../../../*[2]/*[1]").text == line["direction"])
    times_div = line_img.find_element(By.XPATH, "../../../*[2]/*[2]")
    first_time = times_div.find_element(By.XPATH, "./*[2]/*[1]/*[1]").text
    second_time = times_div.find_element(By.XPATH, "./*[3]/*[1]/*[1]").text
    return {
        "line_number": line["number"],
        "times": [first_time, second_time]
        }
