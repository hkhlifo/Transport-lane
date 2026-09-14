from pydantic import BaseModel, Field


class LaneQuote(BaseModel):
    lane: str = Field(..., min_length=1)
    quotes: dict[str, float]


class TransporterInput(BaseModel):
    lanes: list[LaneQuote]