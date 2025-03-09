# -*- coding: utf-8 -*-
# indicator_test_template.py
"""
This file contains a template for adding test functions to indicator files.
Copy and paste the test function below into your indicator file, replacing
'your_indicator_function' with the name of your indicator function.
"""

def test():
    """
    Test function for the your_indicator_function indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the your_indicator_function indicator.
    
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
        test_indicator(your_indicator_function)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 