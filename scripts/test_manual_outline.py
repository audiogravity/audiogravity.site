"""Tests for assets/manual-outline.js: the part it marks, the sidebar it scrolls, the menu it folds.

The script runs under Node on a stand-in for a page, as the landing's scripts do in
test_halloween.py: headings at given heights in the page, the sidebar's entries at given offsets
in it, a scroll position each step moves. Skipped where Node is not installed.

The marks were only checked by reading the script's text until the review of 2026-11-01, which
also found, measured in Chromium, the mark leaving the sidebar from the 25th of a chapter's 33
parts: the sidebar now follows it, and that is held here too.

Run with ``python3 -m pytest scripts/test_manual_outline.py`` from the repository root.
"""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = (Path(__file__).resolve().parent.parent / "assets" / "manual-outline.js").read_text(encoding="utf-8")

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="Node is not installed")

#: The page the script runs on. The top bar ends 52px down, so with a window 852px tall a heading
#: counts as passed once its top is 252px from the top of the window or less.
HARNESS = r"""
const cfg = %(cfg)s;
let scrollY = cfg.scrollY;
const listeners = {};
let frames = [];
globalThis.window = globalThis;
Object.defineProperty(globalThis, 'scrollY', { get: () => scrollY });
globalThis.innerHeight = cfg.innerHeight;
globalThis.Node = { DOCUMENT_POSITION_FOLLOWING: 4 };
globalThis.addEventListener = (type, fn) => { listeners[type] = fn; };
globalThis.requestAnimationFrame = (fn) => { frames.push(fn); };
const flush = () => { const run = frames; frames = []; run.forEach((fn) => fn()); };

const headings = {};
cfg.headings.forEach(([id, top], index) => {
    headings[id] = {
        index,
        getBoundingClientRect: () => ({ top: top - scrollY }),
        compareDocumentPosition(other) { return other.index > this.index ? 4 : 2; },
    };
});

const makeLink = (id, inSide, offsetTop) => {
    const classes = new Set();
    const attrs = { href: '#' + id };
    return {
        id, inSide, offsetTop, offsetHeight: 20,
        getAttribute: (k) => (k in attrs ? attrs[k] : null),
        setAttribute: (k, v) => { attrs[k] = String(v); },
        removeAttribute: (k) => { delete attrs[k]; },
        classList: { toggle: (c, on) => { if (on) classes.add(c); else classes.delete(c); } },
        marked: () => classes.has('is-current') && attrs['aria-current'] === 'true',
        tidy: () => !classes.has('is-current') && !('aria-current' in attrs),
    };
};
const sideLinks = cfg.headings.map(([id], i) => makeLink(id, true, cfg.outlineTop + 20 * i));
const menuLinks = cfg.headings.map(([id]) => makeLink(id, false, 0));
const named = (name) => ({ contains: (c) => c === name });
const group = { classList: named('man-nav-group'), offsetTop: cfg.entryTop - 30 };
const outline = { classList: named('man-outline'), offsetTop: cfg.outlineTop, offsetHeight: 20 * cfg.headings.length };
const entry = { offsetTop: cfg.entryTop, offsetHeight: 40, nextElementSibling: outline,
                previousElementSibling: cfg.groupAbove ? group : null };
const side = {
    scrollTop: 0, clientHeight: cfg.sideHeight, scrollHeight: cfg.sideScrollHeight,
    contains: (el) => !!el.inSide,
    querySelector: (s) => (s === '.man-nav-item.active' ? entry : null),
};
const menu = { open: true, addEventListener: (type, fn) => { menu.onclick = fn; } };
const bar = { getBoundingClientRect: () => ({ bottom: 52 }) };
globalThis.document = {
    documentElement: { scrollHeight: cfg.pageHeight },
    getElementById: (id) => headings[id] || null,
    querySelectorAll: (s) => (s === '.man-outline a[href^="#"]' ? [...sideLinks, ...menuLinks] : []),
    querySelector: (s) => ({ '.man-top': bar, '.man-shell > .man-nav': side, '.man-outline-menu': menu })[s] || null,
};

%(script)s

const state = () => ({
    marked: sideLinks.filter((l) => l.marked()).map((l) => l.id),
    menuMarked: menuLinks.filter((l) => l.marked()).map((l) => l.id),
    othersTidy: [...sideLinks, ...menuLinks].filter((l) => !l.marked()).every((l) => l.tidy()),
    sideTop: side.scrollTop,
    menuOpen: menu.open,
});
const seen = [state()];
for (const step of cfg.steps) {
    if ('scroll' in step) { scrollY = step.scroll; listeners.scroll(); flush(); }
    if ('click' in step) {
        menu.onclick({ target: { closest: (s) => (s === 'a' && step.click === 'link' ? {} : null) } });
    }
    seen.push(state());
}
console.log(JSON.stringify(seen));
"""


