import httpx


async def request_testnet_funds(wallet, chain_id: int = 421614, broker_id: str = "empyreal") -> bool:
    url = "https://testnet-operator-evm.orderly.org/v1/faucet/usdc"
    payload = {
        "chain_id": str(chain_id),
        "user_address": wallet.address,
        "broker_id": broker_id
    }
    headers = {"Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.request("POST", url, json=payload, headers=headers)
    return response.json()['success']
