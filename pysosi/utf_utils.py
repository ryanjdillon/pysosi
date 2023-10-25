import io
import os
from chardet import detect
from codecs import BOM_UTF8
from pathlib import Path
from typing import BinaryIO, Union


def utf_open(fp: Union[str, Path]) -> BinaryIO:
    """
    Read utf encoded files
    """

    with Path(fp).open("rb") as fh:
        raw = fh.read(min(32, os.path.getsize(fp)))

    return io.open(
        fp,
        "r",
        encoding="utf-8-sig" if raw.startswith(BOM_UTF8) else detect(raw)["encoding"],
    )
