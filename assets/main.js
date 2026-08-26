// Hero carousel — runs immediately, script is at end of body
(function () {
    var imgs = document.querySelectorAll('.hero-screenshot');
    var dots = document.querySelectorAll('.hero-dots .dot');
    // Caption and annotations, each tagged with the slide it belongs to. Collected in one
    // list because they share a rule: shown only while their own slide is.
    var notes = document.querySelectorAll('.hero-caption, .hero-note');
    var prevBtn = document.getElementById('heroPrev');
    var nextBtn = document.getElementById('heroNext');
    var playBtn = document.getElementById('heroPlay');
    if (!imgs.length) return;

    var cur = 0;
    var playing = false;
    var timer = null;

    function show(n) {
        imgs[cur].classList.remove('active');
        if (dots[cur]) dots[cur].classList.remove('active');
        cur = ((n % imgs.length) + imgs.length) % imgs.length;
        imgs[cur].classList.add('active');
        if (dots[cur]) dots[cur].classList.add('active');
        notes.forEach(function (el) {
            el.classList.toggle('active', Number(el.dataset.slide) === cur);
        });
    }

    function startTimer() {
        clearInterval(timer);
        timer = setInterval(function () { show(cur + 1); }, 3500);
    }

    function pause() {
        playing = false;
        clearInterval(timer);
        timer = null;
        if (playBtn) playBtn.classList.add('paused');
    }

    function play() {
        playing = true;
        if (playBtn) playBtn.classList.remove('paused');
        startTimer();
    }

    dots.forEach(function (dot, i) {
        dot.addEventListener('click', function () {
            show(i);
            if (playing) startTimer();
        });
    });

    if (prevBtn) prevBtn.addEventListener('click', function () {
        show(cur - 1);
        if (playing) startTimer();
    });

    if (nextBtn) nextBtn.addEventListener('click', function () {
        show(cur + 1);
        if (playing) startTimer();
    });

    if (playBtn) playBtn.addEventListener('click', function () {
        if (playing) pause(); else play();
    });

    pause();
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

// Theme toggle
(function () {
    var root = document.documentElement;
    var KEY = 'ag-theme';
    var SUN = '<circle cx="12" cy="12" r="4" /> <path d="M12 2v2" /> <path d="M12 20v2" /> <path d="m4.93 4.93 1.41 1.41" /> <path d="m17.66 17.66 1.41 1.41" /> <path d="M2 12h2" /> <path d="M20 12h2" /> <path d="m6.34 17.66-1.41 1.41" /> <path d="m19.07 4.93-1.41 1.41" />';
    var MOON = '<path d="M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401" />';

    function isDark() {
        var t = root.getAttribute('data-theme');
        if (t === 'dark') return true;
        if (t === 'light') return false;
        return window.matchMedia('(prefers-color-scheme: dark)').matches;
    }

    function applyIcon() {
        var icon = document.getElementById('themeIcon');
        if (icon) icon.innerHTML = isDark() ? SUN : MOON;
    }

    function toggle() {
        root.setAttribute('data-theme', isDark() ? 'light' : 'dark');
        localStorage.setItem(KEY, root.getAttribute('data-theme'));
        applyIcon();
    }

    var saved = localStorage.getItem(KEY);
    if (saved) root.setAttribute('data-theme', saved);

    var btn = document.getElementById('themeToggle');
    if (btn) btn.addEventListener('click', toggle);
    applyIcon();
})();

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
