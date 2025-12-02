"""Triangulator module."""

from .pointset import PointSet
from .triangles import Triangles


def triangulate(points: PointSet) -> Triangles:
    """Triangulate a set of points.

    Args:
        points (PointSet): The PointSet to triangulate.

    Returns:
        Triangles: The triangulated result.

    """
    pass


def get_and_compute(point_set_id: str) -> bytes:
    """Retrieve a PointSet by its ID using the PointSetManager.

    Args:
        point_set_id (str): The ID of the PointSet to retrieve and triangulate.

    Returns:
        bytes: The serialized Triangles object.

    """
    pass