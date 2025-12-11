import time
from collections.abc import Iterator
from random import randint

import pytest

from triangulator.data_types import Point
from triangulator.pointset import PointSet
from triangulator.triangles import Triangles
from triangulator.triangulator import triangulate


def generate_random_distincts_points(num_points: int) -> Iterator[Point]:
    seen = set()
    while len(seen) < num_points:
        point = Point(randint(0, 1_000_000), randint(0, 1_000_000))
        if point not in seen:
            seen.add(point)
            yield point


@pytest.mark.performance
@pytest.mark.parametrize("num_points", [3, 100, 500, 1_000, 5_000, 10_000],
                         ids=["MIN", "XS", "S", "M", "L", "XL"])
def test_triangulate_large_pointset(num_points: int):
    # Generate a large PointSet with num_points points
    points = PointSet(generate_random_distincts_points(num_points))
    # Measure the time taken to triangulate
    start_time = time.time()
    triangles = triangulate(points)
    elapsed_time = time.time() - start_time
    
    print(f"Triangulated {num_points} points in {elapsed_time:.2f} seconds.")
    assert isinstance(triangles, Triangles)