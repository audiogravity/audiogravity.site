"""Guards for what the days the landing dresses up share (assets/days.js, assets/days.css).

Halloween and Christmas lay their decoration and rest it out of sight through the same code, both
make the strip that shows a track playing play the day's own record, with a button that plays an
excerpt of it — Danse macabre on 31 October, the Nutcracker on 24 and 25 December — and both play
the same game, a lifetime licence hidden down the page: an orange ghost, a gift. The mechanism is
held once here, and each day's part of it (its record, its game's words) for both days. The
announce bar the game writes in, with the release's sentence, is the page's own, held here too.

Run with ``python3 -m pytest scripts/`` from the repository root.
"""
import re

import pytest

from landing_days import PAGE, ROOT, announce_script, column, needs_node, px, run_announce, webp_size

DAYS_JS = (ROOT / "assets" / "days.js").read_text(encoding="utf-8")
DAYS_CSS = (ROOT / "assets" / "days.css").read_text(encoding="utf-8")
SITE_CSS = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")
DAYS = {"halloween": "hw", "christmas": "xm"}
STRIP = DAYS_JS[DAYS_JS.index("function strip(record)"):DAYS_JS.index("function listen(progress, record)")]
LISTEN = DAYS_JS[DAYS_JS.index("function listen(progress, record)"):DAYS_JS.index("// THE GAME")]

# Titles measured not to take more lines than the usual one at any width (Chromium, 320 to 1440px):
# "Danse macabre" (2026-10-25), "The Nutcracker" (2026-11-10, where "Sugar Plum Fairy" took a second
# line at 360px and the usual title one). A new title is measured, then named here.
FITTING_TITLES = {"Danse macabre", "The Nutcracker"}


def _script(day: str) -> str:
    """A day's own script."""
    return (ROOT / "assets" / f"{day}.js").read_text(encoding="utf-8")


def _sheet(day: str) -> str:
    """A day's own sheet."""
    return (ROOT / "assets" / f"{day}.css").read_text(encoding="utf-8")


def _record(day: str) -> dict:
    """The day's record, as its script hands it to the strip (agDays.strip)."""
    block = re.search(r"agDays\.strip\(\{(.*?)\}\);", _script(day), re.S).group(1)
    record = dict(re.findall(r"(\w+): '([^']*)'", block))
    record["heard"] = re.findall(r"'([^']*)'", re.search(r"heard: \[(.*?)\]", block).group(1))
    return record


def _strip_page() -> str:
    """The strip in the page, as it shows on any other day."""
    return re.search(r'<section class="np-strip">(.*?)</section>', PAGE, re.S).group(1)


class TestTheLoader:
    """Each day's template asks for the shared sheet and script first, then its own."""

    @pytest.mark.parametrize("day", DAYS)
    def test_the_shared_files_come_first(self, day):
        template = re.search(r'<template id="[\w-]+" data-day="%s">(.*?)</template>' % day, PAGE, re.S).group(1)
        sheets = re.findall(r'href="assets/([\w.-]+)\?v=[0-9a-f]{10}"', template)
        scripts = re.findall(r'src="assets/([\w.-]+)\?v=[0-9a-f]{10}"', template)
        assert sheets == ["days.css", f"{day}.css"] and scripts == ["days.js", f"{day}.js"]

    def test_the_shared_files_are_asked_for_in_the_templates_alone(self):
        outside = re.sub(r'<template id="[\w-]+" data-day="\w+">.*?</template>', "", PAGE, flags=re.S)
        assert not re.search(r'(?:src|href)="assets/days\.(?:js|css)', outside), "fetched on every day"

    def test_the_loader_waits_for_every_sheet_and_keeps_the_scripts_in_order(self):
        loader = PAGE[PAGE.index('<template id="hw-assets"'):PAGE.index("</body>")]
        assert "if (--waiting) return;" in loader, "a script could run before a sheet is in"
        assert "script.async = false;" in loader, "the day's script could run before days.js"
        assert loader.index("sheet.onload") < loader.index("script.src")


