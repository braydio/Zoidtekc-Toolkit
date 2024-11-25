
# -- Dependent Code before # can be saved externally and imported

import os

def collect_python_files(directory, include_files=None):
    """
    Collects specified Python files from the directory.

    Args:
        directory (str): Directory to search for Python files.
        include_files (list of str): List of specific files to include (optional).

    Returns:
        list of str: List of full paths to collected Python files.
    """
    print(f"pyCatenating scripts in {directory}.")
    python_files = []
    include_files = include_files or []

    # Walk through the directory and collect Python files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and (not include_files or file in include_files):
                python_files.append(os.path.join(root, file))
    return python_files


def write_files_to_text(file_paths, output_file):
    """
    Writes the content of collected Python files to a text file.

    Args:
        file_paths (list of str): List of Python file paths to write.
        output_file (str): Output text file to write the content to.

    Returns:
        bool: True if writing is successful, False otherwise.
    """
    try:
        with open(output_file, 'w') as output:
            for file_path in file_paths:
                with open(file_path, 'r') as file:
                    output.write(f"# Content from {file_path}\n")
                    output.write(file.read())
                    output.write("\n\n")
        print(f"Successfully pyCatenated to {output_file}.")
        return True
    except Exception as e:
        print(f"Error writing files: {e}")
        return False


def append_python_files(directory, output_file, include_files=None):
    """
    Modular function to collect and write specified Python files to a text file.

    Args:
        directory (str): Path to the directory containing Python files.
        output_file (str): Path to the output text file.
        include_files (list of str): List of specific Python files to include (optional).

    Returns:
        bool: True if processing is successful, False otherwise.
    """
    python_files = collect_python_files(directory, include_files)
    if not python_files:
        print("No Python files found to process.")
        return False

    return write_files_to_text(python_files, output_file)


# Dependent code appended above ^
# from processor.add_files import append_python_files

import pyperclip

def main():
    directory = "./"  # Directory to search
    output_file = "pyCat-all.txt"  # Output file name
    include_files = ["review_for_submit.py"]  # Files to include

    # Combine Python files
    success = append_python_files(directory, output_file, include_files)

    # If successful, copy to clipboard
    if success:
        try:
            with open(output_file, 'r') as output:
                content = output.read()
                pyperclip.copy(content)  # Copy content to clipboard
                print(f"Copy {output_file} to clipboard: Success.")
        except Exception as e:
            print(f"Error reading file for clipboard copy: {e}")
    else:
        print("Failed to process files.")

if __name__ == "__main__":
    main()
