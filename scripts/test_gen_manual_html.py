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
    MANUAL_DIR,
    REPO_DIR,
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
        out = page("Listening", "", TOC, "04-listening", "04-listening")
        assert 'href="04-listening" aria-current="page"' in out
        assert out.count('aria-current="page"') == 1

    def test_contents_page_marks_no_chapter_active(self):
        assert 'aria-current' not in page("Contents", "", TOC, "", "")

    def test_lists_every_chapter_in_the_sidebar(self):
        out = page("Contents", "", TOC, "", "")
        assert out.count('class="man-nav-item') == len(TOC)

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


class TestBuildCanonicals:
    """What build() actually puts in the canonical, as opposed to what page() echoes back.

    Every other test here calls page() directly, so all of them passed while build() was
    handing it an address that redirects — GitHub Pages serves these pages without the
    ``.html`` suffix and 308s the suffixed one to them. A canonical naming a redirect is the
    one thing a canonical must never do, and nothing in the suite could see it.
    """

    def test_no_canonical_carries_a_suffix_that_redirects(self):
        import gen_manual_html as g
        for path, content in g.build().items():
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
