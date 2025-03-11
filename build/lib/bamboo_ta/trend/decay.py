# -*- coding: utf-8 -*-
# decay.py

import pandas as pd
import numpy as np


def decay(df: pd.DataFrame, length: int = 5, mode: str = "linear", column: str = "close") -> pd.DataFrame:
    """Decay Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 5
    mode = mode.lower() if isinstance(mode, str) else "linear"
    
    # Get price series
    close = df_copy[column]
    
    # Calculate difference based on mode
    if mode == "exponential" or mode == "exp":
        diff = close.shift(1) - np.exp(-length)
        mode_suffix = "exp"
    else:  # "linear"
        diff = close.shift(1) - (1 / length)
        mode_suffix = "lin"
    
    # Set the first value
    if len(diff) > 0:
        diff.iloc[0] = close.iloc[0] if not pd.isna(close.iloc[0]) else np.nan
    
    # Calculate decay by taking maximum of price, difference, and 0
    decay_values = pd.DataFrame({
        "close": close,
        "diff": diff,
        "zero": pd.Series(0, index=close.index)
    }).max(axis=1)
    
    # Store result
    df_copy[f"decay_{mode_suffix}"] = decay_values
    
    return df_copy[[f"decay_{mode_suffix}"]]


decay.__doc__ = \
"""
Name:
    Decay Indicator

Description:
    The Decay indicator creates a curve that gradually decays moving forward from 
    prior signals, like crosses or other events. This can be useful for trailing 
    signals or creating trailing stops that gradually decrease over time.
    
    The indicator supports two decay modes:
    - Linear: Applies a constant rate of decay based on 1/length
    - Exponential: Applies an exponential decay based on exp(-length)
    
    In both cases, the indicator ensures the decay value never falls below 0 and 
    resets when a new price exceeds the decaying value, creating a sawtooth-like pattern.
    
    This can be particularly useful for:
    - Creating trailing stops that decay over time
    - Generating fading signals after indicator crosses
    - Implementing time-based exits from positions

More info:
    https://tulipindicators.org/decay

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for decay calculation. Higher values result in slower decay. Default is 5.
    - mode (str): Decay mode, either 'linear' or 'exponential' (can also use 'exp'). Default is 'linear'.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    # Linear decay
    result = bta.decay(df)
    df['decay_lin'] = result['decay_lin']
    
    # Exponential decay
    result = bta.decay(df, mode='exp')
    df['decay_exp'] = result['decay_exp']

Returns:
    pd.DataFrame: DataFrame with 'decay_lin' or 'decay_exp' column depending on the mode.
"""


def test():
    """
    Test function for the decay indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the decay indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(decay)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 