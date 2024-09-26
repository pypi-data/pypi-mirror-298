from datetime import timedelta
from typing import Self

from pydantic import BaseModel, PositiveFloat

from .validation.subject import SampleRateUnit


class SampleRate(BaseModel):
    value: PositiveFloat
    unit: SampleRateUnit

    class Config:
        validate_assignment = True

    def __str__(self):
        return f"{self.value}{self.unit}"

    def to_seconds(self) -> float:
        return (
            self.value  # type: ignore
            if self.unit == SampleRateUnit.SECOND
            else 1 / self.value  # type: ignore
        )

    def to_hz(self) -> float:
        return (
            self.value  # type: ignore
            if self.unit == SampleRateUnit.HERTZ
            else 1 / self.value  # type: ignore
        )

    def to_timedelta(self) -> timedelta:
        seconds = self.to_seconds()
        return timedelta(seconds=seconds)

    def set_unit(self, target: SampleRateUnit) -> None:
        if target == self.unit:
            pass
        elif target == SampleRateUnit.SECOND:
            value = self.to_seconds()
        elif target == SampleRateUnit.HERTZ:
            value = self.to_hz()

        self.value = value
        self.unit = target

    @classmethod
    def from_timedelta(cls, value: timedelta) -> Self:
        return cls(value=value.total_seconds(), unit=SampleRateUnit.SECOND)

    # @model_serializer
    # def ser_model(self) -> timedelta:
    #     return self.to_timedelta()
