# -*- coding: utf-8 -*-
# on_balance_volume_oscillator.py
import numpy as np
import pandas as pd


def on_balance_volume_oscillator(
    df: pd.DataFrame, length: int = 20, fillna: bool = False
) -> pd.DataFrame:
    """On Balance Volume Oscillator"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate OBV
    df_copy["change"] = df_copy["close"].diff()
    df_copy["obv"] = np.where(
        df_copy["change"] > 0,
        df_copy["volume"],
        np.where(df_copy["change"] < 0, -df_copy["volume"], 0),
    )
    df_copy["obv"] = df_copy["obv"].cumsum()

    # Calculate OBV Oscillator
    df_copy["ema_obv"] = df_copy["obv"].ewm(span=length, adjust=False).mean()
    df_copy["obv_oscillator"] = df_copy["obv"] - df_copy["ema_obv"]

    # Fill NaN values if requested
    if fillna:
        df_copy["obv_oscillator"] = df_copy["obv_oscillator"].fillna(0)

    return df_copy[["obv_oscillator"]]


on_balance_volume_oscillator.__doc__ = """
Name:
    On Balance Volume (OBV) Oscillator

Description:
    The On Balance Volume (OBV) Oscillator measures the difference between the OBV and its 
    Exponential Moving Average (EMA). It helps in identifying trends and confirming price 
    movements. An increasing OBV oscillator indicates buying pressure, while a decreasing 
    one indicates selling pressure. Crossovers of the zero line can be used as potential 
    trading signals.

More info:
    https://www.investopedia.com/terms/o/onbalancevolume.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - length (int): Length for the EMA calculation. Default is 20.
    - fillna (bool): If True, fill nan values with 0.

Call with:
    df['obv_oscillator'] = bta.on_balance_volume_oscillator(df, length=20, fillna=True)['obv_oscillator']

Returns:
    pd.DataFrame: DataFrame with 'obv_oscillator' column.
"""


def test():
    """
    Test function for the on_balance_volume_oscillator indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the on_balance_volume_oscillator indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(on_balance_volume_oscillator)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
