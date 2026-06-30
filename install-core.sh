#!/bin/bash
# Audiogravity Core — Public Bootstrap Installer (token-authenticated)
#
# Downloads release assets from the private GitHub repo via the API.
#
# Usage:
#   curl -fsSL https://audiogravity.app/install-core.sh | sudo bash -s -- --token ghp_xxx
#   curl -fsSL https://audiogravity.app/install-core.sh | sudo bash -s -- --token ghp_xxx --version 1.2.0
#   curl -fsSL https://audiogravity.app/install-core.sh | sudo bash -s -- --token ghp_xxx --vapid-email you@example.com
#   curl -fsSL https://audiogravity.app/install-core.sh | sudo bash -s -- --token ghp_xxx --public-url https://audiogravity.example.com

set -e

REPO="audiogravity/audiogravity-releases"
INSTALL_DIR="/tmp/ag-install-$$"

GREEN='\033[0;32m'; RED='\033[0;31m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "  ${GREEN}✓${NC} $1"; }
fail() { echo -e "  ${RED}✗${NC} $1" >&2; exit 1; }
info() { echo -e "  ${BLUE}→${NC} $1"; }
warn() { echo -e "  ${YELLOW}!${NC} $1"; }

[ "$EUID" -eq 0 ] || fail "Run as root: curl ... | sudo bash -s -- --token <PAT>"

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

[ -n "$TOKEN" ] || fail "Missing --token <PAT>. Request your access token from contact@audiogravity.app."

ARCH=$(uname -m)
case "$ARCH" in
    x86_64)        ARCH_TAG="x86_64"  ;;
    aarch64|arm64) ARCH_TAG="aarch64" ;;
    *) fail "Unsupported architecture: $ARCH. Only x86_64 and aarch64 are supported." ;;
esac

for cmd in curl tar sha256sum python3; do
    command -v "$cmd" >/dev/null 2>&1 || fail "'$cmd' is required but not installed."
done

AUTH_HEADER="Authorization: Bearer $TOKEN"
API_BASE="https://api.github.com/repos/$REPO"

echo ""
echo -e "${BLUE}╔═══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Audiogravity Core Installer      ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════╝${NC}"
echo ""

if [ -z "$VERSION" ]; then
    info "Fetching latest release version..."
    RELEASE_JSON=$(curl -fsSL -H "$AUTH_HEADER" "$API_BASE/releases/latest") \
        || fail "Could not fetch release info. Check your token and internet connection."
else
    info "Fetching release v${VERSION}..."
    RELEASE_JSON=$(curl -fsSL -H "$AUTH_HEADER" "$API_BASE/releases/tags/v${VERSION}") \
        || fail "Could not fetch release v${VERSION}. Check the version exists and your token is valid."
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
    -H "$AUTH_HEADER" -H "Accept: application/octet-stream" \
    "$TARBALL_URL" -o "$INSTALL_DIR/$TARBALL" \
    || fail "Download failed."
ok "Download complete"

info "Verifying integrity..."
if [ -n "$SUMS_URL" ]; then
    curl -fsSL -H "$AUTH_HEADER" -H "Accept: application/octet-stream" \
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
bash "$PACKAGE_DIR/install.sh" "${INSTALL_ARGS[@]}"
