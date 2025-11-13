from typing import Iterable, Iterator

from .data_types import Point as _Point, Triangle as _Triangle
from .pointset import PointSet


type Point = _Point|tuple[float, float]
type Triangle = _Triangle|tuple[int, int, int]


class Triangles:
    """A set of triangles defined by a PointSet and a list of triangles.

    Args:
        points (Iterable[Point|tuple[float, float]] | None): an iterable of points to initialize the PointSet
        triangles (Iterable[Triangle|tuple[int, int, int]] | None): an iterable of triangles to initialize the set of triangles
        
    Raises:
        ValueError: if any triangle contains an index out of bounds of the points set
        ValueError: if any triangle has non-distinct points
        ValueError: if duplicate triangles are found (regardless of the order of the points)
    """
    def __init__(self,
                 points : Iterable[Point] | None = None,
                 triangles : Iterable[Triangle] | None = None
                ) -> None:
        pass
        
    @property
    def points(self) -> PointSet:
        """
        Return the PointSet of points used in the triangles.
        """
        pass
    
    def add_triangle(self, triangle : Triangle) -> int:
        """adds a triangle to the set

        Args:
            triangle (Triangle): the triangle to add
        
        Raises:
            IndexError: if any index in the triangle is out of bounds of the points set
            ValueError: if the three points are not distinct
            ValueError: if a triangle with the same points already exists, regardless of the order of the points

        Returns:
            int: the index of the added triangle
        """
        pass
    
    def remove_triangle(self, triangle_or_id : Triangle|int) -> None:
        """removes a triangle from the set
        
        Args:
            triangle_or_id (Triangle|int): the triangle to remove, or its index
            
        Raises:
            ValueError: if the triangle does not exist in the set
            IndexError: if the index is out of bounds
        """
        pass
    
    def __iter__(self) -> Iterator[Triangle]:
        """Returns an iterator over the triangles in the set
        
        Returns:
            Iterable[Triangle]: an iterator over the triangles in the set
        """
        pass
    
    def nb_triangles(self) -> int:
        """Returns the number of triangles in the set

        Returns:
            int: the number of triangles in the set
        """
        pass
    
    def __len__(self) -> int:
        """Returns the number of triangles in the set

        Returns:
            int: the number of triangles in the set
        """
        return self.nb_triangles()
    
    def get_triangle(self, index: int) -> Triangle:
        """Returns the triangle at the given index

        Args:
            index (int): the index of the triangle to retrieve

        Raises:
            IndexError: if the index is out of bounds

        Returns:
            Triangle: the triangle at the given index
        """
    
    def set_triangle(self, index: int, value: Triangle) -> None:
        """
        Sets the triangle at the given index
        Args:
            index (int): the index of the triangle to set
            value (Triangle): the new triangle value

        Raises:
            IndexError: if the index is out of bounds
            ValueError: if any index in the triangle is out of bounds of the points set
            ValueError: if the three points are not distinct
            ValueError: if a triangle with the same points already exists, regardless of the order of the points
        """
        pass
    
    def __eq__(self, other: object) -> bool:
        """Checks if two Triangles objects are equal

        Args:
            other (object): the other Triangles object to compare with

        Raises:
            TypeError: if the other object is not a Triangles object

        Returns:
            bool: True if the two Triangles objects are equal (all triangles are the same and in the same order, and the underlying PointSets are equal), False otherwise
        """
        pass
    
    def to_bytes(self) -> bytes:
        """Serializes the Triangles to bytes for transmission

        Returns:
            bytes: the serialized Triangles
        """
        pass
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'Triangles':
        """Deserializes bytes to a Triangles object

        Args:
            data (bytes): the serialized Triangles
            
        Raises:
            ValueError: if the data is invalid or corrupted

        Returns:
            Triangles: the deserialized Triangles object
        """
        pass