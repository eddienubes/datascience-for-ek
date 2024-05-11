from yahooquery import Ticker
import pandas as pd


class YahooApiClient:

    def __init__(self):
        self.__ticker = Ticker('^gspc', asynchronous=True)

    def get_history(self, asset: str | list, period='max') -> pd.DataFrame:
        ticker = self.__get_ticker(asset)

        history = ticker.history(period=period)
        return history

    def __get_ticker(self, asset: str | list[str]) -> Ticker:
        return Ticker(asset, asynchronous=True)
