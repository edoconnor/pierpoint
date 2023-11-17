import requests
import pandas as pd
import csv
import json
import creds  # Make sure this file contains your Marketstack API key

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
        'limit': 1  # Assuming we only want the latest closing price
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['data']:
            # Marketstack API wraps the data in a 'data' key
            latest_data = data['data'][0]  # Get the latest data point
            close = latest_data['close']
            results.append({
                'symbol': symbol,
                'date': latest_data['date'],
                'close': close
            })
        else:
            print(f"No data available for symbol {symbol}")
    else:
        print(f"Error fetching data for symbol {symbol}: {response.status_code} - {response.text}")

df = pd.DataFrame(results)

# Convert the date to the desired format
df['date'] = pd.to_datetime(df['date']).dt.strftime('%m/%d')

# Save to CSV
df.to_csv('dow.csv', index=False)

# Function to convert CSV to JSON
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
