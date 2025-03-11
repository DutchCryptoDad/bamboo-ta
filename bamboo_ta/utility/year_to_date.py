# -*- coding: utf-8 -*-
# year_to_date.py

import pandas as pd
from datetime import datetime


def year_to_date(df: pd.DataFrame) -> pd.DataFrame:
    """Year-to-Date Filter"""
    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()
    
    # Get current year's first day
    start_of_year = datetime.now().strftime("%Y-01-01")
    
    # Filter DataFrame for dates >= start of year
    try:
        in_ytd = df_copy.index >= start_of_year
        if any(in_ytd):
            return df_copy[in_ytd]
        
        # If no data in the current year, return the original
        return df_copy
    except Exception as e:
        # Handle potential issues with date filtering
        raise ValueError(f"Error filtering for year-to-date: {str(e)}")


year_to_date.__doc__ = """
Name:
    Year-to-Date Filter

Description:
    Filters a DataFrame to include only data from the beginning of the current year
    to the present. This is useful for analyzing performance or trends within the
    current calendar year.

More info:
    Year-to-date (YTD) is a period starting from the beginning of the current calendar
    year and continuing up to the present day. YTD information is useful for analyzing
    business trends over time or comparing performance to previous years.

Parameters:
    - df (pandas.DataFrame): Input DataFrame with a DatetimeIndex.

Call with:
    ytd_df = bta.year_to_date(df)

Returns:
    pd.DataFrame: DataFrame filtered to contain only data from the beginning of
    the current year. If no data exists for the current year, returns the
    original DataFrame.
"""


def test():
    """
    Test function for the year_to_date function.
    
    This function creates a simple test DataFrame with dates spanning multiple
    years and tests the year_to_date filtering functionality.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Create a test DataFrame with dates spanning multiple years
        import numpy as np
        
        # Create a date range spanning 3 years
        dates = pd.date_range(start='2021-01-01', end='2023-12-31', freq='MS')
        
        # Create a test DataFrame
        test_df = pd.DataFrame({
            'close': np.random.rand(len(dates)) * 100,
            'volume': np.random.randint(1000, 100000, len(dates))
        }, index=dates)
        
        # Add the current year if it's not in the range
        current_year = datetime.now().year
        if current_year > 2023:
            # Add some dates for the current year
            current_dates = pd.date_range(
                start=f'{current_year}-01-01',
                end=f'{current_year}-12-31',
                freq='MS'
            )
            current_df = pd.DataFrame({
                'close': np.random.rand(len(current_dates)) * 100,
                'volume': np.random.randint(1000, 100000, len(current_dates))
            }, index=current_dates)
            
            # Concatenate with the test DataFrame
            test_df = pd.concat([test_df, current_df])
        
        # Apply the year_to_date function
        ytd_df = year_to_date(test_df)
        
        # Print results
        print(f"Original DataFrame shape: {test_df.shape}")
        print(f"Year-to-Date DataFrame shape: {ytd_df.shape}")
        print("\nFirst few rows of Original DataFrame:")
        print(test_df.head())
        print("\nFirst few rows of Year-to-Date DataFrame:")
        print(ytd_df.head())
        
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 