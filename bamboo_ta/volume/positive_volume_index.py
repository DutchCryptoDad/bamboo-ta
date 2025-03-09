# -*- coding: utf-8 -*-
# positive_volume_index.py
import numpy as np
import pandas as pd


def positive_volume_index(
    df: pd.DataFrame,
    signal_type: str = "EMA",
    signal_length: int = 255,
    fillna: bool = False,
) -> pd.DataFrame:
    """Positive Volume Index"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate Rate of Change (ROC)
    df_copy["roc"] = df_copy["close"].pct_change() * 100

    # Initialize PVI column with appropriate dtype
    df_copy["pvi"] = 0.0

    # Calculate PVI
    pvi_condition = df_copy["volume"] > df_copy["volume"].shift(1)
    df_copy.loc[pvi_condition, "pvi"] = df_copy["roc"]
    df_copy["pvi"] = df_copy["pvi"].cumsum().shift(1).fillna(0)

    # Calculate PVI Signal
    if signal_type == "EMA":
        df_copy["pvi_signal"] = (
            df_copy["pvi"].ewm(span=signal_length, adjust=False).mean()
        )
    elif signal_type == "SMA":
        df_copy["pvi_signal"] = (
            df_copy["pvi"].rolling(window=signal_length, min_periods=1).mean()
        )
    else:
        raise ValueError(f"Invalid signal_type: {signal_type}. Use 'EMA' or 'SMA'.")

    if fillna:
        df_copy["pvi"] = df_copy["pvi"].fillna(0)
        df_copy["pvi_signal"] = df_copy["pvi_signal"].fillna(0)

    return df_copy[["pvi", "pvi_signal"]]


positive_volume_index.__doc__ = """
Name:
    Positive Volume Index (PVI)

Description:
    The Positive Volume Index (PVI) measures price changes on days when the trading volume 
    increases compared to the previous day. It accumulates the price rate of change on those 
    days, helping to identify trends driven by high-volume activity. The PVI is often used 
    in conjunction with the Negative Volume Index (NVI) to understand different aspects of 
    market behavior.

More info:
    https://school.stockcharts.com/doku.php?id=technical_indicators:positive_volume_index

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - signal_type (str): Type of signal smoothing ('EMA' or 'SMA'). Default is 'EMA'.
    - signal_length (int): Length for the EMA/SMA calculation. Default is 255.
    - fillna (bool): If True, fill nan values.

Call with:
    pvi_df = bta.positive_volume_index(df, signal_type='EMA', signal_length=255, fillna=True)
    df['pvi'] = pvi_df['pvi']
    df['pvi_signal'] = pvi_df['pvi_signal']

Returns:
    pd.DataFrame: DataFrame with 'pvi' and 'pvi_signal' columns.
"""


def test():
    """
    Test function for the positive_volume_index indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the positive_volume_index indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(positive_volume_index)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
