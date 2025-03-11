# -*- coding: utf-8 -*-
# breakouts.py
import numpy as np
import pandas as pd


def breakouts(df: pd.DataFrame, length: int = 20) -> pd.DataFrame:
    """S/R Breakouts and Retests"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    high = df_copy["high"]
    low = df_copy["low"]
    close = df_copy["close"]

    # Find pivot highs and lows
    pl = low.rolling(window=length * 2 + 1).min()
    ph = high.rolling(window=length * 2 + 1).max()

    # Calculate locations for support and resistance
    s_yLoc = low.shift(length + 1).where(
        low.shift(length + 1) > low.shift(length - 1), low.shift(length - 1)
    )
    r_yLoc = high.shift(length + 1).where(
        high.shift(length + 1) > high.shift(length - 1), high.shift(length + 1)
    )

    # Determine breakouts
    cu = close < s_yLoc.shift(length)
    co = close > r_yLoc.shift(length)

    # Calculate retest conditions for support
    s1 = (high >= s_yLoc.shift(length)) & (close <= pl.shift(length))
    s2 = (
        (high >= s_yLoc.shift(length))
        & (close >= pl.shift(length))
        & (close <= s_yLoc.shift(length))
    )
    s3 = (high >= pl.shift(length)) & (high <= s_yLoc.shift(length))
    s4 = (
        (high >= pl.shift(length))
        & (high <= s_yLoc.shift(length))
        & (close < pl.shift(length))
    )

    # Calculate retest conditions for resistance
    r1 = (low <= r_yLoc.shift(length)) & (close >= ph.shift(length))
    r2 = (
        (low <= r_yLoc.shift(length))
        & (close <= ph.shift(length))
        & (close >= r_yLoc.shift(length))
    )
    r3 = (low <= ph.shift(length)) & (low >= r_yLoc.shift(length))
    r4 = (
        (low <= ph.shift(length))
        & (low >= r_yLoc.shift(length))
        & (close > ph.shift(length))
    )

    # Calculate support and resistance levels
    df_copy["support_level"] = pl.diff().where(pl.diff().notna())
    df_copy["resistance_level"] = ph.diff().where(ph.diff().notna())

    df_copy["support_level"] = df_copy["support_level"].combine_first(
        df_copy["support_level"].shift()
    )
    df_copy["resistance_level"] = df_copy["resistance_level"].combine_first(
        df_copy["resistance_level"].shift()
    )

    # Store breakout and retest signals
    df_copy["support_breakout"] = cu
    df_copy["resistance_breakout"] = co
    df_copy["support_retest"] = (s1 | s2 | s3 | s4).astype(int)
    df_copy["potential_support_retest"] = (s1 | s2 | s3).astype(int)
    df_copy["resistance_retest"] = (r1 | r2 | r3 | r4).astype(int)
    df_copy["potential_resistance_retest"] = (r1 | r2 | r3).astype(int)

    return df_copy[
        [
            "support_level",
            "resistance_level",
            "support_breakout",
            "resistance_breakout",
            "support_retest",
            "potential_support_retest",
            "resistance_retest",
            "potential_resistance_retest",
        ]
    ]


breakouts.__doc__ = """
Name:
    S/R Breakouts and Retests

Description:
    Makes it easy to work with Support and Resistance.
    Find Retests, Breakouts, and the next levels.

More info:
    https://www.tradingview.com/script/iHKi8BGJ-S-R-Breakouts-and-Retests/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - length (int): Lookback period.

Call with:
    breakout = bta.breakouts(df, length=20)
    df['support_level'] = breakout['support_level']
    df['resistance_level'] = breakout['resistance_level']
    df['support_breakout'] = breakout['support_breakout']
    df['resistance_breakout'] = breakout['resistance_breakout']
    df['support_retest'] = breakout['support_retest']
    df['potential_support_retest'] = breakout['potential_support_retest']
    df['resistance_retest'] = breakout['resistance_retest']
    df['potential_resistance_retest'] = breakout['potential_resistance_retest']

Returns:
    pd.DataFrame: DataFrame with event columns populated.
"""


def test():
    """
    Test function for the breakouts indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the breakouts indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(breakouts)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
