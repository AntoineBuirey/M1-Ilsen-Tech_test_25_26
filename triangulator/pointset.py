""""Module for managing a set of 2D points."""

from collections.abc import Iterable, Iterator
from struct import pack, unpack, calcsize

from .data_types import Point as _Point

type Point = tuple[float, float] | _Point
class PointSet:
    """A set of 2D points."""
    
    def __init__(self, points : Iterable[Point] | None = None) -> None:
        """Initialize the PointSet."""
        self.__points : list[_Point] = []
        if points is not None:
            for point in points:
                self.add_point(point)
    
    def add_point(self, point : Point) -> int:
        """Add a point to the set.

        Args:
            point (Point): The point to add.

        Raises:
            ValueError: If the point already exists in the set.

        Returns:
            int: The index of the added point.

        """
        if isinstance(point, tuple):
            point = _Point(*point)
        if point in self.__points:
            raise ValueError("Point already exists in the set.")
        self.__points.append(point)
        return len(self.__points) - 1
    
    def remove_point(self, point : Point) -> None:
        """Remove a point from the set.

        Args:
            point (Point): The point to remove.

        Raises:
            ValueError: If the point does not exist in the set.

        """
        if isinstance(point, tuple):
            point = _Point(*point)
        self.__points.remove(point)
    
    def __iter__(self) -> Iterator[Point]:
        """Return an iterator over the points in the set.

        Returns:
            Iterable[Point]: An iterator over the points in the set.

        """
        return iter(self.__points)
    
    def nb_points(self) -> int:
        """Return the number of points in the set.

        Returns:
            int: The number of points in the set.

        """
        return len(self.__points)
    
    def __len__(self) -> int:
        """Return the number of points in the set.

        Returns:
            int: The number of points in the set.

        """
        return self.nb_points()
    
    def get_point(self, index: int) -> Point:
        """Return the point at the given index.

        Args:
            index (int): The index of the point to retrieve.

        Raises:
            IndexError: If the index is out of bounds.

        Returns:
            Point: The point at the given index.

        """
        return self.__points[index]
    
    def set_point(self, index: int, value: Point) -> None:
        """Set the point at the given index.

        Args:
            index (int): The index of the point to set.
            value (Point): The new value for the point.

        Raises:
            IndexError: If the index is out of bounds.

        """
        if isinstance(value, tuple):
            value = _Point(*value)
        self.__points[index] = value

    def __eq__(self, other: object) -> bool:
        """Compare this PointSet with another PointSet for equality.

        Args:
            other (object): The other PointSet to compare with.

        Raises:
            TypeError: If other is not a PointSet.

        Returns:
            bool: True if the PointSets are equal, False otherwise.

        """
        if not isinstance(other, PointSet):
            raise TypeError("Can only compare PointSet with another PointSet.")
        return self.__points == other.__points
    
    def to_bytes(self) -> bytes:
        """Serialize the PointSet to bytes for transmission.
        
        PointSet est un ensemble de points dans un espace en 2D, chaque point de l'ensemble se résume donc à 2 coordonnées, X et Y.
        La représentation de ces données est assez simple:

        - Les 4 premiers bytes représentent un unsigned long donnant le nombre de points dans l'ensemble
        - Les bytes suivants représentent les points, avec pour chaque point 8 bytes. Les 4 premiers bytes sont la coordonnée X (un float)
            et les 4 bytes suivant la coordonnée Y (un float aussi).

        Returns:
            bytes: The serialized PointSet.

        """
        data = pack('!L', len(self.__points))
        for point in self.__points:
            data += pack('!ff', point.x, point.y)
        return data
    

    @classmethod
    def from_bytes_with_size(cls, data: bytes, nb_points) -> 'PointSet':
        """Deserialize bytes to a PointSet object.
        Only handle the points data, nb_points must be provided.

        Args:
            data (bytes): The bytes to deserialize.

        Raises:
            ValueError: If the data is invalid.

        Returns:
            PointSet: The deserialized PointSet object.

        """
        point_size = calcsize('!ff')
        expected_size = nb_points * point_size
        if len(data) != expected_size:
            raise ValueError(f"Invalid data: size does not match number of points. (expected {expected_size}, got {len(data)})")
        points = []
        offset = 0
        for _ in range(nb_points):
            x, y = unpack('!ff', data[offset:offset + point_size])
            points.append(_Point(x, y))
            offset += point_size
        return cls(points)
    
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'PointSet':
        """Deserialize bytes to a PointSet object.

        Args:
            data (bytes): The bytes to deserialize.

        Raises:
            ValueError: If the data is invalid.

        Returns:
            PointSet: The deserialized PointSet object.

        """
        if len(data) < 4:
            raise ValueError("Invalid data: too short to contain number of points.")
        nb_points = unpack('!L', data[:4])[0]
        return cls.from_bytes_with_size(data[4:], nb_points)

    def __repr__(self) -> str:
        """Return a string representation of the PointSet.

        Returns:
            str: A string representation of the PointSet.

        """
        return f"PointSet({self.__points})"
