# FreightOpt — Transporter Assignment Optimization API

FreightOpt is a backend service for assigning transporters to trade lanes while minimizing transportation cost and respecting a maximum transporter limit.

The project was developed as part of the FreightFox backend assignment.

---

## Problem Statement

Given:

- A set of trade lanes
- Multiple transporters
- A quote from each transporter for one or more lanes
- A maximum number of transporters that may be used

The system generates an assignment that:

1. Covers every lane.
2. Uses no more than the requested transporter limit.
3. Minimizes the total assignment cost among valid solutions.

---

## Tech Stack

- Python 3
- FastAPI
- Pydantic
- Pytest
- Uvicorn

---

## Project Structure

```text
Transport Lane Assignment/
│
├── app/
│   ├── main.py
│   │
│   ├── models/
│   │   └── transporter.py
│   │
│   └── services/
│       ├── optimizer.py
│       └── storage.py
│
├── tests/
│   ├── test_api.py
│   └── test_optimizer.py
│
├── requirements.txt
├── README.md
└── .gitignore
````

---

## Architecture

```text
                    Client
                      │
                      ▼
                FastAPI API
                      │
             ┌────────┴────────┐
             ▼                 ▼
       Input Validation    Assignment
          Pydantic          Request
             │                 │
             ▼                 ▼
          Storage          Optimizer
                               │
                               ▼
                         Best Assignment
                               │
                               ▼
                            Response
```

---

## API Endpoints

### 1. Health Check

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

---

### 2. Submit Transporter Quotes

```http
POST /api/v1/transporters/input
```

Example request:

```json
{
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
```

Response:

```json
{
  "message": "Transporter quotes received successfully"
}
```

---

### 3. Generate Transporter Assignment

```http
POST /api/v1/transporters/assignment
```

Request:

```json
{
  "maxTransporters": 2
}
```

Response:

```json
{
  "totalCost": 21000,
  "assignments": {
    "Lane 1": "T1",
    "Lane 2": "T2"
  },
  "transporters": [
    "T1",
    "T2"
  ]
}
```

---

## Optimization Approach

The optimizer evaluates combinations of available transporters.

For each candidate transporter group:

1. Check whether every lane can be covered.
2. Select the lowest quote available for each lane within that group.
3. Calculate the total cost.
4. Compare valid solutions.

The implementation uses Python's `itertools.combinations` to evaluate transporter groups.

This approach was chosen because the assignment requires optimization over a bounded set of transporters and keeps the logic deterministic and easy to test.

---

## Optimization Objectives

The assignment describes three objectives:

1. Full lane coverage.
2. Maximum transporter usage up to the requested limit.
3. Cost minimization.

For this implementation, the objectives are interpreted as:

```text
1. Find a feasible solution covering every lane.
2. Respect the maximum transporter limit.
3. Minimize total cost among feasible assignments.
```

The exact interpretation of "maximize transporter usage" can be ambiguous when fewer transporters can achieve the same or lower cost. Therefore, the implementation prioritizes the explicit maximum limit as a constraint and cost minimization among valid solutions.

---

## Validation

The API validates:

* At least one lane must be provided.
* Each lane must have at least one transporter quote.
* Transporter quotes cannot be negative.
* `maxTransporters` must be greater than zero.
* An assignment cannot be generated before quotes are submitted.
* An error is returned when full lane coverage is impossible.

---

## Running Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd "Transport Lane Assignment"
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Running Tests

Run:

```bash
pytest
```

The test suite covers:

* Optimizer correctness
* API input handling
* Assignment generation
* Invalid transporter limits
* Missing input data
* Negative transporter quotes
* Impossible lane coverage
* Health check

---

## Design Decisions

### In-memory storage

Transporter quotes are currently stored in memory because the assignment focuses on the optimization workflow rather than persistent data storage.

The storage layer is isolated in:

```text
app/services/storage.py
```

This allows persistent storage to be introduced later without changing the optimization logic.

### Separation of concerns

The application separates:

* API routing
* Request/response validation
* Storage
* Optimization logic

This keeps the optimizer independent from FastAPI and makes it easier to test.

---

## Limitations

The current implementation uses an exhaustive transporter-group search.

For a very large number of transporters, the number of combinations can grow significantly. A production system with a substantially larger search space could use techniques such as integer programming, constraint programming, or other optimization algorithms.

For the scope of this assignment, the current approach keeps the implementation deterministic, transparent, and easy to validate.

---

## Future Improvements

Potential production improvements include:

* Persistent database storage
* Redis or another caching layer
* Authentication and authorization
* Request IDs and structured logging
* Docker containerization
* CI/CD pipeline
* Optimization metrics and execution-time monitoring
* More advanced optimization algorithms for larger datasets
* API versioning and centralized error handling

---

## License

This project was created as part of a technical assignment.

---
