import ast
import re
import csv
import json
import argparse
import os


def extract_subsections(file_path):
    """Extracts subsection names from comments labeled with '# Chapt {name}' or similar formats."""
    subsections = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for lineno, line in enumerate(file, start=1):
                # Match subsections marked with various formats
                match = re.match(r"#\s*(Ch|Chapt|Chapter|Section|Subsection)[:\s]+(.+)", line.strip())
                if match:
                    subsections.append({
                        "type": "subsection",
                        "name": match.group(2),
                        "start_line": lineno,
                        "end_line": None
                    })

        # Assign end lines to each subsection
        for i in range(len(subsections) - 1):
            subsections[i]["end_line"] = subsections[i + 1]["start_line"] - 1

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error extracting subsections: {e}")

    return subsections


def generate_function_index(file_path):
    """Generates an index of all functions (sync and async) in a Python file."""
    function_index = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            print(f"Error parsing file {file_path}: {e}")
            return []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                function_index.append({
                    "type": "async def" if isinstance(node, ast.AsyncFunctionDef) else "def",
                    "name": node.name,
                    "start_line": node.lineno,
                    "end_line": getattr(node, 'end_lineno', None)
                })

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

    return function_index


def group_functions_by_subsection(functions, subsections):
    """Groups functions under their respective subsections."""
    grouped = []

    for subsection in subsections:
        # Find functions within the subsection's range
        subsection_functions = [
            func for func in functions
            if subsection["start_line"] <= func["start_line"] <= (subsection["end_line"] or float('inf'))
        ]
        grouped.append({
            "subsection": subsection["name"],
            "functions": subsection_functions
        })

    return grouped


def export_to_json(entries, output_path):
    """Exports the combined index to a JSON file."""
    try:
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(entries, file, indent=4)
        print(f"Exported data to JSON file: {output_path}")
    except Exception as e:
        print(f"Error exporting to JSON: {e}")


def export_to_csv(entries, output_path):
    """Exports the combined index to a CSV file."""
    try:
        with open(output_path, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Subsection", "Type", "Name", "Start Line", "End Line"])
            for entry in entries:
                subsection = entry["subsection"]
                for func in entry["functions"]:
                    writer.writerow([subsection, func["type"], func["name"], func["start_line"], func["end_line"]])
        print(f"Exported data to CSV file: {output_path}")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an index of functions and subsections in a Python file.")
    parser.add_argument("file", help="Path to the input Python file.")
    parser.add_argument("--json", action="store_true", help="Export the index to a JSON file.")
    parser.add_argument("--csv", action="store_true", help="Export the index to a CSV file.")

    args = parser.parse_args()
    file_path = args.file

    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        exit(1)

    # Extract subsections and functions
    subsections = extract_subsections(file_path)
    print(f"Extracted Subsections: {subsections}")

    functions = generate_function_index(file_path)
    print(f"Extracted Functions: {functions}")

    # Group functions by subsection
    grouped_entries = group_functions_by_subsection(functions, subsections)

    if grouped_entries:
        print(f"\nIndex of functions grouped by subsections in {file_path}:\n")
        for entry in grouped_entries:
            print(f"Subsection: {entry['subsection']}")
            for func in entry["functions"]:
                print(f"  {func['type']} {func['name']} (Line {func['start_line']} - {func['end_line']})")
            print()

        # Prepare output file paths
        base_name = os.path.splitext(file_path)[0]
        json_output_path = f"{base_name}_index.json"
        csv_output_path = f"{base_name}_index.csv"

        # Export based on flags
        if not args.json and not args.csv:
            print("No output format specified. Exporting both JSON and CSV by default.")
            args.json = True
            args.csv = True

        if args.json:
            export_to_json(grouped_entries, json_output_path)
        if args.csv:
            export_to_csv(grouped_entries, csv_output_path)
    else:
        print(f"No functions or subsections found in {file_path} or the file could not be processed.")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate an index of functions and subsections in a Python file.")
    parser.add_argument("file", help="Path to the input Python file.")
    parser.add_argument("--json", action="store_true", help="Export the index to a JSON file.")
    parser.add_argument("--csv", action="store_true", help="Export the index to a CSV file.")
    args = parser.parse_args()

    file_path = args.file

    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        return

    # Extract subsections and functions
    subsections = extract_subsections(file_path)
    functions = generate_function_index(file_path)
    grouped_entries = group_functions_by_subsection(functions, subsections)

    if grouped_entries:
        print(f"\nIndex of functions grouped by subsections in {file_path}:\n")
        for entry in grouped_entries:
            print(f"Subsection: {entry['subsection']}")
            for func in entry["functions"]:
                print(f"  {func['type']} {func['name']} (Line {func['start_line']} - {func['end_line']})")
            print()

        # Prepare output file paths
        base_name = os.path.splitext(file_path)[0]
        json_output_path = f"{base_name}_index.json"
        csv_output_path = f"{base_name}_index.csv"

        # Export based on flags
        if not args.json and not args.csv:
            print("No output format specified. Exporting both JSON and CSV by default.")
            args.json = True
            args.csv = True

        if args.json:
            export_to_json(grouped_entries, json_output_path)
        if args.csv:
            export_to_csv(grouped_entries, csv_output_path)
    else:
        print(f"No functions or subsections found in {file_path} or the file could not be processed.")