def run(**overrides) -> list[dict]:
    """Run the script on the stand-in page, then each step, and read the page after each.

    Args:
        **overrides: Settings of the page, over a four-part page whose entry sits far down a
            sidebar taller than the screen: ``headings`` (id, height in the page), ``steps``
            ({"scroll": y} or {"click": "link" | "summary"}), and the sizes below.

    Returns:
        The page as the script left it at load, then after each step: the parts marked in the
        sidebar and in the phone's menu, whether every other link is unmarked, the sidebar's
        scroll, and whether the phone's menu is open.
    """
    cfg = {"innerHeight": 852, "pageHeight": 5000, "scrollY": 0,
           "headings": [["one", 600], ["two", 1500], ["three", 2400], ["four", 3300]],
           "sideHeight": 800, "sideScrollHeight": 2000, "entryTop": 1500, "outlineTop": 1540,
           "groupAbove": True, "steps": []}
    cfg.update(overrides)
    harness = HARNESS % {"cfg": json.dumps(cfg), "script": SCRIPT}
    out = subprocess.run(["node", "-e", harness], capture_output=True, text=True, timeout=20, check=True)
    return json.loads(out.stdout)


def marks(seen: list[dict]) -> list[list[str]]:
    """The parts marked in the sidebar, at load and after each step."""
    return [state["marked"] for state in seen]


class TestThePartBeingRead:
    def test_none_above_the_first_part(self):
        assert marks(run()) == [[]]

    def test_a_part_counts_once_its_heading_reaches_the_upper_quarter(self):
        """Its top 252px from the window's: 253 is not yet, 252 is."""
        assert marks(run(steps=[{"scroll": 347}, {"scroll": 348}])) == [[], [], ["one"]]

    def test_the_mark_moves_with_the_reading_and_back(self):
        seen = run(steps=[{"scroll": 400}, {"scroll": 1300}, {"scroll": 2300}, {"scroll": 400}])
        assert marks(seen) == [[], ["one"], ["two"], ["three"], ["one"]]

    def test_both_lists_are_marked_and_no_other_link(self):
        """The sidebar's and the phone's menu's, each for assistive technology too."""
        for state in run(steps=[{"scroll": 1300}, {"scroll": 2300}])[1:]:
            assert state["menuMarked"] == state["marked"] and len(state["marked"]) == 1
            assert state["othersTidy"]

    def test_the_last_part_at_the_very_bottom(self):
        """A short closing part never lifts its heading to the upper quarter."""
        seen = run(headings=[["one", 600], ["two", 1500], ["last", 4900]], steps=[{"scroll": 4148}])
        assert seen[-1]["marked"] == ["last"]

    def test_a_page_that_does_not_scroll_marks_nothing_for_being_at_its_bottom(self):
        assert marks(run(pageHeight=800, headings=[["one", 600], ["two", 700]])) == [[]]


class TestTheSidebar:
    def test_shows_the_page_entry_with_its_theme_when_its_outline_was_below(self):
        """A page far down the guides' list had its outline below the fold."""
        assert run()[0]["sideTop"] == 1500 - 30 - 12          # the theme's label, 12px of air
        assert run(groupAbove=False)[0]["sideTop"] == 1500 - 12

    def test_leaves_it_where_it_is_when_the_outline_is_in_view(self):
        assert run(entryTop=100, outlineTop=140)[0]["sideTop"] == 0

    def test_keeps_the_part_being_read_in_view_down_and_up(self):
        """A chapter of 33 parts: the mark left the sidebar from the 25th on (Chromium,
        2026-11-01). It scrolls as little as it takes, both ways."""
        headings = [[f"p{k}", 600 + 300 * k] for k in range(40)]
        to = lambda k: {"scroll": 600 + 300 * k - 200}     # noqa: E731 - the part k at 200px
        seen = run(headings=headings, pageHeight=14600, entryTop=100, outlineTop=140,
                   steps=[to(35), to(39), to(0)])
        assert marks(seen) == [[], ["p35"], ["p39"], ["p0"]]
        assert [state["sideTop"] for state in seen] == [58, 72, 152, 128]

    def test_a_hidden_sidebar_is_left_alone(self):
        """On a phone the sidebar is not shown, and measures nothing."""
        seen = run(sideHeight=0, sideScrollHeight=0, steps=[{"scroll": 1300}])
        assert [state["sideTop"] for state in seen] == [0, 0]
        assert seen[-1]["menuMarked"] == ["two"]


class TestThePhoneMenu:
    def test_folds_once_a_part_is_chosen(self):
        seen = run(steps=[{"click": "summary"}, {"click": "link"}])
        assert [state["menuOpen"] for state in seen] == [True, True, False]
