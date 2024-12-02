from web3 import AsyncWeb3
from eth_account.signers.local import LocalAccount

 class Client:
    private_key: str
    rpc: str
    w3: AsyncWeb3
    account: LocalAccount
 account
    def __init__(self, private_key: str, rpc: str):
        self.private_key = private_key
        self.rpc = rpc
        self.w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
        self.account = self.w3.eth.account.from_key(private_key)