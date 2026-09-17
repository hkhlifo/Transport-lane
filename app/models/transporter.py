from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class LaneQuote(BaseModel):
    lane: str = Field(..., min_length=1)
    quotes: dict[str, Annotated[float, Field(ge=0)]] = Field(
        ...,
        min_length=1
    )


class TransporterInput(BaseModel):
    lanes: list[LaneQuote] = Field(..., min_length=1)