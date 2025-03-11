# -*- coding: utf-8 -*-
# linear_regression_candles.py
import numpy as np
import pandas as pd


def linear_regression_candles(df, linreg_length=11, sma_signal=True, signal_length=11):
    """Linear Regression Candles"""

    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["open", "high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate linear regression coefficients for open, high, low, and close
    df_copy["bopen"] = (
        df_copy["open"]
        .rolling(window=linreg_length)
        .apply(
            lambda x: np.polyfit(np.arange(len(x)), x, 1)[1]
            + np.polyfit(np.arange(len(x)), x, 1)[0] * (len(x) - 1),
            raw=True,
        )
    )

    df_copy["bhigh"] = (
        df_copy["high"]
        .rolling(window=linreg_length)
        .apply(
            lambda x: np.polyfit(np.arange(len(x)), x, 1)[1]
            + np.polyfit(np.arange(len(x)), x, 1)[0] * (len(x) - 1),
            raw=True,
        )
    )

    df_copy["blow"] = (
        df_copy["low"]
        .rolling(window=linreg_length)
        .apply(
            lambda x: np.polyfit(np.arange(len(x)), x, 1)[1]
            + np.polyfit(np.arange(len(x)), x, 1)[0] * (len(x) - 1),
            raw=True,
        )
    )

    df_copy["bclose"] = (
        df_copy["close"]
        .rolling(window=linreg_length)
        .apply(
            lambda x: np.polyfit(np.arange(len(x)), x, 1)[1]
            + np.polyfit(np.arange(len(x)), x, 1)[0] * (len(x) - 1),
            raw=True,
        )
    )

    # Calculate the signal line using SMA or EMA
    if sma_signal:
        df_copy["signal"] = df_copy["bclose"].rolling(window=signal_length).mean()
    else:
        df_copy["signal"] = (
            df_copy["bclose"].ewm(span=signal_length, adjust=False).mean()
        )

    return df_copy[["bopen", "bhigh", "blow", "bclose", "signal"]]


linear_regression_candles.__doc__ = """
Name:
    Linear Regression Candles

Description:
    Linear Regression Candles with Optional Signal Line
    The Linear Regression Candles transform the traditional OHLC bars using a
    linear regression algorithm, providing a smoothed representation of price
    action. The function also provides an optional signal line, which can be
    either an SMA or an EMA of the Linear Regression Candle close. This signal
    line can help to identify trends and potential trading signals.

More info:
    https://www.investopedia.com/terms/l/linearregression.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns:
        'open', 'high', 'low', and 'close'.
    - linreg_length (int, optional): Period for linear regression calculation.
        Default is 11.
    - sma_signal (bool, optional): If True, uses SMA for the signal line. If
        False, uses EMA. Default is True.
    - signal_length (int, optional): Period for the moving average signal line.
        Default is 11.

Call with:
    lr_df = bta.linear_regression_candles(df)
    df['lrc_open'] = lr_df['bopen']
    df['lrc_high'] = lr_df['bhigh']
    df['lrc_low'] = lr_df['blow']
    df['lrc_close'] = lr_df['bclose']
    df['lrc_signal'] = lr_df['signal']

Returns:
    pd.DataFrame: DataFrame with 'bopen', 'bhigh', 'blow', 'bclose' as the
    Linear Regression Candles, and 'signal' as the signal line.
"""


def test():
    """
    Test function for the linear_regression_candles indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the linear_regression_candles indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(linear_regression_candles)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
