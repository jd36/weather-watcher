from fastapi.testclient import TestClient
from weather_watcher.main import app


client = TestClient(app)
LIMIT = 20
HTTP_SUCCESS = 200


def test_get_stations():
    response = client.get("/api/weather/stations")
    response_json = response.json()
    first_item = response_json[0]

    assert response.status_code == HTTP_SUCCESS
    assert len(response_json) == LIMIT
    assert isinstance(response_json, list)
    assert isinstance(first_item, dict)
    assert set(first_item.keys()) == {"id", "name"}
    print(first_item)


def test_get_measurements():
    response = client.get("/api/weather/")
    response_json = response.json()
    first_item = response_json[0]

    assert response.status_code == HTTP_SUCCESS
    assert len(response_json) == LIMIT
    assert isinstance(response_json, list)
    assert isinstance(first_item, dict)
    assert set(first_item.keys()) == {
        "id",
        "station_name",
        "date",
        "max_temperature",
        "min_temperature",
        "precipitation",
    }
    print(first_item)


def test_get_stats():
    response = client.get("/api/weather/stats")
    response_json = response.json()
    first_item = response_json[0]

    assert response.status_code == HTTP_SUCCESS
    assert len(response_json) == LIMIT
    assert isinstance(response_json, list)
    assert isinstance(first_item, dict)
    assert set(first_item.keys()) == {
        "id",
        "station_name",
        "year",
        "avg_max_temperature",
        "avg_min_temperature",
        "total_precipitation",
    }
    print(first_item)
