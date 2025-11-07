from typing import Iterable

type Point = tuple[float, float]
type Triangle = tuple[int, int, int]



class PointSet:
    def __init__(self, points : Iterable[Point] | None = None) -> None:
        pass
    
    def add_point(self, point : Point) -> None:
        pass
    
    def remove_point(self, point : Point) -> None:
        pass
    
    def __iter__(self):
        pass
    
    def __len__(self) -> int:
        pass
    
    def __getitem__(self, index: int) -> Point:
        pass
    
    def __setitem__(self, index: int, value: Point) -> None:
        pass

    def __eq__(self, other: object) -> bool:
        pass
    
    def to_bytes(self) -> bytes:
        pass
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'PointSet':
        pass


class Triangles(PointSet):
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
    
    def add_triangle(self, triangle : Triangle) -> None:
        pass
    
    def remove_triangle(self, triangle : Triangle) -> None:
        pass
    
    def __iter__(self):
        pass
    
    def __len__(self) -> int:
        pass
    
    def __getitem__(self, index: int) -> Triangle:
        pass
    
    def __setitem__(self, index: int, value: Triangle) -> None:
        pass
    
    def __eq__(self, other: object) -> bool:
        pass
    
    def to_bytes(self) -> bytes:
        pass
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'Triangles':
        pass