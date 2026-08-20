#!/bin/bash
# Audiogravity Core — Public Bootstrap Installer
#
# Downloads release assets from the GitHub releases repo via the API. --token is
# OPTIONAL: needed only while the releases repo is private (Early Access).
#
# Usage:
#   curl -fsSL https://audiogravity.app/install-core.sh | sudo bash
#   curl -fsSL https://audiogravity.app/install-core.sh | sudo bash -s -- --version 1.2.0
#   curl -fsSL https://audiogravity.app/install-core.sh | sudo bash -s -- --vapid-email you@example.com
#   curl -fsSL https://audiogravity.app/install-core.sh | sudo bash -s -- --public-url https://audiogravity.example.com
#   (add --token <PAT> only while the releases repo is private)

set -e

REPO="audiogravity/audiogravity.releases"
INSTALL_DIR="/tmp/ag-install-$$"

GREEN='\033[0;32m'; RED='\033[0;31m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "  ${GREEN}✓${NC} $1"; }
fail() { echo -e "  ${RED}✗${NC} $1" >&2; exit 1; }
info() { echo -e "  ${BLUE}→${NC} $1"; }
warn() { echo -e "  ${YELLOW}!${NC} $1"; }

[ "$EUID" -eq 0 ] || fail "Run as root: curl ... | sudo bash"

TOKEN=""
VERSION=""
VAPID_EMAIL=""
PUBLIC_URL=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --token)       TOKEN="$2";       shift 2 ;;
        --version)     VERSION="$2";     shift 2 ;;
        --vapid-email) VAPID_EMAIL="$2"; shift 2 ;;
        --public-url)  PUBLIC_URL="$2";  shift 2 ;;
        *) fail "Unknown argument: $1" ;;
    esac
done

# The download token is OPTIONAL: required only while the releases repo is
# private (Early Access). For a public repo, omit --token and the API downloads
# work anonymously; when present, requests are authenticated.

ARCH=$(uname -m)
case "$ARCH" in
    x86_64)        ARCH_TAG="x86_64"  ;;
    aarch64|arm64) ARCH_TAG="aarch64" ;;
    *) fail "Unsupported architecture: $ARCH. Only x86_64 and aarch64 are supported." ;;
esac

# Prerequisites. python3 is the one that is genuinely absent on a minimal image; it
# used to be a hard failure here, which made the whole "bare box to playing box" claim
# untrue: the tarball's own install.sh DOES apt-install python3, but this script aborts
# long before that tarball is ever downloaded. We are root (asserted above), so install
# what is missing instead of handing the operator a chore.
#
# Duplicated verbatim in scripts/bootstrap-ui-install.sh, and it has to be: both are
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

AUTH_ARGS=()
[ -n "$TOKEN" ] && AUTH_ARGS=(-H "Authorization: Bearer $TOKEN")
API_BASE="https://api.github.com/repos/$REPO"

echo ""
echo -e "${BLUE}╔═══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Audiogravity Core Installer      ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════╝${NC}"
echo ""

if [ -z "$VERSION" ]; then
    info "Fetching latest release version..."
    RELEASE_JSON=$(curl -fsSL "${AUTH_ARGS[@]}" "$API_BASE/releases/latest") \
        || fail "Could not fetch release info. Check your connection (and --token if the repo is private)."
else
    info "Fetching release v${VERSION}..."
    RELEASE_JSON=$(curl -fsSL "${AUTH_ARGS[@]}" "$API_BASE/releases/tags/v${VERSION}") \
        || fail "Could not fetch release v${VERSION}. Check the version exists (and --token if the repo is private)."
fi

VERSION=$(echo "$RELEASE_JSON" | python3 -c "import sys, json; print(json.load(sys.stdin)['tag_name'].lstrip('v'))")
info "Version  : $VERSION"
info "Arch     : $ARCH_TAG"

TARBALL="audiogravity-core-${VERSION}-${ARCH_TAG}.tar.gz"

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

PACKAGE_DIR=$(find "$INSTALL_DIR" -maxdepth 1 -type d -name "audiogravity-core-*" | head -1)
[ -n "$PACKAGE_DIR" ] || fail "Could not find package directory after extraction."

info "Running installer..."
echo ""
INSTALL_ARGS=()
[ -n "$VAPID_EMAIL" ] && INSTALL_ARGS+=(--vapid-email "$VAPID_EMAIL")
[ -n "$PUBLIC_URL" ]  && INSTALL_ARGS+=(--public-url "$PUBLIC_URL")
# Forward the token so the install persists it (RELEASE_DOWNLOAD_TOKEN) for the
# one-click self-update. Omitted for a public repo.
[ -n "$TOKEN" ]       && INSTALL_ARGS+=(--token "$TOKEN")
bash "$PACKAGE_DIR/install.sh" "${INSTALL_ARGS[@]}"
