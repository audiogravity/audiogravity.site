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



def _announce_script() -> str:
    """The script right after the announce bar: the bar's writer, and what it says before the day."""
    after = PAGE[PAGE.index('<div class="announce-bar">'):]
    return re.search(r"</div>\s*<script>(.*?)</script>", after, re.S).group(1)


def _run_announce(now: str, steps: tuple = (), fade: str = "0.18s") -> dict:
    """Run that script under Node at a given instant, on a stand-in for the bar and a clock of its own.

    Args:
        now: The visitor's local date and time, ISO 8601 without a zone.
        steps: What happens next, in order: a number of milliseconds to let pass, or an event on
            the bar ("mouseenter", "mouseleave", "focusin", "focusout").
        fade: The links' transition length, as the browser reports it.

    Returns:
        Which link shows at the start and after each step ("release", "news", or "fading" while
        the bar fades), where the news leads and what it says (None when it was never written),
        every property the script wrote on the release's link, and each reading of a link's
        opacity: which link, whether the bar was fading, whether the link was hidden.
    """
    harness = """
        const RealDate = Date;
        const fixed = new RealDate(%(now)s).getTime();
        globalThis.Date = class extends RealDate {
            constructor(...a) { a.length ? super(...a) : super(fixed); }
            static now() { return fixed; }
        };
        let clock = 0;
        let last = 0;
        const timers = new Map();
        globalThis.setTimeout = (fn, ms) => { timers.set(++last, { at: clock + (ms || 0), fn }); return last; };
        globalThis.clearTimeout = (id) => { timers.delete(id); };
        const pass = (ms) => {
            const end = clock + ms;
            for (;;) {
                let due = null;
                for (const [id, t] of timers) if (t.at <= end && (!due || t.at < due[1].at)) due = [id, t];
                if (!due) break;
                timers.delete(due[0]);
                clock = due[1].at;
                due[1].fn();
            }
            clock = end;
        };
        const wrote = [];
        const release = new Proxy({ hidden: false }, { set(t, k, v) { wrote.push(k); t[k] = v; return true; } });
        const news = { hidden: true, href: '', said: null, firstChild: null,
                       set textContent(v) { this.said = null; this.firstChild = null; },
                       append(...parts) {
                           this.said = parts.map((p) => typeof p === 'string' ? p : p.textContent);
                           this.firstChild = parts[0];
                       } };
        const classes = new Set();
        const listeners = {};
        const bar = {
            classList: { add: (c) => classes.add(c), remove: (c) => classes.delete(c) },
            addEventListener: (type, fn) => { listeners[type] = fn; },
            querySelector: (s) => (s === 'a:not(.announce-news)' ? release : s === '.announce-news' ? news : null),
        };
        globalThis.window = globalThis;
        const reads = [];
        const name = (el) => (el === release ? 'release' : el === news ? 'news' : '?');
        globalThis.getComputedStyle = (el) => ({
            transitionDuration: %(fade)s,
            get opacity() { reads.push([name(el), classes.has('announce-turning'), !!el.hidden]); return '0'; },
        });
        globalThis.document = {
            querySelector: (s) => (s === '.announce-bar' ? bar : null),
            createElement: () => ({ className: '', textContent: '' }),
        };
        %(script)s
        const showing = () => (classes.has('announce-turning') ? 'fading'
            : release.hidden === news.hidden ? 'both or none' : release.hidden ? 'news' : 'release');
        const seen = [showing()];
        for (const step of %(steps)s) {
            if (typeof step === 'number') pass(step); else listeners[step]();
            seen.push(showing());
        }
        console.log(JSON.stringify({ seen, href: news.href, said: news.said, wrote, reads }));
    """ % {"now": json.dumps(now), "steps": json.dumps(list(steps)), "fade": json.dumps(fade),
           "script": _announce_script()}
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
        thread = float(re.search(r"\.hw-s%d \{[^}]*--hw-thread-length: ([\d.]+)px" % n, CSS).group(1))
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
        """Nor ghosts: the one at the foot of the page lives outside any sky."""
        block = re.search(r"@media \(prefers-reduced-motion: reduce\)\s*\{(.*?)\n\}", CSS, re.S).group(1)
        assert re.search(r"\.hw-sky,\s*\.hw-ghost\s*\{\s*display:\s*none", block)
        assert re.search(r"\.hw-halo,\s*\.hw-lit,\s*\.hw-fog\s*\{\s*animation:\s*none", block)

    def test_the_heros_ghost_rises_behind_the_pumpkins_at_the_phones_foot(self):
        """Laid before the near pumpkins, so behind them; out of a panel too narrow for the scene
        beside the phone, with the pumpkins that leave; and clear of the caption, which from
        1551px stands at the phone's mid-height on that side, far above the foot."""
        assert re.search(r"MIST_BACK\s*\+ ghost\(3\) \+ pumpkin\('hw-pk-c', 'c'\)", JS)
        narrow = re.search(r"@container hw-panel \(max-width: 599px\) \{\s*([^{]*)\{\s*display: none", CSS).group(1)
        assert ".hw-g3" in narrow and ".hw-pk-c" in narrow
        assert re.search(r"^\.hero-caption \{[^}]*top: 50%", SITE_CSS, re.M), "the caption moved: see the hero's ghost"

    def test_every_ghost_has_its_motion(self):
        """Each ghost built has its rule and its keyframes, and stays unseen without them."""
        built = {int(n) for n in re.findall(r"\bghost\((\d)", JS)}
        assert built == {1, 2, 3}
        for n in built:
            name = re.search(r"\.hw-g%d \{[^}]*animation-name: ([\w-]+)" % n, CSS).group(1)
            assert re.search(r"@keyframes %s \{" % re.escape(name), CSS), f"ghost {n} has no {name}"
        assert re.search(r"^\.hw-ghost \{[^}]*opacity: 0", CSS, re.M), "a ghost without its motion would stand still in sight"
        assert re.search(r"^\.hw-ghost svg \{[^}]*fill: var\(--hw-ink\)", CSS, re.M)

    def test_it_rests_while_out_of_sight(self):
        """Part by part — the hero, each section, the footer — rather than the whole page with
        the hero, now that the decoration runs down the page."""
        assert "IntersectionObserver" in JS
        assert "entry.target.classList.toggle('hw-paused', !entry.isIntersecting)" in JS
        assert "var parts = [hero].concat(sections);" in JS and "if (footer) parts.push(footer);" in JS
        assert "rest.observe(part)" in JS
        assert re.search(r"\.hw-paused \.hw-decor \*,?[^{]*\{\s*animation-play-state:\s*paused", CSS)

    def test_the_footers_pumpkins_keep_their_light_in_sight(self):
        """They stand above the footer that pauses them, their glow higher still: the screen is
        taken taller at its foot by as much, or their candles froze in sight while the footer
        was just under the screen (measured: 35px under it, the large one fully shown)."""
        margin = re.search(r"rootMargin: '0px 0px (\d+)px 0px'", JS)
        assert margin, "the screen is no longer taken taller at its foot"
        # The glow is a circle drawn past the pumpkin's box: its top, in the box's units.
        halo = re.search(r'<circle cx="100" cy="(\d+)" r="(\d+)" fill="url\(#hw-halo\)"', JS)
        box = re.search(r'<svg class="hw-halo" viewBox="0 0 (\d+) (\d+)"', JS)
        above = int(halo.group(2)) - int(halo.group(1))
        width, height = (int(v) for v in box.groups())
        wide, _ = _foot_rules()
        tallest = max(_px(rule, "bottom") + _px(rule, "width") * (height + above) / width for rule in wide.values())
        assert int(margin.group(1)) >= tallest

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
        assert re.search(r"lay\(footer, 'hw-foot', ghost\(2\) \+ pumpkin\(", JS), "the ghost no longer rises from behind"
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

    def test_a_ghost_is_drawn_once(self):
        """Like the pumpkins' bodies: one drawing in DEFS, used by every ghost down the page."""
        assert '<symbol id="hw-ghost" viewBox="0 0 40 50">' in JS
        assert "var GHOST = '<svg viewBox=\"0 0 40 50\"><use href=\"#hw-ghost\" /></svg>';" in JS
        assert JS.count("M4 44V20A16 16 0 0 1 36 20V44") == 1

    def test_the_ghost_stays_in_the_room_above_the_edge(self):
        """At its highest, under the last section's bottom padding less 6px, as the pumpkins;
        on a phone, whose room is 60px, it is not drawn."""
        room = int(re.search(r"^\.section\s*\{\s*padding:\s*(\d+)px", SITE_CSS, re.M).group(1))
        rule = re.search(r"^\.hw-g2 \{([^}]*)\}", CSS, re.M).group(1)
        width = int(re.search(r"^\.hw-ghost \{[^}]*width: (\d+)px", CSS, re.M).group(1))
        view = re.search(r'var GHOST = \'<svg viewBox="0 0 (\d+) (\d+)"', JS)
        height = width * int(view.group(2)) / int(view.group(1))
        rise = re.search(r"@keyframes hw-rise \{(.*?)\n\}", CSS, re.S).group(1)
        highest = -min(float(v) for v in re.findall(r"translateY\((-?[\d.]+)px\)", rise))
        assert _px(rule, "bottom") + height + highest <= room - 6
        # And at its lowest, out of sight behind the pumpkin rather than over the footer: sunk
        # 34px, its tails showed under the edge as it faded (36/255 on a pixel, measured).
        assert rise.count("translateY(var(--hw-sink, 34px))") == 2
        pumpkin = re.search(r"^\.hw-pk-eb \{([^}]*)\}", CSS, re.M).group(1)
        assert _px(rule, "bottom") - _px(rule, "--hw-sink") >= _px(pumpkin, "bottom")
        assert re.search(r"@media \(max-width: 720px\) \{\s*\.hw-g2 \{\s*display: none", CSS)

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
        assert re.search(r"\.hw-sky-foot \.hw-spider \{\s*--hw-ink: var\(--hw-pale-ink\);"
                         r"\s*--hw-thread: var\(--hw-pale-thread\)", CSS)


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

    def test_it_can_play_an_excerpt_at_a_press_only(self):
        """The excerpt is asked for at the first press, never by the page: a browser plays no
        sound before the visitor has pressed something, and a file nobody plays costs nothing."""
        code = JS[JS.index("function listen(progress)"):]
        src = re.search(r"new Audio\('([^']+)'\)", code).group(1)
        audio = ROOT / src
        assert audio.is_file(), f"{src} is missing"
        head = audio.read_bytes()[:12]
        assert head[4:8] == b"ftyp", f"{src} is not an MP4 audio file"
        assert audio.stat().st_size < 1_500_000, f"{src} weighs {audio.stat().st_size} bytes"
        assert code.count("new Audio(") == 1 and code.count("fresh()") == 1
        assert code.index("sound = fresh();") > code.index("button.addEventListener('click'"), "fetched before a press"
        assert src not in PAGE and JS.count(src) == 1, "the excerpt is named outside the press"

    def test_while_the_excerpt_plays_the_strip_shows_what_is_heard(self):
        """Its own format, as the file says, and its own time, by the sound's own clock (no timer
        of the page's); paused, over or failed, the box's again, as the strip stood. An
        audiophile reading DSD256 over a browser's AAC preview would be right to feel misled."""
        code = JS[JS.index("function listen(progress)"):JS.index("document.title =")]
        heard = re.search(r"var heard = \['([^']*)', '([^']*)', '([^']*)', '([^']*)'\];", code).groups()
        cells = re.findall(r'<div class="cell[^"]*"><span>([^<]+)</span>', PAGE)
        assert cells == ["Format", "Sample", "Bitrate", "Codec"], "the strip's cells moved: see heard"
        audio = (ROOT / re.search(r"new Audio\('([^']+)'\)", code).group(1)).read_bytes()
        mp4a = audio.index(b"mp4a")
        rate = int.from_bytes(audio[mp4a + 28:mp4a + 32], "big") >> 16
        mvhd = audio.index(b"mvhd")
        if audio[mvhd + 4] == 0:
            scale, length = (int.from_bytes(audio[mvhd + i:mvhd + i + 4], "big") for i in (16, 20))
        else:
            scale = int.from_bytes(audio[mvhd + 24:mvhd + 28], "big")
            length = int.from_bytes(audio[mvhd + 28:mvhd + 36], "big")
        kbps = len(audio) * 8 / (length / scale) / 1000
        assert heard[0] == heard[3] == "AAC"
        assert heard[1] == f"{rate / 1000:g}kHz"
        assert abs(int(heard[2].removesuffix("kbps")) - kbps) / kbps < .02
        assert "if (!element.paused) show(element.currentTime, element.duration || 30);" in code
        assert "show(element.currentTime, element.duration || 30);\n                return;" in code
        pause = code[code.index("element.addEventListener('pause'"):]
        error = code[code.index("element.addEventListener('error'"):]
        assert "hearing(null);" in pause[:pause.index("});")] and "hearing(null);" in error[:error.index("});")]
        assert not re.search(r"setInterval|setTimeout|requestAnimationFrame", code)
        assert "progress.setAttribute('aria-label', clock(s) + ' played, ' + clock(total - s) + ' left')" in code

    def test_a_failed_load_does_not_silence_the_button(self):
        """A failed element stays failed: the next press must start from a new one."""
        code = JS[JS.index("function listen(progress)"):JS.index("document.title =")]
        error = code[code.index("element.addEventListener('error'"):]
        assert "if (sound === element) sound = null;" in error[:error.index("});")]
        assert "if (!sound) sound = fresh();" in code

    def test_its_button_sits_beside_the_time_without_moving_the_page(self):
        """Not in the progress row, which assistive technology reads as an image whose content is
        not read; and no taller than the time's 16px row (measured in Chromium), so that nothing
        under the strip moves when it is put in."""
        assert re.search(r'<div class="np-progress" role="img"', PAGE)
        code = JS[JS.index("function listen(progress)"):JS.index("document.title =")]
        assert "row.appendChild(button);\n        row.appendChild(progress);" in code
        assert "progress.insertBefore(button" not in code and "progress.appendChild(button" not in code
        button = re.search(r"^\.hw-np-play \{([^}]*)\}", CSS, re.M).group(1)
        margin = float(re.search(r"margin: (-[\d.]+)px 0;", button).group(1))
        assert _px(button, "height") + 2 * margin <= 16
        gap = int(re.search(r"^\.np-visual \{[^}]*gap: (\d+)px", SITE_CSS, re.M).group(1))
        assert -margin < gap, "the button would reach the cells above or the line below"

    def test_its_button_is_a_real_button_with_the_carousels_icons(self):
        """Named for what a press will do, reached by the keyboard, and wearing the carousel's
        play and pause icons, copied from it rather than drawn a second time."""
        code = JS[JS.index("function listen(progress)"):]
        assert "button.type = 'button';" in code
        assert "playing ? 'Pause the excerpt' : 'Play an excerpt'" in code
        assert "document.querySelector('#heroPlay .ic-play')" in code and "cloneNode(true)" in code
        hero = re.search(r'<button class="hero-ctrl" id="heroPlay"[^>]*>(.*?)</button>', PAGE, re.S).group(1)
        assert 'class="ic-play"' in hero and 'class="ic-pause"' in hero
        assert re.search(r"^\.hw-np-play:focus-visible \{", CSS, re.M)

    def test_the_cover_is_named_as_the_title_is_written(self):
        """One work, one spelling, in the image's name as in the strip."""
        title = re.search(r"\.track-name'\)\.textContent = '([^']*)'", JS).group(1)
        alt = re.search(r"cover\.alt = '([^']*)'", JS).group(1)
        assert title in alt

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
        assert not re.search(r"link\[rel|rel=.?icon", JS)
        # It changes no address itself: the news's, in the announce bar, is written by the page's
        # own writer of that news (window.agAnnounce, in index.html).
        assert not re.search(r"\.href\s*=", JS)


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


