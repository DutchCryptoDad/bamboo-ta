# -*- coding: utf-8 -*-
# volume_profile.py

import pandas as pd
import numpy as np


def volume_profile(df: pd.DataFrame, width: int = 10, sort_close: bool = False) -> pd.DataFrame:
    """Volume Profile (VP)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    width = int(width) if width > 0 else 10
    
    # Calculate signed price and volume
    df_copy["price_change"] = df_copy["close"].diff().fillna(0)
    df_copy["signed_price"] = np.where(df_copy["price_change"] >= 0, 1, -1)
    
    # Positive and negative volume
    df_copy["pos_volume"] = np.where(
        df_copy["signed_price"] > 0, df_copy["volume"], 0
    )
    df_copy["neg_volume"] = np.where(
        df_copy["signed_price"] < 0, -df_copy["volume"], 0
    )
    
    if sort_close:
        # Sort by close price and cut into bins
        df_copy["mean_price"] = df_copy["close"]
        bins = pd.cut(df_copy["close"], width, include_lowest=True, precision=2)
        
        # Group by price bins and aggregate
        vpdf = df_copy.groupby(bins).agg({
            "mean_price": np.mean,
            "pos_volume": np.sum,
            "neg_volume": np.sum,
        })
        
        # Get bin boundaries
        vpdf["low_price"] = [x.left for x in vpdf.index]
        vpdf["high_price"] = [x.right for x in vpdf.index]
        vpdf = vpdf.reset_index(drop=True)
        
        # Reorder columns
        vpdf = vpdf[["low_price", "mean_price", "high_price", "pos_volume", "neg_volume"]]
    else:
        # Split data into equal sections
        vp_ranges = np.array_split(df_copy, width)
        
        # Compute statistics for each section
        result = []
        for r in vp_ranges:
            if len(r) > 0:  # Ensure the range has data
                section = {
                    "low_price": r["close"].min(),
                    "mean_price": r["close"].mean(),
                    "high_price": r["close"].max(),
                    "pos_volume": r["pos_volume"].sum(),
                    "neg_volume": r["neg_volume"].sum(),
                }
                result.append(section)
        
        # Create DataFrame from results
        vpdf = pd.DataFrame(result)
    
    # Calculate total volume
    vpdf["total_volume"] = vpdf["pos_volume"] + vpdf["neg_volume"]
    
    return vpdf


volume_profile.__doc__ = \
"""
Name:
    Volume Profile (VP)

Description:
    The Volume Profile indicator divides the price range into a specified number of 
    price levels and calculates the trading volume that occurred at each level. This 
    provides insight into which price levels had the most trading activity.
    
    It differentiates between positive and negative volume based on whether the price 
    was rising or falling, allowing for more detailed analysis of buying and selling 
    pressure at different price levels.
    
    Note: Value Area is not calculated in this implementation.

More info:
    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:volume_by_price
    https://www.tradingview.com/wiki/Volume_Profile

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - width (int): How many price ranges to divide the data into. Default is 10.
    - sort_close (bool): Whether to sort data by close price before splitting into ranges. 
                          When False (default), data is split chronologically. When True, 
                          it's split by price level.

Call with:
    result = bta.volume_profile(df)
    # Access results with:
    low_prices = result['low_price']
    mean_prices = result['mean_price']
    high_prices = result['high_price']
    pos_volumes = result['pos_volume']
    neg_volumes = result['neg_volume']
    total_volumes = result['total_volume']

Returns:
    pd.DataFrame: DataFrame with columns 'low_price', 'mean_price', 'high_price', 
                 'pos_volume', 'neg_volume', and 'total_volume'.
"""


def test():
    """
    Test function for the volume_profile indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the volume_profile indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(volume_profile)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 