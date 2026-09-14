from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.models.transporter import TransporterInput
from app.services.storage import transporter_quotes
from app.services.optimizer import optimize_assignments


app = FastAPI(
    title="FreightOpt",
    description="Transporter Assignment Optimization API",
    version="1.0.0",
)


class AssignmentRequest(BaseModel):
    maxTransporters: int = Field(..., gt=0)


@app.post("/api/v1/transporters/input")
def submit_transporter_quotes(data: TransporterInput):
    global transporter_quotes

    transporter_quotes = {
        lane.lane: lane.quotes
        for lane in data.lanes
    }

    return {
        "message": "Transporter quotes received successfully"
    }


@app.post("/api/v1/transporters/assignment")
def generate_assignment(data: AssignmentRequest):

    if not transporter_quotes:
        raise HTTPException(
            status_code=400,
            detail="Transporter quotes have not been submitted"
        )

    result = optimize_assignments(
        transporter_quotes,
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