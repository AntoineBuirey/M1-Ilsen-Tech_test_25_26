
class Point:
    def __init__(self, x: float, y: float) -> None:
        pass
    
    def __eq__(self, other: object) -> bool:
        """Compares this Point with another Point for equality

        Args:
            other (object): the other Point to compare with
            
        Raises:
            TypeError: if other is not a Point

        Returns:
            bool: True if the points are equal, False otherwise
        """
        pass
    
    @property
    def x(self) -> float:
        """Returns the x coordinate of the point

        Returns:
            float: the x coordinate of the point
        """
        pass
    
    @property
    def y(self) -> float:
        """Returns the y coordinate of the point

        Returns:
            float: the y coordinate of the point
        """
        pass
    
class Triangle:
    def __init__(self, p1: int, p2: int, p3: int) -> None:
        pass
    
    def __eq__(self, other: object) -> bool:
        """Compares this Triangle with another Triangle for equality

        Args:
            other (object): the other Triangle to compare with
            
        Raises:
            TypeError: if other is not a Triangle

        Returns:
            bool: True if the triangles are equal, False otherwise the order of points does not matter
        """
        pass

    @property
    def indices(self) -> set[int, int, int]:
        """Returns the indices of the points that make up the triangle

        Returns:
            set[int, int, int]: the indices of the points that make up the triangle
        """
        pass