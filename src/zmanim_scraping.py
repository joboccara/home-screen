from font_utils import reverse_script
import re
from selenium.webdriver.common.by import By

def scrape_zmanim(calj_driver):
    try:
        tef_time = _find_time_from_label(calj_driver, "début tefilin")
        tzet_time = _find_time_from_label(calj_driver, "tzeit hacokhavim")
        plag_time = _find_time_from_label(calj_driver, 'plag haminḥa (GR"A)')

        sh_start_label_span = calj_driver.find_element(By.XPATH, "//*[text() = 'allumage avant :']")

        # using find_elements and not find_element as it doesn't throw if the element doesn't exist
        sh_start_time = _find_element_or_empty(sh_start_label_span, "../../../*[3]/*[1]/*[1]")
        sh_end_time = _find_element_or_empty(sh_start_label_span, "../../../*[3]/*[2]/*[1]")
        par = reverse_script(_find_element_or_empty(sh_start_label_span, "../../../../../../../*[3]/*[1]/*[2]"))
        omer_label = _find_element_or_empty(sh_start_label_span, 15 * "../" + 4 * "*[1]/" + "*[2]/*[1]/*[1]/*[1]/*[3]/*[1]")
        digits_match = re.match(r'^\d+', omer_label)
        omer_day = digits_match.group(0) if digits_match else ''

        result = {"tef": tef_time,
                  "tzet": tzet_time,
                  "plag": plag_time,
                  "sh_start": sh_start_time,
                  "sh_end": sh_end_time,
                  "par": par,
                  "omer_day": omer_day}
    except:
        result = {"error": True}
    finally:
        return result

def _find_element_or_empty(start_element, path):
    elements_array = start_element.find_elements(By.XPATH, path)
    return elements_array[0].text if len(elements_array) == 1 else ""

def _find_time_from_label(driver, label):
    tef_label_a = driver.find_element(By.XPATH, f"//*[text() = '{label}']")
    return tef_label_a.find_element(By.XPATH, "../../*[2]").text
