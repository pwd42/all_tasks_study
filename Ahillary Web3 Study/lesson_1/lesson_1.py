import json

from web3 import AsyncHTTPProvider, AsyncWeb3
import asyncio

rpc_url = "https://eth.drpc.org"
w3 = AsyncWeb3(AsyncHTTPProvider(rpc_url))

eth_nft_address = AsyncWeb3.to_checksum_address('0x183368d767b299681fdf660233e39f9f8cf8be3a')

def read_json_file(name_file):
    with open(name_file, "r", encoding="utf-8") as file:
        return json.load(file)

# async def check_connect():
#     return await w3.is_connected()
#
# async def check_gas():
#     return await w3.eth.gas_price

async def main():
    abi_nft = read_json_file("abi_nft_eth.json")
    contract = w3.eth.contract(eth_nft_address, abi=abi_nft)

    # cc = await check_connect()
    # gas = await check_gas()

    print('name: ', await contract.functions.name().call())
    print('count nft by top holder: ', await contract.functions.balanceOf("0x50b33581b3f48c91D3eF98C78f021f2dEB8349d6").call())
    print('symbol: ', await contract.functions.symbol().call())
    print('owner: ', await contract.functions.owner().call())


if __name__ == '__main__':
    asyncio.run(main())