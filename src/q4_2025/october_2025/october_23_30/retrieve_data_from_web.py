from requests import get

# URL
url = "https://jsonplaceholder.typicode.com/photos"

# Perform a GET request
response = get(url=url)

# Deserialization
data = response.json()

print(type(data))

# Count objects
print(len(data))

print(data[:10])