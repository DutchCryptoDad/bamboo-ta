# -*- coding: utf-8 -*-
# first_crossed_below_second.py
import pandas as pd


def first_crossed_below_second(series1: pd.Series, series2: pd.Series) -> pd.Series:
    """
    Check if series1 crosses below series2 in a vectorized manner.

    Parameters:
    - series1 (pd.Series): First input series to check for crossover.
    - series2 (pd.Series): Second input series to compare against.

    Call with:
        df['first_crossed_below_second'] = bta.first_crossed_below_second(series1, series2)

    Returns:
    - pd.Series: Boolean series where True indicates a crossover below.
    """
    # Ensure both series have the same length
    if len(series1) != len(series2):
        raise ValueError("Input series must have the same length")

    # Vectorized check for crossover below
    return (series1 < series2) & (series1.shift(1) >= series2.shift(1))


first_crossed_below_second.__doc__ = """
Name:
    First Crossed Below Second

Description:
    This function checks if the first series crosses below the second series.
    It returns a boolean series where True indicates the exact candle where
    the crossover occurred. This is useful for generating trading signals
    based on indicator crossovers.
    
    The function performs a vectorized comparison, making it efficient for
    large datasets.

More info:
    In technical analysis, crossovers often indicate potential trading signals.
    For example, when a faster moving average crosses below a slower moving average,
    it may indicate a bearish signal.

Parameters:
    - series1 (pd.Series): First input series to check for crossover (e.g., fast moving average).
    - series2 (pd.Series): Second input series to compare against (e.g., slow moving average).

Call with:
    df['cross_down'] = bta.first_crossed_below_second(df['ema5'], df['ema20'])

Returns:
    pd.Series: Boolean series where True indicates a crossover below.
"""
