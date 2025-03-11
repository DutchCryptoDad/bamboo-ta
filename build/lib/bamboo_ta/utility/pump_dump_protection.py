# -*- coding: utf-8 -*-
# pump_dump_protection.py
import numpy as np
import pandas as pd


def pump_dump_protection(
    df: pd.DataFrame,
    rsi_period: int = 14,
    short_volume_window: int = 4,
    long_volume_window: int = 48,
    volume_warn_threshold: float = 5.0,
) -> pd.DataFrame:
    """
    Pump and Dump Protection Indicator

    This function detects abnormal volume changes and price movements to identify potential pump-and-dump
    scenarios. It eliminates dependency on a specific timeframe, relying only on rolling calculations.

    Parameters:
    - df (pd.DataFrame): Input DataFrame with required columns:
        - 'close': Closing price.
        - 'high': High price for the interval.
        - 'low': Low price for the interval.
        - 'volume': Volume for the interval.
    - rsi_period (int, default=14): Lookback period for RSI calculation.
    - short_volume_window (int, default=4): Rolling window size for short-term volume mean.
    - long_volume_window (int, default=48): Rolling window size for long-term volume mean.
    - volume_warn_threshold (float, default=5.0): Threshold for detecting abnormal short-term volume spikes.

    Call with:
        pd_result = bta.pump_dump_protection_no_timeframe(
            df,
            rsi_period=14,
            short_volume_window=4,
            long_volume_window=48,
            volume_warn_threshold=5.0
        )

        # Add all calculated columns to the original DataFrame
        df['volume_mean_short'] = pd_result['volume_mean_short']
        df['volume_mean_long'] = pd_result['volume_mean_long']
        df['volume_change_percentage'] = pd_result['volume_change_percentage']
        df['rsi'] = pd_result['rsi']
        df['pnd_volume_warn'] = pd_result['pnd_volume_warn']

    Returns:
    - pd.DataFrame: The DataFrame with the following additional columns:
        - 'volume_mean_short': Rolling mean of volume over `short_volume_window` intervals.
        - 'volume_mean_long': Rolling mean of volume over `long_volume_window` intervals.
        - 'volume_change_percentage': Ratio of 'volume_mean_short' to 'volume_mean_long'.
        - 'rsi': Calculated RSI values.
        - 'pnd_volume_warn': Indicator for abnormal volume spikes.
    """
    df_copy = df.copy()

    # Calculate RSI
    delta = df_copy["close"].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=rsi_period).mean()
    avg_loss = pd.Series(loss).rolling(window=rsi_period).mean()
    rs = avg_gain / avg_loss
    df_copy["rsi"] = 100 - (100 / (1 + rs))

    # Calculate rolling volume means
    df_copy["volume_mean_short"] = df_copy["volume"].rolling(short_volume_window).mean()
    df_copy["volume_mean_long"] = df_copy["volume"].rolling(long_volume_window).mean()

    # Calculate volume change percentage
    df_copy["volume_change_percentage"] = (
        df_copy["volume_mean_short"] / df_copy["volume_mean_long"]
    )

    # Abnormal volume spike detection
    df_copy["pnd_volume_warn"] = np.where(
        (
            df_copy["volume_mean_short"] / df_copy["volume_mean_long"]
            > volume_warn_threshold
        ),
        -1,
        0,
    )

    return df_copy[
        [
            "volume_mean_short",
            "volume_mean_long",
            "volume_change_percentage",
            "rsi",
            "pnd_volume_warn",
        ]
    ]


pump_dump_protection.__doc__ = """
Name:
    Pump and Dump Protection

Description:
    This indicator helps detect potential pump-and-dump schemes in cryptocurrency markets
    by monitoring abnormal volume activity and rapid price movements. It calculates several
    metrics including short and long-term volume averages, the relative change in volume,
    and the RSI to identify suspicious market behavior.
    
    Pump-and-dump schemes typically involve artificially inflating an asset's price through
    false recommendations and heavy volume (the "pump") followed by selling off shares at
    the higher price (the "dump"). This indicator can help traders avoid being caught in
    such manipulative schemes.

More info:
    Key warning signs that this indicator identifies:
    - Abnormal increases in trading volume (compared to recent history)
    - Extreme RSI values indicating overbought conditions
    - Sudden, dramatic price increases with volume spikes
    
    When the indicator detects these conditions, it sets the 'pnd_volume_warn' flag to -1,
    suggesting caution and potential manipulation in the market.

Parameters:
    - df (pd.DataFrame): Input DataFrame with required OHLCV columns.
    - rsi_period (int, default=14): Period for RSI calculation.
    - short_volume_window (int, default=4): Period for short-term volume average.
    - long_volume_window (int, default=48): Period for long-term volume average.
    - volume_warn_threshold (float, default=5.0): Threshold for volume spike warning.

Call with:
    # Get pump and dump protection indicators
    pnd_data = bta.pump_dump_protection(
        df,
        rsi_period=14,
        short_volume_window=6,
        long_volume_window=72,
        volume_warn_threshold=4.0
    )
    
    # Add results to the original dataframe
    df['vol_short'] = pnd_data['volume_mean_short']
    df['vol_long'] = pnd_data['volume_mean_long']
    df['vol_change'] = pnd_data['volume_change_percentage']
    df['rsi'] = pnd_data['rsi']
    df['pnd_warning'] = pnd_data['pnd_volume_warn']

Returns:
    pd.DataFrame: A DataFrame with the following columns:
    - 'volume_mean_short': Short-term volume average
    - 'volume_mean_long': Long-term volume average
    - 'volume_change_percentage': Ratio between short and long-term volume
    - 'rsi': Relative Strength Index values
    - 'pnd_volume_warn': Warning flag (-1 for potential pump-and-dump, 0 otherwise)
"""


def test():
    """
    Test function for the pump_dump_protection indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the pump_dump_protection indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(pump_dump_protection)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
