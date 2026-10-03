// Back to top, for the landing and every page of the manual: a round button in the
// bottom-right corner, shown once the first screen is behind, with a ring round it that fills
// with the reading. Its look is in style.css (.to-top), which both kinds of page load.
//
// The button is built here rather than written into each page: without this script it could
// never be shown (it stays hidden until the reader has scrolled), so a page without the script
// is better off without the button. One source for the landing and the generated manual.
//
// The ring is drawn here, not by a scroll-driven animation: Safari before 26 and Firefox cannot
// run those, and the ring stayed empty there (seen in Safari on 2026-10-03). One listener, one
// write per frame at most, and only while the page moves.
(function () {
    var ARROW = '<svg class="tt-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"'
        + ' stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        + '<path d="m5 12 7-7 7 7" /><path d="M12 19V5" /></svg>'; // Lucide: arrow-up
    var RING = '<svg class="tt-ring" viewBox="0 0 52 52" aria-hidden="true">'
        + '<circle class="tt-track" cx="26" cy="26" r="24" pathLength="100" />'
        + '<circle class="tt-progress" cx="26" cy="26" r="24" pathLength="100" /></svg>';

    var btn = document.createElement('a');
    btn.className = 'to-top';
    // "#top" needs no element: the browser scrolls to the top of the page for it.
    btn.href = '#top';
    btn.setAttribute('aria-label', 'Back to top');
    btn.innerHTML = RING + ARROW;
    document.body.appendChild(btn);

    var mark = btn.querySelector('.tt-progress');
    var queued = false;

    /**
     * Shows the button once the first screen is behind, and draws the share of the page read
     * as the length of the ring, out of 100.
     */
    function paint() {
        queued = false;
        var y = window.scrollY;
        var max = document.documentElement.scrollHeight - window.innerHeight;
        var read = max > 0 ? Math.min(1, Math.max(0, y / max)) : 0;
        mark.style.strokeDashoffset = String(+(100 - 100 * read).toFixed(2));
        btn.classList.toggle('is-visible', y > window.innerHeight);
    }

    /** Asks for one paint on the next frame, however many scroll events arrive before it. */
    function queue() {
        if (queued) return;
        queued = true;
        window.requestAnimationFrame(paint);
    }

    window.addEventListener('scroll', queue, { passive: true });
    window.addEventListener('resize', queue, { passive: true });
    paint();

    // Scrolled here rather than followed as a link: following "#top" wrote it into the address
    // and added a step to the history, so Back then scrolled down again instead of leaving the
    // page. scrollTo with no behaviour follows the page's own scroll-behavior: smooth, or a jump
    // for whoever asked for less motion. The button is gone once the top is reached: keyboard
    // focus moves to the first link of the bar (the landing's logo, the manual's home link).
    btn.addEventListener('click', function (event) {
        event.preventDefault();
        window.scrollTo({ top: 0 });
        var home = document.querySelector('.nav-logo, .man-home');
        if (home) home.focus({ preventScroll: true });
    });
})();
