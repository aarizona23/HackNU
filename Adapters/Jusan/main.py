from xml.etree.ElementTree import tostring
import api
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import nltk
from nltk.tokenize import sent_tokenize

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
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[itemprop="text"]'))
            )

            text_divs = driver.find_elements(By.CSS_SELECTOR, 'div[itemprop="text"]')

            for div in text_divs:
                tmp = div.text
                cleaned_string = tmp.strip() 
                ret.append(cleaned_string) 

        finally:
            driver.quit()

    return ret

def get_cashback_map():
    refs = parse_refs("https://jusan.kz/faq/bank/cashback-bonus/bon-prog", "faq-questions_faq_accordion_item__G9bcV", "https://jusan.kz/faq/bank/cashback-bonus/bon-prog/")

    text = get_text(refs)

    sentences = []

    for i in text:
        a = sent_tokenize(i, language='russian')
        sentences = sentences + a

    filtered_sentences = [
        sentence for sentence in sentences
        if any(word.lower() in sentence.lower() for word in special_words)
    ]

    joined_string = ' '.join(filtered_sentences)

    print(api.make_map(joined_string))