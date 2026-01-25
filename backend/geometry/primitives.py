"""
Primitive shape generators for the splitting workbench.

Provides: kite (deltoid prism), diamond (octahedron), and sphere.
"""

import numpy as np
import trimesh


def create_kite(width: float = 50, height: float = 70, depth: float = 20) -> trimesh.Trimesh:
    """
    Create a kite-shaped prism (deltoid cross-section extruded).

    A kite has two pairs of adjacent sides that are equal.
    The cross-section is a deltoid/arrowhead shape.

    Args:
        width: Width of the kite at its widest point
        height: Total height of the kite
        depth: Extrusion depth (thickness)

    Returns:
        trimesh.Trimesh: The kite prism mesh
    """
    # Define kite vertices in 2D (XY plane)
    # Kite shape: top point, right point, bottom point, left point
    # The horizontal axis is at 1/3 from top for classic kite proportions
    top_y = height / 2
    bottom_y = -height / 2
    side_y = height / 6  # Slightly above center

    # 2D profile vertices (counterclockwise)
    profile = np.array([
        [0, top_y],           # Top point
        [width / 2, side_y],  # Right point
        [0, bottom_y],        # Bottom point
        [-width / 2, side_y], # Left point
    ])

    # Create front and back faces
    z_front = depth / 2
    z_back = -depth / 2

    # 8 vertices: 4 front + 4 back
    vertices = np.zeros((8, 3))
    vertices[:4, :2] = profile
    vertices[:4, 2] = z_front
    vertices[4:, :2] = profile
    vertices[4:, 2] = z_back

    # Define faces (triangles, counterclockwise when viewed from outside)
    faces = [
        # Front face (2 triangles)
        [0, 1, 2],
        [0, 2, 3],
        # Back face (2 triangles, reversed winding)
        [4, 6, 5],
        [4, 7, 6],
        # Side faces (8 triangles for 4 edges)
        # Top-right edge
        [0, 5, 1],
        [0, 4, 5],
        # Right-bottom edge
        [1, 6, 2],
        [1, 5, 6],
        # Bottom-left edge
        [2, 7, 3],
        [2, 6, 7],
        # Left-top edge
        [3, 4, 0],
        [3, 7, 4],
    ]

    mesh = trimesh.Trimesh(vertices=vertices, faces=np.array(faces))
    mesh.fix_normals()
    return mesh


def create_diamond(size: float = 50, aspect: float = 1.5) -> trimesh.Trimesh:
    """
    Create a diamond shape (octahedron/bipyramid).

    This is a classic gem-like polyhedron with 8 triangular faces.

    Args:
        size: Distance from center to the equatorial vertices
        aspect: Ratio of height to width (1.0 = regular octahedron)

    Returns:
        trimesh.Trimesh: The diamond/octahedron mesh
    """
    # Octahedron vertices: 6 points along axes
    half_height = size * aspect

    vertices = np.array([
        [0, 0, half_height],     # Top
        [size, 0, 0],            # +X
        [0, size, 0],            # +Y
        [-size, 0, 0],           # -X
        [0, -size, 0],           # -Y
        [0, 0, -half_height],    # Bottom
    ])

    # 8 triangular faces
    faces = np.array([
        # Top pyramid
        [0, 1, 2],
        [0, 2, 3],
        [0, 3, 4],
        [0, 4, 1],
        # Bottom pyramid
        [5, 2, 1],
        [5, 3, 2],
        [5, 4, 3],
        [5, 1, 4],
    ])

    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.fix_normals()
    return mesh


def create_sphere(radius: float = 30, subdivisions: int = 3) -> trimesh.Trimesh:
    """
    Create a smooth sphere using icosphere subdivision.

    Args:
        radius: Radius of the sphere
        subdivisions: Number of subdivision iterations (more = smoother)

    Returns:
        trimesh.Trimesh: The sphere mesh
    """
    return trimesh.creation.icosphere(radius=radius, subdivisions=subdivisions)


