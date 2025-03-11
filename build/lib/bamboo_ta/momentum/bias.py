# -*- coding: utf-8 -*-
# bias.py

import pandas as pd


def bias(df: pd.DataFrame, length: int = 26, mamode: str = "sma") -> pd.DataFrame:
    """Bias Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if "close" not in df.columns:
        raise KeyError("DataFrame must contain 'close' column")
    
    # Calculate the moving average based on the selected mode
    if mamode.lower() == "sma":
        ma = df_copy["close"].rolling(window=length).mean()
    elif mamode.lower() == "ema":
        ma = df_copy["close"].ewm(span=length, adjust=False).mean()
    else:
        raise ValueError("mamode must be either 'sma' or 'ema'")
    
    # Calculate BIAS
    df_copy["bias"] = (df_copy["close"] / ma) - 1
    
    return df_copy[["bias"]]


bias.__doc__ = \
"""
Name:
    Bias

Description:
    The Bias indicator measures the percentage deviation of the current price from a
    moving average. It helps identify potential overbought or oversold conditions when
    the price deviates significantly from the moving average.

More info:
    This indicator is popular among Asian traders and is sometimes used to identify
    market extremes.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): The period for the moving average. Default is 26.
    - mamode (str): Moving average type, either 'sma' or 'ema'. Default is 'sma'.

Call with:
    df['bias'] = bta.bias(df)['bias']

Returns:
    pd.DataFrame: DataFrame with 'bias' column.
"""


def test():
    """
    Test function for the bias indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the bias indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(bias)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 