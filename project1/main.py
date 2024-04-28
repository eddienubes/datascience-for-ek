import asyncio

from yahoo_api_client import YahooApiClient


async def main() -> None:
    api = YahooApiClient()

    await api.get_history('^GSPC')


asyncio.run(main())
