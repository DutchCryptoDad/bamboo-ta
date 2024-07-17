import os
import fnmatch

def list_files(startpath, exclude_dirs=None, exclude_files=None):
    if exclude_dirs is None:
        exclude_dirs = []
    if exclude_files is None:
        exclude_files = []

    structure = []
    for root, dirs, files in os.walk(startpath):
        # Exclude directories
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(os.path.join(root, d), pattern) for pattern in exclude_dirs)]
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        structure.append(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            # Exclude files
            if not any(fnmatch.fnmatch(os.path.join(root, f), pattern) for pattern in exclude_files):
                structure.append(f"{subindent}{f}")
                with open(os.path.join(root, f), 'r') as file_content:
                    try:
                        content = file_content.read()
                        structure.append(f"\n{subindent}----- Start of {f} -----\n")
                        structure.append(f"{content}")
                        structure.append(f"{subindent}----- End of {f} -----\n")
                    except:
                        structure.append(f"{subindent}Contents of {f}:\n{subindent}Unable to read file.\n")
    return structure

def create_directory_overview(startpath, exclude_dirs=None, exclude_files=None):
    if exclude_dirs is None:
        exclude_dirs = []
    if exclude_files is None:
        exclude_files = []

    overview = ["## Project Structure\n", "The project is organized into the following directories:\n", "```\n"]
    for root, dirs, files in os.walk(startpath):
        # Exclude directories
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(os.path.join(root, d), pattern) for pattern in exclude_dirs)]
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * level + "├── " if level > 0 else ""
        overview.append(f"{indent}{os.path.basename(root)}/\n")
        subindent = '│   ' * (level + 1) + "├── "
        for i, d in enumerate(dirs):
            overview.append(f"{subindent}{d}/\n")
        for f in files:
            # Exclude files
            if not any(fnmatch.fnmatch(os.path.join(root, f), pattern) for pattern in exclude_files):
                file_indent = '│   ' * (level + 1) + "└── "
                overview.append(f"{file_indent}{f}\n")
    overview.append("```\n")
    return overview

def save_structure_to_file(startpath, output_file, exclude_dirs=None, exclude_files=None):
    structure = list_files(startpath, exclude_dirs, exclude_files)
    overview = create_directory_overview(startpath, exclude_dirs, exclude_files)
    with open(output_file, 'w') as f:
        for line in overview:
            f.write(line)
        f.write("\nDetailed File Contents:\n\n")
        for line in structure:
            f.write(line + '\n')

if __name__ == "__main__":
    startpath = '.'  # Current directory
    output_file = 'directory_structure.txt'
    
    # Specify directories and files to exclude with wildcards
    exclude_dirs = ['*__pycache__*', './bamboo_ta.egg-info', './build', './dist', './.git', './images']
    exclude_files = ['./BTC_USDT-1d.json', './__init__.py*', './README*', './LICENSE', './**/*.log', '*/.gitignore' , './test.py', './custom_indicators.py', './legendary_ta.py', './fetchproject.py', './directory_structure.txt' ]
    
    save_structure_to_file(startpath, output_file, exclude_dirs, exclude_files)
    print(f"Directory structure and contents saved to {output_file}")

