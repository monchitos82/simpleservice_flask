import pytest


def test_data_get(client, init_db) -> None:
    response = client.get("/data")
    assert response.status_code == 200
    assert "remote_random_data" in response.get_json()


@pytest.mark.parametrize(("number", "value"), [(0, 0), (1, 1), (2, 1), (3, 2), (7, 13), (-1, None)])
def test_fibo_get(client, init_db, number, value) -> None:
    response = client.get(f"/fibo/{number}")
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        assert response.get_json().get("result", None) == value


def test_data_post(client, init_db) -> None:
    data = {"key": "value"}
    response = client.post("/data", json=data)
    assert response.status_code == 200
    assert response.get_json() == data


def test_error(client, init_db) -> None:
    response = client.get("/errors")
    assert response.status_code in [400, 401, 404, 419, 429, 500, 503]
