# -*- coding: utf-8 -*-
# percentage_volume_oscillator.py

import pandas as pd


def percentage_volume_oscillator(
    df: pd.DataFrame,
    volume_col: str = "volume",
    window_slow: int = 26,
    window_fast: int = 12,
    window_sign: int = 9,
    fillna: bool = False,
) -> pd.DataFrame:
    """Percentage Volume Oscillator (PVO)"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required column
    if volume_col not in df.columns:
        raise KeyError(f"DataFrame must contain '{volume_col}' column")

    volume = df_copy[volume_col]

    # Calculate EMA
    emafast = volume.ewm(span=window_fast, adjust=False).mean()
    emaslow = volume.ewm(span=window_slow, adjust=False).mean()
    pvo = ((emafast - emaslow) / emaslow) * 100

    pvo_signal = pvo.ewm(span=window_sign, adjust=False).mean()
    pvo_hist = pvo - pvo_signal

    if fillna:
        pvo = pvo.fillna(0)
        pvo_signal = pvo_signal.fillna(0)
        pvo_hist = pvo_hist.fillna(0)

    df_copy["pvo"] = pvo
    df_copy["pvo_signal"] = pvo_signal
    df_copy["pvo_hist"] = pvo_hist

    return df_copy[["pvo", "pvo_signal", "pvo_hist"]]


percentage_volume_oscillator.__doc__ = """
Name:
    Percentage Volume Oscillator (PVO)

Description:
    The Percentage Volume Oscillator (PVO) is a technical indicator that shows the relationship
    between two moving averages of a security's volume. It is calculated by subtracting a slow
    exponential moving average (EMA) from a fast EMA and then dividing the result by the slow EMA.

More info:
    https://www.investopedia.com/terms/p/pvo.asp
    https://www.tradingview.com/script/DdT7MmPa/

Call with:
    pvo = bta.percentage_volume_oscillator(df)
    df['pvo'] = pvo['pvo']
    df['pvo_signal'] = pvo['pvo_signal']
    df['pvo_hist'] = pvo['pvo_hist']

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the volume column.
    - volume_col (str): Name of the column containing volume data. Default is 'volume'.
    - window_slow (int): n period long-term. Default is 26.
    - window_fast (int): n period short-term. Default is 12.
    - window_sign (int): n period to signal. Default is 9.
    - fillna (bool): if True, fill nan values. Default is False.


Returns:
    pd.DataFrame: DataFrame with columns ['pvo', 'pvo_signal', 'pvo_hist'].
"""


def test():
    """
    Test function for the percentage_volume_oscillator indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the percentage_volume_oscillator indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(percentage_volume_oscillator)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
