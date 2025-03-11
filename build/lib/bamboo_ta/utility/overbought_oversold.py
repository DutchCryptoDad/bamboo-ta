# -*- coding: utf-8 -*-
# overbought_oversold.py
import numpy as np
import pandas as pd


def overbought_oversold(
    df: pd.DataFrame,
    indicator_col: str,
    overbought_value: float = 75,
    oversold_value: float = 30,
    previous_rows: int = 5,
) -> pd.Series:
    """
    Overbought/Oversold (OBOS) Indicator

    Determines overbought, oversold, and trigger conditions based on a specified indicator column.

    Parameters:
    - df (pd.DataFrame): The input DataFrame containing the indicator column.
    - indicator_col (str): The name of the column containing the indicator values.
    - overbought_value (float, default=75): The overbought threshold.
    - oversold_value (float, default=30): The oversold threshold.
    - previous_rows (int, default=5): Number of previous rows to consider for trigger conditions.

    Call with:
        obos = bta.overbought_oversold(
            df,
            indicator_col='indicator',  # Replace 'indicator' with the column name containing the indicator values
            overbought_value=75,       # Specify the overbought threshold (default: 75)
            oversold_value=30,         # Specify the oversold threshold (default: 30)
            previous_rows=5            # Number of previous rows to consider for trigger conditions (default: 5)
        )

        # Integrate results into the original DataFrame
        df['obos_condition'] = obos

    Returns:
    - pd.Series: A Series containing the OBOS conditions:
        - 'overbought'
        - 'oversold'
        - 'overbought_trigger'
        - 'oversold_trigger'
        - 'neutral'
    """
    if indicator_col not in df.columns:
        raise ValueError(f"Column '{indicator_col}' not found in the DataFrame.")

    # Create arrays for efficiency
    indicator = df[indicator_col].values
    obos_condition = np.full(len(df), "neutral", dtype=object)

    # Determine 'overbought' and 'oversold'
    obos_condition[indicator > overbought_value] = "overbought"
    obos_condition[indicator < oversold_value] = "oversold"

    # Determine 'overbought_trigger' and 'oversold_trigger' conditions
    for i in range(previous_rows, len(df)):
        if obos_condition[i] == "neutral":
            previous_values = indicator[i - previous_rows : i]
            if (previous_values < oversold_value).any():
                obos_condition[i] = "oversold_trigger"
            elif (previous_values > overbought_value).any():
                obos_condition[i] = "overbought_trigger"

    return pd.Series(obos_condition, index=df.index, name="obos_condition")


overbought_oversold.__doc__ = """
Name:
    Overbought/Oversold (OBOS) Indicator

Description:
    This function analyzes an oscillator-type indicator (like RSI, Stochastic, etc.)
    and categorizes market conditions as overbought, oversold, or in trigger states.
    It not only identifies when the indicator is currently in extreme territory but
    also detects when the indicator has recently been in extreme territory but has
    now returned to neutral levels - these are the "trigger" conditions that often
    represent good entry points.

More info:
    Oscillator indicators typically fluctuate between fixed boundaries (often 0-100)
    and help identify market extremes. Values above a certain threshold (e.g., 70-80)
    suggest overbought conditions, while values below another threshold (e.g., 20-30)
    suggest oversold conditions.
    
    The "trigger" conditions identified by this function are particularly valuable
    as they often represent potential reversal points with better risk/reward ratios
    than entering during extreme readings.

Parameters:
    - df (pd.DataFrame): The input DataFrame containing the indicator column.
    - indicator_col (str): The name of the column containing the indicator values
      (e.g., 'rsi', 'stoch_k', 'cci', etc.).
    - overbought_value (float, default=75): The threshold above which the market
      is considered overbought.
    - oversold_value (float, default=30): The threshold below which the market
      is considered oversold.
    - previous_rows (int, default=5): Number of previous rows to check when
      determining trigger conditions.

Call with:
    # Using RSI as the indicator
    df['obos'] = bta.overbought_oversold(df, indicator_col='rsi', 
                                          overbought_value=70, oversold_value=30)
    
    # Using Stochastic as the indicator
    df['stoch_obos'] = bta.overbought_oversold(df, indicator_col='stoch_k', 
                                               overbought_value=80, oversold_value=20)

Returns:
    pd.Series: A Series containing string values representing the market condition:
        - 'overbought': Current indicator value is above the overbought threshold
        - 'oversold': Current indicator value is below the oversold threshold
        - 'overbought_trigger': Indicator recently left overbought territory
        - 'oversold_trigger': Indicator recently left oversold territory
        - 'neutral': None of the above conditions are met
"""


def test():
    """
    Test function for the overbought_oversold indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the overbought_oversold indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(overbought_oversold)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
