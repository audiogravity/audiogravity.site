#!/bin/bash
# Audiogravity — All-in-one installer (core + ui)
#
# Use this when core and ui run on the same host.
#
# --token is OPTIONAL: needed only while the releases repo is private (Early Access).
#
# Usage:
#   curl -fsSL https://audiogravity.app/install.sh | sudo bash
#   curl -fsSL https://audiogravity.app/install.sh | sudo bash -s -- --version 1.2.0
#   curl -fsSL https://audiogravity.app/install.sh | sudo bash -s -- --public-url https://your-domain
#   (add --token <PAT> only while the releases repo is private)

set -e

TOKEN=""
VERSION=""
COMMON_ARGS=()    # forwarded to both core and ui
CORE_ARGS=()   # core-only (the ui installer rejects unknown flags)
while [[ $# -gt 0 ]]; do
    case $1 in
        --token)       TOKEN="$2";   COMMON_ARGS+=("--token" "$2");   shift 2 ;;
        --version)     VERSION="$2"; COMMON_ARGS+=("--version" "$2"); shift 2 ;;
        --vapid-email) CORE_ARGS+=("--vapid-email" "$2");          shift 2 ;;
        --public-url)  CORE_ARGS+=("--public-url" "$2");           shift 2 ;;
        *) echo "Unknown argument: $1" >&2; exit 1 ;;
    esac
done

[ "$EUID" -eq 0 ] || { echo "✗ Run as root: curl ... | sudo bash" >&2; exit 1; }

BASE="https://audiogravity.app"

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║   Audiogravity — Full Installer       ║"
echo "║   Core + UI on this host              ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# Download both, check they ARE scripts, then run them. Never `curl | bash` here.
#
# Two reasons, both met in the field:
#   - an unknown path on the site answers 200 with the landing page instead of 404,
#     so a stale or mistyped URL does not fail — it feeds 90 KB of HTML to bash,
#     which replies `syntax error near unexpected token` and means nothing to an owner;
#   - in a pipeline only the last command's status counts, and bash on empty input
#     exits 0 — so a download that failed outright still ended on "installed".
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

fetch_script() {
    local url="$1" dest="$2"
    curl -fsSL "$url" -o "$dest" \
        || { echo "✗ Could not download $url — check your connection." >&2; exit 1; }
    # A shell script starts with a shebang. Anything else (an HTML page, a captive
    # portal, a truncated transfer) is refused here rather than executed.
    if ! head -n 1 "$dest" | grep -q '^#!'; then
        echo "✗ $url did not return a script." >&2
        echo "  It starts with: $(head -c 60 "$dest" | tr -d '\n')" >&2
        echo "  Check the address, or report it to contact@audiogravity.app." >&2
        exit 1
    fi
}

fetch_script "$BASE/install-core.sh" "$TMP_DIR/install-core.sh"
fetch_script "$BASE/install-ui.sh"   "$TMP_DIR/install-ui.sh"

# stdin is /dev/null, as it effectively was when these were piped into bash: both
# installers ask their questions on /dev/tty, and this script may itself be running
# from a pipe whose remaining bytes a child must never consume.
bash "$TMP_DIR/install-core.sh" "${COMMON_ARGS[@]}" "${CORE_ARGS[@]}" < /dev/null
bash "$TMP_DIR/install-ui.sh" "${COMMON_ARGS[@]}" < /dev/null

echo ""
echo "✓ Audiogravity installed (core + ui)."
echo "  Open the UI address printed above in a browser."
echo ""
