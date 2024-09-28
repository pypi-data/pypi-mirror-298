# quantifyindia/nse_data.py

from nsetools import Nse

def get_realtime_data(symbol):
    nse = Nse()
    try:
        stock_data = nse.get_quote(symbol)
        return stock_data
    except Exception as e:
        return f"Error fetching data: {str(e)}"
