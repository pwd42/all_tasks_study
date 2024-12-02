import aiohttp
from aiohttp.web_exceptions import HTTPError


class BaseRequest:
    def __init__(self):
        self.url = "https://www.okx.com/api/v5/public/"
        self.params = {}

    async def make_session_and_request(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, params=self.params) as response:
                    return await response.json()
        except HTTPError as http_err:
            print(f"Ошибка HTTP {self.url}: {http_err}")
        except Exception as err:
            print(f"Общая ошибка {self.url}: {err}")

