import os
import shutil
import toml
import argparse

# Define paths
NEW_TOOLS_DIR = "make-dotpy"
PACKAGE_DIR = "dotpy_toolkit"
PYPROJECT_FILE = "pyproject.toml"

# Helper functions
def find_python_files(directory):
    """Find all Python files in the specified directory."""
    return [f for f in os.listdir(directory) if f.endswith(".py")]

def create_sub_package(tool_name, tool_file, source_dir):
    """Create a sub-package for a tool."""
    tool_package_dir = os.path.join(PACKAGE_DIR, tool_name)
    os.makedirs(tool_package_dir, exist_ok=True)

    # Add __init__.py to mark it as a package
    init_file_path = os.path.join(tool_package_dir, "__init__.py")
    if not os.path.exists(init_file_path):
        with open(init_file_path, "w") as init_file:
            init_file.write(f"__version__ = '1.0.0'\n")
    shutil.move(os.path.join(source_dir, tool_file), os.path.join(tool_package_dir, tool_name + ".py"))
    print(f"Integrated tool '{tool_name}' into the '{tool_package_dir}' package.")

def update_pyproject_toml(tool_name):
    """Update the pyproject.toml file with the new tool's entry point."""
    with open(PYPROJECT_FILE, "r") as file:
        pyproject_data = toml.load(file)

    # Add the tool's script entry point
    script_entry = f"{PACKAGE_DIR}.{tool_name}.{tool_name}:main"
    pyproject_data["project"]["scripts"][tool_name] = script_entry

    with open(PYPROJECT_FILE, "w") as file:
        toml.dump(pyproject_data, file)

    print(f"Updated pyproject.toml with entry point for '{tool_name}'.")

def increment_version():
    """Increment the version number in pyproject.toml."""
    with open(PYPROJECT_FILE, "r") as file:
        pyproject_data = toml.load(file)

    current_version = pyproject_data["project"]["version"]
    major, minor, patch = map(int, current_version.split("."))
    new_version = f"{major}.{minor}.{patch + 1}"
    pyproject_data["project"]["version"] = new_version

    with open(PYPROJECT_FILE, "w") as file:
        toml.dump(pyproject_data, file)

    print(f"Main project version updated: {current_version} -> {new_version}")

def increment_tool_version(tool_name):
    """Increment the version number for a specific tool."""
    init_file_path = os.path.join(PACKAGE_DIR, tool_name, "__init__.py")
    if not os.path.exists(init_file_path):
        print(f"No __init__.py found for tool '{tool_name}'. Skipping version increment.")
        return

    with open(init_file_path, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.startswith("__version__"):
            current_version = line.split("=")[-1].strip().strip("'")
            major, minor, patch = map(int, current_version.split("."))
            new_version = f"{major}.{minor}.{patch + 1}"
            lines[i] = f"__version__ = '{new_version}'\n"
            print(f"Tool '{tool_name}' version updated: {current_version} -> {new_version}")
            break

    with open(init_file_path, "w") as file:
        file.writelines(lines)

def build_and_test_tool():
    """Rebuild and test the package."""
    os.system("pip install --upgrade build")
    os.system("python -m build")
    os.system("pip install .")

def process_tool(tool_name, source_dir, increment_tool_version_flag=True):
    """Process a single tool."""
    tool_file = f"{tool_name}.py"
    if not os.path.exists(os.path.join(source_dir, tool_file)):
        print(f"Python file '{tool_file}' not found in '{source_dir}'. Exiting.")
        return False

    create_sub_package(tool_name, tool_file, source_dir)
    update_pyproject_toml(tool_name)

    if increment_tool_version_flag:
        increment_tool_version(tool_name)
    return True

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Tool integrator for dotpy-toolkit.")
    parser.add_argument("-r", "--remake", help="Specify a tool to update directly.", nargs="?", const=True)
    parser.add_argument("-v", "--version-up", help="Increment version (default: skip)", action="store_true")
    args = parser.parse_args()

    # Determine behavior based on flags
    increment_main_version = args.inc_vers

    if args.remake:
        if args.remake is True:
            # Prompt the user if tool name is not provided
            tool_name = input("Enter the command name to update (e.g., 'mytool'): ").strip()
        else:
            tool_name = args.remake

        source_dir = os.path.join(PACKAGE_DIR, tool_name)
        print(f"Processing tool '{tool_name}' from '{source_dir}'...")
        if not os.path.exists(source_dir):
            print(f"Tool '{tool_name}' not found in '{PACKAGE_DIR}'. Exiting.")
            return

        if process_tool(tool_name, source_dir, increment_tool_version_flag=increment_main_version):
            print(f"Tool '{tool_name}' processed successfully.")
    else:
        # Default behavior for processing tools in make-dotpy
        if not os.path.exists(NEW_TOOLS_DIR):
            print(f"No '{NEW_TOOLS_DIR}' directory found. Exiting.")
            return

        new_tools = find_python_files(NEW_TOOLS_DIR)
        if not new_tools:
            print(f"No Python files found in '{NEW_TOOLS_DIR}'. Exiting.")
            return

        print(f"Found {len(new_tools)} new tools: {', '.join(new_tools)}")
        for tool_file in new_tools:
            tool_name = os.path.splitext(tool_file)[0]
            if process_tool(tool_name, NEW_TOOLS_DIR, increment_tool_version_flag=increment_main_version):
                print(f"Tool '{tool_name}' processed successfully.")

    if increment_main_version:
        increment_version()

    # Rebuild the package
    print("Rebuilding and testing the updated package...")
    build_and_test_tool()
    print("Integration complete.")
