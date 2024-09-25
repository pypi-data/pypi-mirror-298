# my_package/main.py

import requests

def fetch_data(url):
    response = requests.get(url)
    return response.json()
