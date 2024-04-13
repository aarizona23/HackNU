import json
from xml.etree.ElementTree import tostring
import Cashback.Adapters.Halyk.api1 as api1
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import nltk
from nltk.tokenize import sent_tokenize
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

special_words = ["билеты", "супермаркеты", "кафе", "рестораны", "доставка еды", "доставка", "еды", "одежда", "обувь", "товары для детей", "товары", "детей", "такси", "салоны красоты", "салоны", "красоты",
                 "косметика", "кино", "музыка", "фитнес", "spa", "мебель", "игровые сервисы", "игровые","медицинские услуги", "медицинские", "путешествия", "питомцы", "образование"]

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def parse_refs(url, condition, pattern):
    driver = setup_driver()

    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, condition))
    )

    a_elements = driver.find_elements(By.TAG_NAME, "a")

    hrefs = [a.get_attribute('href') for a in a_elements if a.get_attribute('href') and a.get_attribute('href').startswith(pattern)]

    driver.quit()

    return hrefs
    

def get_text(refs):
    ret = []
    for url in refs:
        driver = setup_driver()

        try:
            driver.get(url)

            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="border-b border-gray-100 pb-6 mb-6 content-inner-editer"]'))
            )

            text_divs = driver.find_elements(By.CSS_SELECTOR, 'div[class="border-b border-gray-100 pb-6 mb-6 content-inner-editer"]')

            for div in text_divs:
                tmp = div.text
                cleaned_string = tmp.strip() 
                ret.append(cleaned_string) 

        finally:
            driver.quit()

    return ret

def get_json():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    else:
        refs = parse_refs("https://halykbank.kz/promo", "lazy", "https://halykbank.kz/promo/")
        
        text = get_text(refs)

        joined_string = ' '.join(text)

        return api1.make_map(joined_string)

def get_cashbacks(map):
    utc_plus_5_time = datetime.now(timezone.utc).astimezone(ZoneInfo('Asia/Ashgabat')).date().__str__()
    cashbacks = []

    for key, value in map.items():
        tmp = {
            'bank_name' : 'Halyk Bank',
            'category' : key.lower(),
            'percentage' : value.lower(),
            'valid_from' : utc_plus_5_time,
            'company' : None,
            'min_purchase_amount': None,
            'valid_to': None, 
            'payment_method': None,
            'days_of_week': None,
            'bank_type': None
        }
        cashbacks.append(tmp)
    
    return cashbacks

def get_data():
    data = get_json()
    json_string = json.dumps(data, indent=4, ensure_ascii=False)

    return json_string

print(get_data())