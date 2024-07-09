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
    exclude_files = ['./BTC_USDT-1d.json', './__init__.py*', './README*', './LICENSE', './**/*.log', '*/.gitignore' , './test.py']
    
    save_structure_to_file(startpath, output_file, exclude_dirs, exclude_files)
    print(f"Directory structure and contents saved to {output_file}")

"""
GPT Prompt:
1. You are a developer with extensive knowledge of Python and Pinescript. You have this project where you are converting Pinscripts into Python functions so that you can use these in a library for further data analysis in python. The project structure and code of the Python code will follow. After that wait for further instructions about the pinescript to convert. Is that understood?

2. The following pinsecript should be converted into a python function. If this pinescript is depending on other indicators from other libraries (e.g. pandas-ta), do not use that, but instead create additional functions that will take care of the missing indicators. If the indicators are already available in the given project, then use these indicators. Is this clear?

3. Further instructions based on output GPT.

"""
