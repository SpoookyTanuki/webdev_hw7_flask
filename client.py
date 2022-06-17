import requests

URL = 'http://127.0.0.1:5000'

response = requests.post(f'{URL}/user/',
                         json={'user_name': 'user_8'})

print(response.status_code)
print(response.json())
