/* Copy buttons on the manual's code blocks.
 *
 * Added by this script rather than written into the pages: a copy button with no script behind
 * it is a button that does nothing. A block flagged `nocopy` in the Markdown carries
 * data-copy="no" and gets none — it holds values the reader must replace before running it,
 * and a one-click copy of an example address or password is an invitation to run it as is.
 *
 * The copied text has no trailing newline, so its last line waits for Enter. A terminal with
 * bracketed paste (bash's default since 5.1) holds the whole paste until then; one without runs
 * the lines before the last as they land — which is why the manual gives a step the reader must
 * check before going on (a reboot, say) a block of its own.
 *
 * First-party and dependency-free, like everything else the site loads. The icons are Lucide's
 * `copy` and `check` (ISC licence) — the same two the app's manual uses.
 */
(function () {
    'use strict';

    var SVG_OPEN = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor"'
        + ' stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">';
    var ICON_COPY = SVG_OPEN + '<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/>'
        + '<path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>';
    var ICON_DONE = SVG_OPEN + '<path d="M20 6 9 17l-5-5"/></svg>';

    /** How long the check mark stays before the button offers to copy again. */
    var RESET_MS = 1500;

    /** How long a refusal stays on the button — long enough to read, then it offers again. */
    var FAILED_MS = 4000;

    /**
     * The block's text as the reader should paste it: no trailing newline (see the header).
     * @param {HTMLElement} pre
     * @returns {string}
     */
    function textOf(pre) {
        var code = pre.querySelector('code') || pre;
        return code.textContent.replace(/\n+$/, '');
    }

    /**
     * Select the block's text, so a reader whose browser refuses the clipboard can copy it
     * with the keyboard instead of getting nothing.
     * @param {HTMLElement} pre
     */
    function selectText(pre) {
        var range = document.createRange();
        range.selectNodeContents(pre.querySelector('code') || pre);
        var selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
    }

    /**
     * Name the button — for the tooltip and for assistive technology alike.
     * @param {HTMLButtonElement} btn
     * @param {string} text
     */
    function label(btn, text) {
        btn.setAttribute('aria-label', text);
        btn.title = text;
    }

    /**
     * Show what happened on the button for a moment, then offer to copy again.
     * @param {HTMLButtonElement} btn
     * @param {string} state - `is-copied` or `is-failed`
     * @param {string} text - what the button says meanwhile
     * @param {number} ms - for how long
     */
    function show(btn, state, text, ms) {
        btn.classList.remove('is-copied', 'is-failed');
        btn.classList.add(state);
        label(btn, text);
        clearTimeout(btn.resetTimer);
        btn.resetTimer = setTimeout(function () {
            btn.classList.remove(state);
            label(btn, 'Copy');
        }, ms);
    }

    /**
     * The browser refused the clipboard: select the block so it can be copied with the
     * keyboard, and say so — a selection alone is easy to miss, and the reader would paste
     * whatever the clipboard held before.
     * @param {HTMLButtonElement} btn
     * @param {HTMLElement} pre
     */
    function refused(btn, pre) {
        selectText(pre);
        show(btn, 'is-failed', 'Copy failed — the text is selected, copy it with the keyboard', FAILED_MS);
    }

    /**
     * Give one block its frame and its button. The button sits on the frame, not in the
     * <pre>: the <pre> scrolls sideways on a long line, and would carry the button with it.
     * @param {HTMLElement} pre
     */
    function attach(pre) {
        if (pre.getAttribute('data-copy') === 'no') return;
        if (pre.parentNode.classList.contains('man-code')) return;

        var frame = document.createElement('div');
        frame.className = 'man-code';
        pre.parentNode.insertBefore(frame, pre);
        frame.appendChild(pre);

        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'man-copy';
        label(btn, 'Copy');
        btn.innerHTML = '<span class="man-copy-icon">' + ICON_COPY + '</span>'
            + '<span class="man-copy-done">' + ICON_DONE + '</span>';
        btn.addEventListener('click', function () {
            if (!navigator.clipboard) {
                refused(btn, pre);
                return;
            }
            navigator.clipboard.writeText(textOf(pre)).then(
                function () { show(btn, 'is-copied', 'Copied', RESET_MS); },
                function () { refused(btn, pre); }
            );
        });
        frame.appendChild(btn);
    }

    document.querySelectorAll('.man-md pre').forEach(attach);
})();
