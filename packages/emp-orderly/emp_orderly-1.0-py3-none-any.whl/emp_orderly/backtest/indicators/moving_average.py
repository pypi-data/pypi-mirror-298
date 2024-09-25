import pandas as pd
import pandas_ta as ta


def SMA(arr: pd.Series, n: int) -> pd.Series:
    """
    Returns `n`-period simple moving average of array `arr`.
    """
    series = pd.Series(arr)
    return ta.sma(series, length=n)


def EMA(arr: pd.Series, n: int) -> pd.Series:
    """
    Returns `n`-period simple moving average of array `arr`.
    """
    series = pd.Series(arr)
    return ta.ema(series, length=n)


def CHOP(arr: pd.Series, n: int) -> pd.Series:
    """
    Returns `n`-period simple moving average of array `arr`.
    """
    series = pd.Series(arr)
    return ta.chop(series, length=n)


def SLOPE(arr: pd.Series, n: int) -> pd.Series:
    """
    Returns `n`-period simple moving average of array `arr`.
    """
    series = pd.Series(arr)
    return ta.slope(series, length=n)
