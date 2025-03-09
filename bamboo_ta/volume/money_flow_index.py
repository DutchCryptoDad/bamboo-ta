# -*- coding: utf-8 -*-
# money_flow_index.py
import numpy as np
import pandas as pd


def money_flow_index(
    df: pd.DataFrame, window: int = 14, fillna: bool = False
) -> pd.DataFrame:
    """Money Flow Index"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate typical price
    typical_price = (df_copy["high"] + df_copy["low"] + df_copy["close"]) / 3.0
    up_down = np.where(
        typical_price > typical_price.shift(1),
        1,
        np.where(typical_price < typical_price.shift(1), -1, 0),
    )
    mfr = typical_price * df_copy["volume"] * up_down

    # Calculate positive and negative money flow
    min_periods = 0 if fillna else window
    n_positive_mf = mfr.rolling(window, min_periods=min_periods).apply(
        lambda x: np.sum(np.where(x >= 0.0, x, 0.0)), raw=True
    )
    n_negative_mf = abs(
        mfr.rolling(window, min_periods=min_periods).apply(
            lambda x: np.sum(np.where(x < 0.0, x, 0.0)), raw=True
        )
    )

    # Calculate Money Flow Index
    mfi = n_positive_mf / n_negative_mf
    mfi = 100 - (100 / (1 + mfi))
    if fillna:
        mfi = mfi.fillna(50)

    df_copy["mfi"] = mfi

    return df_copy[["mfi"]]


money_flow_index.__doc__ = """
Name:
    Money Flow Index (MFI)

Description:
    The Money Flow Index (MFI) uses both price and volume to measure buying and selling pressure.
    It is often referred to as volume-weighted RSI. MFI is a momentum indicator that analyzes
    the flow of money into and out of an asset. Values above 80 are considered overbought,
    while values below 20 are considered oversold.

More info:
    https://www.investopedia.com/terms/m/mfi.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - window (int): Period for calculating MFI. Default is 14.
    - fillna (bool): If True, fill NaN values.

Call with:
    df['mfi'] = bta.money_flow_index(df, window=14, fillna=True)['mfi']

Returns:
    pd.DataFrame: DataFrame with 'mfi' column.
"""
