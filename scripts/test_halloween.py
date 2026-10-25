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
import unicodedata
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
        assert built == flights == named == set(range(1, 10))

    def test_every_spider_has_its_drop_and_hangs_in_a_sky(self):
        """In a sky, which clips its thread and hides it for less motion: the panel's, or down
        the page a section's band (on a phone) or margin."""
        built = {int(n) for n in re.findall(r"\bspider\((\d)", JS)}
        drops = {int(n) for n in re.findall(r"@keyframes hw-drop-(\d)", CSS)}
        named = {int(n) for n in re.findall(r"animation-name:\s*hw-drop-(\d)", CSS)}
        assert built == drops == named == {1, 2, 3, 4, 5}
        assert re.search(r"lay\(panel, 'hw-sky hw-sky-panel', spider\(1\)", JS)
        assert re.search(r"lay\(section, 'hw-sky hw-sky-top', spider\(4", JS)
        assert re.search(r"margins\[i % 2\] \+= spider\(3", JS)
        assert re.search(r"lay\(section, 'hw-sky hw-sky-margin hw-margin-l', margins\[0\]\)", JS)
        assert re.search(r"lay\(footer, 'hw-sky hw-sky-foot', spider\(5\)\)", JS)

    @pytest.mark.parametrize("n", [3, 4, 5])
    def test_a_spider_down_the_page_has_thread_enough_for_its_drop(self, n):
        """Its thread is as long as the sheet says, not a share of its sky: shorter than the
        drop, it would end in mid-air with the spider hanging from nothing."""
        drop = re.search(r"@keyframes hw-drop-%d \{(.*?)\n\}" % n, CSS, re.S).group(1)
        deepest = max(float(v) for v in re.findall(r"translateY\((-?[\d.]+)px\)", drop))
        thread = float(re.search(r"\.hw-s%d::before \{ height: ([\d.]+)px \}" % n, CSS).group(1))
        assert thread > deepest

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
        assert re.search(r"\.hw-halo,\s*\.hw-lit,\s*\.hw-fog\s*\{\s*animation:\s*none", block)

    def test_it_rests_while_out_of_sight(self):
        """Part by part — the hero, each section, the footer — rather than the whole page with
        the hero, now that the decoration runs down the page."""
        assert "IntersectionObserver" in JS
        assert "entry.target.classList.toggle('hw-paused', !entry.isIntersecting)" in JS
        assert "var parts = [hero].concat(sections);" in JS and "if (footer) parts.push(footer);" in JS
        assert "rest.observe(part)" in JS
        assert re.search(r"\.hw-paused \.hw-decor \*\s*\{\s*animation-play-state:\s*paused", CSS)

    def test_the_candle_flickers_in_the_face_and_the_halo_together(self):
        """One flame: the lit face and the halo on one animation, at the pace of their pumpkin.
        A near pumpkin has a pace of its own, so that no two flicker as one; a far one, blurred
        as a whole, stays still, or its blur would be drawn again at every frame."""
        assert re.search(r"\.hw-halo,\s*\.hw-lit\s*\{\s*animation:\s*hw-flicker var\(--hw-flame, [\d.]+s\)"
                         r" ease-in-out var\(--hw-flame-at, [\d.]+s\) infinite", CSS)
        assert re.search(r"\.hw-far \.hw-halo,\s*\.hw-far \.hw-lit\s*\{\s*animation:\s*none", CSS)
        laid = re.findall(r"pumpkin\('([\w -]+)', '[a-d]'\)", JS)
        near = {p for p in laid if "hw-far" not in p}
        assert {"hw-pk-a", "hw-pk-b", "hw-pk-c", "hw-pk-cc", "hw-pk-ca", "hw-pk-ea"} <= near
        paces = {}
        for place in near:
            rule = re.search(r"\.%s\s*\{([^}]*)\}" % place, CSS).group(1)
            pace = re.search(r"--hw-flame: ([\d.]+s); --hw-flame-at: (-?[\d.]+s)", rule)
            assert pace, f"{place} flickers at the common pace"
            paces[place] = pace.groups()
        assert len({d for d, _ in paces.values()}) == len(paces), "two pumpkins flicker as one"


