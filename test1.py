import os
import pandas as pd
import bamboo_ta.bamboo_ta as bta


class IndicatorTester:
    def __init__(self, df):
        self.df = df
        self.results = {}

    def run_test(self, indicator_name, *args, **kwargs):
        """Run a test for a given indicator and store the result."""
        try:
            method = getattr(bta, indicator_name)
            
            # Get the function signature to determine parameter types
            import inspect
            sig = inspect.signature(method)
            params = list(sig.parameters.values())
            
            # Check if the first parameter is expected to be a Series
            series_based_indicators = [
                # Utility indicators
                "z_score", "st_dev", "regression_slope", "linear_decay", "linear_growth",
                "consecutive_count", "cumulative_return", "daily_log_return", "daily_return",
                "first_crossed_above_second", "first_crossed_below_second", "get_min_max",
                "same_length", "top_percent_change", "overbought_oversold", "pump_dump_protection",
                
                # Volume indicators
                "force_index", "on_balance_volume", "on_balance_volume_oscillator", 
                "price_volume_trend", "relative_volume",
                
                # Volatility indicators
                "true_range",
                
                # Momentum indicators
                "rate_of_change", "smoothed_rate_of_change", "ma_streak"
            ]
            
            # Special handling for indicators with specific parameter patterns
            special_indicators = {
                "relative_strength_index": {"df_param": True, "column_param": True},
                "percentage_volume_oscillator": {"df_param": True, "column_param": True},
                "macd_v": {"df_param": True, "column_param": True},
                "kaufmans_adaptive_moving_average": {"df_param": True, "column_param": True},
                "stochastic_rsi": {"df_param": True, "column_param": True}
            }
            
            if indicator_name in series_based_indicators:
                # Handle Series-based indicators
                result_dict = {}
                
                # Process each column name in args and convert to Series
                if args and all(isinstance(arg, str) for arg in args if isinstance(arg, str)):
                    # Extract column names and other parameters
                    series_args = []
                    other_args = []
                    
                    for arg in args:
                        if isinstance(arg, str) and arg in self.df.columns:
                            series_args.append(self.df[arg])
                        else:
                            other_args.append(arg)
                    
                    # Call the function with the Series and other args
                    if len(series_args) == 1:
                        # Most common case: one Series and other parameters
                        result = method(series_args[0], *other_args, **kwargs)
                        # Create a descriptive column name
                        col_name = f"{args[0]}_{indicator_name}"
                        if isinstance(result, pd.Series):
                            result_dict[col_name] = result
                        else:
                            # Handle case where result is not a Series
                            result_dict[col_name] = result
                    elif len(series_args) > 1:
                        # Handle case with multiple Series arguments
                        result = method(*series_args, *other_args, **kwargs)
                        if isinstance(result, pd.Series):
                            col_name = f"{indicator_name}"
                            result_dict[col_name] = result
                        else:
                            # Handle case where result is not a Series
                            result_dict = result if isinstance(result, dict) else {indicator_name: result}
                else:
                    # Handle special cases like linear_decay, linear_growth
                    result = method(*args, **kwargs)
                    if isinstance(result, pd.Series):
                        result_dict[indicator_name] = result
                    else:
                        result_dict = result if isinstance(result, dict) else {indicator_name: result}
                
                # Convert result to DataFrame if it's not already
                if not isinstance(result_dict, pd.DataFrame):
                    result = pd.DataFrame(result_dict)
                else:
                    result = result_dict
            elif indicator_name in special_indicators:
                # Handle indicators with specific parameter patterns
                indicator_config = special_indicators[indicator_name]
                
                if indicator_config.get("df_param", False) and indicator_config.get("column_param", False):
                    # This indicator expects a DataFrame and column name
                    if args and isinstance(args[0], str) and args[0] in self.df.columns:
                        column_name = args[0]
                        other_args = args[1:] if len(args) > 1 else []
                        
                        # Create a kwargs dict with the column parameter
                        if indicator_name == "relative_strength_index":
                            kwargs["column"] = column_name
                        elif indicator_name == "percentage_volume_oscillator":
                            kwargs["volume_col"] = column_name
                        elif indicator_name == "macd_v":
                            kwargs["column"] = column_name
                        elif indicator_name == "kaufmans_adaptive_moving_average":
                            kwargs["close_col"] = column_name
                        elif indicator_name == "stochastic_rsi":
                            kwargs["close_col"] = column_name
                        
                        # Call the function with the DataFrame and other args
                        result = method(self.df, *other_args, **kwargs)
                    else:
                        # No column name provided, use default
                        result = method(self.df, *args, **kwargs)
                else:
                    # Standard handling
                    result = method(self.df, *args, **kwargs)
            else:
                # Standard handling for DataFrame-based indicators
                # Check if the first argument is a column name
                if args and args[0] and isinstance(args[0], str) and args[0] in self.df.columns:
                    # This is a DataFrame-based indicator that expects column names
                    # We need to pass only the DataFrame and the rest of the arguments
                    result = method(self.df, *args[1:], **kwargs)
                else:
                    # Regular DataFrame-based indicator
                    result = method(self.df, *args, **kwargs)
            
            self.results[indicator_name] = result
            for key, value in result.items():
                self.df[key] = value
        except AttributeError:
            print(f"Indicator {indicator_name} not found in bamboo_ta.")
        except Exception as e:
            print(f"Error testing {indicator_name}: {e}")

    def print_results(self):
        """Print the last few rows of the DataFrame to verify results."""
        print(self.df.tail(32))


