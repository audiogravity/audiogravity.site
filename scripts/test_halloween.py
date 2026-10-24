"""Guards for the landing's Halloween: the day it comes, the theme it opens in, what it costs.

The decoration is fetched on 31 October only, by the visitor's own clock, or with ?halloween in
the address to preview it (index.html: the theme script in <head>, the loader at the end of
<body>; assets/halloween.css and assets/halloween.js). The rule that decides is a few lines of
JavaScript in the page, run here under Node when Node is installed — as it is on the Landing
workflow's runner — so that the date is checked as the browser reads it rather than as the
source reads to a person. The rest is held by what the files say: a page that never fetches
the decoration on another day, a flight for every bat, nothing over the text, nothing that
moves for a visitor who asked for less motion.

Run with ``python3 -m pytest scripts/`` from the repository root.
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PAGE = (ROOT / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "assets" / "halloween.css").read_text(encoding="utf-8")
JS = (ROOT / "assets" / "halloween.js").read_text(encoding="utf-8")
SITE_CSS = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")


def _head_script() -> str:
    """The theme script of the landing's <head>, the one that decides on Halloween."""
    head = PAGE[:PAGE.index("</head>")]
    scripts = re.findall(r"<script>(.*?)</script>", head, re.S)
    found = [s for s in scripts if "ag-theme" in s]
    assert len(found) == 1, "the theme script of <head> is gone or doubled"
    return found[0]


def _run_head(now: str, search: str = "", saved: str | None = None) -> dict:
    """Run the head script under Node, on a given day, address and saved theme.

    Args:
        now: The visitor's local date and time, ISO 8601 without a zone.
        search: The address's query string, "?…" or empty.
        saved: The theme the visitor chose with the button, if any.

    Returns:
        The classes and the data-theme the script left on the root element.
    """
    harness = """
        const RealDate = Date;
        const fixed = new RealDate(%(now)s).getTime();
        globalThis.Date = class extends RealDate {
            constructor(...a) { a.length ? super(...a) : super(fixed); }
            static now() { return fixed; }
        };
        const classes = new Set();
        const attrs = {};
        globalThis.localStorage = { getItem: (k) => (k === 'ag-theme' ? %(saved)s : null) };
        globalThis.location = { search: %(search)s };
        globalThis.document = { documentElement: {
            classList: { add: (c) => classes.add(c) },
            setAttribute: (k, v) => { attrs[k] = v; },
        } };
        %(script)s
        console.log(JSON.stringify({ classes: [...classes], theme: attrs['data-theme'] || null }));
    """ % {"now": json.dumps(now), "saved": json.dumps(saved), "search": json.dumps(search),
           "script": _head_script()}
    out = subprocess.run(["node", "-e", harness], capture_output=True, text=True, timeout=20, check=True)
    return json.loads(out.stdout)


needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="Node is not installed")


@needs_node
class TestTheDay:
    """31 October, every year, from midnight to midnight by the visitor's clock."""

    @pytest.mark.parametrize("now", ["2026-10-31T00:00:00", "2026-10-31T23:59:59", "2031-10-31T12:00:00"])
    def test_comes_on_31_october_every_year(self, now):
        assert _run_head(now) == {"classes": ["halloween"], "theme": "dark"}

    @pytest.mark.parametrize("now", ["2026-10-30T23:59:59", "2026-11-01T00:00:00", "2026-10-24T15:00:00",
                                     "2027-12-31T12:00:00"])
    def test_stays_away_on_any_other_day(self, now):
        assert _run_head(now) == {"classes": [], "theme": None}

    @pytest.mark.parametrize("search", ["?halloween", "?halloween=1", "?lang=en&halloween"])
    def test_shows_itself_on_any_day_for_a_preview(self, search):
        assert _run_head("2026-10-24T15:00:00", search)["classes"] == ["halloween"]

    @pytest.mark.parametrize("search", ["?halloweenx", "?x=halloween", "?nohalloween"])
    def test_a_lookalike_address_is_no_preview(self, search):
        assert _run_head("2026-10-24T15:00:00", search)["classes"] == []

    def test_a_theme_the_visitor_chose_is_kept(self):
        """Dark by default that day: one who chose light with the button keeps light."""
        assert _run_head("2026-10-31T20:00:00", saved="light") == {"classes": ["halloween"], "theme": "light"}

    def test_another_day_follows_the_saved_theme_as_before(self):
        assert _run_head("2026-11-01T09:00:00", saved="light") == {"classes": [], "theme": "light"}


