MESSAGE_TYPES = {
    "EIP712Domain": [
        {"name": "name", "type": "string"},
        {"name": "version", "type": "string"},
        {"name": "chainId", "type": "uint256"},
        {"name": "verifyingContract", "type": "address"},
    ],
    "AddOrderlyKey": [
        {"name": "brokerId", "type": "string"},
        {"name": "chainId", "type": "uint256"},
        {"name": "orderlyKey", "type": "string"},
        {"name": "scope", "type": "string"},
        {"name": "timestamp", "type": "uint64"},
        {"name": "expiration", "type": "uint64"},
    ],
    "Registration": [
        {"name": "brokerId", "type": "string"},
        {"name": "chainId", "type": "uint256"},
        {"name": "timestamp", "type": "uint64"},
        {"name": "registrationNonce", "type": "uint256"},
    ],
}
