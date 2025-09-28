import requests
import time
import os  
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

POLYGON_API_Key = os.getenv("POLYGON_API_KEY")

LIMIT = 1000

url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_Key}"

def get_with_retry(url, params=None):
    while True:
        response = requests.get(url, params=params)
        if response.status_code == 429:
            retry_after_seconds = int(response.headers.get('Retry-After', '12'))
            time.sleep(retry_after_seconds)
            continue
        if not response.ok:
            raise RuntimeError(f"Polygon API error {response.status_code}: {response.text}")
        return response

response = get_with_retry(url)
tickers = []


data = response.json()
for ticker in data['results']:
    tickers.append(ticker)
    

while 'next_url' in data:
    next_url = data['next_url']
    response = get_with_retry(next_url, params={"apiKey": POLYGON_API_Key})
    data = response.json()
    for ticker in data.get('results', []):
        tickers.append(ticker)




# Export to CSV
df = pd.DataFrame(tickers)
df.to_csv('all_tickers.csv', index=False)
print(f"Exported {len(tickers)} tickers to all_tickers.csv")