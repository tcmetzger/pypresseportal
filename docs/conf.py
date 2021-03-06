"""Configuration file for the Sphinx documentation builder."""

# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

# from pypresseportal import __version__

sys.path.insert(0, os.path.abspath(".."))

# Add path for _ext/ogtag.py extension
sys.path.append(os.path.abspath("_ext"))


# -- Project information -----------------------------------------------------

project = "PyPresseportal"
copyright = "2020, Timo Cornelius Metzger"
author = "Timo Cornelius Metzger"

# The full version, including alpha/beta/rc tags

release = "0.0.1"


# -- General configuration ---------------------------------------------------

master_doc = "index"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinxcontrib.spelling",
    "ogtag",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for spell checking ----------------------------------------------
# source: https://sphinxcontrib-spelling.readthedocs.io/en/latest/customize.html
spelling_lang = "en_US"
tokenizer_lang = "en_US"
spelling_word_list_filename = "spelling_wordlist.txt"
spelling_show_suggestions = False
# spelling_filters=[]  # https://github.com/pyenchant/pyenchant/blob/master/website/content/tutorial.rst

# -- Options for HTML output -------------------------------------------------

# Constants for _ext/ogtag.py extension
og_site_url = "https://pypresseportal.readthedocs.io/en/latest/"
og_twitter_site = "@tcmetzger"
og_fallback_image = "https://www.tcmetzger.de/STATIC/pypresseportal_default.png"

# The theme to use for HTML and HTML Help pages. See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
