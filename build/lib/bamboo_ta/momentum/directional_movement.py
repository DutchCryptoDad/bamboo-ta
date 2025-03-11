# -*- coding: utf-8 -*-
# directional_movement.py

import pandas as pd
import numpy as np


def directional_movement(df: pd.DataFrame, length: int = 14, mamode: str = "rma", drift: int = 1) -> pd.DataFrame:
    """Directional Movement"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Calculate up and down movements
    up = df_copy["high"] - df_copy["high"].shift(drift)
    dn = df_copy["low"].shift(drift) - df_copy["low"]
    
    # Calculate positive and negative directional movement
    pos_ = ((up > dn) & (up > 0)) * up
    neg_ = ((dn > up) & (dn > 0)) * dn
    
    # Replace zeros with NaN to avoid affecting the moving average
    pos_ = pos_.replace(0, np.nan)
    neg_ = neg_.replace(0, np.nan)
    
    # Calculate the moving average based on the selected mode
    if mamode.lower() == "rma":
        # RMA (Wilder's Smoothing Method)
        alpha = 1 / length
        pos = pos_.fillna(0).ewm(alpha=alpha, adjust=False).mean()
        neg = neg_.fillna(0).ewm(alpha=alpha, adjust=False).mean()
    elif mamode.lower() == "sma":
        pos = pos_.fillna(0).rolling(window=length).mean()
        neg = neg_.fillna(0).rolling(window=length).mean()
    elif mamode.lower() == "ema":
        pos = pos_.fillna(0).ewm(span=length, adjust=False).mean()
        neg = neg_.fillna(0).ewm(span=length, adjust=False).mean()
    else:
        raise ValueError("mamode must be one of 'rma', 'sma', or 'ema'")
    
    # Prepare the result
    df_copy["dmp"] = pos
    df_copy["dmn"] = neg
    
    return df_copy[["dmp", "dmn"]]


directional_movement.__doc__ = \
"""
Name:
    Directional Movement

Description:
    The Directional Movement (DM) indicator was developed by J. Welles Wilder to 
    determine which direction the price of an asset is moving. It compares prior 
    highs and lows to yield two series: +DM (positive directional movement) and 
    -DM (negative directional movement).
    
    +DM measures upward price movement, while -DM measures downward price movement.
    These values are often used as components in calculating the Directional Movement
    Index (DMI) and Average Directional Index (ADX).

More info:
    https://www.investopedia.com/terms/d/directionalmovement.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high' and 'low' columns.
    - length (int): The period for the moving average calculation. Default is 14.
    - mamode (str): Moving average type, one of 'rma', 'sma', or 'ema'. Default is 'rma'.
    - drift (int): The difference period for calculating movements. Default is 1.

Call with:
    result = bta.directional_movement(df)
    df['dmp'] = result['dmp']  # Positive Directional Movement
    df['dmn'] = result['dmn']  # Negative Directional Movement

Returns:
    pd.DataFrame: DataFrame with 'dmp' (+DM) and 'dmn' (-DM) columns.
"""


def test():
    """
    Test function for the directional_movement indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the directional_movement indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(directional_movement)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 