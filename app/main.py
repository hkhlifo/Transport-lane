from fastapi import FastAPI

from app.models.transporter import TransporterInput
from app.services.storage import transporter_quotes


app = FastAPI(
    title="FreightOpt",
    description="Transporter Assignment Optimization API",
    version="1.0.0",
)


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