# -*- coding: utf-8 -*-
# daily_return.py
import numpy as np
import pandas as pd


def daily_return(
    df: pd.DataFrame, column: str = "close", fillna: bool = False
) -> pd.Series:
    """
    Calculate the Daily Return (DR) of a specified column in a DataFrame.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which the daily return is to be calculated. Default is "close".
    - fillna (bool): If True, fill NaN values with 0. Default is False.

    Call with:
        df['daily_return'] = bta.daily_return(df)

    Returns:
    - pd.Series: Series of daily return values.
    """
    # Copy the DataFrame to avoid modifying the original data
    df_copy = df.copy()

    # Calculate the daily return as a percentage
    df_copy["daily_return"] = (df_copy[column] / df_copy[column].shift(1)) - 1
    df_copy["daily_return"] *= 100

    # Handle NaN values if requested
    if fillna:
        df_copy["daily_return"] = df_copy["daily_return"].fillna(0)

    return df_copy["daily_return"].rename("daily_return")


daily_return.__doc__ = """
Name:
    Daily Return

Description:
    Daily Return (also known as simple return) calculates the percentage change in price
    between consecutive periods. It's a fundamental measure in financial analysis that
    shows how much an investment has gained or lost over a single period, expressed as
    a percentage of the initial investment.

More info:
    The formula for daily return is: ((Pt/Pt-1) - 1) * 100, where Pt is the price at time t.
    
    This is the standard measure of return used in many financial applications. Unlike
    logarithmic returns, simple returns directly represent the actual percentage gain or
    loss experienced by an investor.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which the daily return is to be calculated. Default is "close".
    - fillna (bool): If True, fill NaN values with 0. Default is False.

Call with:
    df['daily_ret'] = bta.daily_return(df)
    
    # Using a different price column:
    df['daily_ret'] = bta.daily_return(df, column='adjusted_close')

Returns:
    pd.Series: Series of daily return values expressed as percentages.
"""
