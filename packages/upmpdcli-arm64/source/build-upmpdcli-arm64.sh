#!/bin/bash
# Audiogravity — upmpdcli arm64 .deb builder
#
# upmpdcli (UPnP→MPD bridge) is NOT published for arm64 by its author
# (lesbonscomptes.com ships amd64/armhf/i386 only) nor by Debian. This script
# compiles the full chain natively for aarch64 and produces installable .deb
# packages, to be uploaded to the AudioGravity GitHub release so AG can install
# UPnP Bridge on ARM when no official arm64 package exists.
#
# Build chain (each depends on the previous):
#   libnpupnp  ->  libupnpp  ->  upmpdcli
# Qt5 is intentionally left out (confgui option, off by default).
#
# Usage:
#   ./scripts/build-upmpdcli-arm64.sh                 # build with pinned versions
#   ./scripts/build-upmpdcli-arm64.sh --deps          # apt-install build deps first
#
# Output: dist/upmpdcli-arm64/*.deb + SHA256SUMS (dist/ is gitignored), and
# dist/upmpdcli-arm64/source/: the upstream archives the packages were built
# from, exactly as downloaded and verified, a copy of this script (it is what
# builds and packages them), and their own SHA256SUMS. upmpdcli is
# LGPL-2.1-or-later with GPL parts and libupnpp LGPL-2.1-or-later, so whoever
# distributes these binaries must offer their source — and offering it from
# the same place is what --publish does. The root SHA256SUMS must list the .deb files and nothing
# else: AG reads it as the bundle's file list and refuses any other entry
# (`_parse_manifest_entries` in the core), which is why the sources sit in a
# folder of their own.
# Run on an aarch64 Debian host (the AG ARM target).

set -euo pipefail

# ── Pinned upstream versions + source tarball checksums ───────────────────────
# The .deb produced here are installed as root on user devices, so the upstream
# sources are pinned by SHA256 and verified before building — a compromised
# upstream host or broken TLS can't silently flow into a root-installed package.
# On a version bump: update the version AND its SHA256 (download once, sha256sum,
# paste). Verify against upstream signatures when available.
LIBNPUPNP_VER="6.3.0"
LIBUPNPP_VER="1.0.4"
UPMPDCLI_VER="1.10.1"
LIBNPUPNP_SHA="082d999178291ed45ae24c3fd9e781120d3ec94d61d11121e5bac90c69365cda"
LIBUPNPP_SHA="4738a19be51c09bd59a26b28e305172e2052c0e970b2fad92320a2d7cf1157c5"
UPMPDCLI_SHA="15bc3cd9b4db4dc540d9e106031ba476a57310be254fc7d0f01b2b1ccd065b44"
# Debian package revision suffix for our rebuilds. No '~' so the resulting
# filename (..._<ver>-1ag_arm64.deb) needs no URL-encoding in the registry URLs.
DEB_REV="1ag"

DL_BASE="https://www.lesbonscomptes.com/upmpdcli/downloads"

# Runtime Depends copied from the author's official amd64 control files
# (same on arm64 — only the compiled code differs). Keep in sync on version bump.
DEP_LIBNPUPNP="libc6 (>= 2.38), libcurl3t64-gnutls (>= 7.16.2), libgcc-s1 (>= 3.0), libmicrohttpd12t64 (>= 0.9.50), libstdc++6 (>= 13.1)"
DEP_LIBUPNPP="libc6 (>= 2.38), libcurl3t64-gnutls (>= 7.16.2), libgcc-s1 (>= 3.0), libnpupnp13 (>= 6.3.0), libstdc++6 (>= 13.1)"
DEP_UPMPDCLI="libc6 (>= 2.38), libcurl3t64-gnutls (>= 7.16.2), libgcc-s1 (>= 3.0), libjsoncpp26 (>= 1.9.6), libmicrohttpd12t64 (>= 0.9.50), libmpdclient2t64 (>= 2.2), libstdc++6 (>= 13.1), libupnpp17 (>= 1.0.4), adduser, python3, python3-requests"

# Build-time -dev packages (no Qt5: confgui is off by default).
BUILD_DEPS="meson ninja-build libexpat1-dev libcurl4-gnutls-dev libjsoncpp-dev libmicrohttpd-dev libmpdclient-dev"

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WORK="$(mktemp -d /tmp/upmpdcli-build.XXXXXX)"
OUT_DIR="$REPO_ROOT/dist/upmpdcli-arm64"
SRC_OUT="$OUT_DIR/source"

