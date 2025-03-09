# -*- coding: utf-8 -*-
# volume_weighted_average_price_bands.py
import numpy as np
import pandas as pd


def volume_weighted_average_price_bands(
    df: pd.DataFrame, window_size: int = 20, num_of_std: float = 1.0
) -> pd.DataFrame:
    """Volume-Weighted Average Price Bands"""
    if not {"close", "high", "low", "volume"}.issubset(df.columns):
        raise ValueError(
            "DataFrame must contain 'close', 'high', 'low', and 'volume' columns."
        )

    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()

    # Calculate typical price
    df_copy["typical_price"] = (df_copy["close"] + df_copy["high"] + df_copy["low"]) / 3

    # Calculate cumulative VWAP
    df_copy["cum_typical_volume"] = (
        df_copy["typical_price"] * df_copy["volume"]
    ).cumsum()
    df_copy["cum_volume"] = df_copy["volume"].cumsum()
    df_copy["vwap"] = df_copy["cum_typical_volume"] / df_copy["cum_volume"]

    # Calculate rolling standard deviation for VWAP
    rolling_std = df_copy["vwap"].rolling(window=window_size).std()

    # Calculate VWAP bands
    df_copy["vwap_low"] = df_copy["vwap"] - (rolling_std * num_of_std)
    df_copy["vwap_high"] = df_copy["vwap"] + (rolling_std * num_of_std)

    # Return only the relevant columns
    return df_copy[["vwap_low", "vwap", "vwap_high"]]


volume_weighted_average_price_bands.__doc__ = """
Name:
    Volume-Weighted Average Price Bands (VWAPB)

Description:
    Calculates the Volume-Weighted Average Price (VWAP) along with upper and lower bands
    based on a rolling standard deviation. The VWAP provides a cumulative weighted average 
    price, while the bands create a channel that can help identify potential support and 
    resistance levels. Price movement outside these bands may indicate overbought or 
    oversold conditions.

More info:
    https://www.investopedia.com/terms/v/vwap.asp

Parameters:
    - df (pd.DataFrame): Input DataFrame containing the following required columns:
        - 'close': Closing price.
        - 'high': High price for each interval.
        - 'low': Low price for each interval.
        - 'volume': Trading volume for each interval.
    - window_size (int, default=20): The rolling window size for VWAP and standard deviation calculations.
    - num_of_std (float, default=1.0): The number of standard deviations to calculate the upper and lower bands.

Call with:
    vwapb_result = bta.volume_weighted_average_price_bands(df, window_size=20, num_of_std=1.0)
    df['vwap_low'] = vwapb_result['vwap_low']
    df['vwap'] = vwapb_result['vwap']
    df['vwap_high'] = vwapb_result['vwap_high']

Returns:
    pd.DataFrame: A DataFrame containing the following columns:
        - 'vwap': The Volume-Weighted Average Price (VWAP).
        - 'vwap_low': The lower band (VWAP - num_of_std × rolling std deviation).
        - 'vwap_high': The upper band (VWAP + num_of_std × rolling std deviation).
"""


def test():
    """
    Test function for the volume_weighted_average_price_bands indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the volume_weighted_average_price_bands indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(volume_weighted_average_price_bands)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
