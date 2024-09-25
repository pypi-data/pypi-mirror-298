from datetime import datetime, timezone
import math


def make_timestamp():
    d = datetime.now(timezone.utc)
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    timestamp = math.trunc((d - epoch).total_seconds() * 1_000)
    return timestamp
