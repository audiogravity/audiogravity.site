// Halloween on the landing, every 31 October by the visitor's own clock: bats over the hero,
// spiders coming down on their threads, webs in the corners and jack-o'-lanterns at the foot of
// the phone. Its look is in halloween.css.
//
// Neither file is fetched on another day. The theme script in index.html's <head> decides —
// the date, or ?halloween in the address to preview it — sets html.halloween, and opens the
// page dark unless the visitor chose a theme with the button. The loader at the end of <body>
// then asks for the sheet, and for this script once the sheet is in, so that nothing is ever
// drawn unstyled.
//
// Everything built here is decoration: hidden from assistive technology, deaf to the pointer,
// and laid over the page rather than into it, so that the page reads and works as on any day.
(function () {
    var root = document.documentElement;
    var hero = document.querySelector('.hero');
    var panel = hero && hero.querySelector('.hero-right');
    var phone = panel && panel.querySelector('.hero-carousel');
    var buttons = hero && hero.querySelector('.hero-cta');
    if (!root.classList.contains('halloween') || !phone || !buttons) return;

    // Shapes drawn more than once, defined once (the same reasoning as the page's icon sprite).
    // Gradients rather than blur filters wherever a shape only has to glow, which costs nothing.
    var DEFS = '<svg class="hw-decor" aria-hidden="true" style="position:absolute;width:0;height:0;overflow:hidden">'
        + '<defs>'
        + '<radialGradient id="hw-flame" cx="50%" cy="58%" r="62%">'
        + '<stop offset="0%" stop-color="#fff4cf" /><stop offset="38%" stop-color="#ffd36b" />'
        + '<stop offset="72%" stop-color="#ff9a2e" /><stop offset="100%" stop-color="#c9500c" /></radialGradient>'
        + '<radialGradient id="hw-rib" cx="50%" cy="62%" r="62%">'
        + '<stop offset="0%" stop-color="#5c2a0d" /><stop offset="55%" stop-color="#2e1406" />'
        + '<stop offset="100%" stop-color="#100602" /></radialGradient>'
        + '<radialGradient id="hw-halo" cx="50%" cy="50%" r="50%">'
        + '<stop offset="0%" stop-color="#ff9b3d" stop-opacity=".42" />'
        + '<stop offset="55%" stop-color="#ff8a2a" stop-opacity=".12" />'
        + '<stop offset="100%" stop-color="#ff8a2a" stop-opacity="0" /></radialGradient>'
        + '<radialGradient id="hw-ground" cx="50%" cy="50%" r="50%">'
        + '<stop offset="0%" stop-color="#ff8a2a" stop-opacity=".4" />'
        + '<stop offset="100%" stop-color="#ff8a2a" stop-opacity="0" /></radialGradient>'
        // Its region spans three deviations past either bank (see MIST_BACK).
        + '<filter id="hw-mist" x="-20%" y="-110%" width="140%" height="320%"><feGaussianBlur stdDeviation="16" /></filter>'
        + '<g id="hw-body">'
        + '<ellipse cx="58" cy="100" rx="50" ry="62" fill="url(#hw-rib)" />'
        + '<ellipse cx="142" cy="100" rx="50" ry="62" fill="url(#hw-rib)" />'
        + '<ellipse cx="78" cy="101" rx="42" ry="66" fill="url(#hw-rib)" />'
        + '<ellipse cx="122" cy="101" rx="42" ry="66" fill="url(#hw-rib)" />'
        + '<ellipse cx="100" cy="101" rx="33" ry="67" fill="url(#hw-rib)" />'
        + '<path d="M92 40 C90 26 96 14 108 9 C112 13 108 24 108 40 Z" fill="#24170a" /></g>'
        // Triangle eyes and nose, a toothy grin.
        + '<g id="hw-face-a"><path d="M54 88 L92 80 L76 52 Z" /><path d="M108 80 L146 88 L124 52 Z" />'
        + '<path d="M92 108 L108 108 L100 92 Z" />'
        + '<path d="M40 112 L52 123 L59 112 L69 127 L79 114 L89 129 L100 116 L111 129 L121 114 L131 127 L141 112 L148 123'
        + ' L160 112 C152 142 130 156 112 156 L106 143 L100 156 L94 143 L88 156 C70 156 48 142 40 112 Z" /></g>'
        // Round eyes and a long stitched smile; the stitches are drawn over it (hw-teeth-b).
        + '<g id="hw-face-b"><ellipse cx="74" cy="76" rx="17" ry="21" /><ellipse cx="126" cy="76" rx="17" ry="21" />'
        + '<path d="M94 98 L99 107 L93 107 Z" /><path d="M106 98 L107 107 L101 107 Z" />'
        + '<path d="M36 104 C60 144 140 144 164 104 C140 130 60 130 36 104 Z" /></g>'
        + '<path id="hw-teeth-b" fill="none" stroke="#140802" stroke-width="3" d="M50 112 L48 122 M60 116 L59 128'
        + ' M70 119 L69 131 M80 121 L80 134 M90 122 L90 136 M100 123 L100 137 M110 122 L110 136 M120 121 L120 134'
        + ' M130 119 L131 131 M140 116 L141 128 M150 112 L152 122" />'
        // Angry slits and fangs.
        + '<g id="hw-face-c"><path d="M50 66 L94 84 L82 95 L58 85 Z" /><path d="M150 66 L106 84 L118 95 L142 85 Z" />'
        + '<path d="M93 102 L107 102 L100 113 Z" />'
        + '<path d="M58 122 C78 134 122 134 142 122 L136 132 L128 125 L120 137 L111 128 L100 140 L89 128 L80 137'
        + ' L72 125 L64 132 Z" /></g>'
        // The far one: two triangles and an open mouth, all that the distance leaves.
        + '<g id="hw-face-d"><path d="M62 84 L90 84 L77 62 Z" /><path d="M110 84 L138 84 L123 62 Z" />'
        + '<ellipse cx="100" cy="122" rx="22" ry="14" /></g>'
        + '</defs></svg>';

    // A bat seen from below, its wings pivoting about the shoulders (54,28) and (66,28).
    var BAT = '<path class="hw-wing-l" d="M54 24 C44 10 26 4 6 12 C11 16 13 22 12 28 C18 24 25 25 28 31'
        + ' C33 26 40 27 43 33 C47 29 51 30 54 34 Z" />'
        + '<path class="hw-wing-r" d="M66 24 C76 10 94 4 114 12 C109 16 107 22 108 28 C102 24 95 25 92 31'
        + ' C87 26 80 27 77 33 C73 29 69 30 66 34 Z" />'
        + '<ellipse cx="60" cy="34" rx="7" ry="12" />'
        + '<path d="M53 23 L54 12 L58 18 L62 18 L66 12 L67 23 C67 28 53 28 53 23 Z" />';

    // Mist, two banks of it: one between the far pumpkins and the near ones, one in front. Drawn
    // in a frame 760 wide, but each viewBox reaches three deviations of the blur past its banks,
    // where the blur has faded out: an svg cuts what it draws at its own edges, and a cut through
    // the blur shows as a straight edge. halloween.css places each box from its viewBox.
    var MIST_BACK = '<svg class="hw-fog hw-fog-back" viewBox="-130 -14 1020 184"><g filter="url(#hw-mist)" fill="#d9cfc4">'
        + '<ellipse cx="120" cy="70" rx="200" ry="34" opacity=".14" />'
        + '<ellipse cx="420" cy="82" rx="240" ry="38" opacity=".11" />'
        + '<ellipse cx="650" cy="66" rx="190" ry="30" opacity=".14" /></g></svg>';
    var MIST_FRONT = '<svg class="hw-fog hw-fog-front" viewBox="-110 -28 960 146"><g filter="url(#hw-mist)" fill="#d9cfc4">'
        + '<ellipse cx="200" cy="44" rx="260" ry="22" opacity=".08" />'
        + '<ellipse cx="560" cy="48" rx="240" ry="20" opacity=".08" /></g></svg>';

    // A corner web, its corner at the top left: seven threads from the corner, and seven turns of
    // the spiral sagging toward it between each pair. The other corner is the same web mirrored.
    var WEB = '<svg viewBox="0 0 200 200"><path d="M0 0L199.9 5.2M0 0L188.4 54.0M0 0L168.0 100.9M0 0L133.7 143.3'
        + 'M0 0L92.0 173.1M0 0L47.4 190.2M0 0L5.2 199.9M21.7 0.6Q18.2 2.8 20.6 5.9Q17.1 7.4 19.1 11.5Q14.4 11.7 14.5 15.5'
        + 'Q10.7 15.0 10.4 19.5Q6.7 17.5 5.3 21.1Q2.5 18.2 0.6 21.2M42.0 1.1Q34.8 5.4 38.9 11.1Q32.1 14.0 35.8 21.5'
        + 'Q27.2 22.1 27.7 29.7Q20.1 28.2 19.1 35.9Q12.6 32.8 10.1 40.5Q4.9 35.9 1.1 43.1M62.1 1.6Q52.6 8.1 60.2 17.3'
        + 'Q49.7 21.6 55.4 33.3Q43.3 35.1 45.2 48.5Q32.4 45.4 30.2 56.9Q19.6 50.9 15.4 61.6Q7.5 55.0 1.7 66.4'
        + 'M84.8 2.2Q73.9 11.4 87.0 25.0Q69.2 30.1 74.2 44.6Q56.9 46.1 58.3 62.5Q42.3 59.3 40.1 75.3Q26.3 68.5 21.0 84.1'
        + 'Q10.2 74.9 2.4 90.2M111.1 2.9Q95.2 14.7 110.3 31.6Q89.9 39.1 98.8 59.4Q75.5 61.1 77.0 82.5Q56.3 78.9 53.7 101.0'
        + 'Q34.3 89.4 26.6 106.7Q12.7 93.2 2.9 109.9M138.6 3.6Q119.2 18.3 138.5 39.7Q111.5 48.5 121.0 72.7Q93.0 75.3 95.4 102.3'
        + 'Q70.0 98.2 67.1 126.2Q43.5 113.3 34.2 137.3Q16.2 119.1 3.7 139.7M176.0 4.6Q147.9 22.8 168.0 48.2Q134.2 58.3 144.4 86.8'
        + 'Q113.0 91.5 118.0 126.5Q85.5 119.9 80.9 152.2Q53.5 139.3 42.9 171.9Q20.3 149.2 4.6 175.1" /></svg>';

    // A spider hanging head down, as one coming down its thread does: the abdomen to the thread at
    // the top, the head below, eight legs bent at the knee.
    var SPIDER = '<svg viewBox="0 0 40 44"><g class="hw-legs" fill="none" stroke-width="1.6" stroke-linecap="round"'
        + ' stroke-linejoin="round"><path d="M16 17 L8 9 L3 2" /><path d="M15 20 L6 16 L1 13" />'
        + '<path d="M15 24 L6 27 L2 33" /><path d="M16 27 L9 34 L6 42" /><path d="M24 17 L32 9 L37 2" />'
        + '<path d="M25 20 L34 16 L39 13" /><path d="M25 24 L34 27 L38 33" /><path d="M24 27 L31 34 L34 42" /></g>'
        + '<ellipse cx="20" cy="13" rx="6.5" ry="8" /><circle cx="20" cy="26" r="4.6" /></svg>';

    /**
     * One spider, coming down on its thread and climbing back, as hw-drop-<n> in halloween.css says.
     *
     * @param {number} n - Its number, which names its drop and its place.
     * @returns {string} The spider's markup, its thread drawn by the stylesheet.
     */
    function spider(n) {
        return '<div class="hw-spider hw-s' + n + '"><div class="hw-sway">' + SPIDER + '</div></div>';
    }

    /**
     * One bat, flying the path named after it in halloween.css.
     *
     * @param {number} n - Its number, which names its flight (hw-fly-b<n>) and its size.
     * @param {string} [pace] - 'fast' or 'slow' wings; a medium beat when omitted.
     * @returns {string} The bat's markup.
     */
    function bat(n, pace) {
        return '<div class="hw-bat hw-b' + n + '"><div class="hw-bob' + (pace ? ' hw-' + pace : '') + '">'
            + '<svg viewBox="0 0 120 64">' + BAT + '</svg></div></div>';
    }

    /**
     * One jack-o'-lantern, in three layers: the halo behind, the body, the lit face in front.
     *
     * @param {string} place - Its classes: where it sits (hw-pk-*), and hw-far for a distant one.
     * @param {string} face - Which face, 'a' to 'd' (hw-face-<face>).
     * @returns {string} The pumpkin's markup.
     */
    function pumpkin(place, face) {
        return '<span class="hw-pumpkin ' + place + '">'
            + '<svg class="hw-halo" viewBox="0 0 200 170"><circle cx="100" cy="100" r="170" fill="url(#hw-halo)" />'
            + '<ellipse cx="100" cy="166" rx="92" ry="10" fill="url(#hw-ground)" /></svg>'
            + '<svg viewBox="0 0 200 170"><use href="#hw-body" /></svg>'
            + '<svg class="hw-lit" viewBox="0 0 200 170"><use href="#hw-face-' + face + '" fill="url(#hw-flame)" />'
            + (face === 'b' ? '<use href="#hw-teeth-b" />' : '') + '</svg></span>';
    }

    /**
     * Lays a piece of the decoration at the end of an element of the page, or just after it.
     *
     * @param {Element} element - Where it goes.
     * @param {string} classes - Its classes, after hw-decor.
     * @param {string} inner - Its content.
     * @param {boolean} [after] - True to place it after the element rather than inside.
     */
    function lay(element, classes, inner, after) {
        element.insertAdjacentHTML(after ? 'afterend' : 'beforeend',
            '<div class="hw-decor ' + classes + '" aria-hidden="true">' + inner + '</div>');
    }

    document.body.insertAdjacentHTML('beforeend', DEFS);
    lay(hero, 'hw-web hw-web-page', WEB);
    lay(hero, 'hw-sky hw-sky-top', bat(1) + bat(2, 'fast'));
    // The web first, so that the spiders and the bats go in front of it.
    lay(panel, 'hw-web hw-web-panel', WEB);
    lay(panel, 'hw-sky hw-sky-panel', spider(1) + spider(2)
        + bat(3, 'slow') + bat(4) + bat(5) + bat(6, 'slow') + bat(7, 'fast'));
    // Just under the phone, back to front: the far ones, the mist between, then the near ones
    // and the mist before them.
    lay(phone, 'hw-ground', pumpkin('hw-pk-f1 hw-far', 'd') + pumpkin('hw-pk-f2 hw-far', 'd') + MIST_BACK
        + pumpkin('hw-pk-c', 'c') + pumpkin('hw-pk-a', 'a') + pumpkin('hw-pk-b', 'b') + MIST_FRONT, true);
    lay(buttons, 'hw-cta-patch',
        pumpkin('hw-pk-cf hw-far', 'd') + pumpkin('hw-pk-cc', 'c') + pumpkin('hw-pk-ca', 'a'));

    // Nothing moves while the hero is out of sight: it is the only place the decoration is.
    if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (entries) {
            root.classList.toggle('hw-paused', !entries[0].isIntersecting);
        }).observe(hero);
    }
})();
