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


GPT Prompt:
1. You are a developer with extensive knowledge of Python and Technical Indicators in Trading. You have this project where you are converting Third party Python code into your own TA library with Python functions so that you can use these within your own library in a consequent and familiar way for further data analysis in python. The project structure and code of the Python code will follow. After that wait for further instructions about the third party Python code to convert. Is that understood?

2. The following third party python should be converted into the same format as my own functions  and should also be added to their consequitive modules. Please check first if they already exist, if they do, then ignore these (but say that you will not create these). If the third party Python code is depending on other libraries (e.g. pandas-ta), do not use these external libraries, but instead create additional functions that will take care of the missing functions or indicators. If these dependend functions alreaty exist in your own project, then use those instead. Is this clear?

3. Further instructions based on output GPT.


GPT Prompt:
1. I have a Readme file that is part of a complete python programm. It contains the descriptions of functions that are in the submoduled. However I have added more functions to these modules and I would like to recreate this Readme section so that it also contains the added funtions. In other words the Readme file is updated with the most current situation. 

I can give you the current modules Readme section now and later the complete contents of all other modules so that you can update the Readme section with this. Do you understand?


1. I now have a competely different question concerning the Readme file I have for this modules library. Can you help me with this too?


2. The original Readme file looks like this, but it now misses a lot of new functions we added to the different modules. Please rewrite this section with the information I give you in the next prompt. There you should extract the functions from the modules and add these to the Readme section in the same original style. Do you understand?

This is the original Readme section:

3. Further instructions based on output GPT.

"""
