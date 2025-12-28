import requests

headers = {
    'Content-Type': 'application/json',
    'X-API-KEY' : "sk_5pgKqEW-Wz9gnNPoBiNei46ogG9FS_7lS8pGw4cfWLQ"
}

url = 'http://localhost:8070/items'

# Response
response = requests.get(url=url, headers=headers)

print(response.json())