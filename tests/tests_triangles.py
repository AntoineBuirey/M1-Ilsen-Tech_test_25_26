import pytest

from triangulator.triangles import Triangles
from triangulator.data_types import Triangle


class TestTriangles:
    @pytest.fixture
    def sample_triangles(self) -> Triangles:
        points = [ (0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (1.0, 1.0), (0.5, 0.5) ]
        triangles = [ (0, 1, 2), (2, 3, 4) ]
        return Triangles(points, triangles)
    
    def test_get_triangle(self, sample_triangles: Triangles) -> None:
        assert sample_triangles.get_triangle(0) == Triangle(0, 1, 2)
        assert sample_triangles.get_triangle(1) == Triangle(2, 3, 4)
        with pytest.raises(IndexError):
            sample_triangles.get_triangle(2)
    
    def test_set_triangle(self, sample_triangles: Triangles) -> None:
        sample_triangles.set_triangle(1, (5, 6, 7))
        assert sample_triangles.get_triangle(1) == Triangle(5, 6, 7)
        with pytest.raises(IndexError):
            sample_triangles.set_triangle(2, (8, 9, 10))
    
    def test_len_nb_triangles(self, sample_triangles: Triangles) -> None:
        assert len(sample_triangles) == 2
        assert sample_triangles.nb_triangles() == 2
        
    def test_iter(self, sample_triangles: Triangles) -> None:
        triangles = list(sample_triangles)
        assert triangles == [Triangle(0, 1, 2), Triangle(2, 3, 4)]
        
    def test_remove_triangle(self, sample_triangles: Triangles) -> None:
        sample_triangles.remove_triangle(0)
        assert len(sample_triangles) == 1
        assert sample_triangles.get_triangle(0) == Triangle(2, 3, 4)
        with pytest.raises(IndexError):
            sample_triangles.remove_triangle(1)
        with pytest.raises(ValueError):
            sample_triangles.remove_triangle((0, 1, 2))

    def test_to_from_bytes(self, sample_triangles: Triangles) -> None:
        data = sample_triangles.to_bytes()
        new_triangles = Triangles.from_bytes(data)
        assert len(new_triangles) == len(sample_triangles)
        for i in range(len(sample_triangles)):
            assert new_triangles.get_triangle(i) == sample_triangles.get_triangle(i)
    
    def test_from_bytes_invalid(self) -> None:
        invalid_data = b'\x00\x01\x02'  # too short to be valid
        with pytest.raises(ValueError):
            Triangles.from_bytes(invalid_data)
