"""Guards for the hero's carousel: a capture per theme for every slide, the words with it, and
its controls.

Every slide is a <picture>: its dark capture behind a prefers-color-scheme query, its light one in
the <img>, both files on the site, and main.js pointing the query at the theme chosen with the
button. A slide's caption and annotations carry its number, so a slide added, removed or moved
without them leaves words on the wrong screen or a screen without words — and nothing on the
page says so. Nor does anything say that a dot is missing, or that a capture is the wrong theme.

The controls are a pill of dots, a button each, and a play button. The current dot fills over
the time its screen stays, and that fill — an animation of style.css — is what moves the
carousel on: main.js keeps no timer that could drift from the bar.

Run with ``python3 -m pytest scripts/`` from the repository root.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = (ROOT / "index.html").read_text(encoding="utf-8")
CAROUSEL = PAGE[PAGE.index('<div class="hero-carousel">'):PAGE.index('<div class="hero-controls">')]
CONTROLS = PAGE[PAGE.index('<div class="hero-controls">'):PAGE.index("</section>", PAGE.index('<div class="hero-controls">'))]
SLIDES = re.findall(r'<picture class="hero-screenshot[^"]*">(.*?)</picture>', CAROUSEL, re.S)
SITE_CSS = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")
MAIN_JS = (ROOT / "assets" / "main.js").read_text(encoding="utf-8")
CAROUSEL_JS = MAIN_JS[:MAIN_JS.index("// Sparklines")]


def _one_screen_in_both_themes(picture: str) -> None:
    """A <picture> of the app: its dark capture marked for the theme script, its light one in
    the <img>, of the same screen, both on the site."""
    dark = re.search(r'<source srcset="(assets/pics/[^"]+)-black\.webp" media="\(prefers-color-scheme: dark\)"'
                     r' data-dark>', picture)
    light = re.search(r'<img [^>]*src="(assets/pics/[^"]+)-light\.webp"', picture)
    assert dark and light, picture
    assert dark.group(1) == light.group(1), f"two screens in one picture: {dark.group(1)} / {light.group(1)}"
    for theme in ("black", "light"):
        assert (ROOT / f"{dark.group(1)}-{theme}.webp").is_file(), f"{dark.group(1)}-{theme}.webp"


def test_every_slide_has_a_light_and_a_dark_capture_of_one_screen():
    assert len(SLIDES) > 1
    for slide in SLIDES:
        _one_screen_in_both_themes(slide)


def test_every_capture_of_the_app_on_the_page_follows_the_theme():
    """The carousel's and the others — the passkey login further down: a dark capture the theme
    script cannot find would show the system's theme against the visitor's choice."""
    pictures = re.findall(r"<picture[^>]*>(.*?)</picture>", PAGE, re.S)
    assert len(pictures) > len(SLIDES)
    for picture in pictures:
        _one_screen_in_both_themes(picture)
    assert PAGE.count('media="(prefers-color-scheme: dark)"') == len(re.findall(r"<source [^>]* data-dark>", PAGE))


def test_every_capture_says_what_it_shows_and_holds_its_place():
    for slide in SLIDES:
        assert re.search(r'alt="[^"]{3,}"', slide), slide
        assert 'width="760" height="1497"' in slide, slide


def test_the_first_slide_alone_loads_at_once():
    first, *rest = SLIDES
    assert 'loading="lazy"' not in first
    assert all('loading="lazy"' in slide for slide in rest)


def test_the_first_slide_shows_first_with_its_words():
    assert CAROUSEL.count('<picture class="hero-screenshot active">') == 1
    assert CAROUSEL.index('<picture class="hero-screenshot active">') == CAROUSEL.index('<picture class="hero-screenshot')
    shown = re.findall(r'class="hero-(?:caption|note) active" data-slide="(\d+)"', CAROUSEL)
    assert shown and set(shown) == {"0"}


def test_a_dot_for_every_slide_each_a_button_naming_its_screen():
    dots = re.findall(r'<button class="dot( active)?" type="button" aria-label="Screen (\d+)"( aria-current="true")?>'
                      r'<span><i></i></span></button>', CONTROLS)
    assert [int(n) for _, n, _ in dots] == list(range(1, len(SLIDES) + 1))
    # The first is the screen shown first, and says so.
    first_only = [True] + [False] * (len(SLIDES) - 1)
    assert [bool(a) for a, _, _ in dots] == first_only
    assert [bool(c) for _, _, c in dots] == first_only
    assert CONTROLS.count('class="dot') == len(SLIDES)


def test_the_controls_are_the_dots_and_the_play_button():
    assert CONTROLS.count("<button ") == len(SLIDES) + 1
    assert "heroPrev" not in PAGE + MAIN_JS and "heroNext" not in PAGE + MAIN_JS


def test_it_starts_paused_and_its_button_says_so():
    assert '<button class="hero-ctrl" id="heroPlay" type="button" aria-label="Play">' in CONTROLS
    assert CAROUSEL_JS.strip().endswith("setPlaying(false);\n})();")
    assert "playBtn.setAttribute('aria-label', on ? 'Pause' : 'Play')" in CAROUSEL_JS


def test_the_next_screen_comes_when_the_fill_ends():
    """No timer of main.js's own to drift from the bar: the stylesheet's fill sets the time."""
    assert "setInterval" not in CAROUSEL_JS and "setTimeout" not in CAROUSEL_JS
    assert "controls.addEventListener('animationend'" in CAROUSEL_JS
    assert "e.animationName === 'hero-progress'" in CAROUSEL_JS
    fill = re.search(r"\.hero-dots \.dot\.active i \{\s*animation: hero-progress ([\d.]+)s linear forwards paused;",
                     SITE_CSS)
    assert fill and float(fill.group(1)) > 0
    assert re.search(r"\.hero-controls\.playing \.dot\.active i \{\s*animation-play-state: running;", SITE_CSS)
    # Moved by the compositor alone, every frame of the 3.5s.
    keyframes = re.search(r"@keyframes hero-progress \{(.*?)\}\s*\}", SITE_CSS, re.S).group(1)
    assert set(re.findall(r"([a-z-]+)\s*:", keyframes)) == {"transform"}


def test_nothing_of_the_panel_is_drawn_over_the_controls():
    """A box placed absolutely is painted after the boxes that are not: the panel's grid drew its
    lines across the dots and the buttons, and the captures' shadow darkened the pill, until the
    grid went to the bottom of the panel and the controls were raised."""
    panel = re.search(r"^\.hero-right \{(.*?)\}", SITE_CSS, re.S | re.M).group(1)
    grid = re.search(r"^\.hero-right::before \{(.*?)\}", SITE_CSS, re.S | re.M).group(1)
    controls = re.search(r"^\.hero-controls \{(.*?)\}", SITE_CSS, re.S | re.M).group(1)
    assert re.search(r"isolation:\s*isolate", panel)
    assert re.search(r"z-index:\s*-1", grid)
    assert re.search(r"position:\s*relative", controls)
    assert int(re.search(r"z-index:\s*(\d+)", controls).group(1)) >= 1


def test_every_slide_has_its_caption_and_every_note_its_slide():
    captions = [int(n) for n in re.findall(r'class="hero-caption[^"]*" data-slide="(\d+)"', CAROUSEL)]
    assert sorted(captions) == list(range(len(SLIDES)))
    notes = re.findall(r'class="hero-note[^"]*" data-slide="(\d+)" style="--y:([\d.]+)%"', CAROUSEL)
    assert len(notes) == CAROUSEL.count('class="hero-note'), "a note without its slide or its height"
    for slide, y in notes:
        assert int(slide) < len(SLIDES) and 0 < float(y) < 100, (slide, y)


def test_the_captures_follow_a_theme_chosen_with_the_button():
    """Right after the slides: from main.js, at the end of the page, a visitor who chose the
    other theme downloaded every capture twice."""
    after = PAGE[PAGE.index('<div class="hero-carousel">'):PAGE.index('<div class="hero-controls">')]
    script = re.findall(r"<script>(.*?)</script>", after, re.S)
    assert len(script) == 1, "the theme script is no longer right after the slides"
    script = script[0]
    assert "querySelectorAll('source[data-dark]')" in script
    # The captures further down the page do not exist yet when it first runs.
    assert "addEventListener('DOMContentLoaded', follow)" in script
    assert "attributeFilter: ['data-theme']" in script
    assert "'all'" in script and "'not all'" in script and "'(prefers-color-scheme: dark)'" in script
