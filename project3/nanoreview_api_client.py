import aiohttp
import asyncio
from scrapy.selector import Selector
from quantulum3 import parser
from common import catchable
from nanoreview_api_client_exception import NanoReviewApiClientException
from nanoreview_info import NanoReviewInfo


@catchable(NanoReviewApiClientException)
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
        except Exception as e:
            raise e

    async def get_redirect_url(self, laptop: str):
        form_data = aiohttp.FormData()
        form_data.add_field(name='page1', value=laptop)
        form_data.add_field(name='page2', value=laptop)
        form_data.add_field(name='lang', value='en')

        res = await self.session.post('/api/search/url', data=form_data, verify_ssl=self.verify_ssl)
        return (await res.json())['url']

    async def get_info(self, laptop: str) -> NanoReviewInfo:
        """
        Gets nanoreview characteristics information.
        All values are out of 100.
        """
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

        weight_raw = selector.xpath(
            "//table[@class='specs-table']//tr[td[contains(@class, 'cell-h') and normalize-space("
            ")='Weight']]/td[@class='cell-s']/text()").get()

        screen_to_body_ratio_raw = selector.xpath("//table[@class='specs-table']//tr[td[contains(@class, 'cell-h') and "
                                                  "normalize-space()='Screen-to-body ratio']]/td["
                                                  "@class='cell-s']/text()").get()

        refresh_rate_raw = selector.xpath(
            "//table[@class='specs-table']//tr[td[@class='cell-h' and normalize-space()='Refresh rate']]/td["
            "@class='cell-s']/text()").get()

        ppi_raw = selector.xpath(
            "//table[@class='specs-table']//tr[td[@class='cell-h' and normalize-space()='PPI']]/td["
            "@class='cell-s']/text()").get()

        max_brightness_raw = selector.xpath(
            "//div[contains(@class, 'score-bar-name') and contains(text(), "
            "'Max. brightness')]/following-sibling::div[contains(@class, 'score-bar-result')]/span["
            "@class='score-bar-result-number']/text()").get()

        weight = parser.parse(weight_raw).pop(0).value
        screen_to_body_ratio = parser.parse(screen_to_body_ratio_raw).pop(0).value
        refresh_rate = parser.parse(refresh_rate_raw).pop(0).value
        ppi = parser.parse(ppi_raw).pop(0).value
        max_brightness = parser.parse(max_brightness_raw).pop(0).value

        name = selector.xpath("//div[contains(@class, 'card-head')]//h1[@class='title-h1']/text()").get()

        return NanoReviewInfo(
            name=name,
            performance=int(performance),
            gaming=int(gaming),
            display=int(display),
            battery=int(battery_life),
            connectivity=int(connectivity),
            portability=int(portability),
            nano_score=int(nano_score),
            weight=float(weight),
            screen_to_body_ratio=int(screen_to_body_ratio),
            refresh_rate=int(refresh_rate),
            ppi=int(ppi),
            max_brightness=int(max_brightness)
        )

    async def search(self, term: str):
        """
        Searches laptops by name.
        :return: the most relevant result
        """
        params = {
            'q': term,
            'limit': 500,
            'type': 'laptop'
        }

        res = await self.session.get('/api/search', params=params, verify_ssl=self.verify_ssl)
        return (await res.json())[0]['name']
