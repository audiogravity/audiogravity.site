"""Tests for the manual renderer.

These matter more than most: the generator runs unattended in CI and commits its own output,
so a regression reaches the published site without anyone reading a diff.

Run with ``python3 -m pytest scripts/`` from the repository root.
"""

import html
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_manual_html import (  # noqa: E402
    MANUAL_DIR,
    REPO_DIR,
    build,
    heading_ids,
    highlight_code,
    highlight_fence,
    lazy_load_images,
    markdown,
    link_between_pages,
    page,
    parse_toc,
    slugify,
    stamp_heading_ids,
    stamp_version,
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
        # GitHub replaces each space with a dash and does NOT collapse the run. This
        # case used to assert the opposite, which is what let seven cross-references
        # ship broken: an em dash between two words leaves two spaces behind, so the
        # anchor the author wrote carries two hyphens.
        ("  Spaced   out  ", "spaced---out"),
        ("2. Sign in — and secure your account", "2-sign-in--and-secure-your-account"),
        # The heading reaches slugify as HTML, where & is an entity. Left encoded it
        # produced "users-amp-access", a word in no heading.
        ("Users &amp; access", "users--access"),
        ("Users & access", "users--access"),
        # Underscores are kept, as GitHub keeps them.
        ("Under_scores", "under_scores"),
    ])
    def test_matches_github_anchors(self, text, expected):
        """The landing links to GitHub-style anchors; a mismatch silently lands at the top."""
        assert slugify(text) == expected

    @pytest.mark.parametrize("heading,in_app_slug", [
        # Expected values computed by hand from the rule in ag-manual-modal.js:
        #   lower → trim → drop anything not letter/number/_/space/- → each space to '-'
        ("No sound / wrong output", "no-sound--wrong-output"),
        ("Users & access", "users--access"),
        ("Getting HTTPS — for passkeys and push", "getting-https--for-passkeys-and-push"),
        ("2. Sign in — and secure your account", "2-sign-in--and-secure-your-account"),
    ])
    def test_agrees_with_the_in_app_manual(self, heading, in_app_slug):
        """The app and the site must compute the same anchor for the same heading.

        `ag-manual-modal.js` renders the very same Markdown for the in-app reader, and
        the manual's cross-references are written once for both. When the two rules
        disagree, a link works in the app and lands silently at the top of the page on
        the site — which is what shipped.
        """
        assert slugify(heading) == in_app_slug


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
        # No suffix: GitHub Pages serves the page at the extension-less address and
        # 308-redirects the .html one, so linking with it costs a round trip on every click
        # and shows search engines two addresses for one page.
        assert link_between_pages('href="04-listening.md"', self.KNOWN) == 'href="04-listening"'

    def test_carries_the_anchor(self):
        assert (link_between_pages('href="04-listening.md#queue"', self.KNOWN)
                == 'href="04-listening#queue"')

    def test_readme_becomes_the_directory(self):
        assert link_between_pages('href="README.md"', self.KNOWN) == 'href=""'

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


class TestStampVersion:
    def test_states_the_release_under_the_title(self):
        out = stamp_version("<h1>Manual</h1><p>body</p>", "0.9.31")
        assert ('<h1>Manual</h1>\n'
                '<p class="man-version">Describes Audiogravi<sup>ty</sup> v0.9.31</p>') in out

    def test_inserts_once_even_with_later_headings(self):
        out = stamp_version("<h1>A</h1><h1>B</h1>", "1.0.0")
        assert out.count("man-version") == 1

    def test_falls_back_to_the_top_when_there_is_no_title(self):
        out = stamp_version("<p>body</p>", "0.9.31")
        assert out.startswith('<p class="man-version">')


class TestReadVersion:
    def test_reads_the_badge_the_release_script_writes(self, tmp_path, monkeypatch):
        import gen_manual_html as g
        (tmp_path / "README.md").write_text(
            'x <img src="https://img.shields.io/badge/version-0.9.31_beta-blue" /> y')
        monkeypatch.setattr(g, "REPO_DIR", tmp_path)
        assert g.read_version() == "0.9.31"

    @pytest.mark.parametrize("badge, version", [
        ("version-1.0.0--rc.1-blue", "1.0.0-rc.1"),
        ("version-1.0.0--rc.10-orange", "1.0.0-rc.10"),
        ("version-1.0.0-blue", "1.0.0"),
        ("version-1.2.3--beta.2_beta-blue", "1.2.3-beta.2"),
    ])
    def test_a_pre_release_keeps_its_suffix(self, tmp_path, monkeypatch, badge, version):
        """The badge doubles the dash of a pre-release; the manual of a release candidate must
        not claim to describe the final release."""
        import gen_manual_html as g
        (tmp_path / "README.md").write_text(f'<img src="https://img.shields.io/badge/{badge}" />')
        monkeypatch.setattr(g, "REPO_DIR", tmp_path)
        assert g.read_version() == version

    def test_fails_loudly_when_the_badge_is_gone(self, tmp_path, monkeypatch):
        """Silently omitting the version is the drift this line exists to prevent."""
        import gen_manual_html as g
        (tmp_path / "README.md").write_text("no badge here")
        monkeypatch.setattr(g, "REPO_DIR", tmp_path)
        with pytest.raises(SystemExit):
            g.read_version()


class TestPage:
    def test_canonical_is_written_exactly_as_given(self):
        out = page("Listening", "<p>x</p>", TOC, "04-listening", "04-listening")
        assert ('<link rel="canonical" '
                'href="https://audiogravity.app/docs/manual/04-listening">') in out

    def test_canonical_of_the_contents_page_is_the_directory(self):
        """Derived from the chapter id, this produced `/docs/manual/.html` — a 404, which is
        the one address a canonical link must never carry."""
        out = page("Contents", "<p>x</p>", TOC, "", "")
        assert '<link rel="canonical" href="https://audiogravity.app/docs/manual/">' in out
        assert "/docs/manual/.html" not in out

    def test_marks_the_active_chapter_for_assistive_technology(self):
        """Once in each list — the sidebar and the phone's menu, one of them hidden at any
        width, so a reader is told it once."""
        out = page("Listening", "", TOC, "04-listening", "04-listening")
        assert 'href="04-listening" aria-current="page"' in out
        assert out.count('aria-current="page"') == 2

    def test_contents_page_marks_no_chapter_active(self):
        """Its lists mark no chapter; the top bar marks the manual, as the page it is."""
        out = page("Contents", "", TOC, "", "")
        assert all("aria-current" not in found for found in _lists(out))
        assert '<a href="../manual/" aria-current="page">Manual</a>' in out

    def test_lists_every_chapter_in_the_sidebar_and_in_the_phone_menu(self):
        out = page("Contents", "", TOC, "", "")
        assert out.count('class="man-nav-item') == 2 * len(TOC)

    def test_the_way_back_carries_the_app_icon_and_names_itself(self):
        """Two ways home per page: this one and the footer link. The icon is decorative — the
        link is named by aria-label, not by an alt text repeating the wordmark beside it."""
        out = page("Listening", "", TOC, "04-listening", "04-listening")
        assert 'href="../../index.html" aria-label="Audiogravity home"' in out
        assert 'class="man-home-icon" src="../../assets/icons/apple-touch-180.png" alt=""' in out
        assert out.count('href="../../index.html"') == 2  # top bar and footer

    def test_strips_markup_from_the_document_title(self):
        out = page("About Audiogravi<sup>ty</sup>", "", TOC, "", "")
        assert "<title>About Audiogravity — Audiogravity manual</title>" in out

