import requests
from nsetools import Nse
import datetime

ALPHA_VANTAGE_API_KEY = '3EHFBSOM4UTGNPAU'  # Replace with your actual API key

def get_realtime_data(symbol):
    nse = Nse()
    try:
        stock_data = nse.get_quote(symbol)
        return stock_data
    except Exception as e:
        return f"Error fetching data: {str(e)}"

def get_historical_data(symbol, start_date, end_date):
    # Format the dates to YYYY-MM-DD for the API request
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # Make a request to Alpha Vantage
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={ALPHA_VANTAGE_API_KEY}'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Check if the API returned a valid response
        if 'Time Series (Daily)' not in data:
            return f"Error fetching historical data: {data.get('Error Message', 'Unknown error')}"

        # Filter the data for the specified date range
        historical_data = {}
        for date, metrics in data['Time Series (Daily)'].items():
            if start_date_str <= date <= end_date_str:
                historical_data[date] = metrics

        return historical_data

    except Exception as e:
        return f"Error fetching historical data: {str(e)}"

# Example usage
if __name__ == "__main__":
    symbol = 'RELIANCE'
    print(get_realtime_data(symbol))

    # Fetch historical data for the last 30 days
    start_date = datetime.datetime.now() - datetime.timedelta(days=30)
    end_date = datetime.datetime.now()
    historical_data = get_historical_data(symbol, start_date, end_date)
    print(historical_data)
