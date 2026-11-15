/* The pictures of a blog post, full screen: a window over the page that shows one at a time, as
 * large as the screen allows, with its caption and its place among the post's ("2 / 6"), and goes
 * on to the others by its arrows, the keyboard's or a swipe.
 *
 * A set of screenshots (.man-shots) is a series of its own, read in its own numbering: the press
 * release's are numbered 1 to 9 in their captions, and the window counted the post's photograph
 * before them, showing the first as "2 / 10" (Chromium, 2026-11-15). The post's other pictures are
 * the other series.
 *
 * gen_manual_html.py makes each picture of a post a link to its own file (link_images()), so a
 * picture opens full size without this script too, on a page of its own. The script takes the
 * click over and opens the picture here instead — but not a click that asks for a new tab or
 * window, by a modifier key or the middle button: that one is left to the browser.
 *
 * The window is a <dialog>: it keeps the keyboard inside while it is open and closes on Escape,
 * and the focus goes back to the picture's link when it closes. A browser without one (Safari
 * before 15.4) keeps the plain links. It is built on the first opening: a reader who opens no
 * picture costs this file and nothing more.
 *
 * A thumbnail leads to a larger file than it shows (the press release's screenshots): the window
 * shows the thumbnail, already loaded, at once, and the large file as soon as it has arrived. The
 * pictures either side of the one shown are asked for in advance, two at most at each step, so a
 * swipe does not wait on the network.
 *
 * First-party and dependency-free, like everything else the site loads.
 */
