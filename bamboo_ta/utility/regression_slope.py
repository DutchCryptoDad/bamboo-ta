# -*- coding: utf-8 -*-
# regression_slope.py
import numpy as np
import pandas as pd


def regression_slope(df: pd.DataFrame, lookback_period: int = 20) -> pd.DataFrame:
    """
    Calculate the slope of the linear regression for a given lookback period.

    This function computes the slope of a linear regression line (least squares) fitted to the
    'close' prices over the specified lookback period.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the 'close' prices.
    - lookback_period (int): The lookback period for calculating the regression slope. Default is 20.

    Returns:
    - pd.DataFrame: DataFrame containing the regression slopes in the 'slope' column.
    """
    # Ensure the 'close' column exists in the DataFrame
    if "close" not in df.columns:
        raise KeyError("The input DataFrame must contain a 'close' column.")

    # Extract the 'close' prices as a NumPy array for faster processing
    y_values = df["close"].values

    # Create an array for the x-values (time steps) for the regression
    x_values = np.arange(lookback_period)
    x_mean = x_values.mean()

    # Function to calculate the slope for a given rolling window
    def calculate_slope(window):
        y_mean = window.mean()
        numerator = np.sum((x_values - x_mean) * (window - y_mean))
        denominator = np.sum((x_values - x_mean) ** 2)
        return numerator / denominator

    # Apply the slope calculation to the rolling window on the 'close' prices
    slope_series = (
        df["close"].rolling(window=lookback_period).apply(calculate_slope, raw=True)
    )

    # Create a DataFrame with the slope column and return it
    result_df = pd.DataFrame(index=df.index)
    result_df['slope'] = slope_series

    return result_df


regression_slope.__doc__ = """
Name:
    Regression Slope

Description:
    This function calculates the slope of a linear regression line fitted to price data
    over a specified lookback period. The slope indicates the rate of change of price
    and can be used to identify the strength and direction of a trend.
    
    A positive slope indicates an uptrend, while a negative slope indicates a downtrend.
    The steepness of the slope corresponds to the strength of the trend.

More info:
    Linear regression is a statistical method used to model the relationship between
    a dependent variable (price) and an independent variable (time). In technical analysis,
    the slope of the regression line provides valuable information about trend direction
    and strength.
    
    The calculation uses the least squares method to find the line that minimizes the
    sum of squared distances between the line and the actual price points.

Parameters:
    - df (pd.DataFrame): Input DataFrame containing the 'close' price column.
    - lookback_period (int): Number of periods to use for the regression calculation.
      Default is 20.

Call with:
    # Calculate regression slope with default 20-period lookback
    result = bta.regression_slope(df)
    df['reg_slope'] = result['slope']
    
    # Calculate regression slope with custom lookback
    result = bta.regression_slope(df, lookback_period=50)
    df['reg_slope_50'] = result['slope']
    
    # Use with other indicators
    df['slope_signal'] = np.where(df['reg_slope'] > 0, 1, -1)

Returns:
    pd.DataFrame: A DataFrame containing the regression slope values in the 'slope' column.
    The first (lookback_period - 1) values will be NaN.
"""


def test():
    """
    Test function for the regression_slope indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the regression_slope indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(regression_slope)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
