# -*- coding: utf-8 -*-
# accumulation_distribution_index.py
import numpy as np
import pandas as pd


def accumulation_distribution_index(
    df: pd.DataFrame, fillna: bool = False
) -> pd.DataFrame:
    """Accumulation/Distribution Index"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate the ADI values
    clv = (
        (df_copy["close"] - df_copy["low"]) - (df_copy["high"] - df_copy["close"])
    ) / (df_copy["high"] - df_copy["low"])
    clv = clv.fillna(0.0)  # Handling division by zero
    adi = clv * df_copy["volume"]
    adi = adi.cumsum()

    if fillna:
        adi = adi.fillna(0)

    df_copy["adi"] = adi

    return df_copy[["adi"]]


accumulation_distribution_index.__doc__ = """
Name:
    Accumulation/Distribution Index (ADI)

Description:
    The ADI acts as a leading indicator of price movements. It is calculated using the
    high, low, close, and volume data. The indicator evaluates the relationship between 
    price and volume, aiming to identify divergences that may precede price movements.

More info:
    https://www.investopedia.com/terms/a/accumulationdistribution.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - fillna (bool): If True, fill NaN values.

Call with:
    df['adi'] = bta.accumulation_distribution_index(df, fillna=True)['adi']

Returns:
    pd.DataFrame: DataFrame with 'adi' column.
"""


def test():
    """
    Test function for the accumulation_distribution_index indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the accumulation_distribution_index indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(accumulation_distribution_index)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
