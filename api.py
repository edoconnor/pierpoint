import requests
import pandas as pd
import csv
import json
import creds 

endpoint = 'https://api.marketstack.com/v1/eod'

symbols = [
    'MMM', 'AXP', 'AMGN', 'AAPL', 'BA', 'CAT', 'CVX', 'CSCO', 'KO',
    'DIS', 'DOW', 'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM',
    'MCD', 'MRK', 'MSFT', 'NKE', 'PG', 'CRM', 'TRV', 'UNH', 'VZ',
    'V', 'WBA', 'WMT'
]

results = []

# Loop through all symbols
for symbol in symbols:
    params = {
        'access_key': creds.api_key,
        'symbols': symbol,
        'sort': 'DESC',
        'limit': 5  # Get the last 5 days of EOD data
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['data']:
            # Marketstack API wraps the data in a 'data' key
            for daily_data in data['data']:
                close = daily_data['close']
                results.append({
                    'symbol': symbol,
                    'date': daily_data['date'],
                    'close': close
                })
        else:
            print(f"No data available for symbol {symbol}")
    else:
        print(f"Error fetching data for symbol {symbol}: {response.status_code} - {response.text}")

# Convert the results to a DataFrame
df = pd.DataFrame(results)

# Convert the date to the desired format
df['date'] = pd.to_datetime(df['date']).dt.strftime('%m/%d')

# Save to CSV
df.to_csv('dow.csv', index=False)

# Convert CSV to JSON
def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []

    # Open the CSV and read data into a list of dictionaries
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for row in csvReader:
            jsonArray.append(row)

    # Write the JSON data to a file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)

csvFilePath = r'dow.csv'
jsonFilePath = r'dow.json'
csv_to_json(csvFilePath, jsonFilePath)
