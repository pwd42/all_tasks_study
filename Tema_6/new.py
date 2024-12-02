from eth_typing import ChecksumAddress, HexAddress, HexStr
from web3 import AsyncHTTPProvider, AsyncWeb3
import asyncio


rpc = "https://eth.drpc.org"
w3 = AsyncWeb3(AsyncHTTPProvider(rpc))

async def check_connect():
    return await w3.is_connected()

async def check_gas():
    return await w3.eth.gas_price

async def check_gas_max_priority_fee():
    return await w3.eth.max_priority_fee

async def main():

    cc = await check_connect()
    gas = await check_gas()
    max_priority_fee = await check_gas_max_priority_fee()

    print(f"Connected - {cc}")
    print(f"Gas - {gas / 10 ** 9} GWEI")
    print(f"Max Priority Fee - {max_priority_fee / 10 ** 9} GWEI")

asyncio.run(main())