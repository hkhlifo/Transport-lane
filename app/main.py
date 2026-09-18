from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.models.transporter import (
    TransporterInput,
    AssignmentResponse,
)
from app.services.storage import (
    get_quotes,
    save_quotes,
)
from app.services.optimizer import optimize_assignments


app = FastAPI(
    title="FreightOpt",
    description="Transporter Assignment Optimization API",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


class AssignmentRequest(BaseModel):
    maxTransporters: int = Field(..., gt=0)


@app.post("/api/v1/transporters/input")
def submit_transporter_quotes(data: TransporterInput):

    quotes = {
        lane.lane: lane.quotes
        for lane in data.lanes
    }

    save_quotes(quotes)

    return {
        "message": "Transporter quotes received successfully"
    }


@app.post(
    "/api/v1/transporters/assignment",
    response_model=AssignmentResponse
)
def generate_assignment(data: AssignmentRequest):

    quotes = get_quotes()

    if not quotes:
        raise HTTPException(
            status_code=400,
            detail="Transporter quotes have not been submitted"
        )

    result = optimize_assignments(
        quotes,
        data.maxTransporters
    )

    if result is None:
        raise HTTPException(
            status_code=400,
            detail="Unable to find a valid assignment"
        )

    return {
        "totalCost": result["total_cost"],
        "assignments": result["assignments"],
        "transporters": result["transporters"],
    }