from enum import StrEnum

import pandera as pr


class Column(StrEnum):
    SUBJECT_ID = "subject_id"
    START = "start"
    END = "end"


SCHEMA = pr.DataFrameSchema(
    columns={
        Column.SUBJECT_ID: pr.Column(
            dtype="string",
            required=True,
            nullable=True,
        ),
        Column.START: pr.Column(
            dtype="datetime64[ns]",
            required=False,
            nullable=True,
        ),
        Column.END: pr.Column(
            dtype="datetime64[ns]",
            required=False,
            nullable=True,
        ),
    },
    coerce=True,
    strict=False,
)
