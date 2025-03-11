# -*- coding: utf-8 -*-
# sharpe_ratio.py

import pandas as pd
import numpy as np


def sharpe_ratio(
    df: pd.DataFrame,
    benchmark_rate: float = 0.0,
    use_log_returns: bool = False,
    use_cagr: bool = False,
    trading_days_per_year: int = 252,
    column: str = "close"
) -> pd.DataFrame:
    """Sharpe Ratio Indicator"""
    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Extract the price series
    price = df_copy[column]
    
    # Check if we have enough data
    if len(price) < 2:
        raise ValueError("At least two price points are required to calculate Sharpe ratio")
    
    # Calculate returns based on specified method
    if use_log_returns:
        # Calculate log returns: ln(price_t / price_{t-1})
        returns = np.log(price / price.shift(1)).dropna()
    else:
        # Calculate percentage returns: (price_t / price_{t-1}) - 1
        returns = (price / price.shift(1) - 1).dropna()
    
    if use_cagr:
        # Calculate CAGR if specified
        start_price = price.iloc[0]
        end_price = price.iloc[-1]
        
        # Determine the time period in years
        if isinstance(df_copy.index, pd.DatetimeIndex):
            years_diff = (df_copy.index[-1] - df_copy.index[0]).days / 365.25
        else:
            years_diff = len(price) / trading_days_per_year
            
        # Calculate CAGR
        cagr = ((end_price / start_price) ** (1 / years_diff)) - 1
        
        # Calculate annualized standard deviation of returns
        ann_std = np.sqrt(trading_days_per_year) * returns.std()
        
        # Calculate Sharpe ratio using CAGR method
        sharpe = (cagr - benchmark_rate) / ann_std
    else:
        # Calculate annualized return
        ann_return = trading_days_per_year * returns.mean()
        
        # Calculate annualized standard deviation of returns
        ann_std = np.sqrt(trading_days_per_year) * returns.std()
        
        # Calculate Sharpe ratio using annualized returns method
        sharpe = (ann_return - benchmark_rate) / ann_std
    
    # Create a DataFrame with the result
    result = pd.DataFrame({"sharpe_ratio": [sharpe]}, index=[df_copy.index[-1]])
    
    return result


sharpe_ratio.__doc__ = """
Name:
    Sharpe Ratio

Description:
    Calculates the Sharpe ratio, which measures the performance of an investment 
    compared to a risk-free asset, after adjusting for its risk. It's defined as 
    the excess return per unit of deviation (typically standard deviation) of an
    investment asset or portfolio.

More info:
    The Sharpe ratio was developed by Nobel laureate William F. Sharpe and is used
    to help investors understand the return of an investment compared to its risk.
    The ratio is the average return earned in excess of the risk-free rate per unit
    of volatility or total risk.
    
    A higher Sharpe ratio indicates a better risk-adjusted performance.
    Generally, a Sharpe ratio greater than 1.0 is considered acceptable.
    A ratio higher than 2.0 is considered very good.
    A ratio of 3.0 or higher is considered excellent.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified.
    - benchmark_rate (float): The risk-free rate to compare against. Default is 0.0.
    - use_log_returns (bool): If True, uses logarithmic returns instead of percentage
      returns for calculation. Default is False.
    - use_cagr (bool): If True, uses CAGR (Compound Annual Growth Rate) instead of
      simple annualized returns for calculation. Default is False.
    - trading_days_per_year (int): Number of trading days in a year, used for
      annualizing returns and volatility. Default is 252.
    - column (str): The column to calculate the Sharpe ratio on. Default is 'close'.

Call with:
    sharpe_result = bta.sharpe_ratio(df, benchmark_rate=0.02)
    df['sharpe'] = sharpe_result['sharpe_ratio'][0]  # Extract single value

Returns:
    pd.DataFrame: DataFrame with a single row containing the Sharpe ratio value in
    a column named 'sharpe_ratio'.
"""


def test():
    """
    Test function for the sharpe_ratio function.
    
    This function creates test DataFrames with different return patterns
    and calculates their Sharpe ratios.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        import numpy as np
        from datetime import datetime, timedelta
        
        # Function to generate price series with given return and volatility
        def generate_prices(init_price, days, annual_return, annual_volatility):
            # Convert annual values to daily
            daily_return = annual_return / 252
            daily_volatility = annual_volatility / np.sqrt(252)
            
            # Generate random daily returns
            np.random.seed(42)  # For reproducibility
            daily_returns = np.random.normal(daily_return, daily_volatility, days)
            
            # Calculate cumulative returns and price series
            cumulative_returns = np.cumprod(1 + daily_returns)
            prices = init_price * cumulative_returns
            
            return prices
        
        # Create date range for 1 year of trading days
        start_date = datetime(2023, 1, 1)
        dates = [start_date + timedelta(days=i) for i in range(252)]
        
        # Test case 1: Good return, low volatility (should have high Sharpe)
        good_prices = generate_prices(100, 252, 0.15, 0.10)  # 15% return, 10% volatility
        good_df = pd.DataFrame({'close': good_prices}, index=dates)
        
        # Test case 2: Good return, high volatility (should have medium Sharpe)
        medium_prices = generate_prices(100, 252, 0.15, 0.20)  # 15% return, 20% volatility
        medium_df = pd.DataFrame({'close': medium_prices}, index=dates)
        
        # Test case 3: Low return, high volatility (should have low Sharpe)
        bad_prices = generate_prices(100, 252, 0.05, 0.20)  # 5% return, 20% volatility
        bad_df = pd.DataFrame({'close': bad_prices}, index=dates)
        
        # Calculate Sharpe ratios
        good_sharpe = sharpe_ratio(good_df, benchmark_rate=0.02)
        medium_sharpe = sharpe_ratio(medium_df, benchmark_rate=0.02)
        bad_sharpe = sharpe_ratio(bad_df, benchmark_rate=0.02)
        
        # Calculate log return Sharpe ratios
        good_sharpe_log = sharpe_ratio(good_df, benchmark_rate=0.02, use_log_returns=True)
        medium_sharpe_log = sharpe_ratio(medium_df, benchmark_rate=0.02, use_log_returns=True)
        bad_sharpe_log = sharpe_ratio(bad_df, benchmark_rate=0.02, use_log_returns=True)
        
        # Print results
        print("Sharpe Ratio Test Results (benchmark rate = 2%):")
        print(f"High performance portfolio (15% return, 10% volatility):")
        print(f"  Sharpe ratio: {good_sharpe['sharpe_ratio'].iloc[0]:.4f}")
        print(f"  Sharpe ratio (log returns): {good_sharpe_log['sharpe_ratio'].iloc[0]:.4f}")
        
        print(f"\nMedium performance portfolio (15% return, 20% volatility):")
        print(f"  Sharpe ratio: {medium_sharpe['sharpe_ratio'].iloc[0]:.4f}")
        print(f"  Sharpe ratio (log returns): {medium_sharpe_log['sharpe_ratio'].iloc[0]:.4f}")
        
        print(f"\nLow performance portfolio (5% return, 20% volatility):")
        print(f"  Sharpe ratio: {bad_sharpe['sharpe_ratio'].iloc[0]:.4f}")
        print(f"  Sharpe ratio (log returns): {bad_sharpe_log['sharpe_ratio'].iloc[0]:.4f}")
        
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 