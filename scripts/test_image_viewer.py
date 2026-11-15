"""Tests for assets/image-viewer.js: a blog post's pictures, full screen.

The script runs under Node on a stand-in for a post, as manual-outline.js does in
test_manual_outline.py: an article whose pictures are links to their files, each followed by its
caption or not, and a <dialog> that opens, closes and gives the focus to its autofocus control the
way a browser's does. Each step clicks, presses a key, swipes or lets the files arrive, and the
window is read after it. Skipped where Node is not installed.

Run with ``python3 -m pytest scripts/test_image_viewer.py`` from the repository root.
"""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = (Path(__file__).resolve().parent.parent / "assets" / "image-viewer.js").read_text(encoding="utf-8")

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="Node is not installed")

#: Where the stand-in post is served: a link's ``href`` property and a picture's ``currentSrc``
#: are absolute, as in a browser.
BASE = "https://audiogravity.app/docs/blog/"

#: The post the script runs on, and the steps it takes.
HARNESS = r"""
const cfg = %(cfg)s;
const BASE = %(base)s;
const requested = [];
const loaders = [];
const dialogs = [];
let activeElement = null;

function textNode(data) {
    return { data: String(data), parentNode: null, cloneNode() { return textNode(this.data); } };
}

function el(tag, attrs) {
    const classes = new Set();
    const e = {
        tagName: tag.toUpperCase(),
        attrs: Object.assign({}, attrs || {}),
        childNodes: [],
        parentNode: null,
        listeners: {},
        hidden: false,
        className: (attrs && attrs.class) || '',
        innerHTML: '',
        classList: { add: (c) => classes.add(c), remove: (c) => classes.delete(c), contains: (c) => classes.has(c) },
        setAttribute(k, v) { this.attrs[k] = String(v); },
        getAttribute(k) { return k in this.attrs ? this.attrs[k] : null; },
        hasAttribute(k) { return k in this.attrs; },
        appendChild(c) { c.parentNode = this; this.childNodes.push(c); return c; },
        addEventListener(t, fn) { (this.listeners[t] = this.listeners[t] || []).push(fn); },
        fire(t, ev) { (this.listeners[t] || []).slice().forEach((fn) => fn(ev)); },
        get children() { return this.childNodes.filter((n) => n.tagName); },
        get firstElementChild() { return this.children[0] || null; },
        get nextElementSibling() {
            if (!this.parentNode) return null;
            const sib = this.parentNode.children;
            return sib[sib.indexOf(this) + 1] || null;
        },
        get textContent() { return this.childNodes.map((n) => (n.tagName ? n.textContent : n.data)).join(''); },
        set textContent(v) { this.childNodes = []; if (v !== '') this.appendChild(textNode(v)); },
        querySelector(sel) {
            for (const c of this.children) {
                if (c.tagName === sel.toUpperCase()) return c;
                const deeper = c.querySelector(sel);
                if (deeper) return deeper;
            }
            return null;
        },
        closest(sel) {
            const tests = sel.split(',').map((s) => s.trim()).map((s) => (s[0] === '.'
                ? (n) => (' ' + n.className + ' ').includes(' ' + s.slice(1) + ' ')
                : (n) => n.tagName === s.toUpperCase()));
            for (let n = this; n && n.tagName; n = n.parentNode) if (tests.some((t) => t(n))) return n;
            return null;
        },
        cloneNode() {
            const c = el(this.tagName.toLowerCase(), this.attrs);
            c.className = this.className;
            this.childNodes.forEach((n) => c.appendChild(n.cloneNode(true)));
            return c;
        },
        focus() { activeElement = this; },
    };
    return e;
}

function find(root, test) {
    for (const c of root.children) {
        if (test(c)) return c;
        const deeper = find(c, test);
        if (deeper) return deeper;
    }
    return null;
}
const byClass = (root, name) => find(root, (n) => (' ' + n.className + ' ').includes(' ' + name + ' '));

globalThis.Image = function () { loaders.push(this); };
Object.defineProperty(Image.prototype, 'src', {
    set(v) { this._src = v; requested.push(v); },
    get() { return this._src; },
});

globalThis.document = {
    documentElement: el('html'),
    body: el('body'),
    keyListeners: [],
    createElement(tag) {
        const e = el(tag);
        if (tag === 'dialog') {
            dialogs.push(e);
            e.open = false;
            if (cfg.dialog) {
                // A browser's dialog focusing steps: the dialog itself when it has autofocus, else
                // its first descendant that has.
                e.showModal = () => {
                    e.open = true;
                    const first = e.hasAttribute('autofocus') ? e : find(e, (n) => n.hasAttribute('autofocus'));
                    if (first) first.focus();
                };
                e.close = () => {
                    if (!e.open) return;
                    e.open = false;
                    e.fire('close', {});
                };
            }
        }
        return e;
    },
    querySelectorAll(sel) { return sel === '.man-md a.man-zoom' ? links : []; },
    addEventListener(t, fn) { if (t === 'keydown') this.keyListeners.push(fn); },
    removeEventListener(t, fn) { if (t === 'keydown') this.keyListeners = this.keyListeners.filter((f) => f !== fn); },
};

const article = el('article', { class: 'man-md' });
const links = [];
let shots = null;
cfg.pictures.forEach((p) => {
    const img = el('img', { src: p.src, alt: p.alt });
    const loaded = p.loaded !== false;
    img.complete = loaded;
    img.naturalWidth = loaded ? 500 : 0;
    img.currentSrc = loaded ? BASE + p.src : '';
    const link = el('a', { class: 'man-zoom', href: p.href });
    link.href = BASE + p.href;
    link.appendChild(img);
    // A picture of a set of screenshots sits in the set's .man-shots, as the press release's do.
    const holder = p.set ? (shots || (shots = article.appendChild(el('div', { class: 'man-shots' })))) : article;
    if (p.caption === 'figure') {
        const fig = el('figure');
        fig.appendChild(link);
        const cap = el('figcaption');
        cap.appendChild(textNode(p.text));
        fig.appendChild(cap);
        holder.appendChild(fig);
    } else {
        holder.appendChild(link);
        if (p.caption === 'em' || p.caption === 'mixed') {
            const para = el('p');
            const em = el('em');
            em.appendChild(textNode(p.text));
            if (p.caption === 'mixed') para.appendChild(textNode('Before it: '));
            para.appendChild(em);
            holder.appendChild(para);
        }
    }
    links.push(link);
});

%(script)s

const clickEvent = (extra) => Object.assign({
    button: 0, metaKey: false, ctrlKey: false, shiftKey: false, altKey: false,
    defaultPrevented: false, preventDefault() { this.defaultPrevented = true; },
}, extra || {});

const state = (ev) => {
    const d = dialogs[0];
    const built = !!(d && d.childNodes.length);
    const pick = (name) => (built ? byClass(d, name) : null);
    const img = pick('man-viewer-img');
    const count = pick('man-viewer-count');
    const text = pick('man-viewer-text');
    const prev = pick('man-viewer-prev');
    const next = pick('man-viewer-next');
    const close = pick('man-viewer-close');
    const at = links.indexOf(activeElement);
    const where = at >= 0 ? 'link' + at : (activeElement && activeElement === d ? 'window'
        : (activeElement && activeElement === close ? 'close' : null));
    return {
        open: !!(d && d.open),
        src: img ? img.src : null,
        alt: img ? img.alt : null,
        count: count && !count.hidden ? count.textContent : null,
        caption: text ? text.textContent : null,
        arrows: prev && !prev.hidden ? [prev.getAttribute('aria-disabled'), next.getAttribute('aria-disabled')] : null,
        locked: document.documentElement.classList.contains('man-viewer-open'),
        focus: where,
        label: d ? d.getAttribute('aria-label') : null,
        prevented: ev ? ev.defaultPrevented : null,
        requested: requested.slice(),
        clickListeners: links.map((l) => (l.listeners.click || []).length),
    };
};

const seen = [];
for (const step of cfg.steps) {
    const d = dialogs[0];
    let ev = null;
    if ('click' in step) {
        ev = clickEvent(step.mods);
        links[step.click].fire('click', ev);
    }
    if ('press' in step) {
        const b = byClass(d, 'man-viewer-' + step.press);
        b.fire('click', {});
        d.fire('click', { target: b });
    }
    if ('key' in step) {
        ev = { key: step.key, defaultPrevented: false, preventDefault() { this.defaultPrevented = true; } };
        document.keyListeners.slice().forEach((fn) => fn(ev));
    }
    if ('escape' in step) d.close();
    if ('tap' in step) {
        const target = step.tap === 'ground' ? d : byClass(d, step.tap === 'picture' ? 'man-viewer-img' : 'man-viewer-text');
        d.fire('click', { target });
    }
    if ('swipe' in step) {
        const [dx, dy, kind] = step.swipe;
        d.fire('pointerdown', { pointerType: kind || 'touch', clientX: 200, clientY: 300 });
        d.fire('pointerup', { pointerType: kind || 'touch', clientX: 200 + dx, clientY: 300 + dy });
        if (step.thenClick) d.fire('click', { target: byClass(d, 'man-viewer-img') });
    }
    if ('pinch' in step) {
        d.fire('pointerdown', { pointerType: 'touch', clientX: 200, clientY: 300 });
        d.fire('pointerdown', { pointerType: 'touch', clientX: 260, clientY: 300 });
        d.fire('pointerup', { pointerType: 'touch', clientX: 80, clientY: 300 });
        d.fire('pointerup', { pointerType: 'touch', clientX: 380, clientY: 300 });
    }
    if ('arrive' in step) loaders.forEach((l) => { if (l.onload) l.onload(); });
    seen.push(state(ev));
}
console.log(JSON.stringify(seen));
"""

