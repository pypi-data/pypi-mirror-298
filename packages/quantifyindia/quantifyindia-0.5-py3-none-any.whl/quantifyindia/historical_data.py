import requests
import datetime

ALPHA_VANTAGE_API_KEY = '3EHFBSOM4UTGNPAU'  # Replace with your actual API key

def get_historical_data(symbol, start_date, end_date):
    try:
        # Format dates to YYYY-MM-DD
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}&outputsize=full'
        response = requests.get(url)
        data = response.json()

        # Extract the time series data
        time_series = data.get('Time Series (Daily)', {})

        # Filter the data within the specified date range
        historical_data = {date: values for date, values in time_series.items() 
                           if start_date_str <= date <= end_date_str}

        return historical_data
    except Exception as e:
        return f"Error fetching historical data: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Test real-time data fetching
    stock_symbol = 'RELIANCE'
    realtime_data = get_realtime_data(stock_symbol)
    print("Real-time Data for", stock_symbol, ":", realtime_data)

    # Test historical data fetching
    start_date = datetime.datetime.now() - datetime.timedelta(days=30)
    end_date = datetime.datetime.now()
    historical_data = get_historical_data(stock_symbol, start_date, end_date)
    print("Historical Data for", stock_symbol, ":", historical_data)
