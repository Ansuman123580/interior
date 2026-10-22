#!/usr/bin/env python3
import os
import sys
import mimetypes
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Register clean MIME types
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("application/javascript", ".mjs")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("font/woff2", ".woff2")
mimetypes.add_type("font/woff", ".woff")
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("image/avif", ".avif")
mimetypes.add_type("image/svg+xml", ".svg")
mimetypes.add_type("video/mp4", ".mp4")
mimetypes.add_type("video/webm", ".webm")
mimetypes.add_type("video/quicktime", ".mov")
mimetypes.add_type("application/json", ".json")

class MultiSiteHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=ROOT_DIR, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def translate_path(self, path):
        clean = path.split("?")[0].split("#")[0]

        # Route media if requested at root /media/
        if clean.startswith("/media/"):
            cand = os.path.join(ROOT_DIR, "dsgninterior.se", "media", clean[7:])
            if os.path.exists(cand):
                return cand

        resolved = super().translate_path(path)
        if not os.path.exists(resolved):
            if os.path.exists(resolved + ".html"):
                return resolved + ".html"
            if os.path.isdir(resolved) and os.path.exists(os.path.join(resolved, "index.html")):
                return os.path.join(resolved, "index.html")

        return resolved

def start_server_on_port(port, directory, name):
    class PortHandler(MultiSiteHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

    server = HTTPServer(("", port), PortHandler)
    print(f"  • {name:<20} : http://localhost:{port}/")
    server.serve_forever()

def main():
    print(f"\n=======================================================")
    print(f"🚀 INTERIOR STUDIOS: STANZZA & DSGN INTERIOR SERVERS")
    print(f"=======================================================")

    servers = [
        (8002, os.path.join(ROOT_DIR, "stanzza.design"), "Stanzza Design"),
        (8004, os.path.join(ROOT_DIR, "dsgninterior.se"), "dsgn interior"),
        (8080, ROOT_DIR, "Launchpad Hub"),
    ]

    threads = []
    for port, path, name in servers:
        t = threading.Thread(target=start_server_on_port, args=(port, path, name), daemon=True)
        t.start()
        threads.append(t)

    print(f"=======================================================\n")
    print("Servers running. Press Ctrl+C to terminate.")
    
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping servers.")

if __name__ == "__main__":
    main()
