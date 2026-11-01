/* The outline of a page of the manual, the guides or the blog: its parts, which
 * gen_manual_html.py lists in the sidebar under the page's own entry and, on a phone, in the
 * "On this page" menu under its title.
 *
 * Without this script the outline already works: its entries are plain links to the headings.
 * The script adds three things.
 *
 * - It marks the part being read, in both lists: the last part whose heading has passed the
 *   upper quarter of the screen, below the top bar; at the very bottom of the page, the last
 *   part, whose heading a short closing section never lifts that far.
 * - It keeps the page's entry and the part being read in view in the sidebar, when its list is
 *   taller than the screen. A page far down the guides' list had its outline below the fold, and
 *   on a chapter of 33 parts the mark left the sidebar from the 25th on (Chromium, 2026-11-01).
 *   Only the sidebar's own scroll is set: scrollIntoView would move the page too.
 * - It folds the phone's menu once a part is chosen, so the menu does not stand open above the
 *   text when the reader comes back up.
 *
 * One scroll listener, one pass per frame at most and only while the page moves — the pattern
 * of to-top.js. First-party and dependency-free, like everything else the site loads.
 */
(function () {
    'use strict';

    var links = Array.prototype.slice.call(document.querySelectorAll('.man-outline a[href^="#"]'));
    if (!links.length) return;

    /** The page's parts in page order, each with its heading and the links pointing at it. */
    var parts = [];
    var byId = {};
    links.forEach(function (link) {
        var id = decodeURIComponent(link.getAttribute('href').slice(1));
        var part = byId[id];
        if (!part) {
            var heading = document.getElementById(id);
            if (!heading) return;
            part = byId[id] = { heading: heading, links: [] };
            parts.push(part);
        }
        part.links.push(link);
    });
    if (!parts.length) return;
    // Both lists give the parts in page order, but nothing has to keep them so.
    parts.sort(function (a, b) {
        return a.heading.compareDocumentPosition(b.heading) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1;
    });

    var bar = document.querySelector('.man-top');
    var side = document.querySelector('.man-shell > .man-nav');
    var current = null;
    var queued = false;

    /** Room kept above and below an entry the sidebar is scrolled to, so it does not touch an edge. */
    var MARGIN = 12;

    /**
     * Whether the sidebar scrolls on its own: its list is taller than the screen. A hidden sidebar
     * — on a phone — measures nothing, and is left alone.
     *
     * @returns {boolean} Whether its scroll can be set.
     */
    function sideScrolls() {
        return !!side && side.scrollHeight > side.clientHeight;
    }

    /**
     * Scrolls the sidebar, and nothing else, as little as it takes to show an element of it.
     * Its entries are placed against the sidebar, the nearest positioned box (it is sticky).
     *
     * @param {HTMLElement} el An element of the sidebar.
     */
    function showInSide(el) {
        var top = el.offsetTop;
        var bottom = top + el.offsetHeight;
        if (top - MARGIN < side.scrollTop) {
            side.scrollTop = Math.max(0, top - MARGIN);
        } else if (bottom + MARGIN > side.scrollTop + side.clientHeight) {
            side.scrollTop = bottom + MARGIN - side.clientHeight;
        }
    }

    /**
     * Marks a part's links as the one being read, or clears them.
     *
     * @param {{links: HTMLAnchorElement[]}} part The part.
     * @param {boolean} on Whether it is the one being read.
     */
    function mark(part, on) {
        part.links.forEach(function (link) {
            link.classList.toggle('is-current', on);
            if (on) link.setAttribute('aria-current', 'true');
            else link.removeAttribute('aria-current');
        });
    }

    /**
     * Finds the part being read and marks it, if it changed since the last pass, keeping its
     * entry in view in the sidebar.
     */
    function paint() {
        queued = false;
        var top = bar ? bar.getBoundingClientRect().bottom : 0;
        var line = top + (window.innerHeight - top) * 0.25;
        var found = null;
        for (var i = 0; i < parts.length; i++) {
            if (parts[i].heading.getBoundingClientRect().top > line) break;
            found = parts[i];
        }
        var doc = document.documentElement;
        if (window.scrollY > 0 && window.innerHeight + window.scrollY >= doc.scrollHeight - 2) {
            found = parts[parts.length - 1];
        }
        if (found === current) return;
        if (current) mark(current, false);
        if (found) mark(found, true);
        current = found;
        if (found && sideScrolls()) {
            found.links.forEach(function (link) {
                if (side.contains(link)) showInSide(link);
            });
        }
    }

    /** Asks for one pass on the next frame, however many scroll events arrive before it. */
    function queue() {
        if (queued) return;
        queued = true;
        window.requestAnimationFrame(paint);
    }

    // The page's entry and its outline first, its theme's label with it when it sits right
    // above; the part being read, if the page opened further down, then has its say.
    var entry = side && side.querySelector('.man-nav-item.active');
    if (entry && sideScrolls()) {
        var outline = entry.nextElementSibling;
        var last = outline && outline.classList.contains('man-outline') ? outline : entry;
        if (last.offsetTop + last.offsetHeight > side.scrollTop + side.clientHeight) {
            var first = entry.previousElementSibling;
            if (!first || !first.classList.contains('man-nav-group')) first = entry;
            side.scrollTop = Math.max(0, first.offsetTop - MARGIN);
        }
    }

    window.addEventListener('scroll', queue, { passive: true });
    window.addEventListener('resize', queue, { passive: true });
    paint();

    // A part chosen in the phone's menu: the menu folds as the page goes to the part.
    var menu = document.querySelector('.man-outline-menu');
    if (menu) {
        menu.addEventListener('click', function (event) {
            if (event.target.closest('a')) menu.open = false;
        });
    }
})();