class TestSectionLinks:
    """The top bar links to the sections of the page's family (2026-11-01). It named only the
    section being read, in 10px capitals: a reader who came in on a guide reached the blog through
    the landing. The guides and the blog link to each other; the manual stands alone."""

    @staticmethod
    def _bar(out):
        return re.search(r'<header class="man-top">(.*?)</header>', out, re.S).group(1)

    @staticmethod
    def _sections(out):
        return re.findall(r'<a href="\.\./(\w+)/"[^>]*>(\w+)</a>', TestSectionLinks._bar(out))

    def test_a_guide_or_a_post_links_the_guides_and_the_blog(self):
        import gen_manual_html as g
        for section in (g.GUIDES, g.BLOG):
            out = g.page("x", "", [("a", "A")], "a", "a", section)
            assert self._sections(out) == [("guides", "Guides"), ("blog", "Blog")], section.crumb

    def test_the_manual_names_the_manual_alone(self):
        """The product's documentation, read by its owners: a guide that has something to say
        about Audiogravity links to the chapter that says it, in its own text."""
        out = page("Listening", "", TOC, "04-listening", "04-listening")
        assert self._sections(out) == [("manual", "Manual")]

    def test_marks_the_section_being_read(self):
        import gen_manual_html as g
        bar = self._bar(g.page("x", "", [("a", "A")], "a", "a", g.GUIDES))
        assert '<a href="../guides/" aria-current="true">Guides</a>' in bar
        assert bar.count("aria-current") == 1

    def test_on_its_front_page_the_section_is_the_page(self):
        import gen_manual_html as g
        bar = self._bar(g.page("Blog", "", [("a", "A")], "", "", g.BLOG))
        assert '<a href="../blog/" aria-current="page">Blog</a>' in bar

    def test_a_section_without_pages_gets_no_link(self, tmp_path, monkeypatch):
        import gen_manual_html as g
        monkeypatch.setattr(g, "BLOG_DIR", tmp_path / "blog")
        assert g.present_sections() == (g.MANUAL, g.GUIDES)
        out = g.page("x", "", [("a", "A")], "a", "a", g.GUIDES, sections=g.present_sections())
        assert self._sections(out) == [("guides", "Guides")]

    def test_every_page_built_links_the_sections_of_its_family(self):
        import gen_manual_html as g
        for pages, count in ((build(), 1), (g.build_guides() | g.build_blog(), 2)):
            for path, text in pages.items():
                assert self._bar(text).count('<a href="../') == count, path.name

    def test_the_wordmark_gives_way_on_the_narrowest_phones_and_the_link_keeps_its_name(self):
        """A guide's bar needs 344px with it (Chromium, 2026-11-01): below 360 the logo stays
        alone, and the link is still named for assistive technology."""
        out = page("Listening", "", TOC, "04-listening", "04-listening")
        assert '<span class="man-home-word">Audiogravi<sup>ty</sup></span></a>' in out
        assert 'aria-label="Audiogravity home"' in out
        css = (REPO_DIR / "assets" / "manual.css").read_text(encoding="utf-8")
        rule = re.search(r"@media\(max-width:359px\)\s*\{\s*\.man-home-word\s*\{([^}]*)\}", css)
        assert rule and re.search(r"display:\s*none", rule.group(1))


class TestFrontPages:
    """The front page of the guides and of the blog keeps the sidebar and the phone's menu,
    though they repeat its list. Left out on 2026-11-01, they were put back the same day: the
    list page then had another frame than the pages it leads to, and the text jumped 134px to
    the right at the click on a guide (Chromium, 1440px)."""

    def test_the_guides_and_the_blog_keep_their_frame_on_their_front_page(self):
        import gen_manual_html as g
        for folder, pages in ((g.GUIDES_DIR, g.build_guides()), (g.BLOG_DIR, g.build_blog())):
            front = pages[folder / "index.html"]
            assert len(_lists(front)) == 2 and '<details class="man-menu">' in front, folder.name


def _lists(out):
    """The page lists of a page: the phone's menu's, then the sidebar's."""
    return re.findall(r'<nav class="man-nav"[^>]*>(.*?)</nav>', out, re.S)


class TestPhoneMenu:
    """On a phone the page list is a menu, closed until asked for: the strip it replaces ran
    to 4,424px for the guides on a 375px phone, not one title whole (2026-10-21)."""

    def test_holds_the_same_list_as_the_sidebar(self):
        out = page("Listening", "", TOC, "04-listening", "04-listening")
        menu, sidebar = _lists(out)
        assert menu == sidebar and menu.count('class="man-nav-item') == len(TOC)

    def test_comes_closed_and_names_the_section_and_its_count(self):
        out = page("Listening", "", TOC, "04-listening", "04-listening")
        assert '<details class="man-menu">' in out          # no `open`: the page comes first
        assert '<summary><span>All chapters</span><span class="man-menu-count">2</span>' in out

    def test_sits_above_the_text_and_the_sidebar(self):
        out = page("Listening", "<p>x</p>", TOC, "04-listening", "04-listening")
        assert out.index('<details class="man-menu">') < out.index('<div class="man-shell">')

    def test_the_guides_call_it_all_guides(self):
        import gen_manual_html as g
        out = g.page("x", "", [("a", "A"), ("b", "B"), ("c", "C")], "a", "a", g.GUIDES)
        assert '<summary><span>All guides</span><span class="man-menu-count">3</span>' in out


class TestBuildCanonicals:
    """What build() actually puts in the canonical, as opposed to what page() echoes back.

    Every other test here calls page() directly, so all of them passed while build() was
    handing it an address that redirects — GitHub Pages serves these pages without the
    ``.html`` suffix and 308s the suffixed one to them. A canonical naming a redirect is the
    one thing a canonical must never do, and nothing in the suite could see it.
    """

    def test_no_canonical_carries_a_suffix_that_redirects(self):
        import gen_manual_html as g
        for path, content in (g.build() | g.build_guides()).items():
            m = re.search(r'<link rel="canonical" href="([^"]+)">', content)
            assert m, f"{path.name} has no canonical"
            assert not m.group(1).endswith(".html"), (
                f"{path.name} points at {m.group(1)}, which GitHub Pages redirects"
            )

    def test_each_chapter_names_its_own_address(self):
        import gen_manual_html as g
        pages = g.build()
        chapter = next(p for p in pages if p.name == "04-listening.html")
        assert 'href="https://audiogravity.app/docs/manual/04-listening">' in pages[chapter]

    def test_the_contents_page_names_the_directory(self):
        import gen_manual_html as g
        pages = g.build()
        index = next(p for p in pages if p.name == "index.html")
        assert 'href="https://audiogravity.app/docs/manual/">' in pages[index]


class TestSitemap:
    """The sitemap is written with the pages, from the same Contents list and the same address
    function, so it cannot announce a chapter that has no page or miss one that has."""

    def test_lists_the_landing_the_contents_then_each_chapter_in_order(self):
        import gen_manual_html as g
        locs = re.findall(r"<loc>([^<]+)</loc>", g.sitemap(TOC))
        assert locs == [
            "https://audiogravity.app/",
            "https://audiogravity.app/docs/manual/",
            "https://audiogravity.app/docs/manual/00-quick-start",
            "https://audiogravity.app/docs/manual/04-listening",
        ]

    def test_is_a_sitemap_document(self):
        import xml.etree.ElementTree as ET
        import gen_manual_html as g
        root = ET.fromstring(g.sitemap(TOC))
        assert root.tag == "{http://www.sitemaps.org/schemas/sitemap/0.9}urlset"
        assert len(root) == len(TOC) + 2

    def test_names_each_page_at_the_address_its_canonical_gives(self):
        """A sitemap address that differs from the page's canonical — a suffix, a missing
        slash — sends search engines to an address the page itself disowns."""
        import gen_manual_html as g
        canonicals = {re.search(r'<link rel="canonical" href="([^"]+)">', text).group(1)
                      for text in (g.build() | g.build_guides() | g.build_blog()).values()}
        listed = set(re.findall(r"<loc>([^<]+)</loc>", g.outputs()[g.SITEMAP]))
        assert listed == canonicals | {g.SITE_URL}

    def test_lists_the_guides_after_the_manual(self):
        import gen_manual_html as g
        locs = re.findall(r"<loc>([^<]+)</loc>", g.sitemap(TOC, ["hqplayer-on-a-pi"]))
        assert locs[-2:] == ["https://audiogravity.app/docs/guides/",
                             "https://audiogravity.app/docs/guides/hqplayer-on-a-pi"]

    def test_lists_no_guides_page_while_there_is_no_guide(self):
        import gen_manual_html as g
        assert "docs/guides" not in g.sitemap(TOC, [])

    def test_lists_the_blog_after_the_guides(self):
        import gen_manual_html as g
        locs = re.findall(r"<loc>([^<]+)</loc>", g.sitemap(TOC, ["hqplayer-on-a-pi"], ["naim-nait-2"]))
        assert locs[-4:] == ["https://audiogravity.app/docs/guides/",
                             "https://audiogravity.app/docs/guides/hqplayer-on-a-pi",
                             "https://audiogravity.app/docs/blog/",
                             "https://audiogravity.app/docs/blog/naim-nait-2"]

    def test_lists_no_blog_page_while_there_is_no_post(self):
        import gen_manual_html as g
        assert "docs/blog" not in g.sitemap(TOC, ["hqplayer-on-a-pi"], [])

    def test_a_run_writes_the_pages_and_the_sitemap_at_the_root(self):
        import gen_manual_html as g
        files = g.outputs()
        assert g.SITEMAP == REPO_DIR / "sitemap.xml"
        assert set(files) == set(g.build()) | set(g.build_guides()) | set(g.build_blog()) | {g.SITEMAP}

    def test_the_committed_sitemap_is_current(self):
        """What --check holds a release to, and what the Manual workflow keeps true on a push."""
        import gen_manual_html as g
        assert g.SITEMAP.read_text(encoding="utf-8") == g.outputs()[g.SITEMAP]


