// Hero carousel — runs immediately, script is at end of body
(function () {
    var imgs = document.querySelectorAll('.hero-screenshot');
    var dots = document.querySelectorAll('.hero-dots .dot');
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
    var SUN = '<circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>';
    var MOON = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>';

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

// Shake ribbon on trial button click
(function () {
    document.addEventListener('DOMContentLoaded', function () {
        var btn = document.querySelector('a.cta-primary[href="#install"]');
        var ribbon = document.querySelector('.ribbon');
        if (!btn || !ribbon) return;
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            ribbon.classList.remove('shake');
            void ribbon.offsetWidth;
            ribbon.classList.add('shake');
            ribbon.addEventListener('animationend', function () {
                ribbon.classList.remove('shake');
            }, { once: true });
        });
    });
})();

// Shake ribbon on GitHub Releases click
(function () {
    document.addEventListener('DOMContentLoaded', function () {
        var btn = document.querySelector('a.nav-gh');
        var ribbon = document.querySelector('.ribbon');
        if (!btn || !ribbon) return;
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            ribbon.classList.remove('shake');
            void ribbon.offsetWidth;
            ribbon.classList.add('shake');
            ribbon.addEventListener('animationend', function () {
                ribbon.classList.remove('shake');
            }, { once: true });
        });
    });
})();
