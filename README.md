# dotpy-toolkit

**dotpy-toolkit** is a Python-based utility collection designed to make life easier for developers and system administrators. It contains multiple tools for working with files, directories, and Python scripts, all packaged for ease of use via the command line.

## Overview

The project includes the following tools:

- **pycat**: Combines and extracts Python files into a single text file.
- **indexy**: Generates an index of functions and sections in a Python file.
- **mappy**: Creates a directory tree map of a given directory, with options to exclude certain folders.
- **makedot**: Integrates new tools into the `dotpy-toolkit` package.
- **remakedot**: Automates updating command entry points, incrementing version numbers, and rebuilding/reinstalling the package.
- **pytransfer**: A placeholder for future tools.

## Installation

To install the package:

### Setting up a Virtual Environment

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - On Linux/macOS:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```

3. Install the package locally:
   ```bash
   pip install .
   ```

For local development, use:
   ```bash
   pip install --force-reinstall .
   ```

### Running the `makedot.py` Script

To add and package new tools, run:
```bash
python makedot.py
```

This script integrates new tools, updates entry points in `pyproject.toml`, and rebuilds the package.

## Tools and Usage

### 1. **makedot**

Main script for integrating new tools into the toolkit. It automatically creates sub-packages, updates the `pyproject.toml` file, and increments version numbers.

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
python makedot.py
```

### 2. **pycat**

Combines multiple Python scripts into a single text file and optionally copies the result to the clipboard.

#### Example:

```bash
python pycat.py
```

### 3. **indexy**

Analyzes a Python script and generates an index of functions grouped by sections.

#### Example:

```bash
python indexy.py file.py --json --csv
```

### 4. **mappy**

Creates a visual directory tree map of a folder, excluding specified directories.

#### Example:

```bash
python mappy.py --dir /path/to/dir --exclude __pycache__ .git
```

### 5. **remakedot**

Automates the process of updating command entry points, incrementing the project version, and rebuilding/reinstalling the package.

#### Example:

```bash
python remakedot.py
```

## Project Structure

```plaintext
.
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

