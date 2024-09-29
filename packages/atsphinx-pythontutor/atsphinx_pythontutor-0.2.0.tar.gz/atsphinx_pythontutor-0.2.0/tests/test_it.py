"""Standard tests."""

from io import StringIO

import pytest
from bs4 import BeautifulSoup
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html")
def test__it(app: SphinxTestApp, status: StringIO, warning: StringIO):
    """Test to pass."""
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "html.parser")
    assert soup.find("iframe") is not None


@pytest.mark.sphinx("html")
def test__with_alt_text(app: SphinxTestApp):
    """Test to pass."""
    app.build()
    soup = BeautifulSoup((app.outdir / "with-alt.html").read_text(), "html.parser")
    assert soup.find("iframe") is not None
    href = [
        a for a in soup.find_all("a") if a["href"].startswith("https://pythontutor.com")
    ][0]
    assert href.text == "help text"
