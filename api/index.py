from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {
            "name": "Shape Splitting Workbench API",
            "version": "1.0.0",
            "endpoints": [
                "/api/shapes - List available shapes",
                "/api/generate - Generate a shape",
                "/api/splitters - List available splitters",
                "/api/split - Split current mesh",
            ]
        }
        self.wfile.write(json.dumps(response).encode())
