from fastapi.testclient import TestClient
from app.services.storage import clear_quotes

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
    
def test_rejects_negative_transporter_quote():
    payload = {
        "lanes": [
            {
                "lane": "Lane 1",
                "quotes": {
                    "T1": -5000
                }
            }
        ]
    }

    response = client.post(
        "/api/v1/transporters/input",
        json=payload
    )

    assert response.status_code == 422
    
    
def test_assignment_fails_when_lane_coverage_is_impossible():
    clear_quotes()

    payload = {
        "lanes": [
            {
                "lane": "Lane 1",
                "quotes": {
                    "T1": 10000
                }
            },
            {
                "lane": "Lane 2",
                "quotes": {
                    "T2": 12000
                }
            }
        ]
    }

    input_response = client.post(
        "/api/v1/transporters/input",
        json=payload
    )

    assert input_response.status_code == 200

    response = client.post(
        "/api/v1/transporters/assignment",
        json={"maxTransporters": 1}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Unable to find a valid assignment"
    )
    
def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }
    
def test_freightfox_dataset_assignment():
    clear_quotes()

    payload = {
        "lanes": [
            {
                "lane": "Lane 1",
                "quotes": {
                    "T1": 20835,
                    "T2": 48844,
                    "T3": 39020,
                    "T4": 14400,
                    "T5": 11601,
                    "T6": 35095,
                    "T7": 26070,
                },
            },
            {
                "lane": "Lane 2",
                "quotes": {
                    "T1": 10512,
                    "T2": 31326,
                    "T3": 20648,
                    "T4": 44514,
                    "T5": 19760,
                    "T6": 12494,
                    "T7": 41098,
                },
            },
            {
                "lane": "Lane 3",
                "quotes": {
                    "T1": 22105,
                    "T2": 18640,
                    "T3": 31438,
                    "T4": 14316,
                    "T5": 40870,
                    "T6": 17808,
                    "T7": 20932,
                },
            },
            {
                "lane": "Lane 4",
                "quotes": {
                    "T1": 42481,
                    "T2": 45828,
                    "T3": 36447,
                    "T4": 10678,
                    "T5": 20635,
                    "T6": 36210,
                    "T7": 16897,
                },
            },
            {
                "lane": "Lane 5",
                "quotes": {
                    "T1": 19862,
                    "T2": 18297,
                    "T3": 12789,
                    "T4": 13032,
                    "T5": 26421,
                    "T6": 39444,
                    "T7": 27938,
                },
            },
            {
                "lane": "Lane 6",
                "quotes": {
                    "T1": 13567,
                    "T2": 45810,
                    "T3": 49985,
                    "T4": 46024,
                    "T5": 28809,
                    "T6": 29948,
                    "T7": 43517,
                },
            },
            {
                "lane": "Lane 7",
                "quotes": {
                    "T1": 10015,
                    "T2": 49573,
                    "T3": 35285,
                    "T4": 42342,
                    "T5": 27815,
                    "T6": 17320,
                    "T7": 25881,
                },
            },
            {
                "lane": "Lane 8",
                "quotes": {
                    "T1": 17886,
                    "T2": 45122,
                    "T3": 10281,
                    "T4": 35742,
                    "T5": 17024,
                    "T6": 10492,
                    "T7": 46136,
                },
            },
            {
                "lane": "Lane 9",
                "quotes": {
                    "T1": 43996,
                    "T2": 31856,
                    "T3": 40092,
                    "T4": 48921,
                    "T5": 44691,
                    "T6": 37864,
                    "T7": 31286,
                },
            },
        ]
    }

    input_response = client.post(
        "/api/v1/transporters/input",
        json=payload,
    )

    assert input_response.status_code == 200

    response = client.post(
        "/api/v1/transporters/assignment",
        json={"maxTransporters": 3},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["totalCost"] == 134876
    assert len(data["assignments"]) == 9
    assert len(data["transporters"]) == 3