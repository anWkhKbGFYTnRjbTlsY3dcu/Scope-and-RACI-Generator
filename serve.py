"""
Serves the project over localhost so Chrome remembers mic permission.
Shuts down automatically when the browser tab is closed.
"""
import http.server
import socketserver
import webbrowser
import threading
import os
import json
import time

PORT = 8765
FILE = "project_scope_form.html"
HEARTBEAT_TIMEOUT = 8  # seconds — shut down if no ping received

os.chdir(os.path.dirname(os.path.abspath(__file__)))

last_ping = time.time()
server_ref = None


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self._cors(200)

    def do_GET(self):
        global last_ping
        if self.path == "/api/alive":
            self._json({"status": "ok"})
        elif self.path == "/api/ping":
            last_ping = time.time()
            self._json({"status": "ok"})
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/shutdown":
            self._json({"status": "shutting down"})
            threading.Thread(target=server_ref.shutdown, daemon=True).start()
        else:
            self.send_error(404)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()

    def _cors(self, code):
        self.send_response(code)
        self.end_headers()

    def _json(self, data):
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass  # silence request logs


def watchdog():
    """Shut down if no heartbeat received within HEARTBEAT_TIMEOUT seconds."""
    # Give the browser time to open before we start watching
    time.sleep(HEARTBEAT_TIMEOUT * 2)
    while True:
        time.sleep(2)
        if time.time() - last_ping > HEARTBEAT_TIMEOUT:
            print("\nTab closed — shutting down server.")
            server_ref.shutdown()
            break


def open_browser():
    webbrowser.open(f"http://localhost:{PORT}/{FILE}")


print(f"  Serving at http://localhost:{PORT}/{FILE}")
print("  Server will stop automatically when the tab is closed.")
print("  Press Ctrl+C to stop manually.\n")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.allow_reuse_address = True
    server_ref = httpd
    threading.Timer(0.6, open_browser).start()
    threading.Thread(target=watchdog, daemon=True).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
