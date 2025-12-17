"""Debug script for triangulation."""

from typing import cast

from triangulator.data_types import Point as _Point
from triangulator.pointset import PointSet

points_data = [(0.0, 0.0), (2.0, 0.0), (1.0, 1.0), (0.0, 2.0), (2.0, 2.0)]
points = PointSet(points_data)
n = len(points)

print(f"Number of points: {n}")
print("Points:")
for i in range(n):
    p = cast(_Point, points.get_point(i))
    print(f"  {i}: ({p.x}, {p.y})")

# Create super-triangle
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

super_points = [
    _Point(mid_x - 20 * delta_max, mid_y - delta_max),
    _Point(mid_x, mid_y + 20 * delta_max),
    _Point(mid_x + 20 * delta_max, mid_y - delta_max)
]

print(f"\nSuper-triangle vertices (indices {n}, {n+1}, {n+2}):")
for i, sp in enumerate(super_points):
    print(f"  {n+i}: ({sp.x}, {sp.y})")

all_points = [cast(_Point, points.get_point(i)) for i in range(n)] + super_points
triangles_list = [(n, n + 1, n + 2)]

print(f"\nInitial triangles: {triangles_list}")

# Simulate adding points
for i in range(n):
    point = all_points[i]
    print(f"\n=== Adding point {i}: ({point.x}, {point.y}) ===")
    print(f"Triangles before: {triangles_list}")
    
    # Find bad triangles
    bad_triangles = []
    for tri_idx, tri in enumerate(triangles_list):
        p0 = all_points[tri[0]]
        p1 = all_points[tri[1]]
        p2 = all_points[tri[2]]
        
        ax = p0.x - point.x
        ay = p0.y - point.y
        bx = p1.x - point.x
        by = p1.y - point.y
        cx = p2.x - point.x
        cy = p2.y - point.y
        
        det = (ax * ax + ay * ay) * (bx * cy - cx * by) - \
              (bx * bx + by * by) * (ax * cy - cx * ay) + \
              (cx * cx + cy * cy) * (ax * by - bx * ay)
        
        # Check triangle orientation
        orientation = (p1.x - p0.x) * (p2.y - p0.y) - (p1.y - p0.y) * (p2.x - p0.x)
        
        # If triangle is clockwise, flip the determinant sign
        if orientation < 0:
            det = -det
        
        print(f"  Triangle {tri_idx} {tri}: orientation={orientation:.4f}, det={det:.4f}")
        
        if det > 0:
            bad_triangles.append(tri_idx)
            print("    -> BAD (point inside circumcircle)")
    
    # Find polygon boundary
    polygon = []
    for tri_idx in bad_triangles:
        tri = triangles_list[tri_idx]
        edges = [
            (tri[0], tri[1]),
            (tri[1], tri[2]),
            (tri[2], tri[0])
        ]
        
        for edge in edges:
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
    
    print(f"  Polygon edges: {polygon}")
    
    # Remove bad triangles
    for tri_idx in sorted(bad_triangles, reverse=True):
        triangles_list.pop(tri_idx)
    
    # Add new triangles
    new_triangles = []
    for edge in polygon:
        new_tri = (edge[0], edge[1], i)
        triangles_list.append(new_tri)
        new_triangles.append(new_tri)
    
    print(f"  New triangles: {new_triangles}")
    print(f"  Triangles after: {triangles_list}")

print("\n=== Final triangles (before filtering super-triangle) ===")
print(f"Triangles: {triangles_list}")

# Filter out super-triangle vertices
final_triangles = []
for tri in triangles_list:
    if tri[0] < n and tri[1] < n and tri[2] < n:
        final_triangles.append(tri)
        print(f"  Keeping: {tri}")
    else:
        print(f"  Filtering: {tri} (has super-triangle vertex)")

print(f"\nFinal triangles: {final_triangles}")
