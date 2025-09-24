import requests
import os  
from dotenv import load_dotenv

load_dotenv()

POLYGON_API_Key = os.getenv("POLYGON_API_KEY")

LIMIT = 1000

url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_Key}"

response = requests.get(url)
tickers = []


if not response.ok:
    raise RuntimeError(f"Polygon API error {response.status_code}: {response.text}")

data = response.json()



for ticker in data['results']:
    tickers.append(ticker)
    

while 'next_url' in data:
    next_url = data['next_url']
    response = requests.get(next_url, params ={"apiKey": POLYGON_API_Key})
    data = response.json()
    for ticker in data.get['results',[]]:
        tickers.append(ticker)

print(len(tickers))