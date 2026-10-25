// Halloween on the landing, every 31 October by the visitor's own clock: bats and spiders from
// the top of the page to its foot, webs in the hero's corners, jack-o'-lanterns at the foot of
// the phone and on the footer's edge, Danse macabre in the strip that shows a track playing, and
// a pumpkin in the tab's title. Its look is in halloween.css.
//
// Neither file is fetched on another day. The theme script in index.html's <head> decides —
// the date, or ?halloween in the address to preview it — sets html.halloween, and opens the
// page dark unless the visitor chose a theme with the button. The loader at the end of <body>
// then asks for the sheet, and for this script once the sheet is in, so that nothing is ever
// drawn unstyled.
//
// Everything built here is decoration: hidden from assistive technology, deaf to the pointer,
// and laid over the page rather than into it, so that the page reads and works as on any day.
// Three things are changed rather than built, the track in the strip, the title and, while the
// day's game runs, the news in the announce bar, and those are read as they show, a screen reader's
// "jack-o'-lantern" included. Two things are built to be used, real buttons named and reached
// like any other: the strip's play button, and the orange ghost of the day's game.
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
        // A ghost seen face on: a dome, a hem hanging in four tails, and eyes and a mouth cut out of
        // it — holes, so that the page shows through them. Its colour comes from where it is used.
        + '<symbol id="hw-ghost" viewBox="0 0 40 50"><path fill-rule="evenodd" d="M4 44V20A16 16 0 0 1 36 20V44'
        + 'Q32 50 28 44Q24 50 20 44Q16 50 12 44Q8 50 4 44Z'
        + 'M11 20a3 4.2 0 1 0 6 0a3 4.2 0 1 0-6 0Z'
        + 'M23 20a3 4.2 0 1 0 6 0a3 4.2 0 1 0-6 0Z'
        + 'M17 31a3 4 0 1 0 6 0a3 4 0 1 0-6 0Z" /></symbol>'
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
     * The style attribute of a piece that carries its own, nothing for one that does not.
     *
     * @param {string} [style] - Its inline style.
     * @returns {string} The attribute, with its leading space, or an empty string.
     */
    function inline(style) {
        return style ? ' style="' + style + '"' : '';
    }

    /**
     * One spider, coming down on its thread and climbing back, as hw-drop-<n> in halloween.css says.
     *
     * @param {number} n - Its number, which names its drop and its place.
     * @param {string} [style] - Its own delay, for the spiders that share a drop down the page.
     * @returns {string} The spider's markup, its thread drawn by the stylesheet.
     */
    function spider(n, style) {
        return '<div class="hw-spider hw-s' + n + '"' + inline(style) + '><div class="hw-sway">' + SPIDER + '</div></div>';
    }

    // A ghost, drawn once in DEFS (hw-ghost): every one down the page uses that drawing.
    var GHOST = '<svg viewBox="0 0 40 50"><use href="#hw-ghost" /></svg>';

    /**
     * One ghost, haunting the way hw-g<n> in halloween.css says.
     *
     * @param {number} n - Its number, which names its motion and its place.
     * @param {string} [style] - Its own delay, and the height it haunts (top), down the page.
     * @returns {string} The ghost's markup.
     */
    function ghost(n, style) {
        return '<div class="hw-ghost hw-g' + n + '"' + inline(style) + '>' + GHOST + '</div>';
    }

    /**
     * One bat, flying the path named after it in halloween.css.
     *
     * @param {number} n - Its number, which names its flight (hw-fly-b<n>) and its size.
     * @param {string} [pace] - 'fast' or 'slow' wings; a medium beat when omitted.
     * @param {string} [style] - Its own delay, and where its flight is laid (top), for the bats
     *     that share a flight down the page.
     * @returns {string} The bat's markup.
     */
    function bat(n, pace, style) {
        return '<div class="hw-bat hw-b' + n + '"' + inline(style) + '><div class="hw-bob' + (pace ? ' hw-' + pace : '') + '">'
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
    // The ghost between the two banks of mist, so that it rises from behind the near pumpkins.
    lay(phone, 'hw-ground', pumpkin('hw-pk-f1 hw-far', 'd') + pumpkin('hw-pk-f2 hw-far', 'd') + MIST_BACK
        + ghost(3) + pumpkin('hw-pk-c', 'c') + pumpkin('hw-pk-a', 'a') + pumpkin('hw-pk-b', 'b') + MIST_FRONT, true);
    lay(buttons, 'hw-cta-patch',
        pumpkin('hw-pk-cf hw-far', 'd') + pumpkin('hw-pk-cc', 'c') + pumpkin('hw-pk-ca', 'a'));

    // Down the page, every section but the figures that close "End the jitter" (one band with
    // it, no edge of their own): a bat across the band above the section's label, and in the
    // margins beside its text a spider let down from the section's top, and bats that come in
    // from the screen's edge, fly a loop and go back out — about one for each 900px of the
    // section, on alternate sides. A phone has no margins: its spider hangs in the band. Each
    // piece starts its loop at its own point, so that no two along the page move as one.
    var sections = [].filter.call(document.querySelectorAll('.section'), function (section) {
        return !section.classList.contains('rt-proof');
    });
    sections.forEach(function (section, i) {
        var delay = 'animation-delay:' + (-3.7 * (i + 1)).toFixed(1) + 's';
        var count = Math.max(1, Math.round(section.offsetHeight / 900));
        var margins = ['', ''];
        margins[i % 2] += spider(3, delay);
        // Below the spider, on its side, a ghost rising through the margin.
        margins[i % 2] += ghost(1, 'top:60%;animation-delay:' + (-4.1 * (i + 1)).toFixed(1) + 's');
        for (var j = 0; j < count; j++) {
            var perch = 'top:' + ((j + .5) / count * 100).toFixed(1) + '%;animation-delay:'
                + (-5.3 * (i + j + 1)).toFixed(1) + 's';
            margins[(i + j + 1) % 2] += j % 2 ? bat(9, 'slow', perch) : bat(8, '', perch);
        }
        lay(section, 'hw-sky hw-sky-top', spider(4, delay) + (i % 2 ? bat(2, 'fast', delay) : bat(1, '', delay)));
        lay(section, 'hw-sky hw-sky-margin hw-margin-l', margins[0]);
        lay(section, 'hw-sky hw-sky-margin hw-margin-r', margins[1]);
    });

    // The last scene: lit pumpkins standing on the footer's top edge, at the right of the text
    // column, with one more on its left on a wider screen; and, hung from that edge into the
    // footer's empty top, a last spider. Back to front, as at the foot of the phone.
    var footer = document.querySelector('footer');
    if (footer) {
        // The ghost first, so that it rises from behind the pumpkins.
        lay(footer, 'hw-foot', ghost(2) + pumpkin('hw-pk-ed', 'c') + pumpkin('hw-pk-ec hw-far', 'd')
            + pumpkin('hw-pk-eb', 'b') + pumpkin('hw-pk-ea', 'a'));
        lay(footer, 'hw-sky hw-sky-foot', spider(5));
    }

    // The strip that shows a track playing plays Danse macabre that day: its cover, its title,
    // how far it has got. The path and the format stay: they are the box's, not the record's —
    // except while the excerpt plays, when the strip shows the excerpt's own (listen).
    // The cover, 400 x 400 as the usual one, is asked for only now, the image being lazy.
    var strip = document.querySelector('.np-strip');
    if (strip) {
        var cover = strip.querySelector('.np-cover');
        cover.src = 'assets/pics/cover-danse-macabre.webp';
        cover.alt = 'Cover of Saint-Saëns: Danse macabre by Charles Dutoit';
        strip.querySelector('.track-name').textContent = 'Danse macabre';
        // No longer than the usual "The Beatles — Abbey Road": "Charles Dutoit" in full took a
        // second line on a 390px phone, where the usual line takes one (measured in Chromium).
        strip.querySelector('.track-artist').textContent = 'Saint-Saëns — C. Dutoit';
        // 6:55 in all, the recording's length: 3:33 played, 3:22 left, the bar 51.3% full.
        var progress = strip.querySelector('.np-progress');
        progress.setAttribute('aria-label', '3:33 played, 3:22 left');
        progress.firstElementChild.textContent = '3:33';
        progress.lastElementChild.textContent = progress.lastElementChild.textContent.replace(/\d+:\d\d/, '3:22');
        progress.querySelector('.fill').style.width = '51.3%';
        listen(progress);
    }

    /**
     * Lets the strip play what it shows: a round button beside the time plays an excerpt of the
     * recording, Apple's 30 s preview of the Decca album, asked for only at the first press. While
     * it plays, the strip tells the truth about what is heard: the excerpt's own format and its own
     * time, 0:00 to 0:30. Paused or over, it shows the box's again. An audiophile reading DSD256
     * over a browser's AAC preview would be right to feel misled. Never on its own: a browser plays
     * no sound before the visitor has pressed something, and the page would not want to. The
     * recording is protected (Decca, 1981): playing it that day is the site owner's decision, the
     * risk taken knowingly (2026-10-25). The button wears the carousel's own play and pause icons,
     * copied from it rather than drawn twice.
     *
     * @param {Element} progress - The strip's progress row: the time played, the bar, the time left.
     */
    function listen(progress) {
        var playIcon = document.querySelector('#heroPlay .ic-play');
        var pauseIcon = document.querySelector('#heroPlay .ic-pause');
        if (!playIcon || !pauseIcon) return;
        var played = progress.firstElementChild;
        var left = progress.lastElementChild;
        var fill = progress.querySelector('.fill');
        var values = [].slice.call(document.querySelectorAll('.np-fmt .cell b'));
        // What the box shows, put back when the excerpt stops; and what the excerpt is (ffprobe on
        // its file: AAC, 44,100 Hz, 262,603 b/s, 30.0 s).
        var box = {
            values: values.map(function (b) { return b.textContent; }),
            played: played.textContent,
            left: left.textContent,
            width: fill.style.width,
            label: progress.getAttribute('aria-label')
        };
        var heard = ['AAC', '44.1kHz', '263kbps', 'AAC'];
        var sound = null;
        var button = document.createElement('button');
        button.type = 'button';
        button.className = 'hw-np-play';
        button.appendChild(playIcon.cloneNode(true));
        button.appendChild(pauseIcon.cloneNode(true));
        // Beside the progress row, not in it: the row is an image to assistive technology, whose
        // content is not read, and a button there would be heard as nothing.
        var row = document.createElement('div');
        row.className = 'hw-np-row';
        progress.parentNode.insertBefore(row, progress);
        row.appendChild(button);
        row.appendChild(progress);

        var clock = function (s) {
            return Math.floor(s / 60) + ':' + ('0' + Math.floor(s % 60)).slice(-2);
        };
        var show = function (s, total) {
            played.textContent = clock(s);
            left.textContent = left.textContent.replace(/\d+:\d\d/, clock(total - s));
            fill.style.width = (100 * s / total).toFixed(1) + '%';
            progress.setAttribute('aria-label', clock(s) + ' played, ' + clock(total - s) + ' left');
        };
        // The strip as the excerpt is heard, from an element playing it; as the box shows it, from none.
        var hearing = function (element) {
            values.forEach(function (b, i) {
                b.textContent = element ? heard[i] : box.values[i];
            });
            if (element) {
                show(element.currentTime, element.duration || 30);
                return;
            }
            played.textContent = box.played;
            left.textContent = box.left;
            fill.style.width = box.width;
            progress.setAttribute('aria-label', box.label);
        };
        var state = function (playing) {
            button.classList.toggle('playing', playing);
            button.setAttribute('aria-label', playing ? 'Pause the excerpt' : 'Play an excerpt');
        };
        var fresh = function () {
            var element = new Audio('assets/audio/danse-macabre.m4a');
            element.addEventListener('timeupdate', function () {
                if (!element.paused) show(element.currentTime, element.duration || 30);
            });
            element.addEventListener('play', function () {
                state(true);
                hearing(element);
            });
            element.addEventListener('pause', function () {
                state(false);
                hearing(null);
            });
            // A load that failed, or a network lost on the way: the element stays failed, so the
            // next press starts again from a new one.
            element.addEventListener('error', function () {
                if (sound === element) sound = null;
                state(false);
                hearing(null);
            });
            return element;
        };
        state(false);

        button.addEventListener('click', function () {
            if (!sound) sound = fresh();
            if (!sound.paused) {
                sound.pause();
                return;
            }
            var started = sound.play();
            if (started && started.catch) started.catch(function () { state(false); });
        });
    }

    // The tab says it too: a pumpkin before the page's name. Not the site's icon, which a
    // browser may keep well past the day.
    document.title = String.fromCodePoint(0x1F383) + ' ' + document.title;

    // THE ORANGE GHOST, the day's game, run by the licence server (its routers/ghost.py): ten
    // licence keys wake through 31 October, Paris time, each at a secret instant, and the first
    // visitor to ask after one wakes is shown an orange ghost somewhere down the page, with
    // twenty minutes to catch it. The page asks once a visit and decides nothing: it can neither
    // make a ghost appear nor know a key before the server gives it. The rules are on
    // orange-ghost.html.
    var LICENCE_SERVER = location.hostname === 'audiogravity.app'
        ? 'https://lic.audiogravity.app:8443/ls/portal/'
        // Anywhere else, the page is a developer's copy: it asks the licence server beside it.
        : location.protocol + '//' + location.hostname + ':8100/ls/portal/';
    var KEY = /^AG(-[A-Z0-9]{4}){4}$/;
    var KEPT = 'ag-orange-ghost';
    hunt();

    /**
     * Asks the licence server whether the game is on and whether a ghost is here for this
     * visitor, words the banner from the answer, and hides the ghost when there is one. A visitor
     * who caught one this year on this device is offered their key again, and asks nothing.
     */
    function hunt() {
        var mine = kept();
        if (mine) {
            announce('You caught an orange ghost: show your licence key', 'Show your licence key', function () {
                reveal(mine);
            });
            return;
        }
        ask('ghost-draw').then(function (answer) {
            var left = parseInt(answer.data.left, 10) || 0;
            if (answer.data.state === 'open' && left > 0) {
                announce('Find the orange ghost on this page today: ' + left
                    + (left === 1 ? ' lifetime licence' : ' lifetime licences') + ' left to win',
                    'Find the orange ghost');
                if (answer.data.ghost && answer.data.ghost.ticket) haunt(answer.data.ghost);
            } else if (answer.data.state === 'over') {
                announce('Every orange ghost has been caught. Thank you for hunting!', 'All the ghosts are caught');
            }
        }, function () {});
    }

    /**
     * Asks the licence server one of the game's two questions.
     *
     * @param {string} route - 'ghost-draw' or 'ghost-claim'.
     * @param {Object} [body] - What the question sends, as JSON.
     * @returns {Promise<{status: number, data: Object}>} The answer's status, and its JSON (empty
     *     when it carries none); rejected when the server cannot be reached in time.
     */
    function ask(route, body) {
        var options = { method: 'POST' };
        if (body) {
            options.headers = { 'Content-Type': 'application/json' };
            options.body = JSON.stringify(body);
        }
        // A server that does not answer must not keep the page waiting: the game is just not there.
        if (window.AbortSignal && AbortSignal.timeout) options.signal = AbortSignal.timeout(8000);
        return fetch(LICENCE_SERVER + route, options).then(function (response) {
            return response.json().then(null, function () {
                return {};
            }).then(function (data) {
                return { status: response.status, data: data || {} };
            });
        });
    }

    /**
     * Writes the game's news in the announce bar, where it takes turns with the release's sentence,
     * with the page's own writer of that news (window.agAnnounce, in index.html): its badge, a
     * sentence, and where a press leads — the rules, or the visitor's own key.
     *
     * @param {string} sentence - What it says.
     * @param {string} short - The same for a phone, whose bar holds one line.
     * @param {Function} [open] - What a press does instead of leading to the rules.
     */
    function announce(sentence, short, open) {
        if (!window.agAnnounce) return;
        window.agAnnounce({ badge: 'HALLOWEEN', sentence: sentence, short: short, href: 'orange-ghost.html', open: open });
    }

    /**
     * Hides the orange ghost in the band at the top of a section taken at random, somewhere
     * along it: the band the bats and the spiders use, above every label. It stays there as long
     * as the ticket the server gave with it lasts, counted from now rather than read off the
     * visitor's clock, which may be wrong by any amount. Caught, it trades the ticket for the key.
     *
     * @param {{ticket: string, ttl: number}} ghost - The server's ticket, and the seconds it lasts.
     */
    function haunt(ghost) {
        var section = sections[Math.floor(Math.random() * sections.length)];
        if (!section) return;
        var button = document.createElement('button');
        button.type = 'button';
        button.className = 'hw-orange';
        button.setAttribute('aria-label', 'An orange ghost: catch it to win a lifetime licence');
        button.style.left = 'calc(' + (6 + Math.random() * 88).toFixed(1) + '% - 22px)';
        button.innerHTML = GHOST;
        section.appendChild(button);
        var lapse = setTimeout(function () {
            button.remove();
        }, Math.max(0, +ghost.ttl || 0) * 1000);
        button.addEventListener('click', function () {
            if (button.getAttribute('aria-disabled') === 'true') return;
            button.setAttribute('aria-disabled', 'true');
            ask('ghost-claim', { ticket: ghost.ticket }).then(function (answer) {
                clearTimeout(lapse);
                button.remove();
                var mine = { key: answer.data.key, year: new Date().getFullYear() };
                if (answer.status === 200 && KEY.test(mine.key || '')) {
                    try {
                        localStorage.setItem(KEPT, JSON.stringify(mine));
                    } catch (e) { /* refused storage: the key is shown this once */ }
                    announce('You caught an orange ghost: show your licence key', 'Show your licence key', function () {
                        reveal(mine);
                    });
                    reveal(mine);
                } else {
                    tell(answer.status === 409
                        ? 'One ghost per visitor: you caught one already today.'
                        : 'Too late: this ghost has vanished. Another one may wake later today.');
                }
            }, function () {
                // No answer, though the server may have given the key on its side: the ghost
                // stays, past its time if need be, since the same ticket gives the same key again.
                clearTimeout(lapse);
                button.removeAttribute('aria-disabled');
                tell('The licence server did not answer. The ghost is still there: try again in a moment.');
            });
        });
    }

    /**
     * The key this device caught, kept so that a reload shows it again, for this year's game
     * only. Storage may be refused (private browsing): the key was then shown once, when caught.
     *
     * @returns {?{key: string, year: number}} The key and its year, or null.
     */
    function kept() {
        try {
            var mine = JSON.parse(localStorage.getItem(KEPT));
            return mine && mine.year === new Date().getFullYear() && KEY.test(mine.key) ? mine : null;
        } catch (e) {
            return null;
        }
    }

    /**
     * Opens a window over the page, closed by its button or by Escape: a <dialog>, which keeps
     * the focus inside while it is open and gives it back on closing. A browser without one
     * (Safari before 15.4) is told the same in a plain message: a winner must see the key,
     * whatever the browser.
     *
     * @param {string} label - Its name, for assistive technology.
     * @param {string} html - Its content, the page's own words only.
     * @param {function(HTMLDialogElement)} fill - Sets in it what comes from the server, as text.
     * @param {string} plain - What it says, as plain text, for a browser without <dialog>.
     */
    function windowOf(label, html, fill, plain) {
        var dialog = document.createElement('dialog');
        if (typeof dialog.showModal !== 'function') {
            window.alert(plain);
            return;
        }
        dialog.className = 'hw-catch';
        dialog.setAttribute('aria-label', label);
        dialog.innerHTML = html + '<form method="dialog"><button class="hw-catch-close">Close</button></form>';
        fill(dialog);
        dialog.addEventListener('close', function () {
            dialog.remove();
        });
        document.body.appendChild(dialog);
        dialog.showModal();
    }

    /**
     * Shows the key the visitor caught, how to activate it, and the rules.
     *
     * @param {{key: string}} mine - The key.
     */
    function reveal(mine) {
        windowOf('Your lifetime licence', '<h2>You caught the orange ghost!</h2>'
            + '<p>Your lifetime Audiogravi<sup>ty</sup> licence:</p>'
            + '<p class="hw-catch-key"><code></code><button type="button" class="hw-catch-copy">Copy</button></p>'
            + '<ol><li>In Audiogravi<sup>ty</sup>, open the <b>Admin</b> tab.</li>'
            + '<li>Tap <b>LICENSE KEY</b>, at the top of the licence panel, and paste the key.</li>'
            + '<li>Tap <b>CHECK KEY</b>, then <b>ACTIVATE THIS MACHINE</b>.</li></ol>'
            + '<p class="hw-catch-note">The key works once: the first box to activate it keeps it, so keep'
            + ' it to yourself. No box yet? It will wait for you, and this page keeps it on this device.</p>'
            + '<p class="hw-catch-note"><a href="orange-ghost.html">The rules</a> · '
            + '<a href="mailto:orange-ghost@audiogravity.app">orange-ghost@audiogravity.app</a></p>',
        function (dialog) {
            dialog.querySelector('code').textContent = mine.key;
            var copy = dialog.querySelector('.hw-catch-copy');
            copy.addEventListener('click', function () {
                if (!navigator.clipboard) return;
                navigator.clipboard.writeText(mine.key).then(function () {
                    copy.textContent = 'Copied';
                }, function () {});
            });
        },
        // Plain text: the brand as an attribute writes it, there being no markup to raise "ty".
        'You caught the orange ghost! Your lifetime Audiogravity licence key:\n\n' + mine.key
            + '\n\nIn Audiogravity, open the Admin tab, tap LICENSE KEY and paste the key, then tap'
            + ' CHECK KEY and ACTIVATE THIS MACHINE. The key works once: keep it to yourself.');
    }

    /**
     * Says one sentence about the game in a window: a ghost gone, or a server that did not answer.
     *
     * @param {string} sentence - What it says.
     */
    function tell(sentence) {
        windowOf('The orange ghost', '<p></p>', function (dialog) {
            dialog.querySelector('p').textContent = sentence;
        }, sentence);
    }

    // Nothing moves in a part of the page scrolled out of sight: the hero, a section, the footer.
    // The screen is taken 120px taller at its foot: the pumpkins on the footer's edge stand
    // above the footer, their glow higher still, and froze in sight while the footer itself was
    // just under the screen.
    if ('IntersectionObserver' in window) {
        var rest = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                entry.target.classList.toggle('hw-paused', !entry.isIntersecting);
            });
        }, { rootMargin: '0px 0px 120px 0px' });
        var parts = [hero].concat(sections);
        if (footer) parts.push(footer);
        parts.forEach(function (part) {
            rest.observe(part);
        });
    }
})();
