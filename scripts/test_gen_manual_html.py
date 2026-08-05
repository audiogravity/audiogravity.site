"""Tests for the manual renderer.

These matter more than most: the generator runs unattended in CI and commits its own output,
so a regression reaches the published site without anyone reading a diff.

Run with ``python3 -m pytest scripts/`` from the repository root.
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_manual_html import (  # noqa: E402
    lazy_load_images,
    link_between_pages,
    page,
    parse_toc,
    slugify,
    stamp_heading_ids,
    wrap_tables,
)

TOC = [("00-quick-start", "Quick start"), ("04-listening", "Listening")]


class TestParseToc:
    def test_reads_numbered_entries_in_order_including_chapter_zero(self):
        md = (
            "# Manual\n\n## Contents\n\n"
            "0. [Quick start](00-quick-start.md) — from zero to music\n"
            "1. [Introduction](01-introduction.md) — what it is\n"
            "10. [Glossary](10-glossary.md) — terms\n"
        )
        assert parse_toc(md) == [
            ("00-quick-start", "Quick start"),
            ("01-introduction", "Introduction"),
            ("10-glossary", "Glossary"),
        ]

    def test_keeps_inline_markup_in_a_label(self):
        """The brand carries <sup>; labels go straight into HTML, so it must survive."""
        md = "1. [About Audiogravi<sup>ty</sup>](01-introduction.md) — x\n"
        assert parse_toc(md) == [("01-introduction", "About Audiogravi<sup>ty</sup>")]

    def test_ignores_prose_and_bullet_links(self):
        md = "See [Listening](04-listening.md) for details.\n- [Bullet](02-installation.md)\n"
        assert parse_toc(md) == []


class TestSlugify:
    @pytest.mark.parametrize("text,expected", [
        ("Audio topology (signal-chain map)", "audio-topology-signal-chain-map"),
        ("3. Install the audio engines", "3-install-the-audio-engines"),
        ("Réglages", "réglages"),
        ("  Spaced   out  ", "spaced-out"),
        ("Under_scores", "under-scores"),
    ])
    def test_matches_github_anchors(self, text, expected):
        """The landing links to GitHub-style anchors; a mismatch silently lands at the top."""
        assert slugify(text) == expected


class TestStampHeadingIds:
    def test_stamps_h2_h3_and_h4(self):
        out = stamp_heading_ids("<h2>Roon</h2><h3>Setup</h3><h4>Detail</h4>")
        assert 'id="roon"' in out and 'id="setup"' in out and 'id="detail"' in out

    def test_leaves_h1_alone(self):
        """h1 is the chapter title — nothing links to it, and one page has exactly one."""
        assert stamp_heading_ids("<h1>Listening</h1>") == "<h1>Listening</h1>"

    def test_de_duplicates_repeated_headings(self):
        out = stamp_heading_ids("<h2>Notes</h2><h2>Notes</h2><h2>Notes</h2>")
        assert re.findall(r'id="([^"]+)"', out) == ["notes", "notes-1", "notes-2"]

    def test_strips_markup_before_slugging(self):
        out = stamp_heading_ids("<h2>What <strong>Audiogravi<sup>ty</sup></strong> is</h2>")
        assert 'id="what-audiogravity-is"' in out


class TestLinkBetweenPages:
    KNOWN = {"00-quick-start", "04-listening", "README"}

    def test_rewrites_a_known_chapter(self):
        assert link_between_pages('href="04-listening.md"', self.KNOWN) == 'href="04-listening.html"'

    def test_carries_the_anchor(self):
        assert (link_between_pages('href="04-listening.md#queue"', self.KNOWN)
                == 'href="04-listening.html#queue"')

    def test_readme_becomes_the_index(self):
        assert link_between_pages('href="README.md"', self.KNOWN) == 'href="index.html"'

    def test_leaves_a_sibling_document_alone(self):
        """No page is generated for ../../RELEASE_NOTES.md — rewriting it would make a 404."""
        html = 'href="../../RELEASE_NOTES.md"'
        assert link_between_pages(html, self.KNOWN) == html

    def test_leaves_absolute_links_alone(self):
        html = 'href="https://example.com/a.md"'
        assert link_between_pages(html, self.KNOWN) == html

    def test_leaves_an_unknown_chapter_alone(self):
        html = 'href="99-nope.md"'
        assert link_between_pages(html, self.KNOWN) == html


class TestWrapTables:
    def test_wraps_each_table_once(self):
        out = wrap_tables("<table><tr><td>a</td></tr></table><table><tr><td>b</td></tr></table>")
        assert out.count('<div class="man-table">') == 2
        assert out.count("<table>") == 2

    def test_keeps_the_table_element(self):
        """Flattening it to a block is the usual shortcut; it costs the table its role."""
        out = wrap_tables("<table><tr><td>a</td></tr></table>")
        assert out == '<div class="man-table"><table><tr><td>a</td></tr></table></div>'

    def test_leaves_html_with_no_table_untouched(self):
        assert wrap_tables("<p>x</p>") == "<p>x</p>"


class TestLazyLoadImages:
    def test_adds_the_attribute(self):
        assert lazy_load_images('<img src="a.webp">') == '<img loading="lazy" src="a.webp">'

    def test_does_not_add_it_twice(self):
        html = '<img loading="eager" src="a.webp">'
        assert lazy_load_images(html) == html

    def test_handles_every_image_on_a_page(self):
        html = '<img src="a.webp"><p>x</p><img src="b.webp">'
        assert lazy_load_images(html).count('loading="lazy"') == 2


class TestPage:
    def test_canonical_of_a_chapter_is_its_own_file(self):
        out = page("Listening", "<p>x</p>", TOC, "04-listening", "04-listening.html")
        assert ('<link rel="canonical" '
                'href="https://audiogravity.app/docs/manual/04-listening.html">') in out

    def test_canonical_of_the_contents_page_is_the_directory(self):
        """Derived from the chapter id, this produced `/docs/manual/.html` — a 404, which is
        the one address a canonical link must never carry."""
        out = page("Contents", "<p>x</p>", TOC, "", "")
        assert '<link rel="canonical" href="https://audiogravity.app/docs/manual/">' in out
        assert "/docs/manual/.html" not in out

    def test_marks_the_active_chapter_for_assistive_technology(self):
        out = page("Listening", "", TOC, "04-listening", "04-listening.html")
        assert 'href="04-listening.html" aria-current="page"' in out
        assert out.count('aria-current="page"') == 1

    def test_contents_page_marks_no_chapter_active(self):
        assert 'aria-current' not in page("Contents", "", TOC, "", "")

    def test_lists_every_chapter_in_the_sidebar(self):
        out = page("Contents", "", TOC, "", "")
        assert out.count('class="man-nav-item') == len(TOC)

    def test_the_way_back_carries_the_app_icon_and_names_itself(self):
        """Two ways home per page: this one and the footer link. The icon is decorative — the
        link is named by aria-label, not by an alt text repeating the wordmark beside it."""
        out = page("Listening", "", TOC, "04-listening", "04-listening.html")
        assert 'href="../../index.html" aria-label="Audiogravity home"' in out
        assert 'class="man-home-icon" src="../../assets/icons/apple-touch-180.png" alt=""' in out
        assert out.count('href="../../index.html"') == 2  # top bar and footer

    def test_strips_markup_from_the_document_title(self):
        out = page("About Audiogravi<sup>ty</sup>", "", TOC, "", "")
        assert "<title>About Audiogravity — Audiogravity manual</title>" in out
