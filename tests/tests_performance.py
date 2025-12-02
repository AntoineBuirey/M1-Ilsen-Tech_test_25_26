import pytest
from random import randint
import time

from triangulator.triangulator import triangulate
from triangulator.pointset import PointSet
from triangulator.data_types import Point
from triangulator.triangles import Triangles


def generate_random_points(num_points: int) -> list[Point]:
    return [Point(randint(0, 10000), randint(0, 10000)) for _ in range(num_points)]


@pytest.mark.performance
@pytest.mark.parametrize("num_points", [3, 100, 1_000, 10_000, 100_000, 1_000_000],
                         ids=["minimal", "xs", "s", "m", "l", "xl"])
def test_triangulate_large_pointset(num_points: int):
    # Generate a large PointSet with num_points points
    points = PointSet(generate_random_points(num_points))
    # Measure the time taken to triangulate
    start_time = time.time()
    triangles = triangulate(points)
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"Triangulated {num_points} points in {elapsed_time:.2f} seconds.")
    assert isinstance(triangles, Triangles)