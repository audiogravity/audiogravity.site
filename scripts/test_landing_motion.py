"""Guards for what moves on the landing on any day: the pipeline drawing's dots.

They are SMIL animations, which the browser runs on the page's main thread and never stops by
itself when the drawing is out of sight. Left running, they kept the whole page redrawing sixty
times a second wherever the reader was: mid-page, a CPU slowed four times was 49% busy with them
and 20% with them stopped (Chromium, 2026-10-25). assets/main.js now runs them only while the
drawing is on screen, and keeps them still for a visitor who asked for less motion, whom they
used to ignore. These tests hold that, and that no other SMIL animation joins them unwatched.

The Landing workflow runs this file; run it locally with ``python3 -m pytest scripts/``.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = (ROOT / "index.html").read_text(encoding="utf-8")
MAIN_JS = (ROOT / "assets" / "main.js").read_text(encoding="utf-8")
SMIL = re.compile(r"<(?:animate|animateMotion|animateTransform|set)\b")


def _drawing() -> str:
    """The pipeline drawing's markup, from its frame to the end of its svg."""
    start = PAGE.index('<div class="pipeline-frame">')
    return PAGE[start:PAGE.index("</svg>", start)]


def _dots_code() -> str:
    """The part of main.js that drives the pipeline's dots."""
    return MAIN_JS[MAIN_JS.index("// The pipeline's moving dots."):]


def test_the_drawing_is_the_only_smil_on_the_page():
    """A SMIL animation anywhere else would run as these did, unseen and unstopped."""
    drawing = _drawing()
    assert SMIL.search(drawing), "the dots are no longer SMIL: this guard holds nothing"
    assert not SMIL.search(PAGE.replace(drawing, "")), "a SMIL animation outside the drawing runs unwatched"


def test_the_dots_move_only_while_the_drawing_is_in_sight():
    code = _dots_code()
    assert "document.querySelector('.pipeline-frame svg')" in code
    assert re.search(r"new IntersectionObserver\(function \(entries\) \{\s*"
                     r"if \(entries\[0\]\.isIntersecting\) drawing\.unpauseAnimations\(\);\s*"
                     r"else drawing\.pauseAnimations\(\);\s*\}\)\.observe\(drawing\)", code)


def test_the_dots_stay_still_for_less_motion():
    """Stopped before any observer could start them, and left so."""
    code = _dots_code()
    reduced = code.index("matchMedia('(prefers-reduced-motion: reduce)').matches")
    assert re.search(r"\{\s*drawing\.pauseAnimations\(\);\s*return;\s*\}", code[reduced:])
    assert reduced < code.index("new IntersectionObserver")
