"""Guards for the landing's Christmas: the days it comes, the theme it opens in, what it costs.

The decoration is fetched on 24 and 25 December only, by the visitor's own clock, or with
?christmas in the address to preview it (index.html: the theme script in <head>, the loader at
the end of <body>; assets/christmas.css, assets/christmas.js and the drawings in
assets/christmas/). The rule that decides is run under Node when Node is installed
(landing_days.py), so that the date is checked as the browser reads it. The rest is held by what
the files say: a page that never fetches the decoration on another day, drawings that are all
there, all used and each whole on its own, nothing standing on the phone, nothing in the text's
way down the page, nothing that moves for a visitor who asked for less motion.

Run with ``python3 -m pytest scripts/`` from the repository root.
"""
import re
from pathlib import Path

import pytest

from landing_days import SITE_CSS, column, contrast, grounds, needs_node, run_announce, run_head

ROOT = Path(__file__).resolve().parent.parent
PAGE = (ROOT / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "assets" / "christmas.css").read_text(encoding="utf-8")
JS = (ROOT / "assets" / "christmas.js").read_text(encoding="utf-8")
DAYS_JS = (ROOT / "assets" / "days.js").read_text(encoding="utf-8")
FIGURES = ROOT / "assets" / "christmas"


def _block(start: str) -> str:
    """A top-level block of the sheet, from the line that opens it to its closing brace.

    Args:
        start: The block's opening, as written (an at-rule's prelude).

    Returns:
        The block's text.
    """
    text = CSS[CSS.index(start):]
    return text[:text.index("\n}\n")]


def _z(selector: str) -> int:
    """The z-index of the first rule written for a selector (a regular expression)."""
    return int(re.search(selector + r"\s*\{[^}]*z-index:\s*(\d+)", CSS).group(1))


def _ratio(name: str) -> float:
    """A drawing's height over its width, from its frame."""
    found = re.search(r'viewBox="-?\d+ -?\d+ (\d+) (\d+)"', (FIGURES / f"{name}.svg").read_text(encoding="utf-8"))
    return int(found.group(2)) / int(found.group(1))


def _rule(cls: str, text: str = CSS) -> str:
    """The declarations of a one-line rule written for a class, the first one found."""
    return re.search(r"^\s*\." + cls + r" \{([^}]*)\}", text, re.M).group(1)


def _phone_block() -> str:
    """The phone's block of the footer's last scene (THE FOOT OF THE PAGE)."""
    foot = CSS[CSS.index("THE FOOT OF THE PAGE"):]
    block = foot[foot.index("@media (max-width: 720px)"):]
    return block[:block.index("\n}\n")]


def _hidden(block: str) -> set:
    """The classes a block of the sheet hides: those of its rules that do nothing else."""
    return {cls for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", block)
            if re.fullmatch(r"\s*display:\s*none\s*", body) for cls in re.findall(r"\.([\w-]+)", selectors)}


def _place(cls: str) -> tuple[float, float]:
    """Where a figure of the scene stands on the wide layout: its left and its width, in % of the phone."""
    found = re.search(r"\." + cls + r" \{ left: (-?[\d.]+)%; width: ([\d.]+)%", CSS)
    return float(found.group(1)), float(found.group(2))