class TestDownThePage:
    """Bats and spiders from the hero to the last section, never over a line of text: in the
    band at each section's top, and in the margins beside its text where there are any."""

    def test_every_section_has_its_own_skies(self):
        """Every one, but the figures that close "End the jitter": one band with it, no top
        padding and no edge, so no band to fly in nor top to hang from."""
        assert "document.querySelectorAll('.section')" in JS
        skipped = re.findall(r"section\.classList\.contains\('([\w-]+)'\)", JS)
        assert skipped == ["rt-proof"]
        assert re.search(r'<section class="section rt-proof">', PAGE), "the figures moved: see what is skipped"
        assert re.search(r"\.section\.rt-proof\s*\{\s*padding-top:\s*0", SITE_CSS)
        assert re.search(r"\.halloween \.hero,\s*\.halloween \.section\s*\{\s*position:\s*relative", CSS)

    def test_the_band_stays_above_every_label(self):
        """A section's label comes after its top padding, on a phone as on a wide screen."""
        band = int(re.search(r"\.hw-sky-top\s*\{[^}]*height:\s*(\d+)px", CSS).group(1))
        wide = int(re.search(r"^\.section\s*\{\s*padding:\s*(\d+)px", SITE_CSS, re.M).group(1))
        # The phone's own block: the rule first in it, after its comment at most — a looser
        # pattern ran on past the block to the wide screen's rule, and read 100px for 60.
        phone = int(re.search(r"@media\(max-width:720px\)\s*\{\s*(?:/\*(?:(?!\*/).)*\*/\s*)?"
                              r"\.section\s*\{\s*padding:\s*(\d+)px", SITE_CSS, re.S).group(1))
        assert phone < wide
        assert band < phone

    def test_the_margins_are_the_ones_the_page_leaves(self):
        """The section's padding, the column's width and its own padding (style.css, .section
        and .w): the margin's width is worked out from them, and it stops where the column's
        padding drops to a phone's, at the same width."""
        width, inner, outer = _column()
        assert "--hw-margin: calc((100%% - min(100%% - %dpx, %dpx)) / 2 + %dpx)" % (2 * outer, width, inner) in CSS
        assert CSS.count("min(100% -") == 1, "the margin is worked out in more than one place"
        assert re.search(r"^\.hw-sky-margin \{[^}]*width: var\(--hw-margin\)", CSS, re.M)
        phone = re.search(r"@media\(max-width:(\d+)px\)\s*\{\s*\.w\s*\{\s*padding: 0 max\((\d+)px", SITE_CSS)
        assert int(phone.group(2)) < inner, "the column keeps its padding on a phone: see the margins"
        assert re.search(r"@media \(max-width: %spx\) \{\s*\.hw-sky-margin \{\s*display: none" % phone.group(1), CSS)

    def test_the_last_scene_is_as_wide_as_the_column(self):
        """Its ground and its sky start and end where the text does: the margin on either side,
        and on a phone the column's own padding."""
        shared = re.search(r"^\.hw-foot,\s*\.hw-sky-foot \{([^}]*)\}", CSS, re.M).group(1)
        assert re.search(r"left: var\(--hw-margin\);\s*right: var\(--hw-margin\)", shared)
        phone = re.search(r"@media\(max-width:(\d+)px\)\s*\{\s*\.w\s*\{\s*padding: 0 max\((\d+)px", SITE_CSS)
        block = re.search(r"@media \(max-width: %spx\) \{\s*\.hw-foot,\s*\.hw-sky-foot \{([^}]*)\}" % phone.group(1),
                          CSS, re.S)
        assert block and re.search(r"left: %spx;\s*right: %spx" % (phone.group(2), phone.group(2)), block.group(1))

    @pytest.mark.parametrize("n", [8, 9])
    def test_a_bat_in_a_margin_keeps_clear_of_the_text(self, n):
        """In the narrowest margin — the two paddings, on any screen too narrow for the column
        to leave more — the furthest a bat flies out, plus half its width, leaves 12px."""
        _, inner, outer = _column()
        narrowest = inner + outer
        flight = re.search(r"@keyframes hw-fly-b%d\{(.*)\}" % n, CSS).group(1)
        furthest = max(float(x) for x in re.findall(r"translate\((-?[\d.]+)cqw", flight))
        half = int(re.search(r"\.hw-b%d svg \{ width: (\d+)px" % n, CSS).group(1)) / 2
        assert furthest / 100 * narrowest + half <= narrowest - 12, f"b{n} flies {furthest}cqw out"


