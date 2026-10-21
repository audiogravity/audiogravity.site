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
        assert 'aria-current' not in page("Contents", "", TOC, "", "")

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

    def test_the_crumb_leads_to_the_contents(self):
        """No page of a section linked back to its list: the crumb in the top bar does."""
        out = page("Listening", "", TOC, "04-listening", "04-listening")
        assert '<a class="man-crumb" href="./">User manual</a>' in out


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
                      for text in (g.build() | g.build_guides()).values()}
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

    def test_a_run_writes_the_pages_and_the_sitemap_at_the_root(self):
        import gen_manual_html as g
        files = g.outputs()
        assert g.SITEMAP == REPO_DIR / "sitemap.xml"
        assert set(files) == set(g.build()) | set(g.build_guides()) | {g.SITEMAP}

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

    def test_it_is_filed_under_guides_without_numbers(self):
        out = self._page()
        assert '<a class="man-crumb" href="./">Guides</a>' in out
        assert '<nav class="man-nav" aria-label="Guides">' in out
        assert "man-nav-n" not in out
        assert 'href="hqplayer-on-a-pi" aria-current="page"><span>HQPlayer on a Pi</span></a>' in out

    def test_a_label_with_markup_stays_one_piece_in_the_sidebar(self):
        """The sidebar item is a flex row: unwrapped, "Audiogravi<sup>ty</sup>, Volumio or moOde"
        became three flex items set side by side, like columns."""
        import gen_manual_html as g
        toc = [("ag-vs", "Audiogravi<sup>ty</sup>, Volumio or moOde")]
        out = g.page("x", "", toc, "ag-vs", "ag-vs", g.GUIDES)
        assert '><span>Audiogravi<sup>ty</sup>, Volumio or moOde</span></a>' in out
        chapter = page("Listening", "", TOC, "04-listening", "04-listening")
        assert '<span class="man-nav-n">04</span><span>Listening</span></a>' in chapter

    def test_it_carries_the_trademark_notice(self):
        """A guide names HQPlayer, Roon and the streaming services as much as a chapter does."""
        assert '<p class="man-notice">' in self._page()

    def test_the_manual_keeps_its_own_labels(self):
        out = page("Listening", "", TOC, "04-listening", "04-listening")
        assert '<a class="man-crumb" href="./">User manual</a>' in out
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
        chapters = {cid for cid, _ in parse_toc((MANUAL_DIR / "README.md").read_text(encoding="utf-8"))}
        guides = {gid for gid, _, _ in self._guides()}
        checked = 0
        for path, text in g.build_guides().items():
            for target in re.findall(r'\s(?:href|src)="(?!https?:|mailto:|#)([^"]+)"', text):
                target = target.split("?v=")[0]
                where, _, anchor = target.partition("#")
                if where.startswith("../manual/"):
                    chapter = where[len("../manual/"):]
                    if chapter.startswith("images/"):
                        assert (MANUAL_DIR / chapter).is_file(), f"{path.name}: {target}"
                    else:
                        assert chapter in chapters | {""}, f"{path.name}: {target}"
                        if anchor:
                            assert anchor in heading_ids((MANUAL_DIR / f"{chapter}.md").read_text(encoding="utf-8")), f"{path.name}: {target}"
                elif where.startswith("../../"):
                    assert (REPO_DIR / where[len("../../"):]).is_file(), f"{path.name}: {target}"
                else:
                    # "./" is the guides' contents, which the crumb in the top bar leads to.
                    assert where in guides | {"", "./"}, f"{path.name}: {target}"
                checked += 1
        assert checked > 20


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
        """style.css moves the landing's toggle 34 to 84px off the corner below 1100px, clear
        of the "Public beta" ribbon; the manual has none, so its bar puts the toggle back."""
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
        for directory, pages in ((MANUAL_DIR, built), (g.GUIDES_DIR, g.build_guides())):
            for path, text in pages.items():
                assert len(re.findall(r'\.(?:css|js)\?v=[0-9a-f]{10}"', text)) == 5, path.name
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
