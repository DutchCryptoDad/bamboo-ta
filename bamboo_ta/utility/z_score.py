# -*- coding: utf-8 -*-
# z_score.py
import pandas as pd


def z_score(series: pd.Series, window: int = 500) -> pd.Series:
    """
    Calculate the z-score of a series.

    Parameters:
    - series (pd.Series): Input series.
    - window (int): Lookback window for mean and standard deviation calculation.

    Call with:
        df['zscore']  = bta.z_score(series)

    Like:
        df['zscore']  = bta.z_score(df['close'])

    Returns:
    - pd.Series: Z-score series.
    """
    mean = series.rolling(window=window, min_periods=1).mean()
    std = series.rolling(window=window, min_periods=1).std(ddof=0)
    zscore = (series - mean) / std
    zscore = zscore.fillna(
        0
    )  # Fill NaN values with 0 to avoid issues with calculations

    return zscore


z_score.__doc__ = """
Name:
    Z-Score

Description:
    The Z-Score measures how many standard deviations a data point is from the mean 
    of a dataset. In finance, it helps identify when prices or indicators are statistically 
    abnormal relative to their historical values.
    
    A Z-Score of 0 means the value is exactly at the mean. Positive Z-Scores indicate
    values above the mean, while negative Z-Scores indicate values below the mean.
    
    Typical interpretation:
    - Z-Score > 2: Significantly higher than normal (potentially overbought)
    - Z-Score < -2: Significantly lower than normal (potentially oversold)

More info:
    https://www.investopedia.com/terms/z/zscore.asp

Parameters:
    - series (pd.Series): Input series of values to analyze.
    - window (int, default=500): Lookback window for calculating the mean and standard deviation.

Call with:
    df['zscore'] = bta.z_score(df['close'], window=200)

Returns:
    pd.Series: The Z-Score values for each point in the input series.
"""
