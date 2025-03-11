# -*- coding: utf-8 -*-
# time_relative_volume_oscillator.py
import numpy as np
import pandas as pd


def time_relative_volume_oscillator(
    df: pd.DataFrame,
    column: str = "close",
    relative_len: int = 6,
    delta_smoothing: int = 9,
    smoothing_line: bool = True,
    show_total_volume: bool = False,
) -> pd.DataFrame:
    """Time Relative Volume Oscillator"""
    df_copy = df.copy()

    # Compute 200-period SMA of volume (used for scaling)
    df_copy["volume_sma_200"] = df["volume"].rolling(200).mean()

    # Calculate Relative Volume using the past `relative_len` bars only (shifted by 1 to exclude the current bar)
    df_copy["total_volume"] = df["volume"].shift(1).rolling(relative_len).sum()
    df_copy["relative_volume"] = df["volume"] / (df_copy["total_volume"] / relative_len)

    # Apply Pine Script's sigmoid-like transformation to relative volume
    df_copy["osc"] = 4 / (1 + np.exp(-2 * df_copy["relative_volume"] + 3)) - 0.18

    # Compute final adjusted relative_plot (multiplied by volume_sma_200, no extra factor)
    df_copy["relative_plot"] = df_copy["osc"] * df_copy["volume_sma_200"]

    # Buy/Sell Volume Calculation (weighted by price position in high-low range)
    high_low_range = df["high"] - df["low"]
    df_copy["relative_buy_volume"] = np.where(
        high_low_range == 0,
        0,
        df_copy["relative_plot"] * (df["close"] - df["low"]) / high_low_range,
    )
    # Compute the sell volume as a positive value (for correct percentage calculations)
    df_copy["relative_sell_volume_pos"] = np.where(
        high_low_range == 0,
        0,
        df_copy["relative_plot"] * (df["high"] - df["close"]) / high_low_range,
    )

    # Compute Buy and Sell Volume Percentages using positive values
    eps = 1e-10
    vol_sum = df_copy["relative_buy_volume"] + df_copy["relative_sell_volume_pos"] + eps
    df_copy["buy_volume_percent"] = df_copy["relative_buy_volume"] / vol_sum
    df_copy["sell_volume_percent"] = df_copy["relative_sell_volume_pos"] / vol_sum

    # Compute Buy vs. Sell Difference
    df_copy["buy_vs_sell"] = (
        df_copy["buy_volume_percent"] - df_copy["sell_volume_percent"]
    )

    # Apply EMA Smoothing for Delta Mode
    df_copy["buy_vs_sell_short_ema"] = (
        df_copy["buy_vs_sell"].ewm(span=21, adjust=False).mean()
        * df_copy["volume_sma_200"]
        * 20
    )
    df_copy["buy_vs_sell_long_ema"] = (
        df_copy["buy_vs_sell"].ewm(span=36, adjust=False).mean()
        * df_copy["volume_sma_200"]
        * 20
    )
    df_copy["buy_vs_sell_diff"] = (
        df_copy["buy_vs_sell_short_ema"] - df_copy["buy_vs_sell_long_ema"]
    )

    if smoothing_line:
        df_copy["smoothed_delta"] = (
            df_copy["buy_vs_sell_diff"].ewm(span=delta_smoothing, adjust=False).mean()
        )
    else:
        df_copy["smoothed_delta"] = df_copy["buy_vs_sell_diff"]

    # Now, flip the sign of the sell volume for output (to match Pine Script's negative plotting)
    df_copy["relative_sell_volume"] = -df_copy["relative_sell_volume_pos"]

    # Return selected columns
    columns_to_return = [
        "relative_buy_volume",
        "relative_sell_volume",
        "buy_vs_sell",
        "smoothed_delta",
    ]
    if show_total_volume:
        columns_to_return.append("total_volume")

    return df_copy[columns_to_return]


time_relative_volume_oscillator.__doc__ = """
Name:
    Time Relative Volume Oscillator (TRVO)

Description:
    Time Relative Volume Oscillator (TRVO) - Delta Mode
    
    This indicator measures relative volume compared to historical values and differentiates
    between buy and sell volumes. It first calculates a relative volume by comparing current
    volume to a historical average, then applies a sigmoid-like transformation to normalize
    the values. The volume is then split into buy and sell components based on where the close
    price sits within the high-low range. Finally, the indicator creates a "delta" or difference
    between short and long EMAs of the buy/sell percentage differences.

More info:
    This is a custom indicator inspired by volume profile analysis techniques used by 
    professional traders. The sigmoid transformation helps normalize volume spikes.

Parameters:
    - df (pd.DataFrame): Input DataFrame containing 'high', 'low', 'close', and 'volume'.
    - column (str): Column name for price source (default: "close").
    - relative_len (int): Number of previous periods used for relative volume calculation (default: 6).
    - delta_smoothing (int): Smoothing factor for the buy/sell volume difference (default: 9).
    - smoothing_line (bool): If True, applies EMA smoothing to buy/sell volume difference (default: True).
    - show_total_volume (bool): If True, includes the 'total_volume' column in the output DataFrame (default: False).

Call with:
    trvo_result = bta.time_relative_volume_oscillator(
        df,
        column="close",
        relative_len=6,
        delta_smoothing=9,
        smoothing_line=True,
        show_total_volume=False,
    )
    df["relative_buy_volume"] = trvo_result["relative_buy_volume"]
    df["relative_sell_volume"] = trvo_result["relative_sell_volume"]
    df["buy_vs_sell"] = trvo_result["buy_vs_sell"]
    df["smoothed_delta"] = trvo_result["smoothed_delta"]

Returns:
    pd.DataFrame: A DataFrame containing:
        - "relative_buy_volume": Volume attributed to buyers.
        - "relative_sell_volume": Volume attributed to sellers (negative).
        - "buy_vs_sell": Difference between buy and sell volume percentages.
        - "smoothed_delta": EMA-smoothed buy/sell volume difference.
        - "total_volume" (optional): Raw total volume for each period (if show_total_volume=True).
"""


def test():
    """
    Test function for the time_relative_volume_oscillator indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the time_relative_volume_oscillator indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(time_relative_volume_oscillator)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