class TestTheLastScene:
    """Lit pumpkins standing on the footer's top edge, and a last spider hung from it."""

    def test_it_stands_on_the_footers_top_edge(self):
        assert re.search(r"lay\(footer, 'hw-foot', pumpkin\(", JS)
        assert re.search(r"\.halloween footer\s*\{\s*position:\s*relative", CSS)
        ground = re.search(r"^\.hw-foot \{([^}]*)\}", CSS, re.M).group(1)
        assert re.search(r"height:\s*0\b", ground)
        shared = re.search(r"^\.hw-foot,\s*\.hw-sky-foot \{([^}]*)\}", CSS, re.M).group(1)
        assert re.search(r"top:\s*0\b", shared)
        # The far one stands further back, so higher up; the others rest on the edge.
        far = {p.split()[0] for p in re.findall(r"pumpkin\('([\w -]+)', '[a-d]'\)", JS) if "hw-far" in p}
        wide, _ = _foot_rules()
        assert far & set(wide), "no far pumpkin at the foot: see what stands higher up"
        for place, rule in wide.items():
            if place not in far:
                assert _px(rule, "bottom") <= 0, f"{place} floats over the edge"

    @pytest.mark.parametrize("screen", ["wide", "phone"])
    def test_each_pumpkin_fits_the_room_above_the_edge(self, screen):
        """The last section's bottom padding, 100px (60px on a phone), less 6px: a pumpkin
        taller than the room would stand on its last lines."""
        wide_room = int(re.search(r"^\.section\s*\{\s*padding:\s*(\d+)px", SITE_CSS, re.M).group(1))
        phone_room = int(re.search(r"@media\(max-width:720px\)\s*\{\s*(?:/\*(?:(?!\*/).)*\*/\s*)?"
                                   r"\.section\s*\{\s*padding:\s*(\d+)px", SITE_CSS, re.S).group(1))
        wide, phone = _foot_rules()
        room = wide_room if screen == "wide" else phone_room
        for place, rule in wide.items():
            own = phone.get(place, "") if screen == "phone" else ""
            if "display: none" in own:
                continue
            width = _px(own, "width") or _px(rule, "width")
            bottom = _px(own, "bottom")
            bottom = _px(rule, "bottom") if bottom is None else bottom
            assert bottom + width * 170 / 200 <= room - 6, f"{place} on a {screen} screen"

    @pytest.mark.parametrize("screen", ["wide", "phone"])
    def test_the_last_spider_hangs_in_the_footers_empty_top(self, screen):
        """Its sky is the footer's top padding, and at its lowest the spider keeps 6px above
        the footer's first line."""
        if screen == "wide":
            top = int(re.search(r"^footer\s*\{[^}]*padding:\s*(\d+)px", SITE_CSS, re.M).group(1))
            sky = int(re.search(r"^\.hw-sky-foot \{\s*height: (\d+)px", CSS, re.M).group(1))
            width = int(re.search(r"^\.hw-spider \{[^}]*width: (\d+)px", CSS, re.M).group(1))
        else:
            top = int(re.search(r"@media\(max-width:720px\)\s*\{\s*footer\s*\{\s*padding:\s*(\d+)px", SITE_CSS).group(1))
            block = re.search(r"@media \(max-width: 720px\) \{\s*\.hw-foot,\s*\.hw-sky-foot \{(.*?)\n\}", CSS, re.S).group(1)
            sky = int(re.search(r"\.hw-sky-foot \{\s*height: (\d+)px", block).group(1))
            width = int(re.search(r"\.hw-s5 \{ width: (\d+)px", block).group(1))
        assert sky == top
        drop = re.search(r"@keyframes hw-drop-5 \{(.*?)\n\}", CSS, re.S).group(1)
        deepest = max(float(v) for v in re.findall(r"translateY\((-?[\d.]+)px\)", drop))
        assert deepest + width * 44 / 40 <= top - 6

    def test_the_last_spider_is_pale_on_the_dark_footer(self):
        """The footer is dark in both themes — black in the light one, #1a1a1a in the dark —
        so the spider is not drawn in the page's ink there, which would be dark on dark."""
        assert re.search(r"^footer\s*\{\s*background:\s*var\(--inv\)", SITE_CSS, re.M)
        assert re.search(r"^:root\s*\{[^}]*--inv:\s*#000\b", SITE_CSS, re.M)
        assert re.search(r"\[data-theme=\"dark\"\] footer \{ background: #1a1a1a \}", SITE_CSS)
        assert re.search(r"\.hw-sky-foot \.hw-spider svg \{\s*fill: #c3bad6;\s*stroke: #c3bad6", CSS)
        assert re.search(r"\.hw-sky-foot \.hw-spider::before \{\s*background: rgba\(195, 186, 214", CSS)


