"""Definition of directives."""

from urllib.parse import quote

from docutils.nodes import Text, paragraph, reference
from docutils.parsers.rst import Directive, directives  # type:ignore

from . import nodes


class PythonTutor(Directive):  # noqa: D101
    has_content = True

    option_spec = {
        "width": directives.positive_int,
        "height": directives.positive_int,
        "alt": directives.unchanged,
    }

    def run(self):  # noqa: D102
        code = quote("\n".join(self.content), safe="/',")
        attrs = {
            "width": self.options.get("width", 800),
            "height": self.options.get("height", 500),
            "code": code,
        }
        node = nodes.pythontutor(**attrs)
        alt = self.options.get("alt", None)
        if not alt:
            return [
                node,
            ]
        alt_url = f"https://pythontutor.com/live.html#code={code}&py=311"
        alt_ref = reference(refuri=alt_url)
        alt_ref.append(Text(alt))
        alt_node = paragraph()
        alt_node.append(alt_ref)
        return [
            alt_node,
            node,
        ]