class TestGuides:
    """The guides share the manual's shell and pipeline; what differs is checked here, and so
    is everything they point at, since nothing else reads them."""

    README = (
        "# Guides\n\nAnswers to forum questions.\n\n"
        "- [HQPlayer on a Pi](hqplayer-on-a-pi.md) — How to run it, by Audiogravi<sup>ty</sup>.\n"
        "- [NAA on a Pi](naa-on-a-pi.md) — The other end of the network.\n"
        "- [Not a guide](elsewhere.md)\n"
    )

    def test_reads_each_guide_with_its_summary_in_order(self):
        import gen_manual_html as g
        assert g.parse_guides(self.README) == [
            ("hqplayer-on-a-pi", "HQPlayer on a Pi", "How to run it, by Audiogravi<sup>ty</sup>."),
            ("naa-on-a-pi", "NAA on a Pi", "The other end of the network."),
        ]

    def _page(self):
        import gen_manual_html as g
        toc = [("hqplayer-on-a-pi", "HQPlayer on a Pi"), ("naa-on-a-pi", "NAA on a Pi")]
        return g.page("HQPlayer on a Pi", "<p>x</p>", toc, "hqplayer-on-a-pi", "hqplayer-on-a-pi",
                      g.GUIDES, g.plain_text("How to run it, by Audiogravi<sup>ty</sup>."))

    def test_a_guide_page_names_its_address_and_its_question(self):
        out = self._page()
        assert '<link rel="canonical" href="https://audiogravity.app/docs/guides/hqplayer-on-a-pi">' in out
        assert "<title>HQPlayer on a Pi — Audiogravity</title>" in out

    def test_its_search_snippet_is_its_summary_without_markup(self):
        """An attribute shows a tag as typed: the brand is written plain there."""
        assert '<meta name="description" content="How to run it, by Audiogravity.">' in self._page()

    def test_reads_a_numbered_list_as_it_reads_bullets(self):
        """The README lists its guides as bullets under their themes; a numbered line, as it
        wrote them until 2026-11-01, reads the same."""
        import gen_manual_html as g
        assert g.parse_guides(self.README.replace("- [", "1. [")) == g.parse_guides(self.README)

    def test_it_is_filed_under_guides_without_numbers(self):
        """Filed by theme, a guide's rank would only say where it happens to sit (2026-11-01)."""
        out = self._page()
        assert '<a href="../guides/" aria-current="true">Guides</a>' in out
        assert '<nav class="man-nav" aria-label="Guides">' in out
        assert 'href="hqplayer-on-a-pi" aria-current="page"><span>HQPlayer on a Pi</span></a>' in out
        assert "man-nav-n" not in out

    def test_a_label_with_markup_stays_one_piece_in_the_sidebar(self):
        """The sidebar item is a flex row: unwrapped, "Audiogravi<sup>ty</sup>, Volumio or moOde"
        became three flex items set side by side, like columns."""
        import gen_manual_html as g
        toc = [("ag-vs", "Audiogravi<sup>ty</sup>, Volumio or moOde")]
        out = g.page("x", "", toc, "ag-vs", "ag-vs", g.GUIDES)
        assert '><span>Audiogravi<sup>ty</sup>, Volumio or moOde</span></a>' in out
        chapter = page("Listening", "", TOC, "04-listening", "04-listening")
        assert '<span class="man-nav-n">04</span><span>Listening</span></a>' in chapter

    def test_it_carries_no_trademark_notice(self):
        """The notice speaks for the product, which a guide is not about."""
        assert "man-notice" not in self._page()

    def test_the_manual_keeps_its_own_labels(self):
        out = page("Listening", "", TOC, "04-listening", "04-listening")
        assert '<a href="../manual/" aria-current="true">Manual</a>' in out
        assert '<span class="man-nav-n">04</span>' in out
        assert "<title>Listening — Audiogravity manual</title>" in out

    def test_no_guides_folder_means_no_guide_pages(self, tmp_path, monkeypatch):
        import gen_manual_html as g
        monkeypatch.setattr(g, "GUIDES_DIR", tmp_path / "guides")
        assert g.build_guides() == {}

    def test_a_guide_listed_but_missing_stops_the_run(self, tmp_path, monkeypatch):
        import gen_manual_html as g
        (tmp_path / "README.md").write_text(self.README)
        monkeypatch.setattr(g, "GUIDES_DIR", tmp_path)
        with pytest.raises(SystemExit):
            g.build_guides()

    def test_a_readme_listing_nothing_stops_the_run(self, tmp_path, monkeypatch):
        """A summary wrapped onto a second line does not match: better a stop than no page."""
        import gen_manual_html as g
        (tmp_path / "README.md").write_text("# Guides\n\n- [A guide](a-guide.md) —\n  its summary\n")
        monkeypatch.setattr(g, "GUIDES_DIR", tmp_path)
        with pytest.raises(SystemExit):
            g.build_guides()


def links_that_land(pages: dict[Path, str], folder: Path, own: set[str]) -> int:
    """Check that every relative link and image of a section's pages reaches something.

    A page links into the manual by chapter and heading, to the guides and the posts, to files
    of the site such as a kept copy, and to its own figures; a heading reworded, a page renamed
    or a figure moved breaks it without a sound.

    Args:
        pages: The section's rendered pages, by path.
        folder: The section's folder, where its own figures sit under ``images/``.
        own: Ids of the section's pages, which it links to by bare id.

    Returns:
        How many links and images were checked, so a caller can tell the page was read at all.
    """
    import gen_manual_html as g
    chapters = {cid for cid, _ in parse_toc((MANUAL_DIR / "README.md").read_text(encoding="utf-8"))}
    sections = {"../guides/": {gid for gid, _, _ in g.read_guides()},
                "../blog/": {pid for pid, _, _, _ in g.read_posts()}}
    checked = 0
    for path, text in pages.items():
        for target in re.findall(r'\s(?:href|src)="(?!https?:|mailto:|#)([^"]+)"', text):
            target = target.split("?v=")[0]
            where, _, anchor = target.partition("#")
            other = next((s for s in sections if where.startswith(s)), None)
            if where.startswith("../manual/"):
                chapter = where[len("../manual/"):]
                if chapter.startswith("images/"):
                    assert (MANUAL_DIR / chapter).is_file(), f"{path.name}: {target}"
                else:
                    assert chapter in chapters | {""}, f"{path.name}: {target}"
                    if anchor:
                        assert anchor in heading_ids((MANUAL_DIR / f"{chapter}.md").read_text(encoding="utf-8")), f"{path.name}: {target}"
            elif other:
                assert where[len(other):] in sections[other] | {""}, f"{path.name}: {target}"
            elif where.startswith("../../"):
                assert (REPO_DIR / where[len("../../"):]).is_file(), f"{path.name}: {target}"
            elif where.startswith("images/"):
                assert (folder / where).is_file(), f"{path.name}: {target}"
            else:
                # "./" is the section's front page, which the foot of each page leads back to.
                assert where in own | {"", "./"}, f"{path.name}: {target}"
            checked += 1
    return checked


class TestPublishedGuides:
    """The guides as they are in docs/guides."""

    @staticmethod
    def _guides():
        import gen_manual_html as g
        return g.read_guides()

    def test_every_guide_written_is_listed(self):
        """A guide missing from the README gets no page, and nothing would say so."""
        import gen_manual_html as g
        listed = {gid for gid, _, _ in self._guides()}
        written = {p.stem for p in g.GUIDES_DIR.glob("*.md")} - {"README"}
        assert written and written == listed

    def test_every_snippet_fits_a_search_result(self):
        import gen_manual_html as g
        snippets = [re.search(r'<meta name="description" content="([^"]*)">', text).group(1)
                    for text in g.build_guides().values()]
        assert len(snippets) == len(self._guides()) + 1
        for s in snippets:
            assert 70 <= len(html.unescape(s)) <= 155, s

    def test_every_link_and_image_of_a_guide_lands(self):
        """A guide links into the manual by chapter and heading, and borrows its figures: a
        heading reworded or a figure renamed there breaks the guide without a sound."""
        import gen_manual_html as g
        assert links_that_land(g.build_guides(), g.GUIDES_DIR,
                               {gid for gid, _, _ in self._guides()}) > 20

    def test_every_guide_says_its_reading_time(self):
        """Under its title, and again in the list of guides."""
        import gen_manual_html as g
        pages = g.build_guides()
        for gid, _, _ in self._guides():
            assert re.search(r'<p class="man-guide-meta">\d+ min read</p>',
                             pages[g.GUIDES_DIR / f"{gid}.html"]), gid
        assert pages[g.GUIDES_DIR / "index.html"].count('class="man-guide-time"') == len(self._guides())

    def test_every_guide_is_filed_under_a_theme(self):
        """A guide above the first theme would sit under none; a theme alone says little."""
        import gen_manual_html as g
        themes = g.parse_guide_groups((g.GUIDES_DIR / "README.md").read_text(encoding="utf-8"))
        assert self._guides()[0][0] in themes
        assert len(themes) >= 2

    def test_the_list_gives_each_guide_an_entry_under_its_theme(self):
        import gen_manual_html as g
        front = g.build_guides()[g.GUIDES_DIR / "index.html"]
        themes = g.parse_guide_groups((g.GUIDES_DIR / "README.md").read_text(encoding="utf-8"))
        assert front.count('<li class="man-entry">') == len(self._guides())
        assert front.count('<ul class="man-entries">') == len(themes)


