"""
Radial mesh splitting.

Splits mesh from centroid outward using radial planes like pizza slices.
"""

from typing import Any
import numpy as np
import trimesh

from .base import BaseSplitter


class RadialSplitter(BaseSplitter):
    """Split mesh using radial planes from center."""

    @property
    def name(self) -> str:
        return "Radial"

    @property
    def description(self) -> str:
        return "Split into wedge-shaped sectors from center (like pizza slices)"

    def get_parameters(self) -> dict[str, dict[str, Any]]:
        return {
            "axis": {
                "type": "select",
                "default": "z",
                "options": ["x", "y", "z"],
                "description": "Axis of rotation (perpendicular to cut planes)",
            },
            "start_angle": {
                "type": "float",
                "default": 0.0,
                "min": 0.0,
                "max": 360.0,
                "step": 15.0,
                "description": "Starting angle offset in degrees",
            },
            "use_centroid": {
                "type": "bool",
                "default": True,
                "description": "Use mesh centroid as center",
            },
        }

    def split(self, mesh: trimesh.Trimesh, **params) -> list[trimesh.Trimesh]:
        """
        Split mesh into radial wedges.

        Args:
            mesh: Input mesh
            axis: Rotation axis ('x', 'y', or 'z')
            start_angle: Starting angle offset in degrees
            use_centroid: Whether to use mesh centroid as center

        Returns:
            List of wedge-shaped mesh parts
        """
        if not self.validate_mesh(mesh):
            return []

        axis = params.get("axis", "z")
        start_angle = params.get("start_angle", 0.0)
        use_centroid = params.get("use_centroid", True)

        # Determine center point
        if use_centroid:
            center = mesh.centroid
        else:
            center = (mesh.bounds[0] + mesh.bounds[1]) / 2

        # Get axis vectors
        axis_map = {
            "x": (np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])),
            "y": (np.array([0, 1, 0]), np.array([0, 0, 1]), np.array([1, 0, 0])),
            "z": (np.array([0, 0, 1]), np.array([1, 0, 0]), np.array([0, 1, 0])),
        }
        rot_axis, u_axis, v_axis = axis_map.get(axis, axis_map["z"])

        # Calculate angles for radial cuts
        angle_step = 2 * np.pi / self.num_parts
        start_rad = np.radians(start_angle)

        parts = []
        remaining = mesh.copy()

        for i in range(self.num_parts):
            angle = start_rad + i * angle_step

            # Create cutting plane normal (perpendicular to rot_axis, at this angle)
            # Normal rotates around rot_axis
            normal = np.cos(angle) * u_axis + np.sin(angle) * v_axis

            if i < self.num_parts - 1:
                # Cut and keep the "right" side of this plane
                try:
                    # First cut: keep the side where we accumulate parts
                    next_angle = start_rad + (i + 1) * angle_step
                    next_normal = np.cos(next_angle) * u_axis + np.sin(next_angle) * v_axis

                    # Create a wedge by intersecting with two halfspaces
                    wedge = remaining.copy()

                    # Cut 1: keep points where normal . (x - center) >= 0
                    wedge = wedge.slice_plane(center, -normal, cap=True)
                    if wedge is None or len(wedge.vertices) == 0:
                        continue

                    # Cut 2: keep points where next_normal . (x - center) <= 0
                    wedge = wedge.slice_plane(center, next_normal, cap=True)
                    if wedge is None or len(wedge.vertices) == 0:
                        continue

                    parts.append(wedge)

                except Exception:
                    continue
            else:
                # Last wedge: everything remaining after all previous cuts
                # Apply both boundary planes
                try:
                    wedge = remaining.copy()

                    # Cut 1: first boundary
                    wedge = wedge.slice_plane(center, -normal, cap=True)
                    if wedge is None or len(wedge.vertices) == 0:
                        continue

                    # Cut 2: wrap around to first angle
                    first_normal = np.cos(start_rad) * u_axis + np.sin(start_rad) * v_axis
                    wedge = wedge.slice_plane(center, first_normal, cap=True)
                    if wedge is not None and len(wedge.vertices) > 0:
                        parts.append(wedge)

                except Exception:
                    continue

        # Fallback if radial splitting failed
        if len(parts) < 2:
            from .plane import PlaneSplitter
            fallback = PlaneSplitter(self.num_parts)
            return fallback.split(mesh)

        return self._ensure_watertight(parts)
