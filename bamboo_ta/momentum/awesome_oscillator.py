# -*- coding: utf-8 -*-
# awesome_oscillator.py
import pandas as pd 

def awesome_oscillator(
    df: pd.DataFrame, 
    high_col: str = 'high', 
    low_col: str = 'low', 
    window1: int = 5, 
    window2: int = 34, 
    fillna: bool = False
) -> pd.DataFrame:
    """Awesome Oscillator (AO)"""
    df_copy = df.copy()

    median_price = 0.5 * (df_copy[high_col] + df_copy[low_col])
    min_periods_s = 0 if fillna else window1
    min_periods_l = 0 if fillna else window2

    df_copy['ao'] = (
        median_price.rolling(window1, min_periods=min_periods_s).mean()
        - median_price.rolling(window2, min_periods=min_periods_l).mean()
    )
    
    if fillna:
        df_copy['ao'] = df_copy['ao'].fillna(0)

    return df_copy[['ao']]

awesome_oscillator.__doc__ = \
"""
Name:
    Awesome Oscillator

Description:
    The Awesome Oscillator is a momentum indicator used to measure market momentum.
    It is calculated by subtracting a 34-period simple moving average (SMA) of the
    median price from a 5-period SMA of the median price.

More info:
    https://www.investopedia.com/terms/a/awesomeoscillator.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing 'high' and 'low' columns.
    - high_col (str): The name of the 'high' column. Default is 'high'.
    - low_col (str): The name of the 'low' column. Default is 'low'.
    - window1 (int, optional): Short period. Default is 5.
    - window2 (int, optional): Long period. Default is 34.
    - fillna (bool, optional): If True, fill nan values with 0. Default is False.

Call with:
    df['ao'] = bta.awesome_oscillator(df, 'high', 'low', 5, 34)['ao']

Returns:
    pd.DataFrame: DataFrame with the 'ao' column.
"""
