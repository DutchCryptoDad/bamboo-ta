# -*- coding: utf-8 -*-
# ehlers_fisher_stochastic_center_of_gravity.py

import numpy as np
import pandas as pd

def ehlers_fisher_stochastic_center_of_gravity(df: pd.DataFrame, length: int = 8) -> pd.DataFrame:
    """Ehlers Fisher Stochastic Center of Gravity"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['high', 'low']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    price = (df['high'] + df['low']) / 2

    # Initialize series
    num = pd.Series([0.0] * len(df), index=df.index)
    denom = pd.Series([0.0] * len(df), index=df.index)
    sg = pd.Series([0.0] * len(df), index=df.index)

    min_bar = length + 1
    l = (length + 1) / 2

    # Calculate CG
    for i in range(min_bar, len(df)):
        num_val = 0.0
        denom_val = 0.0
        for count in range(length):
            num_val += (1 + count) * price.iloc[i - count]
            denom_val += price.iloc[i - count]

        if denom_val != 0:
            sg.iloc[i] = l - num_val / denom_val
        else:
            sg.iloc[i] = 0.0

        max_cg = sg.iloc[i - length + 1:i + 1].max()
        min_cg = sg.iloc[i - length + 1:i + 1].min()

        if max_cg != min_cg:
            num.iloc[i] = (sg.iloc[i] - min_cg) / (max_cg - min_cg)
        else:
            num.iloc[i] = 0.0

        denom.iloc[i] = (4 * num.iloc[i] + 3 * num.iloc[i - 1] + 
                         2 * num.iloc[i - 2] + num.iloc[i - 3]) / 10

    # Calculate Value3 (V3) and Trigger
    v3 = 0.5 * np.log((1 + 1.98 * (denom - 0.5)) / (1 - 1.98 * (denom - 0.5)))
    trigger = v3.shift(1)

    df_copy['cg'] = v3
    df_copy['trigger'] = trigger

    return df_copy[['cg', 'trigger']]

ehlers_fisher_stochastic_center_of_gravity.__doc__ = \
"""
Name:
    Ehlers Fisher Stochastic Center of Gravity Indicator

Description:
    The Fisher Stochastic Center of Gravity indicator, developed by John Ehlers, 
    is used to identify potential turning points in the market by calculating 
    the center of gravity of price movements.

More info:
    https://ninjatraderecosystem.com/user-app-share-download/john-ehlers-the-fisher-stochastic-center-of-gravity/
    https://fxstill.com/indikators/the-fisher-stochastic-center-of-gravity
    https://viewer.mathworks.com/?viewer=plain_code&url=https%3A%2F%2Fes.mathworks.com%2Fmatlabcentral%2Fmlc-downloads%2Fdownloads%2F5a9e5f01-906c-4152-98c6-87484eed86bf%2F853ab8ad-8751-4bcd-ae00-60a9444e9182%2Ffiles%2Fmatlab%2FChapter4-Ehlers%2FEhlerStochCG.m&embed=web
    https://www.tradingview.com/script/TLjl71aL-Ehlers-Fisher-Stochastic-Center-Of-Gravity-CC/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'high', 'low'.
    - length (int): Period for the indicator. Default is 8.

Call with:
    fscg = bta.ehlers_fisher_stochastic_center_of_gravity(df)
    df['cg'] = fscg['cg']
    df['trigger'] = fscg['trigger']

Returns:
    pd.DataFrame: DataFrame with 'CG' and 'Trigger' columns.
"""

def test():
    """
    Test function for the ehlers_fisher_stochastic_center_of_gravity indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the ehlers_fisher_stochastic_center_of_gravity indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(ehlers_fisher_stochastic_center_of_gravity)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
