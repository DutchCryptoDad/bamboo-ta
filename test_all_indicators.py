# -*- coding: utf-8 -*-
# test1.py
"""
This script tests all indicators in the bamboo-ta library using their individual
test functions. It helps identify erroneous indicators quickly and provides
detailed error reports.
"""

import os
import sys
import importlib
import inspect
import time
import traceback
from pathlib import Path
import pandas as pd

def find_indicator_modules():
    """
    Find all indicator modules in the bamboo_ta package.
    
    Returns:
        list: A list of module paths (as strings) for all indicators
    """
    indicator_modules = []
    bamboo_ta_dir = Path(__file__).parent / "bamboo_ta"
    
    # Categories to search
    categories = [
        "candles", "cycles", "momentum", "performance", 
        "statistics", "trend", "utility", "volatility", "volume"
    ]
    
    for category in categories:
        category_dir = bamboo_ta_dir / category
        if not category_dir.is_dir():
            continue
            
        for file_path in category_dir.glob("*.py"):
            if file_path.name.startswith("__"):
                continue
                
            # Convert path to module format
            rel_path = file_path.relative_to(Path(__file__).parent)
            module_path = str(rel_path).replace(os.sep, ".")[:-3]  # Remove .py extension
            indicator_modules.append(module_path)
    
    return indicator_modules

def test_indicator(module_path):
    """
    Test a single indicator by importing its module and calling its test function.
    
    Args:
        module_path (str): The module path of the indicator to test
        
    Returns:
        tuple: (success, error_info) where success is a boolean indicating if the test passed
               and error_info is a dict with error details if the test failed
    """
    try:
        # Import the module
        module = importlib.import_module(module_path)
        
        # Get the indicator name from the module path
        indicator_name = module_path.split('.')[-1]
        
        # Check if it has a test function
        if hasattr(module, 'test') and callable(module.test):
            print(f"\n{'='*80}\nTesting {indicator_name}...\n{'='*80}")
            
            # Get the main indicator function
            indicator_func = None
            for name, obj in inspect.getmembers(module):
                if name == indicator_name and callable(obj):
                    indicator_func = obj
                    break
            
            # Call the test function with error handling
            try:
                # Patch the test_indicator function to capture the result
                original_test_indicator = None
                result = None
                
                if hasattr(module, 'test_indicator'):
                    original_test_indicator = module.test_indicator
                    
                    def patched_test_indicator(func, *args, **kwargs):
                        nonlocal result
                        result = func(*args, **kwargs)
                        if not isinstance(result, pd.DataFrame):
                            raise TypeError(f"{indicator_name} did not return a DataFrame")
                        return result
                    
                    module.test_indicator = patched_test_indicator
                
                # Call the test function
                module.test()
                
                # Restore original test_indicator if it was patched
                if original_test_indicator:
                    module.test_indicator = original_test_indicator
                
                return True, None
                
            except TypeError as e:
                # Handle type errors (common for DataFrame issues)
                return False, {
                    "type": "TypeError",
                    "message": str(e),
                    "indicator": indicator_name,
                    "suggestion": "Ensure the indicator returns a pandas DataFrame"
                }
            except ValueError as e:
                # Handle value errors
                return False, {
                    "type": "ValueError",
                    "message": str(e),
                    "indicator": indicator_name,
                    "suggestion": "Check the input values and parameters"
                }
            except AttributeError as e:
                # Handle attribute errors
                return False, {
                    "type": "AttributeError",
                    "message": str(e),
                    "indicator": indicator_name,
                    "suggestion": "Check for missing attributes or methods"
                }
            except TypeError as e:
                # Handle type errors
                return False, {
                    "type": "TypeError",
                    "message": str(e),
                    "indicator": indicator_name,
                    "suggestion": "Check parameter types and return values"
                }
            except Exception as e:
                # Handle other exceptions
                return False, {
                    "type": type(e).__name__,
                    "message": str(e),
                    "indicator": indicator_name,
                    "traceback": traceback.format_exc(),
                    "suggestion": "Review the error message and traceback"
                }
        else:
            return False, {
                "type": "MissingTestFunction",
                "message": f"No test function found in {module_path}",
                "indicator": indicator_name,
                "suggestion": "Add a test function to the indicator module"
            }
    except Exception as e:
        indicator_name = module_path.split('.')[-1]
        return False, {
            "type": type(e).__name__,
            "message": str(e),
            "indicator": indicator_name,
            "traceback": traceback.format_exc(),
            "suggestion": "Check if the module can be imported correctly"
        }

