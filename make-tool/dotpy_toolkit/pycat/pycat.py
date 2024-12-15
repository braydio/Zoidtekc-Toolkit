import os
import pyperclip
import argparse

def collect_python_files(directory, include_files=None, skip_files=None, skip_dirs=None):
    """
    Collects specified Python files from the directory.

    Args:
        directory (str): Directory to search for Python files.
        include_files (list of str): List of specific files to include (optional).
        skip_files (list of str): List of specific files to skip (optional).
        skip_dirs (list of str): List of directories to skip (optional).

    Returns:
        list of str: List of full paths to collected Python files.
    """
    absolute_directory = os.path.abspath(directory)
    print(f"pyCatenating scripts in directory: {absolute_directory}")
    python_files = []
    include_files = include_files or []
    skip_files = skip_files or []
    skip_dirs = skip_dirs or []

    # Track which top-level directories are skipped
    skipped_top_dirs = set()

    # Walk through the directory and collect Python files
    for root, dirs, files in os.walk(directory):
        # Skip specified directories
        dirs_to_process = []
        for d in dirs:
            if any(d.startswith(skip_dir.rstrip("/")) for skip_dir in skip_dirs):
                if d not in skipped_top_dirs:
                    skipped_top_dirs.add(d)
                    print(f"Skipping directory: {d}")
            else:
                dirs_to_process.append(d)
        dirs[:] = dirs_to_process

        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)

                # Skip files if specified
                if file in skip_files:
                    continue

                # Include files if specified
                if include_files:
                    if file in include_files:
                        python_files.append(full_path)
                else:
                    python_files.append(full_path)

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
                    output.write(f"# Section {file_path}\n")
                    output.write(file.read())
                    output.write("\n\n")
        print(f"Successfully pyCatenated to {output_file}.")
        return True
    except Exception as e:
        print(f"Error writing files: {e}")
        return False


def append_python_files(directory, output_file, include_files=None, skip_files=None, skip_dirs=None):
    """
    Modular function to collect and write specified Python files to a text file.

    Args:
        directory (str): Path to the directory containing Python files.
        output_file (str): Path to the output text file.
        include_files (list of str): List of specific Python files to include (optional).
        skip_files (list of str): List of specific Python files to skip (optional).
        skip_dirs (list of str): List of directories to skip (optional).

    Returns:
        bool: True if processing is successful, False otherwise.
    """
    python_files = collect_python_files(directory, include_files, skip_files, skip_dirs)
    if not python_files:
        print("No Python files found to process.")
        return False

    return write_files_to_text(python_files, output_file)


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="pyCat CLI for managing Python file concatenation.")
    parser.add_argument("-d", "--dir", default="./", help="Root directory to search for Python files (default: './').")
    parser.add_argument("-o", "--output", default="pyCat-all.txt", help="Output file to save concatenated content (default: 'pyCat-all.txt').")
    parser.add_argument("-i", "--include", nargs="*", help="List of specific Python files to pycat (optional).")
    parser.add_argument("-sf", "--skip-files", nargs="*", help="List of specific Python files to skip (optional).")
    parser.add_argument("-sd", "--skip-dirs", nargs="*", help="List of directories to skip (optional).")
    args = parser.parse_args()

    directory = args.dir
    output_file = args.output
    include_files = args.include
    skip_files = args.skip_files
    skip_dirs = args.skip_dirs

    # Display the working directory
    absolute_directory = os.path.abspath(directory)
    print(f"Starting pyCat in: {absolute_directory}")

    # Concatenate Python files
    success = append_python_files(directory, output_file, include_files, skip_files, skip_dirs)

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
