from __future__ import annotations

import asyncio
from web3_study import AsyncWeb3, AsyncHTTPProvider
from web3_study.exceptions import TransactionNotFound


class Client:
    def __init__(self, private_key, proxy):
        self.private_key = private_key

        request_kwargs = {'proxy': f'http://{proxy}'}
        rpc_url = 'https://arbitrum.llamarpc.com'

        self.eip_1559 = True
        self.explorer_url = 'https://arbiscan.io/'
        self.w3 = AsyncWeb3(AsyncHTTPProvider(rpc_url, request_kwargs=request_kwargs))
        self.address = self.w3.to_checksum_address(self.w3.eth.account.from_key(self.private_key).address)

    def to_wei_custom(self, number: int | float, decimals: int):

        unit_name = {
            6: 'mwei',
            9: 'gwei',
            18: 'ether',
        }.get(decimals)

        if not unit_name:
            raise RuntimeError(f'Can not find unit name with decimals: {decimals}')

        return self.w3.to_wei(number, unit_name)

    async def get_priotiry_fee(self) -> int:
        fee_history = await self.w3.eth.fee_history(5, 'latest', [80.0])
        non_empty_block_priority_fees = [fee[0] for fee in fee_history["reward"] if fee[0] != 0]

        divisor_priority = max(len(non_empty_block_priority_fees), 1)
        priority_fee = int(round(sum(non_empty_block_priority_fees) / divisor_priority))

        return priority_fee

    async def prepare_tx(self, value: int | float = 0):
        transaction = {
            'chainId': await self.w3.eth.chain_id,
            'nonce': await self.w3.eth.get_transaction_count(self.address),
            'from': self.address,
            'value': self.w3.to_wei(value, 'ether'),
            'gasPrice': int((await self.w3.eth.gas_price) * 1.25)
        }

        if self.eip_1559:
            del transaction['gasPrice']

            base_fee = await self.w3.eth.gas_price
            max_priority_fee_per_gas = await self.w3.eth.max_priority_fee

            if max_priority_fee_per_gas == 0:
                max_priority_fee_per_gas = base_fee

            max_fee_per_gas = int(base_fee * 1.25 + max_priority_fee_per_gas)

            transaction['maxPriorityFeePerGas'] = max_priority_fee_per_gas
            transaction['maxFeePerGas'] = max_fee_per_gas
            transaction['type'] = '0x2'

        return transaction

    async def sign_and_send_tx(self, transaction, without_gas=False):
        if not without_gas:
            transaction['gas'] = int((await self.w3.eth.estimate_gas(transaction)) * 1.5)

        signed_raw_tx = self.w3.eth.account.sign_transaction(transaction, self.private_key).rawTransaction

        print('Successfully signed transaction!')

        tx_hash_bytes = await self.w3.eth.send_raw_transaction(signed_raw_tx)

        print('Successfully sent transaction!')

        tx_hash_hex = self.w3.to_hex(tx_hash_bytes)

        return tx_hash_hex

    async def wait_tx(self, tx_hash):
        total_time = 0
        timeout = 120
        poll_latency = 10
        while True:
            try:
                receipts = await self.w3.eth.get_transaction_receipt(tx_hash)
                status = receipts.get("status")
                if status == 1:
                    print(f'Transaction was successful: {self.explorer_url}tx/{tx_hash}')
                    return True
                elif status is None:
                    await asyncio.sleep(poll_latency)
                else:
                    print(f'Transaction failed: {self.explorer_url}tx/{tx_hash}')
                    return False
            except TransactionNotFound:
                if total_time > timeout:
                    print(f"Transaction is not in the chain after {timeout} seconds")
                    return False
                total_time += poll_latency
                await asyncio.sleep(poll_latency)
