# -*- coding: utf-8 -*-
# compounded_annual_growth_rate.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def compounded_annual_growth_rate(
    df: pd.DataFrame,
    column: str = "close"
) -> pd.DataFrame:
    """Compounded Annual Growth Rate Indicator"""
    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Extract the price series
    price = df_copy[column]
    
    # Check if we have enough data
    if len(price) < 2:
        raise ValueError("At least two price points are required to calculate CAGR")
    
    # Get the start and end prices
    start_price = price.iloc[0]
    end_price = price.iloc[-1]
    
    # If either price is zero or negative, CAGR can't be calculated
    if start_price <= 0 or end_price <= 0:
        raise ValueError("Prices must be positive to calculate CAGR")
    
    # Calculate the time difference in years
    if isinstance(df_copy.index, pd.DatetimeIndex):
        # Calculate years difference as a float
        start_date = df_copy.index[0]
        end_date = df_copy.index[-1]
        
        # Calculate time difference in years
        years_diff = (end_date - start_date).days / 365.25
    else:
        # If not a datetime index, assume each row represents one trading day
        # and there are approximately 252 trading days in a year
        years_diff = len(price) / 252
    
    # Ensure we have a meaningful time period
    if years_diff < 0.01:  # Less than ~3.65 days
        raise ValueError("Time period is too short to calculate a meaningful CAGR")
    
    # Calculate CAGR
    cagr = ((end_price / start_price) ** (1 / years_diff)) - 1
    
    # Create a DataFrame with the result
    result = pd.DataFrame({"cagr": [cagr]}, index=[df_copy.index[-1]])
    
    return result


compounded_annual_growth_rate.__doc__ = """
Name:
    Compounded Annual Growth Rate (CAGR)

Description:
    Calculates the Compounded Annual Growth Rate (CAGR) which represents
    the mean annual growth rate of an investment over a specified time period
    longer than one year. It measures the smoothed rate of return as if the
    investment had grown at a steady rate annually.

More info:
    CAGR is a widely used metric to evaluate the performance of investments
    over time. It's particularly useful when comparing investments with
    different time horizons as it standardizes returns to an annual basis.
    
    The formula is:
    CAGR = (Ending Value / Beginning Value)^(1 / Years) - 1

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified
      and have a DatetimeIndex or be organized by trading days.
    - column (str): The column to calculate CAGR on. Default is 'close'.

Call with:
    cagr_result = bta.compounded_annual_growth_rate(df)
    df['cagr'] = cagr_result['cagr'][0]  # Extract single value

Returns:
    pd.DataFrame: DataFrame with a single row containing the CAGR value in
    a column named 'cagr'.
"""


def test():
    """
    Test function for the compounded_annual_growth_rate function.
    
    This function creates a simple test DataFrame with price data over
    multiple years and calculates the CAGR.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Create a test DataFrame spanning 3 years
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2023, 1, 1)
        
        # Create date range (1 data point per month)
        dates = pd.date_range(start=start_date, end=end_date, freq='MS')
        
        # Create example price data with 10% annual growth
        # Starting at 100 and growing to ~133.1 over 3 years (10% annual growth)
        price_growth = 1.10  # 10% annual growth
        prices = [100 * (price_growth ** (i/12)) for i in range(len(dates))]
        
        # Create test DataFrame
        test_df = pd.DataFrame({
            'close': prices
        }, index=dates)
        
        # Calculate CAGR
        cagr_result = compounded_annual_growth_rate(test_df)
        
        # Print results
        print(f"Test data with approximately 10% annual growth over 3 years:")
        print(f"Start price: {test_df['close'].iloc[0]:.2f}")
        print(f"End price: {test_df['close'].iloc[-1]:.2f}")
        print(f"Duration in years: {3.0}")
        print(f"Calculated CAGR: {cagr_result['cagr'].iloc[0]:.4f} ({cagr_result['cagr'].iloc[0]*100:.2f}%)")
        print(f"Expected CAGR: 0.1000 (10.00%)")
        
        # Create another test with negative growth
        prices_down = [100 * (0.9 ** (i/12)) for i in range(len(dates))]
        test_df_down = pd.DataFrame({
            'close': prices_down
        }, index=dates)
        
        # Calculate CAGR for negative growth
        cagr_result_down = compounded_annual_growth_rate(test_df_down)
        
        print(f"\nTest data with approximately 10% annual decline over 3 years:")
        print(f"Start price: {test_df_down['close'].iloc[0]:.2f}")
        print(f"End price: {test_df_down['close'].iloc[-1]:.2f}")
        print(f"Calculated CAGR: {cagr_result_down['cagr'].iloc[0]:.4f} ({cagr_result_down['cagr'].iloc[0]*100:.2f}%)")
        print(f"Expected CAGR: -0.1000 (-10.00%)")
        
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 