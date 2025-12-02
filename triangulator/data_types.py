"""Module defining basic data types: Point and Triangle."""

class Point:
    """A 2D point with x and y coordinates."""

    def __init__(self, x: float, y: float) -> None:
        """Initialize the Point with x and y coordinates."""
        self.__x = x
        self.__y = y
    
    def __eq__(self, other: object) -> bool:
        """Compare this Point with another Point for equality.

        Args:
            other (object): The other Point to compare with.

        Raises:
            TypeError: If other is not a Point.

        Returns:
            bool: True if the points are equal, False otherwise.

        """
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, tuple) and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        elif isinstance(other, list) and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            raise TypeError("Comparison is only supported with Point, tuple of two floats, or list of two floats.")
    
    @property
    def x(self) -> float:
        """Return the x coordinate of the point.

        Returns:
            float: The x coordinate of the point.

        """
        return self.__x
    
    @property
    def y(self) -> float:
        """Return the y coordinate of the point.

        Returns:
            float: The y coordinate of the point.

        """
        return self.__y
    
class Triangle:
    """A triangle defined by three point indices."""
    
    def __init__(self, p1: int, p2: int, p3: int) -> None:
        """Initialize the Triangle with three point indices."""
        self.__points = (p1, p2, p3)
    
    def __eq__(self, other: object) -> bool:
        """Compare this Triangle with another Triangle for equality.

        Args:
            other (object): The other Triangle to compare with.

        Raises:
            TypeError: If other is not a Triangle.

        Returns:
            bool: True if the triangles are equal, False otherwise. The order of points does not matter.

        """
        if not isinstance(other, Triangle):
            raise TypeError("Comparison is only supported with Triangle.")
        return set(self.__points) == set(other.__points)

    @property
    def indices(self) -> tuple[int, int, int]:
        """Return the indices of the points that make up the triangle.

        Returns:
            tuple[int, int, int]: The indices of the points that make up the triangle.

        """
        return self.__points