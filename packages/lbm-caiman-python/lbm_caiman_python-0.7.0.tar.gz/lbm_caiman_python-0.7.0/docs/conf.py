# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
from pathlib import Path

notebooks_mod = os.path.abspath(os.path.join("../", "demos/notebooks/"))
sys.path.insert(0, os.path.abspath(os.path.join("..")))
sys.path.insert(0, os.path.abspath(os.path.join("..", "lbm_caiman_python")))
print(os.path.join("..", "lbm_caiman_python"))

project = "LBM-CaImAn-Python"
copyright = "2024, Elizabeth R. Miller Brain Observatory | The Rockefeller University. All Rights Reserved"
author = "Flynn OConnell"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

exclude_patterns = ["Thumbs.db", ".DS_Store"]


myst_enable_extensions = [
    "colon_fence",
    "dollarmath",
    "html_image",
]

extensions = [
    "sphinx.ext.autodoc",
    # "sphinxcontrib.images",
    "sphinxcontrib.video",
    "myst_nb",
    "sphinx_copybutton",
    "sphinx_togglebutton",
    "numpydoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_design",
    "sphinx_tippy",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".ipynb": "myst-nb",
    ".md": "myst-nb",
}

myst_admonition_enable = True
myst_amsmath_enable = True
myst_html_img_enable = True
myst_url_schemes = ("http", "https", "mailto")

images_config = {"cache_path": "./_images/"}

templates_path = ["_templates"]
html_static_path = ["_static"]

# A shorter title for the navigation bar.  Default is the same as html_title.
html_title = "LBM-CaImAn-Python"

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_static/logo_caiman_python_with_icon.png"

html_favicon = "./_static/icon_caiman_python.svg"

html_theme = "sphinx_book_theme"
# html_short_title = "LB.py"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_use_modindex = True
html_copy_source = False
html_file_suffix = ".html"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3.9", None),
    "numpydoc": ("https://numpydoc.readthedocs.io/en/latest", None),
    "mbo": (
        "https://millerbrainobservatory.github.io/",
        None,
    ),
    "caiman": ("https://caiman.readthedocs.io/en/latest/", None),
    "suite2p": ("https://suite2p.readthedocs.io/en/latest/", None),
}

templates_path = ["_templates"]
intersphinx_disabled_reftypes = ["*"]

html_theme_options = {
    "path_to_docs": "docs",
    "repository_url": "https://github.com/MillerBrainObservatory/LBM-CaImAn-Python/",
    "repository_branch": "master",
    "use_edit_page_button": True,
    "use_source_button": True,
    "use_issues_button": True,
    "use_download_button": True,
    "show_toc_level": 3,
    "icon_links": [
        {
            "name": "MBO User Hub",
            "url": "https://millerbrainobservatory.github.io/",
            "icon": "./_static/icon_mbo_home.png",
            "type": "local",
        },
        {
            "name": "MBO Github",
            "url": "https://github.com/MillerBrainObservatory/",
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
        {
            "name": "Connect with MBO",
            "url": "https://mbo.rockefeller.edu/contact/",
            "icon": "fa-regular fa-address-card",
            "type": "fontawesome",
        },
    ],
}
