# -*- coding: utf-8 -*-
# on_balance_volume.py
import numpy as np
import pandas as pd


def on_balance_volume(
    df: pd.DataFrame,
    signal_type: str = "SMA",
    signal_length: int = 21,
    show_signal: bool = True,
    fillna: bool = False,
) -> pd.DataFrame:
    """On Balance Volume"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate OBV
    df_copy["change"] = df_copy["close"].diff()
    df_copy["obv"] = np.where(
        df_copy["change"] > 0,
        df_copy["volume"],
        np.where(df_copy["change"] < 0, -df_copy["volume"], 0),
    )
    df_copy["obv"] = df_copy["obv"].cumsum()

    # Calculate Signal if requested
    if show_signal:
        if signal_type == "EMA":
            df_copy["signal"] = (
                df_copy["obv"].ewm(span=signal_length, adjust=False).mean()
            )
        elif signal_type == "SMA":
            df_copy["signal"] = (
                df_copy["obv"].rolling(window=signal_length, min_periods=1).mean()
            )
        else:
            raise ValueError(f"Invalid signal_type: {signal_type}. Use 'EMA' or 'SMA'.")
    else:
        df_copy["signal"] = np.nan

    # Fill NaN values if requested
    if fillna:
        df_copy["obv"] = df_copy["obv"].fillna(0)
        df_copy["signal"] = df_copy["signal"].fillna(0)

    return df_copy[["obv", "signal"]]


on_balance_volume.__doc__ = """
Name:
    On Balance Volume (OBV)

Description:
    The On Balance Volume (OBV) indicator measures buying and selling pressure by accumulating 
    volume based on price movements. When the close price is higher than the previous close, 
    the volume is added to the OBV; when lower, it's subtracted. Rising OBV indicates buying 
    pressure, and falling OBV suggests selling pressure. This implementation includes an 
    optional signal line for additional trend confirmation.

More info:
    https://www.investopedia.com/terms/o/onbalancevolume.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - signal_type (str): Type of signal smoothing ('EMA' or 'SMA'). Default is 'SMA'.
    - signal_length (int): Length for the signal smoothing. Default is 21.
    - show_signal (bool): If True, calculate and return the signal line. Default is True.
    - fillna (bool): If True, fill nan values with 0. Default is False.

Call with:
    obv_df = bta.on_balance_volume(df, signal_type='SMA', signal_length=21, show_signal=True, fillna=True)
    df['obv'] = obv_df['obv']
    df['signal'] = obv_df['signal']

Returns:
    pd.DataFrame: DataFrame with 'obv' and 'signal' columns.
"""
