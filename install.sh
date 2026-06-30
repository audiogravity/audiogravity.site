#!/bin/bash
# Audiogravity — All-in-one installer (core + ui)
#
# Use this when core and ui run on the same host.
#
# Usage:
#   curl -fsSL https://audiogravity.app/install.sh | sudo bash -s -- --token ghp_xxx
#   curl -fsSL https://audiogravity.app/install.sh | sudo bash -s -- --token ghp_xxx --version 1.2.0
#   curl -fsSL https://audiogravity.app/install.sh | sudo bash -s -- --token ghp_xxx --public-url https://your-domain

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

if [ -z "$TOKEN" ]; then
    echo "✗ Missing --token <PAT>. Request your access token from contact@audiogravity.app." >&2
    exit 1
fi

[ "$EUID" -eq 0 ] || { echo "✗ Run as root: curl ... | sudo bash -s -- --token <PAT>" >&2; exit 1; }

BASE="https://audiogravity.app"

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║   Audiogravity — Full Installer       ║"
echo "║   Core + UI on this host              ║"
echo "╚═══════════════════════════════════════╝"
echo ""

curl -fsSL "$BASE/install-core.sh"  | bash -s -- "${COMMON_ARGS[@]}" "${CORE_ARGS[@]}"
curl -fsSL "$BASE/install-ui.sh" | bash -s -- "${COMMON_ARGS[@]}"

echo ""
echo "✓ Audiogravity installed (core + ui)."
echo "  Open https://<this-host>/ in a browser."
echo ""
