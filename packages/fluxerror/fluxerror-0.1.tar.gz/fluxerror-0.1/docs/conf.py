# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import pathlib
import sys
sys.path.insert(0, os.path.abspath('../fluxerror'))

root = pathlib.Path(__file__).parent.parent.absolute()
os.environ["PYTHONPATH"] = str(root)
sys.path.insert(0, str(root))
print("python exec:", sys.executable)
print("sys.path:", sys.path)

import fluxerror

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'FluxError'
copyright = '2024, Luke Gloege'
author = 'Luke Gloege'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "numpydoc",
#    "nbsphinx",
#    "recommonmark",
#    "IPython.sphinxext.ipython_directive",
#    "IPython.sphinxext.ipython_console_highlighting",
#    "sphinxcontrib.srclinks",
    ]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# have to change background color here and in custom CSS
html_theme_options = {
    "logo_only": True,
    "display_version": False,
    "style_nav_header_background": "#434C5E",
}


# make file (relative to this directory) to place at the top of the sidebar.
html_logo = "img/fluxerror-logo.png"
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = [
    "css/custom.css",
]