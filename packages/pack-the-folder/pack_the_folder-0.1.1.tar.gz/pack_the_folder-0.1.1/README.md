# pack__the__folder

A simple Python library to pack the contents of a folder into a single file. Particularly useful when you need to condense multiple text files (including source code) into a single file usable with LLMs that handle large context memories.

## Description

`pack_the_folder` is a Python library that provides a function to:

- Read the structure of a directory (including nested subdirectories) without file names.
- Append the content of each file in the directory to the output file, preceded by a comment with the full path of the file.
- Support a list of allowed file extensions to include.
- Handle deeply nested folder structures.

## Installation

Clone the GitHub repository:

```bash
git clone https://github.com/ltoscano/pack_the_folder.git
```

Or install via pip:

```bash
pip install pack_the_folder
```

## Features

- Packs the contents of a folder, including all subdirectories, into a single file.
- Provides a clear "Folder Tree" visualization at the beginning of the output file.
- Separates the folder structure from file contents in the output for better readability.
- Supports filtering of files based on their extensions.
- Handles multiple file encodings (UTF-8, Latin-1, UTF-16).
- Defaults to including only Python files (`.py`) if no extensions are specified.
- Provides clear structure visualization with indentation for nested directories.
- Gracefully handles binary files.

## Usage

```python
from pack_the_folder import pack_the_folder

# Pack only Python files (default behavior)
pack_the_folder('input_directory', 'output.txt')

# Pack all files
pack_the_folder('input_directory', 'output.txt', allowed_extensions=[])

# Pack only specific file types
pack_the_folder('input_directory', 'output.txt', allowed_extensions=['.py', '.txt', '.md'])
```

## Example

Suppose we have the following directory structure:

```
input_folder/
├── main.py
├── config.txt
├── subfolder1/
│   └── helper.py
└── subfolder2/
    ├── data.csv
    └── notes.md
```

If we run:

```python
pack_the_folder('input_folder', 'output.txt', allowed_extensions=['.py', '.txt', '.md'])
```

The `output.txt` file will contain:

```
Folder Tree:
===========

input_folder/
    subfolder1/
    subfolder2/

File Contents:
==============

# input_folder/main.py
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()

# input_folder/config.txt
# Configuration file
DEBUG=True
LOG_LEVEL=INFO

# input_folder/subfolder1/helper.py
def helper_function():
    return "I'm helping!"

# input_folder/subfolder2/notes.md
# Project Notes

Remember to update the documentation.

```

Note that `data.csv` is not included in the output because it doesn't match the allowed extensions.

## Parameters

- **`input_directory`** *(str)*: The path of the input folder.
- **`output_file`** *(str)*: The full path of the output file.
- **`allowed_extensions`** *(list, optional)*: List of allowed file extensions. If not specified, defaults to `['.py']`. If an empty list is provided, all files will be included.

## License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for more details.
