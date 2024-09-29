header_comment = "# COMMAND ----------"
markdown_comment = "# MAGIC %md"
magic_code = "# MAGIC "
databricks_nb_start = "# Databricks notebook source\n"


def nb2py(notebook):
    """Function for converting from notebook to py file"""
    result = []
    cells = notebook["cells"]

    for idx, cell in enumerate(cells):
        cell_type = cell["cell_type"]

        if cell_type == "markdown":
            cell_content = (
                markdown_comment
                + "\n"
                + magic_code
                + "".join(cell["source"]).replace("\n", "\n" + magic_code)
            )
            if idx == 0:
                cell_content = databricks_nb_start + cell_content
            else:
                cell_content = cell_content
            result.append(cell_content)

        if cell_type == "code":
            cell_content = "".join(cell["source"])
            if idx == 0:
                cell_content = databricks_nb_start + cell_content
            else:
                cell_content = cell_content
            result.append(cell_content)

    return ("\n\n" + header_comment + "\n\n").join(result)


def py2nb(py_str):
    """Function for converting from py file to notebook"""
    # remove leading header comment
    if py_str.startswith(header_comment):
        py_str = py_str[len(header_comment) :]

    # remove leading Databricks notebook start
    if py_str.startswith(databricks_nb_start):
        py_str = py_str[len(databricks_nb_start) :]

    cells = []
    chunks = py_str.split("\n\n%s\n\n" % header_comment)

    for chunk in chunks:
        cell_type = "code"
        if chunk.startswith(markdown_comment):
            chunk = chunk[len(markdown_comment) :]
            chunk = chunk.strip("'\n")
            chunk = chunk.replace(magic_code, "")
            cell_type = "markdown"

        cell = {
            "cell_type": cell_type,
            "metadata": {},
            "source": chunk.splitlines(True),
        }

        if cell_type == "code":
            cell.update({"outputs": [], "execution_count": None})

        cells.append(cell)

    notebook = {
        "cells": cells,
        "metadata": {
            "anaconda-cloud": {},
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.6.1",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 1,
    }

    return notebook
