from eth_typing import ChecksumAddress, HexAddress, HexStr
from web3 import AsyncWeb3, AsyncHTTPProvider
import asyncio

from web3.types import Wei

private_key = ''
proxy = ''  # log:pass@ip:port

request_kwargs = {
        'proxy': f'http://{proxy}'
    } if proxy else {}

rpc_url = 'https://arbitrum.llamarpc.com'

w3_client = AsyncWeb3(AsyncHTTPProvider(rpc_url, request_kwargs=request_kwargs))


# async def check_connect():
#     return await w3_client.is_connected()
#
#
# print(asyncio.run(check_connect()))

#

address = w3_client.to_checksum_address(w3_client.eth.account.from_key(private_key).address)


async def check_gas():
    return await w3_client.eth.gas_price


async def get_nonce():
    return await w3_client.eth.get_transaction_count(address)


async def get_native_balance():
    return await w3_client.eth.get_balance(address)


async def main():
    decimals = 18

    print(f"Количество транзакций на кошельке: {await get_nonce()} txs")
    print(f"Баланс кошелька: {(await get_native_balance()) / 10 ** decimals:.6f} ETH")



# asyncio.run(main())


dex_address = '0xaaaaaaaacb71bf2c8cae522ea5fa455571a74106'
dex_checksum_address = w3_client.to_checksum_address(dex_address)

transaction = {
    'from': address,
    'to': dex_checksum_address,
    'data': '0x',
    'nonce': 0,
    'gasPrice': 1,
    'gas': 1
}

raw_tx = w3_client.eth.account.sign_transaction(transaction, private_key).rawTransaction
print(raw_tx.hex())