class TestLayingAndResting:
    """One way to lay a piece of decoration and one to rest it, both days."""

    def test_what_is_laid_is_hidden_from_assistive_technology(self):
        assert """'<div class="' + prefix + '-decor ' + classes + '" aria-hidden="true">' + inner + '</div>'""" in DAYS_JS
        assert DAYS_JS.count("insertAdjacentHTML") == 1

    @pytest.mark.parametrize("day", DAYS)
    def test_each_day_finds_the_page_through_it(self, day):
        """The parts of the page a day dresses are found once, in days.js (parts): a day that
        looked for them itself would drift from the other when the page changes."""
        js = _script(day)
        assert "var page = agDays.parts();" in js and "page.all" in js
        for lookup in ("querySelector('.hero')", "querySelectorAll('.section')", "querySelector('footer')", "rt-proof"):
            assert lookup not in js, lookup
        assert "return !section.classList.contains('rt-proof');" in DAYS_JS
        assert "all: [hero].concat(sections, footer ? [footer] : [])" in DAYS_JS

    @pytest.mark.parametrize("day, prefix", DAYS.items())
    def test_each_day_lays_through_it(self, day, prefix):
        js = _script(day)
        assert f"var lay = agDays.lay.bind(null, '{prefix}');" in js
        assert js.count("insertAdjacentHTML") == 1, "something is laid outside lay() and the day's shapes"
        assert re.search(r"\.%s-decor\s*\{\s*pointer-events:\s*none" % prefix, _sheet(day))

    def test_a_part_rests_while_out_of_sight(self):
        assert "entry.target.classList.toggle(prefix + '-paused', !entry.isIntersecting);" in DAYS_JS
        # Taken taller at both ends: a part scrolled back up to comes in at the top of the screen,
        # and the observer answers a frame late — Christmas's figures appeared in sight.
        assert "rootMargin: '120px 0px 120px 0px'" in DAYS_JS

    @pytest.mark.parametrize("day, prefix", DAYS.items())
    def test_each_day_rests_its_parts(self, day, prefix):
        """Its sheet says what resting is: Halloween holds its decoration still, Christmas takes it
        off the page (christmas.css, where the measures are)."""
        assert re.search(r"agDays\.rest\('%s', " % prefix, _script(day))
        assert re.search(r"\.%s-paused \.%s-decor,?[^{]*\{\s*(?:animation-play-state:\s*paused|display:\s*none)"
                         % (prefix, prefix), _sheet(day))


class TestTheMargin:
    """The margin beside the text column down the page, where both days lay a section's margins
    and the ends of the last scene on the footer's edge: worked out once, from the page's own
    paddings and widths."""

    def test_it_is_the_one_the_page_leaves(self):
        """The section's padding, the column's width and its own padding (style.css, .section and .w)."""
        width, inner, outer = column()
        assert "--day-margin: calc((100%% - min(100%% - %dpx, %dpx)) / 2 + %dpx)" % (2 * outer, width, inner) in DAYS_CSS

    def test_it_is_worked_out_in_one_place(self):
        sheets = DAYS_CSS + "".join(_sheet(day) for day in DAYS)
        assert sheets.count("min(100% -") == 1, "the margin is worked out in more than one place"
        assert "--hw-margin" not in sheets and "--xm-margin" not in sheets

    @pytest.mark.parametrize("day, prefix", DAYS.items())
    def test_each_day_lays_its_margins_and_its_last_scene_in_it(self, day, prefix):
        sheet = _sheet(day)
        assert re.search(r"^\.%s-sky-margin \{[^}]*width: var\(--day-margin\)" % prefix, sheet, re.M)
        assert re.search(r"^\.%s-foot,\s*\.%s-sky-foot \{[^}]*left: var\(--day-margin\);\s*right: var\(--day-margin\)"
                         % (prefix, prefix), sheet, re.M)


