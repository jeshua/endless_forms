from .base import BaseSplitter
from .plane import PlaneSplitter
from .voronoi import VoronoiSplitter
from .radial import RadialSplitter
from .convex import ConvexSplitter

SPLITTERS = {
    "plane": PlaneSplitter,
    "voronoi": VoronoiSplitter,
    "radial": RadialSplitter,
    "convex": ConvexSplitter,
}
