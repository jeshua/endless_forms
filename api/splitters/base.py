"""
Base splitter interface for mesh splitting algorithms.
"""

from abc import ABC, abstractmethod
from typing import Any
import trimesh


class BaseSplitter(ABC):
    """Abstract base class for mesh splitting algorithms."""

    def __init__(self, num_parts: int = 3):
        """
        Initialize the splitter.

        Args:
            num_parts: Target number of parts to split into
        """
        self.num_parts = num_parts

    @abstractmethod
    def split(self, mesh: trimesh.Trimesh, **params) -> list[trimesh.Trimesh]:
        """
        Split a mesh into multiple parts.

        Args:
            mesh: Input trimesh to split
            **params: Algorithm-specific parameters

        Returns:
            List of trimesh objects, one per part
        """
        pass

    @abstractmethod
    def get_parameters(self) -> dict[str, dict[str, Any]]:
        """
        Return configurable parameters for this splitter.

        Returns:
            Dictionary mapping parameter names to their metadata:
            {
                "param_name": {
                    "type": "float" | "int" | "bool" | "select",
                    "default": value,
                    "min": value (for numeric),
                    "max": value (for numeric),
                    "step": value (for numeric),
                    "options": [...] (for select),
                    "description": "Human-readable description"
                }
            }
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of the splitter."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what this splitter does."""
        pass

    def validate_mesh(self, mesh: trimesh.Trimesh) -> bool:
        """
        Check if mesh is valid for splitting.

        Args:
            mesh: Input mesh to validate

        Returns:
            True if mesh can be split
        """
        if mesh is None:
            return False
        if not hasattr(mesh, 'vertices') or len(mesh.vertices) < 4:
            return False
        if not hasattr(mesh, 'faces') or len(mesh.faces) < 4:
            return False
        return True

    def _ensure_watertight(self, parts: list[trimesh.Trimesh]) -> list[trimesh.Trimesh]:
        """
        Attempt to make each part watertight.

        Args:
            parts: List of mesh parts

        Returns:
            List of processed mesh parts
        """
        result = []
        for part in parts:
            if part is None or len(part.vertices) == 0:
                continue
            # Fix normals and fill holes if possible
            part.fix_normals()
            result.append(part)
        return result
