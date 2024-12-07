import asyncio
import time

from eth_account.datastructures import SignedMessage
from eth_account.messages import encode_defunct, encode_typed_data, SignableMessage
from web3 import AsyncWeb3



DBR_MESSAGE = """I am not the person or entities who reside in, are citizens of, are incorporated in, or have a registered office in the United States of America or any Prohibited Localities, as defined in the Terms of Use.
I will not in the future access this site or use DLN dApp while located within the United States any Prohibited Localities, as defined in the Terms of Use.
I am not using, and will not in the future use, a VPN to mask my physical location from a restricted territory.
I am lawfully permitted to access this site and use DLN dApp under the laws of the jurisdiction on which I reside and am located.
I understand the risks associated with entering into using DLN Network protocols."""


class Client:
    def __init__(self):
        self.private_key = ''
        self.chain_id = 534352  # Scroll chainId

        self.w3 = AsyncWeb3()
        self.address = self.w3.to_checksum_address(self.w3.eth.account.from_key(self.private_key).address)

    def custom_sign_message(self, data_to_sign, eip_712_data: bool = False):

        if eip_712_data:
            text_encoded: SignableMessage = encode_typed_data(full_message=data_to_sign)
        else:
            text_encoded: SignableMessage = encode_defunct(text=data_to_sign)

        return self.w3.eth.account.sign_message(text_encoded, private_key=self.private_key)


async def sign_permit_data():
    client = Client()

    deadline = int(time.time() + 360)

    permit_data = {
        "types": {
            "Permit": [
                {
                    "name": "owner",
                    "type": "address"
                },
                {
                    "name": "spender",
                    "type": "address"
                },
                {
                    "name": "value",
                    "type": "uint256"
                },
                {
                    "name": "nonce",
                    "type": "uint256"
                },
                {
                    "name": "deadline",
                    "type": "uint256"
                }
            ],
            "EIP712Domain": [
                {
                    "name": "name",
                    "type": "string"
                },
                {
                    "name": "version",
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
            "name": "USD Coin",
            "version": "2",
            "chainId": 534352,
            "verifyingContract": "0x06efdbff2a14a7c8e15944d1f4a48f9f95f663a4"
        },
        "primaryType": "Permit",
        "message": {
            "owner": client.address,
            "spender": "0xfd541d0e2773a189450a70f06bc7edd3c1dc9115",
            "value": 2 ** 256 - 1,
            "nonce": 0,
            "deadline": deadline
        }
    }

    signed_message: SignedMessage = client.custom_sign_message(data_to_sign=permit_data, eip_712_data=True)

    print(client.w3.to_hex(signed_message.v))
    print(client.w3.to_hex(signed_message.r))
    print(client.w3.to_hex(signed_message.s))


async def sign_simple_message():
    client = Client()

    signed_message: SignedMessage = client.custom_sign_message(data_to_sign=DBR_MESSAGE)

    print(client.w3.to_hex(signed_message.signature))


asyncio.run(sign_permit_data())
# asyncio.run(sign_simple_message())
