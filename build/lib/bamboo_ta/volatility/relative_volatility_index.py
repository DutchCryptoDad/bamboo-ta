# -*- coding: utf-8 -*-
# relative_volatility_index.py

import pandas as pd
import numpy as np


def relative_volatility_index(
    df: pd.DataFrame,
    length: int = 14,
    scalar: float = 100,
    refined: bool = False,
    thirds: bool = False,
    column: str = "close"
) -> pd.DataFrame:
    """Relative Volatility Index (RVI)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["close"]
    if refined or thirds:
        required_columns.extend(["high", "low"])
    
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 14
    scalar = float(scalar) if scalar > 0 else 100
    
    # Define the RVI calculation function
    def _calculate_rvi(source, length, scalar):
        # Calculate standard deviation
        std = source.rolling(window=length).std()
        
        # Calculate price differences
        diff = source.diff()
        
        # Separate positive and negative differences
        pos = pd.Series(np.where(diff > 0, 1, 0), index=source.index)
        neg = pd.Series(np.where(diff <= 0, 1, 0), index=source.index)
        
        # Multiply with standard deviation
        pos_std = pos * std
        neg_std = neg * std
        
        # Calculate exponential moving averages
        pos_avg = pos_std.ewm(span=length, adjust=False).mean()
        neg_avg = neg_std.ewm(span=length, adjust=False).mean()
        
        # Calculate RVI
        rvi = scalar * pos_avg / (pos_avg + neg_avg)
        return rvi
    
    # Calculate RVI based on selected mode
    mode_suffix = ""
    if refined:
        high_rvi = _calculate_rvi(df_copy["high"], length, scalar)
        low_rvi = _calculate_rvi(df_copy["low"], length, scalar)
        df_copy["rvi"] = 0.5 * (high_rvi + low_rvi)
        mode_suffix = "r"
    elif thirds:
        high_rvi = _calculate_rvi(df_copy["high"], length, scalar)
        low_rvi = _calculate_rvi(df_copy["low"], length, scalar)
        close_rvi = _calculate_rvi(df_copy["close"], length, scalar)
        df_copy["rvi"] = (high_rvi + low_rvi + close_rvi) / 3.0
        mode_suffix = "t"
    else:
        df_copy["rvi"] = _calculate_rvi(df_copy[column], length, scalar)
    
    # Add column name suffix if needed
    if mode_suffix:
        df_copy[f"rvi_{mode_suffix}"] = df_copy["rvi"]
        df_copy.drop("rvi", axis=1, inplace=True)
        return df_copy[[f"rvi_{mode_suffix}"]]
    else:
        return df_copy[["rvi"]]


relative_volatility_index.__doc__ = \
"""
Name:
    Relative Volatility Index (RVI)

Description:
    The Relative Volatility Index (RVI) was created by Donald Dorsey in 1993 and 
    revised in 1995. It's a volatility indicator that works similarly to the 
    Relative Strength Index (RSI) but uses standard deviation instead of price changes.
    
    Instead of adding up price changes like RSI based on price direction, the RVI 
    adds up standard deviations based on price direction. This makes it more of a 
    measure of the "quality" of volatility rather than just the amount of volatility.
    
    The indicator has three calculation modes:
    - Standard: Uses only close prices
    - Refined: Uses the average of high and low calculations
    - Thirds: Uses the average of high, low, and close calculations
    
    The RVI oscillates between 0 and 100, with readings above 50 suggesting that 
    upward volatility is stronger, while readings below 50 suggest that downward 
    volatility is stronger.

More info:
    https://www.tradingview.com/wiki/Relative_Volatility_Index_(RVI)

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' column, 
      and 'high' and 'low' columns if using refined or thirds modes.
    - length (int): The period for calculations. Default is 14.
    - scalar (float): A multiplier for scaling the result. Default is 100.
    - refined (bool): Whether to use the 'refined' calculation (average of high and low). Default is False.
    - thirds (bool): Whether to use the 'thirds' calculation (average of high, low, and close). Default is False.
    - column (str): The column to use for calculations if not using refined or thirds modes. Default is 'close'.

Call with:
    # Standard mode
    result = bta.relative_volatility_index(df)
    df['rvi'] = result['rvi']
    
    # Refined mode
    result = bta.relative_volatility_index(df, refined=True)
    df['rvi_r'] = result['rvi_r']
    
    # Thirds mode
    result = bta.relative_volatility_index(df, thirds=True)
    df['rvi_t'] = result['rvi_t']

Returns:
    pd.DataFrame: DataFrame with 'rvi', 'rvi_r', or 'rvi_t' column depending on the mode.
"""


def test():
    """
    Test function for the relative_volatility_index indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the relative_volatility_index indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(relative_volatility_index)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 