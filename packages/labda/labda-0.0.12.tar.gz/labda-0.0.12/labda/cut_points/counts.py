from typing import Any

from ..structure.validation import Column, Placement, SampleRateUnit

COUNTS_CUT_POINTS: dict[str, Any] = {
    "freedson_adult_1998": {
        "name": "Freedson Adult (1998)",
        "reference": "https://journals.lww.com/acsm-msse/fulltext/1998/05000/calibration_of_the_computer_science_and.21.aspx",
        "sample_rate": {"value": 60, "unit": SampleRateUnit.SECOND},
        "category": "adult",
        "placement": Placement.HIP,
        "required_data": Column.COUNTS_X,
        "cut_points": [
            {"name": "sedentary", "max": 99},
            {"name": "light", "max": 1951},
            {"name": "moderate", "max": 5724},
            {"name": "vigorous", "max": 9498},
            {"name": "very vigorous", "max": float("inf")},
        ],
    },
    "freedson_adult_vm3_2011": {
        "name": "Freedson Adult VM3 (2011)",
        "reference": "https://doi.org/10.1016/j.jsams.2011.04.003",
        "sample_rate": {"value": 60, "unit": SampleRateUnit.SECOND},
        "category": "adult",
        "placement": Placement.HIP,
        "required_data": Column.COUNTS_VM,
        "cut_points": [
            {"name": "light", "max": 2689},
            {"name": "moderate", "max": 6166},
            {"name": "vigorous", "max": 9642},
            {"name": "very vigorous", "max": float("inf")},
        ],
    },
    "evenson_children_2018": {
        "name": "Evenson Children (2008)",
        "reference": "https://doi.org/10.1080/02640410802334196",
        "sample_rate": {"value": 15, "unit": SampleRateUnit.SECOND},
        "category": "children",
        "placement": Placement.HIP,
        "required_data": Column.COUNTS_VM,
        "cut_points": [
            {"name": "sedentary", "max": 25},
            {"name": "light", "max": 573},
            {"name": "moderate", "max": 1002},
            {"name": "vigorous", "max": float("inf")},
        ],
    },
}
