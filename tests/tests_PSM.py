import re
import os
import urllib.request as req
from io import BytesIO

import pytest
from datasets import IDS, POINTS, UNKNOWN_ID, MALFORMED_ID

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
    
    def __enter__(self) -> "MockResponse":
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._data.close()


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

def mocked_getenv(key: str, default: str | None = None) -> str | None:
    if key == "POINTSET_API_URL":
        return "http://mocked.api/pointset"
    return default

class TestPointSetManager:
    @pytest.mark.parametrize("point_set_id", IDS[2:])
    def test_get_point_set_success(self, monkeypatch, point_set_id : str) -> None:
        monkeypatch.setattr(req, "urlopen", mocked_urlopen)
        monkeypatch.setattr(os, "getenv", mocked_getenv)
        point_set = PointSetManager.get_point_set(point_set_id)
        assert isinstance(point_set, PointSet)


    def test_get_point_set_not_found(self, monkeypatch) -> None:
        monkeypatch.setattr(req, "urlopen", mocked_urlopen)
        monkeypatch.setattr(os, "getenv", mocked_getenv)
        with pytest.raises(KeyError) as excinfo:
            PointSetManager.get_point_set(UNKNOWN_ID)
        assert f"The requested resource '{UNKNOWN_ID}' could not be found" in excinfo.value.args[0]

    def test_get_point_set_unavailable_database(self, monkeypatch) -> None:
        monkeypatch.setattr(req, "urlopen", mocked_urlopen_unavailable_database)
        monkeypatch.setattr(os, "getenv", mocked_getenv)
        with pytest.raises(RuntimeError) as excinfo:
            PointSetManager.get_point_set(IDS[2])
        assert "Database is currently unavailable" in str(excinfo.value)

    def test_get_point_set_invalid_id(self, monkeypatch) -> None:
        monkeypatch.setattr(req, "urlopen", mocked_urlopen)
        monkeypatch.setattr(os, "getenv", mocked_getenv)
        with pytest.raises(ValueError) as excinfo:
            PointSetManager.get_point_set(MALFORMED_ID)
        assert f"Malformed point set ID: {MALFORMED_ID}" in excinfo.value.args[0]