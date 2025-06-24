from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

import prompt_config

TEMPLATES, SLOTS = prompt_config.load_config()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/categories":
            self._send_json(sorted(TEMPLATES.keys()))
        elif parsed.path.startswith("/slots/"):
            category = parsed.path.split("/", 2)[2]
            if category not in SLOTS:
                self.send_error(404, "category not found")
                return
            self._send_json(SLOTS[category])
        else:
            self.send_error(404, "not found")

    def log_message(self, fmt: str, *args) -> None:  # noqa: D401
        """Silence default logging."""
        return

    def _send_json(self, data: object) -> None:
        payload = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = HTTPServer((host, port), Handler)
    server.serve_forever()


if __name__ == "__main__":
    run()