class TestBlog:
    """The blog shares the guides' shell and build; a post is dated where a guide is numbered."""

    README = (
        "# Blog\n\nStories about hi-fi equipment.\n\n"
        "- [The Naim NAIT 2](naim-nait-2.md) — 2026-10-31 — Naim's small amplifier, by Audiogravi<sup>ty</sup>.\n"
        "- [An older post](older-post.md) — 2026-09-01 — Before it.\n"
        "- [Not a post](elsewhere.md) — no date — so it is not read\n"
    )

    def test_reads_each_post_with_its_date_and_summary_in_order(self):
        import gen_manual_html as g
        assert g.parse_posts(self.README) == [
            ("naim-nait-2", "The Naim NAIT 2", "Naim's small amplifier, by Audiogravi<sup>ty</sup>.", "2026-10-31"),
            ("older-post", "An older post", "Before it.", "2026-09-01"),
        ]

    def _page(self):
        import gen_manual_html as g
        toc = [("naim-nait-2", "The Naim NAIT 2"), ("older-post", "An older post")]
        return g.page("The Naim NAIT 2", "<p>x</p>", toc, "naim-nait-2", "naim-nait-2",
                      g.BLOG, g.plain_text("Naim's small amplifier, by Audiogravi<sup>ty</sup>."))

    def test_a_post_page_names_its_address_and_its_title(self):
        out = self._page()
        assert '<link rel="canonical" href="https://audiogravity.app/docs/blog/naim-nait-2">' in out
        assert "<title>The Naim NAIT 2 — Audiogravity</title>" in out
        assert '<meta name="description" content="Naim&#x27;s small amplifier, by Audiogravity.">' in out

    def test_it_is_filed_under_the_blog_without_numbers(self):
        """A post's place in the list moves with each new one: it is dated, not numbered."""
        out = self._page()
        assert '<a href="../blog/" aria-current="true">Blog</a>' in out
        assert '<nav class="man-nav" aria-label="Blog posts">' in out
        assert '<summary><span>All posts</span><span class="man-menu-count">2</span>' in out
        assert 'href="naim-nait-2" aria-current="page"><span>The Naim NAIT 2</span></a>' in out
        assert "man-nav-n" not in out

    def test_it_carries_no_trademark_notice(self):
        assert "man-notice" not in self._page()

    def test_a_post_says_its_date_and_reading_time_under_its_title(self):
        import gen_manual_html as g
        assert g.stamp_post_meta("<h1>NAIT 2</h1>\n<p>Body</p>", "2026-10-31", 6) == (
            '<h1>NAIT 2</h1>\n<p class="man-post-meta"><time datetime="2026-10-31">31 October 2026'
            '</time> · 6 min read</p>\n<p>Body</p>')

    def test_no_blog_folder_means_no_blog_pages(self, tmp_path, monkeypatch):
        import gen_manual_html as g
        monkeypatch.setattr(g, "BLOG_DIR", tmp_path / "blog")
        assert g.build_blog() == {}
        assert g.read_posts() == []

    def test_a_post_listed_but_missing_stops_the_run(self, tmp_path, monkeypatch):
        import gen_manual_html as g
        (tmp_path / "README.md").write_text(self.README)
        monkeypatch.setattr(g, "BLOG_DIR", tmp_path)
        with pytest.raises(SystemExit):
            g.build_blog()

    def test_a_date_that_is_no_date_stops_the_run(self, tmp_path, monkeypatch):
        """Read as written, 2026-02-30 would be published; better a stop than a page that lies."""
        import gen_manual_html as g
        (tmp_path / "README.md").write_text("# Blog\n\nx\n\n- [A post](a-post.md) — 2026-02-30 — Its summary.\n")
        (tmp_path / "a-post.md").write_text("# A post\n")
        monkeypatch.setattr(g, "BLOG_DIR", tmp_path)
        with pytest.raises(SystemExit, match="2026-02-30"):
            g.build_blog()

    def test_a_readme_listing_nothing_stops_the_run(self, tmp_path, monkeypatch):
        """A post without its date does not match: better a stop than no page."""
        import gen_manual_html as g
        (tmp_path / "README.md").write_text("# Blog\n\n- [A post](a-post.md) — Its summary.\n")
        monkeypatch.setattr(g, "BLOG_DIR", tmp_path)
        with pytest.raises(SystemExit):
            g.build_blog()


class TestPublishedBlog:
    """The blog as it is in docs/blog."""

    @staticmethod
    def _posts():
        import gen_manual_html as g
        return g.read_posts()

    def test_every_post_written_is_listed(self):
        """A post missing from the README gets no page, and nothing would say so."""
        import gen_manual_html as g
        listed = {pid for pid, _, _, _ in self._posts()}
        written = {p.stem for p in g.BLOG_DIR.glob("*.md")} - {"README"}
        assert written and written == listed

    def test_the_list_is_newest_first(self):
        dates = [date for _, _, _, date in self._posts()]
        assert dates == sorted(dates, reverse=True)

    def test_every_snippet_fits_a_search_result(self):
        import gen_manual_html as g
        snippets = [re.search(r'<meta name="description" content="([^"]*)">', text).group(1)
                    for text in g.build_blog().values()]
        assert len(snippets) == len(self._posts()) + 1
        for s in snippets:
            assert 70 <= len(html.unescape(s)) <= 155, s

    def test_every_link_and_image_of_a_post_lands(self):
        import gen_manual_html as g
        assert links_that_land(g.build_blog(), g.BLOG_DIR, {pid for pid, _, _, _ in self._posts()}) > 10

    def test_every_post_says_its_date_and_reading_time(self):
        """Under its title, and again on its card on the blog's front page."""
        import gen_manual_html as g
        pages = g.build_blog()
        front = pages[g.BLOG_DIR / "index.html"]
        assert front.count('<li class="man-card">') == len(self._posts())
        for pid, _, _, date in self._posts():
            assert re.search(rf'<p class="man-post-meta"><time datetime="{date}">[^<]+</time> · \d+ min read</p>',
                             pages[g.BLOG_DIR / f"{pid}.html"]), pid
            assert re.search(rf'<a href="{pid}">[^<]*(?:<[^>]+>[^<]*)*</a></h2><p class="man-card-meta">'
                             rf'<time datetime="{date}">[^<]+</time> · \d+ min read</p>', front), pid

    def test_every_post_has_a_figure_for_its_card(self):
        """A post without one would get a card without one: allowed, but none has yet."""
        import gen_manual_html as g
        front = g.build_blog()[g.BLOG_DIR / "index.html"]
        assert front.count('<img class="man-card-img"') == len(self._posts())


class TestGuideGroups:
    """The guides are filed under themes, the README's second-level headings (2026-11-01): a flat
    list of eighteen, numbered 1 to 18, said nothing of what each was about."""

    README = (
        "# Guides\n\nAnswers.\n\n"
        "## The DAC\n\n"
        "- [DAC HAT](dac-hat.md) — Why it is not seen.\n"
        "- [USB DAC](usb-dac.md) — What it takes.\n\n"
        "## Nothing under it\n\n"
        "### Not a theme\n\n"
        "## The network\n\n"
        "- [NAS](nas.md) — Mount it.\n"
    )

    def test_each_theme_opens_on_its_first_guide(self):
        import gen_manual_html as g
        assert g.parse_guide_groups(self.README) == {"dac-hat": "The DAC", "nas": "The network"}

    def test_the_guides_keep_their_order(self):
        import gen_manual_html as g
        assert [gid for gid, _, _ in g.parse_guides(self.README)] == ["dac-hat", "usb-dac", "nas"]

    def test_a_readme_without_themes_has_none(self):
        import gen_manual_html as g
        assert g.parse_guide_groups("# Guides\n\n- [NAS](nas.md) — Mount it.\n") == {}

    def test_the_sidebar_and_the_menu_name_each_theme_above_its_guides(self):
        import gen_manual_html as g
        toc = [("dac-hat", "DAC HAT"), ("usb-dac", "USB DAC"), ("nas", "NAS")]
        out = g.page("NAS", "", toc, "nas", "nas", g.GUIDES,
                     groups={"dac-hat": "The DAC", "nas": "The network"})
        for found in _lists(out):
            assert re.findall(r'<p class="man-nav-group">([^<]+)</p>', found) == ["The DAC", "The network"]
            assert found.index('href="usb-dac"') < found.index("The network") < found.index('href="nas"')


