from typing import Annotated

from pydantic import BaseModel, Field, field_validator, model_validator


class LaneQuote(BaseModel):
    lane: str = Field(..., min_length=1)
    quotes: dict[str, Annotated[float, Field(ge=0)]] = Field(
        ...,
        min_length=1,
    )

    @field_validator("lane")
    @classmethod
    def validate_lane_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Lane name cannot be blank")

        return value

    @field_validator("quotes")
    @classmethod
    def validate_transporter_names(
        cls,
        value: dict[str, float],
    ) -> dict[str, float]:
        if any(not name.strip() for name in value):
            raise ValueError("Transporter names cannot be blank")

        return value


class TransporterInput(BaseModel):
    lanes: list[LaneQuote] = Field(..., min_length=1)

    @model_validator(mode="after")
    def validate_unique_lanes(self):
        lane_names = [lane.lane for lane in self.lanes]

        if len(lane_names) != len(set(lane_names)):
            raise ValueError("Lane names must be unique")

        return self


class AssignmentResponse(BaseModel):
    totalCost: float
    assignments: dict[str, str]
    transporters: list[str]


class ErrorResponse(BaseModel):
    detail: str