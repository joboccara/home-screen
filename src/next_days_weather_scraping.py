import cairosvg
from io import BytesIO
from PIL import Image, ImageOps
import requests
from selenium.webdriver.common.by import By

PERIOD_TRANSLATIONS = {
    "Matin": "Morn.",
    "Après-midi": "Aft.",
    "Soirée": "Evening"
}

WEEK_DAYS_TRANSLATIONS = {
    "LUNDI": "Mon",
    "MARDI": "Tue",
    "MECREDI": "Wed",
    "JEUDI": "Thu",
    "VENDREDI": "Fri",
    "SAMEDI": "Sat",
    "DIMANCHE": "Sun"
}

def scrape_next_days_weather(driver):
    day1_day2_lis = driver.find_elements(By.CLASS_NAME, "day")
    day1_day2 = parse_days_weather(day1_day2_lis)
    tomorrow_link = driver.find_element(By.ID, "msc_tomorrow")
    tomorrow_link.click()
    day2_day3_lis = driver.find_elements(By.CLASS_NAME, "day")
    day3 = parse_days_weather([day2_day3_lis[1]])
    return day1_day2 + day3

def parse_days_weather(days_lis):
    days_weather =  list(map(lambda day_li:
                    {
                        "day_name": translate_day_name(day_li.find_element(By.TAG_NAME, "h4").text),
                        "periods_weather": list(map(_period_weather_from_li, _periods_lis_from_day_li(day_li)))[:-1] # remove night weather
                    },
                    days_lis))
    return list(filter(lambda day_weather: len(day_weather["periods_weather"]) > 0, days_weather))

def _periods_lis_from_day_li(day_li):
    periods_ul = day_li.find_element(By.TAG_NAME, "ul")
    return periods_ul.find_elements(By.TAG_NAME, "li")

def _period_weather_from_li(period_li):
    original_period = period_li.find_element(By.CLASS_NAME, "period").find_element(By.TAG_NAME, "p").text
    temperature = period_li.find_element(By.CLASS_NAME, "weather_temp").find_element(By.TAG_NAME, "p").text
    image_url = period_li.find_element(By.TAG_NAME, "img").get_attribute("src")
    image_svg = requests.get(image_url).content
    image_png = cairosvg.svg2png(bytestring=image_svg)
    image = ImageOps.invert(Image.open(BytesIO(image_png)).convert("RGB"))
    return {"period": _translate_period(original_period), "image": image, "temperature": temperature}

def translate_day_name(day_name):
    week_day, day_in_month = day_name.split(" ")
    if week_day in WEEK_DAYS_TRANSLATIONS.keys():
        translated_week_day = WEEK_DAYS_TRANSLATIONS[week_day]
    else:
        translated_week_day = week_day
    return f"{translated_week_day} {day_in_month}"


def _translate_period(period):
    if period in PERIOD_TRANSLATIONS.keys():
        return PERIOD_TRANSLATIONS[period]
    else:
        return period