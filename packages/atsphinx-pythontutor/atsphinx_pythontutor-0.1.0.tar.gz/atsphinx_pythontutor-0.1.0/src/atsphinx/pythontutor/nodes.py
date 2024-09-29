"""Definition of nodes and writing behaviors."""

from docutils import nodes
from sphinx.writers.html5 import HTML5Translator


class pythontutor(nodes.General, nodes.Element):  # noqa: D101
    pass


def visit_pythontutor(self: HTML5Translator, node: pythontutor):  # noqa: D103
    url = f"https://pythontutor.com/iframe-embed.html#code={node['code']}&py=311"
    attrs = {
        "width": node["width"],
        "height": node["height"],
        "src": url,
    }
    self.body.append(self.starttag(node, "iframe", **attrs))


def depart_pythontutor(self: HTML5Translator, node: pythontutor):  # noqa: D103
    self.body.append("</iframe>")
