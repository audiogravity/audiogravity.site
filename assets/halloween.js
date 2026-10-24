// Halloween on the landing, every 31 October by the visitor's own clock: bats over the hero and
// jack-o'-lanterns at the foot of the phone. Its look is in halloween.css.
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
        + '<filter id="hw-mist" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="16" /></filter>'
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

    // Mist, two banks of it: one between the far pumpkins and the near ones, one in front.
    var MIST_BACK = '<svg class="hw-fog hw-fog-back" viewBox="0 0 760 120"><g filter="url(#hw-mist)" fill="#d9cfc4">'
        + '<ellipse cx="120" cy="70" rx="200" ry="34" opacity=".14" />'
        + '<ellipse cx="420" cy="82" rx="240" ry="38" opacity=".11" />'
        + '<ellipse cx="650" cy="66" rx="190" ry="30" opacity=".14" /></g></svg>';
    var MIST_FRONT = '<svg class="hw-fog hw-fog-front" viewBox="0 0 760 80"><g filter="url(#hw-mist)" fill="#d9cfc4">'
        + '<ellipse cx="200" cy="44" rx="260" ry="22" opacity=".08" />'
        + '<ellipse cx="560" cy="48" rx="240" ry="20" opacity=".08" /></g></svg>';

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
    lay(hero, 'hw-sky hw-sky-top', bat(1) + bat(2, 'fast'));
    lay(panel, 'hw-sky hw-sky-panel', bat(3, 'slow') + bat(4) + bat(5) + bat(6, 'slow') + bat(7, 'fast'));
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