"""
GPT Prompt:
1. You are a developer with extensive knowledge of Python and Pinescript. You have this project where you are converting Pinscripts into Python functions so that you can use these in a library for further data analysis in python. The project structure and code of the Python code will follow. After that wait for further instructions about the pinescript to convert. Is that understood?

2. The following pinsecript should be converted into a python function. If this pinescript is depending on other indicators from other libraries (e.g. pandas-ta), do not use that, but instead create additional functions that will take care of the missing indicators. If the indicators are already available in the given project, then use these indicators. Is this clear?

3. Further instructions based on output GPT.

GPT prompt

1. You are a developer with extensive knowledge of Python and Technical Indicators in Trading. You enherited a project where trading technical analsis indicators are programmed in a TA library with Python functions. However you noticed that the previous programmer was very inconsistent in its programming and functions are build in different ways. Your task is to refactor the code so that all the functions have the same building style, input method, calculation method and output method. Also watch for redundant code and if detected solve this too by pointing to the correct funtion.
The project structure and code of the Python code will follow next. After that wait for further instructions about the definitive way each function should be build for consistency.
Is that understood?

2. The code should be refactored into the same format style as previously mentioned. 
Please be extra aware of the naming convention of the functions, the way the descriptions are written, including the "call with:" example and the way the output is provided by means of the df_copy method. Please use the same function style and buildup, inputs and output style, example in the description like "call with" and more from the next example I will provide you next. After this I will provide you with the different modules that have to be refactored.
Is this clear?

3. Here is the example function:

def Waddah_Attar_Explosion(df, sensitivity=150, fast_length=20, slow_length=40, channel_length=20, mult=2.0):
   '''
    Waddah Attar Explosion Indicator

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'open', 'high', 'low', and 'close'.
    - sensitivity (int): Sensitivity factor for the indicator. Default is 150.
    - fast_length (int): Length for the fast EMA. Default is 20.
    - slow_length (int): Length for the slow EMA. Default is 40.
    - channel_length (int): Length for the Bollinger Bands. Default is 20.
    - mult (float): Standard deviation multiplier for the Bollinger Bands. Default is 2.0.

    Call with:
        WAE = bta.Waddah_Attar_Explosion(df)
        df['trend_up'] = WAE['trend_up']
        df['trend_down'] = WAE['trend_down']
        df['explosion_line'] = WAE['explosion_line']
        df['dead_zone_line'] = WAE['dead_zone_line']

    Returns:
    - pd.DataFrame: DataFrame with 'trend_up', 'trend_down', 'explosion_line', and 'dead_zone_line' columns.
    '''
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['open', 'high', 'low', 'close']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # print("DataFrame columns:", df.columns)  # Debug print
    # print("First few rows of the DataFrame:\n", df.head())  # Debug print

    # Calculate DEAD_ZONE
    dead_zone = RMA(TR(df), 100) * 3.7
    # print("DEAD_ZONE calculated")  # Debug print

    # Calculate MACD
    macd_fast = EMA(df, 'close', fast_length)
    macd_slow = EMA(df, 'close', slow_length)
    macd_diff = macd_fast - macd_slow
    t1 = (macd_diff - macd_diff.shift(1)) * sensitivity
    # print("MACD and t1 calculated")  # Debug print

    # Calculate Bollinger Bands
    bb = BollingerBands(df, column='close', period=channel_length, std_dev=mult)
    e1 = bb['BB_upper'] - bb['BB_lower']
    # print("Bollinger Bands calculated")  # Debug print

    trend_up = np.where(t1 >= 0, t1, 0)
    trend_down = np.where(t1 < 0, -t1, 0)

    df_copy['trend_up'] = trend_up.round(2)
    df_copy['trend_down'] = trend_down.round(2)
    df_copy['explosion_line'] = e1.round(2)
    df_copy['dead_zone_line'] = dead_zone.round(2)

    return df_copy[['trend_up', 'trend_down', 'explosion_line', 'dead_zone_line']]


GPT Prompt:
1. You are a developer with extensive knowledge of Python and Technical Indicators in Trading. You have this project where you are converting Third party Python code into your own TA library with Python functions so that you can use these within your own library in a consequent and familiar way for further data analysis in python. The project structure and code of the Python code will follow. After that wait for further instructions about the third party Python code to convert. Is that understood?

2. The following third party python should be converted into the same format as my own functions  and should also be added to their consequitive modules. Please check first if they already exist, if they do, then ignore these (but say that you will not create these). If the third party Python code is depending on other libraries (e.g. pandas-ta), do not use these external libraries, but instead create additional functions that will take care of the missing functions or indicators. If these dependend functions alreaty exist in your own project, then use those instead. Please be extra aware of the naming convention of these functions, the way the descriptions are written, including the "call with:" example and the way the output is provided by means of the df_copy method. 

3. Further instructions based on output GPT.


GPT Prompt:
1. I have a Readme file that is part of a complete python programm. It contains the descriptions of functions that are in the submoduled. However I have added more functions to these modules and I would like to recreate this Readme section so that it also contains the added funtions. In other words the Readme file is updated with the most current situation. 

I can give you the current modules Readme section now and later the complete contents of all other modules so that you can update the Readme section with this. Do you understand?


1. I now have a competely different question concerning the Readme file I have for this modules library. Can you help me with this too?


2. The original Readme file looks like this, but it now misses a lot of new functions we added to the different modules. Please rewrite this section with the information I give you in the next prompt. There you should extract the functions from the modules and add these to the Readme section in the same original style. Do you understand?

This is the original Readme section:

3. Further instructions based on output GPT.

"""
