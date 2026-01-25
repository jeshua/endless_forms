from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add api directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from splitters import SPLITTERS

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        splitters = {}
        for name, info in SPLITTERS.items():
            splitters[name] = {
                "name": info["name"],
                "description": info.get("description", ""),
                "params": info.get("params", {}),
            }

        response = {"splitters": splitters}
        self.wfile.write(json.dumps(response).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
