"""Definition of writers and translator hooks."""

from sphinx.writers.html5 import HTML5Translator

from . import nodes


def visit_pythontutor(self: HTML5Translator, node: nodes.pythontutor):  # noqa: D103
    url = f"https://pythontutor.com/iframe-embed.html#code={node['code']}&py=311"
    attrs = {
        "width": node["width"],
        "height": node["height"],
        "src": url,
    }
    self.body.append(self.starttag(node, "iframe", **attrs))


def depart_pythontutor(self: HTML5Translator, node: nodes.pythontutor):  # noqa: D103
    self.body.append("</iframe>")
