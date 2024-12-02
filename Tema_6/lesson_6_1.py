import asyncio
from logging import exception

from web3 import AsyncWeb3, AsyncHTTPProvider

rpc_url = "https://linea.drpc.org"
# example_cex_address = '0xd3d7DBe73BbdD5A5C7a49Ca322763c4d400fC240'

w3_client = AsyncWeb3(AsyncHTTPProvider(rpc_url))

# проверка коннекта к ноде
async def check_connect():
    try:
        return await w3_client.is_connected()
    except Exception as e:
        print(f"Ошибка подключения, проверь RPC: {e}")
        return False

# получить кол-во транзакций по кошельку
async def get_nonce(address_def):
    return await w3_client.eth.get_transaction_count(address_def)

# получить баланс кошелька, значение в минимальных единицах измерений
async def get_native_balance(address_def):
    return await w3_client.eth.get_balance(address_def)

async def main():
    address_input = input("Введите ваш адрес кошелька: ")
    checksum_address_input = None

    while (checksum_address_input is None):
        try:
            checksum_address_input = w3_client.to_checksum_address(address_input)
        except ValueError:
            print("Некорректно указан адрес кошелька, повторите попытку \n")
            address_input = input("Введите ваш адрес кошелька: ")

    print(f"\nСоединение установлено: {await check_connect()}")
    nonce = await get_nonce(address_input)
    balance = await get_native_balance(address_input)

    print(f"Nonce: {nonce}")
    # print(f"Баланс: {w3_client.from_wei(balance, 'gwei'):.6f} GWEI")
    print(f"Баланс: {w3_client.from_wei(balance, 'ether'):.3f} ETH")


asyncio.run(main())