def analyze_errors(failures):
    """
    Analyze the errors to identify common patterns and provide suggestions.
    
    Args:
        failures (list): List of (module_path, error_info) tuples
        
    Returns:
        dict: Analysis results with error categories and counts
    """
    error_types = {}
    missing_args = {}
    return_type_errors = 0
    
    for module_path, error_info in failures:
        # Count error types
        error_type = error_info.get("type", "Unknown")
        error_types[error_type] = error_types.get(error_type, 0) + 1
        
        # Check for missing arguments
        message = error_info.get("message", "")
        if "missing" in message and "required positional argument" in message:
            indicator = error_info.get("indicator", "unknown")
            missing_args[indicator] = message
        
        # Count return type errors
        if "did not return a DataFrame" in message:
            return_type_errors += 1
    
    return {
        "error_types": error_types,
        "missing_args": missing_args,
        "return_type_errors": return_type_errors
    }

def main():
    """
    Main function to test all indicators and report errors.
    """
    # Find all indicator modules
    indicator_modules = find_indicator_modules()
    
    # Sort modules by category for better organization
    indicator_modules.sort()
    
    print(f"Found {len(indicator_modules)} indicator modules to test.")
    
    # Test each indicator
    results = {
        "success": [],
        "failure": []
    }
    
    for i, module_path in enumerate(indicator_modules, 1):
        print(f"\nTesting indicator {i}/{len(indicator_modules)}: {module_path}")
        success, error_info = test_indicator(module_path)
        
        if success:
            results["success"].append(module_path)
        else:
            results["failure"].append((module_path, error_info))
        
        # Add a small delay to avoid overwhelming the console output
        time.sleep(0.1)
    
    # Print summary
    print("\n" + "="*80)
    print(f"TESTING COMPLETE: {len(results['success'])}/{len(indicator_modules)} indicators passed")
    print("="*80)
    
    if results["failure"]:
        # Analyze errors
        error_analysis = analyze_errors(results["failure"])
        
        print("\nERROR ANALYSIS:")
        print(f"  - Total failures: {len(results['failure'])}")
        
        print("\nError types:")
        for error_type, count in error_analysis["error_types"].items():
            print(f"  - {error_type}: {count} occurrences")
        
        if error_analysis["return_type_errors"] > 0:
            print(f"\nReturn type errors: {error_analysis['return_type_errors']} indicators")
            print("  These indicators are not returning a pandas DataFrame as required.")
        
        if error_analysis["missing_args"]:
            print("\nMissing arguments errors:")
            for indicator, message in error_analysis["missing_args"].items():
                print(f"  - {indicator}: {message}")
        
        print("\nDETAILED ERROR REPORT:")
        for module_path, error_info in results["failure"]:
            indicator = error_info.get("indicator", module_path.split('.')[-1])
            error_type = error_info.get("type", "Unknown")
            message = error_info.get("message", "No error message")
            suggestion = error_info.get("suggestion", "No suggestion available")
            
            print(f"\n{indicator} ({module_path}):")
            print(f"  Error type: {error_type}")
            print(f"  Message: {message}")
            print(f"  Suggestion: {suggestion}")
            
            # Print traceback for complex errors
            if "traceback" in error_info and error_type not in ["MissingTestFunction", "TypeError"]:
                print("\n  Traceback:")
                for line in error_info["traceback"].split("\n"):
                    print(f"    {line}")
    else:
        print("\nAll indicators passed their tests!")
    
    # Return exit code based on test results
    return 1 if results["failure"] else 0

if __name__ == "__main__":
    sys.exit(main())
