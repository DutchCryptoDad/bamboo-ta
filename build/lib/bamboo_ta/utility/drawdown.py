# -*- coding: utf-8 -*-
# drawdown.py

import pandas as pd
import numpy as np


def drawdown(
    df: pd.DataFrame,
    column: str = "close"
) -> pd.DataFrame:
    """Drawdown Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Get the price series
    price = df_copy[column]
    
    # Calculate the running maximum price
    max_price = price.cummax()
    
    # Calculate drawdown in absolute terms
    dd = max_price - price
    
    # Calculate drawdown in percentage terms
    dd_pct = 1 - (price / max_price)
    
    # Calculate drawdown in logarithmic terms (safer approach with error handling)
    with np.errstate(divide='ignore', invalid='ignore'):
        dd_log = np.log(max_price) - np.log(price)
        # Replace infinite values with NaN
        dd_log = dd_log.replace([np.inf, -np.inf], np.nan)
    
    # Store results in DataFrame
    df_copy["drawdown"] = dd
    df_copy["drawdown_pct"] = dd_pct
    df_copy["drawdown_log"] = dd_log
    
    return df_copy[["drawdown", "drawdown_pct", "drawdown_log"]]


drawdown.__doc__ = \
"""
Name:
    Drawdown

Description:
    Drawdown is a peak-to-trough decline during a specific period for an investment,
    trading account, or fund. It measures the magnitude of a decline from a peak to
    a trough in the value of an asset or portfolio.
    
    The drawdown is typically quoted as the percentage between the peak and the
    subsequent trough, but this implementation also provides:
    - Absolute drawdown: The absolute difference between the peak and current price
    - Percentage drawdown: The percentage decline from peak (1 - price/max_price)
    - Logarithmic drawdown: The log difference between peak and current price
    
    Drawdown analysis is important for risk management as it helps assess the
    potential losses and volatility of an investment. Many traders use maximum
    drawdown as a risk metric when evaluating trading strategies.

More info:
    https://www.investopedia.com/terms/d/drawdown.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.drawdown(df)
    df['drawdown'] = result['drawdown']  # Absolute drawdown
    df['drawdown_pct'] = result['drawdown_pct']  # Percentage drawdown
    df['drawdown_log'] = result['drawdown_log']  # Logarithmic drawdown

Returns:
    pd.DataFrame: DataFrame with 'drawdown', 'drawdown_pct', and 'drawdown_log' columns.
"""


def test():
    """
    Test function for the drawdown indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the drawdown indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(drawdown)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 