class TestTheStrip:
    """The strip plays the day's record, and a button in it an excerpt: the mechanism."""

    def test_what_it_changes_is_on_the_page(self):
        """A class renamed in the page would leave the usual track in place, and say nothing."""
        strip = _strip_page()
        for cls in re.findall(r"(?:shown|progress)\.querySelector\('\.([\w-]+)'\)", STRIP):
            assert re.search(r'class="(?:[^"]* )?%s[ "]' % re.escape(cls), strip), cls
        times = re.findall(r"<span>([^<]*)</span>",
                           re.search(r'<div class="np-progress"[^>]*>(.*?)</div>', strip, re.S).group(1))
        assert len(times) == 2 and re.fullmatch(r"\d+:\d\d", times[0])
        # The time left keeps its minus sign: only its figures are replaced.
        assert re.search(r"\d+:\d\d", times[1]) and not times[1][0].isdigit()

    def test_it_can_play_an_excerpt_at_a_press_only(self):
        """Asked for at the first press, never by the page: a browser plays no sound before the
        visitor has pressed something, and a file nobody plays costs nothing."""
        assert LISTEN.count("new Audio(") == 1 and "new Audio(record.excerpt)" in LISTEN
        assert LISTEN.count("fresh()") == 1
        assert LISTEN.index("sound = fresh();") > LISTEN.index("button.addEventListener('click'"), "fetched before a press"

    def test_while_the_excerpt_plays_the_strip_shows_what_is_heard(self):
        """The excerpt's own format and its own time, by the sound's own clock (no timer of the
        page's); paused, over or failed, the box's again, as the strip stood. An audiophile reading
        DSD256 over a browser's AAC preview would be right to feel misled."""
        cells = re.findall(r'<div class="cell[^"]*"><span>([^<]+)</span>', PAGE)
        assert cells == ["Format", "Sample", "Bitrate", "Codec"], "the strip's cells moved: see heard"
        assert "b.textContent = element ? record.heard[i] : box.values[i];" in LISTEN
        assert "if (!element.paused) show(element.currentTime, element.duration || 30);" in LISTEN
        assert "show(element.currentTime, element.duration || 30);\n                return;" in LISTEN
        pause = LISTEN[LISTEN.index("element.addEventListener('pause'"):]
        error = LISTEN[LISTEN.index("element.addEventListener('error'"):]
        assert "hearing(null);" in pause[:pause.index("});")] and "hearing(null);" in error[:error.index("});")]
        assert not re.search(r"setInterval|setTimeout|requestAnimationFrame", LISTEN)
        assert "progress.setAttribute('aria-label', clock(s) + ' played, ' + clock(total - s) + ' left')" in LISTEN

    def test_a_failed_load_does_not_silence_the_button(self):
        """A failed element stays failed: the next press must start from a new one."""
        error = LISTEN[LISTEN.index("element.addEventListener('error'"):]
        assert "if (sound === element) sound = null;" in error[:error.index("});")]
        assert "if (!sound) sound = fresh();" in LISTEN

    def test_its_button_sits_beside_the_time_without_moving_the_page(self):
        """Not in the progress row, which assistive technology reads as an image whose content is
        not read; and no taller than the time's 16px row (measured in Chromium), so that nothing
        under the strip moves when it is put in."""
        assert re.search(r'<div class="np-progress" role="img"', PAGE)
        assert "row.appendChild(button);\n        row.appendChild(progress);" in LISTEN
        assert "progress.insertBefore(button" not in LISTEN and "progress.appendChild(button" not in LISTEN
        button = re.search(r"^\.day-np-play \{([^}]*)\}", DAYS_CSS, re.M).group(1)
        margin = float(re.search(r"margin: (-[\d.]+)px 0;", button).group(1))
        assert px(button, "height") + 2 * margin <= 16
        gap = int(re.search(r"^\.np-visual \{[^}]*gap: (\d+)px", SITE_CSS, re.M).group(1))
        assert -margin < gap, "the button would reach the cells above or the line below"

    def test_its_button_is_a_real_button_with_the_carousels_icons(self):
        """Named for what a press will do, reached by the keyboard, and wearing the carousel's
        play and pause icons, copied from it rather than drawn a second time."""
        assert "button.type = 'button';" in LISTEN
        assert "playing ? 'Pause the excerpt' : 'Play an excerpt'" in LISTEN
        assert "document.querySelector('#heroPlay .ic-play')" in LISTEN and "cloneNode(true)" in LISTEN
        hero = re.search(r'<button class="hero-ctrl" id="heroPlay"[^>]*>(.*?)</button>', PAGE, re.S).group(1)
        assert 'class="ic-play"' in hero and 'class="ic-pause"' in hero
        assert re.search(r"^\.day-np-play:focus-visible \{", DAYS_CSS, re.M)

    @pytest.mark.parametrize("day", DAYS)
    def test_each_day_colours_its_button(self, day):
        """The shared sheet takes the day's colours: each day gives all three."""
        rules = "".join(re.findall(r"^\.%s \{([^}]*)\}" % day, _sheet(day), re.M))
        for name in ("--day-np-bg", "--day-np-ink", "--day-np-ring"):
            assert name + ":" in rules, f"{day}: {name}"