class TestWhatItAsksOfTheBrowser:
    """What a browser too old for some of it is spared, and what every browser is asked to
    keep. These three sat for a while under a helper function, where pytest never collects a
    test: the first of them, older, had stopped running unnoticed (found 2026-10-25, by a
    mutation the suite let through)."""

    def test_a_browser_without_container_units_gets_nothing_they_place(self):
        """Such a browser (Safari before 16) drops every declaration written with them: the
        bats piled in a corner, the panel's web grew to 300px over the phone, the pumpkins at the
        phone's foot hung under it. What they place stays out instead — and every rule that
        places with them names a piece of what stays out, so that a new one cannot slip past."""
        block = re.search(r"@supports not \(width: 1cqw\)\s*\{\s*([^{]*)\{\s*display:\s*none", CSS)
        assert block, "nothing is kept out for a browser without container units"
        assert {s.strip() for s in block.group(1).split(",")} == {".hw-sky", ".hw-web-panel", ".hw-ground"}
        plain = re.sub(r"/\*.*?\*/", "", CSS, flags=re.S)
        # Flights and drops only run in the skies; container queries are skipped whole.
        plain = re.sub(r"@(?:keyframes|container)[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", "", plain)
        held = re.compile(r"\.hw-(?:sky|bat|b\d|spider|s\d|web-panel|ground|fog)|\.hw-pk-(?:a|b|c|f1|f2)(?![\w-])")
        placed = 0
        for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", plain):
            if re.search(r"\dcq(?:w|h|i|b|min|max)\b", body):
                for selector in selectors.split(","):
                    placed += 1
                    assert held.match(selector.strip()), \
                        f"{selector.strip()} is placed with container units, outside what the fallback keeps out"
        assert placed, "no rule uses container units any more: see what the fallback keeps out"

    def test_each_ink_is_written_once(self):
        """The bats', spiders' and webs' ink, dark on light and pale on dark: written once each,
        and read by the pieces; it used to be repeated in six theme blocks."""
        plain = re.sub(r"/\*.*?\*/", "", CSS, flags=re.S)
        for value in ("#c3bad6", "rgba(195, 186, 214, .45)", "rgba(222, 216, 236, .26)",
                      "#1d1a24", "rgba(29, 26, 36, .45)", "rgba(40, 38, 48, .32)"):
            assert plain.count(value) == 1, f"{value} is written {plain.count(value)} times"
        assert re.search(r"\.hw-bat svg \{[^}]*fill: var\(--hw-ink\)", plain)
        assert re.search(r"\.hw-spider \{[^}]*background: linear-gradient\(var\(--hw-thread\), var\(--hw-thread\)\)", plain)
        assert re.search(r"\.hw-spider svg \{[^}]*fill: var\(--hw-ink\);\s*stroke: var\(--hw-ink\)", plain)
        assert re.search(r"\.hw-web svg \{[^}]*stroke: var\(--hw-web\)", plain)
        dark = r"\{\s*--hw-ink: var\(--hw-pale-ink\);\s*--hw-thread: var\(--hw-pale-thread\);\s*--hw-web: var\(--hw-pale-web\)"
        assert re.search(r"^\[data-theme=\"dark\"\] " + dark, plain, re.M)
        assert re.search(r":root:not\(\[data-theme=\"light\"\]\) " + dark, plain)

    def test_the_thread_is_drawn_in_the_spiders_own_box(self):
        """Hanging out of the box as a ::before sized in container units, the thread showed in
        Chromium and in WebKit 26 but not in the user's Safari (capture of 2026-10-25). In the box,
        a stripe of background down its padding, in px: no pseudo-element anywhere in the
        decoration, and every spider says how long its thread is."""
        plain = re.sub(r"/\*.*?\*/", "", CSS, flags=re.S)
        assert not re.search(r"::(?:before|after)", plain), "the decoration draws in a pseudo-element again"
        box = re.search(r"^\.hw-spider \{([^}]*)\}", plain, re.M).group(1)
        assert re.search(r"margin-top: calc\(-1 \* var\(--hw-thread-length\)\)", box)
        assert re.search(r"padding-top: var\(--hw-thread-length\)", box)
        assert re.search(r"background: linear-gradient\(var\(--hw-thread\), var\(--hw-thread\)\) 50% 0 / 1px "
                         r"var\(--hw-thread-length\) no-repeat", box)
        lengths = {}
        for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", plain):
            length = re.search(r"--hw-thread-length: ([^;\s}]+)", body)
            if length:
                for selector in selectors.split(","):
                    lengths[selector.strip()] = length.group(1)
        for n in {int(n) for n in re.findall(r"\bspider\((\d)", JS)}:
            assert f".hw-s{n}" in lengths, f"spider {n} does not say how long its thread is"
            assert re.fullmatch(r"\d+px", lengths[f".hw-s{n}"]), f"spider {n}'s thread is not in px"
        # The hero's drops are shares of the panel, 34% at most.
        for n in (1, 2):
            assert int(lengths[f".hw-s{n}"][:-2]) >= 1000

    def test_nothing_asks_for_a_layer_of_its_own(self):
        """The browser gives a piece a layer while it moves; will-change kept a hundred alive
        down the page, which every frame had to lay out again (38% of a CPU slowed four times
        mid-page against 30% without, measured in Chromium)."""
        assert "will-change" not in re.sub(r"/\*.*?\*/", "", CSS, flags=re.S)


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


