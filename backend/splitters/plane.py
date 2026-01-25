"""
Plane-based mesh splitting.

Splits mesh using parallel or custom cutting planes along an axis.
"""

from typing import Any
import numpy as np
import trimesh

from .base import BaseSplitter


class PlaneSplitter(BaseSplitter):
    """Split mesh using parallel cutting planes."""

    @property
    def name(self) -> str:
        return "Plane"

    @property
    def description(self) -> str:
        return "Split using parallel cutting planes along an axis"

    def get_parameters(self) -> dict[str, dict[str, Any]]:
        return {
            "axis": {
                "type": "select",
                "default": "z",
                "options": ["x", "y", "z"],
                "description": "Axis to cut along",
            },
            "equal_spacing": {
                "type": "bool",
                "default": True,
                "description": "Space cuts equally along axis",
            },
        }

    def split(self, mesh: trimesh.Trimesh, **params) -> list[trimesh.Trimesh]:
        """
        Split mesh using parallel planes.

        Args:
            mesh: Input mesh
            axis: 'x', 'y', or 'z' - axis to cut along
            equal_spacing: If True, space cuts equally

        Returns:
            List of mesh parts
        """
        if not self.validate_mesh(mesh):
            return []

        axis = params.get("axis", "z")
        equal_spacing = params.get("equal_spacing", True)

        # Get axis index
        axis_map = {"x": 0, "y": 1, "z": 2}
        axis_idx = axis_map.get(axis, 2)

        # Get mesh bounds along axis
        bounds = mesh.bounds
        min_val = bounds[0, axis_idx]
        max_val = bounds[1, axis_idx]
        span = max_val - min_val

        if span <= 0:
            return [mesh.copy()]

        # Calculate cut positions (N-1 cuts for N parts)
        num_cuts = self.num_parts - 1
        if equal_spacing:
            # Equal spacing
            cut_positions = [
                min_val + span * (i + 1) / self.num_parts
                for i in range(num_cuts)
            ]
        else:
            # Default to equal spacing anyway for now
            cut_positions = [
                min_val + span * (i + 1) / self.num_parts
                for i in range(num_cuts)
            ]

        # Create plane normal
        normal = np.zeros(3)
        normal[axis_idx] = 1.0

        # Split mesh progressively
        parts = []
        remaining = mesh.copy()

        for cut_pos in cut_positions:
            # Create plane origin
            origin = np.zeros(3)
            origin[axis_idx] = cut_pos

            # Slice the mesh
            try:
                # slice_plane keeps the part on the positive side of the normal
                # So with normal pointing up (+Z), we get the part ABOVE the plane
                # We want to collect the part BELOW and keep the part ABOVE as remaining
                below = remaining.slice_plane(origin, -normal, cap=True)  # Below plane
                above = remaining.slice_plane(origin, normal, cap=True)   # Above plane

                if below is not None and len(below.vertices) > 0:
                    parts.append(below)

                if above is not None and len(above.vertices) > 0:
                    remaining = above
                else:
                    break
            except Exception:
                # If slicing fails, keep the remaining mesh
                break

        # Add the final remaining piece
        if remaining is not None and len(remaining.vertices) > 0:
            parts.append(remaining)

        # Ensure we have at least one part
        if not parts:
            return [mesh.copy()]

        return self._ensure_watertight(parts)
