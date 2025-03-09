# -*- coding: utf-8 -*-
# get_min_max.py
import numpy as np
import pandas as pd


def get_min_max(
    series1: pd.Series, series2: pd.Series, function: str = "min"
) -> pd.Series:
    """
    Find the minimum or maximum value between two series for each index.

    Parameters:
    - series1 (pd.Series): First input series.
    - series2 (pd.Series): Second input series.
    - function (str): Function to apply ("min" or "max"). Default is "min".

    Call with:
        df['min_max'] = bta.get_min_max(series1, series2, function)
    Like:
        df['min_max'] = bta.get_min_max(df['open'], df['open'], 'max')

    Returns:
    - pd.Series: Series with min or max values for each index.
    """
    series1 = np.array(series1)
    series2 = np.array(series2)

    if function == "min":
        output = np.amin([series1, series2], axis=0)
    elif function == "max":
        output = np.amax([series1, series2], axis=0)
    else:
        raise ValueError('"function" variable should be "min" or "max"')

    return pd.Series(output)


get_min_max.__doc__ = """
Name:
    Get Min Max

Description:
    This utility function compares two data series element by element and returns
    either the minimum or maximum value at each position, depending on the specified
    function parameter.
    
    It's particularly useful when you need to create support/resistance lines, 
    determine price extremes, or compare different indicators.

More info:
    This function uses NumPy's efficient array operations to quickly process 
    large datasets without loops.

Parameters:
    - series1 (pd.Series): First input series.
    - series2 (pd.Series): Second input series.
    - function (str): Function to apply, either "min" or "max". Default is "min".

Call with:
    df['min_values'] = bta.get_min_max(df['close'], df['sma20'], 'min')
    df['max_values'] = bta.get_min_max(df['high'], df['upper_band'], 'max')

Returns:
    pd.Series: A series containing the minimum or maximum values between the two input
    series at each position.
"""
