import asyncio
import logging
import time

from eth_account.messages import encode_defunct, encode_typed_data
from web3 import AsyncWeb3

# Настройка логгера
logging.basicConfig(filename='myapp.log', level=logging.INFO)
logger = logging.getLogger(__name__)

PRIVATE_KEY = '93dce5fbe9057709f6c41fe494ee37baad2a8dcdaf78cb9711961c48cbc36cd1'

class Client:
    def __init__(self, private_key):
        if not private_key:
            raise ValueError("Приватный ключ не может быть пустым.")
        self.private_key = private_key
        self.w3 = AsyncWeb3()
        self.address = self.w3.to_checksum_address(self.w3.eth.account.from_key(self.private_key).address)
        if not self.private_key:
            raise ValueError("Приватный ключ не указан. Проверьте настройки клиента.")

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
    try:
        recovered_address = client.w3.eth.account.recover_message(message, signature=signature)
        logger.info(f"Восстановленный адрес: {recovered_address}")

        if recovered_address.lower() == client.address.lower():
            logger.info("Подпись успешно проверена!")
        else:
            logger.error("Ошибка: восстановленный адрес не совпадает с ожидаемым.")
    except Exception as e:
        logger.error(f"Ошибка при проверке подписи: {e}")


async def main():
    client = Client(PRIVATE_KEY)

    permit_data = await prepare_permit_data()
    try:
        signable_message = client.custom_message(data_to_sign=permit_data, eip_712_data=True)
    except Exception as e:
        print(f"Ошибка при создании подписываемого сообщения: {e}")
        return

    signed_message = client.w3.eth.account.sign_message(signable_message=signable_message, private_key=client.private_key)
    logger.info("Сообщение успешно подписано!")
    signature = client.w3.to_hex(signed_message.signature)
    logger.info(f"Signature: {signature}")

    await verification_signature(client, signable_message, signature)

asyncio.run(main())
