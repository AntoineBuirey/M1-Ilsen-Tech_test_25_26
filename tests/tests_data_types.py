import pytest

from triangulator.data_types import Point, Triangle


class TestPoint:
    @pytest.mark.parametrize("point_a, point_b, expected", [
        (Point(0.0, 0.0), Point(0.0, 0.0), True),
        (Point(1.0, 2.0), Point(1.0, 2.0), True),
        (Point(1.0, 2.0), Point(2.0, 1.0), False),
        (Point(-1.0, -2.0), Point(-1.0, -2.0), True),
        (Point(1.5, 2.5), (1.5, 2.5), True),
        (Point(1.5, 2.5), [1.5, 2.5], True)
    ])
    def test_point_equality(self, point_a: Point, point_b: Point, expected: bool) -> None:
        assert (point_a == point_b) == expected
        
    def test_point_equality_type_error(self) -> None:
        point = Point(1.0, 2.0)
        with pytest.raises(TypeError):
            _ = point == "not a point"
        with pytest.raises(TypeError):
            _ = point == (1.0,)
        with pytest.raises(TypeError):
            _ = point == [1.0, 2.0, 3.0]
            
    def test_hash_consistency(self) -> None:
        point1 = Point(3.0, 4.0)
        point2 = Point(3.0, 4.0)
        point3 = Point(4.0, 3.0)
        assert hash(point1) == hash(point2)
        assert hash(point1) != hash(point3)
        
    @pytest.mark.parametrize("point, expected_x, expected_y", [
        (Point(1.5, 2.5), 1.5, 2.5),
        (Point(-1.0, 0.0), -1.0, 0.0),
        (Point(0.0, -3.5), 0.0, -3.5),
    ])
    def test_point_coordinates(self, point: Point, expected_x: float, expected_y: float) -> None:
        assert point.x == expected_x
        assert point.y == expected_y
        

class TestTriangle:
    @pytest.mark.parametrize("triangle_a, triangle_b, expected", [
        (Triangle(0, 1, 2), Triangle(0, 1, 2), True),  # exact same
        (Triangle(0, 1, 2), Triangle(2, 1, 0), True), # same points, different order
        (Triangle(0, 1, 2), Triangle(0, 2, 3), False), # different points
    ])
    def test_triangle_equality(self, triangle_a: Triangle, triangle_b: Triangle, expected: bool) -> None:
        assert (triangle_a == triangle_b) == expected
        
    def test_triangle_equality_type_error(self) -> None:
        triangle = Triangle(0, 1, 2)
        with pytest.raises(TypeError):
            _ = triangle == "not a triangle"
        with pytest.raises(TypeError):
            _ = triangle == (0, 1, 2)
        
    @pytest.mark.parametrize("triangle, expected_indices", [
        (Triangle(0, 1, 2), {0, 1, 2}),
        (Triangle(2, 0, 1), {0, 1, 2}),
        (Triangle(5, 3, 4), {3, 4, 5}),
    ])
    def test_triangle_indices(self, triangle: Triangle, expected_indices: set[int]) -> None:
        assert triangle.indices == expected_indices