def load_data():
    """Load data from JSON file."""
    try:
        file_path = os.path.join(os.path.dirname(__file__), "data", "BTC_USDT-1d.json")
        df = pd.read_json(file_path)
        df.columns = ["date", "open", "high", "low", "close", "volume"]
        df["date"] = pd.to_datetime(df["date"], unit="ms")
        return df
    except FileNotFoundError as e:
        print(
            f"Error: {e}. Please ensure the file path is correct and the file exists."
        )
        return pd.DataFrame()


# Load data
df = load_data()

# Initialize the tester
tester = IndicatorTester(df)

# List of indicators to test with their parameters
indicators_to_test = [
    # Section that tests all the candle indicators
    # ("dynamic_exhaustion_bars", [], {}), # FOUTIEF
    # ("heiken_ashi", [], {}),
    # ("smoothed_heiken_ashi", [], {}),
    # ("hansen_heiken_ashi", [], {}), # FOUTIEF
    # ("linear_regression_candles", [], {}),
    # ("exhaustion_bars", [], {}),

    # Section that tests all the momentum indicators
    # ("awesome_oscillator", [], {}),
    # ("chande_momentum_oscillator", [14], {}),
    # ("macd", ["close", 12, 26, 9], {}),
    # ("macd_leader", ["close", 12, 26, 9], {}),
    # ("momentum_divergence", ["close", 14, 28, 2.0, 30], {}), # FOUTIEF
    ("relative_strength_index", ["close", 14], {}),
    ("stochastic_rsi", ["close", 14, 14, 3, 3], {}), # FOUTIEF
    ("percentage_volume_oscillator", ["volume", 26, 12, 9], {}),
    ("macd_v", ["close", 12, 26, 26, 9], {}),
    ("kaufmans_adaptive_moving_average", ["close", 10], {}),
    # ("elliott_wave_oscillator", ["close", 5, 35], {}),
    # ("ehlers_fisher_stochastic_center_of_gravity", ["close", 14], {}), # FOUTIEF
    # ("calculate_intraday_momentum_index", ["close"], {}), # FOUTIEF
    # ("ma_streak", ["close", 14], {}), # FOUTIEF
    # ("percentage_price_oscillator", ["close", 26, 12, 9], {}),
    # ("relative_momentum_index", ["close", 14, 14], {}), # FOUTIEF
    # ("rate_of_change", ["close", 14], {}),
    # ("smoothed_rate_of_change", ["close", 14], {}), # FOUTIEF
    # ("waddah_attar_explosion", ["close", 14, 20, 40, 20], {}), # FOUTIEF
    # ("waddah_attar_explosion_atr", ["close", 14, 20, 40, 20], {}), # FOUTIEF
    # ("wave_trend", ["close", 10, 21], {}), # FOUTIEF
    # ("wave_trend_oscillator", ["close", 10, 21], {}),
    # ("qqe_mod", ["close", 6, 5, 3, 3, 50, 0.35, 6, 5, 1.61, 3], {}), # FOUTIEF
    # ("stochastic_momentum_index", ["close", 13, 25, 2, 25], {}), # FOUTIEF
    # ("stochastics_oscillator", ["high", "low", "close", 14, 3], {}),
    # ("true_strength_index", ["close", 25, 13], {}),
    # ("ultimate_oscillator", ["high", "low", "close", 7, 14, 28], {}),
    # ("williams_r", ["high", "low", "close", 14], {}),
    # # Section that tests all the trend indicators
    # ("alligator_bands", ["close", 13, 8, 5], {}),
    # ("bollinger_trend", ["close", 20, 2], {}),
    # ("bollinger_trend_fast_with_ma", ["close", 20, 2], {}),
    # ("breakouts", ["high", "low", 14], {}), # FOUTIEF
    # ("exponential_moving_average", ["close", 14], {}),
    # ("hull_moving_average", ["close", 14], {}),
    # ("least_squares_moving_average", ["close", 14], {}),
    # ("percent_price_channel", ["high", "low", 20], {}), # FOUTIEF
    # ("pmax", ["close", "high", "low", 10, 0.65], {}), # FOUTIEF
    # ("price_channel", ["high", "low", 20], {}), # FOUTIEF
    # ("range_filter", ["close", 10], {}),
    # ("rolling_moving_average", ["close", 14], {}),
    # ("simple_moving_average", ["close", 14], {}),
    # ("ssl_channels", ["high", "low", 14], {}), # FOUTIEF
    # ("ssl_channels_atr", ["close", "high", "low", 14], {}), # FOUTIEF
    # ("t3_average", ["close", 14, 0.7], {}),
    # ("ut_bot", ["close", "high", "low", 10, 2], {}), # FOUTIEF
    # ("weighted_moving_average", ["close", 14], {}),
    # ("zero_exponential_moving_average", ["close", 14], {}),
    # ("zero_lag_exponential_moving_average", ["close", 14], {}),
    # # Section that tests all the volatility indicators
    # ("average_true_range", ["high", "low", "close", 14], {}), # FOUTIEF
    # ("bollinger_bands", ["close", 20, 2], {}),
    # ("bbw_expansion", ["close", 20, 2], {}), # FOUTIEF
    # ("true_range", ["high", "low", "close"], {}), # FOUTIEF
    # ("keltner_channel", ["close", "high", "low", 20, 2], {}), # FOUTIEF
    # ("donchian_channel", ["high", "low", 20], {}), # FOUTIEF
    # ("ulcer_index", ["close", 14], {}),
    # # Section that tests all the volume indicators
    # ("accumulation_distribution_index", ["high", "low", "close", "volume"], {}), # FOUTIEF
    # ("chaikin_money_flow", ["high", "low", "close", "volume", 20], {}), # FOUTIEF
    # ("ease_of_movement", ["high", "low", "volume", 14], {}), # FOUTIEF
    # ("force_index", ["close", "volume", 13], {}), # FOUTIEF
    # ("money_flow_index", ["high", "low", "close", "volume", 14], {}), # FOUTIEF
    # ("negative_volume_index", ["close", "volume"], {}), # FOUTIEF
    # ("on_balance_volume", ["close", "volume"], {}), # FOUTIEF
    # ("on_balance_volume_oscillator", ["close", "volume", 14], {}), # FOUTIEF
    # ("positive_volume_index", ["close", "volume"], {}), # FOUTIEF
    # ("price_volume_trend", ["close", "volume"], {}), # FOUTIEF
    # ("relative_volume", ["volume", 14], {}), # FOUTIEF
    # ("time_relative_volume_oscillator", ["volume", 14, "date"], {}), # FOUTIEF
    # ("volume_weighted_average_price", ["high", "low", "close", "volume"], {}), # FOUTIEF
    # (
    #     "volume_weighted_average_price_bands", # FOUTIEF
    #     ["high", "low", "close", "volume", 20, 2.0],
    #     {},
    # ),
    # # Section that tests all the utility indicators
    # ("calculate_atr_stop_loss_take_profit", ["close", "high", "low", 14, 3], {}), # FOUTIEF
    # ("calculate_stop_loss_take_profit", ["close", "high", "low"], {"percent": 0.03}), # FOUTIEF
    # ("consecutive_count", ["close"], {"rising": True}), # FOUTIEF
    # ("cumulative_return", ["close"], {}), # FOUTIEF
    # ("daily_log_return", ["close"], {}), # FOUTIEF
    # ("daily_return", ["close"], {}), # FOUTIEF
    # ("drop_na", [], {}),
    # ("exhaustion_candles", ["open", "high", "low", "close"], {}), # FOUTIEF
    # ("exhaustion_lengths", ["high", "low", 10], {}), # FOUTIEF
    # ("first_crossed_above_second", ["close", "open"], {}), # FOUTIEF
    # ("first_crossed_below_second", ["close", "open"], {}), # FOUTIEF
    # ("get_min_max", ["close", 14], {}), # FOUTIEF
    # ("linear_decay", [10], {"start": 1.0, "end": 0.0}), # FOUTIEF
    # ("linear_growth", [10], {"start": 0.0, "end": 1.0}), # FOUTIEF
    # ("overbought_oversold", ["close", 70, 30], {}),  # FOUTIEF
    # ("pump_dump_protection", ["close", 48, 1.0], {}), # FOUTIEF
    # ("regression_slope", ["close", 14], {}), # FOUTIEF
    # ("same_length", ["close", "open"], {}), # FOUTIEF
    # ("st_dev", ["close", 14], {}), # FOUTIEF
    # ("top_percent_change", ["close"], {"length": 14, "top_pct": 80}), # FOUTIEF
    # ("z_score", ["close", 14], {}),
]

# Run tests
for indicator, args, kwargs in indicators_to_test:
    tester.run_test(indicator, *args, **kwargs)

# Print results
tester.print_results()
