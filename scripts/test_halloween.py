"""Guards for the landing's Halloween: the day it comes, the theme it opens in, what it costs.

The decoration is fetched on 31 October only, by the visitor's own clock, or with ?halloween in
the address to preview it (index.html: the theme script in <head>, the loader at the end of
<body>; assets/halloween.css and assets/halloween.js). The rule that decides is a few lines of
JavaScript in the page, run here under Node when Node is installed — as it is on the Landing
workflow's runner — so that the date is checked as the browser reads it rather than as the
source reads to a person. The rest is held by what the files say: a page that never fetches
the decoration on another day, a flight for every bat, nothing over the text, a mist its own
boxes do not cut, nothing that moves for a visitor who asked for less motion.

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

    def test_every_spider_has_its_drop_and_hangs_in_a_sky(self):
        """In the panel's sky, which clips its thread and hides it for less motion."""
        built = {int(n) for n in re.findall(r"\bspider\((\d)\)", JS)}
        drops = {int(n) for n in re.findall(r"@keyframes hw-drop-(\d)", CSS)}
        named = {int(n) for n in re.findall(r"animation-name:\s*hw-drop-(\d)", CSS)}
        assert built == drops == named == {1, 2}
        assert re.search(r"lay\(panel, 'hw-sky hw-sky-panel', spider\(1\)", JS)

    def test_the_webs_stay_still_and_stay_for_less_motion(self):
        """Laid outside the skies, which less motion hides: the hero's corner and the panel's."""
        assert re.findall(r"lay\((\w+), 'hw-web [\w-]+', WEB\)", JS) == ["hero", "panel"]
        assert not re.search(r"\.hw-web[\w-]*\s*\{[^}]*animation", CSS)

    def test_the_carousel_controls_stay_above_it(self):
        """The mist, the halos and the low bats pass behind the dots and the button."""
        controls = re.search(r"\.halloween \.hero-controls \{([^}]*)\}", CSS).group(1)
        assert re.search(r"position:\s*relative", controls)
        above = int(re.search(r"z-index:\s*(\d+)", controls).group(1))
        others = [int(z) for z in re.findall(r"z-index:\s*(\d+)", CSS.replace(controls, ""))]
        assert others and above > max(others)

    def test_it_animates_only_what_the_browser_composites(self):
        """transform and opacity: anything else would have the page painted at every frame. A
        keyframe may carry its own timing, which is not a property it animates."""
        for name, body in re.findall(r"@keyframes ([\w-]+)\s*\{(.*?\})\s*\}", CSS, re.S):
            props = set(re.findall(r"([a-z-]+)\s*:", body)) - {"animation-timing-function"}
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
        # The spider on the phone's left hangs where the annotations are.
        low = re.search(r"@media \(min-width: \d+px\) \{\s*\.hw-b3,(.*?)\{", CSS, re.S)
        assert low and ".hw-s1" in low.group(1)

    def test_no_mist_is_left_alone_where_the_pumpkins_give_way(self):
        """Without the pumpkins on the phone's left, the mist there was a grey band running to
        the panel's edge: from the same width, it starts at the phone, in both spellings of the
        mask (Safari before 15.4 reads the prefixed one only)."""
        block = re.search(r"@media \(min-width: \d+px\) \{\s*\.hw-pk-a,\s*\.hw-pk-f1 \{\s*display: none\s*\}(.*?)\n\}",
                          CSS, re.S)
        assert block, "the left pumpkins no longer give way to the captions"
        fog = re.search(r"\.hw-fog \{(.*?)\}", block.group(1), re.S)
        assert fog, "the mist stays on the left where the pumpkins are gone"
        for prop in ("-webkit-mask-image", "mask-image"):
            assert re.search(r"(^|[^-])%s: linear-gradient\(to right, transparent \d+%%, #000 \d+%%\)" % prop,
                             fog.group(1), re.M), prop

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


def _mist_banks() -> dict:
    """Each bank of mist in halloween.js: its viewBox, and the ellipses drawn in it.

    Returns:
        ``{"back" | "front": ([x, y, width, height], [{"cx", "cy", "rx", "ry"}, ...])}``.
    """
    banks = {}
    for name, body in re.findall(r"var MIST_(BACK|FRONT) = (.*?);\n", JS, re.S):
        view = [float(v) for v in re.search(r'viewBox="([^"]+)"', body).group(1).split()]
        ellipses = [{k: float(v) for k, v in re.findall(r'\b(c[xy]|r[xy])="([\d.]+)"', e)}
                    for e in re.findall(r"<ellipse [^>]*>", body)]
        banks[name.lower()] = (view, ellipses)
    return banks


class TestTheMist:
    """The mist is a blur, and an svg cuts what it draws at its own edges: a box smaller than
    the blur cuts it straight, and the cut shows as an edge. It did, at both ends of the mist and
    along its foot, until each box held the whole of its blur."""

    def test_each_box_and_the_filter_hold_the_whole_blur(self):
        """Three deviations past the banks, where a gaussian blur has faded out."""
        flt = re.search(r'<filter id="hw-mist" x="(-?[\d.]+)%" y="(-?[\d.]+)%" width="([\d.]+)%" height="([\d.]+)%">'
                        r'<feGaussianBlur stdDeviation="([\d.]+)" />', JS)
        assert flt, "the mist's filter is gone or no longer a single blur"
        fx, fy, fw, fh, sigma = (float(v) for v in flt.groups())
        reach = 3 * sigma
        banks = _mist_banks()
        assert set(banks) == {"back", "front"}
        for name, (view, ellipses) in banks.items():
            x, y, w, h = view
            left = min(e["cx"] - e["rx"] for e in ellipses)
            right = max(e["cx"] + e["rx"] for e in ellipses)
            top = min(e["cy"] - e["ry"] for e in ellipses)
            bottom = max(e["cy"] + e["ry"] for e in ellipses)
            assert x <= left - reach and right + reach <= x + w, f"{name}: the box cuts the blur across"
            assert y <= top - reach and bottom + reach <= y + h, f"{name}: the box cuts the blur down"
            # The filter's region is a share of the box the banks are drawn in.
            bw, bh = right - left, bottom - top
            assert left + bw * fx / 100 <= left - reach and right + reach <= left + bw * (fx + fw) / 100, name
            assert top + bh * fy / 100 <= top - reach and bottom + reach <= top + bh * (fy + fh) / 100, name

    def test_each_box_is_placed_from_its_viewbox(self):
        """At the frame's scale, 760 units across 200% of the ground, its left edge at -50%: a
        viewBox grown without its box would move the mist, or stretch it."""
        for name, (view, _) in _mist_banks().items():
            x, y, w, h = view
            rule = re.search(r"^\.hw-fog-%s \{(.*?)\}" % name, CSS, re.S | re.M).group(1)
            assert re.search(r"left: calc\(-50%% - 200%% \* %g / 760\)" % -x, rule), name
            assert re.search(r"width: calc\(200%% \* %g / 760\)" % w, rule), name
            assert re.search(r"aspect-ratio: %g / %g" % (w, h), rule), name
            foot = re.search(r"bottom: calc\(-[\d.]+cqw - 200cqw \* \((\d+) - \d+\) / 760\)", rule)
            assert foot and float(foot.group(1)) == y + h, f"{name}: the foot is not the viewBox's"