#: Three pictures: two captioned in italics under them, as the posts write it, one without.
THREE = [
    {"href": "images/a.webp", "src": "images/a.webp", "alt": "A", "caption": "em", "text": "Picture A."},
    {"href": "images/b.webp", "src": "images/b.webp", "alt": "B", "caption": "em", "text": "Picture B."},
    {"href": "images/c.webp", "src": "images/c.webp", "alt": "C", "caption": "none"},
]


def run(steps, pictures=None, dialog=True) -> list[dict]:
    """Run the script on the stand-in post, then each step, and read the window after each.

    Args:
        steps: ``{"click": i, "mods": {...}}`` on a picture's link, ``{"press": "prev" | "next" |
            "close"}`` on a button, ``{"key": name}``, ``{"escape": 1}``, ``{"tap": "ground" |
            "picture" | "caption"}``, ``{"swipe": [dx, dy, pointer type], "thenClick": bool}``,
            ``{"pinch": 1}``, ``{"arrive": 1}`` for every file asked for to arrive.
        pictures: The post's pictures, THREE by default.
        dialog: Whether the browser knows <dialog>.

    Returns:
        The window after each step: open or not, the file and description shown, the place
        ("2 / 3") and the caption, the arrows (each one's aria-disabled), the page's scroll lock,
        what has the focus, whether the step's event was taken over, and the files asked for.
    """
    cfg = {"pictures": pictures or THREE, "steps": list(steps), "dialog": dialog}
    harness = HARNESS % {"cfg": json.dumps(cfg), "base": json.dumps(BASE), "script": SCRIPT}
    out = subprocess.run(["node", "-e", harness], capture_output=True, text=True, timeout=20, check=True)
    return json.loads(out.stdout)


