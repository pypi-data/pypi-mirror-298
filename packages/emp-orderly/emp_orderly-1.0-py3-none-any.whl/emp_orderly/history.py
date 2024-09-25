from dataclasses import dataclass
from typing import Union
from datetime import datetime, timezone

from emp_orderly_types import Interval, PerpetualAssetType


@dataclass
class OHLCV:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume_asset: float
    volume: float


def to_unix(dt: Union[datetime, int]):
    if isinstance(dt, int):
        return dt
    if not dt.tzinfo:
        raise ValueError("date is missing timezone information")

    d2 = datetime(1970, 1, 1, tzinfo=timezone.utc)
    time_delta = dt - d2
    return int(time_delta.total_seconds())


class OrderlyHistory:
    async def get_ohlcv(
        self,
        asset: PerpetualAssetType = PerpetualAssetType.BTC,
        resolution: Interval = Interval.minute,
        start_days_behind: float = 1.0,
        end_days_behind: float = 0.0,
        scale: int = 1,
    ):
        import pandas as pd

        start_time = int(
            datetime.now(timezone.utc).timestamp() - start_days_behind * 86_400
        )
        end_time = int(
            datetime.now(timezone.utc).timestamp() - end_days_behind * 86_400
        )
        res = await self._send_request_async(
            "tv/history",
            params={
                "symbol": asset.value,
                "resolution": resolution,
                "from": start_time,
                "to": end_time,
            },
        )

        timestamp = res["t"]
        opens = res["o"]
        closes = res["c"]
        highs = res["h"]
        lows = res["l"]
        volumes = res["v"]
        a_s = res["a"]

        results = []
        for row in zip(timestamp, opens, closes, highs, lows, volumes, a_s):
            results.append(
                OHLCV(
                    timestamp=datetime.fromtimestamp(row[0]),
                    open=row[1],
                    close=row[2],
                    high=row[3],
                    low=row[4],
                    volume_asset=row[5],
                    volume=row[6],
                )
            )
        return pd.DataFrame(results).set_index("timestamp") / scale

    def _send_request(self, path, body=None, params=None, method="GET"):
        raise NotImplementedError()

    def _send_request_async(self, path, body=None, params=None, method="GET"):
        raise NotImplementedError()
