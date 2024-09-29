"""Provides class Dictionary for convenient access to SuŠi dictionaries."""

from pathlib import Path
from typing import Literal, TypedDict
from urllib.request import urlretrieve

from platformdirs import user_cache_path


class _Mapping(TypedDict):
    PM: str
    PM_a: str
    S: str
    S_a: str
    ZT: str
    ZT_a: str


class _DictMeta(type):
    def __getitem__(cls, item: Literal["PM", "PM_a", "S", "S_a", "ZT", "ZT_a"]) -> Path:
        p = cls.download_dir / cls.file_mapping[item]
        if not p.is_file():
            cls.download_file(cls.file_mapping[item])
        return p


class Dictionary(metaclass=_DictMeta):
    """Class for quick access to SuŠi dictionaries.

    If the wanted dictionary is not downloaded, it automatically downloads it and saves it
    for later use.

    **Usage**::

        location = Dictionary["PM_a"]   # returns the path to file with podstatne mena in ascii format
        f = open(location, "r", format="utf-8")     # opens the file

    Valid strings to type into Dictionary[] are:

    - ``"PM"`` => "podstatne_mena.txt",
    - ``"PM_a"`` => "podstatne_mena_ascii.txt",
    - ``"S"`` => "slovnik.txt",
    - ``"S_a"`` => "slovnik-ascii.txt",
    - ``"ZT"`` => "zakladne_tvary.txt",
    - ``"ZT_a"`` => "zakladne_tvary_ascii.txt",
    """

    host_url = (
        "https://raw.githubusercontent.com/olilag/susi-lib/refs/heads/master/assets/"
    )
    download_dir = user_cache_path("susi-lib", False, ensure_exists=True)
    file_mapping: _Mapping = {
        "PM": "podstatne_mena.txt",
        "PM_a": "podstatne_mena_ascii.txt",
        "S": "slovnik.txt",
        "S_a": "slovnik-ascii.txt",
        "ZT": "zakladne_tvary.txt",
        "ZT_a": "zakladne_tvary_ascii.txt",
    }

    @classmethod
    def download_file(cls, name: str) -> None:
        urlretrieve(cls.host_url + name, cls.download_dir / name)
