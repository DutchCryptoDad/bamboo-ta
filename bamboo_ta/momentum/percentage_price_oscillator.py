# -*- coding: utf-8 -*-
# percentage_price_oscillator.py

import pandas as pd


def percentage_price_oscillator(
    df: pd.DataFrame,
    close_col: str = "close",
    window_slow: int = 26,
    window_fast: int = 12,
    window_sign: int = 9,
    fillna: bool = False,
) -> pd.DataFrame:
    """Percentage Price Oscillator (PPO)"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required column
    if close_col not in df.columns:
        raise KeyError(f"DataFrame must contain '{close_col}' column")

    close = df_copy[close_col]

    # Calculate EMA
    emafast = close.ewm(span=window_fast, adjust=False).mean()
    emaslow = close.ewm(span=window_slow, adjust=False).mean()
    ppo = ((emafast - emaslow) / emaslow) * 100

    ppo_signal = ppo.ewm(span=window_sign, adjust=False).mean()
    ppo_hist = ppo - ppo_signal

    if fillna:
        ppo = ppo.fillna(0)
        ppo_signal = ppo_signal.fillna(0)
        ppo_hist = ppo_hist.fillna(0)

    df_copy["ppo"] = ppo
    df_copy["ppo_signal"] = ppo_signal
    df_copy["ppo_hist"] = ppo_hist

    return df_copy[["ppo", "ppo_signal", "ppo_hist"]]


percentage_price_oscillator.__doc__ = """
Name:
    Percentage Price Oscillator (PPO)

Description:
    The Percentage Price Oscillator (PPO) is a technical indicator that shows the relationship
    between two moving averages of a security's price. It is calculated by subtracting a slow
    exponential moving average (EMA) from a fast EMA and then dividing the result by the slow EMA.

More info:
    https://www.investopedia.com/terms/p/ppo.asp

Call with:
    ppo = bta.percentage_price_oscillator(df)
    df['ppo'] = ppo['ppo']
    df['ppo_signal'] = ppo['ppo_signal']
    df['ppo_hist'] = ppo['ppo_hist']

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the close column.
    - close_col (str): Name of the column containing close price data. Default is 'close'.
    - window_slow (int): n period long-term. Default is 26.
    - window_fast (int): n period short-term. Default is 12.
    - window_sign (int): n period to signal. Default is 9.
    - fillna (bool): if True, fill nan values. Default is False.

Returns:
    pd.DataFrame: DataFrame with columns ['ppo', 'ppo_signal', 'ppo_hist'].
"""
