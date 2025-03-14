# bamboo_ta.py
# -*- coding: utf-8 -*-
# Import the individual bamboo ta libraries
from bamboo_ta.candles import *
from bamboo_ta.cycles import *
from bamboo_ta.momentum import *
from bamboo_ta.performance import *
from bamboo_ta.statistics import *
from bamboo_ta.trend import *
from bamboo_ta.utility import *
from bamboo_ta.volatility import *
from bamboo_ta.volume import *

def test_indicator(indicator_func, timeframe="1d", *args, **kwargs):
    """
    Generic test function for any indicator in the bamboo-ta library.
    
    This function loads test data, applies the specified indicator function,
    and displays the results for visual inspection against values that might
    be visible on TradingView.
    
    Parameters:
        indicator_func (function): The indicator function to test
        timeframe (str): The timeframe of data to use for testing ('1d', '4h', '1h', etc.)
        *args: Additional positional arguments to pass to the indicator function
        **kwargs: Additional keyword arguments to pass to the indicator function
        
    Returns:
        None: Displays the results to the console
    """
    import os
    import pandas as pd
    import inspect
    
    # Load test data
    try:
        # Try to find the data file in the data directory
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                               "data", f"BTC_USDT-{timeframe}.json")
        df = pd.read_json(file_path)
        df.columns = ["date", "open", "high", "low", "close", "volume"]
        df["date"] = pd.to_datetime(df["date"], unit="ms")
        
        # Get the indicator name
        indicator_name = indicator_func.__name__
        
        # Apply the indicator
        result = indicator_func(df, *args, **kwargs)
        
        # Check if result is a DataFrame
        if not isinstance(result, pd.DataFrame):
            print(f"Error: {indicator_name} did not return a DataFrame")
            return
        
        # Add the results to the dataframe
        for col in result.columns:
            df[col] = result[col]
        
        # Display the results header
        print(f"\n=== {indicator_name.replace('_', ' ').title()} Test Results ===")
        
        # Display the indicator description
        print("\nIndicator Description:")
        if hasattr(indicator_func, '__doc__') and indicator_func.__doc__:
            print(indicator_func.__doc__.strip())
        else:
            print(f"No documentation available for {indicator_name}")
        
        # Set display options
        pd.set_option('display.max_columns', None)  # Show all columns
        pd.set_option('display.width', 1000)        # Wide display
        pd.set_option('display.max_rows', None)     # Show all rows in the output
        
        # Display the last 32 rows of the dataframe with all columns
        print(f"\nLast 32 rows of data with {indicator_name} values:")
        print(df.tail(32))
        
    except FileNotFoundError as e:
        print(f"Error: {e}. Please ensure the data file exists in the data directory.")
        available_files = os.listdir(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"))
        print(f"Available data files: {available_files}")
    except Exception as e:
        print(f"Error during testing: {e}")