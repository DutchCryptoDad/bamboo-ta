# -*- coding: utf-8 -*-
# daily_log_return.py
import numpy as np
import pandas as pd


def daily_log_return(
    df: pd.DataFrame, column: str = "close", fillna: bool = False
) -> pd.Series:
    """
    Calculate the Daily Log Return (DLR) of a specified column in a DataFrame.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which the daily log return is to be calculated. Default is "close".
    - fillna (bool): If True, fill NaN values with 0. Default is False.

    Call with:
        df['daily_log_return'] = bta.daily_log_return(df)

    Returns:
    - pd.Series: Series of daily log return values.
    """
    # Copy the DataFrame to avoid modifying the original data
    df_copy = df.copy()

    # Calculate the daily log return
    df_copy["daily_log_return"] = (
        np.log(df_copy[column]).diff() * 100
    )  # Expressing as a percentage

    # Handle NaN values if requested
    if fillna:
        df_copy["daily_log_return"] = df_copy["daily_log_return"].fillna(0)

    return df_copy["daily_log_return"].rename("daily_log_return")


daily_log_return.__doc__ = """
Name:
    Daily Log Return

Description:
    Daily Log Return calculates the logarithmic return between consecutive periods in a price series.
    It's a commonly used measure in financial analysis that represents the continuously compounded
    return and has statistical properties that make it useful for analysis, particularly for
    calculating volatility and performing statistical tests. Log returns are also more normally
    distributed than simple returns.

More info:
    The formula for daily log return is: ln(Pt/Pt-1) * 100, where Pt is the price at time t.
    Alternatively, it can be expressed as: (ln(Pt) - ln(Pt-1)) * 100.
    
    Compared to simple returns, log returns are:
    - Additive over time (making multi-period calculations easier)
    - More symmetrically distributed
    - Better for statistical analysis

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which the daily log return is to be calculated. Default is "close".
    - fillna (bool): If True, fill NaN values with 0. Default is False.

Call with:
    df['log_return'] = bta.daily_log_return(df)
    
    # Using a different price column:
    df['log_return'] = bta.daily_log_return(df, column='adjusted_close')

Returns:
    pd.Series: Series of daily log return values expressed as percentages.
"""


def test():
    """
    Test function for the daily_log_return indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the daily_log_return indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(daily_log_return)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
