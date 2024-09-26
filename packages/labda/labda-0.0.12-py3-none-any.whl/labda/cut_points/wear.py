from datetime import timedelta
from typing import Any

from ..structure.validation import Column, Placement, SampleRateUnit

WEAR_CUT_POINTS: dict[str, Any] = {
    "troiano_2007": {
        "name": "Troiano (2007)",
        "reference": " https://doi.org/10.1249/mss.0b013e31815a51b3",
        "sample_rate": {"value": 60, "unit": SampleRateUnit.SECOND},
        "category": ["children", "adolescents", "adults"],
        "placement": Placement.HIP,
        "required_data": Column.COUNTS_VM,  # Originally developed for a uniaxial accelerometer but can be extended to work on triaxial accelerometers by calculating the VM.
        "params": {
            "bout_min_duration": timedelta(minutes=60),
            "bout_min_value": 0,
            "bout_max_value": 0,
            "artefact_max_duration": timedelta(minutes=2),
            "artefact_between_duration": None,
            "artefact_min_value": 0,
            "artefact_max_value": 100,
        },
    },
    "choi_2011": {
        "name": "Choi (2011)",
        "reference": "https://doi.org/10.1249/MSS.0b013e318258cb36",
        "sample_rate": {"value": 60, "unit": SampleRateUnit.SECOND},
        "category": ["children", "adolescents", "adults"],
        "placement": Placement.HIP,
        "required_data": Column.COUNTS_VM,  # Originally developed for a uniaxial accelerometer but can be extended to work on triaxial accelerometers by calculating the VM.
        "params": {
            "bout_min_duration": timedelta(minutes=90),
            "bout_min_value": 0,
            "bout_max_value": 0,
            "artefact_max_duration": timedelta(minutes=2),
            "artefact_between_duration": timedelta(minutes=30),
            "artefact_min_value": 0,
            "artefact_max_value": 0,
        },
    },
}
