# -*- coding: utf-8 -*-
# entropy.py

import pandas as pd
import numpy as np


def entropy(
    df: pd.DataFrame,
    length: int = 10,
    base: float = 2.0,
    column: str = "close"
) -> pd.DataFrame:
    """Entropy Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 10
    base = float(base) if base > 0 else 2.0
    
    # Get the price series
    price = df_copy[column]
    
    # Calculate probability distribution
    p = price / price.rolling(window=length).sum()
    
    # Handle edge cases where p may be 0 or negative
    valid_p = p.copy()
    valid_p[valid_p <= 0] = np.nan  # Replace 0 or negative values with NaN
    
    # Calculate entropy with error handling
    with np.errstate(divide='ignore', invalid='ignore'):
        entropy_vals = (-valid_p * np.log(valid_p) / np.log(base)).rolling(window=length).sum()
    
    # Store result in DataFrame
    df_copy["entropy"] = entropy_vals
    
    return df_copy[["entropy"]]


entropy.__doc__ = \
"""
Name:
    Entropy

Description:
    Entropy, introduced by Claude Shannon in 1948, is a measure of randomness or
    unpredictability in a system. In financial markets, entropy can be used to
    quantify the uncertainty or disorder in price movements.
    
    Higher entropy values indicate more randomness and unpredictability in the price
    series, while lower values suggest more order and predictability. This can help
    traders identify periods of high volatility or uncertainty in the market.
    
    The calculation treats normalized prices as a probability distribution and applies
    the information entropy formula to this distribution over the specified period.

More info:
    https://en.wikipedia.org/wiki/Entropy_(information_theory)
    https://www.investopedia.com/terms/e/entropy.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - length (int): The rolling window period for the entropy calculation. Default is 10.
    - base (float): The logarithmic base to use in the entropy calculation. Default is 2.0.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.entropy(df, length=10, base=2.0)
    df['entropy'] = result['entropy']

Returns:
    pd.DataFrame: DataFrame with 'entropy' column containing the indicator values.
"""


def test():
    """
    Test function for the entropy indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the entropy indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(entropy)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 