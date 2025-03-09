# -*- coding: utf-8 -*-
# bollinger_trend_fast_with_ma.py
import numpy as np
import pandas as pd


def bollinger_trend_fast_with_ma(
    df: pd.DataFrame,
    column: str = "close",
    short_length: int = 10,
    long_length: int = 50,
    short_stddev: float = 1.0,
    long_stddev: float = 2.0,
    ma_type: str = "SMA",
    ma_length: int = 14,
) -> pd.DataFrame:
    """Bollinger Trend Indicator with Selectable Moving Average"""
    df_copy = df.copy()

    # Calculate short Bollinger Bands
    short_middle = df_copy[column].rolling(window=short_length).mean()
    short_std = df_copy[column].rolling(window=short_length).std()
    short_upper = short_middle + short_std * short_stddev
    short_lower = short_middle - short_std * short_stddev

    # Calculate long Bollinger Bands
    long_middle = df_copy[column].rolling(window=long_length).mean()
    long_std = df_copy[column].rolling(window=long_length).std()
    long_upper = long_middle + long_std * long_stddev
    long_lower = long_middle - long_std * long_stddev

    # Calculate BBTrend
    bbtrend = (
        (np.abs(short_lower - long_lower) - np.abs(short_upper - long_upper))
        / short_middle
        * 100
    )
    bbtrend = bbtrend

    # Select and calculate the moving average
    bbtrend_df = df.assign(bbtrend=bbtrend)

    if ma_type == "SMA":
        ma = bbtrend_df["bbtrend"].rolling(window=ma_length).mean()
    elif ma_type == "EMA":
        ma = bbtrend_df["bbtrend"].ewm(span=ma_length, adjust=False).mean()
    elif ma_type == "LSMA":
        # Least Squares Moving Average
        ma_values = []
        for i in range(ma_length - 1, len(bbtrend_df)):
            subset = bbtrend_df.iloc[i + 1 - ma_length : i + 1]
            x = np.arange(len(subset))
            y = subset["bbtrend"].values
            slope, intercept = np.polyfit(x, y, 1)
            ma_values.append(intercept + slope * (ma_length - 1))
        ma = pd.Series(ma_values, index=bbtrend_df.index[ma_length - 1 :])
    elif ma_type == "HMA":
        # Hull Moving Average
        half_length = int(ma_length / 2)
        sqrt_length = int(np.sqrt(ma_length))

        wma_half = (
            bbtrend_df["bbtrend"]
            .rolling(window=half_length, min_periods=1)
            .apply(
                lambda x: np.sum(x * np.arange(1, len(x) + 1))
                / np.sum(np.arange(1, len(x) + 1)),
                raw=True,
            )
        )

        wma_full = (
            bbtrend_df["bbtrend"]
            .rolling(window=ma_length, min_periods=1)
            .apply(
                lambda x: np.sum(x * np.arange(1, len(x) + 1))
                / np.sum(np.arange(1, len(x) + 1)),
                raw=True,
            )
        )

        h = 2 * wma_half - wma_full

        ma = pd.Series(index=bbtrend_df.index)
        ma.iloc[: sqrt_length - 1] = np.nan

        for i in range(sqrt_length - 1, len(bbtrend_df)):
            x = h.iloc[i - sqrt_length + 1 : i + 1].values
            weights = np.arange(1, sqrt_length + 1)
            ma.iloc[i] = np.sum(x * weights) / np.sum(weights)
    elif ma_type == "WMA":
        # Weighted Moving Average
        ma = (
            bbtrend_df["bbtrend"]
            .rolling(window=ma_length)
            .apply(
                lambda x: np.sum(x * np.arange(1, len(x) + 1))
                / np.sum(np.arange(1, len(x) + 1)),
                raw=True,
            )
        )
    else:
        raise ValueError("Unsupported moving average type")

    # Returning as DataFrame
    result = df.copy()
    result["bbtrend"] = bbtrend
    result["bbtrend_ma"] = ma

    return result[["bbtrend", "bbtrend_ma"]]


bollinger_trend_fast_with_ma.__doc__ = """
Name:
    Bollinger Trend Indicator with Selectable Moving Average

Description:
    This function calculates a more responsive Bollinger Trend (BBTrend) and applies a
    selected moving average to the BBTrend.

More info:
    https://www.tradingview.com/script/UtMK7hNw-Bollinger-Trend/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which BBTrend is to be calculated. Default is 'close'.
    - short_length (int): The period for the short Bollinger Bands. Default is 10.
    - long_length (int): The period for the long Bollinger Bands. Default is 50.
    - short_stddev (float): The standard deviation multiplier for the short Bollinger Bands. Default is 1.0.
    - long_stddev (float): The standard deviation multiplier for the long Bollinger Bands. Default is 2.0.
    - ma_type (str): The type of moving average to use ('SMA', 'EMA', 'LSMA', 'HMA', 'WMA'). Default is 'SMA'.
    - ma_length (int): The period for the moving average. Default is 14.

Call with:
    result = bta.bollinger_trend_fast_with_ma(df, 'close', 10, 50, 1.0, 2.0, 'SMA', 14)
    df['bollinger_trend_fast'] = result['bbtrend']
    df['bollinger_trend_fast_ma'] = result['bbtrend_ma']

Returns:
    pd.DataFrame: DataFrame with 'bbtrend' and 'bbtrend_ma' columns.
"""


def test():
    """
    Test function for the bollinger_trend_fast_with_ma indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the bollinger_trend_fast_with_ma indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(bollinger_trend_fast_with_ma)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
