"""Guards for the landing's two grids: the hero's, and the passkey panel's beside it.

The passkey panel's grid was drawn in white at 4% on its black ground: a lightness gap (ΔL*)
of 2.7 between line and ground, where the hero's grid shows 9.1 — the user saw no grid there
(2026-10-27). Each theme's lines must now stand as far from their ground as the hero's do in
the same theme. Computed from the stylesheet's own values, blended as a browser composites
them; the figures match what Chromium draws (9.3 and 5.9 against the hero's 9.1 and 5.7).

The Landing workflow runs this file; run it locally with ``python3 -m pytest scripts/``.
"""

import re
from pathlib import Path

import pytest

CSS = (Path(__file__).resolve().parent.parent / "assets" / "style.css").read_text(encoding="utf-8")

#: How far a panel's grid may stand from the hero's, in ΔL*: a step either way, no more.
TOLERANCE = 1.5


def _rule(selector: str, holding: str = "") -> str:
    """The declarations of the first rule written with exactly this selector at a line's
    start that holds the given text — `:root` is written several times, its colours once."""
    for found in re.finditer(rf"^{re.escape(selector)}\s*\{{([^}}]*)\}}", CSS, re.M):
        if holding in found.group(1):
            return found.group(1)
    raise AssertionError(f"no rule {selector!r} holding {holding!r} in style.css")


def _value(body: str, prop: str) -> str:
    """The value a rule's body gives a property."""
    found = re.search(rf"(?:^|[;{{\s]){re.escape(prop)}:\s*([^;}}]+)", body)
    assert found, f"no {prop} in {body.strip()[:80]!r}"
    return found.group(1).strip()


def _hex(value: str) -> tuple[float, float, float]:
    """An #rgb or #rrggbb colour as three 0-255 channels."""
    digits = value.lstrip("#")
    if len(digits) == 3:
        digits = "".join(d * 2 for d in digits)
    return tuple(int(digits[i:i + 2], 16) for i in (0, 2, 4))


def _white_alpha(value: str) -> float:
    """The alpha of an rgba() white."""
    channels = [c.strip() for c in value.removeprefix("rgba(").removesuffix(")").split(",")]
    assert channels[:3] == ["255"] * 3, f"the panel's grid is a white: {value}"
    return float(channels[3])


def _blend(top, ground, alpha: float):
    """A colour laid over another at the given opacity, as a browser composites it."""
    return tuple(t * alpha + g * (1 - alpha) for t, g in zip(top, ground))


def _lightness(rgb) -> float:
    """CIELAB L* of an sRGB colour."""
    def linear(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    y = 0.2126 * linear(rgb[0]) + 0.7152 * linear(rgb[1]) + 0.0722 * linear(rgb[2])
    return 116 * y ** (1 / 3) - 16 if y > 0.008856 else 903.3 * y


def _gap(line, ground) -> float:
    """How far a grid's lines stand from their ground, in ΔL*."""
    return abs(_lightness(line) - _lightness(ground))


def _hero_gap(theme: str) -> float:
    tokens = _rule(":root" if theme == "light" else ':root[data-theme="dark"]', holding="--bg2")
    ground = _hex(_value(tokens, "--bg2"))
    opacity = float(_value(_rule(".hero-right::before"), "opacity"))
    return _gap(_blend(_hex(_value(tokens, "--border")), ground, opacity), ground)


def _pwa_gap(theme: str) -> float:
    if theme == "light":
        ground = _hex(_value(_rule(":root", holding="--inv"), "--inv"))
        alpha = _white_alpha(_value(_rule(".pwa-visual", holding="--pwa-grid"), "--pwa-grid"))
    else:
        ground = _hex(re.search(r'^\[data-theme="dark"\] \.pwa-visual,[^{]*\{\s*background:\s*(#[0-9a-fA-F]{3,6})', CSS, re.M).group(1))
        alpha = _white_alpha(_value(_rule('[data-theme="dark"] .pwa-visual'), "--pwa-grid"))
    return _gap(_blend((255, 255, 255), ground, alpha), ground)


def test_the_panel_draws_its_grid_with_its_own_line_colour():
    grid = _value(_rule(".pwa-visual::before"), "background-image")
    assert grid.count("var(--pwa-grid)") == 2, grid


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_the_panels_grid_shows_as_the_heros_does(theme):
    hero, pwa = _hero_gap(theme), _pwa_gap(theme)
    assert abs(pwa - hero) <= TOLERANCE, f"{theme}: the panel's grid stands {pwa:.1f} from its ground, the hero's {hero:.1f}"


def test_the_system_dark_theme_gives_the_panel_the_chosen_dark_themes_lines():
    # The dark theme is written twice: for a system set to dark, and for the button's choice.
    chosen = _value(_rule('[data-theme="dark"] .pwa-visual'), "--pwa-grid")
    system = re.search(r':root:not\(\[data-theme="light"\]\) \.pwa-visual \{\s*--pwa-grid:\s*([^;}]+)', CSS)
    assert system, "no --pwa-grid for a system set to dark"
    assert system.group(1).strip() == chosen
