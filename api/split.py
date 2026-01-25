from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add api directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from geometry import PRIMITIVES
from splitters import SPLITTERS

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

# Store current mesh in memory (note: serverless functions are stateless,
# so we need to regenerate or receive the mesh each time)
current_mesh = None

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        global current_mesh

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
            strategy = data.get('strategy', 'voronoi')
            num_parts = data.get('num_parts', 3)
            params = data.get('params', {})

            # Get shape info to regenerate mesh (since serverless is stateless)
            shape_type = data.get('shape_type', 'diamond')
            shape_params = data.get('shape_params', {})

            if strategy not in SPLITTERS:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"detail": f"Unknown splitter: {strategy}"}).encode())
                return

            # Generate the mesh first
            if shape_type in PRIMITIVES:
                generator = PRIMITIVES[shape_type]["generator"]
                current_mesh = generator(**shape_params)
            else:
                # Default to diamond if no valid shape
                current_mesh = PRIMITIVES["diamond"]["generator"]()

            # Get the splitter and split the mesh
            splitter_class = SPLITTERS[strategy]["class"]
            splitter = splitter_class()
            parts = splitter.split(current_mesh, num_parts, **params)

            # Convert parts to response format
            mesh_parts = []
            for i, part in enumerate(parts):
                if part is not None and len(part.vertices) > 0:
                    mesh_parts.append(mesh_to_gltf_json(part, f"part_{i}"))

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            response = {
                "strategy": strategy,
                "num_parts": len(mesh_parts),
                "mesh": {"parts": mesh_parts},
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
