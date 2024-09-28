# quantifyindia/historical_data.py

import requests

ALPHA_VANTAGE_API_KEY = '3EHFBSOM4UTGNPAU'  # Replace with your Alpha Vantage API key

def get_historical_data(symbol, start_date, end_date):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Extract and filter data based on dates
    time_series = data.get('Time Series (Daily)', {})
    historical_data = {
        date: values for date, values in time_series.items()
        if start_date <= date <= end_date
    }
    return historical_data
