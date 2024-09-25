from datetime import datetime, timezone
import math

from eth_account import Account, messages
from eth_account.account import LocalAccount
from eth_typing import HexStr
import httpx

from emp_orderly_types import OrderlyRegistration
from .message_types import MESSAGE_TYPES


OFF_CHAIN_DOMAIN = {
    "name": "Orderly",
    "version": "1",
    "chainId": 42161,
    "verifyingContract": "0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC",
}


class OrderlyAuth:
    BASE_URL = "https://api-evm.orderly.org"
    BROKER_ID = "logx"

    def __init__(self, broker_id: str | None = None):
        self.broker_id = broker_id or self.BROKER_ID

    def approve(self, private_key: HexStr, orderly_key: str):
        account: LocalAccount = Account.from_key(private_key)
        add_key_message, signed_message = self.sign_message(orderly_key, private_key)
        return self.create_account(add_key_message, signed_message, account)

    def sign_message(self, orderly_key: str, private_key: HexStr):
        chain_id = 42161
        d = datetime.now(timezone.utc)
        epoch = datetime(1970, 1, 1)
        timestamp = math.trunc((d - epoch).total_seconds() * 1_000)

        account: LocalAccount = Account.from_key(private_key)
        add_key_message = {
            "brokerId": self.broker_id,
            "chainId": chain_id,
            "orderlyKey": orderly_key,
            "scope": "read,trading",
            "timestamp": timestamp,
            "expiration": timestamp + 1_000 * 60 * 60 * 24 * 365,  # 1 year
        }
        encoded_data = messages.encode_typed_data(
            domain_data=OFF_CHAIN_DOMAIN,
            message_types={"AddOrderlyKey": MESSAGE_TYPES["AddOrderlyKey"]},
            message_data=add_key_message,
        )
        signed_message = account.sign_message(encoded_data)
        return add_key_message, signed_message

    async def create_account(
        self, add_key_message, signed_message, account: LocalAccount
    ):
        async with httpx.AsyncClient() as client:
            res = await client.post(
                f"{self.BASE_URL}/v1/orderly_key",
                headers={"Content-Type": "application/json"},
                json={
                    "message": add_key_message,
                    "signature": signed_message.signature.hex(),
                    "userAddress": account.address,
                },
            )

        return OrderlyRegistration(**res.json()["data"])
