"""Module defining basic data types: Point and Triangle."""

class Point:
    """A 2D point with x and y coordinates."""

    def __init__(self, x: float, y: float) -> None:
        """Initialize the Point with x and y coordinates."""
        pass
    
    def __eq__(self, other: object) -> bool:
        """Compare this Point with another Point for equality.

        Args:
            other (object): The other Point to compare with.

        Raises:
            TypeError: If other is not a Point.

        Returns:
            bool: True if the points are equal, False otherwise.

        """
        pass
    
    @property
    def x(self) -> float:
        """Return the x coordinate of the point.

        Returns:
            float: The x coordinate of the point.

        """
        pass
    
    @property
    def y(self) -> float:
        """Return the y coordinate of the point.

        Returns:
            float: The y coordinate of the point.

        """
        pass
    
class Triangle:
    """A triangle defined by three point indices."""
    
    def __init__(self, p1: int, p2: int, p3: int) -> None:
        """Initialize the Triangle with three point indices."""
        pass
    
    def __eq__(self, other: object) -> bool:
        """Compare this Triangle with another Triangle for equality.

        Args:
            other (object): The other Triangle to compare with.

        Raises:
            TypeError: If other is not a Triangle.

        Returns:
            bool: True if the triangles are equal, False otherwise. The order of points does not matter.

        """
        pass

    @property
    def indices(self) -> set[int, int, int]:
        """Return the indices of the points that make up the triangle.

        Returns:
            set[int, int, int]: The indices of the points that make up the triangle.

        """
        pass