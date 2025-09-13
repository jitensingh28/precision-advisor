import requests
import json

url = 'http://127.0.0.1:5000/suggest'
data = {'farmer_id': 1}
headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)
print('Status Code:', response.status_code)
print('Response:', response.json())
