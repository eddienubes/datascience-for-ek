import asyncio

from nanoreview_api_client import NanoReviewApiClient
from evaluator import Evaluator


async def main() -> None:
    api = NanoReviewApiClient()
    search_hit1 = await api.search('Apple MacBook Pro 16 (2023)')
    search_hit2 = await api.search('Acer Predator Triton 17 X')
    search_hit3 = await api.search('Lenovo ThinkPad E16')

    info1 = await api.get_info(search_hit1)
    info2 = await api.get_info(search_hit2)
    info3 = await api.get_info(search_hit3)

    evaluator = Evaluator()

    evaluator.add(info1)
    evaluator.add(info2)
    evaluator.add(info3)

    result = evaluator.run()

    print(f'The best laptop is {result['best']}')
    print(f'The worst laptop is {result['worst']}')
    print(f'{result['best']} is better than {result['worst']} by {round(result['percentage'], 2) * 100}%')


asyncio.run(main())
