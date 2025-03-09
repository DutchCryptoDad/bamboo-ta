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
        
        # Display the results
        print(f"\n=== {indicator_name.replace('_', ' ').title()} Test Results ===")
        print("\nIndicator Description:")
        if hasattr(indicator_func, '__doc__') and indicator_func.__doc__:
            print(indicator_func.__doc__.strip())
        else:
            print(f"No documentation available for {indicator_name}")
        
        print("\nLast 10 rows of data with indicator values:")
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        
        # Display date, close, and indicator columns
        display_cols = ['date', 'close'] + list(result.columns)
        display_df = df[display_cols].tail(10)
        print(display_df)
        
        # Display some statistics for each indicator column
        print("\nIndicator Statistics:")
        for col in result.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                print(f"\n{col}:")
                print(f"  Min: {df[col].min()}")
                print(f"  Max: {df[col].max()}")
                print(f"  Mean: {df[col].mean()}")
                print(f"  Std Dev: {df[col].std()}")
                
                # If the column contains binary signals (0s and 1s)
                if set(df[col].dropna().unique()).issubset({0, 1}):
                    signal_count = df[col].sum()
                    print(f"  Total signals: {signal_count}")
                    if signal_count > 0:
                        print("\nLast 5 signals:")
                        signals = df[df[col] == 1].tail(5)
                        if not signals.empty:
                            print(signals[['date', 'close', col]])
        
    except FileNotFoundError as e:
        print(f"Error: {e}. Please ensure the data file exists in the data directory.")
        available_files = os.listdir(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"))
        print(f"Available data files: {available_files}")
    except Exception as e:
        print(f"Error during testing: {e}")