#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import datetime

project_directory = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    # 'eoddata_client'
)

print(project_directory)
sys.path.insert(0, project_directory)

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

add_module_names = False

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = 'eoddata-client'
copyright = '%s, Aleksey' % datetime.date.today().year
author = 'Aleksey'

version = '0.3.3'

release = '0.3.3'

language = 'en'

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'sphinx'

todo_include_todos = True

html_theme = 'alabaster'

html_theme_options = {
    'show_powered_by': False,
    'show_related': True
}

html_static_path = ['_static']

# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
        'donate.html',
    ]
}

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'eoddata-clientdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'eoddata-client.tex', 'eoddata-client Documentation',
     'Aleksey', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'eoddata-client', 'eoddata-client Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'eoddata-client', 'eoddata-client Documentation',
     author, 'eoddata-client', 'One line description of project.',
     'Miscellaneous'),
]
