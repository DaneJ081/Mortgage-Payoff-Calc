import pytest
import app


@pytest.fixture
def client():
    app.app.config["TESTING"] = True
    with app.app.test_client() as client:
        yield client


def test_index_get(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<form" in response.data


def test_index_post_valid_data(client):
    data = {
        "loan": "100000",
        "rate": "5",
        "term": "30",
        "extra": "200",
        "tax": "3600",
        "insurance": "1200",
        "HOA": "600",
        "repairs": "1",
    }
    response = client.post("/", data=data)
    assert response.status_code == 200
    assert b"1000" in response.data
    assert b"data:image/png;base64," in response.data


def test_index_post_invalid_data(client):
    data = {
        "loan": "abc",
        "rate": "xyz",
        "term": "0",
        "extra": "0",
        "tax": "0",
        "insurance": "0",
    }
    response = client.post("/", data=data)
    assert response.status_code == 200
    assert b"Invalid input" in response.data


def test_index_post_zero_term_rejected(client):
    data = {
        "loan": "100000",
        "rate": "5",
        "term": "0",
        "extra": "0",
        "tax": "0",
        "insurance": "0",
    }
    response = client.post("/", data=data)
    assert response.status_code == 200
    assert b"Invalid input" in response.data


def test_index_post_negative_extra_payment_rejected(client):
    # Regression test: a negative extra payment used to make the amortization
    # loop's principal reduction clamp to zero forever, hanging the request.
    data = {
        "loan": "100000",
        "rate": "5",
        "term": "30",
        "extra": "-999999",
        "tax": "0",
        "insurance": "0",
    }
    response = client.post("/", data=data)
    assert response.status_code == 200
    assert b"Invalid input" in response.data


@pytest.mark.parametrize("bad_rate", ["nan", "inf", "-inf"])
def test_index_post_non_finite_rejected(client, bad_rate):
    # Regression test: float() parses "nan"/"inf" successfully, and neither
    # passed the existing bounds checks (e.g. inf > 0), letting non-finite
    # values reach the calculation and produce garbage output.
    data = {
        "loan": "100000",
        "rate": bad_rate,
        "term": "30",
        "extra": "0",
        "tax": "0",
        "insurance": "0",
    }
    response = client.post("/", data=data)
    assert response.status_code == 200
    assert b"Invalid input" in response.data


def test_index_post_downpayment_over_100_rejected(client):
    data = {
        "loan": "100000",
        "downpayment": "150",
        "rate": "5",
        "term": "30",
        "extra": "0",
        "tax": "0",
        "insurance": "0",
    }
    response = client.post("/", data=data)
    assert response.status_code == 200
    assert b"Invalid input" in response.data
