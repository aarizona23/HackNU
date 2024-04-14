from .Adapters.Halyk import client as halyk_client
from .Adapters.Jusan import client as jusan_client
from .Adapters.cash import test as cash_test
import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def get_cashbacks(json_data):
    utc_plus_5_time = datetime.now(timezone.utc).astimezone(ZoneInfo('Asia/Almaty')).date().strftime('%Y-%m-%d')
    cashbacks = []
    json_data = json.loads(json_data)

    try:
        # Assuming you have loaded the JSON data into `json_data`
        for data_dict in json_data:  
            tmp = {
                'bank_name': 'Halyk Bank',
                'category': data_dict.get('category', '').lower(),  # Lowercase category if it exists
                'percentage': str(data_dict.get('percentage', '')),  # Ensure percentage is a string
                'valid_from': data_dict.get('date_from', None),
                'company': data_dict.get('company_name', None),  # Get company name if it exists
                'min_purchase_amount': data_dict.get('min_purchase_amount', None),
                'valid_to': data_dict.get('date_to', None), 
                'payment_method': data_dict.get('payment_method', None),
                'days_of_week': data_dict.get('days_of_week', None),
                'bank_type': data_dict.get('bank_type', None)
            }
            cashbacks.append(tmp)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

    return cashbacks

def get_cashbacks1(json_data):
    utc_plus_5_time = datetime.now(timezone.utc).astimezone(ZoneInfo('Asia/Almaty')).date().strftime('%Y-%m-%d')
    cashbacks = []
    json_data = json.loads(json_data)

    try:
        # Assuming you have loaded the JSON data into `json_data`
        for data_dict in json_data:  
            tmp = {
                'bank_name': 'Jusan Bank',
                'category': data_dict.get('category', '').lower(),  # Lowercase category if it exists
                'percentage': str(data_dict.get('percentage', '')),  # Ensure percentage is a string
                'valid_from': data_dict.get('date_from', None),
                'company': data_dict.get('company_name', None),  # Get company name if it exists
                'min_purchase_amount': data_dict.get('min_purchase_amount', None),
                'valid_to': data_dict.get('date_to', None), 
                'payment_method': data_dict.get('payment_method', None),
                'days_of_week': data_dict.get('days_of_week', None),
                'bank_type': data_dict.get('bank_type', None)
            }
            cashbacks.append(tmp)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

    return cashbacks

def get_cashbacks2(json_data):
    utc_plus_5_time = datetime.now(timezone.utc).astimezone(ZoneInfo('Asia/Almaty')).date().strftime('%Y-%m-%d')
    cashbacks = []
    json_data = json.loads(json_data)

    try:
        # Assuming you have loaded the JSON data into `json_data`
        for data_dict in json_data:  
            tmp = {
                'bank_name': data_dict.get('bank_name', None),
                'category': data_dict.get('category', '').lower(),  # Lowercase category if it exists
                'percentage': str(data_dict.get('percentage', '')),  # Ensure percentage is a string
                'valid_from': data_dict.get('valid_from', None),
                'company': data_dict.get('company', None),  # Get company name if it exists
                'min_purchase_amount': data_dict.get('min_purchase_amount', None),
                'valid_to': data_dict.get('valid_to', None), 
                'payment_method': data_dict.get('payment_method', None),
                'days_of_week': data_dict.get('days_of_week', None),
                'bank_type': data_dict.get('bank_type', None)
            }
            cashbacks.append(tmp)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

    return cashbacks

def parse_func():
    json_data = halyk_client.get_data()
    json_data1 = jusan_client.get_data()
    json_data2 = cash_test()
    cashbecks = get_cashbacks(json_data)
    cashbecks1 = get_cashbacks1(json_data1)
    cashbecks2 = get_cashbacks2(json_data2)
    cashbecks.extend(cashbecks1)
    cashbecks.extend(cashbecks2)
    return cashbecks
    