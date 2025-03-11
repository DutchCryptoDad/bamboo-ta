# -*- coding: utf-8 -*-
# populate_leledc_major_minor.py
import numpy as np
import pandas as pd


def populate_leledc_major_minor(
    df: pd.DataFrame,
    maj_qual: np.ndarray,
    min_qual: np.ndarray,
    maj_len: int,
    min_len: int,
) -> pd.DataFrame:
    """
    Populate Leledc Major and Minor columns.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame.
    - maj_qual (np.ndarray): Array of major quality values.
    - min_qual (np.ndarray): Array of minor quality values.
    - maj_len (int): Major length value.
    - min_len (int): Minor length value.

    Call with:
        leledc_major_minor = bta.populate_leledc_major_minor(df, maj_qual, min_qual, maj_len, min_len)
        df['leledc_major'] = leledc_major_minor['leledc_major']
        df['leledc_minor'] = leledc_major_minor['leledc_minor']

    Returns:
    - pd.DataFrame: DataFrame with 'leledc_major' and 'leledc_minor' columns.
    """
    df_copy = df.copy()
    bindex_maj, sindex_maj, trend_maj = 0, 0, 0
    bindex_min, sindex_min = 0, 0

    df_copy["leledc_major"] = np.nan
    df_copy["leledc_minor"] = 0

    for i in range(1, len(df_copy)):
        close = df_copy["close"][i]
        short_length = i if i < 4 else 4

        if close > df_copy["close"][i - short_length]:
            bindex_maj += 1
            bindex_min += 1
        elif close < df_copy["close"][i - short_length]:
            sindex_maj += 1
            sindex_min += 1

        update_major = False
        if (
            bindex_maj > maj_qual[i]
            and close < df_copy["open"][i]
            and df_copy["high"][i] >= df_copy["high"][i - maj_len : i].max()
        ):
            bindex_maj, trend_maj, update_major = 0, 1, True
        elif (
            sindex_maj > maj_qual[i]
            and close > df_copy["open"][i]
            and df_copy["low"][i] <= df_copy["low"][i - maj_len : i].min()
        ):
            sindex_maj, trend_maj, update_major = 0, -1, True

        df_copy.at[i, "leledc_major"] = (
            trend_maj if update_major else np.nan if trend_maj == 0 else trend_maj
        )

        if (
            bindex_min > min_qual[i]
            and close < df_copy["open"][i]
            and df_copy["high"][i] >= df_copy["high"][i - min_len : i].max()
        ):
            bindex_min = 0
            df_copy.at[i, "leledc_minor"] = -1
        elif (
            sindex_min > min_qual[i]
            and close > df_copy["open"][i]
            and df_copy["low"][i] <= df_copy["low"][i - min_len : i].min()
        ):
            sindex_min = 0
            df_copy.at[i, "leledc_minor"] = 1
        else:
            df_copy.at[i, "leledc_minor"] = 0

    return df_copy[["leledc_major", "leledc_minor"]]


populate_leledc_major_minor.__doc__ = """
Name:
    Populate LELEDC Major and Minor

Description:
    LELEDC (Length and Extreme for Low Exhaustion and Determining Cycle) is an
    indicator system that identifies potential exhaustion points in price action.
    This function calculates both major and minor cycle signals based on quality
    parameters and specific price patterns.
    
    The major cycle identifies significant trend changes while the minor cycle
    identifies smaller retracements and continuations within the larger trend.
    
    LELEDC is particularly useful for identifying potential reversal points and
    for determining market cycles.

More info:
    The algorithm tracks consecutive movements in a specific direction and generates
    signals when price makes an extreme move (new high/low) after a sufficient number
    of consecutive moves in one direction, combined with a reversal candle pattern.
    
    Major signals (1/-1) indicate potential significant trend changes.
    Minor signals (1/-1) indicate smaller retracements or continuation patterns.

Parameters:
    - df (pd.DataFrame): Input DataFrame with OHLC price data.
    - maj_qual (np.ndarray): Array of major quality thresholds for each bar.
    - min_qual (np.ndarray): Array of minor quality thresholds for each bar.
    - maj_len (int): Lookback length for major cycle high/low comparisons.
    - min_len (int): Lookback length for minor cycle high/low comparisons.

Call with:
    # Usually used after calculating quality values and lengths:
    maj_qual, min_qual = bta.exhaustion_candles(df)
    maj_len, min_len = bta.exhaustion_lengths(df)
    
    result = bta.populate_leledc_major_minor(df, maj_qual, min_qual, maj_len, min_len)
    df['leledc_major'] = result['leledc_major']
    df['leledc_minor'] = result['leledc_minor']

Returns:
    pd.DataFrame: DataFrame with two columns:
    - 'leledc_major': Major cycle signals (1, -1, or NaN)
    - 'leledc_minor': Minor cycle signals (1, -1, or 0)
"""


def test():
    """
    Test function for the populate_leledc_major_minor indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the populate_leledc_major_minor indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(populate_leledc_major_minor)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
