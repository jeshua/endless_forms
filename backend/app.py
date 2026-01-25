"""
FastAPI backend for the Shape Splitting Workbench.

Provides endpoints for:
- Generating primitive shapes
- Splitting meshes using various algorithms
- Exporting results as STL/glTF
"""

import io
import json
import base64
from typing import Any

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
import numpy as np
import trimesh

from geometry import PRIMITIVES, create_kite, create_diamond, create_sphere
from splitters import SPLITTERS


app = FastAPI(
    title="Shape Splitting Workbench",
    description="API for generating and splitting 3D shapes",
    version="1.0.0",
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for current mesh and parts
current_state = {
    "mesh": None,
    "parts": [],
}


class ShapeRequest(BaseModel):
    """Request to generate a primitive shape."""
    shape_type: str
    params: dict[str, Any] = {}


class SplitRequest(BaseModel):
    """Request to split a mesh."""
    strategy: str
    num_parts: int = 3
    params: dict[str, Any] = {}
    mesh_data: str | None = None  # Base64 encoded STL or None to use current


class ExportRequest(BaseModel):
    """Request to export mesh(es)."""
    format: str = "stl"  # stl or gltf
    part_index: int | None = None  # None = all parts


def mesh_to_gltf_json(mesh: trimesh.Trimesh, name: str = "mesh") -> dict:
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
        "centroid": mesh.centroid.tolist(),
    }


def meshes_to_gltf_json(meshes: list[trimesh.Trimesh], names: list[str] | None = None) -> dict:
    """Convert multiple meshes to glTF-compatible JSON."""
    if names is None:
        names = [f"part_{i}" for i in range(len(meshes))]

    parts = []
    for mesh, name in zip(meshes, names):
        parts.append(mesh_to_gltf_json(mesh, name))

    # Calculate overall bounds
    if meshes:
        all_bounds_min = np.min([m.bounds[0] for m in meshes], axis=0)
        all_bounds_max = np.max([m.bounds[1] for m in meshes], axis=0)
    else:
        all_bounds_min = [0, 0, 0]
        all_bounds_max = [0, 0, 0]

    return {
        "parts": parts,
        "bounds": {
            "min": all_bounds_min.tolist() if isinstance(all_bounds_min, np.ndarray) else all_bounds_min,
            "max": all_bounds_max.tolist() if isinstance(all_bounds_max, np.ndarray) else all_bounds_max,
        },
    }


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "Shape Splitting Workbench API",
        "version": "1.0.0",
        "endpoints": [
            "/shapes - List available shapes",
            "/shapes/generate - Generate a shape",
            "/splitters - List available splitters",
            "/split - Split current mesh",
            "/export - Export mesh(es)",
        ],
    }


@app.get("/shapes")
async def list_shapes():
    """List available primitive shapes and their parameters."""
    shapes = {}
    for name, info in PRIMITIVES.items():
        shapes[name] = {
            "description": info["description"],
            "params": info["params"],
        }
    return {"shapes": shapes}