@needs_node
class TestTheDays:
    """24 and 25 December, every year, from midnight to midnight by the visitor's clock."""

    @pytest.mark.parametrize("now", ["2026-12-24T00:00:00", "2026-12-25T23:59:59", "2031-12-24T12:00:00"])
    def test_comes_on_24_and_25_december_every_year(self, now):
        assert run_head(now) == {"classes": ["christmas"], "theme": "dark"}

    @pytest.mark.parametrize("now", ["2026-12-23T23:59:59", "2026-12-26T00:00:00", "2027-01-01T12:00:00",
                                     "2026-11-24T12:00:00"])
    def test_stays_away_on_any_other_day(self, now):
        assert run_head(now) == {"classes": [], "theme": None}

    def test_halloween_is_not_christmas(self):
        assert run_head("2026-10-31T12:00:00")["classes"] == ["halloween"]

    @pytest.mark.parametrize("now, search, day", [
        ("2026-12-24T12:00:00", "?halloween", "halloween"),
        ("2026-10-31T12:00:00", "?christmas", "christmas"),
        ("2026-11-10T12:00:00", "?halloween&christmas", "halloween"),
    ])
    def test_one_day_at_a_time_the_one_asked_for_first(self, now, search, day):
        """Two days at once laid two decorations, two strips' buttons and two games: the address
        names the one previewed, over the date's; of two named, the first in the year."""
        assert run_head(now, search)["classes"] == [day]

    @pytest.mark.parametrize("search", ["?christmas", "?christmas=1", "?lang=en&christmas"])
    def test_shows_itself_on_any_day_for_a_preview(self, search):
        assert run_head("2026-11-10T15:00:00", search)["classes"] == ["christmas"]

    @pytest.mark.parametrize("search", ["?christmasx", "?x=christmas", "?nochristmas"])
    def test_a_lookalike_address_is_no_preview(self, search):
        assert run_head("2026-11-10T15:00:00", search)["classes"] == []

    def test_a_theme_the_visitor_chose_is_kept(self):
        """Dark by default those days: one who chose light with the button keeps light."""
        assert run_head("2026-12-24T20:00:00", saved="light") == {"classes": ["christmas"], "theme": "light"}

    def test_the_day_after_follows_the_saved_theme_as_before(self):
        assert run_head("2026-12-26T09:00:00", saved="light") == {"classes": [], "theme": "light"}


class TestTheLoader:
    """The decoration costs nothing on the other days: no request, no byte."""

    def test_the_page_names_the_decoration_in_a_template_only(self):
        template = re.search(r'<template id="xm-assets" data-day="christmas">(.*?)</template>', PAGE, re.S)
        assert template, "the decoration's template is gone"
        assert re.search(r'href="assets/christmas\.css\?v=[0-9a-f]{10}"', template.group(1))
        assert re.search(r'src="assets/christmas\.js\?v=[0-9a-f]{10}"', template.group(1))
        outside = PAGE.replace(template.group(0), "")
        assert "christmas.css" not in outside and "christmas.js" not in outside, \
            "the decoration is fetched outside its template, so on every day"
        assert "assets/christmas/" not in outside, "a drawing is named in the page, so fetched every day"

    def test_the_loader_waits_for_each_days_class_and_styles_first(self):
        loader = PAGE[PAGE.index('<template id="hw-assets"'):PAGE.index("</body>")]
        assert "querySelectorAll('template[data-day]')" in loader
        assert "classList.contains(template.getAttribute('data-day'))" in loader
        # The script only once the sheet is in: nothing drawn unstyled.
        assert loader.index("sheet.onload") < loader.index("script.src")

    def test_the_drawings_are_asked_for_by_the_script_alone(self):
        """The figures come with the images the script builds that day; the sheet names no file."""
        assert "var FIGURES = 'assets/christmas/';" in JS
        assert not re.search(r"url\((?!#)", CSS), "the sheet fetches a file of its own"


class TestTheDrawings:
    """Every drawing the script names is there, every one there is used, each whole on its own."""

    @staticmethod
    def _named() -> set:
        names = set(re.findall(r"figure\('([a-z-]+)'", JS))
        # The cast down the page, each in turn.
        names |= set(re.findall(r"\['([a-z-]+)', 'xm-(?:rock|sway|bounce)'\]", JS))
        colours = set(re.findall(r"bauble\('[^']*', '([a-z]+)'", JS))
        colours |= set(re.findall(r"'([a-z]+)'", re.search(r"var COLOURS = \[([^\]]*)\]", JS).group(1)))
        names |= {"bauble-" + colour for colour in colours}
        names |= set(re.findall(r"FIGURES\s*\+\s*'([a-z-]+)\.svg", JS))
        return names

    def test_every_drawing_named_is_there(self):
        missing = sorted(name for name in self._named() if not (FIGURES / f"{name}.svg").is_file())
        assert not missing, missing

    def test_every_drawing_there_is_used(self):
        assert {path.stem for path in FIGURES.glob("*.svg")} == self._named()

    @pytest.mark.parametrize("path", sorted(FIGURES.glob("*.svg")), ids=lambda path: path.name)
    def test_each_drawing_stands_alone(self, path):
        """An image's SVG cannot reach the page: every gradient it fills with is its own, it has a
        size of its own to be drawn at, and it asks for nothing else — no script, no sheet, no file."""
        svg = path.read_text(encoding="utf-8")
        assert svg.startswith('<svg xmlns="http://www.w3.org/2000/svg"')
        assert re.search(r'viewBox="-?\d+ -?\d+ \d+ \d+" width="\d+" height="\d+"', svg), "no size of its own"
        defined = set(re.findall(r'id="([^"]+)"', svg))
        used = set(re.findall(r"url\(#([^)]+)\)", svg))
        assert used <= defined, used - defined
        assert "<script" not in svg and "<style" not in svg and "href=" not in svg


