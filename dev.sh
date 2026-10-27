#!/bin/bash
# Audiogravity site — the landing's local server, which serves the working tree as it is.
#
#   ./dev.sh            serve in the foreground (Ctrl-C stops it), as it always has
#   ./dev.sh start      serve in the background, its output in dev.log
#   ./dev.sh stop       stop the server on the port, however it was started
#   ./dev.sh restart    stop it, then start it in the background
#   ./dev.sh status     say whether it runs, and where
#
# Nothing needs a restart to be seen: the server reads each file as it is asked for it.
cd "$(dirname "$0")" || exit 1
SITE_DIR="$(pwd -P)"
LOG_FILE="$SITE_DIR/dev.log"

# Default 8081: on a mono-host box the AG UI (ag-ui-server) already owns 8080.
# Override with PORT=... if needed.
PORT="${PORT:-8081}"

# Detect the LAN IP just for the printed URL (override with AG_DEV_HOST).
# The server itself binds to all interfaces, so it starts regardless of the IP.
HOST="${AG_DEV_HOST:-$(ip route get 1.1.1.1 2>/dev/null | awk '{for (i=1;i<=NF;i++) if ($i=="src") {print $(i+1); exit}}')}"
[ -z "$HOST" ] && HOST=$(hostname -I 2>/dev/null | awk '{print $1}')
[ -z "$HOST" ] && HOST="localhost"
URL="http://${HOST}:${PORT}"

# Whether anything listens on the port.
in_use() { [ -n "$(ss -ltnH "sport = :$PORT" 2>/dev/null)" ]; }

# The servers of this directory on the port. Found by the port, not by a PID file: a server
# started in the foreground, or before these commands existed, has none. Only these are ever
# stopped — whatever else holds the port is left alone.
ours() {
    local pid
    for pid in $(ss -ltnpH "sport = :$PORT" 2>/dev/null | grep -o 'pid=[0-9]*' | cut -d= -f2 | sort -u); do
        [ "$(readlink "/proc/$pid/cwd")" = "$SITE_DIR" ] && echo "$pid"
    done
}

# Wait up to five seconds for the port to be held (up) or free (down).
wait_port() {
    local _
    for _ in $(seq 50); do
        if [ "$1" = up ]; then in_use && return 0; else in_use || return 0; fi
        sleep 0.1
    done
    return 1
}

# Say who holds the port, and stop there.
refuse_busy() {
    if [ -n "$(ours)" ]; then
        echo "Already running: $URL (PID $(ours | xargs))"
        exit 0
    fi
    echo "Port $PORT is held by another program: PORT=<another port> $0 $*" >&2
    exit 1
}

# ThreadingHTTPServer, not HTTPServer: the plain one handles a single connection at a time
# behind a queue of five, so a client that dies mid-request wedges it and every later request
# hangs until it is restarted. A browser opening the landing fires a dozen parallel requests
# for the screenshots alone, and an automated pass over the manual walks it much harder.
serve() {
    in_use && refuse_busy
    echo "Landing page: $URL"
    exec python3 -c "
import http.server, os
os.chdir('$SITE_DIR')
class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/': self.path = '/index.html'
        return super().do_GET()
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(('', $PORT), H).serve_forever()
"
}

start() {
    in_use && refuse_busy start
    # Its own session: it outlives the terminal, and stop ends it alone.
    PORT="$PORT" AG_DEV_HOST="$HOST" setsid "$SITE_DIR/dev.sh" > "$LOG_FILE" 2>&1 < /dev/null &
    if wait_port up && [ -n "$(ours)" ]; then
        echo "Started: $URL (PID $(ours | xargs))"
    else
        echo "Did not start — dev.log:" >&2
        tail -5 "$LOG_FILE" >&2
        exit 1
    fi
}

stop() {
    local pids
    pids=$(ours)
    if [ -z "$pids" ]; then
        if in_use; then echo "Port $PORT is held by another program: left alone"; else echo "Not running"; fi
        return 0
    fi
    kill $pids
    if wait_port down; then
        echo "Stopped"
    else
        echo "Still listening on $PORT (PID $(ours | xargs))" >&2
        exit 1
    fi
}

status() {
    if [ -n "$(ours)" ]; then
        echo "Running: $URL (PID $(ours | xargs))"
    elif in_use; then
        echo "Port $PORT is held by another program"
        return 1
    else
        echo "Not running"
        return 3
    fi
}

usage() { sed -n '2,10s/^# \{0,1\}//p' "$0"; }

case "${1:-}" in
    "")             serve ;;
    start)          start ;;
    stop)           stop ;;
    restart)        stop && start ;;
    status)         status ;;
    help|-h|--help) usage ;;
    *)              echo "Unknown command: $1" >&2; usage >&2; exit 1 ;;
esac