(function () {
    'use strict';

    var links = Array.prototype.slice.call(document.querySelectorAll('.man-md a.man-zoom'));
    if (!links.length) return;

    var dialog = document.createElement('dialog');
    if (typeof dialog.showModal !== 'function') return;

    /** How far a finger must travel sideways, in CSS pixels, for a swipe to change the picture. */
    var SWIPE = 48;

    var ICONS = {
        close: '<path d="M18 6 6 18" /><path d="m6 6 12 12" />', // Lucide: x
        prev: '<path d="m15 18-6-6 6-6" />', // Lucide: chevron-left
        next: '<path d="m9 18 6-6-6-6" />' // Lucide: chevron-right
    };

    /** The post's series of pictures, by name: "shots" for the screenshots, "page" for the rest. */
    var series = {};

    /** The post's pictures in page order: each one's link, the picture in it, its caption, and
     * its series with its place in it. */
    var items = links.map(function (link) {
        var name = link.closest && link.closest('.man-shots') ? 'shots' : 'page';
        var list = series[name] = series[name] || [];
        var item = { link: link, img: link.querySelector('img'), caption: captionOf(link), list: list, at: list.length };
        list.push(item);
        return item;
    });

    var figure, img, count, text, prev, next;
    var current = null;
    var opener = null;
    var asked = {};
    var touch = null;
    var touches = 0;
    var swiped = false;

    items.forEach(function (item) {
        item.link.addEventListener('click', function (event) {
            if (event.defaultPrevented || event.button !== 0
                || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
            event.preventDefault();
            open(item);
        });
    });

    /**
     * The words that go with a picture: the caption of the figure it is in, or else the paragraph
     * right after it when that paragraph is all in italics — how the posts caption a photograph.
     *
     * @param {Element} link - The picture's link.
     * @returns {Element|null} The element whose content is the caption; null when it has none.
     */
    function captionOf(link) {
        var parent = link.parentNode;
        if (parent && parent.tagName === 'FIGURE') {
            var own = parent.querySelector('figcaption');
            if (own) return own;
        }
        var after = link.nextElementSibling;
        if (after && after.tagName === 'P' && after.children.length === 1) {
            var em = after.firstElementChild;
            if (em.tagName === 'EM' && em.textContent.trim() === after.textContent.trim()) return em;
        }
        return null;
    }

    /**
     * One of the window's round buttons, its icon drawn in the colour of its text.
     *
     * @param {string} name - Its own class, which places it (manual.css).
     * @param {string} label - What it does, for assistive technology.
     * @param {string} icon - The paths of its icon.
     * @returns {HTMLButtonElement} The button.
     */
    function button(name, label, icon) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'man-viewer-btn ' + name;
        b.setAttribute('aria-label', label);
        b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"'
            + ' stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + icon + '</svg>';
        return b;
    }

    /** Builds the window and wires its controls, once, on the first opening. */
    function build() {
        dialog.className = 'man-viewer';
        dialog.setAttribute('aria-label', 'Picture viewer');
        // The window opens on itself, which names itself to assistive technology; Tab goes on to
        // its buttons. Opened on its close button, WebKit drew a focus ring round it at a tap
        // (2026-11-15).
        dialog.setAttribute('tabindex', '-1');
        dialog.setAttribute('autofocus', '');
        figure = document.createElement('figure');
        figure.className = 'man-viewer-figure';
        img = document.createElement('img');
        img.className = 'man-viewer-img';
        img.setAttribute('decoding', 'async');
        var caption = document.createElement('figcaption');
        caption.className = 'man-viewer-caption';
        caption.setAttribute('aria-live', 'polite');
        count = document.createElement('span');
        count.className = 'man-viewer-count';
        text = document.createElement('span');
        text.className = 'man-viewer-text';
        caption.appendChild(count);
        caption.appendChild(text);
        figure.appendChild(img);
        figure.appendChild(caption);
        // The first control the keyboard reaches.
        var close = button('man-viewer-close', 'Close', ICONS.close);
        prev = button('man-viewer-prev', 'Previous picture', ICONS.prev);
        next = button('man-viewer-next', 'Next picture', ICONS.next);
        dialog.appendChild(close);
        dialog.appendChild(figure);
        dialog.appendChild(prev);
        dialog.appendChild(next);

        close.addEventListener('click', function () { dialog.close(); });
        prev.addEventListener('click', function () { step(-1); });
        next.addEventListener('click', function () { step(1); });
        // A click anywhere but on a button or in the caption closes the window: on the dark
        // ground as on the picture. Not the click a swipe may end with.
        dialog.addEventListener('click', function (event) {
            if (swiped) {
                swiped = false;
                return;
            }
            var target = event.target;
            if (target.closest && target.closest('button, .man-viewer-caption')) return;
            dialog.close();
        });
        dialog.addEventListener('pointerdown', down);
        dialog.addEventListener('pointerup', up);
        dialog.addEventListener('pointercancel', cancel);
        dialog.addEventListener('close', closed);
        document.body.appendChild(dialog);
    }

    /**
     * Opens the window on a picture.
     *
     * @param {Object} item - The picture, one of items.
     */
    function open(item) {
        if (!figure) build();
        opener = item.link;
        show(item);
        document.documentElement.classList.add('man-viewer-open');
        document.addEventListener('keydown', key);
        dialog.showModal();
    }

    /**
     * Goes on to the next picture of the series shown, or back to the previous one. Past the
     * first and the last nothing changes: that is where the arrows and the swipes stop.
     *
     * @param {number} by - 1 to go on, -1 to go back.
     */
    function step(by) {
        var to = current && current.list[current.at + by];
        if (to) show(to);
    }

    /**
     * Shows a picture, with its caption and its place in its series, and asks in advance for the
     * files of its neighbours there.
     *
     * @param {Object} item - The picture, one of items.
     */
    function show(item) {
        current = item;
        var list = item.list;
        var file = item.link.href;
        var shown = item.img;
        img.alt = shown ? shown.getAttribute('alt') || '' : '';
        // A thumbnail already in the page stands in until its large file has arrived.
        if (shown && shown.complete && shown.naturalWidth && shown.currentSrc && shown.currentSrc !== file) {
            img.src = shown.currentSrc;
            fetchPicture(file, function () {
                if (current === item) img.src = file;
            });
        } else {
            img.src = file;
        }
        var many = list.length > 1;
        count.hidden = !many;
        count.textContent = (item.at + 1) + ' / ' + list.length;
        text.textContent = '';
        if (item.caption) {
            Array.prototype.forEach.call(item.caption.childNodes, function (node) {
                text.appendChild(node.cloneNode(true));
            });
        }
        prev.hidden = !many;
        next.hidden = !many;
        // aria-disabled rather than disabled: a disabled button loses the focus, which then
        // leaves the window, and the arrow keys with it.
        prev.setAttribute('aria-disabled', String(item.at === 0));
        next.setAttribute('aria-disabled', String(item.at === list.length - 1));
        ahead(list[item.at - 1]);
        ahead(list[item.at + 1]);
    }

    /**
     * Asks for a picture's file.
     *
     * @param {string} file - Its address.
     * @param {function()=} done - Called once it has arrived.
     */
    function fetchPicture(file, done) {
        var loader = new Image();
        if (done) loader.onload = done;
        loader.src = file;
    }

    /**
     * Asks in advance for a picture's file, when there is a picture there and its file was not
     * asked for yet.
     *
     * @param {Object|undefined} item - The picture, one of items; none past either end.
     */
    function ahead(item) {
        if (!item) return;
        var file = item.link.href;
        if (asked[file]) return;
        asked[file] = true;
        fetchPicture(file);
    }

    /**
     * The keyboard while the window is open: the arrows go from picture to picture. Escape is the
     * dialog's own.
     *
     * @param {KeyboardEvent} event - The key pressed.
     */
    function key(event) {
        if (event.key === 'ArrowLeft') step(-1);
        else if (event.key === 'ArrowRight') step(1);
        else return;
        event.preventDefault();
    }

    /**
     * The start of a touch, where a swipe would start. A second finger makes it a pinch, which is
     * no swipe. A mouse does not swipe: it clicks the arrows.
     *
     * @param {PointerEvent} event - The pointer pressed.
     */
    function down(event) {
        swiped = false;
        if (event.pointerType === 'mouse') return;
        touches += 1;
        touch = touches === 1 ? { x: event.clientX, y: event.clientY } : null;
    }

    /**
     * The end of a touch: a swipe sideways, longer than SWIPE and clearly wider than high, goes to
     * the next picture when it runs leftwards, to the previous one when it runs rightwards.
     *
     * @param {PointerEvent} event - The pointer lifted.
     */
    function up(event) {
        if (event.pointerType === 'mouse') return;
        touches = Math.max(0, touches - 1);
        var from = touch;
        touch = null;
        if (!from) return;
        var dx = event.clientX - from.x;
        var dy = event.clientY - from.y;
        if (Math.abs(dx) < SWIPE || Math.abs(dx) < 1.5 * Math.abs(dy)) return;
        swiped = true;
        step(dx < 0 ? 1 : -1);
    }

    /** A touch the browser took over, to zoom or to scroll: no swipe. */
    function cancel() {
        touches = Math.max(0, touches - 1);
        touch = null;
    }

    /** Gives the page back: its scroll, its keyboard, and the focus to the picture's link. */
    function closed() {
        document.documentElement.classList.remove('man-viewer-open');
        document.removeEventListener('keydown', key);
        touch = null;
        touches = 0;
        if (opener) opener.focus({ preventScroll: true });
    }
})();
