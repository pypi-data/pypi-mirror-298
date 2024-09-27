import pandas as pd
import requests
from .trady_models import DealerPositioning, ZeroDteFlow, DailyMarketData,DarkPoolPrints,DashBoardData



class TradySDK:
    def __init__(self, headers):
        """SDK for tradytics. Must have COOKIE to get through."""

        self.headers = headers



    def dealer_positioning(self, ticker:str):
        

        """
        
        """
        try:
            ticker = ticker.upper()

            r = requests.post("https://tradytics.com/get_dealer_positioning_data", data={'ticker': f"{ticker}"}, headers=self.headers).json()

            data = r['data']

            return DealerPositioning(data)
        except Exception as e:
            print(e)
    def zero_dteflow(self, ticker:str='SPY'):
        try:
            """args:
            
            >>> ticker: choose between SPY / IWM / QQQ/ SPX"""
            payload = { 
                'date': 'latest'
            }
            url = f"https://tradytics.com/get_0dte_flow"

            r = requests.post(url, headers=self.headers, data=payload).json()

            data = r['data']

            symbol_data = data['symbol_data']
            ticker_data = symbol_data[f'{ticker}']

            return ZeroDteFlow(ticker_data)
        except Exception as e:
            print(e)

    def get_vol_expectation(self):
        try:
            url = f"https://tradytics.com/get_0dte_vol_expectation"

            r = requests.post(url, headers=self.headers).json()

            df = pd.DataFrame(r, index=[0])

            return df
        except Exception as e:
            print(e)
    
    
    def get_dashboard_data(self, ticker):
        try:
            r = requests.post("https://tradytics.com/get_options_dashboard_data_lite", data={'ticker': f'{ticker}'}, headers=self.headers).json()
            data = r['data']

            return DashBoardData(data)
        except Exception as e:
            print(e)


