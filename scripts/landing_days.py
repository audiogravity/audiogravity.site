"""What the tests of the days the landing dresses up share: the theme script run as a browser runs
it, and readers of the files they check.

index.html's <head> holds a few lines of JavaScript that decide, before the first paint, the theme
a visitor sees and whether the page dresses up for a day of the year: Halloween every 31 October,
Christmas every 24 and 25 December. Each day's tests run that script under Node, at a given local
date and time, so that the date is checked as the browser reads it rather than as the source reads
to a person. Node is installed on the Landing workflow's runner; where it is not, those tests are
skipped (needs_node).

Shared by scripts/test_halloween.py, scripts/test_christmas.py and scripts/test_days.py; not a test
file itself.
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PAGE = (ROOT / "index.html").read_text(encoding="utf-8")
SITE_CSS = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")

needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="Node is not installed")


def head_script() -> str:
    """The theme script of the landing's <head>, the one that decides on the days."""
    head = PAGE[:PAGE.index("</head>")]
    scripts = re.findall(r"<script>(.*?)</script>", head, re.S)
    found = [s for s in scripts if "ag-theme" in s]
    assert len(found) == 1, "the theme script of <head> is gone or doubled"
    return found[0]


def run_head(now: str, search: str = "", saved: str | None = None) -> dict:
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
           "script": head_script()}
    out = subprocess.run(["node", "-e", harness], capture_output=True, text=True, timeout=20, check=True)
    return json.loads(out.stdout)


def column() -> tuple[int, int, int]:
    """The text column down the page, as style.css lays it out.

    Returns:
        The column's widest (.w max-width), its own padding, and the section's padding beside
        it, all in px, on a screen wider than a phone.
    """
    found = re.search(r"^\.w\s*\{\s*max-width:\s*(\d+)px;.*?padding: 0 max\((\d+)px", SITE_CSS, re.S | re.M)
    section = re.search(r"^\.section\s*\{\s*padding:\s*\d+px (\d+)px", SITE_CSS, re.M)
    return int(found.group(1)), int(found.group(2)), int(section.group(1))


def px(rule: str, prop: str) -> float | None:
    """A length in px from a rule's declarations.

    Args:
        rule: The declarations, between the braces.
        prop: The property, e.g. ``width``.

    Returns:
        Its value in px, or None when the rule does not set it.
    """
    found = re.search(r"(?:^|[;{\s])%s:\s*(-?[\d.]+)px" % re.escape(prop), rule)
    return float(found.group(1)) if found else None


def webp_size(path: Path) -> tuple[int, int]:
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


def announce_script() -> str:
    """The script right after the announce bar: the bar's writer, and what it says before the day."""
    after = PAGE[PAGE.index('<div class="announce-bar">'):]
    return re.search(r"</div>\s*<script>(.*?)</script>", after, re.S).group(1)


def run_announce(now: str, steps: tuple = (), fade: str = "0.18s") -> dict:
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
           "script": announce_script()}
    out = subprocess.run(["node", "-e", harness], capture_output=True, text=True, timeout=20, check=True)
    return json.loads(out.stdout)


def grounds() -> list[str]:
    """The page's grounds, light and dark: --bg and --bg2 of each theme (style.css), as #rrggbb."""
    light = re.search(r":root \{[^}]*?--bg: (#[0-9a-f]{3,6});\s*--bg2: (#[0-9a-f]{3,6})", SITE_CSS, re.S)
    dark = re.search(r':root\[data-theme="dark"\] \{[^}]*?--bg: (#[0-9a-f]{3,6});\s*--bg2: (#[0-9a-f]{3,6})',
                     SITE_CSS, re.S)
    found = [g for m in (light, dark) for g in m.groups()]
    assert len(found) == 4, "a theme's grounds moved in style.css"
    return ["#" + "".join(c * 2 for c in g[1:]) if len(g) == 4 else g for g in found]


def contrast(a: str, b: str) -> float:
    """The contrast ratio of two colours, as WCAG reckons it.

    Args:
        a: A colour, #rrggbb.
        b: Another.

    Returns:
        The ratio, 1 to 21.
    """
    def luminance(colour: str) -> float:
        channels = [int(colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in channels]
        return .2126 * linear[0] + .7152 * linear[1] + .0722 * linear[2]

    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + .05) / (lo + .05)
