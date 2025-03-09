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


def test():
    """
    Test function for the _check_fillna indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the _check_fillna indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(_check_fillna)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