# Landing repo (public, served at audiogravity.app via GitHub Pages). With
# --publish, the built .deb and their sources are copied here and committed; the push is left to
# you. Override with AG_LANDING_DIR if the repo lives elsewhere.
LANDING_DIR="${AG_LANDING_DIR:-$(cd "$REPO_ROOT/../audiogravity.site" 2>/dev/null && pwd || true)}"
PAGES_SUBDIR="packages/upmpdcli-arm64"

GREEN='\033[0;32m'; RED='\033[0;31m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "  ${GREEN}✓${NC} $1"; }
info() { echo -e "  ${BLUE}→${NC} $1"; }
warn() { echo -e "  ${YELLOW}!${NC} $1"; }
fail() { echo -e "  ${RED}✗${NC} $1" >&2; exit 1; }

cleanup() { rm -rf "$WORK"; }
trap cleanup EXIT

echo ""
echo -e "${BLUE}Audiogravity — upmpdcli arm64 builder${NC}"
echo ""

# ── Args ──────────────────────────────────────────────────────────────────────
DO_DEPS=false
DO_PUBLISH=false
for arg in "$@"; do
    case "$arg" in
        --deps)    DO_DEPS=true ;;
        --publish) DO_PUBLISH=true ;;
        *) fail "Unknown option: $arg (use --deps and/or --publish)" ;;
    esac
done

# ── Preconditions ─────────────────────────────────────────────────────────────
[ "$(uname -m)" = "aarch64" ] || fail "Must run on aarch64 (got $(uname -m)). Cross-build not supported."

if $DO_DEPS; then
    info "Installing build dependencies (sudo apt-get)..."
    sudo apt-get update -qq
    sudo apt-get install -y $BUILD_DEPS >/dev/null
    ok "Build dependencies installed"
fi

for t in meson ninja gcc g++ pkg-config dpkg-deb curl tar; do
    command -v "$t" >/dev/null 2>&1 || fail "Missing build tool: $t (run with --deps to install)"
done

# ── Helpers ───────────────────────────────────────────────────────────────────
fetch() {
    # fetch <name> <version> <sha256> -> download, verify checksum, extract into $WORK
    local name="$1" ver="$2" sha="$3" tgz="$1-$2.tar.gz"
    info "Downloading $tgz..."
    curl -fsSL -o "$WORK/$tgz" "$DL_BASE/$tgz" || fail "Download failed: $tgz"
    info "Verifying source checksum..."
    echo "$sha  $WORK/$tgz" | sha256sum --check --status \
        || fail "Checksum mismatch for $tgz — refusing to build (got $(sha256sum "$WORK/$tgz" | cut -d' ' -f1))"
    # Kept as downloaded: the source offered with the packages is the very
    # archive they were built from.
    cp "$WORK/$tgz" "$SRC_OUT/"
    tar xzf "$WORK/$tgz" -C "$WORK" || fail "Extract failed: $tgz"
}

# meson build that resolves the previous in-tree libs (they are never installed
# system-wide; we point pkg-config + include/link dirs at their build trees).
NP_DIR=""; UP_DIR=""
build_lib() {
    # build_lib <srcdir> [extra cpp_args] [extra link_args]
    local src="$1" cargs="${2:-}" largs="${3:-}"
    ( cd "$src"
      meson setup build --prefix=/usr --buildtype=release \
          ${cargs:+-Dcpp_args="$cargs"} ${largs:+-Dcpp_link_args="$largs"} >/dev/null
      ninja -C build >/dev/null )
}

