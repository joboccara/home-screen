import cairosvg
from io import BytesIO
from PIL import Image, ImageOps
import requests
from selenium.webdriver.common.by import By

def scrape_next_days_weather(driver):
    next_days_lis = driver.find_elements(By.CLASS_NAME, "day")
    return list(map(lambda day_li:
                    {
                        "day_name": day_li.find_element(By.TAG_NAME, "h4").text,
                        "periods_weather": list(map(period_weather_from_li, periods_lis_from_day_li(day_li)))
                    },
                    next_days_lis))

def periods_lis_from_day_li(day_li):
    periods_ul = day_li.find_element(By.TAG_NAME, "ul")
    return periods_ul.find_elements(By.TAG_NAME, "li")

def period_weather_from_li(period_li):
    period = period_li.find_element(By.CLASS_NAME, "period").find_element(By.TAG_NAME, "p").text
    temperature = period_li.find_element(By.CLASS_NAME, "weather_temp").find_element(By.TAG_NAME, "p").text
    image_url = period_li.find_element(By.TAG_NAME, "img").get_attribute("src")
    image_svg = requests.get(image_url).content
    image_png = cairosvg.svg2png(bytestring=image_svg)
    image = ImageOps.invert(Image.open(BytesIO(image_png)).convert("RGB"))
    return {"period": period, "image": image, "temperature": temperature}