from font_utils import reverse_script
from selenium.webdriver.common.by import By

def scrape_zmanim(calj_driver):
    try:
        tef_time = _find_time_from_label(calj_driver, "début tefilin")
        tzet_time = _find_time_from_label(calj_driver, "tzeit hacokhavim")

        sh_start_label_span = calj_driver.find_element(By.XPATH, "//*[text() = 'allumage avant :']")

        # using find_elements and not find_element as it doesn't throw if the element doesn't exist
        sh_start_time_array = sh_start_label_span.find_elements(By.XPATH, "../../../*[3]/*[1]/*[1]")
        sh_end_time_array = sh_start_label_span.find_elements(By.XPATH, "../../../*[3]/*[2]/*[1]")
        par_array = sh_start_label_span.find_elements(By.XPATH, "../../../../../../../*[3]/*[1]/*[2]")
        sh_data_found = len(sh_start_time_array) == 1 and len(sh_end_time_array) == 1 and len(par_array) == 1
        sh_start_time = sh_start_time_array[0].text if sh_data_found else ""
        sh_end_time = sh_end_time_array[0].text if sh_data_found else ""
        par = reverse_script(par_array[0].text) if sh_data_found else ""
        
        result = {"tef": tef_time, "tzet": tzet_time, "sh_start": sh_start_time, "sh_end": sh_end_time, "par": par}
    except:
        result = {"error": True}
    finally:
        return result

def _find_time_from_label(driver, label):
    tef_label_a = driver.find_element(By.XPATH, f"//*[text() = '{label}']")
    return tef_label_a.find_element(By.XPATH, "../../*[2]").text