stage_and_pack() {
    # stage_and_pack <srcdir> <debname> <version> <depends> [conffiles] [runtime_only] [systemd_unit] [service_user]
    local src="$1" pkg="$2" ver="$3" depends="$4" conffiles="${5:-}" runtime_only="${6:-}" unit="${7:-}" svc_user="${8:-}"
    local stage="$WORK/stage_$pkg"
    rm -rf "$stage"
    DESTDIR="$stage" meson install -C "$src/build" >/dev/null
    # Drop dev artifacts (headers, .pc, bare .so symlink) — runtime package only.
    rm -rf "$stage/usr/include"
    find "$stage" -name "*.pc" -delete 2>/dev/null || true
    if [ "$runtime_only" = "1" ]; then
        find "$stage" -name "*.so" -type l -delete 2>/dev/null || true
    fi

    # systemd unit: meson doesn't install upstream's systemd/<unit>, but the
    # package needs it to be a manageable service (start/enable from the UI).
    local has_unit=false
    if [ -n "$unit" ] && [ -f "$src/systemd/$unit" ]; then
        install -D -m 644 "$src/systemd/$unit" "$stage/lib/systemd/system/$unit"
        has_unit=true
    elif [ -n "$unit" ]; then
        warn "systemd unit '$unit' not found in $src/systemd — package will have no service"
    fi

    mkdir -p "$stage/DEBIAN"
    cat > "$stage/DEBIAN/control" <<CTRL
Package: $pkg
Version: ${ver}-${DEB_REV}
Architecture: arm64
Maintainer: AudioGravity <noreply@audiogravity.app>
Section: sound
Priority: optional
Depends: $depends
Description: $pkg — native arm64 build for AudioGravity
 Rebuilt from upstream source because no official arm64 package exists.
CTRL
    # postinst: refresh linker cache; create the service's system user when one
    # is required (upmpdcli refuses to run as root and needs its own user — the
    # official .deb does the same, hence the 'adduser' dependency); reload
    # systemd when we ship a unit so systemctl sees it immediately.
    {
        printf '#!/bin/sh\nset -e\nldconfig 2>/dev/null || true\n'
        if [ -n "$svc_user" ]; then
            printf "if ! getent passwd %s >/dev/null; then\n" "$svc_user"
            printf "    adduser --system --group --no-create-home \\\\\n"
            printf "        --home /var/lib/%s --shell /usr/sbin/nologin %s\n" "$svc_user" "$svc_user"
            printf "fi\n"
            printf "install -d -o %s -g %s /var/lib/%s /var/cache/%s\n" \
                "$svc_user" "$svc_user" "$svc_user" "$svc_user"
        fi
        if $has_unit; then
            printf 'systemctl daemon-reload 2>/dev/null || true\n'
        fi
    } > "$stage/DEBIAN/postinst"
    chmod 755 "$stage/DEBIAN/postinst"

    # When the package ships a service, stop it before removal (prerm) and
    # disable + daemon-reload after (postrm) — otherwise the running process and
    # the enabled symlink linger after uninstall (the "ghost service" problem).
    if $has_unit; then
        {
            printf '#!/bin/sh\nset -e\n'
            printf 'if [ "$1" = "remove" ] || [ "$1" = "purge" ]; then\n'
            printf "    systemctl stop %s 2>/dev/null || true\n" "$unit"
            printf 'fi\n'
        } > "$stage/DEBIAN/prerm"
        chmod 755 "$stage/DEBIAN/prerm"
        {
            printf '#!/bin/sh\nset -e\n'
            printf 'if [ "$1" = "remove" ] || [ "$1" = "purge" ]; then\n'
            printf "    systemctl disable %s 2>/dev/null || true\n" "$unit"
            printf '    systemctl daemon-reload 2>/dev/null || true\n'
            printf 'fi\n'
        } > "$stage/DEBIAN/postrm"
        chmod 755 "$stage/DEBIAN/postrm"
    fi

    [ -n "$conffiles" ] && printf '%s\n' "$conffiles" > "$stage/DEBIAN/conffiles"
    dpkg-deb --build --root-owner-group "$stage" "$OUT_DIR/${pkg}_${ver}-${DEB_REV}_arm64.deb" >/dev/null
    ok "Built ${pkg}_${ver}-${DEB_REV}_arm64.deb"
}

