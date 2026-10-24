// Hero carousel — runs immediately, script is at end of body
//
// No timer here: the time a screen stays is the current dot's fill, an animation of the
// stylesheet (hero-progress), and the next screen comes when it ends. The bar and the change
// cannot drift apart, and a pause holds both where they are. A dot shown anew starts its fill
// from empty.
(function () {
    var imgs = document.querySelectorAll('.hero-screenshot');
    var dots = document.querySelectorAll('.hero-dots .dot');
    // Caption and annotations, each tagged with the slide it belongs to. Collected in one
    // list because they share a rule: shown only while their own slide is.
    var notes = document.querySelectorAll('.hero-caption, .hero-note');
    var controls = document.querySelector('.hero-controls');
    var playBtn = document.getElementById('heroPlay');
    if (!imgs.length || !controls) return;

    var cur = 0;

    /**
     * Shows a screen, its dot and its words.
     *
     * @param {number} n - The screen's index; one past either end wraps round.
     */
    function show(n) {
        imgs[cur].classList.remove('active');
        if (dots[cur]) {
            dots[cur].classList.remove('active');
            dots[cur].removeAttribute('aria-current');
        }
        cur = ((n % imgs.length) + imgs.length) % imgs.length;
        imgs[cur].classList.add('active');
        if (dots[cur]) {
            dots[cur].classList.add('active');
            dots[cur].setAttribute('aria-current', 'true');
        }
        notes.forEach(function (el) {
            el.classList.toggle('active', Number(el.dataset.slide) === cur);
        });
    }

    /**
     * Plays or pauses the carousel: the class runs or holds the fill, the button says what a
     * press would do.
     *
     * @param {boolean} on - True to play.
     */
    function setPlaying(on) {
        controls.classList.toggle('playing', on);
        if (playBtn) {
            playBtn.classList.toggle('paused', !on);
            playBtn.setAttribute('aria-label', on ? 'Pause' : 'Play');
        }
    }

    controls.addEventListener('animationend', function (e) {
        if (e.animationName === 'hero-progress') show(cur + 1);
    });

    dots.forEach(function (dot, i) {
        dot.addEventListener('click', function () { show(i); });
    });

    if (playBtn) playBtn.addEventListener('click', function () {
        setPlaying(!controls.classList.contains('playing'));
    });

    setPlaying(false);
})();

// Sparklines
function spark(id, seed) {
    var el = document.getElementById(id); if (!el) return;
    var pts = []; var v = .5;
    for (var i = 0; i < 60; i++) {
        v += (Math.sin(i * .4 + seed) * .3 + (Math.random() - .5) * .3) * .1;
        v = Math.max(0, Math.min(1, v));
        pts.push((i / 59 * 200).toFixed(1) + ',' + (16 - v * 14 - 1).toFixed(1));
    }
    el.innerHTML = '<polyline points="' + pts.join(' ') + '" fill="none" stroke="#000" stroke-width="1.2"/>';
}
spark('ds1', 1.2); spark('ds2', 2.8);

// The theme toggle is assets/theme-toggle.js, shared with the manual's pages.

// Right-edge scroll cue on the comparison table.
//
// The cue must vanish once there is nothing left to reveal: at the end of the scroll no
// column is cut any more, so the gradient stops hinting and simply paints over the last
// column's text. Measured at that position, it wiped characters outright rather than
// dimming them. Whether more content exists to the right is scroll state, which CSS alone
// cannot read on iOS, so a class carries it.
//
// Listener is passive and reads two properties already computed by the layout, so a swipe
// costs no measurable work; it only ever runs while this one table is being scrolled.
(function () {
    document.addEventListener('DOMContentLoaded', function () {
        var box = document.querySelector('.cmp-scroll');
        var wrap = document.querySelector('.cmp-scroll-wrap');
        if (!box || !wrap) return;

        /** Flags the wrapper while the table still hides content past its right edge. */
        function update() {
            // 1px of slack: sub-pixel layout keeps scrollLeft just short of the true maximum.
            var more = box.scrollWidth - box.clientWidth - box.scrollLeft > 1;
            wrap.classList.toggle('has-more', more);
        }

        box.addEventListener('scroll', update, { passive: true });
        window.addEventListener('resize', update, { passive: true });
        update();
    });
})();
