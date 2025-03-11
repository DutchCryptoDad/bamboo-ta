# -*- coding: utf-8 -*-
# quarter_to_date.py

import pandas as pd
from datetime import datetime


def quarter_to_date(df: pd.DataFrame) -> pd.DataFrame:
    """Quarter-to-Date Filter"""
    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()
    
    # Get current quarter's first day
    now = datetime.now()
    
    # Determine the start month of the current quarter
    if now.month <= 3:
        quarter_start_month = 1
    elif now.month <= 6:
        quarter_start_month = 4
    elif now.month <= 9:
        quarter_start_month = 7
    else:
        quarter_start_month = 10
    
    # Format the quarter start date
    quarter_start = f"{now.year}-{quarter_start_month:02d}-01"
    
    # Filter DataFrame for dates >= start of quarter
    try:
        in_qtd = df_copy.index >= quarter_start
        if any(in_qtd):
            return df_copy[in_qtd]
        
        # If no data in the current quarter, return the original
        return df_copy
    except Exception as e:
        # Handle potential issues with date filtering
        raise ValueError(f"Error filtering for quarter-to-date: {str(e)}")


quarter_to_date.__doc__ = """
Name:
    Quarter-to-Date Filter

Description:
    Filters a DataFrame to include only data from the beginning of the current quarter
    to the present. This is useful for analyzing quarterly performance or trends.
    
    Quarters are defined as:
    - Q1: January, February, March
    - Q2: April, May, June
    - Q3: July, August, September
    - Q4: October, November, December

More info:
    Quarter-to-date (QTD) is a period starting from the beginning of the current fiscal
    quarter and continuing up to the present day. QTD information is useful for analyzing
    medium-term business trends or comparing performance to previous quarters.

Parameters:
    - df (pandas.DataFrame): Input DataFrame with a DatetimeIndex.

Call with:
    qtd_df = bta.quarter_to_date(df)

Returns:
    pd.DataFrame: DataFrame filtered to contain only data from the beginning of
    the current quarter. If no data exists for the current quarter, returns the
    original DataFrame.
"""


def test():
    """
    Test function for the quarter_to_date function.
    
    This function creates a simple test DataFrame with dates spanning multiple
    quarters and tests the quarter_to_date filtering functionality.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Create a test DataFrame with dates spanning multiple quarters
        import numpy as np
        
        # Create a date range spanning 1 year (4 quarters)
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        
        # Create a test DataFrame
        test_df = pd.DataFrame({
            'close': np.random.rand(len(dates)) * 100,
            'volume': np.random.randint(1000, 100000, len(dates))
        }, index=dates)
        
        # Add the current quarter if test dates don't include it
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        if current_year != 2023:
            # Determine the start of the current quarter
            if current_month <= 3:
                quarter_start = datetime(current_year, 1, 1)
                quarter_end = datetime(current_year, 4, 1) - pd.Timedelta(days=1)
            elif current_month <= 6:
                quarter_start = datetime(current_year, 4, 1)
                quarter_end = datetime(current_year, 7, 1) - pd.Timedelta(days=1)
            elif current_month <= 9:
                quarter_start = datetime(current_year, 7, 1)
                quarter_end = datetime(current_year, 10, 1) - pd.Timedelta(days=1)
            else:
                quarter_start = datetime(current_year, 10, 1)
                quarter_end = datetime(current_year + 1, 1, 1) - pd.Timedelta(days=1)
                
            current_dates = pd.date_range(
                start=quarter_start,
                end=quarter_end,
                freq='D'
            )
            
            current_df = pd.DataFrame({
                'close': np.random.rand(len(current_dates)) * 100,
                'volume': np.random.randint(1000, 100000, len(current_dates))
            }, index=current_dates)
            
            # Concatenate with the test DataFrame
            test_df = pd.concat([test_df, current_df])
        
        # Apply the quarter_to_date function
        qtd_df = quarter_to_date(test_df)
        
        # Print results
        print(f"Original DataFrame shape: {test_df.shape}")
        print(f"Quarter-to-Date DataFrame shape: {qtd_df.shape}")
        
        # Print the quarter date range
        now = datetime.now()
        if now.month <= 3:
            quarter_name = "Q1"
            quarter_start_month = 1
        elif now.month <= 6:
            quarter_name = "Q2"
            quarter_start_month = 4
        elif now.month <= 9:
            quarter_name = "Q3"
            quarter_start_month = 7
        else:
            quarter_name = "Q4"
            quarter_start_month = 10
            
        print(f"\nCurrent Quarter: {quarter_name} (starts {now.year}-{quarter_start_month:02d}-01)")
        
        print("\nFirst few rows of Original DataFrame:")
        print(test_df.head())
        print("\nFirst few rows of Quarter-to-Date DataFrame:")
        print(qtd_df.head())
        
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 