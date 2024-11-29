import os


def create_dir_map(directory, exclude_dirs=None, indent="│   ", last_indent="└── "):
    """
    Creates a directory map starting from the given directory.
    Optional exclusion of subdirectories.

    :param directory: The root directory to map.
    :param exclude_dirs: A list of subdirectory names to exclude.
    :param indent: The indentation for subdirectories.
    :param last_indent: The indentation for the last element in a folder.
    :return: A string representation of the directory map.
    """
    exclude_dirs = set(exclude_dirs or [])
    dir_map = []

    def recursive_map(current_dir, prefix=""):
        try:
            entries = [e for e in os.listdir(current_dir) if e not in exclude_dirs]
            entries.sort()
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


# Example usage
if __name__ == "__main__":
    # Specify the root directory of the project
    root_dir = r"./"
    output_file = "mappied.txt"  # Output file name
    exclude = [".venv", "build", "node_modules", "resources", ".git", "__pycache__"]  # Directories to exclude

    if os.path.exists(root_dir):
        # Generate directory map
        directory_map = create_dir_map(root_dir, exclude_dirs=exclude)

        # Write to a text file
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(directory_map)

        print(f"Directory map written to '{output_file}'")
    else:
        print(f"Directory '{root_dir}' does not exist.")
