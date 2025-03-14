# -*- coding: utf-8 -*-
# linear_regression_slope.py
import numpy as np
import pandas as pd


def linear_regression_slope(
    df: pd.DataFrame, 
    curve_length: int = 50, 
    slope_length: int = 5, 
    signal_length: int = 13
) -> pd.DataFrame:
    """
    Calculate the Linear Regression Slope indicator with smoothing and signal line.

    This function implements the UCSgears Linear Regression Slope indicator from TradingView.
    It calculates a linear regression curve, then derives the slope as the difference between
    consecutive points, smooths it using EMA, and creates a signal line using SMA.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the 'close' prices.
    - curve_length (int): The lookback period for calculating the linear regression curve. Default is 50.
    - slope_length (int): The period for EMA smoothing of the slope. Default is 5.
    - signal_length (int): The period for SMA calculation of the signal line. Default is 13.

    Returns:
    - pd.DataFrame: DataFrame containing 'lrs', 'slrs', 'alrs', and 'trend' columns.
    """
    # Ensure the 'close' column exists in the DataFrame
    if "close" not in df.columns:
        raise KeyError("The input DataFrame must contain a 'close' column.")
    
    result_df = df.copy()
    
    # Step 1: Calculate Linear Regression Curve (linreg in PineScript)
    # Create a function to calculate the endpoint of linear regression for a window of data
    def linear_regression_endpoint(window):
        x = np.arange(len(window))
        if len(window) < 2:  # Need at least 2 points for regression
            return np.nan
        slope, intercept = np.polyfit(x, window, 1)
        return intercept + slope * (len(window) - 1)  # Last point of the regression line
    
    # Calculate linear regression curve using rolling apply
    result_df['lrc'] = df['close'].rolling(window=curve_length).apply(
        linear_regression_endpoint, raw=True
    )
    
    # Step 2: Calculate Linear Regression Slope (difference between consecutive points)
    result_df['lrs'] = result_df['lrc'].diff()
    
    # Step 3: Calculate Smoothed Linear Regression Slope (EMA of slope)
    result_df['slrs'] = result_df['lrs'].ewm(span=slope_length, adjust=False).mean()
    
    # Step 4: Calculate Signal Linear Regression Slope (SMA of smoothed slope)
    result_df['alrs'] = result_df['slrs'].rolling(window=signal_length).mean()
    
    # Step 5: Calculate trend acceleration/deceleration
    # uacce = lrs > alrs and lrs > 0 
    # dacce = lrs < alrs and lrs < 0
    result_df['uacce'] = (result_df['slrs'] > result_df['alrs']) & (result_df['slrs'] > 0)
    result_df['dacce'] = (result_df['slrs'] < result_df['alrs']) & (result_df['slrs'] < 0)
    
    # Create a trend indicator (1: accelerating up, -1: accelerating down, 0: neutral)
    result_df['trend'] = 0
    result_df.loc[result_df['uacce'], 'trend'] = 1
    result_df.loc[result_df['dacce'], 'trend'] = -1
    
    # Return relevant columns as DataFrame
    return result_df[['lrs', 'slrs', 'alrs', 'trend']]


linear_regression_slope.__doc__ = """
Name:
    Linear Regression Slope

Description:
    This indicator measures the slope of a linear regression curve, providing insights into
    the current trend's strength and momentum. It calculates a linear regression curve, 
    then derives the slope as the difference between consecutive points, smooths it using EMA,
    and creates a signal line using SMA.
    
    The indicator helps identify if a trend is accelerating or decelerating:
    - When the slope is above the signal line and positive, the uptrend is accelerating
    - When the slope is below the signal line and negative, the downtrend is accelerating
    - Other conditions indicate potential trend changes or consolidation

More info:
    This implementation is based on UCSgears' Linear Regression Slope indicator from TradingView.
    Linear regression is a statistical method used to model the relationship between variables
    by fitting a linear equation to observed data. In technical analysis, it helps identify
    the direction and momentum of price trends.

Parameters:
    - df (pd.DataFrame): Input DataFrame containing the 'close' price column.
    - curve_length (int): Number of periods for linear regression calculation. Default is 50.
    - slope_length (int): Period for EMA smoothing of the slope. Default is 5.
    - signal_length (int): Period for SMA calculation of the signal line. Default is 13.

Call with:
    # Calculate with default parameters
    lrs = bta.linear_regression_slope(df)
    df['lrs'] = lrs['lrs']       # Raw Linear Regression Slope
    df['slrs'] = lrs['slrs']     # Smoothed Linear Regression Slope (main indicator)
    df['alrs'] = lrs['alrs']     # Signal line
    df['trend'] = lrs['trend']   # Trend indicator (1: accelerating up, -1: accelerating down, 0: neutral)
    
    # Calculate with custom parameters
    lrs = bta.linear_regression_slope(df, curve_length=100, slope_length=10, signal_length=20)
    
    # Use for trading signals
    df['buy_signal'] = np.where((df['slrs'] > df['alrs']) & (df['slrs'] > 0), 1, 0)
    df['sell_signal'] = np.where((df['slrs'] < df['alrs']) & (df['slrs'] < 0), 1, 0)

Returns:
    pd.DataFrame: A DataFrame containing the following columns:
    - 'lrs': Raw Linear Regression Slope (difference between consecutive linear regression points)
    - 'slrs': Smoothed Linear Regression Slope (EMA of lrs)
    - 'alrs': Average Linear Regression Slope (SMA of slrs, signal line)
    - 'trend': Trend indicator (1: accelerating up, -1: accelerating down, 0: neutral)
    
    The first (curve_length + 1) values will contain NaNs due to the window calculations and differencing.
"""


def test():
    """
    Test function for the linear_regression_slope indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the linear_regression_slope indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(linear_regression_slope)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 