# -*- coding: utf-8 -*-
# price_volume_trend.py
import numpy as np
import pandas as pd


def price_volume_trend(
    df: pd.DataFrame,
    fillna: bool = False,
    smoothing_factor: int = None,
    signal_type: str = "SMA",
    signal_length: int = 21,
    dropnans: bool = False,
) -> pd.DataFrame:
    """Price Volume Trend"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Initialize PVT column
    df_copy["price_volume_trend"] = 0.0

    # Calculate PVT iteratively
    for i in range(1, len(df_copy)):
        prev_pvt = df_copy.at[i - 1, "price_volume_trend"]
        price_change = (
            df_copy.at[i, "close"] - df_copy.at[i - 1, "close"]
        ) / df_copy.at[i - 1, "close"]
        df_copy.at[i, "price_volume_trend"] = (
            price_change * df_copy.at[i, "volume"] + prev_pvt
        )

    # Optional smoothing
    if smoothing_factor:
        min_periods = 0 if fillna else smoothing_factor
        df_copy["price_volume_trend"] = (
            df_copy["price_volume_trend"]
            .rolling(smoothing_factor, min_periods=min_periods)
            .mean()
        )

    if dropnans:
        df_copy["price_volume_trend"] = df_copy["price_volume_trend"].dropna()

    if fillna:
        df_copy["price_volume_trend"] = df_copy["price_volume_trend"].fillna(0)

    # Calculate signal based on the specified type
    if signal_type == "SMA":
        df_copy["signal"] = (
            df_copy["price_volume_trend"]
            .rolling(window=signal_length, min_periods=1 if fillna else signal_length)
            .mean()
        )
    elif signal_type == "EMA":
        df_copy["signal"] = (
            df_copy["price_volume_trend"]
            .ewm(
                span=signal_length,
                adjust=False,
                min_periods=1 if fillna else signal_length,
            )
            .mean()
        )
    else:
        raise ValueError("signal_type must be either 'SMA' or 'EMA'")

    if dropnans:
        df_copy["signal"] = df_copy["signal"].dropna()

    if fillna:
        df_copy["signal"] = df_copy["signal"].fillna(0)

    return df_copy[["price_volume_trend", "signal"]]


price_volume_trend.__doc__ = """
Name:
    Price Volume Trend (PVT)

Description:
    Based on cumulative volume that adds or subtracts a multiple of the percentage change in 
    share price trend. The PVT is similar to On Balance Volume (OBV) but instead of adding 
    or subtracting the entire volume, it adds or subtracts a portion of the volume based on 
    the percentage price change. This creates a more refined volume-based indicator that 
    responds proportionally to price movements.

More info:
    https://www.investopedia.com/terms/p/pvtrend.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - fillna (bool): If True, fill nan values.
    - smoothing_factor (int, optional): Will smooth PVT implementation with SMA.
    - signal_type (str): Type of signal smoothing ('SMA' or 'EMA').
    - signal_length (int): Length of the signal smoothing.
    - dropnans (bool): Drop NaN values after indicator calculated.

Call with:
    pvt_df = bta.price_volume_trend(df, fillna=True, signal_type='EMA', signal_length=21, dropnans=True)
    df['pvt'] = pvt_df['price_volume_trend']
    df['pvt_signal'] = pvt_df['signal']

Returns:
    pd.DataFrame: DataFrame with 'price_volume_trend' and 'signal' columns.
"""


def test():
    """
    Test function for the price_volume_trend indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the price_volume_trend indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(price_volume_trend)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
