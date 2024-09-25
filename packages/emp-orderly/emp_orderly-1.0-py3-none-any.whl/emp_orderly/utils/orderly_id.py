from eth_hash.auto import keccak
from eth_abi import encode
from eth_typing import HexAddress, HexStr

def from_address(address: HexAddress, broker_id: str = 'empyreal') -> HexStr:
    encoded = encode(['address', 'bytes32'], [address, keccak(broker_id.encode('utf-8'))])
    return HexStr(f'0x{keccak(encoded).hex()}')
