#!/bin/bash
cd "$(dirname "$0")"

# Default 8081: on a mono-host box the AG UI (ag-ui-server) already owns 8080.
# Override with PORT=... if needed.
PORT="${PORT:-8081}"

# Detect the LAN IP just for the printed URL (override with AG_DEV_HOST).
# The server itself binds to all interfaces, so it starts regardless of the IP.
HOST="${AG_DEV_HOST:-$(ip route get 1.1.1.1 2>/dev/null | awk '{for (i=1;i<=NF;i++) if ($i=="src") {print $(i+1); exit}}')}"
[ -z "$HOST" ] && HOST=$(hostname -I 2>/dev/null | awk '{print $1}')
[ -z "$HOST" ] && HOST="localhost"

echo "Landing page: http://${HOST}:${PORT}"

# ThreadingHTTPServer, not HTTPServer: the plain one handles a single connection at a time
# behind a queue of five, so a client that dies mid-request wedges it and every later request
# hangs until it is restarted. A browser opening the landing fires a dozen parallel requests
# for the screenshots alone, and an automated pass over the manual walks it much harder.
python3 -c "
import http.server, os
os.chdir('$(dirname "$0")')
class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/': self.path = '/index.html'
        return super().do_GET()
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(('', $PORT), H).serve_forever()
"
