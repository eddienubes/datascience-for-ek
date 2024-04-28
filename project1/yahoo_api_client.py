from yahooquery import Ticker


class YahooApiClient:

    def __init__(self):
        self.__ticker = Ticker('^gspc', asynchronous=True)

    async def get_history(self, asset: str | list, period='max'):
        ticker = self.__get_ticker(asset)

        history = await ticker.history(period=period)
        print(history)

    def __get_ticker(self, asset: str | list[str]) -> Ticker:
        return Ticker(asset, asynchronous=True)