class TestTheStrip:
    """The strip that shows a track playing plays Danse macabre that day."""

    def test_its_cover_is_there_at_the_strips_size(self):
        src = re.search(r"cover\.src = '([^']+)'", JS).group(1)
        img = re.search(r'<img class="np-cover" src="[^"]+" width="(\d+)" height="(\d+)"', PAGE)
        assert _webp_size(ROOT / src) == (int(img.group(1)), int(img.group(2)))

    def test_what_it_changes_is_on_the_page(self):
        """A class renamed in the page would leave the usual track in place, and say nothing."""
        strip = re.search(r'<section class="np-strip">(.*?)</section>', PAGE, re.S).group(1)
        for cls in re.findall(r"(?:strip|progress)\.querySelector\('\.([\w-]+)'\)", JS):
            assert re.search(r'class="(?:[^"]* )?%s[ "]' % re.escape(cls), strip), cls
        times = re.findall(r"<span>([^<]*)</span>",
                           re.search(r'<div class="np-progress"[^>]*>(.*?)</div>', strip, re.S).group(1))
        assert len(times) == 2 and re.fullmatch(r"\d+:\d\d", times[0])
        # The time left keeps its minus sign: only its figures are replaced.
        assert re.search(r"\d+:\d\d", times[1]) and not times[1][0].isdigit()

    def test_its_lines_are_no_longer_than_the_usual_ones(self):
        """A longer line can take one more on a phone: "Saint-Saëns — Charles Dutoit" took two
        at 390px where "The Beatles — Abbey Road" takes one (measured in Chromium, 2026-10-25).
        Characters stand for width here, which a proportional font only roughly allows."""
        strip = re.search(r'<section class="np-strip">(.*?)</section>', PAGE, re.S).group(1)
        for cls in ("track-name", "track-artist"):
            usual = re.search(r'<div class="%s">([^<]*)</div>' % cls, strip).group(1)
            today = re.search(r"\.%s'\)\.textContent = '([^']*)'" % cls, JS).group(1)
            assert len(today) <= len(usual), f"{cls}: {today!r} is longer than {usual!r}"

    def test_the_time_and_the_bar_agree(self):
        """What the label says, what the strip writes and how full the bar is: one moment of
        the recording, whose length the script gives."""
        total = re.search(r"(\d+):(\d\d) in all", JS).groups()
        label = re.search(r"aria-label', '(\d+):(\d\d) played, (\d+):(\d\d) left'", JS).groups()
        played, left = int(label[0]) * 60 + int(label[1]), int(label[2]) * 60 + int(label[3])
        assert played + left == int(total[0]) * 60 + int(total[1])
        assert "firstElementChild.textContent = '%s:%s';" % label[:2] in JS
        assert ", '%s:%s');" % label[2:] in JS
        fill = float(re.search(r"\.fill'\)\.style\.width = '([\d.]+)%'", JS).group(1))
        assert abs(fill - 100 * played / (played + left)) < 0.1


