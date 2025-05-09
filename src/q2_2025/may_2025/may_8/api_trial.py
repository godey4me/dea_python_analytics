from requests import get

url = "https://yahoo-finance166.p.rapidapi.com/api/stock/get-statistics"

querystring = {"symbol":"AAPL","region":"US"}

headers = {"x-rapidapi-host": "yahoo-finance166.p.rapidapi.com"}

response = get(url, headers=headers, params=querystring)

print(response.json())