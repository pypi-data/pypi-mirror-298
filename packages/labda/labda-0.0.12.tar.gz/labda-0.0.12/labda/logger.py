import logging
import logging.config
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .structure import Collection, Subject

CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(white)s%(asctime)s%(reset)s | %(log_color)s%(levelname)s%(reset)s | %(bold)s%(category)s%(reset)s:%(subcategory)s:%(function)s | %(purple)s%(collection)s:%(subject)s%(reset)s | %(log_color)s%(message)s%(reset)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": """
                    asctime: %(asctime)s
                    levelname: %(levelname)s
                    category: %(category)s
                    subcategory: %(subcategory)s
                    function: %(function)s
                    collection: %(collection)s
                    subject: %(subject)s
                    message: %(message)s
                """,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "formatter": "console",
            "class": "colorlog.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "json": {
            "formatter": "json",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "labda": {
            "level": "INFO",
            "handlers": ["console"],
        },
    },
}


def generate_extra(
    obj: Any | None,
    type: str,
    category: str,
    subcategory: str,
    function: str,
) -> dict:
    match type:
        case "subject":
            subject = obj.id  # type: ignore
            collection = obj.collection  # type: ignore

        case "collection":
            subject = None
            collection = obj.id  # type: ignore
        case "other":
            subject = None
            collection = None

    return {
        "category": category,
        "subcategory": subcategory,
        "function": function,
        "collection": collection,
        "subject": subject,
    }


# TODO: Change it to generate_extra
def generate_subject_extra(
    subject: "Subject",
    category: str,
    subcategory: str,
    function: str,
):
    return {
        "category": category,
        "subcategory": subcategory,
        "function": function,
        "collection": subject.collection,
        "subject": subject.id,
    }


# TODO: Change it to generate_extra
def generate_collection_extra(
    collection: "Collection",
    category: str,
    subcategory: str,
    function: str,
):
    return {
        "category": category,
        "subcategory": subcategory,
        "function": function,
        "collection": collection.id,
        "subject": None,
    }


def object_parsed(
    subject: "Subject",
    origin: str,
    vendor: str,
    function: str,
) -> None:
    logger = logging.getLogger("labda")

    n_records = len(subject.df)
    sample_rate = subject.metadata.sample_rate
    timezone = subject.metadata.timezone
    crs = subject.metadata.crs

    logger.info(
        f'Parsed {n_records:,} records from "{origin}" ({vendor}). Details: SR={sample_rate}, TZ={timezone}, CRS={crs}.',
        extra=generate_subject_extra(
            subject,
            "structure",
            "parsers",
            f"{vendor.lower()}.{function}",
        ),
    )
