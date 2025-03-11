# -*- coding: utf-8 -*-
# dynamic_exhaustion_bars.py
import numpy as np
import pandas as pd


def dynamic_exhaustion_bars(df, window=500):
    """Dynamic Leledc Exhaustion Bars"""

    def z_score(series, window):
        """Calculate the z-score of a series."""
        mean = series.rolling(window=window).mean()
        std = series.rolling(window=window).std()
        return (series - mean) / std

    def exhaustion_candles(df, window, zscore_multi):
        """Calculate exhaustion candles."""
        maj_qual = np.where(df["pct_change_zscore_smoothed"] > 1.5, 1, 0)
        min_qual = np.where(df["pct_change_zscore_smoothed"] < -1.5, 1, 0)
        return maj_qual, min_qual

    def exhaustion_lengths(df):
        """Calculate exhaustion lengths."""
        maj_len = df["maj_qual"].rolling(window=5).sum()
        min_len = df["min_qual"].rolling(window=5).sum()
        return maj_len, min_len

    def populate_leledc_major_minor(df, maj_qual, min_qual, maj_len, min_len):
        """Populate leledc major and minor columns."""
        df["leledc_major"] = np.where(maj_qual & (maj_len > 2), 1, 0)
        df["leledc_minor"] = np.where(min_qual & (min_len > 2), 1, 0)
        return df

    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    df_copy["close_pct_change"] = df_copy["close"].pct_change()
    df_copy["pct_change_zscore"] = z_score(df_copy["close_pct_change"], window)
    df_copy["pct_change_zscore_smoothed"] = (
        df_copy["pct_change_zscore"].rolling(window=3).mean()
    )
    df_copy["pct_change_zscore_smoothed"] = df_copy[
        "pct_change_zscore_smoothed"
    ].fillna(1.0)

    zscore = df_copy["pct_change_zscore_smoothed"].to_numpy()
    zscore_multi = np.maximum(np.minimum(5.0 - zscore * 2, 5.0), 1.5)

    maj_qual, min_qual = exhaustion_candles(df_copy, window, zscore_multi)

    df_copy["maj_qual"] = maj_qual
    df_copy["min_qual"] = min_qual

    maj_len, min_len = exhaustion_lengths(df_copy)

    df_copy["maj_len"] = maj_len
    df_copy["min_len"] = min_len

    df_copy = populate_leledc_major_minor(df_copy, maj_qual, min_qual, maj_len, min_len)

    return df_copy[["leledc_major", "leledc_minor"]]


dynamic_exhaustion_bars.__doc__ = """
Name:
    Dynamic Leledc Exhaustion Bars

Description:
    The lookback length and exhaustion bars adjust dynamically to the market conditions.

    This indicator dynamically adjusts the lookback length and the exhaustion 
    bars based on the market's behavior, helping to identify potential reversals
    and trend strength.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - window (int): Lookback window for z-score calculation. Default is 500.

Call with:
    dynamic_exhaustion = bta.dynamic_exhaustion_bars(df)
    df['dynamic_leledc_major'] = dynamic_exhaustion['leledc_major']
    df['dynamic_leledc_minor'] = dynamic_exhaustion['leledc_minor']

Returns:
    pd.DataFrame: DataFrame with 'leledc_major' and 'leledc_minor' columns.
"""

def test():
    """
    Test function for the dynamic_exhaustion_bars indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the dynamic_exhaustion_bars indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the dynamic_exhaustion_bars indicator
        test_indicator(dynamic_exhaustion_bars)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