@pytest.mark.parametrize("day", DAYS)
class TestTheRecord:
    """Each day's record: there, true to its excerpt, and no wider than the usual track."""

    def test_its_cover_is_there_at_the_strips_size(self, day):
        img = re.search(r'<img class="np-cover" src="[^"]+" width="(\d+)" height="(\d+)"', PAGE)
        assert webp_size(ROOT / _record(day)["cover"]) == (int(img.group(1)), int(img.group(2)))

    def test_its_excerpt_is_there_and_named_by_the_day_alone(self, day):
        src = _record(day)["excerpt"]
        audio = ROOT / src
        assert audio.is_file(), f"{src} is missing"
        assert audio.read_bytes()[4:8] == b"ftyp", f"{src} is not an MP4 audio file"
        assert audio.stat().st_size < 1_500_000, f"{src} weighs {audio.stat().st_size} bytes"
        assert src not in PAGE and _script(day).count(src) == 1, "the excerpt is named outside the press"

    def test_what_the_strip_says_while_it_plays_is_the_excerpts_own(self, day):
        record = _record(day)
        audio = (ROOT / record["excerpt"]).read_bytes()
        mp4a = audio.index(b"mp4a")
        rate = int.from_bytes(audio[mp4a + 28:mp4a + 32], "big") >> 16
        mvhd = audio.index(b"mvhd")
        if audio[mvhd + 4] == 0:
            scale, length = (int.from_bytes(audio[mvhd + i:mvhd + i + 4], "big") for i in (16, 20))
        else:
            scale = int.from_bytes(audio[mvhd + 24:mvhd + 28], "big")
            length = int.from_bytes(audio[mvhd + 28:mvhd + 36], "big")
        kbps = len(audio) * 8 / (length / scale) / 1000
        heard = record["heard"]
        assert heard[0] == heard[3] == "AAC"
        assert heard[1] == f"{rate / 1000:g}kHz"
        assert abs(int(heard[2].removesuffix("kbps")) - kbps) / kbps < .02

    def test_the_cover_is_named_as_the_title_is_written(self, day):
        """One work, one spelling, in the image's name as in the strip."""
        record = _record(day)
        assert record["title"] in record["alt"]

    def test_its_lines_take_no_more_room_than_the_usual_ones(self, day):
        """A longer line can take one more on a phone: "Saint-Saëns — Charles Dutoit" took two at
        390px where "The Beatles — Abbey Road" takes one (measured in Chromium, 2026-10-25). The
        artist's line is held to the usual one's characters; the title to the measured ones."""
        record = _record(day)
        usual = re.search(r'<div class="track-artist">([^<]*)</div>', _strip_page()).group(1)
        assert len(record["artist"]) <= len(usual), f"{record['artist']!r} is longer than {usual!r}"
        assert record["title"] in FITTING_TITLES, f"{record['title']!r} was never measured"

    def test_the_time_and_the_bar_agree(self, day):
        """What the label says, what the strip writes and how full the bar is: one moment of the
        recording, whose length the day's script gives."""
        record = _record(day)
        total = re.search(r"(\d+):(\d\d) in all", _script(day)).groups()
        played = [int(n) for n in record["played"].split(":")]
        left = [int(n) for n in record["left"].split(":")]
        played, left = played[0] * 60 + played[1], left[0] * 60 + left[1]
        assert played + left == int(total[0]) * 60 + int(total[1])
        assert abs(float(record["fill"].rstrip("%")) - 100 * played / (played + left)) < 0.1


GAME = DAYS_JS[DAYS_JS.index("function game(day)"):]
RULES_PAGES = {"halloween": ROOT / "orange-ghost.html", "christmas": ROOT / "hidden-gift.html"}
RULES_CSS = (ROOT / "assets" / "rules.css").read_text(encoding="utf-8")


def _game_call(day: str) -> str:
    """A day's call to the game: its prize, its words, its rules."""
    js = _script(day)
    call = js[js.index("agDays.game({"):]
    return call[:call.index("\n    });")]