class TestOpening:
    def test_a_click_opens_the_picture_clicked_with_its_caption_and_place(self):
        state = run([{"click": 1}])[0]
        assert state["open"] and state["prevented"]
        assert state["src"] == BASE + "images/b.webp" and state["alt"] == "B"
        assert state["count"] == "2 / 3" and state["caption"] == "Picture B."
        assert state["locked"]

    def test_it_opens_on_itself_and_names_itself(self):
        """Not on its close button, which WebKit then ringed at a tap (2026-11-15); Tab goes on
        to the buttons."""
        state = run([{"click": 0}])[0]
        assert state["focus"] == "window" and state["label"] == "Picture viewer"

    def test_a_click_for_a_new_tab_or_window_is_left_to_the_browser(self):
        for mods in ({"metaKey": True}, {"ctrlKey": True}, {"shiftKey": True}, {"altKey": True}, {"button": 1}):
            state = run([{"click": 0, "mods": mods}])[0]
            assert not state["open"] and not state["prevented"], mods

    def test_without_a_dialog_the_pictures_stay_plain_links(self):
        """Safari before 15.4: the link opens the file, on a page of its own."""
        state = run([{"click": 0}], dialog=False)[0]
        assert not state["open"] and not state["prevented"]
        assert state["clickListeners"] == [0, 0, 0]


