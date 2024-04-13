import json
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

def decode_first_json_object(text):
    decoder = json.JSONDecoder()
    try:
        obj, idx = decoder.raw_decode(text)
        return obj
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e)
        return None


def make_map(data_text):
    # Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
    GOOGLE_API_KEY="AIzaSyARX4EzvcMJHXYQWZ75xTufZz2p1sW1y2k"

    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel('gemini-pro')

    prompt_text = """Выведи ответ в JSON формате где лист JSON форматов в каждом котором есть category, percentage, date_from, date_to, company_name. Category должно быть одно из следующих, так что нужно подобрать подходящее исключительно из
    "билеты", "супермаркеты", "кафе и рестораны", "доставка еды", "одежда и обувь", "товары для детей", "такси", "салоны красоты и косметика", "кино и музыка онлайн", "фитнес и spa", "мебель", "игровые сервисы","медицинские услуги", "путешествия", "питомцы", "образование", "автомобильные заправочные станции". 
    Percentage это процент бонусов. date_from и date_to это длительность акции в формате yyyy-mm-dd каждый, важно что между ними тире! не точки!. company_name это компании где акция в виде строки. Игнорируй акции про обмен бонусов. 
    Пример формата "category":"кафе и рестораны", "percentage":"5", "date_from":"09.02.2024", "date_to":"30.04.2024", "company_name":"Alser, Technodom" не давай ненастоящие данные а только с информации ниже. Выведи только то что существует без пустых элементов."""
    
    response = model.generate_content(prompt_text + data_text)

    cleaned_text = response.text.strip('`').lstrip('json').strip()

    data = decode_first_json_object(cleaned_text)

    return data
