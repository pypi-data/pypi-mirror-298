from datetime import datetime, timezone
import json
import math

from eth_account import Account, messages
from eth_account.account import LocalAccount, SignedMessage
from eth_typing import HexStr
import httpx


MESSAGE_TYPES = {
    "EIP712Domain": [
        {"name": "name", "type": "string"},
        {"name": "version", "type": "string"},
        {"name": "chainId", "type": "uint256"},
        {"name": "verifyingContract", "type": "address"},
    ],
    "Registration": [
        {"name": "brokerId", "type": "string"},
        {"name": "chainId", "type": "uint256"},
        {"name": "timestamp", "type": "uint64"},
        {"name": "registrationNonce", "type": "uint256"},
    ],
}

def get_domain(chain_id: int = 42161):
    OFF_CHAIN_DOMAIN = {
        "name": "Orderly",
        "version": "1",
        "chainId": 42161,
        "verifyingContract": "0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC",
    }
    return OFF_CHAIN_DOMAIN


def build_register_message(timestamp, registration_nonce, chain_id: int = 42161, broker_id: str = "empyreal"):
    register_message = {
        "brokerId": broker_id,
        "chainId": chain_id,
        "timestamp": timestamp,
        "registrationNonce": registration_nonce,
    }
    return register_message


async def orderly_register(private_key: str | HexStr, chain_id: int = 42161, broker_id: str = "empyreal"):
    """Registers an account and returns an Orderly Account ID"""
    domain = get_domain(chain_id)
    base_url = "https://api-evm.orderly.org"
    account: LocalAccount = Account.from_key(private_key)

    async with httpx.AsyncClient() as client:
        res = await client.get("%s/v1/registration_nonce" % base_url)
    response = json.loads(res.text)
    registration_nonce = response["data"]["registration_nonce"]

    d = datetime.now(timezone.utc)
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    timestamp = math.trunc((d - epoch).total_seconds() * 1_000)

    register_message = build_register_message(timestamp, registration_nonce, chain_id, broker_id)

    encoded_data = messages.encode_typed_data(
        domain_data=domain,
        message_types={"Registration": MESSAGE_TYPES["Registration"]},
        message_data=register_message,
    )
    signed_message: SignedMessage = account.sign_message(encoded_data)
    async with httpx.AsyncClient() as client:
        res = await client.post(
            "%s/v1/register_account" % base_url,
            headers={"Content-Type": "application/json"},
            json={
                "message": register_message,
                "signature": signed_message.signature.hex(),
                "userAddress": account.address,
            },
        )
    response = json.loads(res.text)
    if not response['success']:
        raise ValueError(response['message'])

    orderly_account_id = response["data"]["account_id"]
    return orderly_account_id
