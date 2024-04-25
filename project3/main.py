import asyncio

from nanoreview_api_client import NanoReviewApiClient


async def main() -> None:
    api = NanoReviewApiClient()
    searchHit = await api.search('apple')

    res = await api.get_info(searchHit[0]['name'])


asyncio.run(main())
