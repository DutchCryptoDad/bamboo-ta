# -*- coding: utf-8 -*-
# chaikin_money_flow.py
import numpy as np
import pandas as pd


def chaikin_money_flow(
    df: pd.DataFrame, window: int = 20, fillna: bool = False
) -> pd.DataFrame:
    """Chaikin Money Flow"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate the Money Flow Multiplier (MFV)
    mfv = (
        (df_copy["close"] - df_copy["low"]) - (df_copy["high"] - df_copy["close"])
    ) / (df_copy["high"] - df_copy["low"])
    mfv = mfv.fillna(0.0)  # Handling division by zero
    mfv *= df_copy["volume"]

    # Calculate CMF: sum of MFV over window divided by the sum of volume over the same window
    min_periods = 0 if fillna else window
    cmf = (
        mfv.rolling(window, min_periods=min_periods).sum()
        / df_copy["volume"].rolling(window, min_periods=min_periods).sum()
    )

    # Fill NaN values if fillna is True
    if fillna:
        cmf = cmf.fillna(0)

    df_copy["cmf"] = cmf

    return df_copy[["cmf"]]


chaikin_money_flow.__doc__ = """
Name:
    Chaikin Money Flow (CMF)

Description:
    The Chaikin Money Flow measures the amount of Money Flow Volume over a specific period.
    It combines price and volume to form an indicator used to measure buying and selling 
    pressure. A positive value indicates buying pressure, while a negative value suggests 
    selling pressure.

More info:
    https://www.investopedia.com/terms/c/chaikinmoneyflow.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - window (int): Number of periods for the calculation. Default is 20.
    - fillna (bool): If True, fill NaN values with 0.

Call with:
    df['cmf'] = bta.chaikin_money_flow(df, window=20, fillna=True)['cmf']

Returns:
    pd.DataFrame: DataFrame with 'cmf' column.
"""


def test():
    """
    Test function for the chaikin_money_flow indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the chaikin_money_flow indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(chaikin_money_flow)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
