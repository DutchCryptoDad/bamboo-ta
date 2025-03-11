# -*- coding: utf-8 -*-
# ulcer_index.py
import numpy as np
import pandas as pd


def ulcer_index(
    df: pd.DataFrame, column: str = "close", period: int = 14
) -> pd.DataFrame:
    """Ulcer Index"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")

    # Calculate the maximum value in the period
    df_copy["max_value"] = df_copy[column].rolling(window=period).max()

    # Calculate the percentage drawdown from the maximum value
    df_copy["pct_drawdown"] = (
        100 * (df_copy[column] - df_copy["max_value"]) / df_copy["max_value"]
    )

    # Square the percentage drawdowns
    df_copy["pct_drawdown_squared"] = df_copy["pct_drawdown"] ** 2

    # Calculate the Ulcer Index (square root of the mean of squared drawdowns)
    df_copy["ulcer_index"] = np.sqrt(
        df_copy["pct_drawdown_squared"].rolling(window=period).mean()
    )

    return df_copy[["ulcer_index"]]


ulcer_index.__doc__ = """
Name:
    Ulcer Index

Description:
    The Ulcer Index is a volatility indicator that measures downside risk. Unlike 
    standard deviation, which measures all volatility (both up and down), the 
    Ulcer Index only considers drawdowns from recent highs. This makes it a 
    better measure of investor pain because it focuses on losses.
    
    The indicator was created by Peter Martin and Byron McCann in 1987 and named 
    for the stomach ulcers that investors might get from worrying about downside 
    volatility in their investments.

More info:
    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ulcer_index

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing price data.
    - column (str): The column name to use for the calculation. Default is 'close'.
    - period (int): The lookback period for the calculation. Default is 14.

Call with:
    df['ui'] = bta.ulcer_index(df, 'close', 14)['ulcer_index']

Returns:
    pd.DataFrame: DataFrame with 'ulcer_index' column.
"""


def test():
    """
    Test function for the ulcer_index indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the ulcer_index indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(ulcer_index)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
