import json
from typing import Literal

from base58 import b58encode
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from eth_rpc import PrivateKeyWallet
from eth_rpc.types import hash_eip712_bytes
import httpx

from emp_orderly.types.domains import make_domain, AddOrderlyKey
from emp_orderly.utils import make_timestamp


def encode_key(key: bytes):
    return "ed25519:%s" % b58encode(key).decode("utf-8")


def encode_raw(orderly_key: Ed25519PrivateKey):
    return encode_key(orderly_key.public_key().public_bytes_raw())


async def add_access_key(
    wallet: PrivateKeyWallet,
    orderly_key: str,
    base_url: str = "https://testnet-api-evm.orderly.org",
    broker_id: Literal["empyreal"] = "empyreal",
    chain_id: int = 421614,
) -> str:
    """
    wallet = PrivateKeyWallet.create_new()
    orderly_key = Ed25519PrivateKey.generate()

    An orderly key is just a public key formatted in base58 with a `ed25519:` prefix

    returns:
        the users orderly key as a string
    """
    offchain_domain = make_domain(chain_id=chain_id)

    timestamp = make_timestamp()

    add_key_message = AddOrderlyKey(
        broker_id=broker_id,
        chain_id=chain_id,
        orderly_key=orderly_key,
        scope="read,trading",
        timestamp=timestamp,
        expiration=timestamp + 1_000 * 60 * 60 * 24 * 365,  # 1 year
    )

    encoded_data = hash_eip712_bytes(offchain_domain, add_key_message)
    signed_message = wallet.sign_hash(encoded_data)

    async with httpx.AsyncClient() as client:
        res = await client.post(
            "%s/v1/orderly_key" % base_url,
            headers={"Content-Type": "application/json"},
            json={
                "message": add_key_message.model_dump(),
                "signature": signed_message.signature.hex(),
                "userAddress": wallet.address,
            },
        )
    response = json.loads(res.text)
    if not response['success']:
        raise ValueError(response['message'])
    return response['data']['orderly_key']
