import asyncio
import time

from eth_account.messages import encode_defunct, encode_typed_data
from web3 import AsyncWeb3

class Client:
    def __init__(self):
        self.private_key = ''
        self.w3 = AsyncWeb3()
        self.address = self.w3.to_checksum_address(self.w3.eth.account.from_key(self.private_key).address)

    def custom_message(self, data_to_sign, eip_712_data: bool = False):

        if eip_712_data:
            return encode_typed_data(full_message=data_to_sign)
        else:
            return encode_defunct(text=data_to_sign)

async def prepare_permit_data():
    deadline = int(time.time() + 360)

    permit_data = {
        "types": {
            "PermitSingle": [
                {
                    "name": "details",
                    "type": "PermitDetails"
                },
                {
                    "name": "spender",
                    "type": "address"
                },
                {
                    "name": "sigDeadline",
                    "type": "uint256"
                }
            ],
            "PermitDetails": [
                {
                    "name": "token",
                    "type": "address"
                },
                {
                    "name": "amount",
                    "type": "uint160"
                },
                {
                    "name": "expiration",
                    "type": "uint48"
                },
                {
                    "name": "nonce",
                    "type": "uint48"
                }
            ],
            "EIP712Domain": [
                {
                    "name": "name",
                    "type": "string"
                },
                {
                    "name": "chainId",
                    "type": "uint256"
                },
                {
                    "name": "verifyingContract",
                    "type": "address"
                }
            ]
        },
        "domain": {
            "name": "Permit2",
            "chainId": 8453,
            "verifyingContract": "0x000000000022d473030f116ddee9f6b43ac78ba3"
        },
        "primaryType": "PermitSingle",
        "message": {
            "details": {
                "token": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
                "amount": 1461501637330902918203684832716283019655932542975,
                "expiration": deadline,
                "nonce": 0
            },
            "spender": "0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad",
            "sigDeadline": deadline
        }
    }
    return permit_data

async def verification_signature(client, message, signature):
    recovered_address = client.w3.eth.account.recover_message(message, signature=signature)
    print(f"Восстановленный адрес: {recovered_address}")

async def main():
    client = Client()

    permit_data = await prepare_permit_data()
    signable_message = client.custom_message(data_to_sign=permit_data, eip_712_data=True)

    signed_message = client.w3.eth.account.sign_message(signable_message=signable_message, private_key=client.private_key)
    print("Сообщение успешно подписано!")
    signature = client.w3.to_hex(signed_message.signature)
    print(f"Сигнатура: {signature}")

    await verification_signature(client, signable_message, signature)

asyncio.run(main())
