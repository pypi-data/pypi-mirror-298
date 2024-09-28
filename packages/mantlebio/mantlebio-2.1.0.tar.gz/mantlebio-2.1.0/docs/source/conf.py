# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('../../mantlebio'))


project = 'Mantle SDK'
copyright = '2024, MantleBio Inc.'
author = 'MantleBio'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
    'sphinx.ext.autosummary',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db',
                    '.DS_Store', '**tests**',
                    '**helpers**', '**utils**',
                    '**storage**', '**session**']
autosummary_generate = True


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_permalinks_icon = '<span>#</span>'
html_theme = 'sphinxawesome_theme'
html_logo = '_static/logo.png'
html_favicon = '_static/favicon.ico'
html_theme_options = {
    'collapse_navigation': False,
    'navigation_depth': 4,
    "nav_include_hidden": True,  # Include hidden TOC items in navigation
    "nav_links": [
        {"href": "docs.mantlebio.com", "title": "Docs"},
    ]
}

html_static_path = ['_static']
