import random

from aiohttp import ClientSession, TCPConnector
from aiohttp_socks import ProxyConnector


class Client:
    def __init__(self, proxy):
        from task import USE_PROXY

        self.proxy = proxy

        self.session = ClientSession(
            connector=ProxyConnector.from_url(f"http://{proxy}") if USE_PROXY else TCPConnector()
        )

        self.session.headers.update({
            'User-Agent': self.get_user_agent()
        })

    @staticmethod
    def get_user_agent():
        random_version = f"{random.uniform(520, 540):.2f}"
        return (f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random_version} (KHTML, like Gecko)'
                f' Chrome/126.0.0.0 Safari/{random_version} Edg/126.0.0.0')

    async def make_request(self, method: str = 'GET', url: str = None, headers: dict = None, json: dict = None):

        async with self.session.request(method=method, url=url, headers=headers, json=json) as response:
            if response.status in [200, 201]:
                return await response.json()
            raise RuntimeError(f"Bad request to Solver API. Response status: {response.status}")
