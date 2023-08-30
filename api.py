import requests
import pandas as pd
import csv
import json
import creds
import time

endpoint = 'https://www.alphavantage.co/query'

symbols = ['MMM', 'AXP', 'AMGN', 'AAPL', 'BA', 'CAT', 'CVX', 'CSCO', 'KO',
           'DIS', 'DOW', 'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM',
           'MCD', 'MRK', 'MSFT', 'NKE', 'PG', 'CRM', 'TRV', 'UNH', 'VZ',
           'V', 'WBA', 'WMT']

results = []

for i in range(0, len(symbols), 5):
    symbols_batch = symbols[i:i+5]
    for symbol in symbols_batch:
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'apikey': creds.api_key
        }

        response = requests.get(endpoint, params=params)

        data = response.json()

        daily_data = data['Time Series (Daily)']

        for date, daily_entry in list(daily_data.items())[:5]:
            close = daily_entry['4. close']
            results.append({'symbol': symbol, 'date': date, 'close': close})
    time.sleep(60)

df = pd.DataFrame(results)

df['date'] = pd.to_datetime(df['date']).dt.strftime('%m/%d')

df.to_csv('dow.csv', index=False)


def csv_to_json(csvFilePath, jsonFilePath):

    jsonArray = []

    with open(csvFilePath, encoding='utf-8') as csvf:

        csvReader = csv.DictReader(csvf)

        for row in csvReader:

            jsonArray.append(row)

    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)


csvFilePath = r'dow.csv'
jsonFilePath = r'dow.json'
csv_to_json(csvFilePath, jsonFilePath)
