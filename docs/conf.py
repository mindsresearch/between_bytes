# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'SelfScape Insight'
copyright = '(C) 2024, The Authors. License: GNU AGPL-3.0'
author = 'Noah Duggan Erickson, Liam Gore, Peter Hafner, Carter Jacobs, Trevor Le'
release = '1.0rc1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.napoleon', 'sphinx_design', 'sphinx.ext.todo']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_css_files = ['material.css']
# html_logo = "https://raw.githubusercontent.com/google/material-design-icons/master/symbols/web/data_loss_prevention/materialsymbolsoutlined/data_loss_prevention_wght700gradN25_48px.svg"
html_theme_options = {
    "github_url": "https://mindsresearch.github.io/selfscape-insight/",
    "logo": {"image_dark": "_static/logo-dark.svg", "image_light": "https://raw.githubusercontent.com/google/material-design-icons/master/symbols/web/data_loss_prevention/materialsymbolsoutlined/data_loss_prevention_wght700gradN25_48px.svg"}
    }

# -- Options for autodoc ----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration

# Automatically extract typehints when specified and place them in
# descriptions of the relevant function/method.
autodoc_typehints = "description"

# Don't show class signature with the class' name.
autodoc_class_signature = "separated"