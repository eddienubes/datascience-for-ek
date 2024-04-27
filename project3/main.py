import asyncio

from nanoreview_api_client import NanoReviewApiClient
from project3.evaluator import Evaluator


async def main() -> None:
    api = NanoReviewApiClient()
    searchHit = await api.search('Acer Aspire 3')

    info = await api.get_info(searchHit[0]['name'])

    evaluator = Evaluator()

    evaluator.add(info)


asyncio.run(main())