def create_cube(size: float = 50) -> trimesh.Trimesh:
    """
    Create a simple cube.

    Args:
        size: Side length of the cube

    Returns:
        trimesh.Trimesh: The cube mesh
    """
    return trimesh.creation.box(extents=[size, size, size])


def create_cylinder(radius: float = 25, height: float = 60, sections: int = 32) -> trimesh.Trimesh:
    """
    Create a cylinder.

    Args:
        radius: Radius of the cylinder
        height: Height of the cylinder
        sections: Number of radial sections

    Returns:
        trimesh.Trimesh: The cylinder mesh
    """
    return trimesh.creation.cylinder(radius=radius, height=height, sections=sections)


def create_star(outer_radius: float = 50, inner_radius: float = 20, points: int = 5, depth: float = 15) -> trimesh.Trimesh:
    """
    Create a star-shaped prism (extruded star polygon).

    Great for puppets - splits naturally into pointed sections.

    Args:
        outer_radius: Radius to outer points
        inner_radius: Radius to inner valleys
        points: Number of points (5 = classic star)
        depth: Extrusion depth

    Returns:
        trimesh.Trimesh: The star prism mesh
    """
    from shapely.geometry import Polygon

    # Generate star polygon vertices
    angles = np.linspace(0, 2 * np.pi, points * 2, endpoint=False)
    # Rotate so one point faces up
    angles = angles + np.pi / 2

    profile = []
    for i, angle in enumerate(angles):
        r = outer_radius if i % 2 == 0 else inner_radius
        profile.append([r * np.cos(angle), r * np.sin(angle)])

    # Create a shapely polygon and extrude it
    polygon = Polygon(profile)
    mesh = trimesh.creation.extrude_polygon(polygon, height=depth)

    # Center the mesh vertically
    mesh.vertices[:, 2] -= depth / 2

    mesh.fix_normals()
    return mesh


def create_heart(width: float = 60, height: float = 55, depth: float = 20) -> trimesh.Trimesh:
    """
    Create a heart-shaped prism.

    Classic emotional shape, good for asymmetric splits.

    Args:
        width: Width of the heart
        height: Height of the heart
        depth: Extrusion depth

    Returns:
        trimesh.Trimesh: The heart prism mesh
    """
    # Heart shape using parametric curve
    t = np.linspace(0, 2 * np.pi, 40)
    # Heart parametric equations
    x = 16 * np.sin(t) ** 3
    y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)

    # Scale to desired size
    x = x * (width / 32)
    y = y * (height / 30)

    profile = np.column_stack([x, y])
    n_verts = len(profile)

    # Create front and back faces
    z_front = depth / 2
    z_back = -depth / 2

    vertices = np.zeros((n_verts * 2, 3))
    vertices[:n_verts, :2] = profile
    vertices[:n_verts, 2] = z_front
    vertices[n_verts:, :2] = profile
    vertices[n_verts:, 2] = z_back

    # Triangulate using fan from center
    faces = []
    # Front face
    for i in range(1, n_verts - 1):
        faces.append([0, i, i + 1])
    # Back face (reversed)
    for i in range(1, n_verts - 1):
        faces.append([n_verts, n_verts + i + 1, n_verts + i])
    # Side faces
    for i in range(n_verts):
        next_i = (i + 1) % n_verts
        faces.append([i, next_i, next_i + n_verts])
        faces.append([i, next_i + n_verts, i + n_verts])

    mesh = trimesh.Trimesh(vertices=vertices, faces=np.array(faces))
    mesh.fix_normals()
    return mesh


