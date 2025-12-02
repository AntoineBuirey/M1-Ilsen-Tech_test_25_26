""""Module for managing a set of 2D points."""

from collections.abc import Iterable, Iterator

from .data_types import Point as _Point

type Point = _Point|tuple[float, float]

class PointSet:
    """A set of 2D points."""
    
    def __init__(self, points : Iterable[Point] | None = None) -> None:
        """Initialize the PointSet."""
        pass
    
    def add_point(self, point : Point) -> int:
        """Add a point to the set.

        Args:
            point (Point): The point to add.

        Raises:
            ValueError: If the point already exists in the set.

        Returns:
            int: The index of the added point.

        """
        pass
    
    def remove_point(self, point : Point) -> None:
        """Remove a point from the set.

        Args:
            point (Point): The point to remove.

        Raises:
            ValueError: If the point does not exist in the set.

        """
        pass
    
    def __iter__(self) -> Iterator[Point]:
        """Return an iterator over the points in the set.

        Returns:
            Iterable[Point]: An iterator over the points in the set.

        """
    
    def nb_points(self) -> int:
        """Return the number of points in the set.

        Returns:
            int: The number of points in the set.

        """
        pass
    
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
        pass
    
    def set_point(self, index: int, value: Point) -> None:
        """Set the point at the given index.

        Args:
            index (int): The index of the point to set.
            value (Point): The new value for the point.

        Raises:
            IndexError: If the index is out of bounds.

        """
        pass

    def __eq__(self, other: object) -> bool:
        """Compare this PointSet with another PointSet for equality.

        Args:
            other (object): The other PointSet to compare with.

        Raises:
            TypeError: If other is not a PointSet.

        Returns:
            bool: True if the PointSets are equal, False otherwise.

        """
        pass
    
    def to_bytes(self) -> bytes:
        """Serialize the PointSet to bytes for transmission.

        Returns:
            bytes: The serialized PointSet.

        """
        pass
    
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
        pass
