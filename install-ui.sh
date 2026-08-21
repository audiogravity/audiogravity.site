#!/bin/bash
# Audiogravity UI — Public Bootstrap Installer
#
# Downloads release assets from the GitHub releases repo via the API. --token is
# OPTIONAL: needed only while the releases repo is private (Early Access).
#
# Usage:
#   curl -fsSL https://audiogravity.app/install-ui.sh | sudo bash
#   curl -fsSL https://audiogravity.app/install-ui.sh | sudo bash -s -- --version 1.2.0
#   (add --token <PAT> only while the releases repo is private)

set -e

REPO="audiogravity/audiogravity.releases"
INSTALL_DIR="/tmp/ag-ui-install-$$"

GREEN='\033[0;32m'; RED='\033[0;31m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "  ${GREEN}✓${NC} $1"; }
fail() { echo -e "  ${RED}✗${NC} $1" >&2; exit 1; }
info() { echo -e "  ${BLUE}→${NC} $1"; }
warn() { echo -e "  ${YELLOW}!${NC} $1"; }

[ "$EUID" -eq 0 ] || fail "Run as root: curl ... | sudo bash"

TOKEN=""
VERSION=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --token)   TOKEN="$2";   shift 2 ;;
        --version) VERSION="$2"; shift 2 ;;
        *) fail "Unknown argument: $1" ;;
    esac
done

# --token is OPTIONAL: needed only while the releases repo is private. On a public
# repo the release assets download anonymously, so no token is required.

# Prerequisites. python3 is not optional for the ui either: the deployed HTTPS proxy
# IS a python3 process (`ExecStart=/usr/bin/python3 .../server.py`), and unlike the core
# package the ui installer has no system-dependency block of its own. It used to be a
# hard failure here. We are root (asserted above), so install what is missing.
#
# Duplicated verbatim in scripts/bootstrap-core-install.sh, and it has to be: both are
# standalone single-file scripts piped straight into bash from a URL, so they cannot
# source a shared helper. Change one, change the other.
MISSING_CMDS=""
MISSING_PKGS=""
for cmd in curl tar sha256sum python3; do
    command -v "$cmd" >/dev/null 2>&1 && continue
    MISSING_CMDS="$MISSING_CMDS $cmd"
    # Command name != package name for sha256sum (coreutils); apt would 404 on the rest.
    case "$cmd" in
        sha256sum) MISSING_PKGS="$MISSING_PKGS coreutils" ;;
        *)         MISSING_PKGS="$MISSING_PKGS $cmd" ;;
    esac
done

if [ -n "$MISSING_CMDS" ]; then
    info "Installing missing prerequisites:$MISSING_CMDS"
    DEBIAN_FRONTEND=noninteractive apt-get update -qq \
        && DEBIAN_FRONTEND=noninteractive apt-get install -y $MISSING_PKGS \
        || fail "Could not install:$MISSING_PKGS — install them manually and re-run."
    # apt-get can succeed while still not providing the command (wrong package, held
    # back, alternative provider). Verify what we actually need, not what apt reported.
    for cmd in $MISSING_CMDS; do
        command -v "$cmd" >/dev/null 2>&1 \
            || fail "'$cmd' is still missing after installing:$MISSING_PKGS"
    done
fi

# Send the token only when provided (empty on a public repo). Matches the pattern
# in bootstrap-core-install.sh — change one, change the other.
AUTH_ARGS=()
[ -n "$TOKEN" ] && AUTH_ARGS=(-H "Authorization: Bearer $TOKEN")
API_BASE="https://api.github.com/repos/$REPO"

