from atsphinx.mini18n import get_template_dir as get_mini18n_template_dir
from atsphinx.pythontutor import __version__ as version

# -- Project information
project = "atsphinx-pythontutor"
copyright = "2024, Kazuya Takei"
author = "Kazuya Takei"
release = version

# -- General configuration
extensions = [
    "sphinx.ext.todo",
    "atsphinx.pythontutor",
    "atsphinx.mini18n",
]
templates_path = ["_templates", get_mini18n_template_dir()]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for linkcheck
linkcheck_anchors_ignore = [
    "^code=.+",
]

# -- Options for HTML output
html_theme = "furo"
html_static_path = ["_static"]
html_title = f"{project} v{release}"
html_sidebars = {
    "**": [
        "sidebar/scroll-start.html",
        "sidebar/brand.html",
        "mini18n/snippets/select-lang.html",
        "sidebar/search.html",
        "sidebar/navigation.html",
        "sidebar/ethical-ads.html",
        "sidebar/scroll-end.html",
    ]
}

# -- Extension configuration
# atsphinx.mini18n
mini18n_default_language = "en"
mini18n_support_languages = ["en", "ja"]
mini18n_select_lang_label = ""
mini18n_basepath = "/pythontutor/"
