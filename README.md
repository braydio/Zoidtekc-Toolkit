# Dotpy Toolkit

A collection of Python CLI utilities:

- **pytransfer**: File transfer utility using SCP.
- **pycat**: Utility for appending Python files to a single text file.
- **copydot**: [Brief description of copydot].
- **indexy**: [Brief description of indexy].
- **mappy**: [Brief description of mappy].

## Workflow

# Check if the directory structure is correct
tree make-tool

# Build and install the package
cd make-tool
python -m build
pip install ./dist/dotpy_toolkit-1.0.0-py3-none-any.whl

# Test the CLI tools
indexy --help
pycat
pytransfer

# Add a new tool and integrate it
mv ../mappy.py make-dotpy/
python makedot.py

# Rebuild and test the package
python -m build
pip install ./dist/dotpy_toolkit-1.0.0-py3-none-any.whl
mappy --help


## Installation

Clone the repository and install the toolkit:

```bash
git clone https://github.com/braydio/dotpy-toolkit.git
cd dotpy-toolkit
pip install .
