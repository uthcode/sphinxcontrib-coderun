"""
sphinxcontrib.coderun
~~~~~~~~~~~~~~~~~~~~~
Sphinx directive that renders a literalinclude code block with an embedded
codapi "Run" button powered by a self-hosted codeapi instance.

Usage in RST::

    .. coderun:: path/to/file.c
       :language: c
       :sandbox: gcc
       :url: https://codapi.example.com

Global defaults in conf.py::

    coderun_url     = 'https://codapi.example.com'
    coderun_sandbox = 'gcc'
"""

import uuid

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.directives.code import LiteralInclude


class CodeRunDirective(LiteralInclude):
    """Like literalinclude but appends a codapi run widget after the code block."""

    option_spec = {
        **LiteralInclude.option_spec,
        'sandbox': directives.unchanged,
        'url': directives.unchanged,
    }

    def run(self):
        result = super().run()
        sandbox = self.options.get('sandbox') or self.env.config.coderun_sandbox
        url = self.options.get('url') or self.env.config.coderun_url

        # Wrap the code block in a div with a unique ID so the codapi selector
        # can target just the <code> element — excluding any "Copy to clipboard"
        # buttons that themes inject into the surrounding <pre>/<div>.
        code_id = f"coderun-{uuid.uuid4().hex[:8]}"
        wrapper_open = nodes.raw('', f'<div id="{code_id}">', format='html')
        wrapper_close = nodes.raw('', '</div>', format='html')
        snippet_html = (
            f'<codapi-snippet sandbox="{sandbox}" url="{url}" '
            f'editor="basic" selector="#{code_id} pre"></codapi-snippet>'
        )
        return [wrapper_open] + result + [wrapper_close, nodes.raw('', snippet_html, format='html')]


def setup(app):
    app.add_config_value('coderun_url', 'http://localhost:1313', 'html')
    app.add_config_value('coderun_sandbox', 'gcc', 'html')
    app.add_directive('coderun', CodeRunDirective)
    app.add_css_file('coderun.css')
    app.add_js_file(
        'https://unpkg.com/@antonz/codapi@0.19.4/dist/snippet.js',
        **{'type': 'module'},
    )
    app.connect('builder-inited', copy_static_files)
    return {'version': '0.1', 'parallel_read_safe': True}


def copy_static_files(app):
    """Copy the bundled CSS into the build's _static directory."""
    import os
    import shutil
    src = os.path.join(os.path.dirname(__file__), 'static', 'coderun.css')
    if app.builder.format != 'html':
        return
    dst_dir = os.path.join(app.outdir, '_static')
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copy(src, os.path.join(dst_dir, 'coderun.css'))
