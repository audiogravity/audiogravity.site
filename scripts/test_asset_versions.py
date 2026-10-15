"""Tests for asset_versions.py — the stamps that keep a page and its files in step.

On 2026-10-15 Safari showed the manual's new page with a stylesheet kept from before the
update: the host lets a browser keep stylesheets and scripts four hours, pages not at all.
Every page now asks for its own files with a stamp of their content.

Run with ``python3 -m pytest scripts/test_asset_versions.py``; both workflows run it.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from asset_versions import (  # noqa: E402
    HAND_WRITTEN,
    REPO_DIR,
    fingerprint,
    out_of_date,
    stamp,
)


def site(tmp_path: Path) -> Path:
    """A small site: a stylesheet and a script under assets/, a page in a sub-folder."""
    root = tmp_path / "site"
    (root / "assets").mkdir(parents=True)
    (root / "assets" / "style.css").write_text("body { color: black }")
    (root / "assets" / "app.js").write_text("console.log(1)")
    (root / "docs").mkdir()
    return root


class TestStamp:
    def test_stamps_a_stylesheet_and_a_script_with_their_content(self, tmp_path):
        root = site(tmp_path)
        out = stamp('<link href="assets/style.css"><script src="assets/app.js"></script>', root, root)
        assert f'href="assets/style.css?v={fingerprint(root / "assets" / "style.css")}"' in out
        assert f'src="assets/app.js?v={fingerprint(root / "assets" / "app.js")}"' in out

    def test_resolves_from_the_page_folder_and_from_the_root(self, tmp_path):
        root = site(tmp_path)
        out = stamp('<link href="../assets/style.css"><link href="/assets/style.css">', root / "docs", root)
        assert out.count(f'?v={fingerprint(root / "assets" / "style.css")}"') == 2

    def test_a_new_content_gets_a_new_stamp(self, tmp_path):
        root = site(tmp_path)
        before = stamp('<link href="assets/style.css">', root, root)
        (root / "assets" / "style.css").write_text("body { color: white }")
        after = stamp(before, root, root)
        assert before != after
        assert after.count("?v=") == 1   # the old stamp is replaced, not kept beside the new

    def test_stamping_twice_changes_nothing(self, tmp_path):
        root = site(tmp_path)
        once = stamp('<script src="assets/app.js" defer></script>', root, root)
        assert stamp(once, root, root) == once

    def test_leaves_another_site_and_a_missing_file_alone(self, tmp_path):
        root = site(tmp_path)
        page = ('<script src="https://cdn.example.org/lib.js"></script>'
                '<script src="//cdn.example.org/lib.js"></script>'
                '<link href="assets/gone.css">')
        assert stamp(page, root, root) == page

    def test_leaves_fonts_and_images_alone(self, tmp_path):
        """A stylesheet names its fonts itself: a stamp on the page's preload alone would
        fetch each font twice."""
        root = site(tmp_path)
        (root / "assets" / "f.woff2").write_bytes(b"x")
        (root / "assets" / "p.webp").write_bytes(b"x")
        page = '<link rel="preload" href="assets/f.woff2"><img src="assets/p.webp">'
        assert stamp(page, root, root) == page

    def test_never_reaches_out_of_the_site(self, tmp_path):
        root = site(tmp_path)
        (tmp_path / "outside.css").write_text("x")   # beside the site, not in it
        page = '<link href="../outside.css">'
        assert stamp(page, root, root) == page


class TestOutOfDate:
    def test_names_a_missing_and_a_stale_stamp(self, tmp_path):
        root = site(tmp_path)
        page = '<link href="assets/style.css"><script src="assets/app.js?v=0000000000"></script>'
        assert out_of_date(page, root, root) == ['href="assets/style.css"', 'src="assets/app.js?v=0000000000"']

    def test_finds_nothing_once_stamped(self, tmp_path):
        root = site(tmp_path)
        assert out_of_date(stamp('<link href="assets/style.css">', root, root), root, root) == []


class TestTheSite:
    """The real pages, as committed."""

    def test_the_hand_written_pages_ask_for_the_current_files(self):
        """After editing a stylesheet or a script: ``python3 scripts/asset_versions.py``."""
        for name in HAND_WRITTEN:
            page = (REPO_DIR / name).read_text(encoding="utf-8")
            assert re.search(r'\?v=[0-9a-f]{10}"', page), f"{name} names no stamped file"
            assert out_of_date(page, REPO_DIR) == [], f"{name}: run python3 scripts/asset_versions.py"
