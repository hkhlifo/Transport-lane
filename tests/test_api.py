from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_submit_transporter_quotes():
    payload = {
        "lanes": [
            {
                "lane": "Lane 1",
                "quotes": {
                    "T1": 10000,
                    "T2": 12000
                }
            },
            {
                "lane": "Lane 2",
                "quotes": {
                    "T1": 15000,
                    "T2": 11000
                }
            }
        ]
    }

    response = client.post(
        "/api/v1/transporters/input",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Transporter quotes received successfully"