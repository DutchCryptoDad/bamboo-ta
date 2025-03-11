# -*- coding: utf-8 -*-
# relative_momentum_index.py
import numpy as np
import pandas as pd


def relative_momentum_index(
    df: pd.DataFrame, length: int = 20, mom: int = 5
) -> pd.DataFrame:
    """Relative Momentum Index (RMI)"""
    df_copy = df.copy()

    # Calculate the momentum up and down changes
    df_copy["maxup"] = (df_copy["close"] - df_copy["close"].shift(mom)).clip(lower=0)
    df_copy["maxdown"] = (df_copy["close"].shift(mom) - df_copy["close"]).clip(lower=0)

    df_copy.fillna(0, inplace=True)

    # Calculate the EMA of increases and decreases
    def exponential_moving_average(
        df: pd.DataFrame, column: str, period: int
    ) -> pd.Series:
        """Calculate Exponential Moving Average (EMA)"""
        # Calculate the multiplier for the EMA
        multiplier = 2 / (period + 1)

        # Calculate initial SMA value
        sma = df[column].rolling(window=period).mean()

        # Initialize EMA with SMA values
        ema = sma.copy()

        # Calculate EMA values
        for i in range(period, len(df)):
            ema[i] = (df[column][i] * multiplier) + (ema[i - 1] * (1 - multiplier))

        return ema

    df_copy["ema_inc"] = exponential_moving_average(
        df_copy, column="maxup", period=length
    )
    df_copy["ema_dec"] = exponential_moving_average(
        df_copy, column="maxdown", period=length
    )

    # Calculate the Relative Momentum Index (RMI)
    df_copy["rmi"] = np.where(
        df_copy["ema_dec"] == 0,
        0,
        100 - 100 / (1 + df_copy["ema_inc"] / df_copy["ema_dec"]),
    )

    return df_copy[["rmi"]]


relative_momentum_index.__doc__ = """
Name:
    Relative Momentum Index (RMI)

Description:
    The Relative Momentum Index (RMI) is an oscillator that applies the RSI formula
    to momentum rather than price.

More info:
    https://www.tradingview.com/script/DdT7MmPa/
    https://github.com/freqtrade/technical/blob/master/technical/indicators/indicators.py#L912

Call with:
    df['rmi'] = bta.relative_momentum_index(df, length=20, mom=5)['rmi']

Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - length (int): Period for the EMA calculation. Default is 20.
    - mom (int): Momentum period. Default is 5.

Returns:
    pd.DataFrame: DataFrame with 'rmi' column.
"""


def test():
    """
    Test function for the relative_momentum_index indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the relative_momentum_index indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(relative_momentum_index)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
