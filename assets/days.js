// What the days the landing dresses up share — Halloween (halloween.js) and Christmas
// (christmas.js): the parts of the page they dress, laying a piece of decoration, resting the
// parts of the page scrolled away, the
// strip that shows a track playing, which plays the day's own record and lets the visitor hear an
// excerpt of it, and the day's game, a lifetime licence hidden down the page. Fetched with each
// day's script, just before it, and on no other day (the templates at the end of index.html).
window.agDays = (function () {
    /**
     * The parts of the landing a day dresses: the hero, the panel the phone stands in, the phone,
     * the hero's buttons, the sections down the page — every one but the figures that close "End
     * the jitter", one band with it, with no top nor foot of its own — and the footer.
     *
     * @returns {?{hero: Element, panel: Element, phone: Element, buttons: Element,
     *     sections: Element[], footer: ?Element, all: Element[]}} The parts, and all of them that
     *     carry decoration in page order (all, for rest); null when the page has no phone or no
     *     buttons to stand the first scene by.
     */
    function parts() {
        var hero = document.querySelector('.hero');
        var panel = hero && hero.querySelector('.hero-right');
        var phone = panel && panel.querySelector('.hero-carousel');
        var buttons = hero && hero.querySelector('.hero-cta');
        if (!phone || !buttons) return null;
        var sections = [].filter.call(document.querySelectorAll('.section'), function (section) {
            return !section.classList.contains('rt-proof');
        });
        var footer = document.querySelector('footer');
        return {
            hero: hero,
            panel: panel,
            phone: phone,
            buttons: buttons,
            sections: sections,
            footer: footer,
            all: [hero].concat(sections, footer ? [footer] : [])
        };
    }

    /**
     * Lays a piece of a day's decoration at the end of an element of the page, or just after it:
     * hidden from assistive technology, deaf to the pointer (<prefix>-decor in the day's sheet).
     *
     * @param {string} prefix - The day's prefix: 'hw' for Halloween, 'xm' for Christmas.
     * @param {Element} element - Where it goes.
     * @param {string} classes - Its classes, after <prefix>-decor.
     * @param {string} inner - Its content.
     * @param {boolean} [after] - True to place it after the element rather than inside.
     */
    function lay(prefix, element, classes, inner, after) {
        element.insertAdjacentHTML(after ? 'afterend' : 'beforeend',
            '<div class="' + prefix + '-decor ' + classes + '" aria-hidden="true">' + inner + '</div>');
    }

    /**
     * Rests each part of the page while it is scrolled away: <prefix>-paused on it, which the
     * day's sheet reads — Halloween's to hold every animation of the decoration inside,
     * Christmas's to take the decoration off the page. A part comes back to life a little before
     * it shows, 120px before it comes in at the foot of the screen or at its top, so that nothing
     * starts or appears in front of the visitor, whichever way they scroll: the observer answers a
     * frame late, and a section's foot, scrolled back up to, showed its figures appear.
     *
     * @param {string} prefix - The day's prefix.
     * @param {Element[]} parts - The parts of the page that carry decoration (parts().all).
     */
    function rest(prefix, parts) {
        if (!('IntersectionObserver' in window)) return;
        var watch = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                entry.target.classList.toggle(prefix + '-paused', !entry.isIntersecting);
            });
        }, { rootMargin: '120px 0px 120px 0px' });
        parts.forEach(function (part) {
            watch.observe(part);
        });
    }

    /**
     * The strip that shows a track playing plays the day's record: its cover, its title, how far
     * it has got. The path and the format stay: they are the box's, not the record's — except
     * while the excerpt plays, when the strip shows the excerpt's own (listen). The cover, 400 x
     * 400 as the usual one, is asked for only now, the image being lazy.
     *
     * @param {Object} record - The day's record.
     * @param {string} record.cover - The cover's address.
     * @param {string} record.alt - The cover's text, naming the record as the title is written.
     * @param {string} record.title - The track's title.
     * @param {string} record.artist - The composer and the performer, no longer than the usual line.
     * @param {string} record.played - The time played, m:ss.
     * @param {string} record.left - The time left, m:ss.
     * @param {string} record.fill - How full the bar is: the time played over the whole, in %.
     * @param {string} record.excerpt - The excerpt's address: 30 s of the recording.
     * @param {string[]} record.heard - What the four cells say while the excerpt plays: its own
     *     format, sample rate, bitrate and codec.
     */
    function strip(record) {
        var shown = document.querySelector('.np-strip');
        if (!shown) return;
        var cover = shown.querySelector('.np-cover');
        cover.src = record.cover;
        cover.alt = record.alt;
        shown.querySelector('.track-name').textContent = record.title;
        shown.querySelector('.track-artist').textContent = record.artist;
        var progress = shown.querySelector('.np-progress');
        progress.setAttribute('aria-label', record.played + ' played, ' + record.left + ' left');
        progress.firstElementChild.textContent = record.played;
        progress.lastElementChild.textContent = progress.lastElementChild.textContent.replace(/\d+:\d\d/, record.left);
        progress.querySelector('.fill').style.width = record.fill;
        listen(progress, record);
    }

    /**
     * Lets the strip play what it shows: a round button beside the time plays an excerpt of the
     * recording, Apple's 30 s preview, asked for only at the first press. While it plays, the
     * strip tells the truth about what is heard: the excerpt's own format and its own time, 0:00
     * to 0:30. Paused or over, it shows the box's again. An audiophile reading DSD256 over a
     * browser's AAC preview would be right to feel misled. Never on its own: a browser plays no
     * sound before the visitor has pressed something, and the page would not want to. The
     * recordings are protected: playing them on their day is the site owner's decision, the risk
     * taken knowingly (2026-10-25 for Halloween, 2026-11-10 for Christmas). The button wears the
     * carousel's own play and pause icons, copied from it rather than drawn twice.
     *
     * @param {Element} progress - The strip's progress row: the time played, the bar, the time left.
     * @param {Object} record - The day's record (strip).
     */
    function listen(progress, record) {
        var playIcon = document.querySelector('#heroPlay .ic-play');
        var pauseIcon = document.querySelector('#heroPlay .ic-pause');
        if (!playIcon || !pauseIcon) return;
        var played = progress.firstElementChild;
        var left = progress.lastElementChild;
        var fill = progress.querySelector('.fill');
        var values = [].slice.call(document.querySelectorAll('.np-fmt .cell b'));
        // What the box shows, put back when the excerpt stops.
        var box = {
            values: values.map(function (b) { return b.textContent; }),
            played: played.textContent,
            left: left.textContent,
            width: fill.style.width,
            label: progress.getAttribute('aria-label')
        };
        var sound = null;
        var button = document.createElement('button');
        button.type = 'button';
        button.className = 'day-np-play';
        button.appendChild(playIcon.cloneNode(true));
        button.appendChild(pauseIcon.cloneNode(true));
        // Beside the progress row, not in it: the row is an image to assistive technology, whose
        // content is not read, and a button there would be heard as nothing.
        var row = document.createElement('div');
        row.className = 'day-np-row';
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
                b.textContent = element ? record.heard[i] : box.values[i];
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
            var element = new Audio(record.excerpt);
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

    // THE GAME — a prize hidden down the page on the day the game runs, run by the licence server
    // (audiogravity.lic, routers/ghost.py): lifetime licence keys wake through that day, Paris time,
    // each at a secret instant, and the first visitor to ask after one wakes is shown the prize
    // somewhere down the page, with twenty minutes to take it. The page asks once a visit and
    // decides nothing: it can neither make the prize appear nor know a key before the server gives
    // it. The day's script says what the prize is and what the game says — an orange ghost on 31
    // October (halloween.js), a gift on 24 December (christmas.js) — and the day's page the rules.
    var LICENCE_SERVER = location.hostname === 'audiogravity.app'
        ? 'https://lic.audiogravity.app:8443/ls/portal/'
        // Anywhere else, the page is a developer's copy: it asks the licence server beside it.
        : location.protocol + '//' + location.hostname + ':8100/ls/portal/';
    var KEY = /^AG(-[A-Z0-9]{4}){4}$/;

    /**
     * Plays the day's game: asks the licence server whether it is on and whether the prize is here
     * for this visitor, words the banner from the answer, and hides the prize when there is one. A
     * visitor who took one this year on this device is offered their key again, and asks nothing.
     *
     * @param {Object} day - The day's game.
     * @param {Element[]} day.sections - The sections the prize may hide in, at the top of one.
     * @param {string} day.kept - Where this device keeps the key it took (localStorage).
     * @param {string} day.badge - The banner's badge.
     * @param {string} day.rules - The rules' page.
     * @param {string} day.contact - The game's address, in the winner's window.
     * @param {string} day.button - The prize's class, which the day's sheet draws.
     * @param {string} day.figure - The prize's markup, the page's own.
     * @param {string} day.label - The prize's name, for assistive technology.
     * @param {function(): string} day.left - Where along the band it hides, as a CSS length.
     * @param {Object} day.words - What the game says: find, the banner while it is on, before the
     *     count of licences left; over, once every prize is taken; show, once this device took
     *     one; each with its short form for a phone (findShort, overShort, showShort); won, the
     *     winner's window's title; name, a window's name; twice, a second key refused; gone, a
     *     prize lapsed; silent, a server that did not answer.
     */
    function game(day) {
        var words = day.words;
        hunt();

        /**
         * Asks the licence server whether the game is on and whether the prize is here for this
         * visitor, words the banner from the answer, and hides the prize when there is one.
         */
        function hunt() {
            var mine = kept();
            if (mine) {
                announce(words.show, words.showShort, function () {
                    reveal(mine);
                });
                return;
            }
            ask('ghost-draw').then(function (answer) {
                var left = parseInt(answer.data.left, 10) || 0;
                if (answer.data.state === 'open' && left > 0) {
                    announce(words.find + ': ' + left
                        + (left === 1 ? ' lifetime licence' : ' lifetime licences') + ' left to win',
                        words.findShort);
                    if (answer.data.ghost && answer.data.ghost.ticket) haunt(answer.data.ghost);
                } else if (answer.data.state === 'over') {
                    announce(words.over, words.overShort);
                }
            }, function () {});
        }

        /**
         * Asks the licence server one of the game's two questions.
         *
         * @param {string} route - 'ghost-draw' or 'ghost-claim'.
         * @param {Object} [body] - What the question sends, as JSON.
         * @returns {Promise<{status: number, data: Object}>} The answer's status, and its JSON
         *     (empty when it carries none); rejected when the server cannot be reached in time.
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
         * Writes the game's news in the announce bar, where it takes turns with the release's
         * sentence, with the page's own writer of that news (window.agAnnounce, in index.html):
         * the day's badge, a sentence, and where a press leads — the rules, or the visitor's key.
         *
         * @param {string} sentence - What it says.
         * @param {string} short - The same for a phone, whose bar holds one line.
         * @param {Function} [open] - What a press does instead of leading to the rules.
         */
        function announce(sentence, short, open) {
            if (!window.agAnnounce) return;
            window.agAnnounce({ badge: day.badge, sentence: sentence, short: short, href: day.rules, open: open });
        }

        /**
         * Hides the prize in the band at the top of a section taken at random, somewhere along it,
         * above every label. It stays there as long as the ticket the server gave with it lasts,
         * counted from now rather than read off the visitor's clock, which may be wrong by any
         * amount. Taken, it trades the ticket for the key.
         *
         * @param {{ticket: string, ttl: number}} ghost - The server's ticket, and the seconds it lasts.
         */
        function haunt(ghost) {
            var section = day.sections[Math.floor(Math.random() * day.sections.length)];
            if (!section) return;
            var button = document.createElement('button');
            button.type = 'button';
            button.className = day.button;
            button.setAttribute('aria-label', day.label);
            button.style.left = day.left();
            button.innerHTML = day.figure;
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
                            localStorage.setItem(day.kept, JSON.stringify(mine));
                        } catch (e) { /* refused storage: the key is shown this once */ }
                        announce(words.show, words.showShort, function () {
                            reveal(mine);
                        });
                        reveal(mine);
                    } else {
                        tell(answer.status === 409 ? words.twice : words.gone);
                    }
                }, function () {
                    // No answer, though the server may have given the key on its side: the prize
                    // stays, past its time if need be, since the same ticket gives the same key again.
                    clearTimeout(lapse);
                    button.removeAttribute('aria-disabled');
                    tell(words.silent);
                });
            });
        }

        /**
         * The key this device took, kept so that a reload shows it again, for this year's game
         * only. Storage may be refused (private browsing): the key was then shown once, when taken.
         *
         * @returns {?{key: string, year: number}} The key and its year, or null.
         */
        function kept() {
            try {
                var mine = JSON.parse(localStorage.getItem(day.kept));
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
            dialog.className = 'day-catch';
            dialog.setAttribute('aria-label', label);
            dialog.innerHTML = html + '<form method="dialog"><button class="day-catch-close">Close</button></form>';
            fill(dialog);
            dialog.addEventListener('close', function () {
                dialog.remove();
            });
            document.body.appendChild(dialog);
            dialog.showModal();
        }

        /**
         * Shows the key the visitor took, how to activate it, and the rules.
         *
         * @param {{key: string}} mine - The key.
         */
        function reveal(mine) {
            windowOf('Your lifetime licence', '<h2>' + words.won + '</h2>'
                + '<p>Your lifetime Audiogravi<sup>ty</sup> licence:</p>'
                + '<p class="day-catch-key"><code></code><button type="button" class="day-catch-copy">Copy</button></p>'
                + '<ol><li>In Audiogravi<sup>ty</sup>, open the <b>Admin</b> tab.</li>'
                + '<li>Tap <b>LICENSE KEY</b>, at the top of the licence panel, and paste the key.</li>'
                + '<li>Tap <b>CHECK KEY</b>, then <b>ACTIVATE THIS MACHINE</b>.</li></ol>'
                + '<p class="day-catch-note">The key works once: the first box to activate it keeps it, so keep'
                + ' it to yourself. No box yet? It will wait for you, and this page keeps it on this device.</p>'
                + '<p class="day-catch-note"><a href="' + day.rules + '">The rules</a> · '
                + '<a href="mailto:' + day.contact + '">' + day.contact + '</a></p>',
            function (dialog) {
                dialog.querySelector('code').textContent = mine.key;
                var copy = dialog.querySelector('.day-catch-copy');
                copy.addEventListener('click', function () {
                    if (!navigator.clipboard) return;
                    navigator.clipboard.writeText(mine.key).then(function () {
                        copy.textContent = 'Copied';
                    }, function () {});
                });
            },
            // Plain text: the brand as an attribute writes it, there being no markup to raise "ty".
            words.won + ' Your lifetime Audiogravity licence key:\n\n' + mine.key
                + '\n\nIn Audiogravity, open the Admin tab, tap LICENSE KEY and paste the key, then tap'
                + ' CHECK KEY and ACTIVATE THIS MACHINE. The key works once: keep it to yourself.');
        }

        /**
         * Says one sentence about the game in a window: a prize gone, or a server that did not answer.
         *
         * @param {string} sentence - What it says.
         */
        function tell(sentence) {
            windowOf(words.name, '<p></p>', function (dialog) {
                dialog.querySelector('p').textContent = sentence;
            }, sentence);
        }
    }

    return { parts: parts, lay: lay, rest: rest, strip: strip, game: game };
})();
