// Christmas on the landing, every 24 and 25 December by the visitor's own clock: at the foot of
// the phone a cartoon scene standing in the snow — a decorated tree whose bulbs blink, an elf
// carrying a present, a snowman, an elf waving, a penguin and a polar bear — snow falling around
// the phone, baubles swinging on red ribbons, holly in two corners, stars in the dark, Santa's
// sleigh crossing the band above the first line now and then, and a fir tree in the tab's
// title. Its look is in christmas.css; the figures, the sleigh and the snow are drawn once each
// in assets/christmas/.
//
// Neither file is fetched on another day, nor are the drawings. The theme script in
// index.html's <head> decides — the date, or ?christmas in the address to preview it — sets
// html.christmas, and opens the page dark unless the visitor chose a theme with the button.
// The loader at the end of <body> then asks for the sheet, and for this script once the sheet
// is in, so that nothing is ever drawn unstyled.
//
// Everything built here is decoration: hidden from assistive technology, deaf to the pointer,
// and laid over the page rather than into it, so that the page reads and works as on any day.
// Three things are changed rather than built, the track in the strip, the title and, while the
// day's game runs, the news in the announce bar, and those are read as they show. Two things are
// built to be used, real buttons named and reached like any other: the strip's play button, and
// the gold gift of the day's game.
(function () {
    var root = document.documentElement;
    var page = agDays.parts();
    if (!root.classList.contains('christmas') || !page) return;
    var hero = page.hero;
    var panel = page.panel;
    var phone = page.phone;
    var buttons = page.buttons;

    var FIGURES = 'assets/christmas/';

    // The tree's bulbs, in the tree's own frame (120 x 160): where each hangs, and its colour.
    // Every fourth one makes a set, and the four sets blink apart.
    var BULBS = [[32, 113.6, '#ff4d5e'], [44, 118, '#ffd23f'], [56, 120, '#4da3ff'], [68, 119.4, '#5ce08a'],
        [80, 116.3, '#ff4d5e'], [90, 111, '#ffd23f'], [41, 80.8, '#4da3ff'], [52, 84, '#5ce08a'],
        [63, 84.6, '#ff4d5e'], [75, 81.4, '#ffd23f'], [84, 76.2, '#4da3ff'], [50, 46.4, '#ffd23f'],
        [60, 47.2, '#ff4d5e'], [70, 43.4, '#5ce08a']];

    /**
     * One set of the tree's bulbs: each a coloured bead in a warm glow, with a glint.
     *
     * @param {number} set - Which set, 0 to 3: the bulbs whose place in BULBS leaves that remainder by 4.
     * @returns {string} The bulbs' markup.
     */
    function bulbs(set) {
        return BULBS.filter(function (bulb, i) {
            return i % 4 === set;
        }).map(function (bulb) {
            return '<circle cx="' + bulb[0] + '" cy="' + bulb[1] + '" r="5" fill="url(#xc-glow)" />'
                + '<circle cx="' + bulb[0] + '" cy="' + bulb[1] + '" r="2.6" fill="' + bulb[2] + '" />'
                + '<circle cx="' + (bulb[0] - .7).toFixed(1) + '" cy="' + (bulb[1] - .8).toFixed(1) + '" r=".8" fill="#fff" opacity=".8" />';
        }).join('');
    }

    // Shapes drawn more than once, defined once (the same reasoning as the page's icon sprite):
    // the bulbs and their glow, a star, and the snow banks' colours.
    var DEFS = '<svg class="xm-decor" aria-hidden="true" style="position:absolute;width:0;height:0;overflow:hidden">'
        + '<defs>'
        + '<radialGradient id="xc-glow"><stop offset="0" stop-color="#fff1b8" stop-opacity=".95" />'
        + '<stop offset=".45" stop-color="#ffc35a" stop-opacity=".4" /><stop offset="1" stop-color="#ffb347" stop-opacity="0" />'
        + '</radialGradient>'
        // The snow banks: lit from above, bluer below; the dark theme's a shade darker.
        + '<linearGradient id="xm-bank-light" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7fafd" />'
        + '<stop offset=".5" stop-color="#e4ebf3" /><stop offset="1" stop-color="#d0dbe7" /></linearGradient>'
        + '<linearGradient id="xm-bank-dark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eef3f9" />'
        + '<stop offset=".5" stop-color="#cbd7e5" /><stop offset="1" stop-color="#a3b3c7" /></linearGradient>'
        // The mound at the end of the buttons fades into the page below it.
        + '<linearGradient id="xm-mound" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eef3f9" />'
        + '<stop offset=".45" stop-color="#cbd7e5" stop-opacity=".9" /><stop offset="1" stop-color="#a3b3c7" stop-opacity="0" />'
        + '</linearGradient>'
        + '<g id="xc-b0">' + bulbs(0) + '</g><g id="xc-b1">' + bulbs(1) + '</g>'
        + '<g id="xc-b2">' + bulbs(2) + '</g><g id="xc-b3">' + bulbs(3) + '</g>'
        + '<path id="xc-star" d="M0-6L1.6-2.3L5.7-1.9L2.7.9L3.5 4.9L0 2.8L-3.5 4.9L-2.7.9L-5.7-1.9L-1.6-2.3Z" fill="#ffd23f"'
        + ' stroke="#ffd23f" stroke-width="1.6" stroke-linejoin="round" />'
        + '</defs></svg>';

    // The bank at the foot of the phone: its top line, in a frame 1000 x 60 that christmas.css
    // stretches across 400% of the phone, from 150% left of it, so that it reaches both edges of
    // the widest panel; higher where the figures stand (frame 250-370 and 630-740), lower under
    // the phone (375-625).
    var BANK_LINE = 'M0 34C6.7 34 26.7 33.8 40 33.7C53.3 33.7 66.7 33.6 80 33.5C93.3 33.4 106.7 33.2 120 33.1'
        + 'C133.3 33 146.7 33.3 160 32.9C173.3 32.5 186.7 31.5 200 30.7C213.3 30 226.7 29.4 240 28.3'
        + 'C253.3 27.3 266.7 24.8 280 24.3C293.3 23.9 306.7 25.2 320 25.8C333.3 26.5 346.7 27.7 360 28.1'
        + 'C373.3 28.5 386.7 28 400 28C413.3 28 426.7 28.4 440 28.1C453.3 27.9 466.7 26.7 480 26.5'
        + 'C493.3 26.4 506.7 27 520 27.1C533.3 27.2 546.7 26.9 560 27.1C573.3 27.2 586.7 27.9 600 27.9'
        + 'C613.3 27.8 626.7 27.5 640 26.6C653.3 25.8 666.7 23 680 22.7C693.3 22.3 706.7 23.8 720 24.5'
        + 'C733.3 25.2 746.7 26 760 26.9C773.3 27.9 786.7 29.4 800 30.2C813.3 31 826.7 31.5 840 31.7'
        + 'C853.3 31.9 866.7 31.2 880 31.4C893.3 31.6 906.7 32.9 920 33.1C933.3 33.3 946.7 32.6 960 32.7'
        + 'C973.3 32.9 993.3 33.8 1000 34';
    var BANK = '<svg viewBox="0 0 1000 60" preserveAspectRatio="none">'
        + '<path class="xm-bank" d="M0 60L' + BANK_LINE.slice(1) + 'L1000 60Z" />'
        + '<path class="xm-bank-edge" d="' + BANK_LINE + '" /></svg>';

    // The mound under the figures at the end of the buttons, in a frame 170 x 40.
    var MOUND_LINE = 'M6 36C8 35.4 14 33.6 18 32.4C22 31.2 26 29.6 30 28.7C34 27.8 38 27.3 42 27.2C46 27 50 28.1 54 27.7'
        + 'C58 27.4 62 25.3 66 24.9C70 24.5 74 25.2 78 25.3C82 25.4 86 25.9 90 25.5C94 25.2 98 23.5 102 23.1'
        + 'C106 22.7 110 23.3 114 23.2C118 23.1 122 22.5 126 22.4C130 22.3 134 21.9 138 22.7C142 23.4 146 25 150 26.9'
        + 'C154 28.9 159.3 32.7 162 34.2C164.7 35.8 165.3 35.7 166 36';
    var MOUND = '<svg viewBox="0 0 170 40">'
        + '<path fill="url(#xm-mound)" d="M6 40L' + MOUND_LINE.slice(1) + 'L166 40Z" />'
        + '<path class="xm-bank-edge" d="' + MOUND_LINE + '" /></svg>';

    /**
     * One figure, a drawing of assets/christmas/ in an image of its own.
     *
     * @param {string} name - The drawing's file name, without its extension.
     * @param {string} classes - Where it stands, and how it moves (christmas.css).
     * @param {string} [style] - Its own delay, for those that share a move down the page.
     * @returns {string} The figure's markup.
     */
    function figure(name, classes, style) {
        return '<img class="xm-fig ' + classes + '" src="' + FIGURES + name + '.svg" alt="" decoding="async"'
            + (style ? ' style="' + style + '"' : '') + '>';
    }

    /**
     * The decorated tree: its drawing, and its bulbs over it in four sets that blink apart, each
     * set a picture of its own, so that the browser fades it without drawing it again.
     *
     * @param {string} place - Where it stands (christmas.css).
     * @returns {string} The tree's markup.
     */
    function tree(place) {
        var sets = '';
        for (var set = 0; set < 4; set++) {
            sets += '<svg class="xm-tw xm-tw' + (set + 1) + '" viewBox="0 0 120 160"><use href="#xc-b' + set + '" /></svg>';
        }
        return '<span class="xm-fig xm-treebox ' + place + '"><img src="' + FIGURES + 'tree.svg" alt="" decoding="async">'
            + sets + '</span>';
    }

    /**
     * One bauble on its red ribbon, hung from the top of the box it is laid in.
     *
     * @param {string} place - Where it hangs and how it swings (christmas.css).
     * @param {string} colour - Which drawing: 'red', 'gold' or 'blue'.
     * @param {number} [ribbon] - Its ribbon's length in px, for the baubles down the page, each its own.
     * @param {string} [swing] - Its own delay, for those that share a swing down the page.
     * @returns {string} The bauble's markup.
     */
    function bauble(place, colour, ribbon, swing) {
        return '<div class="xm-hang ' + place + '"' + (swing ? ' style="' + swing + '"' : '') + '>'
            + '<div class="xm-ribbon"' + (ribbon ? ' style="height:' + ribbon + 'px"' : '') + '></div>'
            + '<img src="' + FIGURES + 'bauble-' + colour + '.svg" alt="" decoding="async"'
            + (ribbon ? ' style="top:' + (ribbon - 1) + 'px"' : '') + '></div>';
    }

    // The panel's snow: two planes of it, far then near, each a tile of cartoon snow that the
    // stylesheet repeats across the panel and moves down. Two pieces that move, not a piece per
    // flake: 48 flakes with a fall and a sway each kept the page far busier (christmas.css).
    var SNOW = '<div class="xm-snow">'
        + '<div class="xm-plane xm-far" style="background-image:url(' + FIGURES + 'snow-far.svg)"></div>'
        + '<div class="xm-plane xm-near" style="background-image:url(' + FIGURES + 'snow-near.svg)"></div></div>';

    var STARS = '<div class="xm-stars">' + [1, 2, 3, 4, 5, 6, 7].map(function (n) {
        return '<svg class="xm-star xm-st' + n + '" viewBox="-8 -8 16 16"><use href="#xc-star" /></svg>';
    }).join('') + '</div>';

    // Lays a piece of the decoration at the end of an element of the page, or just after it,
    // hidden from assistive technology (days.js, lay): lay(element, classes, inner, after).
    var lay = agDays.lay.bind(null, 'xm');

    var HOLLY = '<img src="' + FIGURES + 'holly.svg" alt="" decoding="async">';

    document.body.insertAdjacentHTML('beforeend', DEFS);
    lay(hero, 'xm-holly xm-holly-page', HOLLY);
    // Santa's sleigh, pulled by a reindeer with a red nose, Santa's hand raised to wave.
    lay(hero, 'xm-sky xm-sky-top', '<div class="xm-ride"><div class="xm-bob"><img src="' + FIGURES
        + 'sleigh.svg" alt="" decoding="async"></div></div>');
    // The holly first, so that the snow falls in front of it.
    lay(panel, 'xm-holly xm-holly-panel', HOLLY);
    lay(panel, 'xm-sky xm-sky-panel', STARS + bauble('xm-h3', 'blue') + bauble('xm-h1', 'red') + bauble('xm-h2', 'gold') + SNOW);
    // Just under the phone, back to front: the bank, the tree's halo and the tree, then the
    // figures before it, the elf waving between the penguin and the bear.
    lay(phone, 'xm-ground', '<div class="xm-drift">' + BANK + '</div><div class="xm-halo"></div>' + tree('xm-tree')
        + figure('gift-green', 'xm-gift') + figure('elf-gift', 'xm-elf-gift xm-bounce')
        + figure('snowman', 'xm-snowman xm-sway') + figure('elf-wave', 'xm-elf-wave xm-sway')
        + figure('penguin', 'xm-penguin xm-rock') + figure('bear', 'xm-bear xm-bounce'), true);
    lay(buttons, 'xm-cta-patch', '<div class="xm-c-mound">' + MOUND + '</div><div class="xm-c-halo"></div>'
        + figure('elf-gift', 'xm-c-elf xm-bounce') + figure('snowman', 'xm-c-snowman xm-sway') + tree('xm-c-tree')
        + figure('gift-red', 'xm-c-gift'));

    // The tab says it too: a fir tree before the page's name. Not the site's icon, which a
    // browser may keep well past the day.
    document.title = String.fromCodePoint(0x1F384) + ' ' + document.title;

    // Down the page, every section but the figures that close "End the jitter" (one band with it,
    // no edge of their own): snow falling in the margins beside its text, the panel's near plane,
    // whose flakes show on a light page as on a dark one, and in one of the margins a bauble hung
    // from the section's top and a figure standing at its foot on a mound of snow — the other
    // margin from one section to the next, so that a figure never has the next section's bauble
    // hanging at its feet. The baubles' colours, their ribbons' lengths and the figures in turn;
    // none at the foot of the last section, where the footer's scene stands. A phone has no
    // margins: its bauble hangs in the band above the section's label. Each piece starts its move
    // at its own point, so that no two along the page move as one.
    var footer = page.footer;
    var sections = page.sections;
    var CAST = [['penguin', 'xm-rock'], ['elf-wave', 'xm-sway'], ['snowman', 'xm-sway'], ['bear', 'xm-bounce'],
        ['elf-gift', 'xm-bounce']];
    var COLOURS = ['red', 'gold', 'blue'];
    var RIBBONS = [70, 120, 90, 150, 60];
    var MARGIN_SNOW = '<div class="xm-snow"><div class="xm-plane xm-near" style="background-image:url(' + FIGURES
        + 'snow-near.svg)"></div></div>';
    sections.forEach(function (section, i) {
        var side = i % 2;
        var start = 'animation-delay:' + (-1.3 * (i + 1)).toFixed(1) + 's';
        var colour = COLOURS[i % COLOURS.length];
        var who = CAST[i % CAST.length];
        var margins = [MARGIN_SNOW, MARGIN_SNOW];
        margins[side] += bauble('xm-mhang', colour, RIBBONS[i % RIBBONS.length], start);
        if (!footer || i < sections.length - 1) {
            margins[side] += '<div class="xm-m-mound">' + MOUND + '</div>'
                + figure(who[0], 'xm-mfig ' + who[1], start);
        }
        lay(section, 'xm-sky xm-sky-margin xm-margin-l', margins[0]);
        lay(section, 'xm-sky xm-sky-margin xm-margin-r', margins[1]);
        lay(section, 'xm-sky xm-sky-band', bauble('xm-bhang xm-b' + side, colour, 0, start));
    });

    // The last scene: figures standing on the footer's top edge, in the room the last section
    // leaves above it, each group on its mound of snow — at the right of the text column a tree,
    // two presents and the polar bear; from 721px the snowman and an elf waving on its left — and,
    // hung from that edge into the footer's empty top, a last bauble. Back to front, as at the
    // foot of the phone.
    if (footer) {
        lay(footer, 'xm-foot', '<div class="xm-f-mound xm-f-mound-r">' + MOUND + '</div>'
            + '<div class="xm-f-mound xm-f-mound-l">' + MOUND + '</div>' + tree('xm-f-tree')
            + figure('gift-green', 'xm-f-gift2') + figure('gift-red', 'xm-f-gift') + figure('bear', 'xm-f-bear xm-bounce')
            + figure('snowman', 'xm-f-snowman xm-sway') + figure('elf-wave', 'xm-f-elf xm-sway'));
        lay(footer, 'xm-sky xm-sky-foot', bauble('xm-f-hang', 'gold'));
    }

    // The strip that shows a track playing plays the Nutcracker's Dance of the Sugar Plum Fairy
    // those days, and a button in it plays an excerpt of it (days.js, strip): the Berliner
    // Philharmoniker and Sir Simon Rattle, Warner Classics. 2:24 in all, the dance's length: 1:12
    // played, 1:12 left, the bar 50% full. Named by the work: "Sugar Plum Fairy" took a second
    // line on a 360px phone, where the usual title takes one (measured in Chromium, 2026-11-10).
    // The excerpt is Apple's 30 s preview of the dance (ffprobe on its file: AAC, 44,100 Hz,
    // 280,654 b/s, 30.0 s).
    agDays.strip({
        cover: 'assets/pics/cover-sugar-plum-fairy.webp',
        alt: 'Cover of Tchaikovsky: The Nutcracker by Sir Simon Rattle',
        title: 'The Nutcracker',
        artist: 'Tchaikovsky — S. Rattle',
        played: '1:12',
        left: '1:12',
        fill: '50%',
        excerpt: 'assets/audio/sugar-plum-fairy.m4a',
        heard: ['AAC', '44.1kHz', '281kbps', 'AAC']
    });

    // THE HIDDEN GIFT, the day's game, run by the licence server (days.js, game): five licence keys
    // wake through 24 December, Paris time, each at a secret instant, and the first visitor to ask
    // after one wakes is shown a gold gift in the band at the top of a section, between 30% and 70%
    // of its width — clear of the baubles in the margins and, on a phone, in the band, at 14% and
    // 86%: at 74% it stood against one (measured at 390px) — with twenty minutes to open it. The page asks on the 25th too, the visitor's day being anyone's:
    // the server alone knows when Paris's 24th is. The rules are on hidden-gift.html.
    agDays.game({
        sections: sections,
        kept: 'ag-hidden-gift',
        badge: 'CHRISTMAS',
        rules: 'hidden-gift.html',
        contact: 'contact@audiogravity.app',
        button: 'xm-hidden-gift',
        figure: '<img src="' + FIGURES + 'gift-gold.svg" alt="" decoding="async">',
        label: 'A hidden gift: open it to win a lifetime licence',
        left: function () {
            return 'calc(' + (30 + Math.random() * 40).toFixed(1) + '% - 22px)';
        },
        words: {
            find: 'Find the hidden gift on this page today',
            findShort: 'Find the hidden gift',
            over: 'Every hidden gift has been found. Merry Christmas!',
            overShort: 'All the gifts are found',
            show: 'You found a hidden gift: show your licence key',
            showShort: 'Show your licence key',
            won: 'You found the hidden gift!',
            name: 'The hidden gift',
            twice: 'One gift per visitor: you found one already today.',
            gone: 'Too late: this gift has vanished. Another one may appear later today.',
            silent: 'The licence server did not answer. The gift is still there: try again in a moment.'
        }
    });

    // Nothing moves in a part of the page scrolled out of sight: the hero, a section, the footer
    // (days.js, rest).
    agDays.rest('xm', page.all);
})();