class TestGoingFromPictureToPicture:
    def test_the_arrows_go_on_and_stop_at_both_ends(self):
        seen = run([{"click": 0}, {"press": "next"}, {"press": "next"}, {"press": "next"},
                    {"press": "prev"}])
        assert [s["count"] for s in seen] == ["1 / 3", "2 / 3", "3 / 3", "3 / 3", "2 / 3"]
        assert [s["arrows"] for s in seen] == [["true", "false"], ["false", "false"],
                                               ["false", "true"], ["false", "true"], ["false", "false"]]
        assert all(s["open"] for s in seen)

    def test_the_keyboard_arrows_do_the_same_and_no_other_key(self):
        seen = run([{"click": 1}, {"key": "ArrowRight"}, {"key": "ArrowLeft"}, {"key": "ArrowLeft"}, {"key": "a"}])
        assert [s["count"] for s in seen] == ["2 / 3", "3 / 3", "2 / 3", "1 / 3", "1 / 3"]
        assert [s["prevented"] for s in seen[1:]] == [True, True, True, False]

    def test_a_picture_without_a_caption_shows_none(self):
        """Not the previous picture's: the caption is cleared at each step."""
        assert run([{"click": 1}, {"press": "next"}])[-1]["caption"] == ""

    def test_a_swipe_sideways_goes_on_leftwards_and_back_rightwards(self):
        seen = run([{"click": 1}, {"swipe": [-120, 10]}, {"swipe": [120, -10]}, {"swipe": [120, 0]}])
        assert [s["count"] for s in seen] == ["2 / 3", "3 / 3", "2 / 3", "1 / 3"]

    def test_a_short_or_mostly_upright_swipe_is_none(self):
        seen = run([{"click": 1}, {"swipe": [-30, 0]}, {"swipe": [-80, 150]}])
        assert [s["count"] for s in seen] == ["2 / 3"] * 3

    def test_a_mouse_drag_and_a_pinch_are_no_swipe(self):
        seen = run([{"click": 1}, {"swipe": [-200, 0, "mouse"]}, {"pinch": 1}])
        assert [s["count"] for s in seen] == ["2 / 3"] * 3

    def test_the_click_a_swipe_ends_with_does_not_close_the_window(self):
        seen = run([{"click": 1}, {"swipe": [-120, 0], "thenClick": True}])
        assert seen[-1]["open"] and seen[-1]["count"] == "3 / 3"

    def test_one_picture_shows_no_place_and_no_arrows(self):
        state = run([{"click": 0}], pictures=THREE[:1])[0]
        assert state["count"] is None and state["arrows"] is None and state["caption"] == "Picture A."

    def test_a_set_of_screenshots_is_a_series_of_its_own(self):
        """The press release's post: its photograph, then nine screenshots numbered 1 to 9 in
        their captions. Counted together, the first showed "2 / 10" (Chromium, 2026-11-15)."""
        pictures = [THREE[0],
                    {"href": "images/s1.webp", "src": "images/s1-small.webp", "alt": "S1", "caption": "figure",
                     "text": "1. One", "set": True},
                    {"href": "images/s2.webp", "src": "images/s2-small.webp", "alt": "S2", "caption": "figure",
                     "text": "2. Two", "set": True}]
        seen = run([{"click": 1}, {"press": "next"}, {"press": "next"}, {"escape": 1}, {"click": 0},
                    {"key": "ArrowRight"}], pictures=pictures)
        assert [s["count"] for s in seen[:3]] == ["1 / 2", "2 / 2", "2 / 2"]
        assert seen[0]["arrows"] == ["true", "false"]
        assert seen[4]["count"] is None and seen[4]["arrows"] is None and seen[4]["caption"] == "Picture A."
        assert seen[5]["src"] == BASE + "images/a.webp"


