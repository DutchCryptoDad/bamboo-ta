# -*- coding: utf-8 -*-
# chande_forecast_oscillator.py

import pandas as pd
import numpy as np


def chande_forecast_oscillator(df: pd.DataFrame, length: int = 9, scalar: float = 100) -> pd.DataFrame:
    """Chande Forecast Oscillator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if "close" not in df.columns:
        raise KeyError("DataFrame must contain 'close' column")
    
    # Calculate linear regression forecast for each window
    df_copy["tsf"] = calculate_linear_regression_forecast(df_copy["close"], length)
    
    # Calculate CFO
    df_copy["cfo"] = scalar * (df_copy["close"] - df_copy["tsf"]) / df_copy["close"]
    
    return df_copy[["cfo"]]


def calculate_linear_regression_forecast(series, length):
    """
    Calculate the Time Series Forecast (linear regression line endpoint) for each window of data.
    """
    result = pd.Series(index=series.index)
    
    for i in range(length - 1, len(series)):
        y = series.iloc[i-(length-1):i+1].values
        x = np.arange(length)
        
        # Calculate slope and intercept
        slope, intercept = np.polyfit(x, y, 1)
        
        # Calculate the forecast (regression line endpoint)
        forecast = intercept + slope * (length - 1)
        
        result.iloc[i] = forecast
    
    return result


chande_forecast_oscillator.__doc__ = \
"""
Name:
    Chande Forecast Oscillator

Description:
    The Chande Forecast Oscillator (CFO) calculates the percentage difference between 
    the actual price and the Time Series Forecast (TSF), which is the endpoint of a 
    linear regression line. It helps identify potential price reversals when the 
    price deviates significantly from its forecasted value.
    
    Positive values indicate that the current price is above the forecasted value, 
    suggesting potential overbought conditions. Negative values indicate that the 
    current price is below the forecasted value, suggesting potential oversold conditions.

More info:
    https://www.fmlabs.com/reference/default.htm?url=ForecastOscillator.htm

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): The period for linear regression calculation. Default is 9.
    - scalar (float): Multiplier for the percentage difference. Default is 100.

Call with:
    df['cfo'] = bta.chande_forecast_oscillator(df)['cfo']

Returns:
    pd.DataFrame: DataFrame with 'cfo' column.
"""


def test():
    """
    Test function for the chande_forecast_oscillator indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the chande_forecast_oscillator indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(chande_forecast_oscillator)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 