from app.services.optimizer import optimize_assignments


def test_finds_best_assignment_with_two_transporters():
    quotes = {
        "L1": {
            "T1": 10,
            "T2": 20,
            "T3": 15,
        },
        "L2": {
            "T1": 30,
            "T2": 12,
            "T3": 18,
        },
        "L3": {
            "T1": 25,
            "T2": 20,
            "T3": 8,
        },
    }

    result = optimize_assignments(
        quotes,
        max_transporters=2,
    )

    assert result["total_cost"] == 35

    assert result["assignments"] == {
        "L1": "T3",
        "L2": "T2",
        "L3": "T3",
    }


def test_optimizer_with_freightfox_data():

    quotes = {
        "Lane 1": {
            "T1": 20835,
            "T2": 48844,
            "T3": 39020,
            "T4": 14400,
            "T5": 11601,
            "T6": 35095,
            "T7": 26070,
        },
        "Lane 2": {
            "T1": 10512,
            "T2": 31326,
            "T3": 20648,
            "T4": 44514,
            "T5": 19760,
            "T6": 12494,
            "T7": 41098,
        },
        "Lane 3": {
            "T1": 22105,
            "T2": 18640,
            "T3": 31438,
            "T4": 14316,
            "T5": 40870,
            "T6": 17808,
            "T7": 20932,
        },
        "Lane 4": {
            "T1": 42481,
            "T2": 45828,
            "T3": 36447,
            "T4": 10678,
            "T5": 20635,
            "T6": 36210,
            "T7": 16897,
        },
        "Lane 5": {
            "T1": 19862,
            "T2": 18297,
            "T3": 12789,
            "T4": 13032,
            "T5": 26421,
            "T6": 39444,
            "T7": 27938,
        },
        "Lane 6": {
            "T1": 13567,
            "T2": 45810,
            "T3": 49985,
            "T4": 46024,
            "T5": 28809,
            "T6": 29948,
            "T7": 43517,
        },
        "Lane 7": {
            "T1": 10015,
            "T2": 49573,
            "T3": 35285,
            "T4": 42342,
            "T5": 27815,
            "T6": 17320,
            "T7": 25881,
        },
        "Lane 8": {
            "T1": 17886,
            "T2": 45122,
            "T3": 10281,
            "T4": 35742,
            "T5": 17024,
            "T6": 10492,
            "T7": 46136,
        },
        "Lane 9": {
            "T1": 43996,
            "T2": 31856,
            "T3": 40092,
            "T4": 48921,
            "T5": 44691,
            "T6": 37864,
            "T7": 31286,
        },
    }
    result = optimize_assignments(
        quotes,
        max_transporters=3,
    )

    assert result is not None
    assert result["total_cost"] == 134876
    assert len(result["transporters"]) == 3
    assert len(result["assignments"]) == 9