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

#: How the trademark notice is found in README.md, the one Markdown file that carries it: its
#: italic passage that says the names are trademarks of their respective owners. The app reads
#: it the same way (audiogravity.ui, js/core/manual-notice.js) and shows it under each chapter;
#: the chapter pages here show it in their footer. check_notice() keeps it in the README and
#: out of the chapters.
NOTICE_ITALIC = re.compile(r"\*([^*]*trademarks\s+of\s+their\s+respective\s+owners[^*]*)\*")


def read_notice(readme: str) -> str | None:
    """The trademark notice, as README.md words it.

    Args:
        readme: Contents of ``docs/manual/README.md``.

    Returns:
        The notice with its lines joined and its inline HTML (``<sup>``) kept, or None when
        the README does not carry it as an italic passage.
    """
    m = NOTICE_ITALIC.search(readme)
    return " ".join(m.group(1).split()) if m else None


def footer_notice() -> str:
    """The notice the chapter pages carry in their footer, in the README's own words.

    Returns:
        The notice; empty when the README has none — which check_notice() refuses first.
    """
    return read_notice((MANUAL_DIR / "README.md").read_text(encoding="utf-8")) or ""


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
    """Give every h2, h3 and h4 an anchor id, de-duplicating repeats.

    markdown-it emits no ids, so without this the manual's own cross-references
    (``09-troubleshooting.md#roon``) land at the top of the page instead of the section.

    Args:
        rendered: HTML from markdown-it.

    Returns:
        The same HTML with ``id`` attributes on h2, h3 and h4.
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


#: Fence languages coloured as shell. The manual writes ``bash``; the other two are what an
#: author reaches for without thinking, and they colour the same way.
SHELL_LANGS = {"bash", "sh", "shell"}

#: A word that hands the command position on to the next one: in ``sudo tee``, both words are
#: commands, and colouring only ``sudo`` would leave what actually runs looking like an argument.
SHELL_PREFIXES = {"sudo"}

#: ``sudo`` options that take the next word as their value: in ``sudo -u audiogravity systemctl``
#: the command is ``systemctl``, and ``audiogravity`` is only the account it runs as.
SUDO_ARG_OPTIONS = {"-u", "-g", "-C", "-D", "-h", "-p", "-r", "-t", "-T", "-U"}

#: A leading assignment — ``LANG=C sort f`` — which leaves the command position to the next word.
SHELL_ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")

#: What ends a shell word. Quotes and ``$`` do not: ``"a"b`` and ``x-$(date)`` are one word each.
SHELL_BREAKS = frozenset(" \t\n|&;()<>")

#: A heredoc opener — ``<<EOF``, ``<<-EOF``, ``<<'EOF'``, ``<<"EOF"`` — with its terminator.
SHELL_HEREDOC = re.compile(r"<<(-?)[ \t]*(?:'([^'\n]*)'|\"([^\"\n]*)\"|([^\s|&;()<>]+))")

#: A redirection — ``>``, ``>>``, ``<``, ``>&2``, ``<&-``.
SHELL_REDIRECT = re.compile(r"[<>]+(?:&(?:[0-9]+|-))?")

#: A JSON number, anchored where the scan stands.
JSON_NUMBER = re.compile(r"-?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?")

#: Fence flag for a block the reader must adapt before running it: no copy button is offered,
#: since a one-click copy of an example address or password is an invitation to run it as is.
NOCOPY_FLAG = "nocopy"


def _esc(text: str) -> str:
    """Escape text for an element body the way the interface's ``escapeHtml`` does.

    That function escapes what a browser escapes when it serialises a text node — ``&``,
    ``<`` and ``>``, and a no-break space written ``&nbsp;`` — nothing else. Matching it
    exactly is what lets the two colourers produce the same bytes for the same block (see
    :func:`highlight_code`).
    """
    return html.escape(text, quote=False).replace("\u00a0", "&nbsp;")


def _span(kind: str, text: str) -> str:
    """Wrap ``text`` in a token span, or return nothing for an empty token."""
    return f'<span class="hl-{kind}">{_esc(text)}</span>' if text else ""


def _shell_expansion_end(code: str, i: int) -> int:
    """Index just past the ``$`` expansion starting at ``i``, or ``i + 1`` for a lone ``$``.

    ``$(…)`` is matched with its nesting counted, ``${…}`` up to its brace, ``$NAME`` over
    its identifier, and ``$?``-style specials over one character.
    """
    n = len(code)
    nxt = code[i + 1] if i + 1 < n else ""
    if nxt == "(":
        depth, j = 0, i + 1
        while j < n:
            if code[j] == "(":
                depth += 1
            elif code[j] == ")":
                depth -= 1
                if depth == 0:
                    return j + 1
            j += 1
        return n
    if nxt == "{":
        close = code.find("}", i + 2)
        return n if close == -1 else close + 1
    if nxt == "_" or nxt.isascii() and nxt.isalpha():
        j = i + 1
        while j < n and (code[j] == "_" or code[j].isascii() and code[j].isalnum()):
            j += 1
        return j
    if nxt and nxt in "0123456789#?@*$!-":
        return i + 2
    return i + 1


def _shell_quote_end(code: str, i: int) -> int:
    """Index just past the quoted string opening at ``i`` (to the end if it never closes)."""
    quote, j, n = code[i], i + 1, len(code)
    while j < n:
        if quote == '"' and code[j] == "\\":
            j += 2
            continue
        if code[j] == quote:
            return j + 1
        j += 1
    return n


def highlight_shell(code: str) -> str:
    """Colour a shell block: commands, options, strings, expansions, comments.

    A line-oriented reading, not a parser — enough for commands a reader copies, and the
    same rules as ``highlightShell`` in the interface (``js/core/code-highlight.js``), which
    must stay in step: the manual is shown in both places.

    * The first word of a command — at the start of a line, after ``|``, ``&``, ``;`` or
      ``(`` — is a command, and so is the word after ``sudo``. A line ending in ``\\``
      continues the command, so the next line starts with an argument.
    * A word starting with ``-`` is an option; it does not use up the command position. The
      value of a ``sudo`` option (``-u audiogravity``) does not either, nor does a leading
      assignment (``LANG=C``), which is an expansion.
    * ``'…'`` and ``"…"`` are strings, ``$…`` an expansion, ``#`` at a word start a comment.
    * The body of a heredoc (``<<'EOF'`` … ``EOF``) is a string.

    Args:
        code: The block's text.

    Returns:
        HTML with token spans; every character of ``code`` is kept, escaped.
    """
    out: list[str] = []
    n, i = len(code), 0
    at_cmd = True
    after_sudo = False  # the command position was handed on by sudo, whose options take values
    skip_arg = False    # the next word is the value of such an option
    heredocs: list[tuple[str, bool]] = []  # (terminator, tabs stripped) awaiting a newline

    while i < n:
        c = code[i]
        if c == "\\" and code.startswith("\n", i + 1):
            out.append("\\\n")  # continuation: the command goes on, the position is kept
            i += 2
        elif c == "\n":
            out.append("\n")
            i += 1
            at_cmd, after_sudo, skip_arg = True, False, False
            for term, strip_tabs in heredocs:
                while i < n:
                    end = code.find("\n", i)
                    line = code[i:] if end == -1 else code[i:end]
                    i = n if end == -1 else end + 1
                    tail = "" if end == -1 else "\n"
                    if (line.lstrip("\t") if strip_tabs else line) == term:
                        out.append(_esc(line) + tail)
                        break
                    out.append(_span("string", line) + tail)
            heredocs = []
        elif c in " \t":
            out.append(c)
            i += 1
        elif c == "#":
            end = code.find("\n", i)
            end = n if end == -1 else end
            out.append(_span("comment", code[i:end]))
            i = end
        elif code.startswith("<<", i) and not code.startswith("<<<", i):
            m = SHELL_HEREDOC.match(code, i)
            if m:
                term = next(g for g in (m.group(2), m.group(3), m.group(4)) if g is not None)
                heredocs.append((term, m.group(1) == "-"))
                out.append(_esc(m.group(0)))
                i = m.end()
            else:
                out.append(_esc("<<"))
                i += 2
            at_cmd = False
        elif c in "<>":
            m = SHELL_REDIRECT.match(code, i)
            out.append(_esc(m.group(0)))
            i = m.end()
            at_cmd = False  # what follows a redirection is a file, not a command
        elif c in "|&;()":
            out.append(_esc(c))
            i += 1
            at_cmd, after_sudo, skip_arg = c != ")", False, False
        else:
            start = i
            if skip_arg:
                kind = None
            elif c == "-":
                kind = "opt"
            elif at_cmd and SHELL_ASSIGNMENT.match(code, i):
                kind = "var"
            else:
                kind = "cmd" if at_cmd else None
            literal: list[str] = []

            def flush() -> None:
                if literal:
                    text = "".join(literal)
                    out.append(_span(kind, text) if kind else _esc(text))
                    literal.clear()

            while i < n and code[i] not in SHELL_BREAKS:
                ch = code[i]
                if ch == "\\":
                    if code.startswith("\n", i + 1):
                        break  # a continuation ends the word; the outer loop emits it
                    literal.append(code[i:i + 2])
                    i += 2
                elif ch in "'\"":
                    flush()
                    end = _shell_quote_end(code, i)
                    out.append(_span("string", code[i:end]))
                    i = end
                elif ch == "$":
                    end = _shell_expansion_end(code, i)
                    if end == i + 1:
                        literal.append(ch)
                    else:
                        flush()
                        out.append(_span("var", code[i:end]))
                    i = end
                else:
                    literal.append(ch)
                    i += 1
            flush()
            word = code[start:i]
            if skip_arg:
                skip_arg = False  # the option's value: the command position is still open
            elif kind == "opt":
                skip_arg = after_sudo and word in SUDO_ARG_OPTIONS
            elif kind == "cmd":
                at_cmd = after_sudo = word in SHELL_PREFIXES
            elif kind is None:  # an argument; an assignment ("var") leaves the position open
                at_cmd = after_sudo = False
    return "".join(out)


def highlight_json(code: str) -> str:
    """Colour a JSON block: keys, strings, numbers and the literals ``true``/``false``/``null``.

    Same rules as ``highlightJson`` in the interface (``js/core/code-highlight.js``).

    Args:
        code: The block's text.

    Returns:
        HTML with token spans; every character of ``code`` is kept, escaped.
    """
    out: list[str] = []
    n, i = len(code), 0
    while i < n:
        c = code[i]
        if c == '"':
            end = _shell_quote_end(code, i)  # JSON strings escape with a backslash too
            j = end
            while j < n and code[j] in " \t":
                j += 1
            out.append(_span("key" if code.startswith(":", j) else "string", code[i:end]))
            i = end
            continue
        m = JSON_NUMBER.match(code, i) if (c == "-" or "0" <= c <= "9") else None
        if m:
            out.append(_span("num", m.group(0)))
            i = m.end()
            continue
        word = next((w for w in ("true", "false", "null") if code.startswith(w, i)), None)
        if word:
            out.append(_span("null" if word == "null" else "lit", word))
            i += len(word)
            continue
        out.append(_esc(c))
        i += 1
    return "".join(out)


def highlight_code(code: str, lang: str) -> str | None:
    """Colour a code block in one of the languages the manual uses.

    Args:
        code: The block's text.
        lang: The fence's language, e.g. ``bash``.

    Returns:
        Highlighted HTML, or None for a language left plain.
    """
    if lang in SHELL_LANGS:
        return highlight_shell(code)
    if lang == "json":
        return highlight_json(code)
    return None


def highlight_fence(content: str, lang: str, attrs: str) -> str:
    """markdown-it's ``highlight`` hook: colour a fenced block and carry its flags.

    Returns the whole ``<pre>`` — markdown-it then uses it as is — so that a block flagged
    ``nocopy`` in its info string (```` ```bash nocopy ````) can say so on the element the
    copy script reads. A block with neither a known language nor a flag returns nothing, and
    markdown-it renders it exactly as it did before.

    Args:
        content: The block's text.
        lang: First word of the info string.
        attrs: The rest of the info string.

    Returns:
        The block's HTML, or an empty string to let markdown-it render it.
    """
    nocopy = NOCOPY_FLAG in attrs.split()
    body = highlight_code(content, lang)
    if body is None and not nocopy:
        return ""
    cls = f' class="language-{html.escape(lang)}"' if lang else ""
    flag = ' data-copy="no"' if nocopy else ""
    return f"<pre{flag}><code{cls}>{body if body is not None else _esc(content)}</code></pre>"


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
    # A chapter carries the trademark notice in its footer; the contents page does not,
    # since README.md — its body — already ends with it.
    notice = f'\n                <p class="man-notice">{footer_notice()}</p>' if active else ""
    return f"""<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    <title>{html.escape(plain)} — Audiogravity manual</title>
    <meta name="description" content="Audiogravity user manual — {html.escape(plain)}.">
    <link rel="canonical" href="https://audiogravity.app/docs/manual/{canonical}">
    <link rel="icon" href="../../assets/icons/favicon.ico" sizes="any">
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
    <script src="../../assets/manual-copy.js" defer></script>
    <script src="../../assets/to-top.js" defer></script>
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
                <a href="../../index.html">← Back to audiogravity.app</a>{notice}
            </footer>
        </main>
    </div>
</body>

</html>
"""


def markdown() -> MarkdownIt:
    """The Markdown renderer the manual's pages are built with.

    Returns:
        A CommonMark renderer that passes raw HTML through, knows tables, and colours the
        manual's shell and JSON blocks (:func:`highlight_fence`).
    """
    return MarkdownIt("commonmark", {"html": True, "highlight": highlight_fence}).enable("table")


def heading_ids(source: str) -> set[str]:
    """The anchor ids a chapter's headings get on the site.

    The landing links into the manual by these ids. Computing them with the pages' own
    renderer and numbering of repeats keeps its guard from drifting from the pages.

    Args:
        source: A chapter's Markdown.

    Returns:
        Every id stamped on its h2, h3 and h4 headings.
    """
    return set(re.findall(r'<h[234] id="([^"]+)"', stamp_heading_ids(markdown().render(source))))


def build() -> dict[Path, str]:
    """Render every chapter.

    Returns:
        Mapping of output path to file contents.
    """
    readme = (MANUAL_DIR / "README.md").read_text(encoding="utf-8")
    toc = parse_toc(readme)
    if not toc:
        sys.exit("no chapters found in docs/manual/README.md — has the Contents list moved?")

    md = markdown()
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


#: Where the trademark notice may appear in the Markdown: README.md only. It used to close all
#: thirteen files, because the Markdown is read in three places — these pages, GitHub, and
#: the app — and a notice in this template alone would have reached the website alone. Each
#: place now shows it once instead: the chapter pages in their footer (footer_notice()), the
#: app's Manual window in its own footer, GitHub in README.md. Repeated at the end of every
#: chapter it read as part of the text. This check keeps it out of the chapters, so it
#: cannot creep back, and in README.md, where GitHub readers find it.
NOTICE_MARK = "trademarks of their respective owners"


def _mentions_notice(path: Path) -> bool:
    """Whether a Markdown file carries the trademark notice, wherever its lines break.

    Args:
        path: A Markdown file of the manual.

    Returns:
        True when the notice's wording is in it.
    """
    return NOTICE_MARK in " ".join(path.read_text(encoding="utf-8").split())


def check_notice() -> list[str]:
    """Where the trademark notice is out of place.

    The README must carry it as the app reads it — an italic passage (read_notice); a chapter
    must not carry it in any form, its words alone being enough to refuse it.

    Returns:
        One line per problem: README.md without it, or a chapter repeating it. Empty when
        the notice is where it belongs.
    """
    problems = []
    if read_notice((MANUAL_DIR / "README.md").read_text(encoding="utf-8")) is None:
        problems.append("README.md lacks the trademark notice")
    problems += [f"{f.name} repeats the trademark notice"
                 for f in sorted(MANUAL_DIR.glob("[0-9][0-9]-*.md")) if _mentions_notice(f)]
    return problems


def main() -> int:
    """Entry point.

    Returns:
        Process exit status: 0 on success, 1 if ``--check`` found a stale page.
    """
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="fail if a committed page differs from what the Markdown produces")
    args = ap.parse_args()

    misplaced = check_notice()
    if misplaced:
        print("trademark notice: " + "; ".join(misplaced))
        print("It belongs in README.md only — each chapter page shows it in its footer.")
        return 1

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
