# -*- coding: utf-8 -*-
# force_index.py
import numpy as np
import pandas as pd


def force_index(
    df: pd.DataFrame, window: int = 13, fillna: bool = False
) -> pd.DataFrame:
    """Force Index"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate the Force Index values
    fi = (df_copy["close"] - df_copy["close"].shift(1)) * df_copy["volume"]
    fi_ema = fi.ewm(span=window, adjust=False).mean()
    if fillna:
        fi_ema = fi_ema.fillna(0)

    df_copy["fi"] = fi_ema

    return df_copy[["fi"]]


force_index.__doc__ = """
Name:
    Force Index (FI)

Description:
    The Force Index (FI) illustrates how strong the actual buying or selling pressure is.
    It combines price movement and volume to quantify the force behind a price move.
    A rising FI indicates increasing buying pressure, while a falling FI suggests 
    increasing selling pressure.

More info:
    https://www.investopedia.com/terms/f/force-index.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - window (int): Period for calculating the exponential moving average of the Force Index. Default is 13.
    - fillna (bool): If True, fill NaN values.

Call with:
    df['fi'] = bta.force_index(df, window=13, fillna=True)['fi']

Returns:
    pd.DataFrame: DataFrame with 'fi' column.
"""


def test():
    """
    Test function for the force_index indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the force_index indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(force_index)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
