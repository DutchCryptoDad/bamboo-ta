# -*- coding: utf-8 -*-
# negative_volume_index.py
import numpy as np
import pandas as pd


def negative_volume_index(
    df: pd.DataFrame,
    signal_type: str = "EMA",
    signal_length: int = 255,
    fillna: bool = False,
) -> pd.DataFrame:
    """Negative Volume Index"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate Rate of Change (ROC)
    df_copy["roc"] = df_copy["close"].pct_change() * 100

    # Initialize the NVI starting from the first valid value with float type
    df_copy["nvi"] = 1000.0  # Starting point for NVI, common practice

    # Calculate NVI values only when volume decreases
    for i in range(1, len(df_copy)):
        if df_copy["volume"].iloc[i] < df_copy["volume"].iloc[i - 1]:
            df_copy.loc[df_copy.index[i], "nvi"] = (
                df_copy["nvi"].iloc[i - 1] + df_copy["roc"].iloc[i]
            )
        else:
            df_copy.loc[df_copy.index[i], "nvi"] = df_copy["nvi"].iloc[i - 1]

    # Calculate NVI Signal
    if signal_type == "EMA":
        df_copy["nvi_signal"] = (
            df_copy["nvi"].ewm(span=signal_length, adjust=False).mean()
        )
    elif signal_type == "SMA":
        df_copy["nvi_signal"] = (
            df_copy["nvi"].rolling(window=signal_length, min_periods=1).mean()
        )
    else:
        raise ValueError(f"Invalid signal_type: {signal_type}. Use 'EMA' or 'SMA'.")

    if fillna:
        df_copy["nvi"] = df_copy["nvi"].fillna(0)
        df_copy["nvi_signal"] = df_copy["nvi_signal"].fillna(0)

    return df_copy[["nvi", "nvi_signal"]]


negative_volume_index.__doc__ = """
Name:
    Negative Volume Index (NVI)

Description:
    The Negative Volume Index (NVI) measures price changes on days when trading volume 
    decreases compared to the previous day. Informed traders are thought to be more 
    active on low volume days, hence the NVI accumulates price rate of change only 
    on such days. The indicator can help identify trends led by smart money.

More info:
    https://www.investopedia.com/terms/n/nvi.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - signal_type (str): Type of signal smoothing ('EMA' or 'SMA'). Default is 'EMA'.
    - signal_length (int): Length for the EMA/SMA calculation. Default is 255.
    - fillna (bool): If True, fill NaN values.

Call with:
    nvi_df = bta.negative_volume_index(df, signal_type='EMA', signal_length=255, fillna=True)
    df['nvi'] = nvi_df['nvi']
    df['nvi_signal'] = nvi_df['nvi_signal']

Returns:
    pd.DataFrame: DataFrame with 'nvi' and 'nvi_signal' columns.
"""


def test():
    """
    Test function for the negative_volume_index indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the negative_volume_index indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(negative_volume_index)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
