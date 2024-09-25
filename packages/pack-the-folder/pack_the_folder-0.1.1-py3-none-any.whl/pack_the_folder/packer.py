import os

def pack_the_folder(input_directory, output_file, allowed_extensions=None, excluded_folders=None):
    """
    Pack the contents of a folder into a single file.
    This function walks through the input directory, including all subdirectories,
    and writes their structure and file contents to the output file. It can filter
    files based on their extensions and handles different file encodings.

    Args:
    input_directory (str): Path to the directory to be packed.
    output_file (str): Path where the output file will be created.
    allowed_extensions (list, optional): List of file extensions to include.
        If None, defaults to ['.py']. If an empty list, includes all files.
    excluded_folders (list, optional): List of additional folder names to exclude.
        __pycache__ is always excluded regardless of this list.

    The function tries multiple encodings when reading files:
    1. UTF-8 (default for most text files)
    2. Latin-1 (covers all 256 possible byte values)
    3. UTF-16 (for Unicode files that use 2-byte encoding)
    If all encoding attempts fail, the file is treated as binary and its content is not included.
    """
    # Set default allowed extensions to ['.py'] if None is provided
    if allowed_extensions is None:
        allowed_extensions = ['.py']
    
    # Ensure __pycache__ is always in the list of excluded folders
    if excluded_folders is None:
        excluded_folders = []
    excluded_folders = set(excluded_folders + ['__pycache__'])

    # List of encodings to try, in order of preference
    encodings_to_try = ['utf-8', 'latin-1', 'utf-16']

    with open(output_file, 'w', encoding='utf-8') as out_file:
        # Write the "Folder Tree" title
        out_file.write("Folder Tree:\n")
        out_file.write("="*11 + "\n\n")  # Underline for emphasis

        # Write the directory structure (without file names)
        for root, dirs, files in os.walk(input_directory):
            # Remove excluded folders from dirs to prevent os.walk from traversing them
            dirs[:] = [d for d in dirs if d not in excluded_folders]

            # Calculate the depth of the current directory
            level = root.replace(input_directory, '').count(os.sep)
            # Create indentation based on directory depth
            indent = ' ' * 4 * level
            # Write the current directory name
            out_file.write('{}{}/\n'.format(indent, os.path.basename(root)))

        # Add a separator between the folder tree and file contents
        out_file.write("\nFile Contents:\n")
        out_file.write("="*14 + "\n\n")

        # Append the content of the files
        for root, dirs, files in os.walk(input_directory):
            # Remove excluded folders from dirs to prevent os.walk from traversing them
            dirs[:] = [d for d in dirs if d not in excluded_folders]

            for file in files:
                # Check if the file extension is allowed
                if allowed_extensions and not any(file.endswith(ext) for ext in allowed_extensions):
                    continue
                full_path = os.path.join(root, file)
                out_file.write('\n# {}\n'.format(full_path))

                # Try to read the file with different encodings
                file_content = None
                for encoding in encodings_to_try:
                    try:
                        with open(full_path, 'r', encoding=encoding) as f:
                            file_content = f.read()
                        break  # If successful, exit the encoding loop
                    except UnicodeDecodeError:
                        continue  # Try the next encoding

                if file_content is not None:
                    # Write the file content if successfully read
                    out_file.write(file_content)
                else:
                    # If all encoding attempts fail, treat as binary
                    out_file.write('(binary file, content not included)\n')

# Example usage
if __name__ == "__main__":
    pack_the_folder('input_directory', 'output.txt', excluded_folders=['temp', 'logs'])
