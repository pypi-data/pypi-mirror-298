from datetime import datetime, timezone
import json
import math
import httpx

from eth_rpc import PrivateKeyWallet
from eth_rpc.types import hash_eip712_bytes

from emp_orderly.types.domains import make_domain, Registration
from emp_orderly.exceptions import OrderlyAccountCreationException


async def create_account(
    wallet: PrivateKeyWallet,
    base_url: str = "https://testnet-api-evm.orderly.org",
    broker_id: str = "empyreal",
    chain_id: int = 421614,
):
    domain = make_domain(chain_id)
    async with httpx.AsyncClient() as client:
        res = await client.get("%s/v1/registration_nonce" % base_url)
    response = json.loads(res.text)
    registration_nonce = response["data"]["registration_nonce"]

    d = datetime.now(timezone.utc)
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    timestamp = math.trunc((d - epoch).total_seconds() * 1_000)

    register_message = Registration(
        broker_id=broker_id,
        chain_id=chain_id,
        timestamp=timestamp,
        registration_nonce=registration_nonce,
    )

    encoded_data = hash_eip712_bytes(domain, register_message)
    signed_message = wallet.sign_hash(encoded_data)

    async with httpx.AsyncClient() as client:
        res = await client.post(
            "%s/v1/register_account" % base_url,
            headers={"Content-Type": "application/json"},
            json={
                "message": register_message.model_dump(),
                "signature": signed_message.signature.hex(),
                "userAddress": wallet.address,
            },
        )
    response = res.json()

    if not response["success"]:
        raise OrderlyAccountCreationException(response["message"])

    orderly_account_id = response["data"]["account_id"]
    return orderly_account_id
