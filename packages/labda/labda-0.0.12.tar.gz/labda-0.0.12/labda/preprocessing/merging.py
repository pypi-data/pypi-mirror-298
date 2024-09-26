import logging
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

from pyproj import CRS

from ..logger import generate_collection_extra, generate_subject_extra

if TYPE_CHECKING:
    from ..structure import Collection, Subject

logger = logging.getLogger("labda")


def _check_ids(left: "Subject", right: "Subject") -> None:
    if left.id != right.id:
        raise ValueError(f"IDs do not match (left: {left.id}, right: {right.id}).")


def _check_sampling_frequency(left: "Subject", right: "Subject") -> None:
    if left.metadata.sample_rate != right.metadata.sample_rate:
        raise ValueError(
            f"Sample rate do not match (left: {left.metadata.sample_rate}, right: {right.metadata.sample_rate})."
        )


def _check_timezones(
    left: "Subject", right: "Subject", extra: dict[str, str]
) -> None | ZoneInfo:
    if not left.metadata.timezone or not right.metadata.timezone:
        logger.warning(
            f"Timezone information is missing in one or both subjects (left: {left.metadata.timezone}, right: {right.metadata.timezone}). Therefore it could lead to incorrect results.",
            extra=extra,
        )
    elif left.metadata.timezone != right.metadata.timezone:
        raise ValueError(
            f"Timezone do not match (left: {left.metadata.timezone}, right: {right.metadata.timezone})."
        )

    return left.metadata.timezone or right.metadata.timezone


def _check_crs(left: "Subject", right: "Subject", extra: dict[str, str]) -> None | CRS:
    if not left.metadata.crs or not right.metadata.crs:
        logger.warning(
            f"CRS information is missing in one or both subjects (left: {left.metadata.crs}, right: {right.metadata.crs}). Therefore it could lead to incorrect results.",
            extra=extra,
        )
    elif left.metadata.crs != right.metadata.crs:
        raise ValueError(
            f"CRS do not match (left: {left.metadata.crs}, right: {right.metadata.crs})."
        )

    return left.metadata.crs or right.metadata.crs


def _check_duplicate_cols(left: "Subject", right: "Subject") -> None:
    duplicate_cols = set(left.df.columns) & set(right.df.columns)
    if duplicate_cols:
        raise ValueError(f"Before merging, remove duplicate columns: {duplicate_cols}.")


def merge_subjects(
    left: "Subject",
    right: "Subject",
    how: str = "inner",
) -> "Subject":
    extra = generate_subject_extra(left, "preprocessing", "subject", "merge")

    _check_ids(left, right)
    _check_sampling_frequency(left, right)
    timezone = _check_timezones(left, right, extra)
    crs = _check_crs(left, right, extra)

    _check_duplicate_cols(left, right)

    left.df = left.df.merge(
        right.df,
        how=how,  # type: ignore
        left_index=True,
        right_index=True,
        suffixes=(False, False),  # type: ignore # Error if columns overlap. # TODO: Multisensor support, add suffixes.
        validate="one_to_one",
    )
    left.metadata.timezone = timezone
    left.metadata.crs = crs

    if left.df.empty:
        raise ValueError("Merging resulted in an empty DataFrame.")

    return left


def _get_subjects(collection: "Collection") -> list[str]:
    return [subject.id for subject in collection.subjects]


def merge_collections(
    left: "Collection",
    right: "Collection",
    how: str = "inner",
) -> tuple["Collection", int]:
    extra = generate_collection_extra(left, "preprocessing", "collection", "merge")

    left_ids = _get_subjects(left)
    right_ids = _get_subjects(right)
    subjects = set(left_ids + right_ids)

    failed = 0

    for subject in subjects:
        try:
            left_subject = left.get_subject(subject)
            right_subject = right.get_subject(subject)
            left_subject.merge(right_subject, how=how)
        except Exception as e:
            extra = generate_subject_extra(
                left_subject, "preprocessing", "subject", "merge"
            )
            logger.error(e, extra=extra)
            failed += 1

    return left, failed
