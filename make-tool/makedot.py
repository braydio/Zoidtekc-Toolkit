import os
import shutil
import toml

# Define paths
NEW_TOOLS_DIR = "make-dotpy"
PACKAGE_DIR = "dotpy_toolkit"
PYPROJECT_FILE = "pyproject.toml"

# Helper functions
def find_python_files(directory):
    """Find all Python files in the specified directory."""
    return [f for f in os.listdir(directory) if f.endswith(".py")]

def create_sub_package(tool_name, tool_file):
    """Create a sub-package for a tool."""
    tool_package_dir = os.path.join(PACKAGE_DIR, tool_name)
    os.makedirs(tool_package_dir, exist_ok=True)

    # Add __init__.py to mark it as a package
    with open(os.path.join(tool_package_dir, "__init__.py"), "w") as init_file:
        init_file.write(f"__version__ = '1.0.0'\n")

    # Move the tool file into the sub-package
    shutil.move(os.path.join(NEW_TOOLS_DIR, tool_file), os.path.join(tool_package_dir, tool_name + ".py"))
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

def build_and_test_tool():
    """Rebuild and test the package."""
    os.system("pip install --upgrade build")
    os.system("python -m build")
    os.system("pip install .")

def main():
    # Check for new tools in the new-dotpy/ directory
    if not os.path.exists(NEW_TOOLS_DIR):
        print(f"No '{NEW_TOOLS_DIR}' directory found. Exiting.")
        return

    new_tools = find_python_files(NEW_TOOLS_DIR)
    if not new_tools:
        print(f"No Python files found in '{NEW_TOOLS_DIR}'. Exiting.")
        return

    print(f"Found {len(new_tools)} new tools: {', '.join(new_tools)}")

    # Integrate each new tool
    for tool_file in new_tools:
        tool_name = os.path.splitext(tool_file)[0]  # Use file name without extension as tool name
        create_sub_package(tool_name, tool_file)
        update_pyproject_toml(tool_name)

    # Rebuild the package
    print("Rebuilding and testing the updated package...")
    build_and_test_tool()
    print("Integration complete.")

if __name__ == "__main__":
    main()