class TestOutline:
    """A page's parts: under its entry in the sidebar and, on a phone, in a menu under its title
    (2026-11-01). A post ran to 13 screens on a phone and a chapter to 33 parts, with nothing to
    show them or reach one but scrolling."""

    BODY = ('<h1>NAIT 2</h1>\n<p class="man-post-meta">31 October 2026 · 9 min read</p>\n<p>Intro</p>\n'
            '<h2 id="what-it-is">What it is</h2>\n<p>x</p>\n'
            '<h2 id="with-audiogravity">With Audiogravi<sup>ty</sup></h2>\n<p>y</p>\n'
            '<h2 id="sources">See <a href="https://example.org">the sources</a></h2>\n')

    def _page(self, body=None, active="b"):
        import gen_manual_html as g
        return g.page("NAIT 2", self.BODY if body is None else body, [("a", "A"), ("b", "B")],
                      active, active, g.BLOG)

    def test_reads_the_parts_by_their_headings(self):
        """A heading's markup is kept, but not a link: the part's own entry is one."""
        import gen_manual_html as g
        assert g.outline(self.BODY) == [("what-it-is", "What it is"),
                                        ("with-audiogravity", "With Audiogravi<sup>ty</sup>"),
                                        ("sources", "See the sources")]

    def test_the_sidebar_lists_them_under_the_page_entry_and_the_menu_does_not(self):
        menu, sidebar = _lists(self._page())
        assert (sidebar.index('href="b" aria-current="page"')
                < sidebar.index('<ul class="man-outline">')
                < sidebar.index('<li><a href="#what-it-is">What it is</a></li>'))
        assert "man-outline" not in menu

    def test_a_phone_gets_them_in_a_menu_under_the_title_and_its_line(self):
        out = self._page()
        article = out[out.index('<article class="man-md">'):out.index("</article>")]
        assert (article.index('class="man-post-meta"') < article.index('<details class="man-outline-menu">')
                < article.index("<p>Intro</p>"))
        assert '<summary><span>On this page</span><span class="man-menu-count">3</span>' in article

    def test_a_chapter_without_a_line_under_its_title_gets_it_right_after(self):
        body = '<h1>Listening</h1>\n<p>Intro</p>\n<h2 id="a">A</h2>\n<h2 id="b">B</h2>\n'
        out = page("Listening", body, TOC, "04-listening", "04-listening")
        assert '<h1>Listening</h1>\n<details class="man-outline-menu">' in out

    def test_a_page_of_one_part_has_none(self):
        assert "man-outline" not in self._page('<h1>T</h1>\n<h2 id="only">Only</h2>\n<p>x</p>\n')

    def test_a_front_page_has_none(self):
        assert "man-outline" not in self._page(active="")

    def test_every_page_loads_the_script_that_marks_the_part_being_read(self):
        assert '<script src="../../assets/manual-outline.js" defer></script>' in self._page()
        js = (REPO_DIR / "assets" / "manual-outline.js").read_text(encoding="utf-8")
        assert "'.man-outline a[href^=\"#\"]'" in js
        assert "is-current" in js and "aria-current" in js

    def test_every_part_listed_lands_on_its_heading(self):
        import gen_manual_html as g
        checked = 0
        for path, text in (build() | g.build_guides() | g.build_blog()).items():
            ids = set(re.findall(r'<h2 id="([^"]+)"', text))
            for target in re.findall(r'<li><a href="#([^"]+)">', text):
                assert target in ids, f"{path.name}: #{target}"
                checked += 1
        assert checked > 100

    def test_the_sidebar_keeps_its_width_whatever_the_parts(self):
        """A long part's name widened the manual's sidebar page by page, the text beside it
        shifting from one chapter to the next (Chromium, 2026-11-01)."""
        css = (REPO_DIR / "assets" / "manual.css").read_text(encoding="utf-8")
        rule = re.search(r"\n\.man-outline \{([^}]*)\}", css)
        assert rule and re.search(r"contain:\s*inline-size", rule.group(1))


class TestCheckedAndShortAnswer:
    """What sets a guide apart, set apart (2026-11-01): its short answer in a box, and what it was
    checked against under its title, beside its date. Both read as ordinary paragraphs."""

    BODY = ('<h1>DSD</h1>\n<p><strong>Short answer:</strong> three ways.</p>\n'
            '<p>Checked on 2026-10-17 against the\nkernel.</p>\n<p>Text.</p>\n'
            '<h2 id="more">More</h2>\n<p>Checked on 2026-10-18 again, in the text.</p>\n'
            '<p><strong>Short answer:</strong> not this one.</p>\n')

    def test_the_short_answer_gets_its_box(self):
        import gen_manual_html as g
        out = g.box_short_answer(self.BODY)
        assert '<p class="man-short"><strong>Short answer:</strong> three ways.</p>' in out
        assert out.count('class="man-short"') == 1

    def test_the_checked_line_moves_under_the_title_with_its_mark(self):
        import gen_manual_html as g
        out = g.lift_checked(self.BODY)
        assert out.startswith('<h1>DSD</h1>\n<p class="man-checked"><svg class="man-checked-icon"')
        assert ('<span>Checked on 2026-10-17 against the\nkernel.</span></p>\n'
                '<p><strong>Short answer:</strong>') in out
        assert "<p>Checked on 2026-10-17" not in out
        assert "<p>Checked on 2026-10-18 again, in the text.</p>" in out

    def test_a_page_without_them_is_left_as_it_is(self):
        import gen_manual_html as g
        body = "<h1>T</h1>\n<p>Text.</p>\n"
        assert g.lift_checked(body) == body and g.box_short_answer(body) == body

    def test_a_measured_page_says_it_under_its_title_too(self):
        """"Measured on" where the page's figures were measured (the volume guide, 2026-11-01)."""
        import gen_manual_html as g
        out = g.lift_checked("<h1>Volume</h1>\n<p>Short.</p>\n<p>Measured on 2026-10-22 on Debian 13.</p>\n")
        assert out.startswith('<h1>Volume</h1>\n<p class="man-checked">')
        assert "<span>Measured on 2026-10-22 on Debian 13.</span>" in out

    def test_a_disclosure_that_dates_its_sources_stays_in_the_text(self):
        """The comparison opens on its author's interest: set small and grey, it would fade."""
        import gen_manual_html as g
        page_ = g.build_guides()[g.GUIDES_DIR / "audiogravity-volumio-moode.html"]
        assert 'class="man-checked"' not in page_
        assert re.search(r"<p>I make Audiogravi<sup>ty</sup>: read this page with that in mind\.", page_)

    def test_it_comes_after_the_date_and_before_the_phone_outline(self):
        import gen_manual_html as g
        body = g.stamp_post_meta(g.lift_checked(self.BODY), "2026-10-31", 3)
        out = g.page("DSD", body + '<h2 id="end">End</h2>\n', [("a", "A"), ("b", "B")], "b", "b", g.BLOG)
        article = out[out.index('<article class="man-md">'):]
        assert (article.index('class="man-post-meta"') < article.index('class="man-checked"')
                < article.index('<details class="man-outline-menu">') < article.index("Short answer"))

    def test_every_guide_has_its_short_answer_boxed(self):
        import gen_manual_html as g
        pages = g.build_guides()
        for gid, _, _ in g.read_guides():
            assert '<p class="man-short"><strong>Short answer:</strong>' in pages[g.GUIDES_DIR / f"{gid}.html"], gid

    def test_every_page_saying_what_it_was_checked_against_says_it_under_its_date(self):
        import gen_manual_html as g
        lifted = 0
        for path, text in (g.build_guides() | g.build_blog()).items():
            if 'class="man-checked"' in text:
                assert re.search(r'</h1>\n<p class="man-(?:guide|post)-meta">.*?</p>\n<p class="man-checked">',
                                 text, re.S), path.name
                lifted += 1
        assert lifted >= 22

    def test_the_phone_outline_follows_the_lines_under_the_title_in_any_order(self):
        """Its place was found by a pattern that took them in one order only."""
        import gen_manual_html as g
        body = ('<h1>T</h1>\n<p class="man-checked">✓ Checked on 2026-11-01.</p>\n'
                '<p class="man-post-meta">1 November 2026 · 2 min read</p>\n<p>Intro.</p>\n'
                '<h2 id="a">A</h2>\n<h2 id="b">B</h2>\n')
        out = g.page("T", body, [("a", "A"), ("b", "B")], "b", "b", g.BLOG)
        assert ('2 min read</p>\n<details class="man-outline-menu">') in out


