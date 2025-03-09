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
        print(self.df.tail(35))


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
    # # Section that tests all the candles indicators
    # ("dynamic_exhaustion_bars", [], {}),
    # ("heiken_ashi", [], {}),
    # ("smoothed_heiken_ashi", [], {}),
    # ("hansen_heiken_ashi", [], {}),
    # ("linear_regression_candles", [], {}),
    # ("exhaustion_bars", [], {}),
    # # Section that tests all the momentum indicators
    # ("awesome_oscillator", [], {}),
    # ("chande_momentum_oscillator", [14], {}),
    # ("macd", ["close", 12, 26, 9], {}),
    # ("macd_leader", ["close", 12, 26, 9], {}),
    # ("momentum_divergence", ["close", 14, 28, 2.0, 30], {}),
    # ("relative_strength_index", ["close", 14], {}),
    # ("stochastic_rsi", ["close", 14, 14, 3, 3], {}),
    # ("percentage_volume_oscillator", ["volume", 26, 12, 9], {}),
    # ("macd_v", ["close", 12, 26, 26, 9], {}),
    # ("kaufmans_adaptive_moving_average", ["close", 10], {}),
    # ("elliott_wave_oscillator", ["close", 5, 35], {}),
    # ("ehlers_fisher_stochastic_center_of_gravity", ["close", 14], {}),
    # ("calculate_intraday_momentum_index", ["close"], {}),
    # ("ma_streak", ["close", 14], {}),
    # ("percentage_price_oscillator", ["close", 26, 12, 9], {}),
    # ("relative_momentum_index", ["close", 14, 14], {}),
    # ("rate_of_change", ["close", 14], {}),
    # ("smoothed_rate_of_change", ["close", 14], {}),
    # ("waddah_attar_explosion", ["close", 14, 20, 40, 20], {}),
    # ("waddah_attar_explosion_atr", ["close", 14, 20, 40, 20], {}),
    # ("wave_trend", ["close", 10, 21], {}),
    # ("wave_trend_oscillator", ["close", 10, 21], {}),
    # ("qqe_mod", ["close", 6, 5, 3, 3, 50, 0.35, 6, 5, 1.61, 3], {}),
    # ("stochastic_momentum_index", ["close", 13, 25, 2, 25], {}),
    # ("stochastics_oscillator", ["high", "low", "close", 14, 3], {}),
    # ("true_strength_index", ["close", 25, 13], {}),
    # ("ultimate_oscillator", ["high", "low", "close", 7, 14, 28], {}),
    # ("williams_r", ["high", "low", "close", 14], {}),
    # # Section that tests all the trend indicators
    # ("alligator_bands", ["close", 13, 8, 5], {}),
    # ("bollinger_trend", ["close", 20, 2], {}),
    # ("bollinger_trend_fast_with_ma", ["close", 20, 2], {}),
    # ("breakouts", ["high", "low", 14], {}),
    # ("exponential_moving_average", ["close", 14], {}),
    # ("hull_moving_average", ["close", 14], {}),
    # ("least_squares_moving_average", ["close", 14], {}),
    # ("percent_price_channel", ["high", "low", 20], {}),
    # ("pmax", ["close", "high", "low", 10, 0.65], {}),
    # ("price_channel", ["high", "low", 20], {}),
    # ("range_filter", ["close", 10], {}),
    # ("rolling_moving_average", ["close", 14], {}),
    # ("simple_moving_average", ["close", 14], {}),
    # ("ssl_channels", ["high", "low", 14], {}),
    # ("ssl_channels_atr", ["close", "high", "low", 14], {}),
    # ("t3_average", ["close", 14, 0.7], {}),
    # ("ut_bot", ["close", "high", "low", 10, 2], {}),
    # ("weighted_moving_average", ["close", 14], {}),
    # ("zero_exponential_moving_average", ["close", 14], {}),
    # ("zero_lag_exponential_moving_average", ["close", 14], {}),
    # # Section that tests all the volatility indicators
    # ("average_true_range", ["high", "low", "close", 14], {}),
    # ("bollinger_bands", ["close", 20, 2], {}),
    # ("bbw_expansion", ["close", 20, 2], {}),
    # ("true_range", ["high", "low", "close"], {}),
    # ("keltner_channel", ["close", "high", "low", 20, 2], {}),
    # ("donchian_channel", ["high", "low", 20], {}),
    # ("ulcer_index", ["close", 14], {}),
    # # Section that tests all the volume indicators
    # ("accumulation_distribution_index", ["high", "low", "close", "volume"], {}),
    # ("chaikin_money_flow", ["high", "low", "close", "volume", 20], {}),
    # ("ease_of_movement", ["high", "low", "volume", 14], {}),
    # ("force_index", ["close", "volume", 13], {}),
    # ("money_flow_index", ["high", "low", "close", "volume", 14], {}),
    # ("negative_volume_index", ["close", "volume"], {}),
    # ("on_balance_volume", ["close", "volume"], {}),
    # ("on_balance_volume_oscillator", ["close", "volume", 14], {}),
    # ("positive_volume_index", ["close", "volume"], {}),
    # ("price_volume_trend", ["close", "volume"], {}),
    # ("relative_volume", ["volume", 14], {}),
    # ("time_relative_volume_oscillator", ["volume", 14, "date"], {}),
    # ("volume_weighted_average_price", ["high", "low", "close", "volume"], {}),
    # (
    #     "volume_weighted_average_price_bands",
    #     ["high", "low", "close", "volume", 20, 2.0],
    #     {},
    # ),
    # # Section that tests all the utility indicators
    # ("calculate_atr_stop_loss_take_profit", ["close", "high", "low", 14, 3], {}),
    # ("calculate_stop_loss_take_profit", ["close", "high", "low"], {"percent": 0.03}),
    # ("consecutive_count", ["close"], {"rising": True}),
    # ("cumulative_return", ["close"], {}),
    # ("daily_log_return", ["close"], {}),
    # ("daily_return", ["close"], {}),
    # ("drop_na", [], {}),
    # ("exhaustion_candles", ["open", "high", "low", "close"], {}),
    # ("exhaustion_lengths", ["high", "low", 10], {}),
    # ("first_crossed_above_second", ["close", "open"], {}),
    # ("first_crossed_below_second", ["close", "open"], {}),
    # ("get_min_max", ["close", 14], {}),
    # ("linear_decay", [10], {"start": 1.0, "end": 0.0}),
    # ("linear_growth", [10], {"start": 0.0, "end": 1.0}),
    # ("overbought_oversold", ["close", 70, 30], {}),
    # ("pump_dump_protection", ["close", 48, 1.0], {}),
    # ("regression_slope", ["close", 14], {}),
    # ("same_length", ["close", "open"], {}),
    # ("st_dev", ["close", 14], {}),
    # ("top_percent_change", ["close"], {"length": 14, "top_pct": 80}),
    # ("z_score", ["close", 14], {}),
]

# Run tests
for indicator, args, kwargs in indicators_to_test:
    tester.run_test(indicator, *args, **kwargs)

# Print results
tester.print_results()
