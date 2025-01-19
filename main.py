#!/usr/bin/env python3

import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# Import any store classes you want to use
from utils.store import CachedStore, FilePersistentStore
from utils.sharding import ShardedKeyValueStore

# GLOBAL lock and store
STORE_LOCK = threading.Lock()

# Example 1: Use a file-based store alone
# STORE = FilePersistentStore(filename="file_store.json")

# Example 2: Combine multiple stores in a sharded arrangement
STORE = ShardedKeyValueStore([
    FilePersistentStore(filename="file_store.json"),
    CachedStore()
])

class KVHandler(BaseHTTPRequestHandler):
    """
    A simple HTTP handler exposing:
      - GET /kv?key=foo     -> returns single key 'foo', or 404 if missing
      - GET /kv             -> returns all key-value pairs in JSON
      - PUT /kv             -> expects JSON: {"key":"...", "value":"..."}
      - DELETE /kv          -> expects JSON: {"key":"..."}
    """

    def do_GET(self):
        """
        1) GET /kv?key=<key> -> get the value of <key>
        2) GET /kv           -> get all key-value pairs
        """
        parsed_url = urlparse(self.path)
        if parsed_url.path.strip("/") != "kv":
            return self._send_response(404, b'{"error": "Invalid path"}')

        # Check if user provided ?key=someKey
        query_params = parse_qs(parsed_url.query)
        key = query_params.get("key", [None])[0]

        if key:
            # Return a single key
            with STORE_LOCK:
                value = STORE.get(key)
            if value is not None:
                payload = json.dumps({key: value}).encode("utf-8")
                self._send_response(200, payload)
            else:
                self._send_response(404, b'{"error": "Key not found"}')
        else:
            # Return all pairs
            with STORE_LOCK:
                all_data = STORE.all_keys() if hasattr(STORE, "all_keys") else STORE.all()
                # If using ShardedKeyValueStore, "all_keys()" might retrieve everything
                # otherwise "all()" from a single store
            payload = json.dumps(all_data).encode("utf-8")
            self._send_response(200, payload)

    def do_PUT(self):
        """
        PUT /kv
        Body: {"key":"someKey","value":"someValue"}
        """
        parsed_url = urlparse(self.path)
        if parsed_url.path.strip("/") != "kv":
            return self._send_response(404, b'{"error":"Invalid path"}')

        content_length = int(self.headers.get("Content-Length", 0))
        body_data = self.rfile.read(content_length).decode("utf-8")
        try:
            payload = json.loads(body_data)
            key = payload.get("key")
            value = payload.get("value")
            if not key or value is None:
                return self._send_response(400, b'{"error":"Missing key or value"}')
            
            with STORE_LOCK:
                STORE.set(key, value)
            
            response = json.dumps({key: value}).encode("utf-8")
            self._send_response(200, response)
        except json.JSONDecodeError:
            self._send_response(400, b'{"error":"Invalid JSON"}')

    def do_DELETE(self):
        """
        DELETE /kv
        Body: {"key":"someKey"}
        """
        parsed_url = urlparse(self.path)
        if parsed_url.path.strip("/") != "kv":
            return self._send_response(404, b'{"error":"Invalid path"}')

        content_length = int(self.headers.get("Content-Length", 0))
        body_data = self.rfile.read(content_length).decode("utf-8")
        try:
            payload = json.loads(body_data)
            key = payload.get("key")
            if not key:
                return self._send_response(400, b'{"error":"Missing key"}')
            
            with STORE_LOCK:
                old_value = STORE.get(key)
                if old_value is not None:
                    STORE.delete(key)
                    self._send_response(200, b'{"result":"Key deleted"}')
                else:
                    self._send_response(404, b'{"error":"Key not found"}')
        except json.JSONDecodeError:
            self._send_response(400, b'{"error":"Invalid JSON"}')

    def _send_response(self, code, payload, content_type="application/json"):
        """Helper method to send an HTTP response with status code, body, and content type."""
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(payload)

def run_server(host="0.0.0.0", port=8080):
    """Starts the HTTP server on the given host and port."""
    server = HTTPServer((host, port), KVHandler)
    print(f"px-kvstore running at http://{host}:{port}")
    server.serve_forever()

def cli():
    """If you install this package and run 'px-kvstore', this function is called."""
    run_server()

if __name__ == "__main__":
    # Optionally accept a port from the command line, e.g. python main.py 9090
    if len(sys.argv) > 1:
        try:
            user_port = int(sys.argv[1])
            run_server(port=user_port)
        except ValueError:
            print("Usage: python main.py [port]")
    else:
        run_server()
