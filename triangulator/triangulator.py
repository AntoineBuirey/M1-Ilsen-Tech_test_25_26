"""Triangulator module."""

from typing import cast
from .pointset import PointSet
from .triangles import Triangles
from .PSM import PointSetManager
from .data_types import Point as _Point


def triangulate(points: PointSet) -> Triangles:
    """Triangulate a set of points using Bowyer-Watson algorithm.

    Args:
        points (PointSet): The PointSet to triangulate.

    Returns:
        Triangles: The triangulated result.

    Raises:
        ValueError: If the point set has fewer than 3 points or all points are collinear.

    """
    n = len(points)
    
    # Validate input
    if n < 3:
        raise ValueError("At least 3 points are required for triangulation.")
    
    # Check if all points are collinear
    if n >= 3 and _are_collinear(points):
        raise ValueError("All points are collinear, cannot triangulate.")
    
    # For 3 points, return a single triangle
    if n == 3:
        return Triangles(points=points, triangles=[(0, 1, 2)])
    
    # Create super-triangle that contains all points
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')
    
    for i in range(n):
        point = cast(_Point, points.get_point(i))
        min_x = min(min_x, point.x)
        max_x = max(max_x, point.x)
        min_y = min(min_y, point.y)
        max_y = max(max_y, point.y)
    
    dx = max_x - min_x
    dy = max_y - min_y
    delta_max = max(dx, dy)
    mid_x = (min_x + max_x) / 2
    mid_y = (min_y + max_y) / 2
    
    # Create super-triangle vertices
    super_points = [
        _Point(mid_x - 20 * delta_max, mid_y - delta_max),
        _Point(mid_x, mid_y + 20 * delta_max),
        _Point(mid_x + 20 * delta_max, mid_y - delta_max)
    ]
    
    # Build complete point set with super-triangle
    all_points: list[_Point] = [cast(_Point, points.get_point(i)) for i in range(n)] + super_points
    triangles_list = [(n, n + 1, n + 2)]  # Start with super-triangle
    
    # Add each point one at a time
    for i in range(n):
        point = all_points[i]
        bad_triangles = []
        
        # Find all triangles whose circumcircle contains the point
        for tri_idx, tri in enumerate(triangles_list):
            if _in_circumcircle(point, tri, all_points):
                bad_triangles.append(tri_idx)
        
        # Find the boundary of the polygonal hole
        polygon = []
        for tri_idx in bad_triangles:
            tri = triangles_list[tri_idx]
            edges = [
                (tri[0], tri[1]),
                (tri[1], tri[2]),
                (tri[2], tri[0])
            ]
            
            for edge in edges:
                # Check if edge is shared with another bad triangle
                is_shared = False
                for other_idx in bad_triangles:
                    if other_idx == tri_idx:
                        continue
                    other_tri = triangles_list[other_idx]
                    other_edges = [
                        (other_tri[0], other_tri[1]),
                        (other_tri[1], other_tri[2]),
                        (other_tri[2], other_tri[0])
                    ]
                    if edge in other_edges or (edge[1], edge[0]) in other_edges:
                        is_shared = True
                        break
                
                if not is_shared:
                    polygon.append(edge)
        
        # Remove bad triangles
        for tri_idx in sorted(bad_triangles, reverse=True):
            triangles_list.pop(tri_idx)
        
        # Re-triangulate the polygonal hole
        for edge in polygon:
            triangles_list.append((edge[0], edge[1], i))
    
    # Remove triangles that share a vertex with the super-triangle
    final_triangles = []
    for tri in triangles_list:
        if tri[0] < n and tri[1] < n and tri[2] < n:
            final_triangles.append(tri)
    
    return Triangles(points=points, triangles=final_triangles)


def _are_collinear(points: PointSet) -> bool:
    """Check if all points in the set are collinear.
    
    Args:
        points (PointSet): The PointSet to check.
    
    Returns:
        bool: True if all points are collinear, False otherwise.
    
    """
    if len(points) < 3:
        return True
    
    p0 = cast(_Point, points.get_point(0))
    p1 = cast(_Point, points.get_point(1))
    
    for i in range(2, len(points)):
        p2 = cast(_Point, points.get_point(i))
        # Calculate cross product
        cross = (p1.x - p0.x) * (p2.y - p0.y) - (p1.y - p0.y) * (p2.x - p0.x)
        if abs(cross) > 1e-10:  # Not collinear
            return False
    
    return True


def _in_circumcircle(point: _Point, triangle: tuple[int, int, int], all_points: list[_Point]) -> bool:
    """Check if a point is inside the circumcircle of a triangle.
    
    Args:
        point: The point to check.
        triangle: Tuple of three point indices.
        all_points: List of all points.
    
    Returns:
        bool: True if the point is inside the circumcircle, False otherwise.
    
    """
    p0 = all_points[triangle[0]]
    p1 = all_points[triangle[1]]
    p2 = all_points[triangle[2]]
    
    # Translate point to origin
    ax = p0.x - point.x
    ay = p0.y - point.y
    bx = p1.x - point.x
    by = p1.y - point.y
    cx = p2.x - point.x
    cy = p2.y - point.y
    
    # Calculate the determinant
    det = (ax * ax + ay * ay) * (bx * cy - cx * by) - \
          (bx * bx + by * by) * (ax * cy - cx * ay) + \
          (cx * cx + cy * cy) * (ax * by - bx * ay)
    
    # Check triangle orientation and adjust
    orientation = (p1.x - p0.x) * (p2.y - p0.y) - (p1.y - p0.y) * (p2.x - p0.x)
    
    # If triangle is clockwise, flip the determinant sign
    if orientation < 0:
        det = -det
    
    return det > 0



def get_and_compute(point_set_id: str) -> bytes:
    """Retrieve a PointSet by its ID using the PointSetManager, triangulate it, and return the serialized Triangles.

    Args:
        point_set_id (str): The ID of the PointSet to retrieve and triangulate.

    Returns:
        bytes: The serialized Triangles object.

    """
    point_set = PointSetManager.get_point_set(point_set_id)
    triangles = triangulate(point_set)
    return triangles.to_bytes()