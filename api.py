import requests
import json

url = 'https://v6.exchangerate-api.com/v6/5cf07c0e1450306c4e495730/latest/USD'
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    with open('exchange_data.json', 'w') as json_file:
        json.dump(data, json_file)




