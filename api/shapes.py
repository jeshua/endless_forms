from http.server import BaseHTTPRequestHandler
import json
import sys
import os
import traceback

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Add api directory to path for imports
            api_dir = os.path.dirname(os.path.abspath(__file__))
            if api_dir not in sys.path:
                sys.path.insert(0, api_dir)

            from geometry import PRIMITIVES

            shapes = {}
            for name, info in PRIMITIVES.items():
                shapes[name] = {
                    "name": info["name"],
                    "description": info.get("description", ""),
                    "params": info.get("params", {}),
                }

            response = {"shapes": shapes}

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            error_msg = f"{str(e)}\n{traceback.format_exc()}"
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": error_msg}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
