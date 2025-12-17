import pytest

from triangulator.pointset import PointSet
from triangulator.triangles import Triangles
from triangulator.triangulator import triangulate, _are_collinear, get_and_compute
from datasets import IDS, TRIANGLES, POINTS


class TestTriangulator:
    @pytest.fixture
    def sample_triangles(self) -> Triangles:
        points = [ (0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (1.0, 1.0), (0.5, 0.5) ]
        triangles = [ (0, 1, 2), (2, 3, 4) ]
        return Triangles(points, triangles)
    
    @pytest.mark.parametrize("dataset", [
        (PointSet([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]),
         Triangles([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)], [(0, 1, 2)])), # minimal case
        (PointSet([(0.0, 0.0), (2.0, 0.0), (1.0, 1.0), (0.0, 2.0), (2.0, 2.0)]),
         Triangles([(0.0, 0.0), (2.0, 0.0), (1.0, 1.0), (0.0, 2.0), (2.0, 2.0)], [(0, 1, 2), (0, 2, 3), (1, 4, 2), (3, 2, 4)])),
    ])
    def test_triangulate_success(self, dataset : tuple[PointSet, Triangles]) -> None:
        points, expected = dataset
        result = triangulate(points)
        print(f"Result:   {result}\nExpected: {expected}")
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
            
            
    @pytest.mark.parametrize("points, expected", [
        (PointSet([(0, 0), (1, 1)]), True), # two points are collinear
        (PointSet([(0, 0), (1, 1), (2, 2)]), True), # collinear points
        (PointSet([(0, 0), (1, 0), (0, 1)]), False), # non-collinear points
        (PointSet([(0, 0), (1, 1), (2, 2), (3, 3)]), True), # collinear points
        (PointSet([(0, 0), (1, 0), (0, 1), (1, 1)]), False), # non-collinear points
    ])
    def test_are_collinear(self, points : PointSet, expected : bool) -> None:
        result = _are_collinear(points)
        assert result == expected
        
    def test_get_and_compute(self, sample_triangles, monkeypatch : pytest.MonkeyPatch) -> None:
        
        def mock_triangulate(points : PointSet) -> Triangles:
            return sample_triangles

        def mock_get_point_set(dataset_id : str) -> PointSet:
            return PointSet()
        
        monkeypatch.setattr("triangulator.triangulator.PointSetManager.get_point_set", mock_get_point_set)
        monkeypatch.setattr("triangulator.triangulator.triangulate", mock_triangulate)

        result = get_and_compute(IDS[0])

        assert result == sample_triangles.to_bytes()