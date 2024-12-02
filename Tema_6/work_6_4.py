import asyncio

from aiohttp import InvalidURL
from web3 import AsyncWeb3, AsyncHTTPProvider

rpc_url = "https://eth-pokt.nodies.app"
# example_proxy_url = 'http://username:password@proxyserver:port'
# example_address = "0xfd5dab27ccdf35742ecd20cf78ae12862cef9e4f"
# example_real_proxy_url = 'http://Mw1ST4:KudKd83jK3@46.8.110.10:3000'

async def build_w3_client_by_input_proxy():
    proxy = None
    while (proxy is None):
        proxy = input("Введите URL прокси-сервера:")
        while len(proxy) == 0:
            proxy = input("Пустое значение, введите URL прокси-сервера:")
        request_kwargs = {
            'proxy': proxy
        }
        return AsyncWeb3(AsyncHTTPProvider(rpc_url, request_kwargs=request_kwargs))

async def print_check_connect(w3_client):
    try:
        result_connect = await w3_client.is_connected()
        if result_connect:
            print("Соединение через прокси установлено!")
            return w3_client
        else:
            print("Не удалось установить соединение через прокси!")
            await build_w3_client_by_input_proxy()
    except InvalidURL:
        print("Некорректно указа Url прокси, повторите попытку")
        w3_client_new = await build_w3_client_by_input_proxy()
        return await print_check_connect(w3_client_new)

async def get_address_by_input(w3_client):
    checksum_address_input = None
    while checksum_address_input is None:
        try:
            address_input = input("Введите ваш адрес кошелька: ")
            return w3_client.to_checksum_address(address_input)
        except ValueError:
            print("Некорректно указан адрес кошелька, повторите попытку")

async def print_balance(w3_client, checksum_address):
    balance = await w3_client.eth.get_balance(checksum_address)
    print(f"Баланс адреса {checksum_address}: {w3_client.from_wei(balance, 'ether'):.2f} ETH")

async def main():
    w3 = await build_w3_client_by_input_proxy()
    w3 = await print_check_connect(w3)
    address = await get_address_by_input(w3)
    await print_balance(w3, address)

asyncio.run(main())