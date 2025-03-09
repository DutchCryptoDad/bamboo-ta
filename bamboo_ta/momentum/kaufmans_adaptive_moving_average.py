# -*- coding: utf-8 -*-
# kaufmans_adaptive_moving_average.py

import pandas as pd
import numpy as np

def kaufmans_adaptive_moving_average(
    df: pd.DataFrame,
    close_col: str = 'close',
    window: int = 14,
    pow1: int = 2,
    pow2: int = 30,
    fillna: bool = False,
) -> pd.DataFrame:
    """Kaufman's Adaptive Moving Average (KAMA)"""
    close = df[close_col]
    close_values = close.values
    vol = pd.Series(abs(close - np.roll(close, 1)))

    min_periods = 0 if fillna else window
    er_num = abs(close_values - np.roll(close_values, window))
    er_den = vol.rolling(window, min_periods=min_periods).sum()
    efficiency_ratio = np.divide(
        er_num, er_den, out=np.zeros_like(er_num), where=er_den != 0
    )

    smoothing_constant = (
        (
            efficiency_ratio * (2.0 / (pow1 + 1) - 2.0 / (pow2 + 1.0))
            + 2 / (pow2 + 1.0)
        )
        ** 2.0
    ).values

    kama = np.zeros(smoothing_constant.size)
    len_kama = len(kama)
    first_value = True

    for i in range(len_kama):
        if np.isnan(smoothing_constant[i]):
            kama[i] = np.nan
        elif first_value:
            kama[i] = close_values[i]
            first_value = False
        else:
            kama[i] = kama[i - 1] + smoothing_constant[i] * (
                close_values[i] - kama[i - 1]
            )
    
    kama_series = pd.Series(kama, index=close.index)

    if fillna:
        kama_series = kama_series.fillna(close)

    df_copy = df.copy()
    df_copy['kama'] = kama_series

    return df_copy[['kama']]

kaufmans_adaptive_moving_average.__doc__ = \
"""
Name:
    Kaufman's Adaptive Moving Average (KAMA)

Description:
    Moving average designed to account for market noise or volatility. KAMA
    will closely follow prices when the price swings are relatively small and
    the noise is low. KAMA will adjust when the price swings widen and follow
    prices from a greater distance. This trend-following indicator can be
    used to identify the overall trend, time turning points, and filter price
    movements.

More info:
    https://www.investopedia.com/terms/k/kama.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - close_col (str): Column name for the close prices. Default is 'close'.
    - window (int): Number of periods for the efficiency ratio. Default is 10.
    - pow1 (int): Number of periods for the fastest EMA constant. Default is 2.
    - pow2 (int): Number of periods for the slowest EMA constant. Default is 30.
    - fillna (bool): If True, fill nan values with the close prices. Default is False.

Call with:
    df['kama'] = bta.kaufmans_adaptive_moving_average(df)['kama']

Returns:
    pd.DataFrame: DataFrame with 'kama' column.
"""


def test():
    """
    Test function for the kaufmans_adaptive_moving_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the kaufmans_adaptive_moving_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(kaufmans_adaptive_moving_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
