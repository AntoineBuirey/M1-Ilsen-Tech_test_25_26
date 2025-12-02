import re
import urllib.request as req
from io import BytesIO

import pytest
from datasets import IDS, POINTS

from triangulator.pointset import PointSet
from triangulator.PSM import PointSetManager

RE_UUID = re.compile(r"^[0-9a-fA-F-]{36}$")

class MockResponse:
    def __init__(self, data: bytes, status: int = 200) -> None:
        self._data = BytesIO(data)
        self.status = status
        self.reason = "OK" if status == 200 else "Error"
        
    def read(self, amt: int | None = None) -> bytes:
        return self._data.read(amt)


def mocked_urlopen(url : str|req.Request, data = None,
    timeout: float | None = None, *, context = None):
    # Extract point_set_id from URL
    if isinstance(url, req.Request):
        url_str = url.full_url
    else:
        url_str = url
    point_set_id = url_str.rsplit('/', 1)[-1]
    if not RE_UUID.match(point_set_id):
        message = b'{"code":"BAD_REQUEST","message":"Invalid point set ID \''+ point_set_id.encode() + b'\'"}'
        return MockResponse(message, status=400)
    if point_set_id not in POINTS:
        message = b'{"code":"NOT_FOUND","message":"The requested resource \'' + point_set_id.encode() + b'\' could not be found"}'
        return MockResponse(message, status=404)
    return MockResponse(POINTS[point_set_id], status=200)

def mocked_urlopen_unavailable_database(url : str|req.Request, data = None,
    timeout: float | None = None, *, context = None):
    return MockResponse(b'{"code":"SERVICE_UNAVAILABLE","message":"Database is currently unavailable"}', status=503)



class TestPointSetManager:
    @pytest.mark.parametrize("point_set_id", IDS[2:])
    def test_get_point_set_success(self, monkeypatch, point_set_id : str) -> None:
        monkeypatch.setattr(req, "urlopen", mocked_urlopen)
        point_set = PointSetManager.get_point_set(point_set_id)
        assert isinstance(point_set, PointSet)

    @pytest.mark.parametrize("point_set_id", [
        "non-existent-id-0000-0000-000000000000", # invalid UUID
        "123e4567-e89b-12d3-a456-426614174000",   # valid UUID but not in DATASETS
    ])
    def test_get_point_set_not_found(self, monkeypatch, point_set_id : str) -> None:
        monkeypatch.setattr(req, "urlopen", mocked_urlopen)
        with pytest.raises(KeyError) as excinfo:
            PointSetManager.get_point_set(point_set_id)
        assert f"The requested resource '{point_set_id}' could not be found" in str(excinfo.value)

    def test_get_point_set_unavailable_database(self, monkeypatch) -> None:
        monkeypatch.setattr(req, "urlopen", mocked_urlopen_unavailable_database)
        with pytest.raises(RuntimeError) as excinfo:
            PointSetManager.get_point_set(IDS[2])
        assert "Database is currently unavailable" in str(excinfo.value)

    def test_get_point_set_invalid_id(self, monkeypatch) -> None:
        monkeypatch.setattr(req, "urlopen", mocked_urlopen)
        with pytest.raises(ValueError) as excinfo:
            PointSetManager.get_point_set("invalid-uuid-format")
        assert "Invalid point set ID 'invalid-uuid-format'" in str(excinfo.value)