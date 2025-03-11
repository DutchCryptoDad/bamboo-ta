# -*- coding: utf-8 -*-
# percent_price_channel.py
import pandas as pd


def percent_price_channel(
    df: pd.DataFrame, period: int = 20, mult: int = 2
) -> pd.DataFrame:
    """Percent Change Channel (PCC)"""
    df_copy = df.copy()

    # Calculate percent changes
    df_copy["previous_close"] = df_copy["close"].shift()
    df_copy["close_change"] = (
        (df_copy["close"] - df_copy["previous_close"]) / df_copy["previous_close"] * 100
    )
    df_copy["high_change"] = (
        (df_copy["high"] - df_copy["close"]) / df_copy["close"] * 100
    )
    df_copy["low_change"] = (df_copy["low"] - df_copy["close"]) / df_copy["close"] * 100
    df_copy["delta"] = df_copy["high_change"] - df_copy["low_change"]

    # Calculate Zero-lag Exponential Moving Average for midline and range
    # ZEMA = 2 * EMA(1) - EMA(2)
    ema1_mid = df_copy["close_change"].ewm(span=period, adjust=False).mean()
    ema2_mid = ema1_mid.ewm(span=period, adjust=False).mean()
    mid = 2 * ema1_mid - ema2_mid

    ema1_range = df_copy["delta"].ewm(span=period, adjust=False).mean()
    ema2_range = ema1_range.ewm(span=period, adjust=False).mean()
    rangema = 2 * ema1_range - ema2_range

    # Calculate upper and lower bands
    df_copy["pcc_upper"] = mid + rangema * mult
    df_copy["pcc_rangema"] = rangema
    df_copy["pcc_lower"] = mid - rangema * mult

    return df_copy[["pcc_upper", "pcc_rangema", "pcc_lower"]]


percent_price_channel.__doc__ = """
Name:
    Percent Change Channel (PCC)

Description:
    PCC is like KC unless it uses percentage changes in price to set channel distance.
    This channel creates bands based on the percentage change of price rather than
    absolute price movements, making it more adaptive to different price levels.

More info:
    https://www.tradingview.com/script/6wwAWXA1-MA-Streak-Change-Channel/

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the data.
    - period (int): Period for the ZEMA calculation. Default is 20.
    - mult (int): Multiplier for the range. Default is 2.

Call with:
    pcc_result = bta.percent_price_channel(df, period=20, mult=2)
    df['pcc_upper'] = pcc_result['pcc_upper']
    df['pcc_rangema'] = pcc_result['pcc_rangema']
    df['pcc_lower'] = pcc_result['pcc_lower']

Returns:
    pd.DataFrame: DataFrame with 'pcc_upper', 'pcc_rangema', and 'pcc_lower' columns.
"""


def test():
    """
    Test function for the percent_price_channel indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the percent_price_channel indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(percent_price_channel)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
