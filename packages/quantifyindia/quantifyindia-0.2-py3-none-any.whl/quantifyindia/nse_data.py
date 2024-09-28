from nsetools import Nse
import datetime

def get_realtime_data(symbol):
    nse = Nse()
    try:
        stock_data = nse.get_quote(symbol)
        return stock_data
    except Exception as e:
        return f"Error fetching data: {str(e)}"

def get_historical_data(symbol, start_date, end_date):
    nse = Nse()
    try:
        # Assuming you want to fetch historical data using some API provided by Nse
        # Replace the following with the actual implementation to get historical data.
        historical_data = nse.get_historical_data(symbol, start_date, end_date)  # Example
        return historical_data
    except Exception as e:
        return f"Error fetching historical data: {str(e)}"
