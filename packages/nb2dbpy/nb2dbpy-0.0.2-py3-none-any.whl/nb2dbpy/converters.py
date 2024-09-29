import yaml


HEADER_COMMENT = "# COMMAND ----------"
MARKDOWN_COMMENT = "# MAGIC %md"
MAGIC_CODE_PREFIX = "# MAGIC "
DATABRICKS_NB_START = "# Databricks notebook source\n"


def nb2py(notebook):
    """Convert a Jupyter notebook object to a Databricks-compatible .py script."""
    result = []
    cells = notebook.get("cells", [])

    for idx, cell in enumerate(cells):
        cell_type = cell.get("cell_type")
        source = "".join(cell.get("source", []))

        if cell_type == "markdown":
            # Format markdown cells
            formatted_source = source.replace("\n", f"\n{MAGIC_CODE_PREFIX}")
            cell_content = (
                f"{MARKDOWN_COMMENT}\n{MAGIC_CODE_PREFIX}{formatted_source}"
            )
        elif cell_type == "code":
            # Format code cells
            lines = source.splitlines(keepends=True)
            formatted_lines = []
            for line in lines:
                if line.startswith("%"):
                    # Prefix magic commands in code cells with '# MAGIC '
                    formatted_lines.append(f"{MAGIC_CODE_PREFIX}{line}")
                else:
                    formatted_lines.append(line)
            cell_content = "".join(formatted_lines)
        else:
            # Skip other cell types
            continue

        # Add Databricks notebook start header to the first cell
        if idx == 0:
            cell_content = f"{DATABRICKS_NB_START}{cell_content}"

        result.append(cell_content)

    return f"\n\n{HEADER_COMMENT}\n\n".join(result)


def py2nb(py_str):
    """Convert a Databricks-compatible .py script to a Jupyter notebook object."""
    # Remove leading header comment and Databricks notebook start
    py_str = py_str.lstrip()
    if py_str.startswith(HEADER_COMMENT):
        py_str = py_str[len(HEADER_COMMENT) :].lstrip()
    if py_str.startswith(DATABRICKS_NB_START):
        py_str = py_str[len(DATABRICKS_NB_START) :]

    # Split the script into chunks based on the header comment
    chunks = py_str.split(f"\n\n{HEADER_COMMENT}\n\n")
    cells = []

    for chunk in chunks:
        chunk = chunk.lstrip()
        if chunk.startswith(MARKDOWN_COMMENT):
            # Process markdown cells
            chunk = chunk[len(MARKDOWN_COMMENT) :].lstrip()
            lines = chunk.splitlines(keepends=True)
            source_lines = []
            for line in lines:
                if line.startswith(MAGIC_CODE_PREFIX):
                    line = line[len(MAGIC_CODE_PREFIX) :]
                source_lines.append(line)
            source = "".join(source_lines)
            cell_type = "markdown"
        else:
            # Process code cells
            lines = chunk.splitlines(keepends=True)
            source_lines = []
            for line in lines:
                if line.startswith(MAGIC_CODE_PREFIX):
                    # Remove '# MAGIC ' prefix from magic commands
                    line = line[len(MAGIC_CODE_PREFIX) :]
                source_lines.append(line)
            source = "".join(source_lines)
            cell_type = "code"

        cell = {
            "cell_type": cell_type,
            "metadata": {},
            "source": source.splitlines(keepends=True),
        }

        if cell_type == "code":
            cell.update({"outputs": [], "execution_count": None})

        cells.append(cell)

    # Define notebook metadata from yaml
    with open("src/nb2dbpy/jupyter_metadata.yaml") as f:
        metadata = yaml.load(f, Loader=yaml.FullLoader)

    notebook = {
        "cells": cells,
        "metadata": metadata,
        "nbformat": 4,
        "nbformat_minor": 2,
    }

    return notebook
