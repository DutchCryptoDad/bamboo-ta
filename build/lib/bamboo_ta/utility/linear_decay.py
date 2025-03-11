# -*- coding: utf-8 -*-
# linear_decay.py


def linear_decay(
    start: float, end: float, start_time: int, end_time: int, trade_time: int
) -> float:
    """
    Simple linear decay function. Decays from start to end after
    end_time minutes (starts after start_time minutes).

    Parameters:
    - start (float): Starting value.
    - end (float): Ending value.
    - start_time (int): Start time in minutes.
    - end_time (int): End time in minutes.
    - trade_time (int): Current trade time in minutes.

    Call with:
        decayed_value = linear_decay(start, end, start_time, end_time, trade_time)

    Returns:
    - float: Decayed value.
    """
    time = max(0, trade_time - start_time)
    rate = (start - end) / (end_time - start_time)
    return max(end, start - (rate * time))


linear_decay.__doc__ = """
Name:
    Linear Decay

Description:
    A utility function that calculates a linear decay from a starting value to an ending value
    over a specified time period. The decay begins after the start_time and reaches the end value
    at end_time. This is particularly useful for time-based parameter adjustments in trading
    strategies, such as gradually reducing position sizes, dynamically adjusting stop-loss levels,
    or implementing time-based risk management.

More info:
    Linear decay follows the equation: 
    value = start - (start-end)/(end_time-start_time) * (current_time-start_time)
    
    The function ensures that:
    1. Decay starts only after start_time (returns start value before that)
    2. Value never goes below the end value

Parameters:
    - start (float): The starting value
    - end (float): The target end value (must be less than or equal to start)
    - start_time (int): The time (in minutes) when decay should begin
    - end_time (int): The time (in minutes) when decay should complete
    - trade_time (int): The current time (in minutes)

Call with:
    # Example: Decay a stop-loss from 2% to 1% between 30 and 120 minutes of a trade
    current_sl = bta.linear_decay(2.0, 1.0, 30, 120, minutes_in_trade)

Returns:
    float: The decayed value at the given trade_time
"""


def test():
    """
    Test function for the linear_decay indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the linear_decay indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(linear_decay)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