class TestPager:
    """The way on at the foot of a page (2026-11-01): every page ended on the way home alone."""

    TOC3 = [("a", "First"), ("b", "Second"), ("c", "Third")]

    def _pager(self, active, section=None):
        import gen_manual_html as g
        out = g.page("x", "", self.TOC3, active, active, section or g.GUIDES)
        m = re.search(r'<nav class="man-pager"[^>]*>(.*?)</nav>', out, re.S)
        return m.group(1) if m else None

    def test_a_page_leads_to_the_one_before_it_and_the_one_after(self):
        found = self._pager("b")
        assert ('<a class="man-pager-prev" href="a" rel="prev"><span class="man-pager-dir">← Previous guide'
                '</span><span class="man-pager-title">First</span></a>') in found
        assert ('<a class="man-pager-next" href="c" rel="next"><span class="man-pager-dir">Next guide →'
                '</span><span class="man-pager-title">Third</span></a>') in found

    def test_the_ends_of_the_list_lead_one_way(self):
        assert "man-pager-prev" not in self._pager("a") and "man-pager-next" in self._pager("a")
        assert "man-pager-next" not in self._pager("c") and "man-pager-prev" in self._pager("c")

    def test_the_blog_says_newer_and_older(self):
        """Its list runs newest first: the post before one in it is a newer one."""
        import gen_manual_html as g
        found = self._pager("b", g.BLOG)
        assert "← Newer post" in found and "Older post →" in found

    def test_the_manual_says_chapter(self):
        out = page("Quick start", "", TOC, "00-quick-start", "00-quick-start")
        assert ('<span class="man-pager-dir">Next chapter →</span>'
                '<span class="man-pager-title">Listening</span>') in out

    def test_a_front_page_has_none(self):
        assert self._pager("") is None

    def test_it_sits_between_the_text_and_the_footer(self):
        import gen_manual_html as g
        out = g.page("x", "<p>Body</p>", self.TOC3, "b", "b", g.GUIDES)
        assert out.index("</article>") < out.index('<nav class="man-pager"') < out.index('<footer class="man-foot">')

    def test_the_footer_leads_back_to_the_list_from_a_page_of_it(self):
        import gen_manual_html as g
        out = g.page("x", "", self.TOC3, "b", "b", g.GUIDES)
        assert '<p class="man-foot-links"><a href="./">All guides</a><a href="../../index.html">' in out
        assert 'href="./">All guides</a>' not in g.page("Guides", "", self.TOC3, "", "", g.GUIDES)


class TestBlogCards:
    """The blog's front page lists its posts as cards (2026-11-01): it was the README's bullets,
    the date "2026-10-31" between two dashes in the text, though every post has a figure."""

    POSTS = [("nait-2", "The Naim NAIT 2", "Naim's small amplifier, by Audiogravi<sup>ty</sup>.", "2026-10-31"),
             ("no-figure", "A post without a figure", "Words only.", "2026-09-01")]
    BODIES = {"nait-2": ('<h1>NAIT 2</h1>\n<p>x</p>\n<img loading="lazy" src="images/nait-2.jpg" '
                         'alt="The front of a NAIT 2" width="870" height="606">\n'
                         '<img src="images/second.webp" alt="">'),
              "no-figure": "<h1>Words</h1>\n<p>x</p>"}

    def _cards(self):
        import gen_manual_html as g
        return g.post_cards(self.POSTS, {"nait-2": 9, "no-figure": 2}, self.BODIES)

    def test_one_card_per_post_in_the_readme_order(self):
        assert re.findall(r'<h2 class="man-card-title"><a href="([^"]+)">', self._cards()) == ["nait-2", "no-figure"]

    def test_a_card_shows_the_first_figure_without_repeating_its_description(self):
        """The title beside it says what the post is; the description would be read twice."""
        cards = self._cards()
        assert '<img class="man-card-img" src="images/nait-2.jpg" alt="" width="870" height="606">' in cards
        assert "second.webp" not in cards

    def test_the_first_row_loads_at_once_and_the_others_when_near(self):
        """Deferred, the first figure — the first thing seen — was fetched last."""
        import gen_manual_html as g
        posts = [(f"p{i}", f"P{i}", "S.", "2026-10-31") for i in range(4)]
        bodies = {pid: f'<img src="images/{pid}.webp" alt="x">' for pid, _, _, _ in posts}
        cards = g.post_cards(posts, {pid: 1 for pid, _, _, _ in posts}, bodies)
        figures = re.findall(r'<img class="man-card-img"[^>]*>', cards)
        assert g.EAGER_CARDS == 2
        assert ["loading" in f for f in figures] == [False, False, True, True]

    def test_a_link_written_in_a_card_is_kept_as_text(self):
        """The card's own link lies over the whole card: one under it could not be followed."""
        import gen_manual_html as g
        posts = [("a", "A [linked](b.md) title", "See [the other post](b.md).", "2026-10-31")]
        cards = g.post_cards(posts, {"a": 1}, {"a": "<p>x</p>"})
        assert '<a href="a">A linked title</a></h2>' in cards
        assert '<p class="man-card-summary">See the other post.</p>' in cards

    def test_a_card_gives_the_date_in_full_and_the_reading_time(self):
        assert ('<p class="man-card-meta"><time datetime="2026-10-31">31 October 2026</time>'
                ' · 9 min read</p>') in self._cards()

    def test_a_card_keeps_the_markup_of_its_summary(self):
        assert "<p class=\"man-card-summary\">Naim's small amplifier, by Audiogravi<sup>ty</sup>.</p>" in self._cards()

    def test_a_post_without_a_figure_gets_a_card_without_one(self):
        card = self._cards().split('<li class="man-card">')[2]
        assert "<img" not in card and 'href="no-figure"' in card

    def test_the_cards_take_the_place_of_the_readme_list(self):
        import gen_manual_html as g
        body = ('<h1>Blog</h1>\n<p>Stories.</p>\n<ul>\n<li><a href="nait-2">The Naim NAIT 2</a> — 2026-10-31 — x</li>\n'
                '</ul>\n<p>After.</p>')
        assert g.replace_page_list(body, {"nait-2"}, "<CARDS>") == (
            '<h1>Blog</h1>\n<p>Stories.</p>\n<CARDS>\n<p>After.</p>')

    def test_the_first_figure_of_a_page(self):
        import gen_manual_html as g
        assert g.first_image('<p>x</p><img src="a.webp" alt="A" width="3" height="2">') == {
            "src": "a.webp", "alt": "A", "width": "3", "height": "2"}
        assert g.first_image("<p>No figure.</p>") is None
        assert g.first_image('<img alt="no source">') is None


class TestReadingTime:
    """How long a page takes to read, and where a guide says it."""

    WORDS = " ".join(["word"] * 238)

    def test_is_its_words_over_the_reading_speed_rounded_up(self):
        import gen_manual_html as g
        assert g.READING_WPM == 238
        assert g.reading_minutes(f"<p>{self.WORDS}</p>") == 1
        assert g.reading_minutes(f"<p>{self.WORDS} one</p>") == 2

    def test_counts_what_a_reader_sees_not_the_markup(self):
        import gen_manual_html as g
        alt = " ".join(["alt"] * 500)
        assert g.reading_minutes(f'<p><b>{self.WORDS}</b></p><img alt="{alt}" src="x.webp">') == 1

    def test_keeps_two_table_cells_two_words(self):
        """Cells sit side by side in the HTML: dropping the tags alone would run them together."""
        import gen_manual_html as g
        cells = "".join(f"<td>w{i}</td>" for i in range(239))
        assert g.reading_minutes(f"<table><tr>{cells}</tr></table>") == 2

    def test_is_one_minute_at_the_least(self):
        import gen_manual_html as g
        assert g.reading_minutes("") == 1

    def test_a_guide_says_it_under_its_title(self):
        import gen_manual_html as g
        assert g.stamp_guide_meta("<h1>DSD</h1>\n<p>Body</p>", 5) == (
            '<h1>DSD</h1>\n<p class="man-guide-meta">5 min read</p>\n<p>Body</p>')

    def test_the_list_gives_each_guide_a_line_and_its_summary_under_it(self):
        """It read as one run of text per guide: title, summary and time (2026-11-01)."""
        import gen_manual_html as g
        body = ('<h2 id="dac">DAC</h2>\n<ul>\n<li><a href="dsd">DSD</a> — Three ways.</li>\n'
                '<li><a href="naa">NAA</a> — The other end.</li>\n</ul>\n'
                '<ul>\n<li><a href="https://example.org">Elsewhere</a></li>\n</ul>')
        out = g.stamp_entries(body, {"dsd": 5, "naa": 3})
        assert ('<ul class="man-entries">\n<li class="man-entry"><a class="man-entry-title" href="dsd">DSD</a>'
                '<span class="man-entry-summary">Three ways. <span class="man-guide-time">5 min read</span>'
                '</span></li>') in out
        assert ('<span class="man-entry-summary">The other end. <span class="man-guide-time">3 min read'
                '</span></span></li>\n</ul>') in out
        assert '<ul>\n<li><a href="https://example.org">Elsewhere</a></li>\n</ul>' in out

    def test_a_loose_list_is_laid_out_the_same(self):
        """A blank line between two guides wraps each entry in a paragraph: a theme kept its
        bullets and lost its reading times over it (seen by provoking it, 2026-11-01)."""
        import gen_manual_html as g
        md, known, minutes = g.markdown(), {"dsd", "naa"}, {"dsd": 5, "naa": 3}
        tight = g.stamp_entries(g.render_body(md, "- [DSD](dsd.md) — Three ways.\n"
                                                  "- [NAA](naa.md) — The other end.\n", known), minutes)
        loose = g.stamp_entries(g.render_body(md, "- [DSD](dsd.md) — Three ways.\n\n"
                                                  "- [NAA](naa.md) — The other end.\n", known), minutes)
        assert "<p>" in md.render("- a\n\n- b\n")       # the form this is about
        assert loose == tight and loose.count('<li class="man-entry">') == 2

    def test_a_list_holding_anything_but_guides_is_left_as_it_is(self):
        import gen_manual_html as g
        body = '<ul>\n<li><a href="dsd">DSD</a> — Three ways.</li>\n<li><a href="x">X</a> — Not a guide.</li>\n</ul>'
        assert g.stamp_entries(body, {"dsd": 5}) == body


