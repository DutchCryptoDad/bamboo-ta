# -*- coding: utf-8 -*-
# first_crossed_below_second.py
import pandas as pd


def first_crossed_below_second(series1: pd.Series, series2: pd.Series) -> pd.Series:
    """
    Check if series1 crosses below series2 in a vectorized manner.

    Parameters:
    - series1 (pd.Series): First input series to check for crossover.
    - series2 (pd.Series): Second input series to compare against.

    Call with:
        df['first_crossed_below_second'] = bta.first_crossed_below_second(series1, series2)

    Returns:
    - pd.Series: Boolean series where True indicates a crossover below.
    """
    # Ensure both series have the same length
    if len(series1) != len(series2):
        raise ValueError("Input series must have the same length")

    # Vectorized check for crossover below
    return (series1 < series2) & (series1.shift(1) >= series2.shift(1))


first_crossed_below_second.__doc__ = """
Name:
    First Crossed Below Second

Description:
    This function checks if the first series crosses below the second series.
    It returns a boolean series where True indicates the exact candle where
    the crossover occurred. This is useful for generating trading signals
    based on indicator crossovers.
    
    The function performs a vectorized comparison, making it efficient for
    large datasets.

More info:
    In technical analysis, crossovers often indicate potential trading signals.
    For example, when a faster moving average crosses below a slower moving average,
    it may indicate a bearish signal.

Parameters:
    - series1 (pd.Series): First input series to check for crossover (e.g., fast moving average).
    - series2 (pd.Series): Second input series to compare against (e.g., slow moving average).

Call with:
    df['cross_down'] = bta.first_crossed_below_second(df['ema5'], df['ema20'])

Returns:
    pd.Series: Boolean series where True indicates a crossover below.
"""


def test():
    """
    Test function for the first_crossed_below_second indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the first_crossed_below_second indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(first_crossed_below_second)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
