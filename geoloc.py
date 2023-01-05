import time
import requests
import json
from functools import cache

@cache
def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

def get_loc():
    ip_address = get_ip()

    request_url = 'http://ip-api.com/json/' + ip_address

    response = requests.get(request_url)
    result = response.content.decode()
    result = json.loads(result)
    return result['city']
def date_time():
    x=time.strftime("%m/%d/%Y,%H:%M:%S")
    x2 = x.split(",")
    return x2

