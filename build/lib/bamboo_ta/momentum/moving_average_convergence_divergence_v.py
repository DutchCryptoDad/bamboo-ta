# -*- coding: utf-8 -*-
# moving_average_convergence_divergence_v.py

import pandas as pd

def macd_v(
    df: pd.DataFrame,
    column: str = 'close',
    short_window: int = 12,
    long_window: int = 26,
    atr_window: int = 26,
    signal_window: int = 9,
    fillna: bool = False
) -> pd.DataFrame:
    """MACD-V (Volatility Normalized Momentum)"""
    def ema_calculation(series, span):
        return series.ewm(span=span, adjust=False).mean()

    def wilder_ema(series, period):
        return series.ewm(alpha=1/period, adjust=False).mean()

    # Calculate MACD
    short_ema = ema_calculation(df[column], span=short_window)
    long_ema = ema_calculation(df[column], span=long_window)
    macd = short_ema - long_ema

    # Calculate ATR using Wilder's method
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    true_range = high_low.combine(high_close, max).combine(low_close, max)
    atr = wilder_ema(true_range, period=atr_window)

    # Calculate MACD-V
    macd_v = (macd / atr) * 100

    # Calculate Signal Line
    macd_v_signal = ema_calculation(macd_v, span=signal_window)

    if fillna:
        macd_v = macd_v.fillna(0)
        macd_v_signal = macd_v_signal.fillna(0)

    df_copy = df.copy()
    df_copy['macd_v'] = macd_v
    df_copy['macd_v_signal'] = macd_v_signal

    return df_copy[['macd_v', 'macd_v_signal']]

macd_v.__doc__ = \
"""
Name:
    MACD-V (Volatility Normalized Momentum)

Description:
    The MACD-V is a refined version of the traditional MACD indicator, adjusted for volatility
    using the Average True Range (ATR). This normalization allows for more stable and comparable
    momentum readings across different markets and timeframes.

More info:
    https://www.investopedia.com/terms/m/macd.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the "close" column.
    - column (str): The column on which MACD-V is to be calculated. Default is "close".
    - short_window (int): The short-term period for EMA. Default is 12.
    - long_window (int): The long-term period for EMA. Default is 26.
    - atr_window (int): The period for ATR calculation. Default is 26.
    - signal_window (int): The period for the signal line EMA. Default is 9.
    - fillna (bool): If True, fill nan values. Default is False.

Call with:
    macd_v_result = bta.macd_v(df, 'close', 12, 26, 26, 9)
    df['macd_v'] = macd_v_result['macd_v']
    df['macd_v_signal'] = macd_v_result['macd_v_signal']

Returns:
    pd.DataFrame: DataFrame with 'macd_v' and 'macd_v_signal' columns.
"""

def test():
    """
    Test function for the macd_v indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the macd_v indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(macd_v)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
