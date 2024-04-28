from yahooquery import Ticker


class YahooApiClient:

    def __init__(self):
        self.__ticker = Ticker('^gspc', asynchronous=True)

    async def get_history(self, asset: str):
        self.__ticker.history(period='max')
    
    
    async def __get_ticker(self, term: str | list[str]) -> Ticker:
        return Ticker(term, asynchronous=True)
        
