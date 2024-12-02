import asyncio
import json
from web3.contract import AsyncContract
from client import Client

with open('erc20_abi.json') as file:
    ERC20_ABI = json.load(file)


USDT_ADDRESS = "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9"

private_key = ''
proxy = ''
recipient = "0x3F83d04eb63bf550499d654b08a677e11aDd954D"
amount_to_transfer = 0.5


async def transfer_usdt():
    client = Client(private_key, proxy)

    usdt_contract: AsyncContract = client.w3.eth.contract(
        address=client.w3.to_checksum_address(USDT_ADDRESS),
        abi=ERC20_ABI
    )

    decimals = await usdt_contract.functions.decimals().call()

    amount_to_transfer_in_wei = client.to_wei_custom(amount_to_transfer, decimals)

    tx_params = await client.prepare_tx()

    transaction = await usdt_contract.functions.transfer(
        client.w3.to_checksum_address(recipient),
        amount_to_transfer
    ).build_transaction(tx_params)

    tx_data = usdt_contract.encode_abi(
        fn_name='transfer',
        args=(
            client.w3.to_checksum_address(recipient),
            amount_to_transfer_in_wei
        )
    )

    transaction = tx_params | {
        'to': usdt_contract.address,
        'data': tx_data
    }

    tx_hash = await client.sign_and_send_tx(transaction, without_gas=True)
    await client.wait_tx(tx_hash)

asyncio.run(transfer_usdt())