class TestHeadingIds:
    def test_matches_the_ids_the_pages_carry(self):
        """The landing's links are checked against these: they must be the pages' own."""
        source = "# Title\n\n## Setup\n\n### Sign in — and secure\n\n#### Deep\n"
        assert heading_ids(source) == {"setup", "sign-in--and-secure", "deep"}

    def test_numbers_repeats_as_the_pages_do(self):
        assert heading_ids("## Setup\n\n## Setup\n") == {"setup", "setup-1"}

    def test_ignores_the_chapter_title(self):
        assert heading_ids("# Only a title\n") == set()


# The same cases, character for character, are in audiogravity.ui/js/core/code-highlight.test.js:
# the manual is coloured twice — here for the site, there for the app — and the two must agree.
SHELL_CASES = [
    ("curl -fsSL https://x/install.sh | sudo bash",
     '<span class="hl-cmd">curl</span> <span class="hl-opt">-fsSL</span> https://x/install.sh | '
     '<span class="hl-cmd">sudo</span> <span class="hl-cmd">bash</span>'),
    ("cat /proc/cmdline   # 'memory' missing",
     '<span class="hl-cmd">cat</span> /proc/cmdline   <span class="hl-comment"># \'memory\' missing</span>'),
    ("sudo cp a b.bak-$(date +%F)",
     '<span class="hl-cmd">sudo</span> <span class="hl-cmd">cp</span> a b.bak-<span class="hl-var">$(date +%F)</span>'),
    ("sed -i '1 s/$/ x/' f",
     '<span class="hl-cmd">sed</span> <span class="hl-opt">-i</span> <span class="hl-string">\'1 s/$/ x/\'</span> f'),
    ('echo "a \\"b\\"" \\\n    | sudo tee -a /etc/fstab',
     '<span class="hl-cmd">echo</span> <span class="hl-string">"a \\"b\\""</span> \\\n    | '
     '<span class="hl-cmd">sudo</span> <span class="hl-cmd">tee</span> <span class="hl-opt">-a</span> /etc/fstab'),
    ("bash -s -- \\\n    --email you@example.com",
     '<span class="hl-cmd">bash</span> <span class="hl-opt">-s</span> <span class="hl-opt">--</span> \\\n'
     '    <span class="hl-opt">--email</span> you@example.com'),
    ("tee f >/dev/null <<'EOF'\nuser=a\nEOF\nls",
     '<span class="hl-cmd">tee</span> f &gt;/dev/null &lt;&lt;\'EOF\'\n<span class="hl-string">user=a</span>\n'
     'EOF\n<span class="hl-cmd">ls</span>'),
    ("a 2>&1 && b",
     '<span class="hl-cmd">a</span> 2&gt;&amp;1 &amp;&amp; <span class="hl-cmd">b</span>'),
    ("x#y $HOME ${A} $? $",
     '<span class="hl-cmd">x#y</span> <span class="hl-var">$HOME</span> <span class="hl-var">${A}</span> '
     '<span class="hl-var">$?</span> $'),
    ("printf '<b>' & ls",
     '<span class="hl-cmd">printf</span> <span class="hl-string">\'&lt;b&gt;\'</span> &amp; '
     '<span class="hl-cmd">ls</span>'),
    ("# note\nsudo -E tee x",
     '<span class="hl-comment"># note</span>\n<span class="hl-cmd">sudo</span> <span class="hl-opt">-E</span> '
     '<span class="hl-cmd">tee</span> x'),
    ("echo a\u00a0b",
     '<span class="hl-cmd">echo</span> a&nbsp;b'),
    ("sudo -u audiogravity systemctl status x",
     '<span class="hl-cmd">sudo</span> <span class="hl-opt">-u</span> audiogravity '
     '<span class="hl-cmd">systemctl</span> status x'),
    ("LANG=C sort f",
     '<span class="hl-var">LANG=C</span> <span class="hl-cmd">sort</span> f'),
    ("echo sudo tee",
     '<span class="hl-cmd">echo</span> sudo tee'),
]

JSON_CASES = [
    ('{"a": "b", "n": -1.5e3, "t": true, "z": null}',
     '{<span class="hl-key">"a"</span>: <span class="hl-string">"b"</span>, <span class="hl-key">"n"</span>: '
     '<span class="hl-num">-1.5e3</span>, <span class="hl-key">"t"</span>: <span class="hl-lit">true</span>, '
     '<span class="hl-key">"z"</span>: <span class="hl-null">null</span>}'),
    ('{"k" : "a\\"<b>", "l": [1, false]}',
     '{<span class="hl-key">"k"</span> : <span class="hl-string">"a\\"&lt;b&gt;"</span>, '
     '<span class="hl-key">"l"</span>: [<span class="hl-num">1</span>, <span class="hl-lit">false</span>]}'),
]


def _manual_blocks():
    """Every fenced block of the published manual, as (chapter, language, text).

    A fence may sit up to three spaces in, inside a list item; its lines then lose that much
    indentation, as they do in the renderer.
    """
    fence = re.compile(r"^( {0,3})```(\w*)[^\n]*\n(.*?)^ {0,3}```", re.S | re.M)
    for f in sorted(MANUAL_DIR.glob("*.md")):
        for m in fence.finditer(f.read_text(encoding="utf-8")):
            indent = len(m.group(1))
            yield f.name, m.group(2), re.sub(rf"(?m)^ {{0,{indent}}}", "", m.group(3))


class TestHighlight:
    @pytest.mark.parametrize("code,expected", SHELL_CASES)
    def test_shell(self, code, expected):
        assert highlight_code(code, "bash") == expected

    @pytest.mark.parametrize("code,expected", JSON_CASES)
    def test_json(self, code, expected):
        assert highlight_code(code, "json") == expected

    @pytest.mark.parametrize("lang", ["sh", "shell"])
    def test_shell_aliases_colour_the_same(self, lang):
        code, expected = SHELL_CASES[0]
        assert highlight_code(code, lang) == expected

    @pytest.mark.parametrize("lang", ["", "text", "ini", "python"])
    def test_leaves_other_languages_alone(self, lang):
        assert highlight_code("x = 1", lang) is None

    def test_keeps_every_character_of_every_block_in_the_manual(self):
        """A colourer that drops or doubles a character hands the reader a command that is not
        the one written — the worst thing a copy button can do. Checked on the real blocks."""
        import html as h
        checked = 0
        for name, lang, text in _manual_blocks():
            out = highlight_code(text, lang)
            if out is None:
                continue
            assert h.unescape(re.sub(r"</?span[^>]*>", "", out)) == text, name
            checked += 1
        # 24 at column 0 and 5 inside list items, on 2026-09-26.
        assert checked >= 29, "the manual's blocks were not found — has the fence syntax changed?"


