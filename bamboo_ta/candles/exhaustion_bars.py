# -*- coding: utf-8 -*-
# exhaustion_bars.py
import numpy as np
import pandas as pd


def exhaustion_bars(df, maj_qual=6, maj_len=30, min_qual=5, min_len=5, core_length=4):
    """Leledc Exhaustion Bars"""

    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["open", "high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    bindex_maj, sindex_maj, trend_maj = 0, 0, 0
    bindex_min, sindex_min = 0, 0

    for i in range(len(df_copy)):
        close = df_copy["close"][i]

        if i < 1 or i - core_length < 0:
            df_copy.loc[i, "leledc_major"] = np.nan
            df_copy.loc[i, "leledc_minor"] = 0
            continue

        bindex_maj = np.nan_to_num(bindex_maj)
        sindex_maj = np.nan_to_num(sindex_maj)
        bindex_min = np.nan_to_num(bindex_min)
        sindex_min = np.nan_to_num(sindex_min)

        if close > df_copy["close"][i - core_length]:
            bindex_maj += 1
            bindex_min += 1
        elif close < df_copy["close"][i - core_length]:
            sindex_maj += 1
            sindex_min += 1

        update_major = False
        if (
            bindex_maj > maj_qual
            and close < df_copy["open"][i]
            and df_copy["high"][i] >= df_copy["high"][i - maj_len : i].max()
        ):
            bindex_maj = 0
            trend_maj = 1
            update_major = True
        elif (
            sindex_maj > maj_qual
            and close > df_copy["open"][i]
            and df_copy["low"][i] <= df_copy["low"][i - maj_len : i].min()
        ):
            sindex_maj = 0
            trend_maj = -1
            update_major = True

        if update_major:
            df_copy.loc[i, "leledc_major"] = trend_maj
        else:
            df_copy.loc[i, "leledc_major"] = np.nan if trend_maj == 0 else trend_maj

        if (
            bindex_min > min_qual
            and close < df_copy["open"][i]
            and df_copy["high"][i] >= df_copy["high"][i - min_len : i].max()
        ):
            bindex_min = 0
            df_copy.loc[i, "leledc_minor"] = -1
        elif (
            sindex_min > min_qual
            and close > df_copy["open"][i]
            and df_copy["low"][i] <= df_copy["low"][i - min_len : i].min()
        ):
            sindex_min = 0
            df_copy.loc[i, "leledc_minor"] = 1
        else:
            df_copy.loc[i, "leledc_minor"] = 0

    return df_copy[["leledc_major", "leledc_minor"]]


exhaustion_bars.__doc__ = """
Name:
    Leledc Exhaustion Bars

Description:
    Infamous S/R Reversal Indicator

    Leledc exhaustion bars are a specific type of price action pattern used in
    technical analysis to identify potential reversals in the market trend.
    These bars are characterized by a sharp move in price with an increase in
    volume, often indicating that the current trend is losing momentum and may
    reverse direction soon. Traders use them to pinpoint the end of a trend
    and the beginning of a new one, thereby making more informed trading decisions.

More info:
    https://www.abundancetradinggroup.com/leledc-exhaustion-bar-mt4-indicator/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'open',
        'high', 'low', and 'close' columns.
    - maj_qual (int): Major quality parameter. Default is 6.
    - maj_len (int): Major length parameter. Default is 30.
    - min_qual (int): Minor quality parameter. Default is 5.
    - min_len (int): Minor length parameter. Default is 5.
    - core_length (int): Core length parameter. Default is 4.

Call with:
    exhaustion = bta.exhaustion_bars(df)
    df['leledc_major'] = exhaustion['leledc_major']
    df['leledc_minor'] = exhaustion['leledc_minor']

Returns:
    pd.DataFrame: DataFrame with 'leledc_major' and 'leledc_minor' columns.
"""


def test():
    """
    Test function for the exhaustion_bars indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the exhaustion_bars indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(exhaustion_bars)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
