import asyncio

from nanoreview_api_client import NanoReviewApiClient


async def main() -> None:
    api = NanoReviewApiClient()
    searchHit = await api.search('Acer Aspire 3')

    info = await api.get_info(searchHit[0]['name'])

    print(info)


asyncio.run(main())
