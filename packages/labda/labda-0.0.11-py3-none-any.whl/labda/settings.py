import logging
import multiprocessing as mp
from typing import Tuple, Type

from pydantic import Field, HttpUrl, field_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
)

logger = logging.getLogger("labda")


class Package(BaseSettings):
    name: str
    version: str
    description: str
    authors: list[str]
    maintainers: list[str]

    license: str
    homepage: HttpUrl
    repository: HttpUrl
    documentation: HttpUrl

    keywords: list[str]

    model_config = SettingsConfigDict(
        pyproject_toml_depth=2,
        pyproject_toml_table_header=("tool", "poetry"),
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (PyprojectTomlConfigSettingsSource(settings_cls),)


class Logger(BaseSettings):
    level: str = "INFO"
    logging: bool = True

    class Config:
        validate_assignment = True

    @field_validator("level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        if v not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(f"Invalid log level: {v}.")

        logger.setLevel(v)

        return v

    @field_validator("logging")
    @classmethod
    def validate_logging(cls, v: bool) -> bool:
        logger.disabled = not v

        return v


class Settings(BaseSettings):
    n_cores: int = Field(default=mp.cpu_count())
    logger: Logger = Logger()

    class Config:
        validate_assignment = True

    @field_validator("n_cores")
    @classmethod
    def validate_n_cores(cls, v: int | str) -> int:
        max_cores = mp.cpu_count()

        if isinstance(v, str) and v == "max":
            v = max_cores
        elif isinstance(v, int) and v > max_cores:
            raise ValueError(f"Maximum number of cores is {max_cores}. Received {v}.")
        elif not isinstance(v, int):
            raise ValueError(f"Invalid value for n_cores: {v}.")

        return v


info = Package()  # type: ignore
settings = Settings()
