import pytest

from triangulator.pointset import PointSet
from triangulator.data_types import Point

class TestPointSet:
    @pytest.fixture
    def sample_pointset(self) -> PointSet:
        points = [ (0.0, 0.0), (1.0, 1.0), (2.0, 2.0) ]
        return PointSet(points)
    
    def test_get_point(self, sample_pointset: PointSet) -> None:
        assert sample_pointset.get_point(0) == (0.0, 0.0)
        assert sample_pointset.get_point(1) == (1.0, 1.0)
        assert sample_pointset.get_point(2) == (2.0, 2.0)
        with pytest.raises(IndexError):
            sample_pointset.get_point(3)
    
    def test_set_point(self, sample_pointset: PointSet) -> None:
        sample_pointset.set_point(1, (5.0, 5.0))
        assert sample_pointset.get_point(1) == (5.0, 5.0)
        with pytest.raises(IndexError):
            sample_pointset.set_point(3, (6.0, 6.0))
    
    def test_len_nb_points(self, sample_pointset: PointSet) -> None:
        assert len(sample_pointset) == 3
        assert sample_pointset.nb_points() == 3
        
    def test_iter(self, sample_pointset: PointSet) -> None:
        points = list(sample_pointset)
        assert points == [ (0.0, 0.0), (1.0, 1.0), (2.0, 2.0) ]
        
    def test_add_point(self, sample_pointset: PointSet) -> None:
        index = sample_pointset.add_point((3.0, 3.0))
        assert index == 3
        assert sample_pointset.get_point(3) == Point(3.0, 3.0)
        with pytest.raises(ValueError):
            sample_pointset.add_point((1.0, 1.0))
            
    def test_remove_point(self, sample_pointset: PointSet) -> None:
        sample_pointset.remove_point((1.0, 1.0))
        assert len(sample_pointset) == 2
        with pytest.raises(ValueError):
            sample_pointset.remove_point((1.0, 1.0))

    def test_to_from_bytes(self, sample_pointset: PointSet) -> None:
        data = sample_pointset.to_bytes()
        new_pointset = PointSet.from_bytes(data)
        assert len(new_pointset) == len(sample_pointset)
        for i in range(len(sample_pointset)):
            assert new_pointset.get_point(i) == sample_pointset.get_point(i)

    def test_from_bytes_invalid(self) -> None:
        invalid_data = b'\x00\x01\x02'  # too short to be valid
        with pytest.raises(ValueError):
            PointSet.from_bytes(invalid_data)