class TestClosing:
    @pytest.mark.parametrize("how", [{"press": "close"}, {"escape": 1}, {"tap": "ground"}, {"tap": "picture"}])
    def test_gives_the_page_back_and_the_focus_to_the_picture_opened(self, how):
        state = run([{"click": 1}, {"press": "next"}, how])[-1]
        assert not state["open"] and not state["locked"]
        assert state["focus"] == "link1"

    def test_a_click_in_the_caption_leaves_it_open(self):
        """The caption may hold a link: the photograph's source."""
        assert run([{"click": 0}, {"tap": "caption"}])[-1]["open"]

    def test_the_arrow_keys_are_the_page_s_again_once_closed(self):
        state = run([{"click": 1}, {"escape": 1}, {"key": "ArrowRight"}])[-1]
        assert not state["open"] and state["prevented"] is False

    def test_it_opens_again_on_another_picture(self):
        state = run([{"click": 0}, {"escape": 1}, {"click": 2}])[-1]
        assert state["open"] and state["count"] == "3 / 3" and state["locked"]


class TestFiles:
    SHOTS = [
        {"href": "images/one.webp", "src": "images/one-small.webp", "alt": "One", "caption": "figure", "text": "1. One"},
        {"href": "images/two.webp", "src": "images/two-small.webp", "alt": "Two", "caption": "figure", "text": "2. Two"},
        {"href": "images/three.webp", "src": "images/three-small.webp", "alt": "Three", "caption": "figure",
         "text": "3. Three", "loaded": False},
    ]

    def test_a_thumbnail_stands_in_until_its_large_file_has_arrived(self):
        seen = run([{"click": 0}, {"arrive": 1}], pictures=self.SHOTS)
        assert seen[0]["src"] == BASE + "images/one-small.webp"
        assert seen[1]["src"] == BASE + "images/one.webp"

    def test_a_large_file_arriving_late_does_not_replace_the_picture_shown_since(self):
        """The next picture is shown from its own file at once: nothing else arrives after it."""
        pictures = [self.SHOTS[0], dict(THREE[1], caption="figure", text="2. B")]
        seen = run([{"click": 0}, {"press": "next"}, {"arrive": 1}], pictures=pictures)
        assert seen[-1]["src"] == BASE + "images/b.webp" and seen[-1]["count"] == "2 / 2"

    def test_a_thumbnail_not_loaded_yet_gives_way_to_the_large_file_at_once(self):
        assert run([{"click": 2}], pictures=self.SHOTS)[0]["src"] == BASE + "images/three.webp"

    def test_the_caption_of_a_figure_is_its_own(self):
        assert run([{"click": 1}], pictures=self.SHOTS)[0]["caption"] == "2. Two"

    def test_a_paragraph_holding_more_than_italics_is_no_caption(self):
        pictures = [dict(THREE[0], caption="mixed"), THREE[1]]
        assert run([{"click": 0}], pictures=pictures)[0]["caption"] == ""

    def test_the_neighbours_are_asked_for_once_each(self):
        seen = run([{"click": 1}, {"press": "next"}, {"press": "prev"}, {"press": "prev"}])
        asked = [f for f in seen[-1]["requested"] if f in {BASE + p["href"] for p in THREE}]
        assert sorted(asked) == sorted({BASE + p["href"] for p in THREE})
        assert len(asked) == len(set(asked))
