"""Guards for the hero's carousel: a capture per theme for every slide, and the words with it.

Every slide is a <picture>: its dark capture behind a prefers-color-scheme query, its light one in
the <img>, both files on the site, and main.js pointing the query at the theme chosen with the
button. A slide's caption and annotations carry its number, so a slide added, removed or moved
without them leaves words on the wrong screen or a screen without words — and nothing on the
page says so. Nor does anything say that a dot is missing, or that a capture is the wrong theme.

Run with ``python3 -m pytest scripts/`` from the repository root.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = (ROOT / "index.html").read_text(encoding="utf-8")
CAROUSEL = PAGE[PAGE.index('<div class="hero-carousel">'):PAGE.index('<div class="hero-controls">')]
SLIDES = re.findall(r'<picture class="hero-screenshot[^"]*">(.*?)</picture>', CAROUSEL, re.S)


def test_every_slide_has_a_light_and_a_dark_capture_of_one_screen():
    assert len(SLIDES) > 1
    for slide in SLIDES:
        dark = re.search(r'<source srcset="(assets/pics/[^"]+)-black\.webp" media="\(prefers-color-scheme: dark\)">',
                         slide)
        light = re.search(r'<img [^>]*src="(assets/pics/[^"]+)-light\.webp"', slide)
        assert dark and light, slide
        assert dark.group(1) == light.group(1), f"two screens in one slide: {dark.group(1)} / {light.group(1)}"
        for theme in ("black", "light"):
            assert (ROOT / f"{dark.group(1)}-{theme}.webp").is_file(), f"{dark.group(1)}-{theme}.webp"


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


def test_a_dot_for_every_slide():
    dots = re.search(r'<div class="hero-dots">(.*?)</div>', PAGE, re.S).group(1)
    assert dots.count('class="dot') == len(SLIDES)


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
    after = PAGE[PAGE.index('<div class="hero-carousel">'):PAGE.index('<div class="hero-dots">')]
    script = re.findall(r"<script>(.*?)</script>", after, re.S)
    assert len(script) == 1, "the theme script is no longer right after the slides"
    script = script[0]
    assert "querySelectorAll('.hero-screenshot source')" in script
    assert "attributeFilter: ['data-theme']" in script
    assert "'all'" in script and "'not all'" in script and "'(prefers-color-scheme: dark)'" in script
