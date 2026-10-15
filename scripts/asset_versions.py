"""Version stamps on the site's own stylesheets and scripts.

The pages and the files they load are cached for different lengths of time: the host asks a
browser to check a page at every visit, and lets it keep a stylesheet or a script four hours
(``cache-control: max-age=14400`` on assets/manual.css, measured 2026-10-15). After an update, a
visitor who came in those four hours gets the new page with the old files — on 2026-10-15 the
manual's new light / dark button sat against the bar's label in Safari, its rule still in a
stylesheet the browser had kept.

So every page asks for each of its stylesheets and scripts with a stamp taken from the file's
content: ``assets/style.css?v=3f2a91c04b``. A file that changes gets a new address, which no
cache holds; one that does not keeps its address, and stays cached. Fonts and images are left
as they are: a stylesheet names its fonts itself, and a stamp on the landing's font preloads
alone would fetch every font twice.

The manual's pages are stamped by their generator (gen_manual_html.py). The pages written by
hand are stamped by this script: ``python3 scripts/asset_versions.py`` rewrites them, and
``--check`` only says which are out of date (the landing's tests run the same check).
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent

#: The pages written by hand. The manual's are generated, and stamped as they are written.
HAND_WRITTEN = ("index.html", "404.html")

#: A stylesheet or script a page names in an attribute, with its stamp if it has one.
ASSET_REF = re.compile(r'(?P<attr>(?:href|src)=")(?P<url>[^"#?:]+\.(?:css|js))(?:\?v=[0-9a-f]*)?"')

#: Characters of the content hash kept: ten hex digits tell a change apart well enough.
STAMP_LENGTH = 10


def fingerprint(path: Path) -> str:
    """The stamp of a file: the start of the hash of its content.

    Args:
        path: The file.

    Returns:
        Ten hexadecimal digits, the same for the same bytes.
    """
    return hashlib.sha256(path.read_bytes()).hexdigest()[:STAMP_LENGTH]


def _target(url: str, page_dir: Path, root: Path) -> Path | None:
    """The file a page's reference names, or None when it is not one of the site's.

    Args:
        url: The reference as written, without its stamp: relative, or from the root.
        page_dir: The folder of the page that names it.
        root: The site's root folder.

    Returns:
        The file, when it exists under the root.
    """
    path = (root / url.lstrip("/")) if url.startswith("/") else (page_dir / url)
    path = path.resolve()
    if not path.is_file() or root.resolve() not in path.parents:
        return None
    return path


def stamp(page: str, page_dir: Path, root: Path = REPO_DIR) -> str:
    """Stamp every stylesheet and script of the site a page names with its current content.

    An earlier stamp is replaced; a reference to a file elsewhere — another site, a file that
    does not exist — is left as written.

    Args:
        page: The page's HTML.
        page_dir: The folder the page is served from, which its relative references start at.
        root: The site's root folder.

    Returns:
        The page, its references stamped.
    """
    def one(match: re.Match) -> str:
        target = _target(match["url"], page_dir, root)
        if target is None:
            return match[0]
        return f'{match["attr"]}{match["url"]}?v={fingerprint(target)}"'

    return ASSET_REF.sub(one, page)


def out_of_date(page: str, page_dir: Path, root: Path = REPO_DIR) -> list[str]:
    """The references of a page whose stamp is missing or no longer matches the file.

    Args:
        page: The page's HTML.
        page_dir: The folder the page is served from.
        root: The site's root folder.

    Returns:
        Each such reference, as written in the page.
    """
    return [
        match[0]
        for match in ASSET_REF.finditer(page)
        if _target(match["url"], page_dir, root) is not None
        and match[0] != stamp(match[0], page_dir, root)
    ]


def main() -> int:
    """Stamp the pages written by hand, or with ``--check``, list the ones out of date.

    Returns:
        The exit status: 1 when ``--check`` finds a page out of date.
    """
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="only list the stale stamps")
    args = parser.parse_args()

    stale = 0
    for name in HAND_WRITTEN:
        path = REPO_DIR / name
        page = path.read_text(encoding="utf-8")
        if args.check:
            for ref in out_of_date(page, path.parent):
                print(f"{name}: {ref}")
                stale += 1
            continue
        stamped = stamp(page, path.parent)
        if stamped != page:
            path.write_text(stamped, encoding="utf-8")
            print(f"stamped {name}")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
