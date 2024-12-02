import asyncio

from datetime import datetime
from web3 import AsyncWeb3, AsyncHTTPProvider
from web3.types import BlockData

rpc_url = "https://eth-pokt.nodies.app"
w3 = AsyncWeb3(AsyncHTTPProvider(rpc_url))

async def get_block_data_by_input():
    number_block = None
    while (number_block is None):
        try:
            number_block =  await w3.eth.get_block(input("Введите номер блока: "))
        except ValueError:
            print("Некорректно указан номер блока, повторите попытку \n")
            number_block = await w3.eth.get_block(input("Введите номер блока: "))
    return number_block

def print_info_by_blok_number(block_data):
    block_hash = block_data["hash"].hex()
    block_timestamp = block_data["timestamp"]
    block_count_tx = len(block_data["transactions"])

    print(f"Хэш блока: {block_hash}")
    print(f"Время создания блока: {datetime.fromtimestamp(block_timestamp)}")
    print (f"Количество транзакций в блоке: {block_count_tx}")

async def main():
    block_data: BlockData = await get_block_data_by_input()
    print_info_by_blok_number(block_data)


asyncio.run(main())