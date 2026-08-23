#!/usr/bin/env python3
"""Render the user manual to static HTML pages for the landing site.

The manual is authored as Markdown in ``audiogravity.site/docs/manual``. Until now the only
readable copy was GitHub's: the landing linked out to ``github.com/.../blob/main/docs/manual``,
which sends a prospective buyer to a code host, and lets GitHub collect the search traffic for
our own documentation.

Why generate rather than render in the browser:

* The landing loads **no third-party script at all** — check ``index.html``, there is not one
  external ``src``. Pulling a Markdown library from a CDN to read documentation would give that
  property away for a page that never changes between deploys.
* The site is GitHub Pages (``CNAME`` + ``.nojekyll``), so there is no build step on the server.
  Whatever is committed is what is served.
* Client-rendered Markdown indexes badly, and being findable is half the point of hosting the
  manual ourselves.

Output lands **next to the Markdown**, in ``docs/manual/``, so the ``images/…`` sources the
chapters already use resolve unchanged — no src rewriting, and the .md and .html copies cannot
drift apart in the file tree.

The chapter list comes from the manual's own README "Contents" list, the same single source of
truth ``ag-manual-modal.js`` parses in the interface. Add a chapter there and it appears here.

It lives in this repo rather than in ``audiogravity.ops``, where the other generators sit: it
reads and writes entirely inside ``audiogravity.site``, and ops is private, so a GitHub Action
running here could not reach it without handing out a token.

Usage::

    python3 scripts/gen_manual_html.py [--check]

``--check`` regenerates into memory and exits non-zero if any committed page is stale, so a
release can fail rather than publish documentation that no longer matches its source.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

try:
    from markdown_it import MarkdownIt
except ImportError:  # pragma: no cover - environment guard
    sys.exit("markdown-it-py is required: pip install markdown-it-py")

REPO_DIR = Path(__file__).resolve().parent.parent
MANUAL_DIR = REPO_DIR / "docs" / "manual"

#: Matches a numbered Contents entry: ``3. [First run](03-first-run.md) — guided audio setup``.
TOC_LINE = re.compile(r"^\s*\d+\.\s*\[(?P<label>.+?)\]\((?P<id>\d{2}-[a-z0-9-]+)\.md\)")

#: Intra-manual links point at ``.md`` files; the generated pages link to each other.
MD_LINK = re.compile(r'href="(?!https?:)(?P<id>[^"#]*?)\.md(?P<anchor>#[^"]*)?"')

BRAND = "Audiogravi<sup>ty</sup>"


def parse_toc(readme: str) -> list[tuple[str, str]]:
    """Extract the ordered chapter list from the manual README.

    Args:
        readme: Contents of ``docs/manual/README.md``.

    Returns:
        ``(chapter_id, label)`` pairs in document order. Inline markup in a label (the brand
        carries ``<sup>``) is kept as authored — these labels are placed into HTML.
    """
    out: list[tuple[str, str]] = []
    for line in readme.split("\n"):
        m = TOC_LINE.match(line)
        if m:
            out.append((m.group("id"), m.group("label")))
    return out


def slugify(text: str) -> str:
    """Turn a heading into a GitHub-style anchor id.

    The manual's cross-references are authored against GitHub's rules, and
    ``ag-manual-modal.js`` implements the same ones, so this has to agree with both or
    a link resolves in the app and lands at the top of the page on the site. Two rules
    are easy to get wrong, and both were:

    * **Runs of whitespace are not collapsed.** GitHub replaces each space with a dash,
      so ``Sign in — and secure`` (dash removed, two spaces left behind) gives
      ``sign-in--and-secure`` with two hyphens, not one.
    * **Entities are decoded first.** The heading arrives as HTML, where ``&`` is
      ``&amp;``; slugifying that produced ``users-amp-access`` — a word that appears in
      no heading — where GitHub gives ``users--access``.

    Underscores survive, for the same reason: GitHub keeps them.

    Args:
        text: Heading text, tags already stripped (entities may remain).

    Returns:
        A lowercase, hyphenated slug, character for character what
        ``ag-manual-modal.js`` computes for the same heading.
    """
    slug = re.sub(r"[^\w\s-]", "", html.unescape(text).strip().lower(), flags=re.UNICODE)
    return re.sub(r"\s", "-", slug)


def stamp_heading_ids(rendered: str) -> str:
    """Give every h2/h3 an anchor id, de-duplicating repeats.

    markdown-it emits no ids, so without this the manual's own cross-references
    (``09-troubleshooting.md#roon``) land at the top of the page instead of the section.

    Args:
        rendered: HTML from markdown-it.

    Returns:
        The same HTML with ``id`` attributes on h2 and h3.
    """
    seen: dict[str, int] = {}

    def add_id(m: re.Match[str]) -> str:
        level, inner = m.group(1), m.group(2)
        base = slugify(re.sub(r"<[^>]+>", "", inner))
        n = seen.get(base, 0)
        seen[base] = n + 1
        anchor = f"{base}-{n}" if n else base
        return f'<h{level} id="{anchor}">{inner}</h{level}>'

    # h2 through h4: a chapter's cross-references reach the deepest heading the author wrote,
    # and a link to a heading with no id lands silently at the top of the page.
    return re.sub(r"<h([234])>(.*?)</h\1>", add_id, rendered, flags=re.S)


def link_between_pages(rendered: str, known: set[str]) -> str:
    """Point intra-manual links at the generated pages rather than the Markdown.

    Only links naming a page this run actually produces are rewritten. A chapter may also link
    out to a document that lives beside the manual rather than in it — ``../../RELEASE_NOTES.md``
    is the case the interface's own link rewriter handles — and there is no generated page for
    those: rewriting them to ``.html`` would turn a working link into a 404.

    Args:
        rendered: HTML from markdown-it.
        known: Page stems this run generates (chapter ids plus ``README``).

    Returns:
        The same HTML with intra-manual ``.md`` hrefs rewritten to ``.html``. Absolute links and
        anything outside the manual are left as authored.
    """
    def swap(m: re.Match[str]) -> str:
        target = m.group("id")
        if target not in known:
            return m.group(0)
        stem = "index" if target == "README" else target
        # No .html: GitHub Pages serves these pages at the extension-less address
        # and 308-redirects the suffixed one. "index" is the directory itself.
        target_href = "" if stem == "index" else stem
        return f'href="{target_href}{m.group("anchor") or ""}"'

    return MD_LINK.sub(swap, rendered)


def read_version() -> str:
    """Read the published version from the repository README's badge.

    Two places in this repo carry a version: the landing's footer, which is maintained by hand
    as a release checklist item, and this badge, which ``update-test-report.sh`` rewrites during
    ``release.sh prepare``. The automated one is the source, so the manual follows a release
    without anyone remembering it.

    Deliberately not ``audiogravity.ops/VERSION``: that file carries ``-dev`` between releases,
    and the manual is published, so it must state what was released, not what is being built.

    Returns:
        The version string, e.g. ``0.9.31``.

    Raises:
        SystemExit: if the badge is gone or reshaped. Failing here is the point — a silently
            omitted version is the drift this line exists to prevent, and it would be invisible.
    """
    readme = (REPO_DIR / "README.md").read_text(encoding="utf-8")
    m = re.search(r"badge/version-(\d+\.\d+\.\d+)", readme)
    if not m:
        sys.exit("no version badge found in README.md — has update-test-report.sh changed shape?")
    return m.group(1)


def stamp_version(rendered: str, version: str) -> str:
    """State which release the manual describes, once, on the contents page.

    On the contents page only, and not on all thirteen: a version on every chapter invites
    "where is the manual for MY version?", which has no answer while only one is published. At
    the entrance it reads as a fact about the document rather than a promise of an archive.

    Args:
        rendered: The contents page body.
        version: Released version, from :func:`read_version`.

    Returns:
        The body with the line inserted after the title.
    """
    # The "v" is presentation and belongs here, not in read_version: the badge carries a bare
    # number, and the landing's footer writes it as v0.9.31 — the manual reads the same way.
    line = f'<p class="man-version">Describes {BRAND} v{html.escape(version)}</p>'
    if "</h1>" in rendered:
        return rendered.replace("</h1>", f"</h1>\n{line}", 1)
    return line + rendered


def lazy_load_images(rendered: str) -> str:
    """Defer images that are not on screen yet.

    An illustrated chapter carries up to six screenshots; without this the browser fetches all
    of them before the reader has scrolled past the first. The interface's reader already does
    this — the same content should not behave differently depending on where it is read.

    Args:
        rendered: HTML from markdown-it.

    Returns:
        The same HTML with ``loading="lazy"`` on every image that lacks it.
    """
    return re.sub(r"<img (?![^>]*\bloading=)", '<img loading="lazy" ', rendered)


def wrap_tables(rendered: str) -> str:
    """Give every table its own horizontal scroll container.

    A comparison table can need more width than a phone has, and it is the one block that cannot
    be reflowed without destroying what it says. Left bare it widens the whole page instead of
    scrolling on its own. Wrapping keeps the ``<table>`` element — and its role for assistive
    technology — rather than restyling it to a block, which is the usual shortcut.

    Args:
        rendered: HTML from markdown-it.

    Returns:
        The same HTML with each table inside ``<div class="man-table">``.
    """
    return re.sub(r"<table>(.*?)</table>",
                  lambda m: f'<div class="man-table"><table>{m.group(1)}</table></div>',
                  rendered, flags=re.S)


def page(title: str, body: str, toc: list[tuple[str, str]], active: str, canonical: str) -> str:
    """Assemble one manual page.

    Args:
        title: Chapter label, may carry inline markup; stripped for ``<title>``.
        body: Rendered chapter HTML.
        toc: Chapter list for the sidebar.
        active: Id of the chapter being rendered, highlighted in the sidebar. Empty on the
            contents page, which is not itself a chapter.
        canonical: Path of this page under the site root, **without the .html suffix**.
            GitHub Pages serves these pages at the extension-less address and 308-redirects
            the ``.html`` one to it, so a canonical carrying the suffix names an address that
            redirects — the one thing a canonical link must never do. Passed in rather than
            derived from ``active``, which has no value on the contents page and produced a
            canonical pointing at ``/docs/manual/.html``.

    Returns:
        A complete HTML document.
    """
    links = "\n".join(
        '            <a class="man-nav-item{cls}" href="{cid}"{cur}>'
        '<span class="man-nav-n">{n:02d}</span>{label}</a>'.format(
            cls=" active" if cid == active else "",
            # Assistive technology reads aria-current; the class only paints a border.
            cur=' aria-current="page"' if cid == active else "",
            cid=cid,
            n=int(cid[:2]),
            label=label,
        )
        for cid, label in toc
    )
    plain = re.sub(r"<[^>]+>", "", title)
    return f"""<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    <title>{html.escape(plain)} — Audiogravity manual</title>
    <meta name="description" content="Audiogravity user manual — {html.escape(plain)}.">
    <link rel="canonical" href="https://audiogravity.app/docs/manual/{canonical}">
    <link rel="icon" href="../../assets/icons/favicon.ico" sizes="any">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="../../assets/style.css">
    <link rel="stylesheet" href="../../assets/manual.css">
    <script>
        /* Applied before first paint: reading the stored theme after the stylesheet has painted
           shows a flash of the wrong one. Same key as the landing, so the toggle carries over. */
        (function () {{
            try {{
                var t = localStorage.getItem('ag-theme');
                if (t) document.documentElement.setAttribute('data-theme', t);
            }} catch (e) {{ /* private mode: fall back to the media query */ }}
        }})();
    </script>
</head>

<body class="man-body">
    <header class="man-top">
        <a class="man-home" href="../../index.html" aria-label="Audiogravity home">
            <img class="man-home-icon" src="../../assets/icons/apple-touch-180.png" alt=""
                 width="28" height="28" decoding="async">{BRAND}</a>
        <span class="man-crumb">User manual</span>
    </header>

    <div class="man-shell">
        <nav class="man-nav" aria-label="Manual chapters">
{links}
        </nav>

        <main class="man-main">
            <article class="man-md">
{body}
            </article>
            <footer class="man-foot">
                <a href="../../index.html">← Back to audiogravity.app</a>
            </footer>
        </main>
    </div>
</body>

</html>
"""


def build() -> dict[Path, str]:
    """Render every chapter.

    Returns:
        Mapping of output path to file contents.
    """
    readme = (MANUAL_DIR / "README.md").read_text(encoding="utf-8")
    toc = parse_toc(readme)
    if not toc:
        sys.exit("no chapters found in docs/manual/README.md — has the Contents list moved?")

    md = MarkdownIt("commonmark", {"html": True}).enable("table")
    known = {cid for cid, _ in toc} | {"README"}

    def render(source: str) -> str:
        """Run one Markdown source through every post-processing pass, in order."""
        return lazy_load_images(
            wrap_tables(
                link_between_pages(stamp_heading_ids(md.render(source)), known)))

    out: dict[Path, str] = {}
    for cid, label in toc:
        src = MANUAL_DIR / f"{cid}.md"
        if not src.exists():
            sys.exit(f"{src} is listed in the Contents but does not exist")
        # Canonical without the suffix: that is the address Pages actually serves.
        out[MANUAL_DIR / f"{cid}.html"] = page(
            label, render(src.read_text(encoding="utf-8")), toc, cid, cid)

    # The README becomes the manual's front page, on the same shell as the chapters. Its
    # canonical address is the directory: that is what a visitor reaches, and what the landing
    # and the chapters link to.
    out[MANUAL_DIR / "index.html"] = page(
        "Contents", stamp_version(render(readme), read_version()), toc, "", "")
    return out


def main() -> int:
    """Entry point.

    Returns:
        Process exit status: 0 on success, 1 if ``--check`` found a stale page.
    """
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="fail if a committed page differs from what the Markdown produces")
    args = ap.parse_args()

    pages = build()
    if args.check:
        stale = [p for p, content in pages.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != content]
        if stale:
            for p in stale:
                print(f"stale: {p.relative_to(MANUAL_DIR.parent.parent)}")
            print(f"\n{len(stale)} page(s) out of date — run scripts/gen_manual_html.py")
            return 1
        print(f"{len(pages)} manual page(s) up to date")
        return 0

    for p, content in pages.items():
        p.write_text(content, encoding="utf-8")
    print(f"wrote {len(pages)} manual page(s) to {MANUAL_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
