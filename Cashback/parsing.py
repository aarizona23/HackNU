from .Adapters.Halyk import client as halyk_client
from .Adapters.Jusan import client as jusan_client
import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
def parse_func():
    return halyk_client.get_data()
def parse_jusan():
    return jusan_client.get_data()
    
    