def create_humanoid(height: float = 80, width: float = 60, depth: float = 15) -> trimesh.Trimesh:
    """
    Create a gingerbread-man style humanoid silhouette.

    Classic puppet shape with head, body, arms, and legs.

    Args:
        height: Total height
        width: Width at arms
        depth: Extrusion depth

    Returns:
        trimesh.Trimesh: The humanoid prism mesh
    """
    h = height / 2
    w = width / 2

    # Define humanoid profile (simplified gingerbread man)
    profile = np.array([
        # Head (top)
        [0, h],
        [w * 0.25, h * 0.85],
        [w * 0.25, h * 0.65],
        # Right arm
        [w, h * 0.5],
        [w, h * 0.35],
        [w * 0.35, h * 0.25],
        # Right side body
        [w * 0.35, h * 0.1],
        # Right leg
        [w * 0.4, -h * 0.3],
        [w * 0.4, -h],
        [w * 0.1, -h],
        [w * 0.1, -h * 0.3],
        # Crotch
        [0, -h * 0.2],
        # Left leg
        [-w * 0.1, -h * 0.3],
        [-w * 0.1, -h],
        [-w * 0.4, -h],
        [-w * 0.4, -h * 0.3],
        # Left side body
        [-w * 0.35, h * 0.1],
        [-w * 0.35, h * 0.25],
        # Left arm
        [-w, h * 0.35],
        [-w, h * 0.5],
        [-w * 0.25, h * 0.65],
        [-w * 0.25, h * 0.85],
    ])

    n_verts = len(profile)
    z_front = depth / 2
    z_back = -depth / 2

    vertices = np.zeros((n_verts * 2, 3))
    vertices[:n_verts, :2] = profile
    vertices[:n_verts, 2] = z_front
    vertices[n_verts:, :2] = profile
    vertices[n_verts:, 2] = z_back

    # Triangulate front and back
    faces = []
    for i in range(1, n_verts - 1):
        faces.append([0, i, i + 1])
    for i in range(1, n_verts - 1):
        faces.append([n_verts, n_verts + i + 1, n_verts + i])
    # Side faces
    for i in range(n_verts):
        next_i = (i + 1) % n_verts
        faces.append([i, next_i, next_i + n_verts])
        faces.append([i, next_i + n_verts, i + n_verts])

    mesh = trimesh.Trimesh(vertices=vertices, faces=np.array(faces))
    mesh.fix_normals()
    return mesh


def create_crescent(outer_radius: float = 40, thickness: float = 15, depth: float = 15) -> trimesh.Trimesh:
    """
    Create a crescent moon shape.

    Mystical shape with interesting curved splits.

    Args:
        outer_radius: Outer curve radius
        thickness: Thickness of the crescent
        depth: Extrusion depth

    Returns:
        trimesh.Trimesh: The crescent prism mesh
    """
    from shapely.geometry import Polygon

    # Outer arc
    outer_angles = np.linspace(-np.pi * 0.7, np.pi * 0.7, 30)
    outer_x = outer_radius * np.cos(outer_angles)
    outer_y = outer_radius * np.sin(outer_angles)

    # Inner arc (offset circle to create crescent)
    inner_radius = outer_radius - thickness * 0.3
    offset = thickness * 0.7
    inner_angles = np.linspace(np.pi * 0.7, -np.pi * 0.7, 25)
    inner_x = inner_radius * np.cos(inner_angles) + offset
    inner_y = inner_radius * np.sin(inner_angles)

    # Combine into closed profile
    profile_x = np.concatenate([outer_x, inner_x])
    profile_y = np.concatenate([outer_y, inner_y])
    profile = list(zip(profile_x, profile_y))

    # Create a shapely polygon and extrude it
    polygon = Polygon(profile)
    mesh = trimesh.creation.extrude_polygon(polygon, height=depth)

    # Center the mesh vertically
    mesh.vertices[:, 2] -= depth / 2

    mesh.fix_normals()
    return mesh


