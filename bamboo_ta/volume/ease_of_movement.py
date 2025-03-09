# -*- coding: utf-8 -*-
# ease_of_movement.py
import numpy as np
import pandas as pd


def ease_of_movement(
    df: pd.DataFrame, eom_length: int = 14, seom_length: int = 14, fillna: bool = False
) -> pd.DataFrame:
    """Ease of Movement"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate the Ease of Movement (EoM) values
    emv = (
        (df_copy["high"].diff(1) + df_copy["low"].diff(1))
        * (df_copy["high"] - df_copy["low"])
    ) / (2 * df_copy["volume"])
    emv *= 100000000
    if fillna:
        emv = emv.fillna(0)

    df_copy["eom"] = emv / 100000  # No rounding per your preference

    # Calculate the Signal Ease of Movement (SMA of EoM)
    min_periods = 0 if fillna else seom_length
    sma_emv = df_copy["eom"].rolling(seom_length, min_periods=min_periods).mean()
    if fillna:
        sma_emv = sma_emv.fillna(0)

    df_copy["seom"] = sma_emv

    return df_copy[["eom", "seom"]]


ease_of_movement.__doc__ = """
Name:
    Ease of Movement (EoM, EMV)

Description:
    Ease of Movement (EoM, EMV) and Signal Ease of Movement (SMA of EoM)

    Relates an asset's price change to its volume and is useful for assessing trend strength.
    The SMA of the EoM serves as a signal line for the indicator. Positive values indicate 
    the price is increasing with relative ease, while negative values suggest price is 
    decreasing with relative ease.

More info:
    https://www.investopedia.com/terms/e/easeofmovement.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'volume' columns.
    - eom_length (int): Period for the EoM calculation. Default is 14.
    - seom_length (int): Period for the SMA of EoM calculation. Default is 14.
    - fillna (bool): If True, fill NaN values.

Call with:
    eom_df = bta.ease_of_movement(df, eom_length=14, seom_length=14, fillna=True)
    df['eom'] = eom_df['eom']
    df['seom'] = eom_df['seom']

Returns:
    pd.DataFrame: DataFrame with 'eom' and 'seom' columns.
"""


def test():
    """
    Test function for the ease_of_movement indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the ease_of_movement indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(ease_of_movement)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
