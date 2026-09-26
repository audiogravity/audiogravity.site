"""Guards for what the landing and the 404 page point at: the files they load, and their
links into the manual.

A capture renamed in assets/pics, or a manual heading reworded, breaks a page without a sound:
the image shows its alt text, the link lands at the top of the chapter instead of the section.
These tests check every target the pages name against the files, the chapters and the headings
that exist.

The manual's anchors come from its Markdown, through the generator's own renderer, and its
chapters from the Contents list the generator builds pages from — so a heading reworded, or a
chapter left out of the Contents, fails here before the pages are even regenerated.

The Landing workflow runs this file; run it locally with ``python3 -m pytest scripts/``.
"""

import functools
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_manual_html import heading_ids, parse_toc  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MANUAL = ROOT / "docs" / "manual"
PAGES = {name: (ROOT / name).read_text(encoding="utf-8") for name in ("index.html", "404.html")}
SITE = "https://audiogravity.app/"

#: Every local file a page loads — images, icons, fonts, the stylesheet — and the link preview
#: image, which the meta tags name by its absolute address on the site. The 404 page is served at
#: any depth, so it names its files from the root as well as relatively; both resolve from ROOT.
LOCAL_FILES = sorted({
    (name, path)
    for name, html in PAGES.items()
    for path in (re.findall(r'\s(?:src|href)="/?(assets/[^"#?]+)"', html)
                 + [u[len(SITE):] for u in re.findall(
                     r'<meta [^>]*content="(https://audiogravity\.app/assets/[^"]+)"', html)])
})
#: Every link into the manual, relative or from the root, as (page, chapter, anchor).
MANUAL_LINKS = sorted({
    (name, chapter, anchor)
    for name, html in PAGES.items()
    for chapter, anchor in re.findall(r'href="/?docs/manual/([^"#]*)(?:#([^"]*))?"', html)
})
#: The chapters the generator turns into pages: the Contents list, not the files on disk.
CHAPTERS = {cid for cid, _ in parse_toc((MANUAL / "README.md").read_text(encoding="utf-8"))}


@functools.lru_cache(maxsize=None)
def _anchors(source: str) -> frozenset[str]:
    """Heading ids of a Markdown file, computed once however many links point into it.

    Args:
        source: Path of the Markdown file, relative to the manual's folder.

    Returns:
        The ids its headings carry on the site.
    """
    return frozenset(heading_ids((MANUAL / source).read_text(encoding="utf-8")))


@pytest.mark.parametrize("page,path", LOCAL_FILES)
def test_every_file_a_page_loads_exists(page, path):
    """A missing image shows its alt text, a missing icon or preview image shows nothing."""
    assert (ROOT / path).is_file()


@pytest.mark.parametrize("page,chapter,anchor", MANUAL_LINKS, ids=lambda v: v or "-")
def test_every_link_into_the_manual_lands_on_its_section(page, chapter, anchor):
    """A chapter outside the Contents gets no page; a missing heading lands at the top."""
    if chapter in ("", "index"):
        assert not anchor or anchor in _anchors("README.md")
        return
    assert chapter in CHAPTERS, f"{chapter} is not in the manual's Contents, so it has no page"
    if anchor:
        assert anchor in _anchors(f"{chapter}.md")


def test_the_pages_were_found_to_point_somewhere():
    """The collections above are empty if the markup changes shape; that must not pass."""
    assert len([f for f in LOCAL_FILES if f[0] == "index.html"]) > 10
    assert [f for f in LOCAL_FILES if f[0] == "404.html"]
    assert len(MANUAL_LINKS) > 5