class TestTheDecoration:
    """Decoration only: nothing to click, nothing read aloud, nothing that moves at a cost."""

    def test_it_never_takes_a_click(self):
        assert re.search(r"\.xm-decor\s*\{\s*pointer-events:\s*none", CSS)

    def test_it_is_hidden_from_assistive_technology(self):
        """Laid by days.js (lay), which hides what it lays (test_days.py); the shapes too."""
        assert "var lay = agDays.lay.bind(null, 'xm');" in JS
        assert '<svg class="xm-decor" aria-hidden="true"' in JS
        assert re.findall(r'alt="[^"]*"', JS) and set(re.findall(r'alt="[^"]*"', JS)) == {'alt=""'}

    def test_every_motion_has_its_keyframes_and_every_keyframes_a_use(self):
        frames = set(re.findall(r"@keyframes ([\w-]+)", CSS))
        used = {token for value in re.findall(r"animation(?:-name)?:\s*([^;}]+)", CSS)
                for token in re.split(r"[\s,]+", value) if token.startswith("xm-")}
        assert used == frames, (used - frames, frames - used)

    def test_it_animates_only_what_the_browser_composites(self):
        for name, body in re.findall(r"@keyframes ([\w-]+)\s*\{(.*?)\n\}", CSS, re.S):
            assert set(re.findall(r"([a-z-]+)\s*:", body)) <= {"transform", "opacity"}, name

    def test_nothing_asks_for_a_layer_of_its_own(self):
        assert "will-change" not in CSS

    def test_less_motion_means_no_snow_no_sleigh_and_figures_standing_still(self):
        block = _block("@media (prefers-reduced-motion: reduce)")
        gone = block[:block.index("display: none")]
        assert ".xm-sky-top" in gone and ".xm-snow" in gone
        for moving in (".xm-hang", ".xm-star", ".xm-tw", ".xm-bounce", ".xm-rock", ".xm-sway"):
            assert moving in block[block.index("display: none"):], moving

    def test_a_part_out_of_sight_is_not_drawn(self):
        """Every part that carries decoration is watched — the hero, each section, the footer —
        and, scrolled away, loses it: held still, it still cost every frame the page draws."""
        assert "var page = agDays.parts();" in JS
        assert "agDays.rest('xm', page.all);" in JS
        assert re.search(r"^\.xm-paused \.xm-decor \{\s*display:\s*none\s*\}", CSS, re.M)
        bare = re.sub(r"/\*.*?\*/", "", CSS, flags=re.S)
        held = [sel.strip() for sel in re.findall(r"([^{}]+)\{\s*animation-play-state:\s*paused", bare)]
        assert held == [".xm-paused .xm-hidden-gift"], "held still again: see the measures above .xm-paused"

    def test_a_browser_without_container_units_gets_nothing_they_place(self):
        block = _block("@supports not (width: 1cqw)")
        assert ".xm-sky" in block and ".xm-ground" in block and "display: none" in block

    def test_the_controls_and_the_words_beside_the_phone_stay_above_it(self):
        above = min(_z(r"\.christmas \.hero-controls"), _z(r"\.christmas \.hero-caption,\s*\.christmas \.hero-note"))
        for piece in (r"\.xm-sky", r"\.xm-ground", r"\.xm-holly", r"\.xm-cta-patch"):
            assert _z(piece) < above, piece

    def test_the_tab_carries_a_fir_tree(self):
        assert "document.title = String.fromCodePoint(0x1F384) + ' ' + document.title;" in JS

    def test_the_sites_icon_is_left_alone(self):
        """A browser may keep the icon well past the day: the title alone says it."""
        assert not re.search(r"favicon|rel=[\"']?(?:shortcut )?icon|\[rel[*~^]?=[\"']?icon", JS)


