import asyncio
from typing import AsyncGenerator

import aiohttp
from HdRezkaApi import *


class MediaApiClient:
    def __init__(self):
        self.rezka = HdRezkaApi('https://rezka.ag/series/thriller/646-vo-vse-tyazhkie-2008.html')
        self.session = aiohttp.ClientSession()

    def get_stream(self) -> str:
        def progress(current, all):
            percent = round(current * 100 / all)
            print(f"{percent}%: {current}/{all}", end="\r")

        return self.rezka.getStream('1', '1', translation='Оригинал (+субтитры)')('360p')[0]

    async def get_mp4_stream(self, url: str, size: int = 1024) -> AsyncGenerator[bytes, None]:
        response = await self.session.get(url, ssl=False, headers={
            'connection': 'keep-alive',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
        }, allow_redirects=True)

        async for chunk in response.content.iter_chunked(size):
            yield chunk

    def __del__(self):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.session.close())
            else:
                loop.run_until_complete(self.session.close())
        except Exception as e:
            raise e