def create_hexagon(radius: float = 40, depth: float = 20) -> trimesh.Trimesh:
    """
    Create a regular hexagon prism.

    Geometric shape that splits evenly into 6 sections.

    Args:
        radius: Radius to vertices
        depth: Extrusion depth

    Returns:
        trimesh.Trimesh: The hexagon prism mesh
    """
    # Regular hexagon vertices
    angles = np.linspace(0, 2 * np.pi, 6, endpoint=False)
    angles = angles + np.pi / 6  # Flat side at bottom

    profile = np.column_stack([
        radius * np.cos(angles),
        radius * np.sin(angles)
    ])

    n_verts = 6
    z_front = depth / 2
    z_back = -depth / 2

    vertices = np.zeros((12, 3))
    vertices[:6, :2] = profile
    vertices[:6, 2] = z_front
    vertices[6:, :2] = profile
    vertices[6:, 2] = z_back

    faces = [
        # Front face
        [0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 5],
        # Back face
        [6, 8, 7], [6, 9, 8], [6, 10, 9], [6, 11, 10],
        # Side faces
        [0, 7, 1], [0, 6, 7],
        [1, 8, 2], [1, 7, 8],
        [2, 9, 3], [2, 8, 9],
        [3, 10, 4], [3, 9, 10],
        [4, 11, 5], [4, 10, 11],
        [5, 6, 0], [5, 11, 6],
    ]

    mesh = trimesh.Trimesh(vertices=vertices, faces=np.array(faces))
    mesh.fix_normals()
    return mesh


# Registry of available primitives with their default parameters
PRIMITIVES = {
    "kite": {
        "function": create_kite,
        "params": {
            "width": {"default": 50, "min": 10, "max": 200, "step": 5},
            "height": {"default": 70, "min": 10, "max": 200, "step": 5},
            "depth": {"default": 20, "min": 5, "max": 100, "step": 5},
        },
        "description": "Kite-shaped prism (deltoid cross-section)",
    },
    "diamond": {
        "function": create_diamond,
        "params": {
            "size": {"default": 50, "min": 10, "max": 200, "step": 5},
            "aspect": {"default": 1.5, "min": 0.5, "max": 3.0, "step": 0.1},
        },
        "description": "Diamond/octahedron shape",
    },
    "sphere": {
        "function": create_sphere,
        "params": {
            "radius": {"default": 30, "min": 10, "max": 100, "step": 5},
            "subdivisions": {"default": 3, "min": 1, "max": 5, "step": 1},
        },
        "description": "Smooth icosphere",
    },
    "cube": {
        "function": create_cube,
        "params": {
            "size": {"default": 50, "min": 10, "max": 200, "step": 5},
        },
        "description": "Simple cube",
    },
    "cylinder": {
        "function": create_cylinder,
        "params": {
            "radius": {"default": 25, "min": 5, "max": 100, "step": 5},
            "height": {"default": 60, "min": 10, "max": 200, "step": 5},
            "sections": {"default": 32, "min": 8, "max": 64, "step": 4},
        },
        "description": "Cylinder with configurable radius and height",
    },
    "star": {
        "function": create_star,
        "params": {
            "outer_radius": {"default": 50, "min": 20, "max": 100, "step": 5},
            "inner_radius": {"default": 20, "min": 5, "max": 50, "step": 5},
            "points": {"default": 5, "min": 3, "max": 8, "step": 1},
            "depth": {"default": 15, "min": 5, "max": 50, "step": 5},
        },
        "description": "Star shape - splits into pointed sections",
    },
    "crescent": {
        "function": create_crescent,
        "params": {
            "outer_radius": {"default": 40, "min": 20, "max": 80, "step": 5},
            "thickness": {"default": 15, "min": 5, "max": 40, "step": 5},
            "depth": {"default": 15, "min": 5, "max": 40, "step": 5},
        },
        "description": "Crescent moon - mystical curved shape",
    },
    "hexagon": {
        "function": create_hexagon,
        "params": {
            "radius": {"default": 40, "min": 15, "max": 80, "step": 5},
            "depth": {"default": 20, "min": 5, "max": 50, "step": 5},
        },
        "description": "Hexagon prism - splits evenly into 6 parts",
    },
}
