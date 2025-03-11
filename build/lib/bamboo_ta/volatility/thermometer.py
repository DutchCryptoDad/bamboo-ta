# -*- coding: utf-8 -*-
# thermometer.py

import pandas as pd
import numpy as np


def thermometer(
    df: pd.DataFrame,
    length: int = 20,
    long_factor: float = 2.0,
    short_factor: float = 0.5,
    drift: int = 1,
    as_int: bool = True
) -> pd.DataFrame:
    """Elders Thermometer (THERMO)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 20
    long_factor = float(long_factor) if long_factor > 0 else 2.0
    short_factor = float(short_factor) if short_factor > 0 else 0.5
    drift = int(drift) if drift > 0 else 1
    
    # Calculate price movements
    thermo_low = np.abs(df_copy["low"].shift(drift) - df_copy["low"])
    thermo_high = np.abs(df_copy["high"] - df_copy["high"].shift(drift))
    
    # Take the larger of the two
    df_copy["thermo"] = np.maximum(thermo_low, thermo_high)
    
    # Calculate EMA of the thermometer
    df_copy["thermo_ma"] = df_copy["thermo"].ewm(span=length, adjust=False).mean()
    
    # Create signals
    df_copy["thermo_long"] = df_copy["thermo"] < (df_copy["thermo_ma"] * long_factor)
    df_copy["thermo_short"] = df_copy["thermo"] > (df_copy["thermo_ma"] * short_factor)
    
    # Convert signals to integers if requested
    if as_int:
        df_copy["thermo_long"] = df_copy["thermo_long"].astype(int)
        df_copy["thermo_short"] = df_copy["thermo_short"].astype(int)
    
    return df_copy[["thermo", "thermo_ma", "thermo_long", "thermo_short"]]


thermometer.__doc__ = \
"""
Name:
    Elders Thermometer (THERMO)

Description:
    Elder's Thermometer is a volatility indicator created by Dr. Alexander Elder. 
    It measures price volatility by comparing the current price range to historical 
    ranges.
    
    The indicator calculates the absolute change in high and low prices between 
    consecutive periods and selects the larger of the two. This value is then 
    compared to its moving average to determine if the market is experiencing 
    normal volatility, high volatility (potentially overbought), or low volatility 
    (potentially oversold).
    
    The indicator generates two signals:
    - Long signal: When the thermometer reading is less than a fraction (long_factor) 
      of its moving average, indicating low volatility.
    - Short signal: When the thermometer reading is greater than a multiple (short_factor) 
      of its moving average, indicating high volatility.

More info:
    https://www.motivewave.com/studies/elders_thermometer.htm
    https://www.tradingview.com/script/HqvTuEMW-Elder-s-Market-Thermometer-LazyBear/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high' and 'low' columns.
    - length (int): The period for the EMA calculation. Default is 20.
    - long_factor (float): The buy factor - thermometer < (thermometer_ma * long_factor). Default is 2.0.
    - short_factor (float): The sell factor - thermometer > (thermometer_ma * short_factor). Default is 0.5.
    - drift (int): The difference period for price changes. Default is 1.
    - as_int (bool): Whether to convert signal outputs to integers (0, 1). Default is True.

Call with:
    result = bta.thermometer(df)
    df['thermo'] = result['thermo']
    df['thermo_ma'] = result['thermo_ma']
    df['thermo_long'] = result['thermo_long']
    df['thermo_short'] = result['thermo_short']

Returns:
    pd.DataFrame: DataFrame with 'thermo', 'thermo_ma', 'thermo_long', 'thermo_short' columns.
"""


def test():
    """
    Test function for the thermometer indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the thermometer indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(thermometer)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 