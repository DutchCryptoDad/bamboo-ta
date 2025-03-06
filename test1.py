# import os
# import pandas as pd
# import bamboo_ta.bamboo_ta as bta

# class IndicatorTester:
#     def __init__(self, df):
#         self.df = df
#         self.results = {}

#     def run_test(self, indicator_name, *args, **kwargs):
#         """Run a test for a given indicator and store the result."""
#         try:
#             method = getattr(bta, indicator_name)
#             result = method(self.df, *args, **kwargs)
#             self.results[indicator_name] = result
#             for key, value in result.items():
#                 self.df[key] = value
#         except AttributeError:
#             print(f"Indicator {indicator_name} not found in bamboo_ta.")
#         except Exception as e:
#             print(f"Error testing {indicator_name}: {e}")

#     def print_results(self):
#         """Print the last few rows of the DataFrame to verify results."""
#         print(self.df.tail(35))

# def load_data():
#     """Load data from JSON file."""
#     try:
#         file_path = os.path.join(os.path.dirname(__file__), "data", "BTC_USDT-1d.json")
#         df = pd.read_json(file_path)
#         df.columns = ["date", "open", "high", "low", "close", "volume"]
#         df["date"] = pd.to_datetime(df["date"], unit="ms")
#         return df
#     except FileNotFoundError as e:
#         print(f"Error: {e}. Please ensure the file path is correct and the file exists.")
#         return pd.DataFrame()

# # Load data
# df = load_data()

# # Initialize the tester
# tester = IndicatorTester(df)

# # List of indicators to test with their parameters
# indicators_to_test = [
    
#     # # Section that tests all the candles indicators
#     # ("dynamic_exhaustion_bars", [], {}),
#     # ("heiken_ashi", [], {}),
#     # ("smoothed_heiken_ashi", [], {}),
#     # ("hansen_heiken_ashi", [], {}),
#     # ("linear_regression_candles", [], {}),
#     # ("exhaustion_bars", [], {}),
    
#     # # Section that tests all the cycles indicators
#     # ("cycles", [], {}),

#     # # Section that tests all the momentum indicators
#     # ("awesome_oscillator", [], {}),
#     # ("chande_momentum_oscillator", [14], {}),
#     # ("macd", ['close', 12, 26, 9], {}),
#     # ("macd_leader", ['close', 12, 26, 9], {}),
#     # ("momentum_divergence", [10, 20, 2.0, 30], {}),
#     # ("relative_strength_index", ['close', 14], {}),
#     # ("stochastic_rsi", [14, 14, 3, 3], {}),
#     # ("percentage_volume_oscillator", ['volume', 26, 12, 9], {}),
#     # ("macd_v", ['close', 12, 26, 26, 9], {}),
#     # ("kaufman_adaptive_moving_average", ['close', 10], {}),
#     # ("trix", ['close', 14], {}),
#     # ("ultimate_oscillator", ['high', 'low', 'close', 7, 14, 28], {}),
    
#     # # section that tests all the performance indicators
#     # ("sharpe_ratio", ['close'], {'risk_free_rate': 0.01, 'window': 252}),
#     # ("sortino_ratio", ['close'], {'risk_free_rate': 0.01, 'window': 252}),
#     # ("maximum_drawdown", ['close'], {}),
#     # ("calmar_ratio", ['close'], {'window': 252}),
#     # ("information_ratio", ['close', 'benchmark'], {}),
#     # ("alpha", ['close', 'benchmark'], {'risk_free_rate': 0.01, 'window': 252}),
#     # ("beta", ['close', 'benchmark'], {}),
#     # ("treynor_ratio", ['close', 'benchmark'], {'risk_free_rate': 0.01, 'window': 252}),
#     # ("jensens_alpha", ['close', 'benchmark'], {'risk_free_rate': 0.01, 'window': 252}),
    
#     # # Section that tests all the trend indicators
#     # ("wave_trend", [10, 21, 4], {}),
#     # ("wave_trend_oscillator", [10, 21, 4], {}),
#     # ("qqe_mod", [6, 5, 3, 3, 50, 0.35, 6, 5, 1.61, 3], {}),
#     # ("wilders_moving_average", ['close', 14], {}),
#     # ("linear_regression", ['close', 14], {}),
#     # ("linear_regression_angle", ['close', 14], {}),
#     # ("linear_regression_intercept", ['close', 14], {}),
#     # ("linear_regression_slope", ['close', 14], {}),
#     # ("linear_regression_r_squared", ['close', 14], {}),
#     # ("linear_regression_std_error", ['close', 14], {}),
#     # ("linear_regression_trend", ['close', 14], {}),
    
#     # Section that tests all the volatility indicators
#     ("average_true_range", ['close', 14], {}),
#     ("average_true_range_indicator", ['close', 14], {}),
#     ("average_true_range_oscillator", ['close', 14], {}),
#     ("average_true_range_trend", ['close', 14], {}),
#     ("average_true_range_trend_oscillator", ['close', 14], {}),
#     ("average_true_range_trend_angle", ['close', 14], {}),
    
#     # Section that tests all the volume indicators
#     ("volume_profile", ['close', 14], {}),
#     ("volume_profile_oscillator", ['close', 14], {}),
#     ("volume_profile_trend", ['close', 14], {}),
#     ("volume_profile_trend_oscillator", ['close', 14], {}),
#     ("volume_profile_trend_angle", ['close', 14], {}),
    
#     # Section that tests all the statistical indicators
#     ("z_score", ['close', 14], {}),
#     ("z_score_oscillator", ['close', 14], {}),
#     ("z_score_trend", ['close', 14], {}),
#     ("z_score_trend_oscillator", ['close', 14], {}),
#     ("z_score_trend_angle", ['close', 14], {}),
    
#     # Section that test all the other indicators
#     ("fisher_transform", ['close', 14], {}),
#     ("fisher_transform_oscillator", ['close', 14], {}),
#     ("fisher_transform_trend", ['close', 14], {}),
#     ("fisher_transform_trend_oscillator", ['close', 14], {}),
#     ("fisher_transform_trend_angle", ['close', 14], {}),
    
# ]

# # Run tests
# for indicator, args, kwargs in indicators_to_test:
#     tester.run_test(indicator, *args, **kwargs)

# # Print results
# tester.print_results()