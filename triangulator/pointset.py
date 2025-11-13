from typing import Iterable, Iterator

from .data_types import Point as _Point

type Point = _Point|tuple[float, float]

class PointSet:
    def __init__(self, points : Iterable[Point] | None = None) -> None:
        pass
    
    def add_point(self, point : Point) -> int:
        """Adds a point to the set

        Args:
            point (Point): the point to add
            
        Raises:
            ValueError: if the point already exists in the set
            
        Returns:
            int: the index of the added point
        """
        pass
    
    def remove_point(self, point : Point) -> None:
        """Removes a point from the set
        
        Args:
            point (Point): the point to remove
            
        Raises:
            ValueError: if the point does not exist in the set 
        """
        pass
    
    def __iter__(self) -> Iterator[Point]:
        """Returns an iterator over the points in the set
        
        Returns:
            Iterable[Point]: an iterator over the points in the set
        """
    
    def nb_points(self) -> int:
        """Returns the number of points in the set
        
        Returns:
            int: the number of points in the set
        """
        pass
    
    def __len__(self) -> int:
        """Returns the number of points in the set
        
        Returns:
            int: the number of points in the set
        """
        return self.nb_points()
    
    def get_point(self, index: int) -> Point:
        """Returns the point at the given index
        
        Args:
            index (int): the index of the point to retrieve
            
        Raises:
            IndexError: if the index is out of bounds
            
        Returns:
            Point: the point at the given index
        """
        pass
    
    def set_point(self, index: int, value: Point) -> None:
        """Sets the point at the given index
        
        Args:
            index (int): the index of the point to set
            value (Point): the new value for the point
            
        Raises:
            IndexError: if the index is out of bounds
        """
        pass

    def __eq__(self, other: object) -> bool:
        """Compares this PointSet with another PointSet for equality
        
        Args:
            other (object): the other PointSet to compare with
            
        Raises:
            TypeError: if other is not a PointSet
            
        Returns:
            bool: True if the PointSets are equal, False otherwise
        """
        pass
    
    def to_bytes(self) -> bytes:
        """Serializes the PointSet to bytes for transmission
        
        Returns:
            bytes: the serialized PointSet
        """
        pass
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'PointSet':
        """Deserializes bytes to a PointSet object
        
        Args:
            data (bytes): the bytes to deserialize
            
        Raises:
            ValueError: if the data is invalid
            
        Returns:
            PointSet: the deserialized PointSet object
        """
        pass
