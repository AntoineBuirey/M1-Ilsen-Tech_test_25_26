import pytest

from triangulator.pointset import PointSet
from triangulator.triangles import Triangles
from triangulator.triangulator import triangulate


class TestTriangulator:
    @pytest.mark.parametrize("dataset", [
        (PointSet([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]),
         Triangles([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)], [(0, 1, 2)])), # minimal case
        (PointSet([(0.0, 0.0), (2.0, 0.0), (1.0, 1.0), (0.0, 2.0), (2.0, 2.0)]),
         Triangles([(0.0, 0.0), (2.0, 0.0), (1.0, 1.0), (0.0, 2.0), (2.0, 2.0)], [(0, 1, 2), (0, 2, 3), (1, 4, 2), (3, 2, 4)])),
    ])
    def test_triangulate_success(self, dataset : tuple[PointSet, Triangles]) -> None:
        points, expected = dataset
        result = triangulate(points)
        assert result == expected



    @pytest.mark.parametrize("points", [
        PointSet([]), # empty set
        PointSet([(0, 0)]), # not enough points
        PointSet([(0, 0), (1, 0)]), # not enough points
        PointSet([(0, 0), (1, 0), (2, 0)]), # duplicate points
    ])
    def test_triangulate_failure(self, points : PointSet) -> None:
        with pytest.raises(ValueError):
            triangulate(points)