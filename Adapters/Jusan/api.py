import json
import os
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
    GOOGLE_API_KEY = os.getenv('API_KEY')

    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel('gemini-pro')

    prompt_text = "Extract categories and percentages from this text and output as JSON. Each category has only one precentage value, so if there are several options use that one which is more recent. Json file must have only category and its percentage, for example Супермаркеты : 5%."

    response = model.generate_content(prompt_text + data_text)

    cleaned_text = response.text.strip('`').lstrip('json').strip()

    data = decode_first_json_object(cleaned_text)

    return data