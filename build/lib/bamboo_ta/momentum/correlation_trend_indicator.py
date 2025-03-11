# -*- coding: utf-8 -*-
# correlation_trend_indicator.py

import pandas as pd
import numpy as np


def correlation_trend_indicator(df: pd.DataFrame, length: int = 12) -> pd.DataFrame:
    """Correlation Trend Indicator"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required column
    if "close" not in df.columns:
        raise KeyError("DataFrame must contain 'close' column")

    # Calculate the correlation between price and time
    def calculate_correlation(window):
        if len(window) < 2:  # Need at least 2 points for correlation
            return np.nan

        # Convert to numpy arrays to avoid the DataFrame.swapaxes deprecation warning
        x = np.arange(len(window))
        y = np.array(window)

        # Calculate correlation coefficient
        return np.corrcoef(x, y)[0, 1]

    # Apply the correlation calculation
    df_copy["cti"] = (
        df_copy["close"].rolling(window=length).apply(calculate_correlation, raw=True)
    )

    return df_copy[["cti"]]


correlation_trend_indicator.__doc__ = """
Name:
    Correlation Trend Indicator

Description:
    The Correlation Trend Indicator (CTI) is an oscillator created by John Ehler. 
    It measures how closely prices follow a straight line over a given period. 
    The indicator calculates the correlation coefficient between price and time, 
    resulting in values that range from -1 to 1.
    
    A value near 1 indicates prices are following a strong uptrend (positively-sloping line).
    A value near -1 indicates prices are following a strong downtrend (negatively-sloping line).
    Values near 0 indicate no clear trend or sideways movement.

More info:
    https://www.mesasoftware.com/papers/TrendCorrelationIndicator.pdf

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): The period for correlation calculation. Default is 12.

Call with:
    df['cti'] = bta.correlation_trend_indicator(df)['cti']

Returns:
    pd.DataFrame: DataFrame with 'cti' column.
"""


def test():
    """
    Test function for the correlation_trend_indicator indicator.

    This function uses the generic test_indicator function from bamboo_ta.py
    to test the correlation_trend_indicator indicator.

    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator

        # Test the indicator
        test_indicator(correlation_trend_indicator)

    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")


# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
