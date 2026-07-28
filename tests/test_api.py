def test_data_get(client, init_db) -> None:
    response = client.get("/data")
    assert response.status_code == 200
    assert "remote_random_data" in response.get_json()


def test_fibo_get(client) -> None:
    response = client.get("/fibo/6")
    assert response.status_code == 200
    assert response.get_json().get("result", None) == 8


def test_data_post(client, init_db) -> None:
    data = {"key": "value"}
    response = client.post("/data", json=data)
    assert response.status_code == 200
    assert response.get_json() == data


def test_error(client, init_db) -> None:
    response = client.get("/errors")
    assert response.status_code in [400, 401, 404, 419, 429, 500, 503]