@app.post("/shapes/generate")
async def generate_shape(request: ShapeRequest):
    """Generate a primitive shape."""
    if request.shape_type not in PRIMITIVES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown shape type: {request.shape_type}. Available: {list(PRIMITIVES.keys())}",
        )

    primitive_info = PRIMITIVES[request.shape_type]
    func = primitive_info["function"]

    # Filter params to only include valid ones
    valid_params = {}
    for key, value in request.params.items():
        if key in primitive_info["params"]:
            valid_params[key] = value

    try:
        mesh = func(**valid_params)
        current_state["mesh"] = mesh
        current_state["parts"] = [mesh]

        return {
            "success": True,
            "mesh": mesh_to_gltf_json(mesh, request.shape_type),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/splitters")
async def list_splitters():
    """List available splitting algorithms and their parameters."""
    splitters = {}
    for name, cls in SPLITTERS.items():
        instance = cls()
        splitters[name] = {
            "name": instance.name,
            "description": instance.description,
            "params": instance.get_parameters(),
        }
    return {"splitters": splitters}


@app.post("/split")
async def split_mesh(request: SplitRequest):
    """Split a mesh using the specified strategy."""
    # Get mesh to split
    if request.mesh_data:
        # Decode uploaded mesh
        try:
            mesh_bytes = base64.b64decode(request.mesh_data)
            mesh = trimesh.load(io.BytesIO(mesh_bytes), file_type="stl")
            if isinstance(mesh, trimesh.Scene):
                mesh = mesh.dump(concatenate=True)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to load mesh: {e}")
    elif current_state["mesh"] is not None:
        mesh = current_state["mesh"]
    else:
        raise HTTPException(
            status_code=400,
            detail="No mesh available. Generate a shape or upload a mesh first.",
        )

    # Get splitter
    if request.strategy not in SPLITTERS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown strategy: {request.strategy}. Available: {list(SPLITTERS.keys())}",
        )

    splitter_cls = SPLITTERS[request.strategy]
    splitter = splitter_cls(num_parts=request.num_parts)

    try:
        parts = splitter.split(mesh, **request.params)
        current_state["parts"] = parts

        return {
            "success": True,
            "num_parts": len(parts),
            "mesh": meshes_to_gltf_json(parts),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Splitting failed: {e}")


@app.post("/upload")
async def upload_mesh(file: UploadFile = File(...)):
    """Upload a mesh file (STL, OBJ, etc.)."""
    try:
        contents = await file.read()

        # Determine file type from extension
        filename = file.filename or "mesh.stl"
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "stl"

        mesh = trimesh.load(io.BytesIO(contents), file_type=ext)
        if isinstance(mesh, trimesh.Scene):
            mesh = mesh.dump(concatenate=True)

        current_state["mesh"] = mesh
        current_state["parts"] = [mesh]

        return {
            "success": True,
            "filename": filename,
            "mesh": mesh_to_gltf_json(mesh, filename),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to load mesh: {e}")


@app.post("/export")
async def export_mesh(request: ExportRequest):
    """Export mesh(es) in the specified format."""
    parts = current_state["parts"]

    if not parts:
        raise HTTPException(status_code=400, detail="No mesh parts to export")

    # Select parts to export
    if request.part_index is not None:
        if request.part_index < 0 or request.part_index >= len(parts):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid part index: {request.part_index}. Available: 0-{len(parts)-1}",
            )
        meshes_to_export = [parts[request.part_index]]
        filename = f"part_{request.part_index}"
    else:
        meshes_to_export = parts
        filename = "all_parts"

    try:
        if request.format.lower() == "stl":
            # Combine all meshes for STL export
            if len(meshes_to_export) > 1:
                combined = trimesh.util.concatenate(meshes_to_export)
            else:
                combined = meshes_to_export[0]

            stl_data = combined.export(file_type="stl")
            return Response(
                content=stl_data,
                media_type="application/octet-stream",
                headers={"Content-Disposition": f"attachment; filename={filename}.stl"},
            )

        elif request.format.lower() == "gltf":
            # Export as glTF scene
            scene = trimesh.Scene()
            for i, mesh in enumerate(meshes_to_export):
                scene.add_geometry(mesh, node_name=f"part_{i}")

            gltf_data = scene.export(file_type="gltf")
            return Response(
                content=gltf_data,
                media_type="model/gltf+json",
                headers={"Content-Disposition": f"attachment; filename={filename}.gltf"},
            )

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported format: {request.format}. Use 'stl' or 'gltf'.",
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {e}")


@app.get("/current")
async def get_current_state():
    """Get the current mesh state."""
    if current_state["mesh"] is None:
        return {"has_mesh": False, "parts": []}

    return {
        "has_mesh": True,
        "num_parts": len(current_state["parts"]),
        "mesh": meshes_to_gltf_json(current_state["parts"]),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