# A token GitHub refuses is worse than no token at all: the releases repo is public,
# so a request carrying no credential succeeds where one carrying a dead credential
# gets 401. Boxes installed during Early Access still hold a revoked token in their
# .env and hand it to us on every self-update, so validate it once and drop it if it
# is refused — that is what lets such a box repair itself without anyone opening a
# terminal on it.
#
# Only 401 is treated this way: "Bad credentials" is the one answer that means the
# token itself is dead. 403 is deliberately NOT included — GitHub answers 403 when a
# client exceeds its quota, and dropping a VALID token there would take us from 5000
# requests an hour down to 60, turning a pause into a failure. On a public repo a
# valid token is never refused for lack of rights, so 403 here means rate limiting far
# more often than a dead credential. Anything else — a network outage, a captive
# portal, GitHub being down — must stay an error: continuing anonymously there would
# turn a diagnosable failure into a confusing one.
#
# TOKEN itself is cleared too, not just the header: it is forwarded to the package
# installer, which persists it for the next self-update. Keeping a dead value would
# make the box drag it along for ever.
if [ -n "$TOKEN" ]; then
    _token_check=$(curl -s -o /dev/null -m 15 -w '%{http_code}' \
        "${AUTH_ARGS[@]}" "$API_BASE" || echo "000")
    case "$_token_check" in
        401)
            warn "Access token refused by GitHub — continuing without it (the releases repo is public)."
            AUTH_ARGS=()
            TOKEN=""
            ;;
    esac
fi

echo ""
echo -e "${BLUE}╔═══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Audiogravity UI Installer     ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════╝${NC}"
echo ""

if [ -z "$VERSION" ]; then
    info "Fetching latest release version..."
    RELEASE_JSON=$(curl -fsSL "${AUTH_ARGS[@]}" "$API_BASE/releases/latest") \
        || fail "Could not fetch release info. Check your token and internet connection."
else
    info "Fetching release v${VERSION}..."
    RELEASE_JSON=$(curl -fsSL "${AUTH_ARGS[@]}" "$API_BASE/releases/tags/v${VERSION}") \
        || fail "Could not fetch release v${VERSION}. Check the version exists and your token is valid."
fi

VERSION=$(echo "$RELEASE_JSON" | python3 -c "import sys, json; print(json.load(sys.stdin)['tag_name'].lstrip('v'))")
info "Version  : $VERSION"

TARBALL="audiogravity-ui-${VERSION}.tar.gz"

asset_url() {
    echo "$RELEASE_JSON" | python3 -c "
import sys, json
r = json.load(sys.stdin)
name = sys.argv[1]
for a in r['assets']:
    if a['name'] == name:
        print(a['url']); break
else:
    sys.exit(1)
" "$1" || fail "Asset '$1' not found in release v${VERSION}."
}

TARBALL_URL=$(asset_url "$TARBALL")
SUMS_URL=$(asset_url "SHA256SUMS" 2>/dev/null || true)

mkdir -p "$INSTALL_DIR"
trap 'rm -rf "$INSTALL_DIR"' EXIT

info "Downloading $TARBALL..."
curl -fL --progress-bar \
    "${AUTH_ARGS[@]}" -H "Accept: application/octet-stream" \
    "$TARBALL_URL" -o "$INSTALL_DIR/$TARBALL" \
    || fail "Download failed."
ok "Download complete"

info "Verifying integrity..."
if [ -n "$SUMS_URL" ]; then
    curl -fsSL "${AUTH_ARGS[@]}" -H "Accept: application/octet-stream" \
        "$SUMS_URL" -o "$INSTALL_DIR/SHA256SUMS" 2>/dev/null || warn "SHA256SUMS download failed"
fi

if [ -f "$INSTALL_DIR/SHA256SUMS" ]; then
    cd "$INSTALL_DIR"
    grep "$TARBALL" SHA256SUMS | sha256sum --check --status \
        || fail "Checksum verification failed — the file may be corrupted."
    ok "Checksum verified"
    cd - >/dev/null
else
    warn "Skipping checksum verification"
fi

info "Extracting..."
tar -xzf "$INSTALL_DIR/$TARBALL" -C "$INSTALL_DIR"
ok "Extracted"

PACKAGE_DIR=$(find "$INSTALL_DIR" -maxdepth 1 -type d -name "audiogravity-ui-*" | head -1)
[ -n "$PACKAGE_DIR" ] || fail "Could not find package directory after extraction."

info "Running installer..."
echo ""
bash "$PACKAGE_DIR/install.sh"
