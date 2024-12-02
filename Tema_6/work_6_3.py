import asyncio

from web3 import AsyncWeb3, AsyncHTTPProvider

rpc_url = "https://eth-pokt.nodies.app"
w3 = AsyncWeb3(AsyncHTTPProvider(rpc_url))

addresses = ["0x742d35Cc6634C0532925a3b844Bc454E4438f44e",
             "0xfe9e8709d3215310075d67e3ed32a380ccf451c8",
             "0xdc76cd25977e0a5ae17155770273ad58648900d3",
             "0x4838b106fce9647bdf1e7877bf73ce8b0bad5f97",
             "0xx"]

async def get_native_balance(address_def):
    try:
        checksum_address = w3.to_checksum_address(address_def)
        return await w3.eth.get_balance(checksum_address)
    except ValueError:
        return None

async def print_balance_with_convert(address, balance):
    if balance is None:
        print(f"Адрес: {address}, Баланс: None")
        return
    print(f"Адрес: {address}, Баланс: {w3.from_wei(balance, 'ether'):.3f} ETH")

async def main():
    tasks = []

    for address in addresses:
        tasks.append(asyncio.create_task(print_balance_with_convert(address, await get_native_balance(address))))

asyncio.run(main())