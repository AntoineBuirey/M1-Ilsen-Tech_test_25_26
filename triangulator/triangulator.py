from .data_types import PointSet, Triangles
from .PSM import PointSetManager

def triangulate(points: PointSet) -> Triangles:
    pass


def get_and_compute(point_set_id: str) -> bytes:
    """
    This method retrieves a PointSet by its ID using the PointSetManager,
    computes its triangulation using the triangulate function, and returns
    the serialized Triangles object as bytes.
    called by the HTTP server to handle requests.
    """
    pass