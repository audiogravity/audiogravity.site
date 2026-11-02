"""Guards for what the site tells search engines: the landing's canonical address, its snippet
and its structured data, robots.txt, and the sitemap they all point to.

None of it shows on the page, so a mistake here costs nothing visible: a canonical with a typo,
a sitemap naming a page that is gone, a ``Disallow: /`` left in robots.txt, and the site quietly
drops out of search results. Found missing on 2026-10-17 — no sitemap, no canonical, and Bing
returning nothing for the domain.

The sitemap itself is written by scripts/gen_manual_html.py and tested there; this file checks
that the landing and robots.txt agree with it.

The Landing workflow runs this file; run it locally with ``python3 -m pytest scripts/``.
"""

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_manual_html import SITE_URL, SITEMAP  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LANDING = (ROOT / "index.html").read_text(encoding="utf-8")
HEAD = LANDING[:LANDING.index("</head>")]
ROBOTS = (ROOT / "robots.txt").read_text(encoding="utf-8")
LOCS = re.findall(r"<loc>([^<]+)</loc>", SITEMAP.read_text(encoding="utf-8"))

#: Where a search result cuts the snippet, give or take the width of the letters.
SNIPPET_MAX = 155


def _meta(attr: str, name: str) -> str:
    """Content of one meta tag of the landing's head.

    Args:
        attr: ``name`` or ``property``.
        name: Its value, e.g. ``description``.

    Returns:
        The tag's content, entities decoded.
    """
    m = re.search(rf'<meta {attr}="{re.escape(name)}"\s+content="([^"]*)"', HEAD)
    assert m, f"no <meta {attr}={name}> in the landing's head"
    return html.unescape(m.group(1))


def _structured_data() -> dict:
    """The landing's JSON-LD block, parsed."""
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', HEAD, re.S)
    assert len(blocks) == 1, "the landing should carry exactly one JSON-LD block"
    return json.loads(blocks[0])


def _local(url: str) -> Path:
    """The file the site serves at an address of its own.

    Args:
        url: An absolute address under SITE_URL.

    Returns:
        The file GitHub Pages answers with: ``index.html`` for a directory, the ``.html`` page
        for an address without a suffix, the file itself otherwise.
    """
    assert url.startswith(SITE_URL), f"{url} is not an address of this site"
    path = ROOT / url[len(SITE_URL):]
    if url.endswith("/"):
        return path / "index.html"
    return path if path.suffix else path.with_suffix(".html")


def test_the_landing_names_its_one_address():
    """www.audiogravity.app serves the same page; the canonical says which address to index."""
    canonicals = re.findall(r'<link rel="canonical" href="([^"]+)">', HEAD)
    assert canonicals == [SITE_URL]


def test_the_link_preview_gives_the_same_address():
    assert _meta("property", "og:url") == SITE_URL


def test_nothing_asks_search_engines_to_stay_away():
    assert not re.search(r'<meta name="robots"[^>]*noindex', HEAD)
    assert not re.search(r"^Disallow:\s*/\s*$", ROBOTS, re.M), "robots.txt shuts the whole site"


def test_the_snippet_fits_and_says_what_the_product_is():
    description = _meta("name", "description")
    assert 70 <= len(description) <= SNIPPET_MAX, f"{len(description)} characters"
    # An attribute shows markup as typed: the brand is written plain here (CLAUDE.md, rule 1bis).
    assert "<" not in description and "Audiogravity" in description
    assert "streamer" in description


def test_robots_txt_points_to_the_sitemap():
    assert re.findall(r"^Sitemap:\s*(\S+)\s*$", ROBOTS, re.M) == [f"{SITE_URL}{SITEMAP.name}"]


def test_every_archived_scan_is_kept_from_crawlers():
    """A magazine scan kept as a post's source is someone else's work: it must not be indexed.

    An archived web page says so itself with a noindex tag; a PDF cannot, and GitHub Pages sends
    no X-Robots-Tag header, so robots.txt has to name each one. A scan added without its line
    would be read and indexed under the site's name.
    """
    scans = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "docs" / "archive").rglob("*.pdf"))
    assert scans, "no archived scan to check: this test guards nothing"
    disallowed = set(re.findall(r"^Disallow:\s*(\S+)\s*$", ROBOTS, re.M))
    assert [s for s in scans if f"/{s}" not in disallowed] == []


def test_an_archived_web_page_asks_not_to_be_indexed():
    """The archived pages carry noindex themselves; robots.txt must not hide that tag from crawlers."""
    disallowed = re.findall(r"^Disallow:\s*(\S+)\s*$", ROBOTS, re.M)
    for page in (ROOT / "docs" / "archive").rglob("*.html"):
        assert re.search(r'<meta name="robots" content="noindex">', page.read_text(encoding="utf-8")), page
        url = "/" + page.relative_to(ROOT).as_posix()
        assert not any(url.startswith(d) for d in disallowed), f"{url} is disallowed: its noindex goes unread"


def test_the_sitemap_opens_on_the_landing():
    assert LOCS and LOCS[0] == SITE_URL


def test_every_address_in_the_sitemap_is_a_page_of_the_site():
    """A sitemap naming a missing page reports an error for it in every search console."""
    assert len(LOCS) > 10
    for url in LOCS:
        assert _local(url).is_file(), f"{url} has no page behind it"


def test_the_structured_data_names_the_site_at_its_address():
    graph = {node["@type"]: node for node in _structured_data()["@graph"]}
    assert graph["WebSite"]["name"] == "Audiogravity"
    assert graph["WebSite"]["url"] == SITE_URL
    assert graph["SoftwareApplication"]["url"] == SITE_URL


def test_every_address_in_the_structured_data_exists():
    """The image and the manual it names are files of this site."""
    urls = re.findall(r'"(https://audiogravity\.app/[^"]*)"', json.dumps(_structured_data()))
    assert len(urls) >= 4
    for url in urls:
        assert _local(url).is_file(), f"{url} has no file behind it"


def test_the_structured_data_carries_no_price():
    """The price is copied by hand from the licence server's settings into the purchase card;
    a copy here would be one more to forget when it changes."""
    assert "offers" not in json.dumps(_structured_data())
