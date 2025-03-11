# -*- coding: utf-8 -*-
# triple_exponential_moving_average.py

import pandas as pd


def triple_exponential_moving_average(df: pd.DataFrame, length: int = 10, 
                                   column: str = "close") -> pd.DataFrame:
    """Triple Exponential Moving Average (TEMA)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Extract the series we'll be working with
    series = df_copy[column]
    
    # Validate parameters
    length = int(length) if length > 0 else 10
    
    # Calculate EMA1
    ema1 = series.ewm(span=length, adjust=False).mean()
    
    # Calculate EMA2 (EMA of EMA1)
    ema2 = ema1.ewm(span=length, adjust=False).mean()
    
    # Calculate EMA3 (EMA of EMA2)
    ema3 = ema2.ewm(span=length, adjust=False).mean()
    
    # Calculate TEMA: 3 * (EMA1 - EMA2) + EMA3
    tema = 3 * (ema1 - ema2) + ema3
    
    # Add result to DataFrame
    df_copy["tema"] = tema
    
    return df_copy[["tema"]]


triple_exponential_moving_average.__doc__ = \
"""
Name:
    Triple Exponential Moving Average (TEMA)

Description:
    Triple Exponential Moving Average (TEMA) is a technical indicator designed to smooth 
    price data while reducing lag. It's more responsive than traditional moving averages,
    making it useful for identifying trend changes earlier.
    
    TEMA uses multiple EMAs and a specific calculation to reduce the lag typically 
    associated with moving averages. It achieves this by applying a formula that gives 
    more weight to recent price movements while maintaining a reasonable smoothing effect.

More info:
    https://www.investopedia.com/terms/t/triple-exponential-moving-average.asp
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/triple-exponential-moving-average-tema/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the EMA calculations. Default is 10.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.triple_exponential_moving_average(df)
    df['tema'] = result['tema']

Returns:
    pd.DataFrame: DataFrame with 'tema' column.
"""


def test():
    """
    Test function for the triple_exponential_moving_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the triple_exponential_moving_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(triple_exponential_moving_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 