from typing import Any
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, field_serializer, field_validator
from pyproj import CRS

from .sample_rate import SampleRate
from .sensor import Sensor


class BaseMetadata(BaseModel):
    timezone: ZoneInfo | None = None
    crs: CRS | None = Field(default=None)

    class Config:
        arbitrary_types_allowed = True
        validate_assignment = True

    def __repr__(self):
        return f"Metadata(timezone={self.timezone}, crs={self.crs})"

    @field_serializer("crs")
    def serialize_crs(
        self,
        crs: CRS,
    ):
        if crs:
            return crs.to_string()

    @field_serializer("timezone")
    def serialize_timezone(
        self,
        timezone: ZoneInfo,
    ):
        if timezone:
            return str(timezone)

    @field_validator("crs", mode="before")
    @classmethod
    def parse_crs(cls, v: Any) -> CRS | Any:
        if v:
            return CRS.from_user_input(v)
        else:
            return v

    @field_validator("timezone", mode="before")
    @classmethod
    def parse_timezone(cls, v: Any) -> ZoneInfo | Any:
        if isinstance(v, str):
            return ZoneInfo(v)
        else:
            return v


class Metadata(BaseMetadata):
    sensors: list[Sensor] = Field(default_factory=list)
    sample_rate: SampleRate

    def __repr__(self):
        return f"Metadata(sensors={repr(self.sensors)}, sample_rate={self.sample_rate}, timezone={self.timezone}, crs={self.crs})"