RULES = (ROOT / "orange-ghost.html").read_text(encoding="utf-8")


class TestTheOrangeGhost:
    """The day's game. The licence server decides everything (audiogravity.lic, routers/ghost.py):
    the page asks it once a visit, shows what it answers, and cannot make a ghost appear nor know
    a key before it is given."""

    def test_the_site_asks_the_licence_server_once_a_visit(self):
        assert re.search(r"location\.hostname === 'audiogravity\.app'\s*\?\s*"
                         r"'https://lic\.audiogravity\.app:8443/ls/portal/'", JS)
        assert JS.count("ask('ghost-draw')") == 1
        assert len(re.findall(r"^\s*hunt\(\);$", JS, re.M)) == 1, "the game is asked for more than once"
        assert JS.count("ask('ghost-claim'") == 1
        # Bounded: a server that does not answer leaves the page as it is.
        assert "AbortSignal.timeout(8000)" in JS

    def test_nothing_the_server_says_is_written_as_markup(self):
        """The key and the counts go in as text; the only markup is the page's own words."""
        for value in re.findall(r"innerHTML\s*=\s*([^;]+);", JS):
            assert "answer" not in value and "mine" not in value and "data" not in value, value
        assert "dialog.querySelector('code').textContent = mine.key" in JS
        bar = _announce_script()
        assert "sentence.textContent = item.sentence;" in bar and "short.textContent = item.short;" in bar
        # A key is shown, or kept, only in its own shape.
        assert "var KEY = /^AG(-[A-Z0-9]{4}){4}$/;" in JS
        assert "KEY.test(mine.key || '')" in JS and "KEY.test(mine.key)" in JS

    def test_the_ghost_is_a_real_button_outside_the_hidden_decoration(self):
        """In a section of its own, not in a piece laid with aria-hidden and deaf to the pointer."""
        assert "var button = document.createElement('button');" in JS
        assert "button.className = 'hw-orange';" in JS
        assert "section.appendChild(button);" in JS
        assert "button.setAttribute('aria-label', 'An orange ghost: catch it to win a lifetime licence');" in JS

    def test_it_waits_in_the_band_above_every_label(self):
        """The band the bats and the spiders use: under its height, which stays above every label
        (TestDownThePage), on a phone as on a wide screen — and 44px to the finger."""
        rule = re.search(r"^\.hw-orange \{([^}]*)\}", CSS, re.M).group(1)
        band = int(re.search(r"\.hw-sky-top\s*\{[^}]*height:\s*(\d+)px", CSS).group(1))
        assert _px(rule, "width") == _px(rule, "height") == 44
        assert _px(rule, "top") + _px(rule, "height") <= band
        # On the skies' level and laid after them, so in front: under them, a bat would hide it.
        assert re.search(r"z-index: 3;", rule)
        assert JS.index("hunt();") > JS.index("lay(section, 'hw-sky hw-sky-margin hw-margin-r', margins[1]);")

    def test_it_stays_for_a_visitor_who_asked_for_less_motion(self):
        """It is the game, not a decoration: still, but there."""
        reduced = re.search(r"@media \(prefers-reduced-motion: reduce\) \{(.*?)\n\}", CSS, re.S).group(1)
        hidden = re.search(r"\{\s*display: none\s*\}", reduced)
        assert ".hw-orange" not in reduced[:hidden.end()]
        assert re.search(r"\.hw-orange\s*\{\s*animation: none", reduced)

    def test_it_rests_while_out_of_sight(self):
        assert re.search(r"\.hw-paused \.hw-orange\s*\{\s*animation-play-state:\s*paused", CSS)

    def test_it_goes_when_its_ticket_lapses(self):
        """After the seconds the server gave, counted from now: the visitor's clock may be wrong
        by any amount. Unless a claim got no answer — the server may have given the key, and the
        same ticket gives it again: the ghost then stays, to be caught again."""
        assert "}, Math.max(0, +ghost.ttl || 0) * 1000);" in JS
        assert "Date.parse" not in JS
        claim = JS[JS.index("ask('ghost-claim'"):JS.index("function kept()")]
        answered, unanswered = claim.split("}, function () {")
        assert "clearTimeout(lapse);" in answered and "button.remove();" in answered
        assert "clearTimeout(lapse);" in unanswered and "button.remove();" not in unanswered

    def test_a_caught_key_is_kept_on_this_device_for_this_year(self):
        assert "var KEPT = 'ag-orange-ghost';" in JS
        assert "localStorage.setItem(KEPT, JSON.stringify(mine));" in JS
        assert "mine.year === new Date().getFullYear()" in JS

    def test_the_banner_leads_to_the_rules(self):
        assert ("window.agAnnounce({ badge: 'HALLOWEEN', sentence: sentence, short: short, "
                "href: 'orange-ghost.html', open: open });") in JS
        assert '<a href="orange-ghost.html">The rules</a>' in JS

    def test_the_rules_name_the_organiser_and_say_when_and_how(self):
        for words in ("Alexandre Di Marco", "orange-ghost@audiogravity.app", "31 October 2026",
                      "Paris time (UTC+1)", "ten orange ghosts", "twenty minutes",
                      "one chance an hour", "can win one licence", "free of charge",
                      "one moment in each tenth", "keeps no list of players or of winners",
                      "logs each request it receives, with the address it came from"):
            assert words in RULES, words

    def test_the_steps_to_activate_are_the_manuals(self):
        """The window and the rules name the app's own buttons: if the manual renames one, so must
        they."""
        manual = (ROOT / "docs" / "manual" / "07-administration.md").read_text(encoding="utf-8")
        for label in ("LICENSE KEY", "CHECK KEY", "ACTIVATE THIS MACHINE"):
            assert label in manual and label in JS and label in RULES, label

    def test_the_brand_is_written_as_the_site_writes_it(self):
        body = RULES[RULES.index("<body>"):]
        assert "Audiogravi<sup>ty</sup>" in body and not re.search(r"Audiogravity(?!\.app)", body)
        assert "Your lifetime Audiogravi<sup>ty</sup> licence" in JS

    def test_its_window_is_centred_and_its_links_look_like_links(self):
        """The page's reset takes away the margin a browser centres a modal window with, and its
        links lose their underline: both are given back (measured: the window stood in the top
        left corner, in Chromium and in WebKit)."""
        assert re.search(r"^\* \{\s*margin: 0", SITE_CSS, re.M), "the reset moved: see .hw-catch"
        assert re.search(r"^\.hw-catch \{\s*margin: auto;", CSS, re.M)
        assert re.search(r"^\.hw-catch a \{[^}]*text-decoration: underline", CSS, re.M)
        assert re.search(r"\.rules a \{[^}]*text-decoration: underline", RULES)

    def test_it_stands_out_on_every_ground_in_the_apps_orange(self):
        """The orange of the app's own switches (audiogravity.ui, themes/minimal.css, dark:
        --switch-notification-bg), and a control's shape needs 3:1 against its ground: on the
        light page's white and grey band as on the dark page's, it reaches it alone."""
        def luminance(hex_colour):
            if len(hex_colour) == 4:
                hex_colour = "#" + "".join(c * 2 for c in hex_colour[1:])
            channels = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in channels]
            return .2126 * linear[0] + .7152 * linear[1] + .0722 * linear[2]

        def contrast(a, b):
            hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
            return (hi + .05) / (lo + .05)

        rule = re.search(r"^\.hw-orange svg \{([^}]*)\}", CSS, re.M).group(1)
        fill = re.search(r"fill: (#[0-9a-f]{6})", rule).group(1)
        assert fill == "#ea580c" and "stroke" not in rule
        light = re.search(r":root \{[^}]*?--bg: (#[0-9a-f]{3,6});\s*--bg2: (#[0-9a-f]{3,6})", SITE_CSS, re.S)
        dark = re.search(r':root\[data-theme="dark"\] \{[^}]*?--bg: (#[0-9a-f]{3,6});\s*--bg2: (#[0-9a-f]{3,6})',
                         SITE_CSS, re.S)
        grounds = [g for m in (light, dark) for g in m.groups()]
        assert len(grounds) == 4
        for ground in grounds:
            assert contrast(fill, ground) >= 3, (fill, ground)

    def test_a_browser_without_dialog_still_shows_the_key(self):
        """Safari before 15.4 has no <dialog>: it is told the key in a plain message instead."""
        body = JS[JS.index("function windowOf("):JS.index("function reveal(")]
        assert "if (typeof dialog.showModal !== 'function') {\n            window.alert(plain);" in body
        plain = JS[JS.index("function reveal("):JS.index("function tell(")]
        assert re.search(r"'You caught the orange ghost! Your lifetime Audiogravity licence key:\\n\\n' \+ mine\.key", plain)
        assert "ACTIVATE THIS MACHINE" in plain.split("function (dialog)")[1]



