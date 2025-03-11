# -*- coding: utf-8 -*-
# momentum_divergence.py

import pandas as pd


def momentum_divergence(
    df: pd.DataFrame,
    mom_length: int = 10,
    bb_length: int = 20,
    bb_dev: float = 2.0,
    lookback: int = 30,
) -> pd.DataFrame:
    """Momentum Divergence"""
    df_copy = df.copy()

    # Calculate momentum
    df_copy["mom"] = df_copy["close"].diff(mom_length)

    # Calculate Bollinger Bands for momentum
    df_copy["mom_mean"] = df_copy["mom"].rolling(window=bb_length).mean()
    df_copy["mom_std"] = df_copy["mom"].rolling(window=bb_length).std()
    df_copy["upperb"] = df_copy["mom_mean"] + (bb_dev * df_copy["mom_std"])
    df_copy["lowerb"] = df_copy["mom_mean"] - (bb_dev * df_copy["mom_std"])

    # Buy and sell signals
    df_copy["buy"] = (df_copy["mom"] < df_copy["lowerb"]).astype(int)
    df_copy["sell"] = (df_copy["mom"] > df_copy["upperb"]).astype(int)

    # Highest high and lowest low over lookback period
    df_copy["hh"] = df_copy["high"].rolling(window=lookback).max()
    df_copy["ll"] = df_copy["low"].rolling(window=lookback).min()
    df_copy["coh"] = (df_copy["high"] >= df_copy["hh"]).astype(int)
    df_copy["col"] = (df_copy["low"] <= df_copy["ll"]).astype(int)

    # Return relevant columns
    result = pd.DataFrame(
        {
            "momentum_divergence_mom": df_copy["mom"],
            "momentum_divergence_upperb": df_copy["upperb"],
            "momentum_divergence_lowerb": df_copy["lowerb"],
            "momentum_divergence_buy": df_copy["buy"],
            "momentum_divergence_sell": df_copy["sell"],
            "momentum_divergence_coh": df_copy["coh"],
            "momentum_divergence_col": df_copy["col"],
        }
    )

    return result


momentum_divergence.__doc__ = """
Name:
    Momentum Divergence (momdiv)

Description:
    A self-contained implementation of the Momentum Divergence indicator. It calculates
    momentum and applies Bollinger Bands to identify potential buy and sell signals
    based on momentum divergence. Additionally, it detects if the current high or low
    breaks the highest high or lowest low over a specified lookback period.

More info:
    https://www.tradingview.com/script/Yq1z7cIv-MA-Streak-Can-Show-When-a-Run-Is-Getting-Long-in-the-Tooth/

Call with:
    momdiv_result = bta.momentum_divergence(df, mom_length=5, bb_length=5, bb_dev=1.0, lookback=5)
    df['momentum_divergence_mom'] = momdiv_result['momentum_divergence_mom']
    df['momentum_divergence_upperb'] = momdiv_result['momentum_divergence_upperb']
    df['momentum_divergence_lowerb'] = momdiv_result['momentum_divergence_lowerb']
    df['momentum_divergence_buy'] = momdiv_result['momentum_divergence_buy']
    df['momentum_divergence_sell'] = momdiv_result['momentum_divergence_sell']
    df['momentum_divergence_coh'] = momdiv_result['momentum_divergence_coh']
    df['momentum_divergence_col'] = momdiv_result['momentum_divergence_col']

Parameters:
    - df (pd.DataFrame): Input DataFrame containing OHLC data.
    - mom_length (int, default=10): Lookback period for momentum calculation.
    - bb_length (int, default=20): Lookback period for Bollinger Bands calculation.
    - bb_dev (float, default=2.0): Number of standard deviations for Bollinger Bands.
    - lookback (int, default=30): Lookback period for detecting highest high and lowest low.

Returns:
    - pd.DataFrame: DataFrame with the following columns:
    - 'momentum_divergence_mom': Calculated momentum.
    - 'momentum_divergence_upperb': Upper Bollinger Band for momentum.
    - 'momentum_divergence_lowerb': Lower Bollinger Band for momentum.
    - 'momentum_divergence_buy': Boolean indicating a buy signal (momentum crossed below lower band).
    - 'momentum_divergence_sell': Boolean indicating a sell signal (momentum crossed above upper band).
    - 'momentum_divergence_coh': Boolean indicating the current high is the highest high over the lookback period.
    - 'momentum_divergence_col': Boolean indicating the current low is the lowest low over the lookback period.
"""


def test():
    """
    Test function for the momentum_divergence indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the momentum_divergence indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Suppress the RuntimeWarning about module imports
        import warnings
        warnings.filterwarnings("ignore", category=RuntimeWarning, 
                               message=".*found in sys.modules after import of package.*")
        
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(momentum_divergence)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
