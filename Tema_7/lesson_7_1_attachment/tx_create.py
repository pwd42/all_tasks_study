import asyncio
from web3 import AsyncWeb3, AsyncHTTPProvider
from web3.exceptions import TransactionNotFound

wallet_private_key = ''
proxy = ''  # log:pass@ip:port

request_kwargs = {
    'proxy': f'http://{proxy}'
} if proxy else {}

rpc_url = 'https://arbitrum.llamarpc.com'
explorer_url = 'https://arbiscan.io/'

w3_client = AsyncWeb3(AsyncHTTPProvider(rpc_url, request_kwargs=request_kwargs))
wallet_address = w3_client.to_checksum_address(w3_client.eth.account.from_key(wallet_private_key).address)


async def get_priotiry_fee() -> int:
    fee_history = await w3_client.eth.fee_history(5, 'latest', [80.0])
    non_empty_block_priority_fees = [fee[0] for fee in fee_history["reward"] if fee[0] != 0]

    divisor_priority = max(len(non_empty_block_priority_fees), 1)
    priority_fee = int(round(sum(non_empty_block_priority_fees) / divisor_priority))

    return priority_fee


async def sign_and_send_tx(transaction):
    signed_raw_tx = w3_client.eth.account.sign_transaction(transaction, wallet_private_key).rawTransaction

    print('Successfully signed transaction!')

    tx_hash_bytes = await w3_client.eth.send_raw_transaction(signed_raw_tx)

    print('Successfully sent transaction!')

    tx_hash_hex = w3_client.to_hex(tx_hash_bytes)

    return tx_hash_hex


async def wait_tx(tx_hash):
    total_time = 0
    timeout = 120
    poll_latency = 10
    while True:
        try:
            receipts = await w3_client.eth.get_transaction_receipt(tx_hash)
            status = receipts.get("status")
            if status == 1:
                print(f'Transaction was successful: {explorer_url}tx/{tx_hash}')
                return True
            elif status is None:
                await asyncio.sleep(poll_latency)
            else:
                print(f'Transaction failed: {explorer_url}tx/{tx_hash}')
                return False
        except TransactionNotFound:
            if total_time > timeout:
                print(f"Transaction is not in the chain after {timeout} seconds")
                return False
            total_time += poll_latency
            await asyncio.sleep(poll_latency)


async def main():
    value = 0.0001  # ETH

    transaction = {
        'chainId': await w3_client.eth.chain_id,
        'nonce': await w3_client.eth.get_transaction_count(wallet_address),
        'from': wallet_address,
        'to': w3_client.to_checksum_address('0x3F83d04eb63bf550499d654b08a677e11aDd954D'),
        'value': w3_client.to_wei(value, 'ether'),
        'gasPrice': int((await w3_client.eth.gas_price) * 1.25)
    }

    if eip_1559:
        del transaction['gasPrice']

        base_fee = await w3_client.eth.gas_price
        max_priority_fee_per_gas = await w3_client.eth.max_priority_fee

        if max_priority_fee_per_gas == 0:
            max_priority_fee_per_gas = base_fee

        max_fee_per_gas = int(base_fee * 1.25 + max_priority_fee_per_gas)

        transaction['maxPriorityFeePerGas'] = max_priority_fee_per_gas
        transaction['maxFeePerGas'] = max_fee_per_gas
        transaction['type'] = '0x2'

    transaction['gas'] = int((await w3_client.eth.estimate_gas(transaction)) * 1.5)

    tx_hash = await sign_and_send_tx(transaction)
    await wait_tx(tx_hash)

eip_1559 = True
asyncio.run(main())
