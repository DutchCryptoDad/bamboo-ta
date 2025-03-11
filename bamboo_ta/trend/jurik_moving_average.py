# -*- coding: utf-8 -*-
# jurik_moving_average.py

import pandas as pd
import numpy as np


def jurik_moving_average(df: pd.DataFrame, length: int = 7, phase: float = 0, 
                       column: str = "close") -> pd.DataFrame:
    """Jurik Moving Average (JMA)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Extract the series we'll be working with
    series = df_copy[column]
    
    # Validate parameters
    _length = int(length) if length > 0 else 7
    phase = float(phase)
    
    # Initialize arrays for calculations
    jma = np.zeros_like(series.values)
    volty = np.zeros_like(series.values)
    v_sum = np.zeros_like(series.values)
    
    # Initialize variables
    kv = det0 = det1 = ma2 = 0.0
    jma[0] = ma1 = uBand = lBand = series.iloc[0]
    
    # Static variables
    sum_length = 10
    length = 0.5 * (_length - 1)
    pr = 0.5 if phase < -100 else 2.5 if phase > 100 else 1.5 + phase * 0.01
    length1 = max((np.log(np.sqrt(length)) / np.log(2.0)) + 2.0, 0)
    pow1 = max(length1 - 2.0, 0.5)
    length2 = length1 * np.sqrt(length)
    bet = length2 / (length2 + 1)
    beta = 0.45 * (_length - 1) / (0.45 * (_length - 1) + 2.0)
    
    # Main calculation loop
    for i in range(1, len(series)):
        price = series.iloc[i]
        
        # Price volatility
        del1 = price - uBand
        del2 = price - lBand
        volty[i] = max(abs(del1), abs(del2)) if abs(del1) != abs(del2) else 0
        
        # Relative price volatility factor
        v_sum[i] = v_sum[i - 1] + (volty[i] - volty[max(i - sum_length, 0)]) / sum_length
        avg_volty = np.mean(v_sum[max(i - 65, 0):i + 1])
        d_volty = 0 if avg_volty == 0 else volty[i] / avg_volty
        r_volty = max(1.0, min(np.power(length1, 1 / pow1), d_volty))
        
        # Jurik volatility bands
        pow2 = np.power(r_volty, pow1)
        kv = np.power(bet, np.sqrt(pow2))
        uBand = price if (del1 > 0) else price - (kv * del1)
        lBand = price if (del2 < 0) else price - (kv * del2)
        
        # Jurik Dynamic Factor
        power = np.power(r_volty, pow1)
        alpha = np.power(beta, power)
        
        # 1st stage - preliminary smoothing by adaptive EMA
        ma1 = ((1 - alpha) * price) + (alpha * ma1)
        
        # 2nd stage - one more preliminary smoothing by Kalman filter
        det0 = ((price - ma1) * (1 - beta)) + (beta * det0)
        ma2 = ma1 + pr * det0
        
        # 3rd stage - final smoothing by unique Jurik adaptive filter
        det1 = ((ma2 - jma[i - 1]) * (1 - alpha) * (1 - alpha)) + (alpha * alpha * det1)
        jma[i] = jma[i-1] + det1
    
    # Replace early values with NaN (initial lookback period)
    jma[:_length - 1] = np.nan
    
    # Convert to pandas Series
    jma_series = pd.Series(jma, index=series.index)
    
    # Add result to DataFrame
    df_copy["jma"] = jma_series
    
    return df_copy[["jma"]]


jurik_moving_average.__doc__ = \
"""
Name:
    Jurik Moving Average (JMA)

Description:
    Mark Jurik's Moving Average (JMA) is an advanced adaptive moving average that attempts
    to eliminate market noise to reveal the underlying trend. Developed by Mark Jurik, this
    indicator features extremely low lag, smooth output, and responsiveness to market gaps.
    
    The JMA uses a combination of techniques including dynamic volatility bands, preliminary
    smoothing with an adaptive EMA, additional smoothing with a Kalman filter, and final
    processing with a unique Jurik adaptive filter. This multi-stage process results in a
    highly responsive yet smooth indicator.
    
    The phase parameter allows fine-tuning the behavior between more responsive (positive values)
    or smoother (negative values) output.

More info:
    https://www.tradingview.com/script/nZuBWW9j-Jurik-Moving-Average-JMA/
    https://www.prorealcode.com/prorealtime-indicators/jurik-volatility-bands/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the JMA calculation. Default is 7.
    - phase (float): Controls how heavy/light the average is. Range [-100, 100], 
      where negative values create a smoother average and positive values create a more responsive average.
      Default is 0.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.jurik_moving_average(df)
    df['jma'] = result['jma']

Returns:
    pd.DataFrame: DataFrame with 'jma' column.
"""


def test():
    """
    Test function for the jurik_moving_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the jurik_moving_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(jurik_moving_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 