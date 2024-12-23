# toolkit-dotpy

**toolkit-dotpy** is this collection of Python scripts with cute names and fun features that I made and packaged for use from the command line. These likely exist in some form elsewhere, likely in a more comprehensive and well maintained library - but not these.
 - remember to fix the dotpy_toolkit dir name... 

## Overview

The project includes the following tools:

- **pycat**: Combines and extracts Python files into a single text file. The results are copied to your clipboard.
- **indexy**: Generates an index of functions and sections in a Python file.
- **mappy**: Creates a directory tree map of a given directory, with options to exclude certain folders.
- **makedot**: Integrates new tools into the `dotpy-toolkit` package and repackages existing tools with updates.
- **pyxpress**: Filezilla python and express shipping. srsly.
- **preprocess**: Will slightly process leading up to processing.

## Installation

To install the package:

### Set up a Virtual Environment in /make-tool/

1. Create a virtual environment:
   ```bash
   cd make-tool
   python -m venv .venv
   ```

2. Activate the virtual environment & install dependencies:
   - On Linux/macOS:
     ```bash
     source .venv/bin/activate
     pip install -r requirements.txt
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     pip install -r requirements.txt
     ```

3. Using the installer makedot.py, install makedot.py:
   ```bash
   copy makedot.py make-dotpy/makedot.py
   python makedot.py --remake
   ```
   
4. Now you can run the command directly to the command line. Neat! New tools can be created too!
   ```bash
   copy new-tool.py ./make-tool/make-dotpy/new-tool.py
   makedot
   ```
   Optional Flag `makedot --remake` to remake an existing tool with updates.

## Tools and Usage

### 1. **makedot**

Main script for integrating new tools into the toolkit. It automatically creates sub-packages, updates the `pyproject.toml` file, and increments version numbers.
This script integrates new tools, updates entry points in `pyproject.toml`, and rebuilds the package.

#### How it works:

1. Looks for new Python scripts in the `make-dotpy/` directory.
2. Creates a sub-package in `dotpy_toolkit/` for each new tool.
3. Updates the `pyproject.toml` file with a new CLI entry point for the tool.
4. Rebuilds and installs the updated package.

#### Key functions:

- **find\_python\_files(directory)**: Finds Python files in the specified directory.
- **create\_sub\_package(tool\_name, tool\_file)**: Creates a sub-package for a tool and moves the tool file into it.
- **update\_pyproject\_toml(tool\_name)**: Updates the CLI entry points in `pyproject.toml`.
- **build\_and\_test\_tool()**: Rebuilds and installs the package locally.

#### Example:

```bash
makedot
```

### 2. **pycat**

Combines multiple Python scripts into a single text file and optionally copies the result to the clipboard.

#### Example:

```bash
pycat
```

### 3. **indexy**

Analyzes a Python script and generates an index of functions grouped by sections.

#### Example:

```bash
indexy file.py --json --csv
```

### 4. **mappy**

Creates a visual directory tree map of a folder, excluding specified directories.

#### Example:

```bash
mappy --dir /path/to/dir --exclude __pycache__ .git
```

### 5. **preprocess**

Light processing, usually done before intensive processing.

```bash
preprocess --file /path/to/file.py --output path/outputfile.json
```

## Project Structure

```plaintext
make-tool
├── dist
│   ├── dotpy_toolkit-1.0.0-py3-none-any.whl
│   └── dotpy_toolkit-1.0.0.tar.gz
├── dotpy_toolkit
│   ├── indexy
│   │   ├── __init__.py
│   │   └── indexy.py
│   ├── mappy
│   │   ├── __init__.py
│   │   └── mappy.py
│   ├── pycat
│   │   ├── __init__.py
│   │   └── pycat.py
│   ├── remakedot
│   │   ├── __init__.py
│   │   └── remakedot.py
│   └── makedot.py
├── make-dotpy
├── pyproject.toml
```

## Contributing

1. Clone the repository.
2. Add new tools into the `make-dotpy` directory.
3. Use `makedot.py` to integrate and test the new tool.
4. Submit a pull request with your changes.

## License

This project is licensed under the MIT License.

