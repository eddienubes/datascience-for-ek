import aiohttp
import asyncio
from scrapy.selector import Selector


class NanoReviewApiClient:
    def __init__(self):
        self.base_url = 'https://nanoreview.net'
        self.session = aiohttp.ClientSession(base_url=self.base_url)
        self.verify_ssl = False

    def __del__(self):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.session.close())
            else:
                loop.run_until_complete(self.session.close())
        except Exception:
            pass

    async def get_redirect_url(self, laptop: str):
        form_data = aiohttp.FormData()
        form_data.add_field(name='page1', value=laptop)
        form_data.add_field(name='page2', value=laptop)
        form_data.add_field(name='lang', value='en')

        res = await self.session.post('/api/search/url', data=form_data, verify_ssl=self.verify_ssl)
        return (await res.json())['url']

    async def get_info(self, laptop: str):
        url = await self.get_redirect_url(laptop)

        res = await self.session.get(url, verify_ssl=self.verify_ssl)
        html = await res.text()

        selector = Selector(text=html)
        performance = selector.xpath(
            "//div[contains(@class, 'score-bar-name') and contains(text(), 'Performance')]/following-sibling::div["
            "contains(@class, 'score-bar-result')]/span/text()").get()

        gaming = selector.xpath(
            "//div[contains(@class, 'score-bar-name') and contains(text(), 'Gaming')]/following-sibling::div["
            "contains(@class, 'score-bar-result')]/span/text()").get()

        display = selector.xpath("//div[contains(@class, 'score-bar-name') and contains(text(), "
                                 "'Display')]/following-sibling::div[contains(@class, 'score-bar-result')]/span/text("
                                 ")").get()

        battery_life = selector.xpath(
            "//div[contains(@class, 'score-bar-name') and contains(text(), 'Battery Life')]/following-sibling::div["
            "contains(@class, 'score-bar-result')]/span/text()").get()

        connectivity = selector.xpath("//div[contains(@class, 'score-bar-name') and contains(text(), "
                                      "'Connectivity')]/following-sibling::div[contains(@class, "
                                      "'score-bar-result')]/span/text()").get()

        portability = selector.xpath(
            "//div[contains(@class, 'score-bar-name') and contains(text(), 'Portability')]/following-sibling::div["
            "contains(@class, 'score-bar-result')]/span/text()").get()

        nano_score = selector.xpath(
            "//div[contains(@class, 'score-bar-name') and contains(text(), 'NanoReview "
            "Score')]/following-sibling::div[contains(@class, 'score-bar-result')]/span[contains(@class, "
            "'score-bar-result-square-dark')]/text()").get()

        return {
            'performance': performance,
            'gaming': gaming,
            'display': display,
            'battery_life': battery_life,
            'connectivity': connectivity,
            'portability': portability,
            'nano_score': nano_score
        }

    async def search(self, term: str):
        params = {
            'q': term,
            'limit': 500,
            'type': 'laptop'
        }

        res = await self.session.get('/api/search', params=params, verify_ssl=self.verify_ssl)
        return await res.json()
