"""Guards for the landing's type scale and for the fonts every page of the site loads.

Both are easy to undo one line at a time, and nothing on screen says so: a size borrowed from
another repository's vocabulary that this site never declares (the comparison table and the
five-layer block drew every word at 16px for four months that way), a literal 9px label, a
<link> back to a font service. Each test below closes one of those doors, and says which one
when it fails, rather than stopping on a traceback.

The scale covers assets/style.css, the landing's sheet. The manual's own sheet, manual.css,
keeps sizes of its own and is not held to it.

The Landing workflow runs this file on the pushes that touch the landing; run it locally with
``python3 -m pytest scripts/`` from the repository root.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "style.css"
PAGES = [ROOT / "index.html", ROOT / "404.html", *sorted((ROOT / "docs" / "manual").glob("*.html"))]

#: The six text steps, documented where they are declared (the :root block of style.css).
TEXT_STEPS = {"xs": 11, "sm": 13, "md": 15, "lg": 17, "xl": 20, "xxl": 28}
#: The display steps: the hero's name, section titles, the pull quote, the big figures.
DISPLAY_STEPS = {"figure", "quote", "title", "hero"}
#: What is read character by character: commands, a configuration file, a file name.
MONO_SELECTORS = {".mono", ".ic", ".rt-config", ".terminal code"}


def _css() -> str:
    """The landing's stylesheet, as served."""
    return CSS.read_text(encoding="utf-8")


def _size_tokens(css: str) -> dict[str, str]:
    """Font-size tokens declared in a stylesheet.

    Args:
        css: Stylesheet text.

    Returns:
        Token name without its ``--font-size-`` prefix, mapped to its declared value.
    """
    return dict(re.findall(r"--font-size-([a-z]+):\s*([^;]+);", css))


def _faces(css: str) -> list[dict[str, str | None]]:
    """The ``@font-face`` rules of a stylesheet, in declaration order.

    A descriptor a face leaves out is recorded as CSS reads it: no ``font-style`` means
    ``normal``, and a face without ``url()`` gets ``None``, for the tests to name.

    Args:
        css: Stylesheet text.

    Returns:
        One dict per face, with its ``family``, ``style`` and ``url``.
    """
    faces = []
    for body in re.findall(r"@font-face\s*\{([^}]*)\}", css):
        family = re.search(r"font-family:\s*([^;]+);", body)
        style = re.search(r"font-style:\s*([^;]+);", body)
        url = re.search(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", body)
        faces.append({
            "family": family.group(1).strip("'\" ") if family else "",
            "style": style.group(1).strip() if style else "normal",
            "url": url.group(1) if url else None,
        })
    return faces


def test_every_size_token_in_use_is_declared():
    """An undeclared token falls back to the inherited size, and nothing reports it."""
    css = _css()
    used = set(re.findall(r"var\(--font-size-([a-z]+)", css))
    assert used - set(_size_tokens(css)) == set(), "tokens used but never declared"


def test_the_text_scale_is_the_six_documented_steps():
    """Six steps, none under 11px, and no seventh slipped in beside them."""
    text = {k: v.strip() for k, v in _size_tokens(_css()).items() if k not in DISPLAY_STEPS}
    not_px = {k: v for k, v in text.items() if not re.fullmatch(r"\d+px", v)}
    assert not_px == {}, "a text step must be a whole number of pixels"
    assert {k: int(v[:-2]) for k, v in text.items()} == TEXT_STEPS


def test_the_display_steps_are_the_documented_four():
    """The big sizes are named steps too, and only these four."""
    assert set(_size_tokens(_css())) - set(TEXT_STEPS) == DISPLAY_STEPS


def test_every_font_size_is_a_step_or_says_why_not():
    """A literal size carries its reason on its own line, or it is a step that was missed."""
    step = r"var\(--font-size-[a-z]+\)"
    offenders = []
    for n, line in enumerate(_css().splitlines(), 1):
        m = re.search(r"font-size:\s*([^;/]+)", line)
        if not m or "scale exception" in line:
            continue
        value = m.group(1).strip()
        if re.fullmatch(step, value) or re.fullmatch(rf"clamp\({step}, [\d.]+vw, {step}\)", value):
            continue
        offenders.append(f"{n}: {line.strip()}")
    assert offenders == []


def test_no_font_shorthand_sets_a_size_behind_the_scale():
    """``font: 600 9px/1 …`` would set a size the line-by-line check above never reads."""
    css = re.sub(r"/\*.*?\*/", "", _css(), flags=re.S)
    assert re.findall(r"(?<![-\w])font\s*:[^;}]*", css) == []


def test_monospace_is_kept_for_what_is_read_character_by_character():
    """Labels and badges are identified at a glance, and take the text face."""
    css = re.sub(r"/\*.*?\*/", "", _css(), flags=re.S)
    users = set()
    for head, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        if "var(--mono)" in body:
            users |= {s.strip() for s in head.split(",")}
    assert users <= MONO_SELECTORS


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.name)
def test_no_page_fetches_a_font_from_a_font_service(page):
    """Every font comes from this site: a font service sees each visitor's address."""
    html = page.read_text(encoding="utf-8")
    assert "fonts.googleapis.com" not in html
    assert "fonts.gstatic.com" not in html


def test_the_manual_template_fetches_no_font_from_a_font_service():
    """The generated pages are rewritten from this template on every push."""
    src = (ROOT / "scripts" / "gen_manual_html.py").read_text(encoding="utf-8")
    assert "fonts.googleapis.com" not in src
    assert "fonts.gstatic.com" not in src


def test_every_declared_face_has_its_file():
    """A face whose file is missing falls back to the system font, with no error shown."""
    faces = _faces(_css())
    assert faces, "no @font-face in the stylesheet"
    assert [f for f in faces if f["url"] is None] == [], "a face without url()"
    assert [f["url"] for f in faces if not (CSS.parent / f["url"]).is_file()] == []


def test_latin_is_declared_after_latin_ext_in_each_pair():
    """The face declared last wins the codepoints both subsets cover; latin must be it.

    Otherwise three combining marks send every page of plain ASCII to fetch latin-ext too.
    """
    order = {}
    for i, face in enumerate(_faces(_css())):
        url = face["url"] or ""
        subset = "latin-ext" if url.endswith("-latin-ext.woff2") else "latin" if url.endswith("-latin.woff2") else None
        if subset:
            order.setdefault((face["family"], face["style"]), {})[subset] = i
    assert order, "no latin / latin-ext face found"
    incomplete = [pair for pair, idx in order.items() if set(idx) != {"latin", "latin-ext"}]
    assert incomplete == [], "each family and style comes as a latin / latin-ext pair"
    assert [pair for pair, idx in order.items() if idx["latin-ext"] > idx["latin"]] == []


def test_the_licenses_travel_with_the_fonts():
    """SIL OFL 1.1 requires the license text to go wherever the font files go."""
    fonts = ROOT / "assets" / "fonts"
    assert (fonts / "OFL-Inter.txt").is_file()
    assert (fonts / "OFL-JetBrains-Mono.txt").is_file()


def test_every_preloaded_font_is_one_the_stylesheet_declares():
    """A preload nothing asks for is a download paid on every visit for nothing."""
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    preloads = re.findall(r'<link rel="preload" href="assets/([^"]+)" as="font"', html)
    assert preloads, "the first screen's faces are no longer preloaded"
    assert set(preloads) <= {f["url"] for f in _faces(_css())}
