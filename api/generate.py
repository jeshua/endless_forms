from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add api directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from geometry import PRIMITIVES

def mesh_to_gltf_json(mesh, name="mesh"):
    """Convert a trimesh to a simple glTF-compatible JSON structure."""
    vertices = mesh.vertices.flatten().tolist()
    normals = mesh.vertex_normals.flatten().tolist()
    indices = mesh.faces.flatten().tolist()

    return {
        "name": name,
        "vertices": vertices,
        "normals": normals,
        "indices": indices,
        "bounds": {
            "min": mesh.bounds[0].tolist(),
            "max": mesh.bounds[1].tolist(),
        },
    }

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
            shape_type = data.get('shape_type', 'diamond')
            params = data.get('params', {})

            if shape_type not in PRIMITIVES:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"detail": f"Unknown shape type: {shape_type}"}).encode())
                return

            # Generate the shape
            generator = PRIMITIVES[shape_type]["generator"]
            mesh = generator(**params)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            response = {
                "shape_type": shape_type,
                "mesh": mesh_to_gltf_json(mesh),
                "num_parts": 1,
            }
            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"detail": str(e)}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
