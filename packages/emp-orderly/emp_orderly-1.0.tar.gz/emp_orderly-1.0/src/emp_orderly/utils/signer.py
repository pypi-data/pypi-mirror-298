from base64 import urlsafe_b64encode
from datetime import datetime, timezone
import json as jsonlib
import math
import secrets
from typing import Literal
from urllib.parse import urlparse

from eth_abi import encode
from eth_hash.auto import keccak
from eth_typing import HexAddress
from eth_utils import to_bytes, to_hex
from base58 import b58encode
from pydantic import BaseModel, PrivateAttr
from requests import PreparedRequest, Request

from .ed25519 import publickey, sign


class OrderlySigner(BaseModel):
    account_id: str
    broker_id: str
    _private_key: bytes = PrivateAttr()
    _orderly_key: str = PrivateAttr()

    def __init__(
        self,
        account_id: str,
        private_key: str,
        # private_key: str,
        broker_id: str = "logx",
    ) -> None:
        # account: LocalAccount = Account.from_key(private_key)
        # account_id = get_account_id(account.address, broker_id)
        # super().__init__(
        #     account_id=account_id,
        #     broker_id=broker_id,
        # )
        # self._private_key = bytes.fromhex(private_key.removeprefix("0x"))
        # self._orderly_key = self.get_orderly_key(private_key)
        super().__init__(
            account_id=account_id,
            broker_id=broker_id,
        )
        self._private_key = bytes.fromhex(private_key.removeprefix("0x"))
        self._orderly_key = self.get_orderly_key(private_key)

    @classmethod
    def get_orderly_key(self, private_key_hex: str):
        key_bytes = publickey(bytes.fromhex(private_key_hex.removeprefix("0x")))
        orderly_key = "ed25519:%s" % b58encode(key_bytes).decode("utf-8")
        return orderly_key

    @classmethod
    def generate(self):
        private_key_hex = "0x" + secrets.token_hex(32)
        key_bytes = publickey(bytes.fromhex(private_key_hex.removeprefix("0x")))
        orderly_key = "ed25519:%s" % b58encode(key_bytes).decode("utf-8")

        return orderly_key, f"0x{key_bytes.hex()}", private_key_hex

    def orderly_key(self):
        return encode_key(publickey(self._private_key))

    def now(self):
        return int(datetime.now().timestamp())

    def build_headers(
        self, url: str, method: Literal["GET", "PUT", "POST", "DELETE"], params, json
    ):
        d = datetime.now(timezone.utc)
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
        timestamp = math.trunc((d - epoch).total_seconds() * 1_000)
        query_string = ""
        if params:
            query_string = "?"
            for k, v in params.items():
                if type(v) is bool:
                    query_string += f"{k}={v}&"
                elif v is not None:
                    query_string += f"{k}={str(v)}&"
            query_string = query_string.rstrip("&")
        json_str = ""
        if json is not None:
            json_str = jsonlib.dumps(json)
        path = urlparse(url).path
        message = str(timestamp) + method + path + query_string + json_str
        orderly_signature = urlsafe_b64encode(
            sign(self._private_key, message.encode())
        ).decode("utf-8")

        headers = {
            "orderly-timestamp": str(timestamp),
            "orderly-account-id": self.account_id,
            "orderly-key": self._orderly_key,
            "orderly-signature": orderly_signature,
        }
        headers["Content-Type"] = (
            "application/json" if json else "application/x-www-form-urlencoded"
        )
        return headers

    def sign_request(self, req: Request) -> PreparedRequest:
        d = datetime.now(timezone.utc)
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
        timestamp = math.trunc((d - epoch).total_seconds() * 1_000)
        query_string = ""
        if req.params:
            query_string = "?"
            for k, v in dict(sorted(req.params.items())).items():
                if type(v) is bool:
                    query_string += f"{k}={v}&"
                elif v is not None:
                    query_string += f"{k}={str(v)}&"
            query_string = query_string.rstrip("&")
        json_str = ""
        if req.json is not None:
            json_str = jsonlib.dumps(req.json)

        path = urlparse(req.url).path
        message = str(timestamp) + req.method + path + query_string + json_str
        orderly_signature = urlsafe_b64encode(
            sign(self._private_key, message.encode())
        ).decode("utf-8")

        req.headers = {
            "orderly-timestamp": str(timestamp),
            "orderly-account-id": self.account_id,
            "orderly-key": self._orderly_key,
            "orderly-signature": orderly_signature,
        }
        req.headers["Content-Type"] = (
            "application/json" if req.json else "application/x-www-form-urlencoded"
        )
        return req.prepare()


def encode_key(public_key: bytes):
    """Convert a public key to an orderly key"""
    return "ed25519:%s" % b58encode(public_key).decode("utf-8")


def get_account_id(user_address: HexAddress, broker_id: str):
    """
    An orderly account id is generated from a user's wallet address and broker id
    """
    user_address_bytes = to_bytes(hexstr=user_address)
    broker_id_bytes = keccak(broker_id.encode("utf-8"))
    encoded_data = encode(["address", "bytes32"], [user_address_bytes, broker_id_bytes])
    return to_hex(keccak(encoded_data))
