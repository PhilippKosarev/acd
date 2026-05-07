# Imports
from pathlib import Path
import sys
import commonmark

# Adding the module directory to PATH
script_file = Path(__file__)
script_dir = script_file.parent
module_dir = script_dir.parent
sys.path.append(str(module_dir))

# Project information
project = 'acd'
copyright = '2026, Philipp Kosarev'
author = 'Philipp Kosarev'

templates_path = ['templates']
exclude_patterns = ['build']

# Extensions
extensions = [
  'sphinx.ext.autodoc',
  'sphinx_copybutton',
]

# Default autodoc options
autodoc_default_options = {
  'members': True,
  'member-order': 'bysource',
}

# HTML theme
html_theme = 'pydata_sphinx_theme'
html_static_path = ['static']
html_css_files = ['style.css']
html_sidebars = { '**': [] }
html_theme_options = {
  'secondary_sidebar_items': [],
  'pygments_dark_style': 'material',
}



# Hooks
def docstring(app, what, name, obj, options, lines):
  """Converts markdown docstrings to ReST."""
  md  = '\n'.join(lines)
  ast = commonmark.Parser().parse(md)
  rst = commonmark.ReStructuredTextRenderer().render(ast)
  lines[:] = rst.splitlines()

# Connecting hooks
def setup(app):
  app.connect('autodoc-process-docstring', docstring)
