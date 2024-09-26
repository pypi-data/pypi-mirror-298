import logging.config

from .logger import CONFIG
from .settings import info, settings
from .structure import (
    Collection,
    Contexts,
    Linkage,
    Metadata,
    Placement,
    SampleRate,
    Sensor,
    Subject,
    Vendor,
)

logging.config.dictConfig(CONFIG)
