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


def test_generate_transporter_assignment():
    input_payload = {
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

    input_response = client.post(
        "/api/v1/transporters/input",
        json=input_payload
    )

    assert input_response.status_code == 200

    assignment_response = client.post(
        "/api/v1/transporters/assignment",
        json={"maxTransporters": 2}
    )

    assert assignment_response.status_code == 200

    data = assignment_response.json()

    assert data["totalCost"] == 21000
    assert data["assignments"]["Lane 1"] == "T1"
    assert data["assignments"]["Lane 2"] == "T2"
    

def test_assignment_rejects_invalid_max_transporters():
    response = client.post(
        "/api/v1/transporters/assignment",
        json={"maxTransporters": 0}
    )

    assert response.status_code == 422
    
def test_assignment_fails_without_input():
    from app.services import storage

    storage.transporter_quotes.clear()

    response = client.post(
        "/api/v1/transporters/assignment",
        json={"maxTransporters": 2}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Transporter quotes have not been submitted"
    )