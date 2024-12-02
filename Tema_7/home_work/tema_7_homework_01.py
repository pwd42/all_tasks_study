import asyncio

from web3 import AsyncWeb3, AsyncHTTPProvider
from web3.exceptions import TransactionNotFound

rpc_url = "https://scroll.drpc.org"
explorer_url = 'https://scrollscan.com/'
sender_text = "отправителя"
recipient_text = "получателя"

async def connect_to_blockchain(rpc):
    w3 = AsyncWeb3(AsyncHTTPProvider(rpc))
    if await w3.is_connected():
        # print("Соединение установлено!")
        return w3
    else:
        print("Не удалось установить соединение!")

def get_address_by_input(w3_client, whose):
    while True:
        try:
            address_input = input(f"Введите адрес {whose}: ")
            return w3_client.to_checksum_address(address_input)
        except ValueError:
            print("Некорректно указан адрес кошелька, повторите попытку")

def get_private_key_by_input():
    private_key = input(f"Введите приватный ключ отправителя: ")
    return private_key

def get_value_for_tx_by_input():
    while True:
        try:
            value = float(input("Введите количество для отправки (ETH): "))
            return value
        except ValueError:
            print("Некорректно указано количество для отправки (ETH), повторите попытку")

async def print_check_balance(w3_client, address, whose, is_after = False):
    balance = await w3_client.eth.get_balance(address)
    if is_after:
        print(f"Баланс {whose} после: {w3_client.from_wei(balance, 'ether'):.6f} ETH")
    else:
        print (f"Баланс {whose} до: {w3_client.from_wei(balance, 'ether'):.6f} ETH")
    return balance

# добавлен метод после проверки для кейса Проверка достаточности баланса с учетом стоимсоти газа
async def control_balance(w3_client, sender, value):
    """Проверка баланса отправителя перед транзакцией."""
    balance = await w3_client.eth.get_balance(sender)
    gas_price = await w3_client.eth.gas_price
    gas_limit = 21000
    total_cost = w3_client.to_wei(value, 'ether') + gas_price * gas_limit

    if balance >= total_cost:
        return True
    else:
        print("⚠️ Недостаточно средств для транзакции. Проверьте баланс.")
        return False

async def prepare_tx(w3_client, sender_address, recipient_address, value_for_tx):
    transaction = {
        'nonce': await w3_client.eth.get_transaction_count(sender_address),
        'from': sender_address,
        'to': w3_client.to_checksum_address(recipient_address),
        'value': w3_client.to_wei(value_for_tx, 'ether'),
        'gas': 21000,
        'maxPriorityFeePerGas': 0,
        'maxFeePerGas': 0,
        'chainId': await w3_client.eth.chain_id

    }
    # Оценка и установка параметров газа:

    # Получаем базовую цену газа и приоритетную комиссию
    base_fee = await w3_client.eth.gas_price
    max_priority_fee_per_gas = await w3_client.eth.max_priority_fee
    max_fee_per_gas = base_fee + max_priority_fee_per_gas
    # Устанавливаем параметры в транзакции
    transaction['maxPriorityFeePerGas'] = max_priority_fee_per_gas
    transaction['maxFeePerGas'] = int(max_fee_per_gas * 1.5)  # Добавляем запас
    return transaction

# def sign_tx(w3_client, transaction, private_key):
#     signed_raw_tx  = w3_client.eth.account.sign_transaction(transaction, private_key)
#     print('Successfully signed transaction!')
#     return signed_raw_tx.rawTransaction
#
# async def send_tx(w3_client, signed_raw_tx):
#     tx_hash_bytes = await w3_client.eth.send_raw_transaction(signed_raw_tx)
#     print('Successfully sent transaction!')
#     tx_hash_hex = w3_client.to_hex(tx_hash_bytes)
#     return tx_hash_hex

async def sign_and_send_tx(w3_client, transaction, private_key):
    try:
        signed_raw_tx = w3_client.eth.account.sign_transaction(transaction, private_key).rawTransaction
        # print('Successfully signed transaction!')
        tx_hash_bytes = await w3_client.eth.send_raw_transaction(signed_raw_tx)
        # print('Successfully sent transaction!')
        tx_hash_hex = w3_client.to_hex(tx_hash_bytes)
        return tx_hash_hex
    except Exception as error:
        print(f"❌ Ошибка при отправке транзакции: {error}")
        return None

async def wait_tx(w3_client, tx_hash):
    total_time = 0
    timeout = 120
    poll_latency = 10
    while True:
        try:
            receipt = await w3_client.eth.wait_for_transaction_receipt(tx_hash)
            if receipt.status == 1:
                print(f'\nТранзакция отправлена! Хэш транзакции: {tx_hash}\n')
                print(f'Ссылка: {explorer_url}tx/{tx_hash}')
                return
            elif receipt.status is None:
                await asyncio.sleep(poll_latency)
            else:
                print(f'\nTransaction failed: {explorer_url}tx/{tx_hash}\n')
        except TransactionNotFound:
            if total_time > timeout:
                print(f"\nTransaction is not in the chain after {timeout} seconds\n")
            total_time += poll_latency
            await asyncio.sleep(poll_latency)

async def main():
    w3 = await connect_to_blockchain(rpc_url)
    if not w3:
        return

    address_sender = get_address_by_input(w3, sender_text)
    private_key =  get_private_key_by_input()
    address_recipient = get_address_by_input(w3, recipient_text)
    value_for_tx = get_value_for_tx_by_input()

    print("\n")
    await print_check_balance(w3, address_sender, sender_text)
    await print_check_balance(w3, address_recipient, recipient_text)
    print("\n")

    if await control_balance(w3, address_sender, value_for_tx):
        print("\n🚀 Создание и отправка транзакции...")
        transaction_prepared = await prepare_tx(w3, address_sender, address_recipient,value_for_tx)
        tx_hash_hex = await sign_and_send_tx(w3, transaction_prepared, private_key)
        if tx_hash_hex:
            await wait_tx(w3, tx_hash_hex)

            await print_check_balance(w3, address_sender, sender_text, True)
            await print_check_balance(w3, address_recipient, recipient_text, True)
        else:
            print("❌ Транзакция не выполнена из-за недостатка средств.")

if __name__ == "__main__":
    asyncio.run(main())