class TestTheTitle:
    """A pumpkin in the tab's title, and the site's icon left alone."""

    def test_the_tab_carries_a_pumpkin(self):
        code = re.search(r"document\.title = String\.fromCodePoint\((0x[0-9A-Fa-f]+)\) \+ ' ' \+ document\.title;", JS)
        assert code and unicodedata.name(chr(int(code.group(1), 16))) == "JACK-O-LANTERN"

    def test_the_sites_icon_is_left_alone(self):
        """A browser may keep an icon well past the day."""
        assert not re.search(r"link\[rel|rel=.?icon|\.href\s*=", JS)


def _foot_rules() -> tuple[dict[str, str], dict[str, str]]:
    """The pumpkins at the foot of the page, as halloween.css sizes them.

    Returns:
        Each pumpkin's class mapped to its declarations: on a screen wider than a phone, and on
        a phone, whose rules override only some of them.
    """
    wide = {m.group(1): m.group(2) for m in re.finditer(r"^\.(hw-pk-e\w)\s*\{([^}]*)\}", CSS, re.M)}
    block = re.search(r"@media \(max-width: 720px\) \{\s*\.hw-foot,\s*\.hw-sky-foot \{(.*?)\n\}", CSS, re.S).group(1)
    phone = {m.group(1): m.group(2) for m in re.finditer(r"\.(hw-pk-e\w)\s*\{([^}]*)\}", block)}
    assert wide and set(phone) <= set(wide)
    return wide, phone


def _px(rule: str, prop: str) -> float | None:
    """A length in px from a rule's declarations.

    Args:
        rule: The declarations, between the braces.
        prop: The property, e.g. ``width``.

    Returns:
        Its value in px, or None when the rule does not set it.
    """
    found = re.search(r"(?:^|[;{\s])%s:\s*(-?[\d.]+)px" % re.escape(prop), rule)
    return float(found.group(1)) if found else None


def _webp_size(path: Path) -> tuple[int, int]:
    """The width and height of a WebP image, read from its header.

    Args:
        path: The image.

    Returns:
        Its width and height, in pixels.
    """
    data = path.read_bytes()[:30]
    assert data[:4] == b"RIFF" and data[8:12] == b"WEBP", f"{path.name} is not a WebP image"
    chunk = data[12:16]
    if chunk == b"VP8X":
        return 1 + int.from_bytes(data[24:27], "little"), 1 + int.from_bytes(data[27:30], "little")
    if chunk == b"VP8 ":
        return int.from_bytes(data[26:28], "little") & 0x3FFF, int.from_bytes(data[28:30], "little") & 0x3FFF
    if chunk == b"VP8L":
        bits = int.from_bytes(data[21:25], "little")
        return 1 + (bits & 0x3FFF), 1 + ((bits >> 14) & 0x3FFF)
    raise AssertionError(f"{path.name}: no size in a {chunk!r} chunk")


def _column() -> tuple[int, int, int]:
    """The text column down the page, as style.css lays it out.

    Returns:
        The column's widest (.w max-width), its own padding, and the section's padding beside
        it, all in px, on a screen wider than a phone.
    """
    column = re.search(r"^\.w\s*\{\s*max-width:\s*(\d+)px;.*?padding: 0 max\((\d+)px", SITE_CSS, re.S | re.M)
    section = re.search(r"^\.section\s*\{\s*padding:\s*\d+px (\d+)px", SITE_CSS, re.M)
    return int(column.group(1)), int(column.group(2)), int(section.group(1))

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
