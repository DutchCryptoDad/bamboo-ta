# -*- coding: utf-8 -*-
# accumulation_on_balance_volume.py

import pandas as pd
import numpy as np


def accumulation_on_balance_volume(
    df: pd.DataFrame,
    fast_length: int = 4,
    slow_length: int = 12,
    max_lookback: int = 2,
    min_lookback: int = 2,
    ma_type: str = "EMA",
    run_length: int = 2,
) -> pd.DataFrame:
    """Accumulation On Balance Volume (AOBV)"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Validate parameters
    fast_length = int(fast_length) if fast_length > 0 else 4
    slow_length = int(slow_length) if slow_length > 0 else 12
    max_lookback = int(max_lookback) if max_lookback > 0 else 2
    min_lookback = int(min_lookback) if min_lookback > 0 else 2
    run_length = int(run_length) if run_length > 0 else 2

    # Ensure fast_length < slow_length
    if slow_length < fast_length:
        fast_length, slow_length = slow_length, fast_length

    # Calculate OBV
    df_copy["change"] = df_copy["close"].diff()
    df_copy["obv"] = np.where(
        df_copy["change"] > 0,
        df_copy["volume"],
        np.where(df_copy["change"] < 0, -df_copy["volume"], 0),
    )
    df_copy["obv"] = df_copy["obv"].cumsum()

    # Calculate fast and slow MAs of OBV
    if ma_type.upper() == "EMA":
        df_copy["obv_fast"] = df_copy["obv"].ewm(span=fast_length, adjust=False).mean()
        df_copy["obv_slow"] = df_copy["obv"].ewm(span=slow_length, adjust=False).mean()
    elif ma_type.upper() == "SMA":
        df_copy["obv_fast"] = df_copy["obv"].rolling(window=fast_length).mean()
        df_copy["obv_slow"] = df_copy["obv"].rolling(window=slow_length).mean()
    else:
        raise ValueError(f"Invalid ma_type: {ma_type}. Use 'EMA' or 'SMA'.")

    # Calculate min and max OBV over lookback periods
    df_copy["obv_min"] = df_copy["obv"].rolling(window=min_lookback).min()
    df_copy["obv_max"] = df_copy["obv"].rolling(window=max_lookback).max()

    # Determine long and short runs
    df_copy["obv_long_run"] = 0
    df_copy["obv_short_run"] = 0

    # Calculate runs
    for i in range(run_length, len(df_copy)):
        # Check for long run
        is_long_run = True
        for j in range(run_length):
            if df_copy["obv_fast"].iloc[i - j] <= df_copy["obv_slow"].iloc[i - j]:
                is_long_run = False
                break
        # Use .loc instead of chained indexing to avoid SettingWithCopyWarning and FutureWarning
        df_copy.loc[i, "obv_long_run"] = 1 if is_long_run else 0

        # Check for short run
        is_short_run = True
        for j in range(run_length):
            if df_copy["obv_fast"].iloc[i - j] >= df_copy["obv_slow"].iloc[i - j]:
                is_short_run = False
                break
        # Use .loc instead of chained indexing to avoid SettingWithCopyWarning and FutureWarning
        df_copy.loc[i, "obv_short_run"] = 1 if is_short_run else 0

    # Select and return only the relevant columns
    result_columns = [
        "obv",
        "obv_min",
        "obv_max",
        "obv_fast",
        "obv_slow",
        "obv_long_run",
        "obv_short_run",
    ]

    return df_copy[result_columns]


accumulation_on_balance_volume.__doc__ = """
Name:
    Accumulation On Balance Volume (AOBV)

Description:
    The Accumulation On Balance Volume (AOBV) is an enhanced version of the classic
    On Balance Volume (OBV) indicator. It uses multiple moving averages of the OBV 
    to generate trading signals based on the relationship between these averages.
    
    This indicator also incorporates min/max values over specified lookback periods,
    as well as 'run' signals that indicate when the fast MA has been consistently above
    (long run) or below (short run) the slow MA for a specified number of periods.

More info:
    https://www.investopedia.com/terms/o/onbalancevolume.asp
    https://school.stockcharts.com/doku.php?id=technical_indicators:on_balance_volume_obv

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - fast_length (int): The fast period for the MA calculation. Default is 4.
    - slow_length (int): The slow period for the MA calculation. Default is 12.
    - max_lookback (int): The period for the rolling maximum calculation. Default is 2.
    - min_lookback (int): The period for the rolling minimum calculation. Default is 2.
    - ma_type (str): The type of moving average to use ('EMA' or 'SMA'). Default is 'EMA'.
    - run_length (int): The number of consecutive periods the fast MA must be above/below
                        the slow MA to trigger a long/short run signal. Default is 2.

Call with:
    result = bta.accumulation_on_balance_volume(df)
    df['obv'] = result['obv']
    df['obv_fast'] = result['obv_fast']
    df['obv_slow'] = result['obv_slow']
    df['obv_long_run'] = result['obv_long_run']
    df['obv_short_run'] = result['obv_short_run']

Returns:
    pd.DataFrame: DataFrame with columns 'obv', 'obv_min', 'obv_max', 
                 'obv_fast', 'obv_slow', 'obv_long_run', and 'obv_short_run'.
"""


def test():
    """
    Test function for the accumulation_on_balance_volume indicator.

    This function uses the generic test_indicator function from bamboo_ta.py
    to test the accumulation_on_balance_volume indicator.

    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator

        # Test the indicator
        test_indicator(accumulation_on_balance_volume)

    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")


# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
