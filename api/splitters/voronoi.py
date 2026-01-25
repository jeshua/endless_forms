"""
Voronoi/Laguerre (Power Diagram) mesh splitting.

Uses the lifting map to compute weighted Voronoi cells via convex hull,
then intersects the mesh with each cell.
"""

from typing import Any
import numpy as np
from scipy.spatial import ConvexHull, Voronoi
import trimesh

from .base import BaseSplitter


class VoronoiSplitter(BaseSplitter):
    """Split mesh using Voronoi/Power Diagram tessellation."""

    @property
    def name(self) -> str:
        return "Voronoi"

    @property
    def description(self) -> str:
        return "Split using Voronoi cells (Power Diagram with weights)"

    def get_parameters(self) -> dict[str, dict[str, Any]]:
        return {
            "randomize": {
                "type": "bool",
                "default": True,
                "description": "Randomize seed positions",
            },
            "seed": {
                "type": "int",
                "default": 42,
                "min": 0,
                "max": 9999,
                "step": 1,
                "description": "Random seed for reproducibility",
            },
            "use_weights": {
                "type": "bool",
                "default": False,
                "description": "Use weighted Voronoi (Power Diagram)",
            },
        }

    def _generate_seed_points(
        self, mesh: trimesh.Trimesh, randomize: bool, seed: int
    ) -> np.ndarray:
        """Generate seed points within the mesh bounds."""
        if seed is not None:
            np.random.seed(seed)

        bounds = mesh.bounds
        center = mesh.centroid

        if randomize:
            # Generate random points within bounds
            points = np.random.uniform(
                bounds[0], bounds[1], size=(self.num_parts, 3)
            )
        else:
            # Distribute points evenly in a pattern
            if self.num_parts == 2:
                # Two points along longest axis
                extents = bounds[1] - bounds[0]
                axis = np.argmax(extents)
                offset = np.zeros(3)
                offset[axis] = extents[axis] * 0.25
                points = np.array([center - offset, center + offset])
            elif self.num_parts == 3:
                # Three points in a triangle pattern
                radius = np.min(bounds[1] - bounds[0]) * 0.3
                angles = np.linspace(0, 2 * np.pi, self.num_parts, endpoint=False)
                points = np.zeros((self.num_parts, 3))
                points[:, 0] = center[0] + radius * np.cos(angles)
                points[:, 1] = center[1] + radius * np.sin(angles)
                points[:, 2] = center[2]
            else:
                # General case: random distribution
                points = np.random.uniform(
                    bounds[0], bounds[1], size=(self.num_parts, 3)
                )

        return points

    def _compute_voronoi_halfspaces(
        self, seeds: np.ndarray, weights: np.ndarray | None = None
    ) -> list[list[tuple[np.ndarray, float]]]:
        """
        Compute halfspace representation of Voronoi/Power cells.

        For each cell, returns a list of (normal, offset) pairs defining
        the halfspaces that bound the cell.

        For Power Diagram, the bisector between points p_i and p_j is:
        2(p_j - p_i) . x = |p_j|^2 - |p_i|^2 - (w_j - w_i)
        """
        n = len(seeds)
        cells = []

        if weights is None:
            weights = np.zeros(n)

        for i in range(n):
            halfspaces = []
            for j in range(n):
                if i == j:
                    continue

                # Normal points from i towards j
                normal = seeds[j] - seeds[i]
                normal_len = np.linalg.norm(normal)
                if normal_len < 1e-10:
                    continue
                normal = normal / normal_len

                # Midpoint for standard Voronoi
                midpoint = (seeds[i] + seeds[j]) / 2

                # Offset along normal for Power Diagram
                if weights[i] != 0 or weights[j] != 0:
                    # Power diagram offset
                    weight_diff = weights[j] - weights[i]
                    offset = weight_diff / (2 * normal_len)
                    midpoint = midpoint + offset * normal

                # Halfspace: normal . x <= normal . midpoint
                d = np.dot(normal, midpoint)
                halfspaces.append((normal, d))

            cells.append(halfspaces)

        return cells

    def _intersect_mesh_with_halfspaces(
        self, mesh: trimesh.Trimesh, halfspaces: list[tuple[np.ndarray, float]]
    ) -> trimesh.Trimesh | None:
        """Intersect mesh with a set of halfspaces defining a convex region."""
        result = mesh.copy()

        for normal, d in halfspaces:
            if result is None or len(result.vertices) == 0:
                return None

            # Create cutting plane
            # The plane passes through point at distance d along normal
            origin = normal * d

            try:
                # Slice to keep the side where normal . x <= d
                result = result.slice_plane(origin, normal, cap=True)
            except Exception:
                continue

        return result

    def split(self, mesh: trimesh.Trimesh, **params) -> list[trimesh.Trimesh]:
        """
        Split mesh using Voronoi cells.

        Args:
            mesh: Input mesh
            randomize: Whether to randomize seed positions
            seed: Random seed for reproducibility
            use_weights: Whether to use weighted Voronoi (Power Diagram)

        Returns:
            List of mesh parts
        """
        if not self.validate_mesh(mesh):
            return []

        randomize = params.get("randomize", True)
        seed = params.get("seed", 42)
        use_weights = params.get("use_weights", False)

        # Generate seed points
        seeds = self._generate_seed_points(mesh, randomize, seed)

        # Optional weights for Power Diagram
        if use_weights:
            np.random.seed(seed + 1000)
            bounds = mesh.bounds
            scale = np.min(bounds[1] - bounds[0]) * 0.1
            weights = np.random.uniform(0, scale**2, size=self.num_parts)
        else:
            weights = None

        # Compute Voronoi cell halfspaces
        cells = self._compute_voronoi_halfspaces(seeds, weights)

        # Intersect mesh with each cell
        parts = []
        for i, halfspaces in enumerate(cells):
            part = self._intersect_mesh_with_halfspaces(mesh, halfspaces)
            if part is not None and len(part.vertices) > 3:
                parts.append(part)

        # If we got fewer parts than expected, fall back to plane splitting
        if len(parts) < 2:
            # Fallback: simple plane split
            from .plane import PlaneSplitter
            fallback = PlaneSplitter(self.num_parts)
            return fallback.split(mesh)

        return self._ensure_watertight(parts)
