import argparse
import ast
import json


def analyze_code_structure(code):
    """
    Analyze the structure of the Python code using AST.
    Returns a list of functions, classes, imports, and their dependencies.
    """
    tree = ast.parse(code)
    structure = {"functions": [], "classes": [], "imports": [], "miscellaneous": []}

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            structure["functions"].append({
                "name": node.name,
                "start_line": node.lineno,
                "end_line": node.end_lineno if hasattr(node, 'end_lineno') else None,
                "dependencies": extract_dependencies(node)
            })
        elif isinstance(node, ast.ClassDef):
            structure["classes"].append({
                "name": node.name,
                "start_line": node.lineno,
                "end_line": node.end_lineno if hasattr(node, 'end_lineno') else None,
                "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            })
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            structure["imports"].append({
                "type": "import",
                "name": ast.unparse(node).strip(),
                "start_line": node.lineno
            })
        elif isinstance(node, ast.Expr) or isinstance(node, ast.Assign):
            structure["miscellaneous"].append({
                "type": "miscellaneous",
                "code": ast.unparse(node).strip(),
                "start_line": node.lineno
            })

    return structure


def extract_dependencies(node):
    dependencies = []
    for child in ast.walk(node):
        if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
            dependencies.append(child.func.id)
    return dependencies


def assign_script_positions(structure, script_length):
    positions = []
    for block_type, blocks in structure.items():
        for block in blocks:
            start_line = block["start_line"]
            position = (
                "beginning" if start_line < script_length * 0.3 else
                "body" if start_line < script_length * 0.7 else
                "end"
            )
            positions.append({
                **block,
                "type": block_type,
                "position": position
            })
    return positions


def preprocess_code(file_path, output_file):
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()

    script_length = len(code.splitlines())
    structure = analyze_code_structure(code)
    preprocessed_data = assign_script_positions(structure, script_length)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(preprocessed_data, file, indent=4)
    print(f"Preprocessed code saved to {output_file}.")

    return preprocessed_data


def main():
    parser = argparse.ArgumentParser(description="Preprocess Python code and output structure.")
    parser.add_argument("--file", help="Path to the Python file to preprocess.")
    parser.add_argument("--output", help="Path to save the preprocessed JSON.")
    args = parser.parse_args()

    file_path = args.file or input("Enter the path to the Python file to preprocess: ").strip()
    output_file = args.output or input("Enter the path to save the preprocessed JSON file: ").strip()

    preprocess_code(file_path, output_file)


if __name__ == "__main__":
    main()
