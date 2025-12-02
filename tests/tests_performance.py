import time
from collections.abc import Iterator
from random import randint

import pytest

from triangulator.data_types import Point
from triangulator.pointset import PointSet
from triangulator.triangles import Triangles
from triangulator.triangulator import triangulate


def generate_random_points(num_points: int) -> Iterator[Point]:
    for _ in range(num_points):
        yield Point(randint(0, 10000), randint(0, 10000))


@pytest.mark.performance
@pytest.mark.parametrize("num_points", [3, 100, 1_000, 10_000, 100_000, 1_000_000],
                         ids=["MIN", "XS", "S", "M", "L", "XL"])
def test_triangulate_large_pointset(num_points: int):
    # Generate a large PointSet with num_points points
    points = PointSet(generate_random_points(num_points))
    # Measure the time taken to triangulate
    start_time = time.time()
    triangles = triangulate(points)
    elapsed_time = time.time() - start_time
    
    print(f"Triangulated {num_points} points in {elapsed_time:.2f} seconds.")
    assert isinstance(triangles, Triangles)