class TestTheGame:
    """A lifetime licence hidden down the page (days.js, game). The licence server decides
    everything (audiogravity.lic, routers/ghost.py): the page asks it once a visit, shows what it
    answers, and cannot make a prize appear nor know a key before it is given."""

    def test_the_site_asks_the_licence_server_once_a_visit(self):
        assert re.search(r"location\.hostname === 'audiogravity\.app'\s*\?\s*"
                         r"'https://lic\.audiogravity\.app:8443/ls/portal/'", DAYS_JS)
        assert GAME.count("ask('ghost-draw')") == 1
        assert len(re.findall(r"^\s*hunt\(\);$", GAME, re.M)) == 1, "the game is asked for more than once"
        assert GAME.count("ask('ghost-claim'") == 1
        # Bounded: a server that does not answer leaves the page as it is.
        assert "AbortSignal.timeout(8000)" in GAME

    @pytest.mark.parametrize("day", DAYS)
    def test_each_day_plays_it_once_its_sections_are_laid(self, day):
        """Once its sections carry their decoration, so that the prize, laid after, stands in
        front of it; before the parts rest, which leaves the prize alone (it is no decoration)."""
        js = _script(day)
        assert js.count("agDays.game({") == 1
        assert js.index("sections.forEach(") < js.index("agDays.game({") < js.index("agDays.rest(")

    @pytest.mark.parametrize("day", DAYS)
    def test_each_day_says_every_word_the_game_says(self, day):
        """A word or a setting missing would show "undefined" in the banner or in a window."""
        call = _game_call(day)
        read = set(re.findall(r"\bwords\.(\w+)", GAME))
        given = set(re.findall(r"^\s{12}(\w+): '", call, re.M))
        assert read == given, (read - given, given - read)
        settings = set(re.findall(r"\bday\.(\w+)", GAME)) - {"words"}
        named = set(re.findall(r"^\s{8}(\w+):", call, re.M)) - {"words"}
        assert settings == named, (settings - named, named - settings)

    def test_nothing_the_server_says_is_written_as_markup(self):
        """The key and the counts go in as text; the only markup is the page's own words."""
        for value in re.findall(r"innerHTML\s*=\s*([^;]+);", DAYS_JS):
            assert "answer" not in value and "mine" not in value and "data" not in value, value
        assert "dialog.querySelector('code').textContent = mine.key" in GAME
        bar = announce_script()
        assert "sentence.textContent = item.sentence;" in bar and "short.textContent = item.short;" in bar
        # A key is shown, or kept, only in its own shape.
        assert "var KEY = /^AG(-[A-Z0-9]{4}){4}$/;" in DAYS_JS
        assert "KEY.test(mine.key || '')" in GAME and "KEY.test(mine.key)" in GAME

    def test_the_prize_is_a_real_button_outside_the_hidden_decoration(self):
        """In a section of its own, not in a piece laid with aria-hidden and deaf to the pointer."""
        assert "var button = document.createElement('button');" in GAME
        assert "button.className = day.button;" in GAME
        assert "section.appendChild(button);" in GAME
        assert "button.setAttribute('aria-label', day.label);" in GAME

    def test_it_goes_when_its_ticket_lapses(self):
        """After the seconds the server gave, counted from now: the visitor's clock may be wrong
        by any amount. Unless a claim got no answer — the server may have given the key, and the
        same ticket gives it again: the prize then stays, to be taken again."""
        assert "}, Math.max(0, +ghost.ttl || 0) * 1000);" in GAME
        assert "Date.parse" not in DAYS_JS
        claim = GAME[GAME.index("ask('ghost-claim'"):GAME.index("function kept()")]
        answered, unanswered = claim.split("}, function () {")
        assert "clearTimeout(lapse);" in answered and "button.remove();" in answered
        assert "clearTimeout(lapse);" in unanswered and "button.remove();" not in unanswered

    def test_a_key_taken_is_kept_on_this_device_for_this_year_under_each_days_name(self):
        """A name per day: under one, a winner of one day's game could not play the other's."""
        assert "localStorage.setItem(day.kept, JSON.stringify(mine));" in GAME
        assert "mine.year === new Date().getFullYear()" in GAME
        kept = {re.search(r"kept: '([\w-]+)'", _game_call(day)).group(1) for day in DAYS}
        assert len(kept) == len(DAYS)

    def test_the_banner_and_the_window_lead_to_the_days_rules(self):
        assert ("window.agAnnounce({ badge: day.badge, sentence: sentence, short: short, "
                "href: day.rules, open: open });") in GAME
        assert """'<p class="day-catch-note"><a href="' + day.rules + '">The rules</a> · '""" in GAME

    @pytest.mark.parametrize("day", DAYS)
    def test_each_days_rules_exist_and_give_its_address(self, day):
        call = _game_call(day)
        rules = re.search(r"rules: '([\w.-]+)'", call).group(1)
        contact = re.search(r"contact: '([\w.@-]+)'", call).group(1)
        assert RULES_PAGES[day].name == rules and RULES_PAGES[day].is_file()
        assert f'<a href="mailto:{contact}">{contact}</a>' in RULES_PAGES[day].read_text(encoding="utf-8")

    def test_the_steps_to_activate_are_the_manuals(self):
        """The window and the rules name the app's own buttons: if the manual renames one, so must
        they."""
        manual = (ROOT / "docs" / "manual" / "07-administration.md").read_text(encoding="utf-8")
        for label in ("LICENSE KEY", "CHECK KEY", "ACTIVATE THIS MACHINE"):
            assert label in manual and label in GAME, label
            for page in RULES_PAGES.values():
                assert label in page.read_text(encoding="utf-8"), (label, page.name)

    def test_the_brand_is_written_as_the_site_writes_it(self):
        assert "Your lifetime Audiogravi<sup>ty</sup> licence" in GAME
        for page in RULES_PAGES.values():
            html = page.read_text(encoding="utf-8")
            body = html[html.index("<body>"):]
            assert "Audiogravi<sup>ty</sup>" in body and not re.search(r"Audiogravity(?!\.app)", body), page.name

    def test_its_window_is_centred_and_its_links_look_like_links(self):
        """The page's reset takes away the margin a browser centres a modal window with, and its
        links lose their underline: both are given back (measured: the window stood in the top
        left corner, in Chromium and in WebKit)."""
        assert re.search(r"^\* \{\s*margin: 0", SITE_CSS, re.M), "the reset moved: see .day-catch"
        assert re.search(r"^\.day-catch \{\s*margin: auto;", DAYS_CSS, re.M)
        assert re.search(r"^\.day-catch a \{[^}]*text-decoration: underline", DAYS_CSS, re.M)
        assert re.search(r"^\.rules a \{[^}]*text-decoration: underline", RULES_CSS, re.M)

    @pytest.mark.parametrize("day", DAYS)
    def test_the_rules_pages_share_their_look_and_stay_out_of_search(self, day):
        html = RULES_PAGES[day].read_text(encoding="utf-8")
        assert re.search(r'<link rel="stylesheet" href="assets/rules\.css\?v=[0-9a-f]{10}">', html)
        assert "<style>" not in html, "a rules page styles itself again: see assets/rules.css"
        assert '<meta name="robots" content="noindex">' in html

    def test_a_browser_without_dialog_still_shows_the_key(self):
        """Safari before 15.4 has no <dialog>: it is told the key in a plain message instead."""
        body = GAME[GAME.index("function windowOf("):GAME.index("function reveal(")]
        assert "if (typeof dialog.showModal !== 'function') {\n                window.alert(plain);" in body
        plain = GAME[GAME.index("function reveal("):GAME.index("function tell(")]
        assert "words.won + ' Your lifetime Audiogravity licence key:\\n\\n' + mine.key" in plain
        assert "ACTIVATE THIS MACHINE" in plain.split("function (dialog)")[1]

    def test_the_game_writes_the_bar_with_the_pages_writer(self):
        """One writer of the bar, in the page: the game calls it, it does not write its own."""
        assert "window.agAnnounce = function (item) {" in announce_script()
        assert "createElement('span')" not in GAME[GAME.index("function announce("):GAME.index("function haunt(")]
        for js in [DAYS_JS] + [_script(day) for day in DAYS]:
            assert ".announce-bar" not in js and ".announce-news" not in js

    @pytest.mark.parametrize("day", DAYS)
    def test_a_phone_reads_the_point_of_each_announcement(self, day):
        """A phone's bar holds one line, which cut a long sentence before its point ("31 OCT An
        orange ghost haunts this ...", measured at 390px): each says it shorter there."""
        shorts = re.findall(r"\w+Short: '([^']+)'", _game_call(day))
        assert len(shorts) == 3
        assert all(len(t) <= 28 for t in shorts), shorts


