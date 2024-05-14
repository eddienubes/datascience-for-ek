import asyncio
import pandas as pd
from termcolor import colored

from nanoreview_api_client import NanoReviewApiClient
from evaluator import Evaluator


async def main() -> None:
    api = NanoReviewApiClient()

    laptops = [
        'Apple MacBook Pro 16 (2023)',
        'Acer Predator Triton 17 X',
        'Lenovo ThinkPad E16',
        'Lenovo Yoga Slim 7 Gen 8 (14″ AMD)',
        'Microsoft Surface Laptop 6 13.5',
        'Microsoft Surface Pro 10',
        'Dell Latitude 5540',
        'Asus TUF Gaming F15'
    ]

    evaluator = Evaluator()

    search_hits = await asyncio.gather(*[api.search(laptop) for laptop in laptops])
    infos = await asyncio.gather(*[api.get_info(hit) for hit in search_hits])
    [evaluator.add(info) for info in infos]

    result = evaluator.run()

    print(f'The {colored('best', 'green')} laptop is {colored(result['best'], attrs=['bold'])}')
    print(f'The {colored('worst', 'magenta')} laptop is {colored(result['worst'], attrs=['bold'])}')
    print(
        f'{result['best']} is {colored('better', 'green')} than {result['worst']} by {colored(f"{round(result['percentage'], 2) * 100}%", 'white', attrs=['bold'])}')

    dataframe = pd.DataFrame(result['scores'])
    print(dataframe[::-1])


asyncio.run(main())