class TestTheSnow:
    """Two planes of snow, each a tile repeated across the panel and moved down a tile a turn."""

    @pytest.mark.parametrize("plane, tile", [("xm-near", "snow-near"), ("xm-far", "snow-far")])
    def test_a_turn_moves_the_plane_by_exactly_its_tile(self, plane, tile):
        """Moved by more or less than its tile, the snow would jump back at the end of every turn."""
        rule = re.search(r"\." + plane + r" \{(.*?)\}", CSS, re.S).group(1)
        above = int(re.search(r"top: -(\d+)px", rule).group(1))
        taller = int(re.search(r"height: calc\(100% \+ (\d+)px\)", rule).group(1))
        width, height = map(int, re.search(r"background-size: (\d+)px (\d+)px", rule).groups())
        frames = re.search(r"animation: ([\w-]+)", rule).group(1)
        moved = int(re.search(r"@keyframes " + frames + r" \{.*?to \{ transform: translateY\((\d+)px\) \}",
                              CSS, re.S).group(1))
        drawn = re.search(r'width="(\d+)" height="(\d+)"', (FIGURES / f"{tile}.svg").read_text(encoding="utf-8"))
        assert above == taller == moved == height == int(drawn.group(2))
        assert width == int(drawn.group(1))

    @pytest.mark.parametrize("tile", ["snow-near", "snow-far"])
    def test_no_flake_is_cut_by_its_tiles_edge(self, tile):
        """A flake across the edge would show cut in two where the tiles join."""
        svg = (FIGURES / f"{tile}.svg").read_text(encoding="utf-8")
        width, height = map(int, re.search(r'width="(\d+)" height="(\d+)"', svg).groups())
        flakes = [(float(x), float(y), float(r)) for x, y, r in re.findall(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"', svg)]
        for x, y, rim in re.findall(r'translate\(([\d.]+) ([\d.]+)\)[^>]*><path d="[^"]*" stroke="#7fb2e5" stroke-width="([\d.]+)"', svg):
            scale = float(rim) / 3.4
            flakes.append((float(x), float(y), 5.6 * scale + float(rim) / 2))
        assert len(flakes) >= 5
        for x, y, reach in flakes:
            assert reach <= x <= width - reach and reach <= y <= height - reach, (x, y)


class TestTheScene:
    """At the foot of the phone, beside it, as on the 1440 x 900 mock-up where the phone is 380 wide."""

    @pytest.mark.parametrize("cls", ["xm-tree", "xm-gift", "xm-elf-gift", "xm-snowman"])
    def test_the_left_side_keeps_off_the_phone(self, cls):
        left, width = _place(cls)
        assert left + width <= 0

    @pytest.mark.parametrize("cls", ["xm-elf-wave", "xm-penguin", "xm-bear"])
    def test_the_right_side_keeps_off_the_phone(self, cls):
        assert _place(cls)[0] >= 100

    def test_the_whole_scene_fits_where_its_query_lets_it_out(self):
        """From 650px of panel (its content box, inside 32px of padding) there are 167px beside the phone."""
        assert "@container xm-panel (max-width: 649px)" in CSS
        room = (650 + 64 - 380) / 2 / 380 * 100
        for cls in ("xm-tree", "xm-gift", "xm-elf-gift", "xm-snowman"):
            assert _place(cls)[0] >= -room - 1, cls
        for cls in ("xm-elf-wave", "xm-penguin", "xm-bear"):
            left, width = _place(cls)
            assert left + width <= 100 + room + 1, cls

    def test_the_bank_reaches_both_edges_of_the_widest_panel(self):
        """A 3040px screen: a 1520px panel, 150% of a 380px phone on either side of it."""
        found = re.search(r"\.xm-drift \{[^}]*left: (-[\d.]+)%;\s*width: ([\d.]+)%", CSS)
        left, width = float(found.group(1)), float(found.group(2))
        assert left <= -150 and left + width >= 250

    def test_the_buttons_patch_gives_way_to_the_second_button(self):
        """The elf goes where it would touch the second button, the snowman too below 340px."""
        assert re.search(r"@media \(min-width: 721px\) and \(max-width: 760px\) \{\s*\.xm-c-elf \{\s*display: none", CSS)
        assert re.search(r"@media \(max-width: 374px\) \{\s*\.xm-c-elf \{\s*display: none", CSS)
        assert re.search(r"@media \(max-width: 339px\) \{\s*\.xm-c-snowman \{\s*display: none", CSS)


class TestDownThePage:
    """Snow in the margins beside each section's text, a bauble hung from its top and a figure at its
    foot in one of them; on a phone a bauble in the band above its label."""

    def test_every_section_but_the_proof_is_dressed(self):
        """The figures under "End the jitter" are one band with it: no top, no foot of their own."""
        assert "var sections = page.sections;" in JS
        assert re.search(r"return !section\.classList\.contains\('rt-proof'\);", DAYS_JS)
        for laid in ("'xm-sky xm-sky-margin xm-margin-l', margins[0]", "'xm-sky xm-sky-margin xm-margin-r', margins[1]",
                     "'xm-sky xm-sky-band', bauble("):
            assert "lay(section, " + laid in JS, laid
        assert re.search(r"\.christmas \.hero,\s*\.christmas \.section,\s*\.christmas footer\s*\{\s*position:\s*relative", CSS)

    def test_the_bauble_and_the_figure_share_a_margin_the_other_from_one_section_to_the_next(self):
        """So that a figure at a section's foot never has the next section's bauble at its feet."""
        assert "var side = i % 2;" in JS
        assert "margins[side] += bauble('xm-mhang'" in JS
        assert re.search(r"margins\[side\] \+= '<div class=\"xm-m-mound\">' \+ MOUND", JS)

    def test_no_figure_at_the_foot_of_the_last_section(self):
        """The footer's scene stands there."""
        assert "if (!footer || i < sections.length - 1) {" in JS
        assert JS.index("var footer = page.footer;") < JS.index("sections.forEach(")

    def test_the_margins_are_the_ones_the_page_leaves(self):
        """As wide as the margin beside the text (days.css, --day-margin), gone on a phone, where the
        column's padding is all there is; the band only there."""
        assert re.search(r"^\.xm-sky-margin \{[^}]*width: var\(--day-margin\)", CSS, re.M)
        phone = re.search(r"@media\(max-width:(\d+)px\)\s*\{\s*\.w\s*\{\s*padding: 0 max\((\d+)px", SITE_CSS)
        assert re.search(r"@media \(max-width: %spx\) \{\s*\.xm-sky-margin \{\s*display: none\s*\}\s*"
                         r"\.xm-sky-band \{\s*display: block" % phone.group(1), CSS)
        assert re.search(r"^\.xm-sky-band \{\s*display: none", CSS, re.M)

    def test_the_margins_snow_is_the_near_plane(self):
        """The far plane's small pale flakes hardly showed on a light page."""
        snow = re.search(r"var MARGIN_SNOW = (.*?);\n", JS, re.S).group(1)
        assert "xm-near" in snow and "snow-near.svg" in snow and "xm-far" not in snow

    def test_a_figure_keeps_clear_of_the_text_in_the_narrowest_margin(self):
        """The two paddings, on any screen too narrow for the column to leave more: 18px or more on
        either side of the figure, and of its bauble swung 5deg out on its longest ribbon."""
        _, inner, outer = column()
        narrowest = inner + outer
        fig = _rule("xm-mfig")
        width = float(re.search(r"width: (\d+)px", fig).group(1))
        assert f"left: calc(50% - {width / 2:g}px)" in fig
        assert (narrowest - width) / 2 >= 18
        hang = _rule("xm-mhang")
        bauble = float(re.search(r"width: (\d+)px", hang).group(1))
        assert f"left: calc(50% - {bauble / 2:g}px)" in hang
        longest = max(int(n) for n in re.search(r"var RIBBONS = \[([^\]]*)\]", JS).group(1).split(","))
        import math
        swing = (longest + bauble * _ratio("bauble-red")) * math.sin(math.radians(5))
        assert (narrowest - bauble) / 2 - swing >= 12

    def test_the_bauble_in_the_band_keeps_above_the_label(self):
        """56px of band, inside the 60px a phone's section leaves above its label."""
        band = float(re.search(r"^\.xm-sky-band \{[^}]*height: (\d+)px", CSS, re.M).group(1))
        phone = int(re.search(r"@media\(max-width:720px\)\s*\{\s*(?:/\*(?:(?!\*/).)*\*/\s*)?"
                              r"\.section\s*\{\s*padding:\s*(\d+)px", SITE_CSS, re.S).group(1))
        assert band < phone
        ribbon = float(re.search(r"\.xm-bhang \.xm-ribbon \{ height: (\d+)px", CSS).group(1))
        width = float(_rule("xm-bhang").split("width:")[1].split("px")[0])
        assert ribbon + width * _ratio("bauble-red") <= band - 8


class TestTheLastScene:
    """Figures standing on the footer's top edge, and a last bauble hung from it."""

    def test_it_is_as_wide_as_the_column(self):
        shared = re.search(r"^\.xm-foot,\s*\.xm-sky-foot \{([^}]*)\}", CSS, re.M).group(1)
        assert re.search(r"top: 0;\s*left: var\(--day-margin\);\s*right: var\(--day-margin\)", shared)
        phone = re.search(r"@media\(max-width:(\d+)px\)\s*\{\s*\.w\s*\{\s*padding: 0 max\((\d+)px", SITE_CSS)
        assert re.search(r"\.xm-foot,\s*\.xm-sky-foot \{\s*left: %spx;\s*right: %spx" % (phone.group(2), phone.group(2)),
                         _phone_block())

    @pytest.mark.parametrize("screen", ["wide", "phone"])
    def test_each_figure_fits_the_room_above_the_edge(self, screen):
        """The last section's bottom padding, 100px (60px on a phone), less 8px of air."""
        wide = int(re.search(r"^\.section\s*\{\s*padding:\s*(\d+)px", SITE_CSS, re.M).group(1))
        phone = int(re.search(r"@media\(max-width:720px\)\s*\{\s*(?:/\*(?:(?!\*/).)*\*/\s*)?"
                              r"\.section\s*\{\s*padding:\s*(\d+)px", SITE_CSS, re.S).group(1))
        room = wide if screen == "wide" else phone
        drawings = {"xm-f-tree": "tree", "xm-f-gift2": "gift-green", "xm-f-gift": "gift-red", "xm-f-bear": "bear",
                    "xm-f-snowman": "snowman", "xm-f-elf": "elf-wave"}
        block = CSS if screen == "wide" else _phone_block()
        hidden = _hidden(block) if screen == "phone" else set()
        for cls, name in drawings.items():
            if cls in hidden:
                continue
            rule = _rule(cls, block)
            width = float(re.search(r"width: (\d+)px", rule).group(1))
            bottom = float(re.search(r"bottom: (-?\d+)px", rule).group(1))
            assert bottom <= 0, f"{cls} floats over the edge"
            assert width * _ratio(name) + bottom <= room - 8, f"{cls} ({screen}) stands too tall"

    @pytest.mark.parametrize("screen", ["wide", "phone"])
    def test_its_bauble_keeps_above_the_footers_first_line(self, screen):
        """In the footer's empty top: 64px (48px on a phone), less 8px of air."""
        block = CSS if screen == "wide" else _phone_block()
        sky = 64 if screen == "wide" else 48
        top = re.search(r"footer\s*\{\s*background: var\(--inv\);\s*color: #fff;\s*padding: (\d+)px", SITE_CSS)
        assert int(top.group(1)) == 64
        if screen == "wide":
            assert re.search(r"^\.xm-sky-foot \{\s*height: 64px", CSS, re.M)
        else:
            assert re.search(r"\.xm-sky-foot \{\s*height: 48px", block)
        width = float(re.search(r"width: (\d+)px", _rule("xm-f-hang", block)).group(1))
        ribbon = float(re.search(r"\.xm-f-hang \.xm-ribbon \{ height: (\d+)px", block).group(1))
        assert ribbon + width * _ratio("bauble-gold") <= sky - 8

    def test_the_phone_keeps_the_right_hand_group_alone(self):
        assert _hidden(_phone_block()) == {"xm-f-mound-l", "xm-f-snowman", "xm-f-elf"}



RULES = (ROOT / "hidden-gift.html").read_text(encoding="utf-8")


def _game_call() -> str:
    """The day's call to the game (days.js, game): its prize, its words, its rules."""
    call = JS[JS.index("agDays.game({"):]
    return call[:call.index("\n    });")]


class TestTheHiddenGift:
    """The day's game as Christmas plays it, on 24 December only: a gold gift, its words and its
    rules. The game itself — asking the licence server, hiding the prize, the winner's window — is
    the days', held by test_days.py; the day it runs, the licence server's (GHOST_DAY)."""

    def test_it_is_played_with_christmass_own_prize(self):
        call = _game_call()
        for setting in ("kept: 'ag-hidden-gift'", "badge: 'CHRISTMAS'", "rules: 'hidden-gift.html'",
                        "contact: 'contact@audiogravity.app'", "button: 'xm-hidden-gift'",
                        """figure: '<img src="' + FIGURES + 'gift-gold.svg" alt="" decoding="async">'""",
                        "label: 'A hidden gift: open it to win a lifetime licence'"):
            assert setting in call, setting

    def test_it_hides_in_the_band_clear_of_the_baubles(self):
        """Above every label, 44px to the finger, and between 30% and 70% of the section: clear of
        the baubles hung in the margins and, on a phone, in the band (at 14% and 86%) — 30px or
        more from them on a 390px phone, where at 74% it stood against one."""
        found = re.search(r"return 'calc\(' \+ \((\d+) \+ Math\.random\(\) \* (\d+)\)\.toFixed\(1\) \+ '% - 22px\)';",
                          _game_call())
        low, high = int(found.group(1)), int(found.group(1)) + int(found.group(2))
        baubles = [int(b) for b in re.findall(r"\.xm-b\d \{ left: calc\((\d+)% - 11px\) \}", CSS)]
        assert len(baubles) == 2
        phone = 390
        for bauble in baubles:
            nearest = high if bauble > high else low
            gap = abs(bauble - nearest) / 100 * phone - 22 - 11
            assert gap >= 28, (bauble, gap)
        rule = _rule("xm-hidden-gift")
        band = float(re.search(r"^\.xm-sky-band \{[^}]*height: (\d+)px", CSS, re.M).group(1))
        width = float(re.search(r"width: (\d+)px", rule).group(1))
        assert width == float(re.search(r"height: (\d+)px", rule).group(1)) == 44
        assert float(re.search(r"top: (\d+)px", rule).group(1)) + 44 <= band
        # On the skies' level and laid after the band, so in front of it.
        assert "z-index: 3;" in rule
        assert JS.index("agDays.game({") > JS.index("lay(section, 'xm-sky xm-sky-band'")

    def test_it_stays_for_a_visitor_who_asked_for_less_motion(self):
        """It is the game, not a decoration: still, but there."""
        block = _block("@media (prefers-reduced-motion: reduce)")
        gone = block[:block.index("display: none")]
        assert ".xm-hidden-gift" not in gone
        assert ".xm-hidden-gift" in block[block.index("display: none"):]

    def test_it_is_no_decoration(self):
        """A real button, not in a piece laid hidden: taken off the page with the decoration out of
        sight, it would be a prize no one could ever see again."""
        assert "xm-decor" not in _game_call()
        assert ".xm-paused .xm-hidden-gift" in CSS

    def test_it_stands_out_on_every_ground(self):
        """A control's shape needs 3:1 against its ground: the gold alone has it on the dark page,
        its dark gold ring on the light one; the focus ring on both."""
        svg = (FIGURES / "gift-gold.svg").read_text(encoding="utf-8")
        rings = set(re.findall(r'<rect [^>]*stroke="(#[0-9a-f]{6})"', svg))
        assert len(rings) == 1
        ring = rings.pop()
        body = "#ffcc33"
        assert f'stop-color="{body}"' in svg
        light, dark = grounds()[:2], grounds()[2:]
        for ground in light:
            assert contrast(ring, ground) >= 3, (ring, ground)
        for ground in dark:
            assert contrast(body, ground) >= 3, (body, ground)
        focus = re.search(r"\.xm-hidden-gift:focus-visible \{\s*outline: 2px solid (#[0-9a-f]{6})", CSS).group(1)
        for ground in light + dark:
            assert contrast(focus, ground) >= 3, (focus, ground)

    def test_it_is_unlike_the_decorations_gifts(self):
        """The decoration's presents are red and green; the game's alone is gold."""
        assert JS.count("gift-gold.svg") == 1
        assert re.findall(r"figure\('(gift-[a-z]+)'", JS) and "gift-gold" not in re.findall(r"figure\('(gift-[a-z]+)'", JS)

    def test_the_rules_name_the_organiser_and_say_when_and_how(self):
        for words in ("Alexandre Di Marco", "contact@audiogravity.app", "24 December 2026",
                      "Paris time (UTC+1)", "five gifts", "twenty minutes", "one chance an hour",
                      "can win one licence", "free of charge", "one moment in each fifth",
                      "keeps no list of players or of winners",
                      "logs each request it receives, with the address it came from"):
            assert words in RULES, words

    @pytest.mark.parametrize("city, zone, hours", [
        ("New York", "America/New_York", "in New York on the 24th from midnight to 18:00"),
        ("Tokyo", "Asia/Tokyo", "in Tokyo from 08:00 on the 24th to 08:00 on the 25th"),
    ])
    def test_the_hours_abroad_are_where_the_days_meet(self, city, zone, hours):
        """The game runs on Paris's 24 December; the page shows on the visitor's 24th and 25th.
        A city plays where the two meet: worked out here, not taken from the text."""
        from datetime import datetime, timedelta
        from zoneinfo import ZoneInfo

        paris, there = ZoneInfo("Europe/Paris"), ZoneInfo(zone)
        game = (datetime(2026, 12, 24, tzinfo=paris), datetime(2026, 12, 25, tzinfo=paris))
        shown = (datetime(2026, 12, 24, tzinfo=there), datetime(2026, 12, 26, tzinfo=there))
        start, end = max(game[0], shown[0]).astimezone(there), min(game[1], shown[1]).astimezone(there)
        assert end - start > timedelta(0)

        def when(t):
            return "midnight" if (t.hour, t.minute) == (0, 0) else t.strftime("%H:%M")

        if start.day == end.day or (end.day == start.day + 1 and (end.hour, end.minute) == (0, 0)):
            said = f"in {city} on the {start.day}th from {when(start)} to {when(end)}"
        else:
            said = f"in {city} from {when(start)} on the {start.day}th to {when(end)} on the {end.day}th"
        assert said == hours
        assert hours in " ".join(RULES.split())

    def test_paris_is_where_the_rules_say(self):
        from datetime import datetime
        from zoneinfo import ZoneInfo

        offset = datetime(2026, 12, 24, 12, tzinfo=ZoneInfo("Europe/Paris")).utcoffset().total_seconds() / 3600
        assert f"Paris time (UTC+{offset:g})" in RULES


@needs_node
class TestTheNewsBeforeTheDay:
    """Until Christmas Eve 2026 the announce bar's news, taking turns with the release's sentence,
    says what comes on the 24th (index.html, the script after the bar). By the visitor's clock."""

    @pytest.mark.parametrize("now", ["2026-12-15T09:00:00", "2026-12-23T23:59:59"])
    def test_until_the_day_the_bar_announces_the_gift(self, now):
        """Its short sentence, 29 characters, one more than Halloween's, holds one line on a phone
        from 320px, and the bar is as high with it as with the release's (measured in Chromium and
        WebKit, 320 to 1440px, 2026-11-10)."""
        result = run_announce(now)
        assert result["href"] == "hidden-gift.html"
        assert result["said"] == ["24 DEC", " ", "A gift hides on this page on 24 December: five lifetime licences to win",
                                  "Five lifetime licences to win", " ", "→"]
        assert result["seen"] == ["release"], "the release's sentence comes first"

    def test_it_says_what_the_rules_say(self):
        said = " ".join(run_announce("2026-12-15T09:00:00")["said"])
        assert "24 December" in said and "five" in said.lower()
        assert "five gifts" in RULES and "24 December 2026" in RULES
