# -*- coding: utf-8 -*-
# test_indicators.py
"""
This script demonstrates how to use the test_indicator function to test
any indicator in the bamboo-ta library.
"""

import bamboo_ta.bamboo_ta as bta
import sys

def main():
    """
    Main function to test indicators based on command line arguments.
    
    Usage:
        python test_indicators.py [indicator_name] [timeframe]
        
    Examples:
        python test_indicators.py dynamic_exhaustion_bars 1d
        python test_indicators.py heiken_ashi 4h
        python test_indicators.py relative_strength_index 1h
    """
    # Get command line arguments
    args = sys.argv[1:]
    
    if not args:
        print("Please provide an indicator name to test.")
        print("Usage: python test_indicators.py [indicator_name] [timeframe]")
        print("\nAvailable indicators:")
        
        # List all available indicators
        indicators = [name for name in dir(bta) if callable(getattr(bta, name)) and not name.startswith('_')]
        for indicator in sorted(indicators):
            print(f"  - {indicator}")
        return
    
    # Get indicator name from command line arguments
    indicator_name = args[0]
    
    # Get timeframe from command line arguments (default to 1d)
    timeframe = args[1] if len(args) > 1 else "1d"
    
    # Check if the indicator exists
    if not hasattr(bta, indicator_name) or not callable(getattr(bta, indicator_name)):
        print(f"Error: Indicator '{indicator_name}' not found in bamboo_ta.")
        return
    
    # Get the indicator function
    indicator_func = getattr(bta, indicator_name)
    
    # Test the indicator
    bta.test_indicator(indicator_func, timeframe)

if __name__ == "__main__":
    main() 