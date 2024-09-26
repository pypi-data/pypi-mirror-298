from typing import Any

from pydantic import BaseModel

from .validation import Placement, Vendor


class Sensor(BaseModel):
    id: str
    serial_number: str | None = None
    model: str | None = None
    vendor: Vendor | None = None
    firmware_version: str | None = None
    placement: Placement | None = None
    extra: dict[str, Any] | None = None

    class Config:
        coerce_numbers_to_str = True
        validate_assignment = True

    def __repr__(self):
        return f"Sensor(id={self.id}, serial_number={self.serial_number}, model={self.model}, vendor={self.vendor}, firmware_version={self.firmware_version}, placement={self.placement}, extra={self.extra})"
