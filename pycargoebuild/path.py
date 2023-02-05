import abc
import typing

from pathlib import Path


class PathWrapperBase(abc.ABC):
    """Base class for opening files in Path/tarfile instances"""

    @abc.abstractmethod
    def open(self, subpath: str) -> typing.BinaryIO:
        """Open specified file for reading in binary mode"""

    @abc.abstractmethod
    def find_in_parents_and_open(self, filename: str) -> typing.BinaryIO:
        """Try to open specified file in directory or its parents"""


class PathWrapper(PathWrapperBase):
    """PathWrapperBase implementation for pathlib.Path"""

    def __init__(self, basedir: Path) -> None:
        self.basedir = basedir

    def open(self, subpath: str) -> typing.BinaryIO:
        return open(self.basedir / subpath, "rb")

    def iterate_parents(self) -> typing.Generator[Path, None, None]:
        directory = self.basedir
        root = directory.absolute().root
        yield directory
        while not directory.samefile(root):
            directory /= ".."
            yield directory

    def find_in_parents_and_open(self, filename: str) -> typing.BinaryIO:
        err: typing.Optional[Exception] = None
        for directory in self.iterate_parents():
            try:
                return open(directory / filename, "rb")
            except FileNotFoundError as e:
                if err is None:
                    err = e
        assert err is not None
        raise err
