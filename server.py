#!/usr/bin/env python3
"""Servidor local simples para visualizar a landing page do Biswatch."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os


class BiswatchHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/health":
            payload = json.dumps({"status": "ok", "service": "biswatch"}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        super().do_GET()

    def log_message(self, format, *args):
        print(f"[Biswatch] {self.address_string()} - {format % args}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), BiswatchHandler)
    print(f"Biswatch disponível em http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        server.server_close()
