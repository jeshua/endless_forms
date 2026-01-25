"""
Convex decomposition mesh splitting.

Uses CoACD or V-HACD to decompose mesh into approximately convex parts,
then optionally merges to reach target part count.
"""

from typing import Any
import numpy as np
import trimesh

from .base import BaseSplitter


class ConvexSplitter(BaseSplitter):
    """Split mesh using convex decomposition algorithms."""

    @property
    def name(self) -> str:
        return "Convex"

    @property
    def description(self) -> str:
        return "Decompose into approximately convex parts (CoACD/V-HACD)"

    def get_parameters(self) -> dict[str, dict[str, Any]]:
        return {
            "threshold": {
                "type": "float",
                "default": 0.05,
                "min": 0.01,
                "max": 1.0,
                "step": 0.01,
                "description": "Concavity threshold (lower = more parts)",
            },
            "preprocess": {
                "type": "bool",
                "default": True,
                "description": "Preprocess mesh for manifoldness",
            },
        }

    def _try_coacd(
        self, mesh: trimesh.Trimesh, threshold: float, preprocess: bool
    ) -> list[trimesh.Trimesh] | None:
        """Try to use CoACD for decomposition."""
        try:
            import coacd

            # Convert to format CoACD expects
            vertices = mesh.vertices.astype(np.float64)
            faces = mesh.faces.astype(np.int32)

            # Run CoACD
            parts = coacd.run_coacd(
                vertices,
                faces,
                threshold=threshold,
                preprocess=preprocess,
            )

            # Convert back to trimesh
            result = []
            for verts, tris in parts:
                part = trimesh.Trimesh(vertices=verts, faces=tris)
                if len(part.vertices) > 3:
                    result.append(part)

            return result if result else None

        except ImportError:
            return None
        except Exception:
            return None

    def _try_vhacd(self, mesh: trimesh.Trimesh) -> list[trimesh.Trimesh] | None:
        """Try to use V-HACD via trimesh's convex decomposition."""
        try:
            # trimesh has built-in V-HACD support
            parts = mesh.convex_decomposition()
            if isinstance(parts, list) and len(parts) > 0:
                return parts
            return None
        except Exception:
            return None

    def _merge_parts(
        self, parts: list[trimesh.Trimesh], target_count: int
    ) -> list[trimesh.Trimesh]:
        """Merge parts to reach target count by combining adjacent ones."""
        if len(parts) <= target_count:
            return parts

        # Simple greedy merging: combine parts with closest centroids
        while len(parts) > target_count:
            # Find pair with minimum centroid distance
            min_dist = float("inf")
            merge_i, merge_j = 0, 1

            for i in range(len(parts)):
                for j in range(i + 1, len(parts)):
                    dist = np.linalg.norm(parts[i].centroid - parts[j].centroid)
                    if dist < min_dist:
                        min_dist = dist
                        merge_i, merge_j = i, j

            # Merge the two closest parts
            try:
                merged = trimesh.util.concatenate([parts[merge_i], parts[merge_j]])
                parts = [p for k, p in enumerate(parts) if k not in (merge_i, merge_j)]
                parts.append(merged)
            except Exception:
                # If merge fails, just remove one part
                parts.pop(merge_j)

        return parts

    def _simple_convex_split(self, mesh: trimesh.Trimesh) -> list[trimesh.Trimesh]:
        """Fallback: split into convex hull segments along principal axis."""
        # Use PCA to find principal axis
        centered = mesh.vertices - mesh.centroid
        try:
            _, _, vh = np.linalg.svd(centered)
            principal_axis = vh[0]
        except Exception:
            principal_axis = np.array([0, 0, 1])

        # Project vertices onto principal axis
        projections = np.dot(mesh.vertices, principal_axis)
        min_proj = projections.min()
        max_proj = projections.max()
        span = max_proj - min_proj

        if span <= 0:
            return [mesh.copy()]

        # Split along principal axis
        parts = []
        remaining = mesh.copy()

        for i in range(self.num_parts - 1):
            cut_pos = min_proj + span * (i + 1) / self.num_parts
            origin = mesh.centroid + principal_axis * (
                cut_pos - np.dot(mesh.centroid, principal_axis)
            )

            try:
                # slice_plane keeps the positive side of the normal
                below = remaining.slice_plane(origin, -principal_axis, cap=True)
                above = remaining.slice_plane(origin, principal_axis, cap=True)

                if below is not None and len(below.vertices) > 0:
                    parts.append(below)

                if above is not None and len(above.vertices) > 0:
                    remaining = above
                else:
                    break
            except Exception:
                break

        if remaining is not None and len(remaining.vertices) > 0:
            parts.append(remaining)

        return parts if parts else [mesh.copy()]

    def split(self, mesh: trimesh.Trimesh, **params) -> list[trimesh.Trimesh]:
        """
        Split mesh using convex decomposition.

        Args:
            mesh: Input mesh
            threshold: Concavity threshold for decomposition
            preprocess: Whether to preprocess mesh

        Returns:
            List of approximately convex mesh parts
        """
        if not self.validate_mesh(mesh):
            return []

        threshold = params.get("threshold", 0.05)
        preprocess = params.get("preprocess", True)

        # Try CoACD first (preferred)
        parts = self._try_coacd(mesh, threshold, preprocess)

        # Fall back to V-HACD
        if parts is None:
            parts = self._try_vhacd(mesh)

        # If we got parts but fewer than requested, use simple split instead
        if parts is None or len(parts) < self.num_parts:
            parts = self._simple_convex_split(mesh)

        # Merge if too many parts
        if len(parts) > self.num_parts:
            parts = self._merge_parts(parts, self.num_parts)

        return self._ensure_watertight(parts)