@needs_node
class TestTheAnnouncement:
    """The announce bar's news takes turns with the release's sentence (index.html, the script
    right after the bar): before a game's day it says what comes, that day the day's game words it
    (days.js, game), and without news the release's sentence stays alone. By the visitor's clock,
    as the day is."""

    BEFORE = "2026-12-20T09:00:00"

    def test_the_news_has_a_link_of_its_own_in_the_bar(self):
        """The release's sentence keeps its link, the release script's to write; the news has one
        beside it, hidden until there is news, so that a day without any shows the bar as it was."""
        bar = PAGE[PAGE.index('<div class="announce-bar">'):]
        bar = bar[:bar.index("</div>")]
        assert bar.count("<a") == 2 and bar.rstrip().endswith('<a class="announce-news" hidden></a>')
        assert PAGE.index('<a class="announce-news" hidden></a>') < PAGE.index("window.agAnnounce = function")

    @pytest.mark.parametrize("now", ["2026-12-24T00:00:00", "2026-12-26T08:00:00", "2027-12-20T12:00:00"])
    def test_without_news_the_release_is_alone(self, now):
        """Without news nothing turns, not even once the pointer or the keyboard has been in the bar
        and left it — the turn would bring an empty link: the bar is the release's, as on any day."""
        steps = (60000, "mouseenter", "mouseleave", "focusin", "focusout", 60000)
        assert run_announce(now, steps) == {"seen": ["release"] * 7, "href": "", "said": None,
                                            "wrote": [], "reads": []}

    def test_the_release_and_the_news_take_turns_six_seconds_each(self):
        seen = run_announce(self.BEFORE, (5999, 1, 179, 1, 5999, 1, 180))["seen"]
        assert seen == ["release", "release", "fading", "fading", "news", "news", "fading", "release"]

    @pytest.mark.parametrize("enter, leave", [("mouseenter", "mouseleave"), ("focusin", "focusout")])
    def test_no_turn_while_the_bar_is_read(self, enter, leave):
        """Under the pointer or with the keyboard in it the bar holds still (WCAG 2.2.2); the next
        turn comes six seconds after they leave, not at once."""
        seen = run_announce(self.BEFORE, (3000, enter, 60000, leave, 5999, 1, 180))["seen"]
        assert seen == ["release", "release", "release", "release", "release", "release", "fading", "news"]

    def test_the_turn_waits_for_the_links_own_fade(self):
        """The links change places once the fade the style sheet gives them is over, however long."""
        seen = run_announce(self.BEFORE, (6000, 499, 1), fade="0.5s")["seen"]
        assert seen == ["release", "fading", "fading", "news"]

    def test_the_link_shown_fades_in(self):
        """Just shown, a link has no opacity yet for the fade to start from: its style is read while
        the bar is still faded out, or it would appear at once instead of fading in."""
        reads = run_announce(self.BEFORE, (6180, 6180))["reads"]
        assert reads == [["news", True, False], ["release", True, False]]

    def test_the_releases_words_are_never_written(self):
        """Over rounds of turns, the release's link is only ever shown and hidden."""
        assert set(run_announce(self.BEFORE, (6180, 6180, 6180))["wrote"]) == {"hidden"}

    def test_a_link_off_its_turn_is_not_drawn(self):
        """`hidden` alone loses to the links' own display (style.css): a rule gives it back. The
        fade is the links' opacity transition, the one the script reads."""
        assert re.search(r"^\.announce-bar a\[hidden\] \{\s*display: none\s*\}", SITE_CSS, re.M)
        assert re.search(r"^\.announce-bar\.announce-turning a \{\s*opacity: 0\s*\}", SITE_CSS, re.M)
        link = re.search(r"^\.announce-bar a \{([^}]*)\}", SITE_CSS, re.M).group(1)
        assert "transition: opacity var(--ease);" in link

    def test_a_phone_shows_the_short_sentence(self):
        """A phone's bar holds one line: there the short sentence replaces the long one."""
        base = SITE_CSS.index(".announce-short {\n    display: none\n}")
        phone = re.search(r"@media\(max-width:720px\) \{.*?\n\}", SITE_CSS[SITE_CSS.index(".announce-bar {"):], re.S)
        assert re.search(r"\.announce-long \{\s*display: none", phone.group(0))
        assert re.search(r"\.announce-short \{\s*display: inline", phone.group(0))
        assert base < SITE_CSS.index(phone.group(0)), "the base rule comes after the phone's and wins"
