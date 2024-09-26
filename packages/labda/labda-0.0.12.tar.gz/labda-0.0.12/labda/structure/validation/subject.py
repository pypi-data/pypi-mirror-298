from enum import StrEnum

import pandera as pr


class SampleRateUnit(StrEnum):
    HERTZ = "hz"
    SECOND = "s"


class Vendor(StrEnum):
    ACTIGRAPH = "ActiGraph"
    AXIVITY = "Axivity"
    QSTARZ = "Qstarz"
    SENS = "Sens"
    TRACCAR = "Traccar"


class Placement(StrEnum):
    THIGH = "thigh"
    HIP = "hip"
    WRIST = "wrist"
    MOBILE = "mobile"


class Column(StrEnum):
    # --- Base ---
    SUBJECT_ID = "subject_id"
    DATETIME = "datetime"
    TIMEDELTA = "timedelta"
    WEAR = "wear"

    # --- Accelerometry ---
    ACC_X = "acc_x"
    ACC_Y = "acc_y"
    ACC_Z = "acc_z"
    ACC_VM = "acc_vm"

    # --- Counts ---
    COUNTS_X = "counts_x"
    COUNTS_Y = "counts_y"
    COUNTS_Z = "counts_z"
    COUNTS_VM = "counts_vm"

    # --- Taxonomy ---
    MOVEMENT = "movement"
    ACTION = "action"
    ACTIVITY = "activity"

    # --- Other ---
    ACTIVITY_INTENSITY = "activity_intensity"
    ACTIVITY_VALUE = "activity_value"
    STEPS = "steps"
    HEART_RATE = "heart_rate"
    TEMPERATURE = "temperature"
    LUX = "lux"

    # --- Spatial ---
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    GNSS_ACCURACY = "gnss_accuracy"
    NSAT_VIEWED = "nsat_viewed"
    NSAT_USED = "nsat_used"
    NSAT_RATIO = "nsat_ratio"
    SNR_VIEWED = "snr_viewed"
    SNR_USED = "snr_used"
    PDOP = "pdop"
    HDOP = "hdop"
    VDOP = "vdop"
    DISTANCE = "distance"
    ELEVATION = "elevation"
    SPEED = "speed"
    ACCELERATION = "acceleration"
    DIRECTION = "direction"
    ENVIRONMENT = "environment"

    # --- Trips and Contexts ---
    SEGMENT_ID = "segment_id"
    TRIP_ID = "trip_id"
    TRIP_STATUS = "trip_status"
    TRIP_MODE = "trip_mode"
    STATIONARY_ID = "stationary_id"
    CONTEXT = "context"


SCHEMA = pr.DataFrameSchema(
    index=pr.Index(
        name=Column.DATETIME,
        dtype="datetime64[ns]",
    ),
    columns={
        # --- Base ---
        Column.SUBJECT_ID: pr.Column(
            dtype="string",
            required=False,
            nullable=False,
        ),
        Column.TIMEDELTA: pr.Column(
            dtype="timedelta",
            required=False,
            nullable=True,
        ),
        Column.WEAR: pr.Column(
            dtype="boolean",
            required=False,
            nullable=True,
        ),
        # --- Accelerometry ---
        Column.ACC_X: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.ACC_Y: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.ACC_Z: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.ACC_VM: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        # --- Counts ---
        Column.COUNTS_X: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.COUNTS_Y: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.COUNTS_Z: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.COUNTS_VM: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        # --- Taxonomy ---
        Column.MOVEMENT: pr.Column(
            dtype="string",
            required=False,
            nullable=True,
        ),  # TODO: Add categories (Bodily movement defined by anatomy and biomechanics)
        Column.ACTION: pr.Column(
            dtype="string",
            required=False,
            nullable=True,
            checks=[
                pr.Check(
                    lambda s: s.isin(
                        [
                            "lying",
                            "lying-sitting",  # Extra class from Sens
                            "reclining",
                            "sitting",
                            "standing",
                            "kneeling",
                            "shuffling",
                            "walking",
                            "ascending (stairs)",
                            "descending (stairs)",
                            "crawling",
                            "dancing",
                            "jumping",
                            "running",
                            "diving",
                            "cycling",
                            "swimming",
                            "climbing",
                            "gliding (skates, skis)",
                            "lying down",
                            "reclining up",
                            "reclining down",
                            "sitting up",
                            "sitting down",
                            "standing up",
                            "turning left",
                            "turning right",
                            "kneeling down",
                        ]
                    ),
                )
            ],
        ),
        Column.ACTIVITY: pr.Column(
            dtype="string",
            required=False,
            nullable=True,
        ),  # TODO: Add categories (HETUS)
        # --- Other ---
        Column.ACTIVITY_INTENSITY: pr.Column(
            dtype="category",
            required=False,
            nullable=True,
            checks=[
                pr.Check(
                    lambda s: s.isin(
                        [
                            "sedentary",
                            "light",
                            "moderate",
                            "moderate-vigorous",
                            "vigorous",
                            "very vigorous",
                        ]
                    ),
                )
            ],
        ),
        Column.ACTIVITY_VALUE: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.STEPS: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.HEART_RATE: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.TEMPERATURE: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.LUX: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        # --- Spatial ---
        Column.LATITUDE: pr.Column(
            dtype="Float64",
            required=False,
            nullable=True,
        ),
        Column.LONGITUDE: pr.Column(
            dtype="Float64",
            required=False,
            nullable=True,
        ),
        Column.GNSS_ACCURACY: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.NSAT_VIEWED: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.NSAT_USED: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.NSAT_RATIO: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.SNR_VIEWED: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.SNR_USED: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.PDOP: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.HDOP: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.VDOP: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.DISTANCE: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.ELEVATION: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.SPEED: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.ACCELERATION: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.DIRECTION: pr.Column(
            dtype="Float32",
            required=False,
            nullable=True,
        ),
        Column.ENVIRONMENT: pr.Column(
            dtype="category",
            required=False,
            nullable=True,
            checks=[
                pr.Check(
                    lambda s: s.isin(
                        [
                            "indoor",
                            "outdoor",
                            "mixed",
                        ]
                    ),
                )
            ],
        ),
        # --- Trips and Contexts ---
        Column.SEGMENT_ID: pr.Column(
            dtype="UInt16",
            required=False,
            nullable=True,
        ),
        Column.TRIP_STATUS: pr.Column(
            dtype="category",
            required=False,
            nullable=True,
            checks=[
                pr.Check(
                    lambda s: s.isin(
                        [
                            "start",
                            "end",
                            "start-end",
                            "transport",
                            "pause",
                            "stationary",
                        ]
                    ),
                )
            ],
        ),
        Column.TRIP_ID: pr.Column(
            dtype="UInt16",
            required=False,
            nullable=True,
        ),
        Column.STATIONARY_ID: pr.Column(
            dtype="UInt16",
            required=False,
            nullable=True,
        ),
        Column.TRIP_MODE: pr.Column(
            dtype="category",
            required=False,
            nullable=True,
            checks=[
                pr.Check(
                    lambda s: s.isin(
                        [
                            "walk",
                            "run",
                            "walk/run",
                            "bicycle",
                            "vehicle",
                            "public transport",
                            "train",
                        ]
                    ),
                )
            ],
        ),
        Column.CONTEXT: pr.Column(
            dtype="category",
            required=False,
            nullable=True,
        ),
    },
    coerce=True,
    strict=False,
)
