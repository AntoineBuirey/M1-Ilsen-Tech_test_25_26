"""Module for managing a set of triangles defined by a PointSet and a list of triangles."""

from collections.abc import Iterable, Iterator

from .data_types import Point as _Point
from .data_types import Triangle as _Triangle
from .pointset import PointSet

type Point = _Point|tuple[float, float]
type Triangle = _Triangle|tuple[int, int, int]


class Triangles:
    """A set of triangles defined by a PointSet and a list of triangles.

    Args:
        points (Iterable[Point|tuple[float, float]] | None): An iterable of points to initialize the PointSet.
        triangles (Iterable[Triangle|tuple[int, int, int]] | None): An iterable of triangles to initialize the set of triangles.

    Raises:
        ValueError: If any triangle contains an index out of bounds of the points set.
        ValueError: If any triangle has non-distinct points.
        ValueError: If duplicate triangles are found (regardless of the order of the points).

    """

    def __init__(self,
                 points : Iterable[Point] | None = None,
                 triangles : Iterable[Triangle] | None = None
                ) -> None:
        """Initialize the Triangles object.

        Args:
            points (Iterable[Point] | None, optional): _points to initialize the PointSet. Defaults to None.
            triangles (Iterable[Triangle] | None, optional): _triangles to initialize the set of triangles. Defaults to None.
        
        """
        pass
        
    @property
    def points(self) -> PointSet:
        """Return the PointSet of points used in the triangles.

        Returns:
            PointSet: The PointSet of points used in the triangles.

        """
        pass
    
    def add_triangle(self, triangle : Triangle) -> int:
        """Add a triangle to the set.

        Args:
            triangle (Triangle): The triangle to add.

        Raises:
            IndexError: If any index in the triangle is out of bounds of the points set.
            ValueError: If the three points are not distinct.
            ValueError: If a triangle with the same points already exists, regardless of the order of the points.

        Returns:
            int: The index of the added triangle.

        """
        pass
    
    def remove_triangle(self, triangle_or_id : Triangle|int) -> None:
        """Remove a triangle from the set.

        Args:
            triangle_or_id (Triangle|int): The triangle to remove, or its index.

        Raises:
            ValueError: If the triangle does not exist in the set.
            IndexError: If the index is out of bounds.

        """
        pass
    
    def __iter__(self) -> Iterator[Triangle]:
        """Return an iterator over the triangles in the set.

        Returns:
            Iterable[Triangle]: An iterator over the triangles in the set.

        """
        pass
    
    def nb_triangles(self) -> int:
        """Return the number of triangles in the set.

        Returns:
            int: The number of triangles in the set.

        """
        pass
    
    def __len__(self) -> int:
        """Return the number of triangles in the set.

        Returns:
            int: The number of triangles in the set.

        """
        return self.nb_triangles()
    
    def get_triangle(self, index: int) -> Triangle:
        """Return the triangle at the given index.

        Args:
            index (int): The index of the triangle to retrieve.

        Raises:
            IndexError: If the index is out of bounds.

        Returns:
            Triangle: The triangle at the given index.

        """
    
    def set_triangle(self, index: int, value: Triangle) -> None:
        """Set the triangle at the given index.

        Args:
            index (int): The index of the triangle to set.
            value (Triangle): The new triangle value.

        Raises:
            IndexError: If the index is out of bounds.
            ValueError: If any index in the triangle is out of bounds of the points set.
            ValueError: If the three points are not distinct.
            ValueError: If a triangle with the same points already exists, regardless of the order of the points.

        """
        pass
    
    def __eq__(self, other: object) -> bool:
        """Check if two Triangles objects are equal.

        Args:
            other (object): The other Triangles object to compare with.

        Raises:
            TypeError: If the other object is not a Triangles object.

        Returns:
            bool: True if the two Triangles objects are equal (all triangles are the same and in the same order, and the underlying PointSets are equal), False otherwise.

        """
        pass
    
    def to_bytes(self) -> bytes:
        """Serialize the Triangles to bytes for transmission.

        Returns:
            bytes: The serialized Triangles.

        """
        pass
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'Triangles':
        """Deserializes bytes to a Triangles object.

        Args:
            data (bytes): The serialized Triangles.

        Raises:
            ValueError: If the data is invalid or corrupted.

        Returns:
            Triangles: The deserialized Triangles object.

        """
        pass