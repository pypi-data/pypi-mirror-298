from eth_typing import HexAddress, HexStr
from eth_rpc.types.typed_data import Domain, EIP712Model
from eth_rpc.types import primitives
from pydantic import Field


def make_domain(
    chain_id: int,
    verifying_contract: HexAddress = HexAddress(HexStr("0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC")),
):
    """
    Verifying Domain is 0xccc.. for offchain signatures
    """
    return Domain(
        name="Orderly",
        version="1",
        chain_id=chain_id,
        verifying_contract=verifying_contract,
    )

class Registration(EIP712Model):
    broker_id: str = Field(serialization_alias="brokerId")
    chain_id: primitives.uint256 = Field(serialization_alias="chainId")
    timestamp: primitives.uint64
    registration_nonce: primitives.uint256 = Field(serialization_alias="registrationNonce")


class AddOrderlyKey(EIP712Model):
    broker_id: str = Field(serialization_alias="brokerId")
    chain_id: primitives.uint256 = Field(serialization_alias="chainId")
    orderly_key: primitives.string = Field(serialization_alias="orderlyKey")
    scope: primitives.string
    timestamp: primitives.uint64
    expiration: primitives.uint64


class Withdraw(EIP712Model):
    broker_id: str = Field(serialization_alias="brokerId")
    chain_id: primitives.uint256 = Field(serialization_alias="chainId")
    receiver: primitives.address
    token: primitives.string
    amount: primitives.uint256
    timestamp: primitives.uint64
    expiration: primitives.uint64


class SettlePnl(EIP712Model):
    broker_id: str = Field(serialization_alias="brokerId")
    chain_id: primitives.uint256 = Field(serialization_alias="chainId")
    settle_nonce: primitives.uint64 = Field(serialization_alias="settleNonce")
    timestamp: primitives.uint64


class DelegateSigner(EIP712Model):
    delegate_contract: primitives.address = Field(serialization_alias="delegateContract")
    broker_id: str = Field(serialization_alias="brokerId")
    chain_id: primitives.uint256 = Field(serialization_alias="chainId")
    timestamp: primitives.uint64
    registration_nonce: primitives.uint64 = Field(serialization_alias="registrationNonce")
    tx_hash: primitives.bytes32 = Field(serialization_alias="txHash")


class DelegateAddOrderlyKey(EIP712Model):
    delegate_contract: primitives.address = Field(serialization_alias="delegateContract")
    broker_id: str = Field(serialization_alias="brokerId")
    chain_id: primitives.uint256 = Field(serialization_alias="chainId")
    orderly_key: primitives.string = Field(serialization_alias="orderlyKey")
    scope: primitives.string
    timestamp: primitives.uint64
    expiration: primitives.uint64


class DelegateWithdraw(EIP712Model):
    delegate_contract: primitives.address = Field(serialization_alias="delegateContract")
    broker_id: str = Field(serialization_alias="brokerId")
    chain_id: primitives.uint256 = Field(serialization_alias="chainId")
    receiver: primitives.address
    token: primitives.string
    amount: primitives.uint256
    withdraw_nonce: primitives.uint64 = Field(serialization_alias="withdrawNonce")
    timestamp: primitives.uint64


class DelegateSettlePnl(EIP712Model):
    delegate_contract: primitives.address = Field(serialization_alias="delegateContract")
    broker_id: str = Field(serialization_alias="brokerId")
    chain_id: primitives.uint256 = Field(serialization_alias="chainId")
    settle_nonce: primitives.uint64 = Field(serialization_alias="settleNonce")
    timestamp: primitives.uint64
