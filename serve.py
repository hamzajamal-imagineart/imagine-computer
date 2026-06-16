#!/usr/bin/env python3
"""Static file server WITH HTTP Range support (needed for <video> seeking /
scroll-scrubbing). Python's http.server doesn't handle Range; this does.
Usage: python3 serve.py [port]
"""
import os, sys, http.server, socketserver

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class RangeHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()
        rng = self.headers.get("Range")
        if not rng:
            return super().send_head()
        try:
            size = os.path.getsize(path)
            unit, _, rangespec = rng.partition("=")
            start_s, _, end_s = rangespec.partition("-")
            start = int(start_s) if start_s else 0
            end = int(end_s) if end_s else size - 1
            end = min(end, size - 1)
            length = end - start + 1
            ctype = self.guess_type(path)
            f = open(path, "rb")
            f.seek(start)
            self.send_response(206)
            self.send_header("Content-Type", ctype)
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.send_header("Content-Length", str(length))
            self.end_headers()
            self._range = length
            return f
        except Exception:
            return super().send_head()

    def copyfile(self, source, outputfile):
        remaining = getattr(self, "_range", None)
        if remaining is None:
            return super().copyfile(source, outputfile)
        while remaining > 0:
            chunk = source.read(min(64 * 1024, remaining))
            if not chunk:
                break
            outputfile.write(chunk)
            remaining -= len(chunk)


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


with Server(("127.0.0.1", PORT), RangeHandler) as httpd:
    print(f"Range-capable server on http://127.0.0.1:{PORT}")
    httpd.serve_forever()
