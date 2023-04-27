# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, root_path)
project = ""
copyright = "2023, lovemefan"
author = "lovemefan"
release = "v2.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


templates_path = ["_templates"]
exclude_patterns = []
extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
]
todo_include_todos = True
language = "zh-CN"

source_suffix = {
    ".rst": "restructuredtext",
}
master_doc = "index"
numfig = True
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
