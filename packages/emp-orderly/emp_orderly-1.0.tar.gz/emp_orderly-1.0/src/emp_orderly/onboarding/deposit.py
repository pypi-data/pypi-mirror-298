from eth_rpc import Network, PrivateKeyWallet, set_default_network
from eth_rpc.networks import ArbitrumSepolia
from eth_rpc.utils import to_checksum
from eth_typing import HexStr
from eth_typeshed.erc20 import ERC20, ApproveRequest


async def deposit(wallet: PrivateKeyWallet, deposit_amount: int = 100000, network: type[Network] = ArbitrumSepolia) -> HexStr:
    set_default_network(network)

    usdc = ERC20(address=to_checksum("0x75faf114eafb1BDbe2F0316DF893fd58CE46AA4d"))
    vault_address = to_checksum("0x0EaC556c0C2321BA25b9DC01e4e3c95aD5CDCd2f")

    # approve USDC ERC-20 to be transferred to Vault contract
    return await usdc.approve(ApproveRequest(
        spender=vault_address,
        amount=deposit_amount,
    )).execute(wallet)
