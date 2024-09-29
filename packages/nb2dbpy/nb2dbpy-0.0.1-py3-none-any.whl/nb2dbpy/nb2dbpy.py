import argparse
import json
import sys
from os import path
from nb2dbpy.converters import nb2py, py2nb


def convert(in_file, out_file=None):
    """Main function to determine conversion direction and perform the conversion."""

    _, in_ext = path.splitext(in_file)

    if in_ext == ".ipynb":
        if not out_file:
            out_file = in_file.replace(".ipynb", ".py")
        with open(in_file, "r", encoding="utf-8") as f:
            notebook = json.load(f)
        py_str = nb2py(notebook)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(py_str)
        print(f"Converted '{in_file}' to '{out_file}'.")

    elif in_ext == ".py":
        if not out_file:
            out_file = in_file.replace(".py", ".ipynb")
        with open(in_file, "r", encoding="utf-8") as f:
            py_str = f.read()
        notebook = py2nb(py_str)
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(notebook, f, indent=2)
        print(f"Converted '{in_file}' to '{out_file}'.")

    else:
        raise Exception("Input file must have a .ipynb or .py extension.")


def main():
    """Entry point for the command-line interface."""

    parser = argparse.ArgumentParser(
        description="Convert between Databricks .ipynb notebooks and .py files."
    )
    parser.add_argument(
        "input_file",
        help="The input file to convert (must have .ipynb or .py extension).",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="The output file name. If not specified, replaces the extension of the input file.",
    )
    args = parser.parse_args()

    in_file = args.input_file
    out_file = args.output

    if not path.exists(in_file):
        print(f"Error: File '{in_file}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if not out_file:
        if in_file.endswith(".ipynb"):
            out_file = in_file.replace(".ipynb", ".py")
        elif in_file.endswith(".py"):
            out_file = in_file.replace(".py", ".ipynb")

    # Check if the output file already exists, ask for confirmation to overwrite
    if path.exists(out_file):
        print(f"Warning: File '{out_file}' already exists.")
        while True:
            response = (
                input("Do you want to overwrite it? (y/n): ").strip().lower()
            )
            if response in ("y", "yes"):
                break
            elif response in ("n", "no"):
                print("Exiting without overwriting the file.")
                sys.exit(0)
            else:
                print("Invalid response. Please enter 'y' or 'n'.")

    try:
        convert(in_file, out_file)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
