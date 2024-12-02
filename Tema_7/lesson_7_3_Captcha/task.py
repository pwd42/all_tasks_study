import asyncio
import random

from aiohttp import ClientSession, TCPConnector
from aiohttp_socks import ProxyConnector


class CaptchaSolver:
    def __init__(self, proxy):
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

    async def create_task_for_captcha(self):
        url = 'https://api.2captcha.com/createTask'

        payload = {
            "clientKey": TWO_CAPTCHA_API_KEY,
            "task": {
                "type": "TurnstileTask" if USE_PROXY else 'TurnstileTaskProxyless',
                "websiteURL": "https://bartio.faucet.berachain.com/",
                "websiteKey": "0x4AAAAAAARdAuciFArKhVwt",
                "userAgent": self.session.headers['User-Agent'],
            }
        }

        if USE_PROXY:
            proxy_tuple = self.proxy.split('@')

            proxy_login, proxy_password = proxy_tuple[0].split(':')
            proxy_address, proxy_port = proxy_tuple[1].split(':')

            payload['task'].update({
                "proxyType": "http",
                "proxyAddress": proxy_address,
                "proxyPort": proxy_port,
                "proxyLogin": proxy_login,
                "proxyPassword": proxy_password
            })

        response = await self.make_request(method="POST", url=url, json=payload)

        if not response['errorId']:
            return response['taskId']
        raise RuntimeError('Bad request to 2Captcha(Create Task)')

    async def get_captcha_key(self, task_id):
        url = 'https://api.2captcha.com/getTaskResult'

        payload = {
            "clientKey": TWO_CAPTCHA_API_KEY,
            "taskId": task_id
        }

        total_time = 0
        timeout = 360
        while True:
            response = await self.make_request(method="POST", url=url, json=payload)

            if response['status'] == 'ready':
                return response['solution']['token']

            total_time += 5
            await asyncio.sleep(5)

            if total_time > timeout:
                raise RuntimeError('Can`t get captcha solve in 360 second')


async def main():
    proxy = ''

    solver = CaptchaSolver(proxy)

    try:
        task_id = await solver.create_task_for_captcha()

        print(f"Task ID: {task_id}")

        captcha_key = await solver.get_captcha_key(task_id)

        print(f"Captcha Key: {captcha_key}")

    except Exception as error:
        print(f'Error while processing captcha! {error}')

    await solver.session.close()

USE_PROXY = True
TWO_CAPTCHA_API_KEY = ''
asyncio.run(main())
