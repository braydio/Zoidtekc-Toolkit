import os

def collect_python_files(directory, skip_subdirs=None):
    """
    Collects the paths of all Python files in a directory, optionally skipping specified subdirectories.

    Args:
        directory (str): Path to the directory to search.
        skip_subdirs (list of str): Names of subdirectories to skip (optional).

    Returns:
        list of str: List of Python file paths.
    """
    print(f"Initialized Unify in {directory}.")
    python_files = []
    skip_subdirs = skip_subdirs or []

    for subdir in skip_subdirs:
        print(f"Unifier: Unify skip {subdir}.")
    
    for root, dirs, files in os.walk(directory):
        # Skip specified subdirectories
        dirs[:] = [d for d in dirs if d not in skip_subdirs]

        for file in files:
            print(f"Unifier: Unify file {file}?")
            if file.endswith('.py'):
                print(f"Yes, Unify file {file}.")
                python_files.append(os.path.join(root, file))
    return python_files

def write_files_to_text(file_paths, output_file):
    """
    Writes the content of a list of files to a single text file.

    Args:
        file_paths (list of str): List of file paths to write.
        output_file (str): Path to the output text file.
    """
    try:
        with open(output_file, 'w') as output:
            for file_path in file_paths:
                with open(file_path, 'r') as file:
                    output.write(f"# Content from {file_path}\n")
                    output.write(file.read())
                    output.write("\n\n")  # Separate files with newlines
        print(f"Files have been successfully written to {output_file}.")
    except Exception as e:
        print(f"An error occurred while writing to {output_file}: {e}")

# Example usage
def append_python_files(directory, output_file, skip_directory=None):
    """
    Modular function to collect and write Python files to a text file.

    Args:
        directory (str): Path to the directory containing Python files.
        output_file (str): Path to the output text file.
        skip_subdirs (list of str): List of subdirectories to skip (optional).
    """
    python_files = collect_python_files(directory, skip_directory)
    print(python_files)
    write_files_to_text(python_files, output_file)