class TestTheLoader:
    """The decoration costs nothing on the other 364 days: no request, no byte."""

    def test_the_page_names_the_decoration_in_a_template_only(self):
        template = re.search(r'<template id="hw-assets">(.*?)</template>', PAGE, re.S)
        assert template, "the decoration's template is gone"
        assert re.search(r'href="assets/halloween\.css\?v=[0-9a-f]{10}"', template.group(1))
        assert re.search(r'src="assets/halloween\.js\?v=[0-9a-f]{10}"', template.group(1))
        outside = PAGE.replace(template.group(0), "")
        assert "halloween.css" not in outside and "halloween.js" not in outside, \
            "the decoration is fetched outside its template, so on every day"

    def test_the_loader_acts_on_halloween_alone_and_styles_first(self):
        loader = PAGE[PAGE.index('<template id="hw-assets">'):PAGE.index("</body>")]
        assert "classList.contains('halloween')" in loader
        # The script only once the sheet is in: nothing drawn unstyled.
        assert loader.index("sheet.onload") < loader.index("script.src")


class TestTheDecoration:
    """What the sheet and the script promise the page."""

    def test_it_never_takes_a_click(self):
        assert re.search(r"\.hw-decor\s*\{\s*pointer-events:\s*none", CSS)

    def test_it_is_hidden_from_assistive_technology(self):
        assert 'aria-hidden="true">\' + inner' in JS, "lay() no longer hides what it lays"
        assert JS.count("insertAdjacentHTML") == 2, "something is laid outside lay() and DEFS"

    def test_every_bat_has_a_flight_and_every_flight_a_bat(self):
        built = {int(n) for n in re.findall(r"\bbat\((\d)", JS)}
        flights = {int(n) for n in re.findall(r"@keyframes hw-fly-b(\d)", CSS)}
        named = {int(n) for n in re.findall(r"animation-name:\s*hw-fly-b(\d)", CSS)}
        assert built == flights == named == set(range(1, 8))

    def test_it_animates_only_what_the_browser_composites(self):
        """transform and opacity: anything else would have the page painted at every frame."""
        for name, body in re.findall(r"@keyframes ([\w-]+)\s*\{(.*?\})\s*\}", CSS, re.S):
            props = set(re.findall(r"([a-z-]+)\s*:", body))
            assert props <= {"transform", "opacity"}, f"{name} animates {props - {'transform', 'opacity'}}"

    def test_it_gives_way_to_the_captions_at_their_own_width(self):
        """The carousel shows its captions from 1551px; the low bats and the left pumpkins then
        keep out of their way. The two thresholds have to move together."""
        hidden_below = re.search(r"@media\s*\(\s*max-width:\s*(\d+)px\s*\)\s*\{\s*\.hero-caption,\s*\.hero-note",
                                 SITE_CSS)
        assert hidden_below, "style.css no longer hides the captions below a width"
        shown_from = int(hidden_below.group(1)) + 1
        gives_way = re.findall(r"@media\s*\(min-width:\s*(\d+)px\)", CSS)
        assert gives_way and set(gives_way) == {str(shown_from)}

    def test_less_motion_means_no_bats_and_no_flicker(self):
        block = re.search(r"@media \(prefers-reduced-motion: reduce\)\s*\{(.*?)\n\}", CSS, re.S).group(1)
        assert re.search(r"\.hw-sky\s*\{\s*display:\s*none", block)
        assert re.search(r"\.hw-halo,\s*\.hw-fog\s*\{\s*animation:\s*none", block)

    def test_it_rests_while_out_of_sight(self):
        assert "IntersectionObserver" in JS and "hw-paused" in JS
        assert re.search(r"\.hw-paused \.hw-decor \*\s*\{\s*animation-play-state:\s*paused", CSS)

    def test_a_browser_without_container_units_gets_no_bats(self):
        """Rather than seven bats piled at the corner where an unread flight leaves them."""
        assert re.search(r"@supports not \(width: 1cqw\)\s*\{\s*\.hw-sky\s*\{\s*display:\s*none", CSS)
