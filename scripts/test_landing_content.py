"""Guards for what the landing and the 404 page point at: the files they load, and their
links into the manual and the guides.

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

from gen_manual_html import GUIDES_DIR, heading_ids, parse_toc, read_guides  # noqa: E402

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
    # A stylesheet or a script carries a stamp of its content (scripts/asset_versions.py).
    for path in (re.findall(r'\s(?:src|href)="/?(assets/[^"#?]+)(?:\?v=[0-9a-f]+)?"', html)
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
#: Every link to the guides, as (page, guide).
GUIDE_LINKS = sorted({
    (name, guide)
    for name, html in PAGES.items()
    for guide in re.findall(r'href="/?docs/guides/([^"#]*)(?:#[^"]*)?"', html)
})


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


@pytest.mark.parametrize("page,guide", GUIDE_LINKS, ids=lambda v: v or "-")
def test_every_link_to_the_guides_lands_on_one(page, guide):
    """The guides' pages come from their README's list, like the chapters from the Contents."""
    if guide in ("", "index"):
        assert (GUIDES_DIR / "README.md").is_file()
        return
    assert guide in {gid for gid, _, _ in read_guides()}, f"{guide} is not in the guides' README"


def test_the_bar_offers_the_guides_beside_the_manual():
    """The guides were given their own tab in the landing's bar (2026-10-17)."""
    bar = re.search(r'<div class="nav-links">(.*?)</div>', PAGES["index.html"], re.S).group(1)
    assert re.search(r'<a href="docs/manual/">Manual</a>\s*<a href="docs/guides/">Guides</a>', bar)


def test_the_bar_offers_the_blog_after_the_guides():
    """The blog took the last tab (2026-10-31), and its front page is one the generator writes."""
    bar = re.search(r'<div class="nav-links">(.*?)</div>', PAGES["index.html"], re.S).group(1)
    assert re.search(r'<a href="docs/guides/">Guides</a>\s*<a href="docs/blog/">Blog</a>\s*$', bar)
    assert (ROOT / "docs" / "blog" / "README.md").is_file()


def test_the_pages_were_found_to_point_somewhere():
    """The collections above are empty if the markup changes shape; that must not pass."""
    assert len([f for f in LOCAL_FILES if f[0] == "index.html"]) > 10
    # The stylesheet and the scripts are named with a stamp: read without it, they would drop
    # out of the list above and nothing would check them any more.
    for name, path in (("index.html", "assets/style.css"), ("index.html", "assets/main.js"), ("404.html", "assets/style.css")):
        assert (name, path) in LOCAL_FILES, f"{name} no longer reads as loading {path}"
    assert [f for f in LOCAL_FILES if f[0] == "404.html"]
    assert len(MANUAL_LINKS) > 5
    assert GUIDE_LINKS


def test_the_theme_toggle_comes_from_the_script_shared_with_the_manual():
    """The light / dark toggle is assets/theme-toggle.js, loaded by the landing and by every
    page of the manual, so that one choice holds across the site. main.js held its own copy
    until 2026-10-15; two copies could drift apart, and the manual had none."""
    assert re.search(r'src="assets/theme-toggle\.js(\?v=[0-9a-f]+)?" defer', PAGES["index.html"]), "the landing no longer loads the toggle"
    assert 'id="themeToggle"' in PAGES["index.html"] and 'id="themeIcon"' in PAGES["index.html"]
    main = (ROOT / "assets" / "main.js").read_text(encoding="utf-8")
    assert "themeToggle" not in main and "ag-theme" not in main, "main.js restates the toggle"


def test_the_back_to_top_control_says_where_it_goes():
    """The corner control leads to the top of the page and names itself to a screen reader.

    The button is built by assets/to-top.js, shared with the manual's pages: the landing must
    load that script, and the script must give the link its target and its name. The click
    itself is handled by the script, which scrolls up without writing ``#top`` into the address;
    the target still says where the link leads, to assistive technology and to a new tab.
    """
    assert re.search(r'src="assets/to-top\.js(\?v=[0-9a-f]+)?"', PAGES["index.html"]), "the landing no longer loads the button"
    script = (ROOT / "assets" / "to-top.js").read_text(encoding="utf-8")
    assert re.search(r"""(\.href\s*=\s*|setAttribute\(\s*['"]href['"]\s*,\s*)['"]#top['"]""", script), "no #top target"
    label = re.search(r"""setAttribute\(\s*['"]aria-label['"]\s*,\s*['"]([^'"]*)['"]\s*\)""", script)
    assert label and label.group(1).strip(), "the control has no accessible name"
