"""Serve the Python string practice tasks on localhost."""

import json
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from string_tasks import TASKS, run_task


ROOT = Path(__file__).resolve().parent
FILES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/styles.css": ("styles.css", "text/css; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
}


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/tasks":
            self._send_json(TASKS)
            return

        file_info = FILES.get(self.path)
        if file_info is None:
            self.send_error(404, "Not found")
            return

        filename, content_type = file_info
        content = (ROOT / filename).read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        if self.path != "/api/run":
            self.send_error(404, "Not found")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 65536:
                raise ValueError("Request is too large.")
            request = json.loads(self.rfile.read(length))
            task_id = int(request["task_id"])
            result = run_task(task_id, request.get("values", {}))
            self._send_json({"result": result})
        except (KeyError, TypeError, json.JSONDecodeError, ValueError) as error:
            self._send_json({"error": str(error) or "Invalid request."}, status=400)

    def _send_json(self, value, status=200):
        content = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format_string, *args):
        print(f"[{self.log_date_time_string()}] {format_string % args}")


def main():
    server = None
    for port in range(8000, 8010):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", port), RequestHandler)
            break
        except OSError:
            continue

    if server is None:
        server = ThreadingHTTPServer(("127.0.0.1", 0), RequestHandler)

    address = f"http://127.0.0.1:{server.server_address[1]}"
    print(f"Python String Practice is running at {address}")
    print("Press Ctrl+C to stop the server.")
    threading.Timer(0.8, webbrowser.open, args=(address,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()