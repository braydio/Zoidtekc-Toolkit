import os
import argparse


def create_dir_map(directory, exclude_dirs=None, indent="│   ", last_indent="└── ", warn_threshold=50):
    """
    Creates a directory map starting from the given directory.
    Optional exclusion of subdirectories.

    :param directory: The root directory to map.
    :param exclude_dirs: A list of subdirectory names to exclude.
    :param indent: The indentation for subdirectories.
    :param last_indent: The indentation for the last element in a folder.
    :param warn_threshold: Maximum number of files allowed in a directory before showing a warning.
    :return: A string representation of the directory map.
    """
    exclude_dirs = set(exclude_dirs or [])
    dir_map = []

    def recursive_map(current_dir, prefix=""):
        try:
            entries = [e for e in os.listdir(current_dir) if e not in exclude_dirs]
            entries.sort()
            
            # Warn if directory has too many files
            if len(entries) > warn_threshold:
                print(f"Warning: Directory '{current_dir}' contains {len(entries)} files.")

            for i, entry in enumerate(entries):
                path = os.path.join(current_dir, entry)
                is_last = i == len(entries) - 1
                connector = last_indent if is_last else "├── "
                dir_map.append(f"{prefix}{connector}{entry}")
                if os.path.isdir(path):
                    next_prefix = prefix + (indent if not is_last else "    ")
                    recursive_map(path, next_prefix)
        except PermissionError:
            dir_map.append(
                f"{prefix}{last_indent if prefix else ''}{current_dir} [Access Denied]"
            )
        except FileNotFoundError:
            dir_map.append(
                f"{prefix}{last_indent if prefix else ''}{current_dir} [Not Found]"
            )

    recursive_map(directory)
    return "\n".join(dir_map)


def main():
    # CLI argument parser
    parser = argparse.ArgumentParser(description="Create a directory map.")
    parser.add_argument("--dir", default="./", help="Root directory to map (default: './').")
    parser.add_argument("--exclude", nargs="*", default=[".venv", "build", "node_modules", ".git", "__pycache__"],
                        help="List of directories to exclude (default: ['.venv', 'build', 'node_modules', '.git', '__pycache__']).")
    parser.add_argument("--warn", type=int, default=50, help="Warn if a directory contains more than this many files (default: 50).")
    parser.add_argument("--output", default="mappied.txt", help="Output file to save the directory map (default: 'mappied.txt').")
    args = parser.parse_args()

    root_dir = args.dir
    exclude_dirs = args.exclude
    warn_threshold = args.warn
    output_file = args.output

    # Check if root directory exists
    if not os.path.exists(root_dir):
        print(f"Error: Directory '{root_dir}' does not exist.")
        return

    # Generate directory map
    print(f"Generating directory map for '{root_dir}' (excluding: {exclude_dirs})...")
    directory_map = create_dir_map(root_dir, exclude_dirs=exclude_dirs, warn_threshold=warn_threshold)

    # Write to output file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(directory_map)

    print(f"Directory map written to '{output_file}'")


if __name__ == "__main__":
    main()