@needs_node
class TestTheAnnouncement:
    """Until Halloween 2026 the announce bar's news, taking turns with the release's sentence, says
    what comes on the 31st; that day the game words it; from 1 November there is none, and the
    release's sentence stays alone. By the visitor's clock, as the day is."""

    BEFORE = "2026-10-28T09:00:00"

    def test_the_news_has_a_link_of_its_own_in_the_bar(self):
        """The release's sentence keeps its link, the release script's to write; the news has one
        beside it, hidden until there is news, so that a day without any shows the bar as it was."""
        bar = PAGE[PAGE.index('<div class="announce-bar">'):]
        bar = bar[:bar.index("</div>")]
        assert bar.count("<a") == 2 and bar.rstrip().endswith('<a class="announce-news" hidden></a>')
        assert PAGE.index('<a class="announce-news" hidden></a>') < PAGE.index("window.agAnnounce = function")

    @pytest.mark.parametrize("now", ["2026-10-26T09:00:00", "2026-10-30T23:59:59"])
    def test_until_the_day_the_bar_announces_the_ghost(self, now):
        result = _run_announce(now)
        assert result["href"] == "orange-ghost.html"
        assert result["said"] == ["31 OCT", " ",
                                  "An orange ghost haunts this page on 31 October: ten lifetime licences to win",
                                  "Ten lifetime licences to win", " ", "→"]
        assert result["seen"] == ["release"], "the release's sentence comes first"

    @pytest.mark.parametrize("now", ["2026-10-31T00:00:00", "2026-11-01T08:00:00", "2027-10-25T12:00:00"])
    def test_from_the_day_on_the_release_is_alone(self, now):
        """Without news nothing turns, not even once the pointer or the keyboard has been in the bar
        and left it — the turn would bring an empty link: the bar is the release's, as on any day."""
        steps = (60000, "mouseenter", "mouseleave", "focusin", "focusout", 60000)
        assert _run_announce(now, steps) == {"seen": ["release"] * 7, "href": "", "said": None,
                                             "wrote": [], "reads": []}

    def test_the_release_and_the_news_take_turns_six_seconds_each(self):
        seen = _run_announce(self.BEFORE, (5999, 1, 179, 1, 5999, 1, 180))["seen"]
        assert seen == ["release", "release", "fading", "fading", "news", "news", "fading", "release"]

    @pytest.mark.parametrize("enter, leave", [("mouseenter", "mouseleave"), ("focusin", "focusout")])
    def test_no_turn_while_the_bar_is_read(self, enter, leave):
        """Under the pointer or with the keyboard in it the bar holds still (WCAG 2.2.2); the next
        turn comes six seconds after they leave, not at once."""
        seen = _run_announce(self.BEFORE, (3000, enter, 60000, leave, 5999, 1, 180))["seen"]
        assert seen == ["release", "release", "release", "release", "release", "release", "fading", "news"]

    def test_the_turn_waits_for_the_links_own_fade(self):
        """The links change places once the fade the style sheet gives them is over, however long."""
        seen = _run_announce(self.BEFORE, (6000, 499, 1), fade="0.5s")["seen"]
        assert seen == ["release", "fading", "fading", "news"]

    def test_the_link_shown_fades_in(self):
        """Just shown, a link has no opacity yet for the fade to start from: its style is read while
        the bar is still faded out, or it would appear at once instead of fading in."""
        reads = _run_announce(self.BEFORE, (6180, 6180))["reads"]
        assert reads == [["news", True, False], ["release", True, False]]

    def test_the_releases_words_are_never_written(self):
        """Over rounds of turns, the release's link is only ever shown and hidden."""
        assert set(_run_announce(self.BEFORE, (6180, 6180, 6180))["wrote"]) == {"hidden"}

    def test_a_link_off_its_turn_is_not_drawn(self):
        """`hidden` alone loses to the links' own display (style.css): a rule gives it back. The
        fade is the links' opacity transition, the one the script reads."""
        assert re.search(r"^\.announce-bar a\[hidden\] \{\s*display: none\s*\}", SITE_CSS, re.M)
        assert re.search(r"^\.announce-bar\.announce-turning a \{\s*opacity: 0\s*\}", SITE_CSS, re.M)
        link = re.search(r"^\.announce-bar a \{([^}]*)\}", SITE_CSS, re.M).group(1)
        assert "transition: opacity var(--ease);" in link

    def test_it_leads_to_rules_that_exist(self):
        assert (ROOT / "orange-ghost.html").is_file()
        assert "href: 'orange-ghost.html'" in _announce_script()

    def test_the_game_writes_the_bar_with_the_same_writer(self):
        """One writer of the bar, in the page: the game's day calls it, it does not write its own."""
        assert "window.agAnnounce = function (item) {" in _announce_script()
        assert "createElement('span')" not in JS[JS.index("function announce("):JS.index("function haunt(")]
        assert ".announce-bar" not in JS and ".announce-news" not in JS

    def test_a_phone_reads_the_point_of_each_announcement(self):
        """A phone's bar holds one line, which cut the long sentence before its point ("31 OCT An
        orange ghost haunts this ...", measured at 390px): each says it shorter there."""
        shorts = ["Ten lifetime licences to win", "Find the orange ghost", "Show your licence key",
                  "All the ghosts are caught"]
        assert "short: 'Ten lifetime licences to win'" in _announce_script()
        for short in shorts[1:]:
            assert "'%s'" % short in JS, short
        assert all(len(t) <= 28 for t in shorts)
        base = SITE_CSS.index(".announce-short {\n    display: none\n}")
        phone = re.search(r"@media\(max-width:720px\) \{.*?\n\}", SITE_CSS[SITE_CSS.index(".announce-bar {"):], re.S)
        assert re.search(r"\.announce-long \{\s*display: none", phone.group(0))
        assert re.search(r"\.announce-short \{\s*display: inline", phone.group(0))
        assert base < SITE_CSS.index(phone.group(0)), "the base rule comes after the phone's and wins"
