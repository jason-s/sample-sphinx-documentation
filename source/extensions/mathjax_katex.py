# -*- coding: utf-8 -*-
"""
    mathjax_katex: based on sphinx.ext.mathjax:
    ~~~~~~~~~~~~~~~~~~

    sphinx.ext.mathjax

    Allow `MathJax <http://mathjax.org/>`_ to be used to display math in
    Sphinx's HTML writer -- requires the MathJax JavaScript library on your
    webserver/computer.

    :copyright: Copyright 2007-2016 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes

import sphinx
try:
    from sphinx.application import ExtensionError
except ImportError:
    from sphinx.errors import ExtensionError
from sphinx.ext.mathbase import setup_math as mathbase_setup

try:
    from sphinx.ext.mathbase import get_node_equation_number
except ImportError:
    from sphinx.util.math import get_node_equation_number

def html_visit_math(self, node):
    try:
        latex = node['latex']
    except KeyError:
        latex = node.astext()
    self.body.append(self.starttag(node, 'span', '', CLASS='math'))
    self.body.append(self.builder.config.mathjax_inline[0] +
                     self.encode(latex) +
                     self.builder.config.mathjax_inline[1] + '</span>')
    raise nodes.SkipNode


def html_visit_displaymath(self, node):
    self.body.append(self.starttag(node, 'div', CLASS='math'))
    try:
        latex = node['latex']
    except KeyError:
        latex = node.astext()
        
    if node['nowrap']:
        self.body.append(self.builder.config.mathjax_display[0] +
                         self.encode(latex) +
                         self.builder.config.mathjax_display[1])
        self.body.append('</div>')
        raise nodes.SkipNode

    # necessary to e.g. set the id property correctly
    if node['number']:
        number = get_node_equation_number(self, node)
        self.body.append('<span class="eqno">(%s)</span>' % number)
    self.body.append(self.builder.config.mathjax_display[0])
    if False:
        parts = [prt for prt in latex.split('\n\n') if prt.strip()]
        if len(parts) > 1:  # Add alignment if there are more than 1 equation
            self.body.append(r' \begin{align}\begin{aligned}')
        for i, part in enumerate(parts):
            part = self.encode(part)
            if r'\\' in part:
                self.body.append(r'\begin{split}' + part + r'\end{split}')
            else:
                self.body.append(part)
            if i < len(parts) - 1:  # append new line if not the last equation
                self.body.append(r'\\')
        if len(parts) > 1:  # Add alignment if there are more than 1 equation
            self.body.append(r'\end{aligned}\end{align} ')
    self.body.append(self.encode(latex))
    self.body.append(self.builder.config.mathjax_display[1])
    self.body.append('</div>\n')
    raise nodes.SkipNode

try:
    basestring
except:
    basestring = str

def builder_inited(app):
    jaxpath = app.config.mathjax_path
    if not jaxpath:
        raise ExtensionError('mathjax_path config value must be set for the '
                             'mathjax extension to work')

    # app.config.mathjax_path can be a string or a list of strings
    if isinstance(jaxpath, basestring):
        app.add_javascript(jaxpath)
    else:
        for p in jaxpath:
            app.add_javascript(p)

    if app.config.mathjax_css:
        app.add_stylesheet(app.config.mathjax_css)


def setup(app):
    try:
        mathbase_setup(app, (html_visit_math, None), (html_visit_displaymath, None))
    except ExtensionError:
        raise ExtensionError('sphinx.ext.mathjax: other math package is already loaded')

    # more information for mathjax secure url is here:
    # http://docs.mathjax.org/en/latest/start.html#secure-access-to-the-cdn
    try:
        app.add_config_value('mathjax_path',
                         'https://cdn.mathjax.org/mathjax/latest/MathJax.js?'
                         'config=TeX-AMS-MML_HTMLorMML', False)
        app.add_config_value('mathjax_inline', [r'\(', r'\)'], 'html')
        app.add_config_value('mathjax_display', [r'\[', r'\]'], 'html')
    except:
        pass
    app.add_config_value('mathjax_css', None, 'html')
    app.add_config_value('mathjax_use_katex', False, 'html')
    app.connect('builder-inited', builder_inited)

    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}
