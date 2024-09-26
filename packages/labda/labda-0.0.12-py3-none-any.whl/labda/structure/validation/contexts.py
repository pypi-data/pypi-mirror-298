from enum import StrEnum

import pandera as pr


class Column(StrEnum):
    SUBJECT_ID = "subject_id"
    CONTEXT = "context"
    PRIORITY = "priority"
    START = "start"
    END = "end"
    GEOMETRY = "geometry"


SCHEMA = pr.DataFrameSchema(
    columns={
        Column.SUBJECT_ID: pr.Column(
            dtype="string",
            required=False,
            nullable=True,
        ),
        Column.CONTEXT: pr.Column(
            dtype="string",
            required=True,
            nullable=False,
        ),
        Column.PRIORITY: pr.Column(
            dtype="UInt16",
            required=False,
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
        Column.GEOMETRY: pr.Column(
            dtype="geometry",
            required=False,
            nullable=True,
        ),
    },
    coerce=True,
    strict=False,
)
