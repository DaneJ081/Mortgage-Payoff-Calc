import io
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


def test_plot_endpoint_no_plot(client):
    backup = app.current_plot
    app.current_plot = None

    response = client.get("/plot.png")
    assert response.status_code == 404

    app.current_plot = backup


def test_plot_endpoint_with_plot(client):
    buf = io.BytesIO()
    app.plt.figure()
    app.plt.plot([0, 1], [0, 1])
    app.plt.savefig(buf, format="png")
    app.plt.close()
    buf.seek(0)

    backup = app.current_plot
    app.current_plot = buf

    response = client.get("/plot.png")
    assert response.status_code == 200
    assert response.content_type == "image/png"

    app.current_plot = backup
