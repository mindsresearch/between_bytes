# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Between Bytes'
copyright = '(C) 2024, The Authors. License: GNU AGPL-3.0'
author = 'Noah Duggan Erickson, Peter Hafner, Carter Jacobs, Trevor Le'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.napoleon', 'sphinx_design']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_css_files = ['material.css', 'i-cards.css']
# html_logo = "https://raw.githubusercontent.com/google/material-design-icons/master/symbols/web/data_loss_prevention/materialsymbolsoutlined/data_loss_prevention_wght700gradN25_48px.svg"
html_theme_options = {
    "github_url": "https://mindsresearch.github.io/between_bytes/",
    "logo": {"image_dark": "_static/btb_logo_dark.svg", "image_light": "_static/btb_logo_light.svg"},
    }

# -- Options for autodoc ----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration

# Automatically extract typehints when specified and place them in
# descriptions of the relevant function/method.
autodoc_typehints = "description"

# Don't show class signature with the class' name.
autodoc_class_signature = "separated"