class TestHighlightFence:
    def test_leaves_an_unknown_unflagged_block_to_markdown_it(self):
        assert highlight_fence("x\n", "", "") == ""
        assert highlight_fence("x\n", "ini", "") == ""

    def test_returns_the_whole_block_for_a_coloured_language(self):
        assert highlight_fence("ls\n", "bash", "") == (
            '<pre><code class="language-bash"><span class="hl-cmd">ls</span>\n</code></pre>')

    def test_marks_a_nocopy_block_whatever_its_language(self):
        assert highlight_fence("a <b>\n", "text", "nocopy") == (
            '<pre data-copy="no"><code class="language-text">a &lt;b&gt;\n</code></pre>')
        assert highlight_fence("ls\n", "bash", "nocopy") == (
            '<pre data-copy="no"><code class="language-bash"><span class="hl-cmd">ls</span>\n</code></pre>')

    def test_renders_through_markdown_it(self):
        md = markdown()
        assert md.render("```bash\nls\n```\n") == (
            '<pre><code class="language-bash"><span class="hl-cmd">ls</span>\n</code></pre>\n')
        # An untagged block comes out exactly as it did before colouring existed.
        assert md.render("```\nplain <x>\n```\n") == "<pre><code>plain &lt;x&gt;\n</code></pre>\n"


class TestCopyScript:
    def test_every_page_loads_it_deferred(self):
        out = page("Listening", "", TOC, "04-listening", "04-listening")
        assert '<script src="../../assets/manual-copy.js" defer></script>' in out

    def test_the_script_exists(self):
        assert (REPO_DIR / "assets" / "manual-copy.js").is_file()

    def test_skips_the_blocks_flagged_nocopy(self):
        """The flag is only worth something if the script reads it."""
        js = (REPO_DIR / "assets" / "manual-copy.js").read_text(encoding="utf-8")
        assert "data-copy" in js and "'no'" in js


class TestBackToTop:
    """The manual's pages carry the landing's back-to-top button, built by one shared script."""

    def test_every_page_loads_it_deferred(self):
        for args in (("Listening", "", TOC, "04-listening", "04-listening"), ("Contents", "", TOC, "", "")):
            assert '<script src="../../assets/to-top.js" defer></script>' in page(*args)

    def test_the_script_exists(self):
        assert (REPO_DIR / "assets" / "to-top.js").is_file()

    def test_the_pages_load_the_sheet_that_draws_it(self):
        """The button's look is in the landing's sheet: a page without it shows a bare link."""
        out = page("Listening", "", TOC, "04-listening", "04-listening")
        assert '<link rel="stylesheet" href="../../assets/style.css">' in out
        assert ".to-top {" in (REPO_DIR / "assets" / "style.css").read_text(encoding="utf-8")


class TestThemeToggle:
    """The manual's pages carry the landing's light / dark toggle (2026-10-15): a reader who
    arrived on a chapter from a search had no way to change the theme their system chose."""

    PAGES = (("Listening", "", TOC, "04-listening", "04-listening"), ("Contents", "", TOC, "", ""))

    def test_every_page_has_the_button_in_its_bar(self):
        for args in self.PAGES:
            out = page(*args)
            bar = re.search(r'<header class="man-top">(.*?)</header>', out, re.S).group(1)
            assert 'class="theme-toggle" id="themeToggle" type="button"' in bar
            assert 'aria-label="Toggle dark mode"' in bar
            assert '<svg id="themeIcon"' in bar

    def test_every_page_loads_the_shared_script_deferred(self):
        """Deferred, it runs once the bar is parsed: the button it looks for is there."""
        for args in self.PAGES:
            assert '<script src="../../assets/theme-toggle.js" defer></script>' in page(*args)
        assert (REPO_DIR / "assets" / "theme-toggle.js").is_file()

    def test_the_choice_is_one_for_the_site(self):
        """The script and the inline guard before the first paint read the landing's key: a
        theme switched on the landing holds in the manual, and the other way round."""
        js = (REPO_DIR / "assets" / "theme-toggle.js").read_text(encoding="utf-8")
        assert "var KEY = 'ag-theme';" in js
        assert "localStorage.getItem('ag-theme')" in page(*self.PAGES[0])
        assert "localStorage.getItem('ag-theme')" in (REPO_DIR / "index.html").read_text(encoding="utf-8")

    def test_it_keeps_the_bar_edge_the_landing_leaves_for_its_ribbon(self):
        """style.css moves the landing's toggle 64 to 114px off the corner below 1240px, clear
        of the stage ribbon; the manual has none, so its bar puts the toggle back."""
        css = (REPO_DIR / "assets" / "manual.css").read_text(encoding="utf-8")
        rule = re.search(r"\.man-top \.theme-toggle \{([^}]*)\}", css)
        assert rule, "no rule for the manual's toggle"
        assert re.search(r"margin-left:\s*auto", rule.group(1))
        assert re.search(r"margin-right:\s*0\b", rule.group(1))
        assert 'class="ribbon"' not in page(*self.PAGES[0])

    def test_it_leaves_the_bar_label_on_one_line_at_320px(self):
        """With the toggle, "User manual" broke onto two lines below 327px (Chromium,
        2026-10-15): a 12px gap instead of 16 keeps it on one at 320."""
        css = (REPO_DIR / "assets" / "manual.css").read_text(encoding="utf-8")
        narrow = re.search(r"@media\(max-width:340px\)\s*\{\s*\.man-top\s*\{([^}]*)\}", css)
        assert narrow and re.search(r"gap:\s*12px", narrow.group(1))


class TestAssetStamps:
    """Every page the generator writes asks for its stylesheets and scripts with a stamp of
    their content (scripts/asset_versions.py): Safari showed a new page with a stylesheet kept
    from before the update (2026-10-15)."""

    def test_every_page_built_asks_for_the_current_files(self):
        import gen_manual_html as g
        from asset_versions import out_of_date
        built = build()
        assert len(built) > 10
        for directory, pages in ((MANUAL_DIR, built), (g.GUIDES_DIR, g.build_guides()),
                                 (g.BLOG_DIR, g.build_blog())):
            for path, text in pages.items():
                assert len(re.findall(r'\.(?:css|js)\?v=[0-9a-f]{10}"', text)) == 6, path.name
                assert out_of_date(text, directory) == [], path.name


class TestTrademarkNotice:
    """The notice is shown once wherever the manual is read, never at the end of a chapter."""

    def test_a_chapter_page_carries_it_in_its_footer(self):
        out = page("Listening", "<p>Body</p>", TOC, "04-listening", "04-listening")
        footer = out[out.index('<footer class="man-foot">'):out.index("</footer>")]
        assert '<p class="man-notice">Roon, HQPlayer, AirPlay' in footer
        assert "trademarks of their respective owners. Audiogravi<sup>ty</sup> is not" in footer

    def test_the_contents_page_does_not_repeat_it(self):
        """README.md, the contents page's body, already ends with it."""
        out = page("Contents", "<p>Body</p>", TOC, "", "")
        assert "man-notice" not in out

    def test_the_manual_places_it_as_it_should(self):
        import gen_manual_html as g
        assert g.check_notice() == []

    def test_a_chapter_repeating_it_is_refused(self, tmp_path, monkeypatch):
        import gen_manual_html as g
        (tmp_path / "README.md").write_text("*… are\ntrademarks of their respective owners. …*\n")
        (tmp_path / "04-listening.md").write_text("# Listening\n\n*… trademarks of their\nrespective owners …*\n")
        monkeypatch.setattr(g, "MANUAL_DIR", tmp_path)
        assert g.check_notice() == ["04-listening.md repeats the trademark notice"]

    def test_a_readme_without_it_is_refused(self, tmp_path, monkeypatch):
        import gen_manual_html as g
        (tmp_path / "README.md").write_text("# Manual\n")
        monkeypatch.setattr(g, "MANUAL_DIR", tmp_path)
        assert g.check_notice() == ["README.md lacks the trademark notice"]

    def test_a_readme_carrying_it_outside_italics_is_refused(self, tmp_path, monkeypatch):
        """The app finds it as an italic passage: the site holds the README to the same form."""
        import gen_manual_html as g
        (tmp_path / "README.md").write_text("Names are trademarks of their respective owners.\n")
        monkeypatch.setattr(g, "MANUAL_DIR", tmp_path)
        assert g.check_notice() == ["README.md lacks the trademark notice"]

    def test_the_footer_takes_its_words_from_the_readme(self, tmp_path, monkeypatch):
        """One wording, the README's: nothing to keep in step by hand."""
        import gen_manual_html as g
        (tmp_path / "README.md").write_text("*Names are trademarks\nof their respective owners.*\n")
        monkeypatch.setattr(g, "MANUAL_DIR", tmp_path)
        out = page("Listening", "", TOC, "04-listening", "04-listening")
        assert '<p class="man-notice">Names are trademarks of their respective owners.</p>' in out

    def test_reads_it_as_the_app_does(self):
        import gen_manual_html as g
        md = "*Roon … are\ntrademarks of their respective owners. Audiogravi<sup>ty</sup> is not affiliated.*"
        assert g.read_notice(md) == ("Roon … are trademarks of their respective owners. "
                                     "Audiogravi<sup>ty</sup> is not affiliated.")
        assert g.read_notice("*An italic line.*") is None
