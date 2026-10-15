// Light / dark toggle, for the landing and every page of the manual: the button
// (#themeToggle, its icon #themeIcon) is written into each page's bar, and this script makes
// it work. One choice for the whole site, kept under the same key: switched on the landing,
// it holds in the manual, and the other way round. Without a choice, the system's appearance
// stands (the stylesheet's media query).
//
// Each page also applies the stored choice in an inline script in its <head>, before the
// first paint; this one only follows the clicks and draws the icon. A browser that refuses
// storage (private mode) still switches, for as long as the page is open.
(function () {
    var root = document.documentElement;
    var KEY = 'ag-theme';
    var SUN = '<circle cx="12" cy="12" r="4" /> <path d="M12 2v2" /> <path d="M12 20v2" /> <path d="m4.93 4.93 1.41 1.41" /> <path d="m17.66 17.66 1.41 1.41" /> <path d="M2 12h2" /> <path d="M20 12h2" /> <path d="m6.34 17.66-1.41 1.41" /> <path d="m19.07 4.93-1.41 1.41" />';
    var MOON = '<path d="M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401" />';

    /**
     * Whether the page shows its dark theme: the choice made, else the system's.
     * @returns {boolean}
     */
    function isDark() {
        var t = root.getAttribute('data-theme');
        if (t === 'dark') return true;
        if (t === 'light') return false;
        return window.matchMedia('(prefers-color-scheme: dark)').matches;
    }

    /** Draws the icon of the theme a click leads to: the sun in dark, the moon in light. */
    function applyIcon() {
        var icon = document.getElementById('themeIcon');
        if (icon) icon.innerHTML = isDark() ? SUN : MOON;
    }

    /** Switches to the other theme, and keeps the choice for every page of the site. */
    function toggle() {
        root.setAttribute('data-theme', isDark() ? 'light' : 'dark');
        try {
            localStorage.setItem(KEY, root.getAttribute('data-theme'));
        } catch (e) { /* private mode: the choice lasts as long as the page */ }
        applyIcon();
    }

    try {
        var saved = localStorage.getItem(KEY);
        if (saved) root.setAttribute('data-theme', saved);
    } catch (e) { /* private mode: the system's appearance stands */ }

    var btn = document.getElementById('themeToggle');
    if (btn) btn.addEventListener('click', toggle);
    applyIcon();
})();
