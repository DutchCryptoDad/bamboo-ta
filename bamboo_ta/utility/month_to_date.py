# -*- coding: utf-8 -*-
# month_to_date.py

import pandas as pd
from datetime import datetime


def month_to_date(df: pd.DataFrame) -> pd.DataFrame:
    """Month-to-Date Filter"""
    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()
    
    # Get current month's first day
    start_of_month = datetime.now().strftime("%Y-%m-01")
    
    # Filter DataFrame for dates >= start of month
    try:
        in_mtd = df_copy.index >= start_of_month
        if any(in_mtd):
            return df_copy[in_mtd]
        
        # If no data in the current month, return the original
        return df_copy
    except Exception as e:
        # Handle potential issues with date filtering
        raise ValueError(f"Error filtering for month-to-date: {str(e)}")


month_to_date.__doc__ = """
Name:
    Month-to-Date Filter

Description:
    Filters a DataFrame to include only data from the beginning of the current month
    to the present. This is useful for analyzing performance or trends within the
    current month.

More info:
    Month-to-date (MTD) is a period starting from the beginning of the current calendar
    month and continuing up to the present day. MTD information is useful for analyzing
    short-term business trends or comparing performance to previous months.

Parameters:
    - df (pandas.DataFrame): Input DataFrame with a DatetimeIndex.

Call with:
    mtd_df = bta.month_to_date(df)

Returns:
    pd.DataFrame: DataFrame filtered to contain only data from the beginning of
    the current month. If no data exists for the current month, returns the
    original DataFrame.
"""


def test():
    """
    Test function for the month_to_date function.
    
    This function creates a simple test DataFrame with dates spanning multiple
    months and tests the month_to_date filtering functionality.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Create a test DataFrame with dates spanning multiple months
        import numpy as np
        
        # Create a date range spanning 12 months
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        
        # Create a test DataFrame
        test_df = pd.DataFrame({
            'close': np.random.rand(len(dates)) * 100,
            'volume': np.random.randint(1000, 100000, len(dates))
        }, index=dates)
        
        # Add the current month if test dates don't include it
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        if current_year != 2023 or (current_year == 2023 and current_month > 12):
            # Generate dates for the current month
            current_month_start = datetime(current_year, current_month, 1)
            if current_month == 12:
                next_month_start = datetime(current_year + 1, 1, 1)
            else:
                next_month_start = datetime(current_year, current_month + 1, 1)
                
            current_dates = pd.date_range(
                start=current_month_start,
                end=next_month_start - pd.Timedelta(days=1),
                freq='D'
            )
            
            current_df = pd.DataFrame({
                'close': np.random.rand(len(current_dates)) * 100,
                'volume': np.random.randint(1000, 100000, len(current_dates))
            }, index=current_dates)
            
            # Concatenate with the test DataFrame
            test_df = pd.concat([test_df, current_df])
        
        # Apply the month_to_date function
        mtd_df = month_to_date(test_df)
        
        # Print results
        print(f"Original DataFrame shape: {test_df.shape}")
        print(f"Month-to-Date DataFrame shape: {mtd_df.shape}")
        print("\nFirst few rows of Original DataFrame:")
        print(test_df.head())
        print("\nFirst few rows of Month-to-Date DataFrame:")
        print(mtd_df.head())
        
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 