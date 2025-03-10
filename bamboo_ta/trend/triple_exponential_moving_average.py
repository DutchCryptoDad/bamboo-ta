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
    
    # Calculate first EMA
    ema1 = df_copy[column].ewm(span=length, adjust=False).mean()
    
    # Calculate second EMA (EMA of first EMA)
    ema2 = ema1.ewm(span=length, adjust=False).mean()
    
    # Calculate third EMA (EMA of second EMA)
    ema3 = ema2.ewm(span=length, adjust=False).mean()
    
    # Calculate TEMA
    tema = 3 * (ema1 - ema2) + ema3
    
    # Add result to DataFrame
    df_copy["tema"] = tema
    
    return df_copy[["tema"]]


triple_exponential_moving_average.__doc__ = \
"""
Name:
    Triple Exponential Moving Average (TEMA)

Description:
    The Triple Exponential Moving Average (TEMA) was developed by Patrick Mulloy in 1994
    to reduce the lag in traditional moving averages. It uses multiple exponential moving
    averages (EMA) to provide a smoother and more responsive indicator than standard moving averages.
    
    By using a combination of three EMAs, the TEMA filters out short-term price fluctuations
    and reduces the lag associated with traditional moving averages. This makes it potentially
    more responsive to price changes while still maintaining a smooth trend line.
    
    The formula effectively eliminates a significant amount of the lag associated with traditional moving averages.

More info:
    https://www.investopedia.com/terms/t/triple-exponential-moving-average.asp
    https://www.tradingview.com/support/solutions/43000502589/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the TEMA calculation. Default is 10.
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