"""Module for managing a set of triangles defined by a PointSet and a list of triangles."""

from collections.abc import Iterable, Iterator
from struct import calcsize, pack, unpack

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
        self._points = PointSet(points) if points is not None else PointSet()
        self._triangles : list[_Triangle] = []
        if triangles is not None:
            for triangle in triangles:
                self.add_triangle(triangle)
        
    @property
    def points(self) -> PointSet:
        """Return the PointSet of points used in the triangles.

        Returns:
            PointSet: The PointSet of points used in the triangles.

        """
        return self._points
    
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
        if not isinstance(triangle, _Triangle):
            triangle = _Triangle(*triangle)
        self._triangles.append(triangle)
        return len(self._triangles) - 1
    
    def remove_triangle(self, triangle_or_id : Triangle|int) -> None:
        """Remove a triangle from the set.

        Args:
            triangle_or_id (Triangle|int): The triangle to remove, or its index.

        Raises:
            ValueError: If the triangle does not exist in the set.
            IndexError: If the index is out of bounds.

        """
        if isinstance(triangle_or_id, int):
            del self._triangles[triangle_or_id]
        else:
            if not isinstance(triangle_or_id, _Triangle):
                triangle_or_id = _Triangle(*triangle_or_id)
            self._triangles.remove(triangle_or_id)
    
    def __iter__(self) -> Iterator[Triangle]:
        """Return an iterator over the triangles in the set.

        Returns:
            Iterable[Triangle]: An iterator over the triangles in the set.

        """
        yield from self._triangles
    
    def nb_triangles(self) -> int:
        """Return the number of triangles in the set.

        Returns:
            int: The number of triangles in the set.

        """
        return len(self._triangles)
    
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
        return self._triangles[index]
    
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
        if not isinstance(value, _Triangle):
            value = _Triangle(*value)
        self._triangles[index] = value
    
    def __eq__(self, other: object) -> bool:
        """Check if two Triangles objects are equal.

        Args:
            other (object): The other Triangles object to compare with.

        Raises:
            TypeError: If the other object is not a Triangles object.

        Returns:
            bool: True if the two Triangles objects are equal (all triangles are the same and in the same order, and the underlying PointSets are equal), False otherwise.

        """
        if isinstance(other, Triangles):
            return self._points == other._points and self._triangles == other._triangles
        raise TypeError("Can only compare Triangles with another Triangles object.")
    
    def to_bytes(self) -> bytes:
        """Serialize the Triangles to bytes for transmission.

        La représentation binaire de Triangles est donc en deux parties:

        - La première partie décrit les sommets et est strictement la même que pour un PointSet
        - La seconde partie décrit les triangles à proprement parler et se compose de:
          - 4 bytes (un unsigned long) qui représente le nombre de triangles
          - 3 x 4 x {nombre de triangles} bytes, pour chaque triangle il y a donc 12 bytes,
            chaque 4 bytes sont un unsigned long qui référence l'indice d'un sommet du triangle dans le PointSet.

        Returns:
            bytes: The serialized Triangles.

        """
        data = self._points.to_bytes()
        data += pack('!L', len(self._triangles))
        for triangle in self._triangles:
            data += pack('!III', *triangle.indices)
        return data

    
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
        offset = 0
        if len(data) < 4:
            raise ValueError("Invalid data: too short to contain number of points.")
        nb_points = unpack('!L', data[:4])[0]
        point_size = calcsize('!ff')
        pointset = PointSet.from_bytes_with_size(data[4:point_size * nb_points + 4], nb_points)
        try:
            ps_size = 4 + nb_points * 8
            offset += ps_size
            nb_triangles = unpack('!L', data[offset:offset + 4])[0]
            offset += 4
            triangles = []
            for _ in range(nb_triangles):
                p1, p2, p3 = unpack('!III', data[offset:offset + 12])
                triangles.append((p1, p2, p3))
                offset += 12
            return cls(points=pointset, triangles=triangles)
        except Exception as e:
            raise ValueError("Invalid or corrupted data for Triangles deserialization.") from e
    
    def __repr__(self) -> str:
        """Return a string representation of the Triangles.

        Returns:
            str: A string representation of the Triangles.

        """
        return f"Triangles(points={self._points}, triangles={self._triangles})"