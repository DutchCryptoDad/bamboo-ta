# -*- coding: utf-8 -*-
# supertrend.py
import numpy as np
import pandas as pd


def supertrend(
    df: pd.DataFrame,
    length: int = 7,
    atr_length: int = None,
    multiplier: float = 3.0,
    atr_mamode: str = "rma"
) -> pd.DataFrame:
    """Supertrend"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Set default atr_length to length if not provided
    if atr_length is None:
        atr_length = length
    
    # Validate parameters
    if length <= 0:
        raise ValueError("length must be a positive integer")
    if atr_length <= 0:
        raise ValueError("atr_length must be a positive integer")
    if multiplier <= 0:
        raise ValueError("multiplier must be a positive number")
    if atr_mamode not in ["sma", "ema", "rma", "wma"]:
        raise ValueError("atr_mamode must be one of: 'sma', 'ema', 'rma', 'wma'")
    
    # Calculate HL2 (midpoint of high and low)
    hl2 = (df_copy["high"] + df_copy["low"]) / 2
    
    # Calculate True Range
    tr1 = df_copy["high"] - df_copy["low"]
    tr2 = np.abs(df_copy["high"] - df_copy["close"].shift(1))
    tr3 = np.abs(df_copy["low"] - df_copy["close"].shift(1))
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # Calculate ATR using the specified moving average method
    if atr_mamode == "sma":
        atr_value = true_range.rolling(window=atr_length).mean()
    elif atr_mamode == "ema":
        atr_value = true_range.ewm(span=atr_length, adjust=False).mean()
    elif atr_mamode == "rma":
        # RMA (Rolling Moving Average) - same as Wilder's smoothing
        alpha = 1.0 / atr_length
        atr_value = true_range.ewm(alpha=alpha, adjust=False).mean()
    elif atr_mamode == "wma":
        # Weighted Moving Average
        weights = np.arange(1, atr_length + 1)
        atr_value = true_range.rolling(window=atr_length).apply(
            lambda x: np.sum(x * weights) / np.sum(weights), raw=True
        )
    
    # Calculate multiplied ATR
    matr = multiplier * atr_value
    
    # Calculate initial upper and lower bands
    upper_band = hl2 + matr
    lower_band = hl2 - matr
    
    # Initialize arrays for the final values
    m = len(df_copy)
    direction = [1] * m  # 1 for uptrend, -1 for downtrend
    trend = [np.nan] * m
    long_values = [np.nan] * m
    short_values = [np.nan] * m
    
    # Calculate Supertrend values
    for i in range(1, m):
        # Determine trend direction
        if df_copy["close"].iloc[i] > upper_band.iloc[i - 1]:
            direction[i] = 1  # Uptrend
        elif df_copy["close"].iloc[i] < lower_band.iloc[i - 1]:
            direction[i] = -1  # Downtrend
        else:
            direction[i] = direction[i - 1]  # Continue previous trend
            
            # Adjust bands to prevent whipsaws
            if direction[i] > 0 and lower_band.iloc[i] < lower_band.iloc[i - 1]:
                lower_band.iloc[i] = lower_band.iloc[i - 1]
            if direction[i] < 0 and upper_band.iloc[i] > upper_band.iloc[i - 1]:
                upper_band.iloc[i] = upper_band.iloc[i - 1]
        
        # Set trend values based on direction
        if direction[i] > 0:
            trend[i] = long_values[i] = lower_band.iloc[i]
        else:
            trend[i] = short_values[i] = upper_band.iloc[i]
    
    # Set initial values to NaN for the length period
    for i in range(min(length, m)):
        direction[i] = np.nan
    
    # Create result DataFrame
    props = f"_{length}_{multiplier}"
    result = pd.DataFrame(index=df_copy.index)
    result[f"supertrend{props}"] = trend
    result[f"supertrend_direction{props}"] = direction
    result[f"supertrend_long{props}"] = long_values
    result[f"supertrend_short{props}"] = short_values
    result[f"supertrend_upper_band{props}"] = upper_band
    result[f"supertrend_lower_band{props}"] = lower_band
    
    return result


supertrend.__doc__ = """
Name:
    Supertrend

Description:
    The Supertrend indicator is a trend-following indicator that uses Average True Range (ATR)
    to calculate dynamic support and resistance levels. It helps identify trend direction and
    potential entry/exit points. The indicator creates upper and lower bands around price action
    and switches between them based on price closes relative to the previous period's bands.

    The Supertrend line acts as:
    - Support during uptrends (when price is above the line)
    - Resistance during downtrends (when price is below the line)
    
    Direction changes occur when:
    - Price closes above the previous upper band (bullish signal)
    - Price closes below the previous lower band (bearish signal)

More info:
https://www.tradingview.com/script/VLWVV7tH-SuperTrend/
    - http://www.freebsensetips.com/blog/detail/7/What-is-supertrend-indicator-its-calculation
    - https://www.investopedia.com/articles/active-trading/121014/using-supertrend-indicator-develop-trading-system.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'high', 'low', 'close'.
    - length (int): The period for HL2 calculation. Default is 7.
    - atr_length (int): The period for ATR calculation. If None, uses length value. Default is None.
    - multiplier (float): Coefficient for upper and lower band distance from HL2. Default is 3.0.
    - atr_mamode (str): Moving average type for ATR calculation. Options: 'sma', 'ema', 'rma', 'wma'. Default is 'rma'.

Call with:
    result = bta.supertrend(df, length=7, multiplier=3.0)
    df['supertrend'] = result['supertrend_7_3.0']
    df['supertrend_direction'] = result['supertrend_direction_7_3.0']
    df['supertrend_long'] = result['supertrend_long_7_3.0']
    df['supertrend_short'] = result['supertrend_short_7_3.0']

Returns:
    pd.DataFrame: DataFrame with multiple columns:
        - 'supertrend_{length}_{multiplier}': Main Supertrend line values
        - 'supertrend_direction_{length}_{multiplier}': Trend direction (1 for up, -1 for down)
        - 'supertrend_long_{length}_{multiplier}': Long trend values (lower band when trending up)
        - 'supertrend_short_{length}_{multiplier}': Short trend values (upper band when trending down)
        - 'supertrend_upper_band_{length}_{multiplier}': Upper band values
        - 'supertrend_lower_band_{length}_{multiplier}': Lower band values
"""


def test():
    """
    Test function for the supertrend indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the supertrend indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(supertrend)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()