# ── Build chain ───────────────────────────────────────────────────────────────
mkdir -p "$OUT_DIR"
rm -f "$OUT_DIR"/*.deb "$OUT_DIR/SHA256SUMS"
rm -rf "$SRC_OUT"
mkdir -p "$SRC_OUT"

info "Build dir: $WORK"
echo ""

# 1) libnpupnp
fetch libnpupnp "$LIBNPUPNP_VER" "$LIBNPUPNP_SHA"
NP_DIR="$WORK/libnpupnp-$LIBNPUPNP_VER"
info "Building libnpupnp $LIBNPUPNP_VER..."
build_lib "$NP_DIR"
stage_and_pack "$NP_DIR" "libnpupnp13" "$LIBNPUPNP_VER" "$DEP_LIBNPUPNP" "" 1

# 2) libupnpp (against in-tree libnpupnp)
fetch libupnpp "$LIBUPNPP_VER" "$LIBUPNPP_SHA"
UP_DIR="$WORK/libupnpp-$LIBUPNPP_VER"
info "Building libupnpp $LIBUPNPP_VER..."
export PKG_CONFIG_PATH="$NP_DIR/build/meson-private"
build_lib "$UP_DIR" \
    "-I$NP_DIR/inc -I$NP_DIR/build/inc" \
    "-L$NP_DIR/build -Wl,-rpath-link,$NP_DIR/build"
stage_and_pack "$UP_DIR" "libupnpp17" "$LIBUPNPP_VER" "$DEP_LIBUPNPP" "" 1

# 3) upmpdcli (against in-tree libnpupnp + libupnpp, no Qt5)
fetch upmpdcli "$UPMPDCLI_VER" "$UPMPDCLI_SHA"
UM_DIR="$WORK/upmpdcli-$UPMPDCLI_VER"
info "Building upmpdcli $UPMPDCLI_VER (no Qt5)..."
export PKG_CONFIG_PATH="$NP_DIR/build/meson-private:$UP_DIR/build/meson-private"
build_lib "$UM_DIR" \
    "-I$NP_DIR/inc -I$NP_DIR/build/inc -I$UP_DIR" \
    "-L$UP_DIR/build -L$NP_DIR/build -Wl,-rpath-link,$NP_DIR/build"
stage_and_pack "$UM_DIR" "upmpdcli" "$UPMPDCLI_VER" "$DEP_UPMPDCLI" "/etc/upmpdcli.conf" "" "upmpdcli.service" "upmpdcli"

# ── Checksums ─────────────────────────────────────────────────────────────────
( cd "$OUT_DIR" && sha256sum *.deb > SHA256SUMS )
ok "SHA256SUMS written"

# The script that builds and packages them is part of the corresponding source.
install -m 644 "${BASH_SOURCE[0]}" "$SRC_OUT/$(basename "${BASH_SOURCE[0]}")"
( cd "$SRC_OUT" && sha256sum *.tar.gz *.sh > SHA256SUMS )
ok "Sources kept in $SRC_OUT"

echo ""
echo -e "${GREEN}Build done.${NC} Artifacts in: $OUT_DIR"
ls -1 "$OUT_DIR"

# ── Publish (opt-in) ──────────────────────────────────────────────────────────
# Copies the artifacts into the public landing repo and commits them, but never
# pushes — review + `git push` stay manual, so nothing reaches audiogravity.app
# without an explicit human step.
if $DO_PUBLISH; then
    echo ""
    [ -n "$LANDING_DIR" ] && [ -d "$LANDING_DIR/.git" ] \
        || fail "Landing repo not found. Set AG_LANDING_DIR to the audiogravity.site checkout."
    dest="$LANDING_DIR/$PAGES_SUBDIR"
    info "Publishing to $dest"
    mkdir -p "$dest"
    cp "$OUT_DIR"/*.deb "$OUT_DIR/SHA256SUMS" "$dest/"
    # Replaced as a whole: the sources published must be those of the
    # packages published, not accumulate beside them.
    rm -rf "$dest/source"
    cp -r "$SRC_OUT" "$dest/source"
    ( cd "$LANDING_DIR"
      git add -A "$PAGES_SUBDIR"
      if git diff --cached --quiet; then
          warn "No changes to commit (artifacts identical to what's already published)."
      else
          git commit -q -m "packages: publish upmpdcli arm64 .deb (${UPMPDCLI_VER})"
          ok "Committed in landing repo ($(git rev-parse --short HEAD))"
          echo ""
          echo -e "  ${YELLOW}Manual step:${NC} review and push:"
          echo "    cd $LANDING_DIR && git push"
          echo "  Then available at: https://audiogravity.app/$PAGES_SUBDIR/"
      fi )
else
    echo ""
    echo "To publish on audiogravity.site (public): re-run with --publish"
    echo "  (copies the .deb and their sources into audiogravity.site + commits; you run 'git push')."
fi
echo ""
