# -*- coding: utf-8 -*-
# add_test_functions.py
"""
This script adds test functions to all indicator files in the bamboo-ta library.
It scans all Python files in the bamboo_ta directory and its subdirectories,
and adds a test function to each file that contains an indicator function.
"""

import os
import re
import sys

def get_indicator_files(root_dir):
    """
    Get all Python files in the bamboo_ta directory and its subdirectories.
    
    Args:
        root_dir (str): The root directory to search in
        
    Returns:
        list: A list of Python file paths
    """
    indicator_files = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.py') and not filename.startswith('__'):
                file_path = os.path.join(dirpath, filename)
                indicator_files.append(file_path)
    
    return indicator_files

def get_indicator_function_name(file_path):
    """
    Extract the main indicator function name from a Python file.
    
    Args:
        file_path (str): The path to the Python file
        
    Returns:
        str: The name of the main indicator function, or None if not found
    """
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Look for function definitions
    function_pattern = r'def\s+([a-zA-Z0-9_]+)\s*\('
    matches = re.findall(function_pattern, content)
    
    if not matches:
        return None
    
    # Assume the first function is the main indicator function
    # This is a simplification and might not work for all files
    return matches[0]

def add_test_function(file_path, indicator_name):
    """
    Add a test function to a Python file.
    
    Args:
        file_path (str): The path to the Python file
        indicator_name (str): The name of the indicator function
        
    Returns:
        bool: True if the test function was added, False otherwise
    """
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if the file already has a test function
    if 'def test(' in content:
        print(f"File {file_path} already has a test function.")
        return False
    
    # Create the test function with proper triple quotes
    test_function = f'''

def test():
    """
    Test function for the {indicator_name} indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the {indicator_name} indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator({indicator_name})
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {{e}}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
'''
    
    # Add the test function to the file
    with open(file_path, 'a') as f:
        f.write(test_function)
    
    print(f"Added test function to {file_path}")
    return True

def main():
    """
    Main function to add test functions to all indicator files.
    
    Usage:
        python add_test_functions.py [bamboo_ta_dir]
    """
    # Get the bamboo_ta directory from command line arguments or use default
    bamboo_ta_dir = sys.argv[1] if len(sys.argv) > 1 else 'bamboo_ta'
    
    if not os.path.isdir(bamboo_ta_dir):
        print(f"Error: Directory '{bamboo_ta_dir}' not found.")
        return
    
    # Get all indicator files
    indicator_files = get_indicator_files(bamboo_ta_dir)
    
    # Add test functions to all indicator files
    added_count = 0
    for file_path in indicator_files:
        indicator_name = get_indicator_function_name(file_path)
        
        if indicator_name:
            if add_test_function(file_path, indicator_name):
                added_count += 1
    
    print(f"Added test functions to {added_count} files.")

if __name__ == "__main__":
    main() 