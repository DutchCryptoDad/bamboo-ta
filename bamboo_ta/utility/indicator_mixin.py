# -*- coding: utf-8 -*-
# indicator_mixin.py
import numpy as np
import pandas as pd


class IndicatorMixin:
    """Utility mixin class for indicator calculations."""

    _fillna = False

    def _check_fillna(self, series: pd.Series, value: int = 0) -> pd.Series:
        """
        Check if the fillna flag is True and handle NaN values accordingly.

        Parameters:
        - series (pd.Series): Calculated indicator series.
        - value (int): Value to fill gaps; if -1, fill values using 'backfill' mode.

        Returns:
        - pd.Series: Series with NaN values handled.
        """
        if self._fillna:
            series_output = series.copy(deep=False)
            series_output = series_output.replace([np.inf, -np.inf], np.nan)
            if isinstance(value, int) and value == -1:
                series = series_output.ffill().bfill()
            else:
                series = series_output.ffill().fillna(value)
        return series

    @staticmethod
    def _true_range(
        high: pd.Series, low: pd.Series, prev_close: pd.Series
    ) -> pd.Series:
        """
        Calculate the true range.

        Parameters:
        - high (pd.Series): High price series.
        - low (pd.Series): Low price series.
        - prev_close (pd.Series): Previous close price series.

        Returns:
        - pd.Series: True range series.
        """
        tr1 = high - low
        tr2 = (high - prev_close).abs()
        tr3 = (low - prev_close).abs()
        true_range = pd.DataFrame(data={"tr1": tr1, "tr2": tr2, "tr3": tr3}).max(axis=1)
        return true_range


# Create a test wrapper function that instantiates IndicatorMixin
def indicator_mixin_test(df: pd.DataFrame) -> pd.DataFrame:
    """Test wrapper for IndicatorMixin"""
    # Create an instance of IndicatorMixin
    mixin = IndicatorMixin()

    # Test _check_fillna
    fillna_result = mixin._check_fillna(df["close"])

    # Test _true_range
    prev_close = df["close"].shift(1)
    tr_result = mixin._true_range(df["high"], df["low"], prev_close)

    # Return results as DataFrame
    result_df = pd.DataFrame({"fillna_result": fillna_result, "true_range": tr_result})

    return result_df


# Add the standard documentation
indicator_mixin_test.__doc__ = """
Name:
    Indicator Mixin

Description:
    A utility mixin class that provides common methods for technical indicators.
    This class includes methods for handling NaN values in indicator series and
    calculating true range, which are commonly used across many technical indicators.
    
    The class is designed to be mixed into other indicator classes to provide
    consistent behavior for common operations.

More info:
    The IndicatorMixin class is part of the utility module in bamboo-ta and provides
    a standardized way to handle common tasks in technical analysis calculations.
    
    The _check_fillna method handles missing values in a consistent way, while the
    _true_range method implements the standard True Range calculation used in many
    volatility indicators like ATR.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at minimum the 'close'
      column for _check_fillna testing, and 'high', 'low', and 'close' columns for
      _true_range testing.

Call with:
    # This is a utility class typically used as a mixin, not called directly
    # Example of how a class would use it:
    class MyIndicator(IndicatorMixin):
        def __init__(self, fillna=False):
            self._fillna = fillna
        
        def calculate(self, df):
            result = some_calculation(df)
            return self._check_fillna(result)

Returns:
    pd.DataFrame: For testing purposes, returns a DataFrame with 'fillna_result' and
                 'true_range' columns demonstrating the mixin's functionality.
"""


def test():
    """
    Test function for the indicator_mixin utility.

    This function uses the generic test_indicator function from bamboo_ta.py
    to test the IndicatorMixin class functionality through a wrapper function.

    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator

        # Test the indicator using the wrapper function
        test_indicator(indicator_mixin_test)

    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")


# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
