import pytest

from datasets import IDS, TRIANGLES, MALFORMED_ID, UNKNOWN_ID



def mocked_get_and_compute(point_set_id: str) -> bytes:
    if point_set_id in IDS:
        return TRIANGLES[point_set_id]
    else:
        raise KeyError("Point set ID not found")
    
def mocked_get_and_compute_failed(point_set_id: str) -> bytes:
    raise Exception("Computation failed")

def mocked_get_and_compute_no_service(point_set_id: str) -> bytes:
    raise RuntimeError("Service not available")

ENDPOINT = "/triangulation/{point_set_id}"

@pytest.fixture
def client():
    from triangulator.http_server import HTTPServer
    server = HTTPServer(__name__)
    server.testing = True
    with server.test_client() as client:
        yield client

def test_triangulation_valid_id(client, monkeypatch):
    test_id = IDS[0]
    expected_response = TRIANGLES[test_id]
    
    monkeypatch.setattr("triangulator.triangulator.get_and_compute", mocked_get_and_compute)
    
    response = client.get(ENDPOINT.format(point_set_id=test_id))
    
    assert response.status_code == 200
    assert response.data == expected_response

def test_triangulation_unknown_id(client, monkeypatch):
    monkeypatch.setattr("triangulator.triangulator.get_and_compute", mocked_get_and_compute)
    
    response = client.get(ENDPOINT.format(point_set_id=UNKNOWN_ID))
    
    assert response.status_code == 404
    assert b"Point set ID not found" in response.data
    
def test_triangulation_malformed_id(client, monkeypatch):
    monkeypatch.setattr("triangulator.triangulator.get_and_compute", mocked_get_and_compute)
    
    response = client.get(ENDPOINT.format(point_set_id=MALFORMED_ID))
    
    assert response.status_code == 400
    assert b"Malformed point set ID" in response.data
    
def test_triangulation_no_id(client, monkeypatch):
    monkeypatch.setattr("triangulator.triangulator.get_and_compute", mocked_get_and_compute)
    
    response = client.get("/triangulation/")
    
    assert response.status_code == 400  # Flask returns 400 for missing parameters

def test_triangulation_internal_error(client, monkeypatch):
    test_id = IDS[0]
    
    monkeypatch.setattr("triangulator.triangulator.get_and_compute", mocked_get_and_compute_failed)
    
    response = client.get(ENDPOINT.format(point_set_id=test_id))
    
    assert response.status_code == 500
    assert b"Internal server error" in response.data
    
def test_triangulation_database_unavailable(client, monkeypatch):
    test_id = IDS[0]
    
    monkeypatch.setattr("triangulator.triangulator.get_and_compute", mocked_get_and_compute_no_service)
    
    response = client.get(ENDPOINT.format(point_set_id=test_id))
    
    assert response.status_code == 503
    assert b"Service not available" in response.data
