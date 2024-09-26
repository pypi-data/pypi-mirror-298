from typing import Any

from ..structure.validation import Column

TRANSPORTATION_CUT_POINTS: dict[str, Any] = {
    "carlson_palms_2015": {
        "name": "Carlson PALMS Validation (2015)",
        "reference": "https://doi.org/10.1249/MSS.0000000000000446",
        "required_data": Column.SPEED,
        "units": "kph",
        "cut_points": [
            {"name": "walk/run", "max": 9},
            {"name": "bicycle", "max": 35},
            {"name": "vehicle", "max": float("inf")},
        ],
    },
    "heidler_palms_2024": {
        "name": "Heidler PALMS Validation (2024)",
        "reference": None,
        "required_data": Column.SPEED,
        "units": "kph",
        "cut_points": [
            {"name": "walk/run", "max": 7},
            {"name": "bicycle", "max": 35},
            {"name": "vehicle", "max": float("inf")},
        ],
    },
}
