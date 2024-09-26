import logging
import multiprocessing as mp
from functools import partial
from pathlib import Path
from typing import Any, Callable

from ..logger import generate_collection_extra

# from ..settings import settings
from ..structure import Collection, Subject

logger = logging.getLogger("labda")


def parse_file(
    file: Path | str,
    parser: Callable,
    extra: dict[str, Any],
    collection_id: str,
    **kwargs,
) -> Subject | None:
    try:
        sbj = parser(file, collection_id=collection_id, **kwargs)
        return sbj

    except Exception as e:
        logger.error(f'Error parsing "{file}". {e}', extra=extra)


def bulk_parser(
    folder: Path | str,
    parser: Callable,
    collection_id: str | None = None,
    **kwargs,
) -> Collection:
    # n_cores = settings.n_cores
    n_cores = mp.cpu_count()

    if isinstance(folder, str):
        folder = Path(folder)

    if not folder.is_dir():
        raise ValueError(f'"{folder}" is not a valid folder or does not exist.')

    files = list(folder.glob("*"))

    if not files:
        raise ValueError(f'"{folder}" is empty.')

    if collection_id is None:
        collection_id = f"{folder.name}[temporary name]"

    collection = Collection(id=collection_id)
    extra = generate_collection_extra(collection, "structure", "parsers", "bulk_parser")

    with mp.Pool(n_cores) as pool:
        results = pool.map(
            partial(
                parse_file,
                parser=parser,
                extra=extra,
                collection_id=collection_id,
                **kwargs,
            ),
            files,
        )

    collection.subjects = [result for result in results if result is not None]

    if len(files) == len(collection.subjects):
        level = logging.INFO
    else:
        level = logging.WARNING

    logger.log(
        level,
        f'Parsed {len(collection.subjects)} out of {len(files)} files from "{folder}".',
        extra=extra,
    )

    return collection
