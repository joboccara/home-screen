from selenium.webdriver.common.by import By

def scrape_zmanim(calj_driver):
    try:
        tef_time = _find_time_from_label(calj_driver, "début tefilin")
        tzet_time = _find_time_from_label(calj_driver, "tzeit hacokhavim")

        sh_start_label_span = calj_driver.find_element(By.XPATH, "//*[text() = 'allumage avant :']")
        sh_start_time = sh_start_label_span.find_element(By.XPATH, "../../../*[3]/*[1]/*[1]").text
        sh_end_time = sh_start_label_span.find_element(By.XPATH, "../../../*[3]/*[2]/*[1]").text
        par = sh_start_label_span.find_element(By.XPATH, "../../../../../../../*[3]/*[1]/*[2]").text[::-1]
        
        result = {"tef": tef_time, "tzet": tzet_time, "sh_start": sh_start_time, "sh_end": sh_end_time, "par": par}
    except:
        result = {"error": True}
    finally:
        return result

def _find_time_from_label(driver, label):
    tef_label_a = driver.find_element(By.XPATH, f"//*[text() = '{label}']")
    return tef_label_a.find_element(By.XPATH, "../../*[2]").text
